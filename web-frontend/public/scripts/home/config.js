'use strict';
angular.module('app.home', [])

.config(['$routeProvider', function($routeProvider) {
      return $routeProvider.when('/', {
        redirectTo: '/bienvenido'
      })
      .when('/bienvenido', {
        templateUrl: 'scripts/home/views/bienvenido.html'
      })
      .when('/noticias', {
        authenticate: true,
        templateUrl: 'scripts/home/views/news.html'
      });
}])




