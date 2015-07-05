#! /usr/bin/env python3
import argparse
import sys
import os
from email.utils import parseaddr
import csv 
import re

VERSION="python-etatsbasen-v0.1"
DEFAULT_CATEGORIES = [12,14,17,18,27,33,38,66,68,76]
DEFAULT_FILENAME = "etatsbasen-small.csv" # "etatsbasen.csv"

DEFAULT_COLUMNS = ["url_nb","url_en","kommunenummer","orgid","orgstructid","parentid"];

RENAME_HEADERS = {
    'tailid': 'id',
    'email': 'request_email',
    'name_nb': 'name',
    'name_nn': 'name.nn',
    'name_en': 'name.en'
  };

def fatal(msg):
    print(msg, file=sys.stderr)
    sys.exit(0)

def cleanup_email(string):
    fix1 = re.sub(r"^mailto:?", "", string)
    if fix1 == valid_email(fix1):
        return fix1
    # Split on ' ?[,/] ?'
    split = re.split(r' ?[,/] ?', string)
    for fix2 in split:
        if fix2 == valid_email(fix2):
            return fix2
    fix3 = re.sub(r"\.$", "", string)
    if fix3 == valid_email(fix3):
        return fix3
    return False

def valid_email(string):
    if re.match(r"^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$", string):
        return string

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

def trim_row(row):
    if row == None:
        return None
    trimmed_row = {}
    for key in row:
        trimmed_row[key] = row[key].strip()
    return trimmed_row


def add_tags(row):
    if row == None:
        return None
    return row

def add_url(row):
    if row == None:
        return None
    if row["url_nb"].strip() != "":
        row["home_page"] = row["url_nb"]
    elif row ["url_en"].strip() != "":
        row["home_page"] = row["url_en"]
    else:
        row["home_page"] = ""
    return row

def printCSV(options):
    with open(options["inputfile"], "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"', strict=True)
        filtered_rows = []
        header = reader.fieldnames
        for row in reader:
            row = filter_orgstructid(row, options["categories"])
            row = filter_email(row)
            row = renameHeader(row)
            row = trim_row(row)
            row = add_tags(row)
            row = add_url(row)
            row = filter_column(row, options["headers"])
            
            if row != None:
                filtered_rows.append(row)
    writer = csv.DictWriter(sys.stdout, delimiter=',', quotechar='"', lineterminator="\n", quoting=csv.QUOTE_MINIMAL, fieldnames=options["headers"], extrasaction='raise')
    #writer.writeheader()
    print("#%s" % (",".join(options["headers"])))
    for row in filtered_rows:
        writer.writerow(row)
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tool for exporting etatsbasen-data to a file that can be imported into alaveteli.')
    parser.add_argument('-c', action='append', metavar="all | -c 12 -c 14 -c ...", help="Categories to include (default: \"%s\")" % ("all"))
    parser.add_argument('-f', metavar="file", default=DEFAULT_FILENAME, help="File to read from (default: \"%s\")" % (DEFAULT_FILENAME))
    #parser.add_argument('-o', action='append', metavar="-o headerName1 [-o headername2 ...] ", help="(i don't really work) ... Include only these headers/columns in output (post-rename)(default: \"%s\")" % (DEFAULT_COLUMNS))
    parser.add_argument('-u', action='append', metavar="headerName1 -u ...", help="Columns and order of columns to output (default: %s)" % (",".join(DEFAULT_COLUMNS)))
    parser.add_argument('-v', help="Print version (%s) and exit" % (VERSION), action='store_true')
    args = parser.parse_args()
    options = {}
    
    if args.v:
        print("version: %s" % (VERSION))
        sys.exit(0)
    
    if os.path.isfile(args.f):
        options["inputfile"] =  args.f
    else:
        fatal("%s: No such file" % (args.f))

    if args.u:
        options["headers"] = args.u
    else:
        options["headers"] = DEFAULT_COLUMNS

    if args.c:
        try:
            if args.c[0] == "all":
                if len(args.c) == 1:
                    options["categories"] = ["all"]
                else:
                    fatal("Failed to parse \"-c %s\"; Categories must be integers or only \"-c all\"" % (" -c ".join(args.c)))
            else:
                options["categories"] = [ int(x) for x in args.c ]
        except ValueError as ve:
            print("Failed to parse \"-c %s\"; Categories must be integers or only \"-c all\"" % (" -c ".join(args.c)))
    else:
        options["categories"] = ["all"] #DEFAULT_CATEGORIES

    printCSV(options)
