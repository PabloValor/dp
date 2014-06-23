'use strict';
angular.module('app.games', [])

.config(['$routeProvider', function($routeProvider) {
      return $routeProvider.when('/games', {
        templateUrl: 'scripts/games/views/all.html'
      })
}])
