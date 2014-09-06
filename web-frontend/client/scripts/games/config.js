'use strict';
angular.module('app.games', [])

.config(['$routeProvider', function($routeProvider) {
      return $routeProvider
            .when('/games', { templateUrl: 'scripts/games/views/all.html' })
            .when('/torneos', { templateUrl: 'scripts/games/views/my_games.html' })
            .when('/torneos/buscador', { templateUrl: 'scripts/games/views/all.html' })
            .when('/torneosNuevoOld', { templateUrl: 'scripts/games/views/my_games_old.html' })

            .when('/game/detail/:gameId', { templateUrl: 'scripts/games/views/detail.html' })
            .when('/torneos/detalle/:gameId', { templateUrl: 'scripts/games/views/detail.html' })
            .when('/torneos/detalle/:gameId/tablas', { templateUrl: 'scripts/games/views/tables.html' })

            .when('/games/create', { templateUrl: 'scripts/games/views/all.html' })
            .when('/torneos/nuevo', { templateUrl: 'scripts/games/views/new.html' })
            .when('/torneos/nuevo/avanzado', { templateUrl: 'scripts/games/views/new_advanced.html' })
}])
