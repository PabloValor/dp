'use strict';
angular.module('app.home', [])

    .config(['$routeProvider', function($routeProvider) {
        var bienvenido_usuario = { redirectTo: '/bienvenido' };
        var bienvenido_empresa = { redirectTo: '/signin' };

        var bienvenido = bienvenido_usuario;
        var templateUrl = 'scripts/home/views/bienvenido.html';

        var host = document.location.host.split('.');
        if(host.length == 3 && host[0] != 'www') {
            bienvenido = bienvenido_empresa;
            templateUrl = 'scripts/users/views/signin.html';
        }

        return $routeProvider
            .when('/', bienvenido)
            .when('/bienvenido', {
                templateUrl: templateUrl
            })
            .when('/noticias', {
                authenticate: true,
                templateUrl: 'scripts/home/views/news.html'
            });
    }]);



