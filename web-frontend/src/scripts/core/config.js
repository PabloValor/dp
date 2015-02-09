'use strict';
angular.module('app.core', [])

    .run(['$rootScope', function($rootScope) {
        var host = document.location.host.split('.');
        if(host.length == 3 && host[0] != 'www') {
            $rootScope.businessSite = true;
        }            
    }]);
