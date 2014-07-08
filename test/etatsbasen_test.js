'use strict';

var etatsbasen = require('../lib/etatsbasen.js');

/*
  ======== A Handy Little Nodeunit Reference ========
  https://github.com/caolan/nodeunit

  Test methods:
    test.expect(numAssertions)
    test.done()
  Test assertions:
    test.ok(value, [message])
    test.equal(actual, expected, [message])
    test.notEqual(actual, expected, [message])
    test.deepEqual(actual, expected, [message])
    test.notDeepEqual(actual, expected, [message])
    test.strictEqual(actual, expected, [message])
    test.notStrictEqual(actual, expected, [message])
    test.throws(block, [error], [message])
    test.doesNotThrow(block, [error], [message])
    test.ifError(value)
*/

exports.etatsbasen = {
  setUp: function(done) {
    // setup here
    done();
  },
  'printCSV': {
    'non existing file': function(test) {
      test.expect(3);
      etatsbasen.printCSV(function(err) {
        test.ok(err);
        test.notEqual(err, '');
        test.ok(err.match(/^Can\'t find file/));
        test.done();
      }, { filename: 'evilmule.csv' });
    },
    'no error with legal file': function(test) {
      test.expect(1);
      var oldLogger = console.log;
      console.log = function() { };
      etatsbasen.printCSV(function(err) {
        console.log = oldLogger;
        test.equal(err, undefined);
        test.done();
      }, { filename: 'fixtures/1.csv' });
    },
    'filter empty emails': function(test) {
      test.expect(4);
      var oldLogger = console.log;
      console.log = function(str) {
        test.ok(str.match(/^\#id/), 'Doesn\'t start with header');
        test.ok(!str.match(/tailid/, 'Tailid header wasn\'t renamed id'));
        test.ok(!str.match(/\n/), 'Contains more than the header');
      };
      etatsbasen.printCSV(function(err) {
        console.log = oldLogger;
        test.ok(!err);
        test.done();
      }, { filename: 'fixtures/1.csv' });
    },
    'filter categories': function(test) {
      test.expect(4);
      var oldLogger = console.log;
      console.log = function(str) {
        test.equal(str.match(/\,36\,/g).length, 3);
        test.equal(str.match(/\,37\,/g).length, 1);
        test.ok(!str.match(/\,39\,/));
      };
      etatsbasen.printCSV(function(err) {
        console.log = oldLogger;
        test.ok(!err);
        test.done();
      }, { filename: 'fixtures/2.csv', categories: [36,37] });
    },
    'filter headers': function(test) {
      var oldLogger = console.log;
      console.log = function(str) {
        test.expect(5);
        test.ok(str.match(/.*request\_email.*/), 'Can\'t find filtered header email');
        test.equal(str.split('\n').length, 10);
        test.ok(!str.match(/\,\,/), 'Found empty entries (WARNING: suspect test)');
        test.ok(str.match(/.*name\.nn.*/, 'Missing name.nn header'));
      };
      etatsbasen.printCSV(function(err) {
        console.log = oldLogger;
        test.ok(!err);
        test.done();
      }, { filename: 'fixtures/2.csv', headers: ['request_email', 3] });
    }
  }
  };
