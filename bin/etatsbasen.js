#!/usr/bin/env node
'use strict';
var path = require('path');
var fs = require('fs');
var pkg = require(path.join(__dirname, '..', 'package.json'));

var argv = require('minimist')(process.argv.slice(2));
var etatsbasen = require('etatsbasen');

process.bin = process.title = 'etatsbasen';

if (argv.v) {
  console.log(pkg.version);
  process.exit();
}

var options = {};
options.filename = argv.f || 'etatsbasen.csv';

if (argv.c && 'string' === typeof argv.c) {
  options.categories = argv.c.split(',');
} else {
  options.categories = [];
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
    '  -c [c1,c2,..]   Categories to include',
    '  -f [file]       File to read from (defaults: `etatsbasen.csv`)',
    '  -v              Print version.',
    '  -h              Write this help.'
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
