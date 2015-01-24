'use strict';
angular.module('app.contact')

.factory('ContactService', ['$http', 'SETTINGS',
    function($http, SETTINGS) {
      return {
          new: function(subject, text) {
	      var data = { 'subject': subject,
		           'text': text };

            $http.post(SETTINGS.url.contactNew(), data);
          }
      }
    }
]);
