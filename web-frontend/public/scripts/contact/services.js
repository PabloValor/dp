'use strict';
angular.module('app.contact')

.factory('ContactService', ['$http', 'SETTINGS',
    function($http, SETTINGS) {
      return {
          new: function(email, subject, text) {
	    var data = { 'email': email,
		         'subject': subject,
		         'text': text };

            $http.post(SETTINGS.url.contactNew(), data);
          }
      }
    }
]);
