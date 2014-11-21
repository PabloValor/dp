'use strict';
angular.module('app.home')

.controller('HomeController', ['$rootScope', '$scope', 'StatisticsService', 
    function($rootScope, $scope, StatisticsService)  {
        $rootScope.loadingLogin = false;
        $scope.game_counts = StatisticsService.getGamesCounts();
        $scope.game_points = StatisticsService.getGamesPoints();
        $scope.friends_count = StatisticsService.getFriendsCounts();
        $scope.notification_counts = StatisticsService.getNotificationCounts();
    }
]);
