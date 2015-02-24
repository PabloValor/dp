'use strict';
angular.module('app.users', [])

    .config(['$httpProvider', function ($httpProvider) {
        $httpProvider.interceptors.push('TokenInterceptor');
    }])

    .config(['$routeProvider', function($routeProvider) {
      return $routeProvider
            .when('/signup', { templateUrl: 'scripts/users/views/signup.html' })
            .when('/signin', { templateUrl: 'scripts/users/views/signin.html' })
    }])


    .run(['$rootScope', 'StatisticsService', function($rootScope, StatisticsService) {
        $rootScope.$on("haveNewFriend",
                       function() {
                           var n = StatisticsService.getFriendsCounts();
                           StatisticsService.setFriendsCounts(parseInt(n) + 1);
                       });

        $rootScope.$on("newFriendNotification",
                       function() {
                           var n = StatisticsService.getFriendsCounts();
                           StatisticsService.setFriendsCounts(parseInt(n) + 1);
                       });
    }]);



