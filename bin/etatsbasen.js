#!/usr/bin/env node
'use strict';
var path = require('path');
var fs = require('fs');
var pkg = require(path.join(__dirname, '..', 'package.json'));

var argv = require('minimist')(process.argv.slice(2));
var etatsbasen = require('etatsbasen');

var defaultCategories = [12,14,17,18,27,33,38,66,68,76];

process.bin = process.title = 'etatsbasen';

if (argv.v) {
  console.log(pkg.version);
  process.exit();
}

var options = {};
options.filename = argv.f || 'etatsbasen.csv';

if (argv.c) {
  if (Array.isArray(argv.c)) {
    options.categories = argv.c;
 } else if ('string' === typeof argv.c) {
   if ('all' !== argv.c) {
     options.categories = [argv.c];
   }
 } else {
   options.categories = defaultCategories;
 }
}

if (argv.o) {
  if (Array.isArray(argv.o)) {
    options.headers = argv.o;
  } else if ('string' === typeof argv.o ||
            'number' === typeof argv.o) {
    options.headers = [argv.o];
  } else {
    console.log('Unable to parse -o option(s)');
    process.exit(1);
  }
}

function fileNotFound() {
  return ! fs.existsSync(options.filename);
}

if (argv.h || fileNotFound()) {
  if (fileNotFound()) {
    console.log(process.title + ': ' + options.filename +
                ': No such file or directory\n');
  }
  console.log([
    'usage: etatsbasen [options]',
    '',
    '  -c [all|[c1,c2,..]]   Categories to include (defaults: `' + defaultCategories.join(',') + '`)',
    '  -f [file]             File to read from (defaults: `etatsbasen.csv`)',
    '  -o h1[,h2,h3]         Include only these headers in output (id or name)',
    '  -v                    Print version.',
    '  -h                    Write this help.'
  ].join('\n'));

  process.exit();
}

var ret = etatsbasen.printCSV(function(err) {
  if (err) {
    throw err;
  }
  }, options);

if (ret) {

} else {
  console.log('Unable to convert');
  process.exit();
}
