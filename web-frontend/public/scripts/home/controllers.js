'use strict';
angular.module('app.home')

.controller('HomeController', ['$scope', 'StatisticsService', 
    function($scope, StatisticsService)  {
        $scope.game_counts = StatisticsService.getGamesCounts();
        $scope.game_points = StatisticsService.getGamesPoints();
        $scope.friends_count = StatisticsService.getFriendsCounts();
        $scope.notification_counts = StatisticsService.getNotificationCounts();
    }
]);
