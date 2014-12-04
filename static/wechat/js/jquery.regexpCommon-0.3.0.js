/**
 * jquery.regexpCommon.js: Common Regular Expressions - jQuery plugin
 *
 * Copyright (c) 2008 Doug Sparling
 * Dual licensed under the MIT and GPL licenses:
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.gnu.org/licenses/gpl.html
 *
 */

/**
 *
 * Return regular expression
 *
 * @example somestring.match($.regexpCommon('url'));
 *
 * @name $.regexpCommon 
 * @cat Plugins/Utilities
 * @author Doug Sparling/doug.sparling@gmail.com
 * @version 0.3.0
 */
(function($) {
  $.regexpCommon = function(regexpDesc) {
    return $.regexpCommon.regexpPattern[regexpDesc].call();
  };

  $.regexpCommon.regexpPattern = {
    // numbers
    numberInteger : function() {
      return /^[-+]?[1-9]\d*\.?[0]*$/;
    },
    numberFloat : function() {
      return /^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$/;
    },
    // email
    email : function() {
      return /^([0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*@([0-9a-zA-Z][-\w]*[0-9a-zA-Z]\.)+[a-zA-Z]{2,9})$/;
    },
    ssn : function() {
      return /^\d{3}-\d{2}-\d{4}$/;
    },
    url : function() {
      return /^(ht|f)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?$/;
    },
    phoneNumberUS : function() {
      return /^[01]?[- .]?(\([2-9]\d{2}\)|[2-9]\d{2})[- .]?\d{3}[- .]?\d{4}$/;
    },
    zipCodeUS : function() {
      return /^(\d{5}-\d{4}|\d{5}|\d{9})$|^([a-zA-Z]\d[a-zA-Z] \d[a-zA-Z]\d)$/;
    },
    currencyUS : function() {
      return /^\$(\d{1,3}(\,\d{3})*|(\d+))(\.\d{2})?$/;
    }, 
    htmlHexCode : function() {
      return /^#([a-fA-F0-9]){3}(([a-fA-F0-9]){3})?$/;
    },
    dottedQuadIP : function() {
      return /^(\d|[01]?\d\d|2[0-4]\d|25[0-5])\.(\d|[01]?\d\d|2[0-4] \d|25[0-5])\.(\d|[01]?\d\d|2[0-4]\d|25[0-5])\.(\d|[01]?\d\d|2[0-4] \d|25[0-5])$/;
    },
    macAddress : function() {
      return /^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$/;
    },
    phoneNumberZN : function() {
      return /^1\d{10}$/;
    },
    pwd : function() {
      return /^\w{6,16}$/;
    },
    username : function() {
      return /^\w{6,20}$/;
    }
  };
}) (jQuery);
