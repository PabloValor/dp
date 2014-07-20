'use strict';
angular.module('app.games', [])

.config(['$routeProvider', function($routeProvider) {
      return $routeProvider
            .when('/games', { templateUrl: 'scripts/games/views/all.html' })
            .when('/torneos', { templateUrl: 'scripts/games/views/all.html' })

            .when('/games/create', { templateUrl: 'scripts/games/views/all.html' })
            .when('/torneos/nuevo', { templateUrl: 'scripts/games/views/new.html' })
}])
