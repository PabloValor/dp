'use strict';
angular.module('app.games', [])

.config(['$routeProvider', function($routeProvider) {
      return $routeProvider
            .when('/games', { templateUrl: 'scripts/games/views/all.html', authenticate: true })
            .when('/torneos', { templateUrl: 'scripts/games/views/my_games.html', authenticate: true })
            .when('/torneos/buscador', { templateUrl: 'scripts/games/views/all.html', authenticate: true })
            .when('/torneosNuevoOld', { templateUrl: 'scripts/games/views/my_games_old.html', authenticate: true })

            .when('/game/detail/:gameId', { templateUrl: 'scripts/games/views/detail.html', authenticate: true })
            .when('/torneos/detalle/:gameId', { templateUrl: 'scripts/games/views/detail.html', authenticate: true })
            .when('/torneos/detalle/:gameId/tablas', { templateUrl: 'scripts/games/views/tables.html', authenticate: true })

            .when('/games/create', { templateUrl: 'scripts/games/views/all.html', authenticate: true })
            .when('/torneos/nuevo', { templateUrl: 'scripts/games/views/new.html', authenticate: true })
            .when('/torneos/nuevo/avanzado', { templateUrl: 'scripts/games/views/new_advanced.html', authenticate: true })
}])
