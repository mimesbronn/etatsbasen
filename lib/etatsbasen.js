'use strict';
/*
 * etatsbasen
 * user/repo
 *
 * Copyright (c) 2014 gorm
 * Licensed under the MIT license.
 */
var csv = require('csv');
var stringify = require('csv-stringify');
var fs = require('fs');

function emailIsInvalid(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return !re.test(email);
}

function filter(csvdata, includeOrgstructIds) {
  if (! csvdata) {
    throw new TypeError('Missing `data` argument');
  }
  var headernameToIndex = {};

  if (includeOrgstructIds && !Array.isArray(includeOrgstructIds)) {
    throw new TypeError('`includedOrgstructIds` should be an array');
  }

  csvdata = csvdata.filter(function(item, i) {
    // make mapping between headerName to index
    if (0 === i) {
      item.forEach(function(item, i) {
        headernameToIndex[item] = i;
      });
      // always include header
      return true;
    } else {
      var email = item[headernameToIndex.email];
      if (emailIsInvalid(email)) {
        return false;
      }

      return (function() {
        var i;

        if (includeOrgstructIds.length) {
          for (i = 0; i < includeOrgstructIds.length; i++) {
            //console.log(i + " " + includeOrgstructIds[i] + " " +  item[headernameToIndex.orgstructid]);
            if (parseInt(includeOrgstructIds[i]) ===
                parseInt(item[headernameToIndex.orgstructid])) {
              return true;
            }
          }
          return false;
        } else {
          return true;
        }
      }());
    }
  });

  return csvdata;
}

function renameHeader(data) {
  if (! data) {
    throw new TypeError('Missing `data` argument');
  }

  var rename = {
    'tailid': 'id',
    'email': 'request_email',
    'name_nb': 'name',
    'name_nn': 'name.nn_NO',
    'name_en': 'name.en'
  };

  var headers = [];

  data[0].forEach(function(header, i) {
    headers[i] = rename[header] || header;
  });

  data[0] = headers;

  return data;
}

function removeColumns(data) {
  if (! data) {
    throw new TypeError('Missing `data` argument');
  }

  var columns = ['url_nb', 'url_en', 'kommunenummer',
                 'orgid', 'orgstructid', 'parentid'];

  columns.forEach(function(name) {
    var toRemove = -1;
    data.forEach(function(item, i) {
      if (0 === i) {
        toRemove = item.indexOf(name);
      }

      if (toRemove >= 0) {
        item.splice(toRemove, 1);
      }
    });
  });

  return data;
}

function addTags(data) {
  if (! data) {
    throw new TypeError('Missing `data` argument');
  }
  var orgstructidIndex;
  data.forEach(function(item, i) {
    if (0 === i) {
      item.push('tag_string');
      orgstructidIndex = item.indexOf('orgstructid');
    } else {
      item.push(item[orgstructidIndex]);
    }
  });
  return data;
}

function addURL(data) {
  if (! data) {
    throw new TypeError('Missing `data` argument');
  }
  // create new column
  var urlenIndex=0;
  var urlnoIndex=0;

  data.forEach(function(item, i) {
    if (0 === i) {
      item.push('home_page');
      urlenIndex = item.indexOf('url_en');
      urlnoIndex = item.indexOf('url_nb');
    } else {
      item.push(item[urlnoIndex] || item[urlenIndex]);
    }
  });

  return data;
}

function print(data) {
  if (! data) {
    throw new TypeError('Missing `data` argument');
  }
  stringify(data, function(err, output) {
    if (err) {
      console.error(err);
      return false;
    }
    // comment first line
    console.log('#'+output);
  });
}

function lookForDataFile(filename) {
  if (fs.existsSync(filename)) {
    return filename;
  } else {
    return false;
  }
}

/** Will output a CSV with all organizations to stdout */
exports.printCSV = function(cb, options) {
  var filename = lookForDataFile(options.filename);

  if (false === filename) {
    cb('Can\'t find file `' + options.filename + '`');
    return false;
  }

  csv().from.path(filename, { comment: '#'}).to.array( function(data) {
    print(
      removeColumns(
        addURL(
          addTags(
            renameHeader(
              filter(data, options.categories)
            )
          )
        )
      )
    );
    cb();
  } );

  return true;
};
