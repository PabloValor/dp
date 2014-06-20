'use strict';
angular.module('app.users', []).config(['$routeProvider', function($routeProvider) {
      return $routeProvider.when('/signin', {
        templateUrl: 'scripts/users/views/signin.html'
      })
}]);



