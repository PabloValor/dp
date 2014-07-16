'use strict';
angular.module('app.home', [])

.config(['$routeProvider', function($routeProvider) {
      return $routeProvider.when('/', {
        redirectTo: '/dashboard'
      }).when('/dashboard', {
        authenticate: true,
        templateUrl: 'scripts/home/views/dashboard.html'
      });
}])




