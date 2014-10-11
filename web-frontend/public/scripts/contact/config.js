'use strict';
angular.module('app.contact', [])

.config(['$routeProvider', function($routeProvider) {
      return $routeProvider
            .when('/contacto', { 
		templateUrl: 'scripts/contact/views/form.html',
	        authenticate: true
	    })
}]);
