#! /usr/bin/env python3
import argparse
import sys
import os
from email.utils import parseaddr
import csv 
import re

VERSION="python-etatsbasen-v0.1"
DEFAULT_CATEGORIES = "12,14,17,18,27,33,38,66,68,76"
DEFAULT_FILENAME = "etatsbasen-small.csv" # "etatsbasen.csv"

DEFAULT_COLUMNS = "url_nb,url_en,kommunenummer,orgid,orgstructid,parentid";

RENAME_HEADERS = {
    'tailid': 'id',
    'email': 'request_email',
    'name_nb': 'name',
    'name_nn': 'name.nn',
    'name_en': 'name.en'
  };

def cleanup_email(string):
    fix1 = re.sub(r"^mailto:?", "", string)
    if fix1 == valid_email(fix1):
        return fix1
    # Split on ' ?[,/] ?'
    split = re.split(r' ?[,/] ?', string)
    for fix2 in split:
        if fix2 == valid_email(fix2):
            return fix2
    return False

def valid_email(string):
    # Think about using https://pypi.python.org/pypi/validate_email ?
    name, email = parseaddr(string)
    if (email == string and '@' in email):
        return email


def filter_orgstructid(row, categories):
    if row == None:
        return None
    if len(categories) == 1 and categories[0] == "all":
        return row
    if int(row["orgstructid"]) in categories:
        return row
    else:
        print("Skipping tailid %s: orgstructid not in selected categories (%s not in %s)" % (row['tailid'], row['orgstructid'], categories), file=sys.stderr)
        return None


def filter_email(row):
    if row == None:
        return None
    if row['email'] == "":
        print("Skipping tailid %s: No email specified" % (row['tailid']), file=sys.stderr)
        return None # No email, skip
    elif not valid_email(row['email']):
        fixed = cleanup_email(row['email'])
        if fixed:
            print("Replaced email for tailid %s: \"%s\" -> \"%s\"" % (row['tailid'], row['email'], fixed), file=sys.stderr)
            row['email'] = fixed
        else:
            print("Skipping tailid %s: Invalid email (%s)" % (row['tailid'], row['email']), file=sys.stderr)
            return None # Invalid email, skip
    return row


def renameHeader(row):
    if row == None:
        return None
    renamed_row = {}
    for key in row:
        if key in RENAME_HEADERS:
            renamed_row[RENAME_HEADERS[key]] = row[key]
        else:
            renamed_row[key] = row[key]
    return renamed_row


def filter_column(row, headers):
    if row == None:
        return None
    if len(headers) == 1 and headers[0] == "all":
        return row # We should include all headers, shortcut
    filtered_row = {}
    for key in row:
        if key in headers:
            filtered_row[key] = row[key]
    return filtered_row

def printCSV(options):
    print(options)
    with open(options["inputfile"], newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        filtered_rows = []
        for row in reader:
            row = filter_orgstructid(row, options["categories"])
            row = filter_email(row)
            row = renameHeader(row)
            row = filter_column(row, options["headers"])
            if row != None:
                filtered_rows.append(row)
    print(filtered_rows)
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tool for exporting etatsbasen-data to a file that can be imported into alaveteli.')
    parser.add_argument('-c', metavar="all|c1[,c2,c3,..]", default=DEFAULT_CATEGORIES, help="Categories to include (default: \"%s\")" % (DEFAULT_CATEGORIES))
    parser.add_argument('-f', metavar="file", default=DEFAULT_FILENAME, help="File to read from (default: \"%s\")" % (DEFAULT_FILENAME))
    parser.add_argument('-o', metavar="all|headerName1[,headername2,...] ", default=DEFAULT_COLUMNS, help="Include only these headers/columns in output (post-rename)(default: \"%s\")" % (DEFAULT_COLUMNS))
    parser.add_argument('-v', help="Print version (%s) and exit" % (VERSION), action='store_true')
    args = parser.parse_args()
    
    options = {}
    
    if args.v:
        print("version: %s" % (VERSION))
        sys.exit(0)
    
    if os.path.isfile(args.f):
        options["inputfile"] =  args.f
    else:
        print("%s: No such file" % (args.f), file=sys.stderr)
        sys.exit(0)

    if args.o == "all":
        options["headers"] = ["all"]
    else:
        options["headers"] = args.o.split(',')

    try:
        if args.c == "all":
            options["categories"] = ["all"]
        else:
            options["categories"] = [ int(x) for x in args.c.split(',') ]
    except ValueError as ve:
        print("Failed to parse \"-c %s\"; Categories must comma separated list of only integers" % (args.c), file=sys.stderr)
        sys.exit(0)
    
    printCSV(options)
