'use strict';
angular.module('app.friends', [])

.config(['$routeProvider', function($routeProvider) {
      return $routeProvider
            .when('/friends', { templateUrl: 'scripts/friends/views/all.html', authenticate: true })
            .when('/amigos', { templateUrl: 'scripts/friends/views/all.html', authenticate: true })
            .when('/friends/search', { templateUrl: 'scripts/friends/views/search.html', authenticate: true })
            .when('/amigos/buscar', { templateUrl: 'scripts/friends/views/search.html', authenticate: true })
}])
