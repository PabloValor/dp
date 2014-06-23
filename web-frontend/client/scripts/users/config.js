'use strict';
angular.module('app.users', []).config(['$routeProvider', function($routeProvider) {
      return $routeProvider.when('/signin', {
        templateUrl: 'scripts/users/views/signin.html'
      })
}]);

angular.module('app.users').config(['$httpProvider', function ($httpProvider) {
    $httpProvider.interceptors.push('TokenInterceptor');
}]);


