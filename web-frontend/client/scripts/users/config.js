'use strict';
angular.module('app.users', [])

.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.interceptors.push('TokenInterceptor');
}])

.config(['$routeProvider', function($routeProvider) {
      return $routeProvider.when('/signup', {
        templateUrl: 'scripts/users/views/signup.html'
      })
}])

.config(['$routeProvider', function($routeProvider) {
      return $routeProvider.when('/signin', {
        templateUrl: 'scripts/users/views/signin.html'
      })
}]);



