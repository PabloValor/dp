'use strict';
angular.module('app.friends', [])

.config(['$routeProvider', function($routeProvider) {
      return $routeProvider
            .when('/friends', { templateUrl: 'scripts/friends/views/all.html' })
            .when('/amigos', { templateUrl: 'scripts/friends/views/all.html' })
            .when('/friends/search', { templateUrl: 'scripts/friends/views/search.html' })
            .when('/amigos/buscar', { templateUrl: 'scripts/friends/views/search.html' })
}])
