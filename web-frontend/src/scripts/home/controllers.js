'use strict';
angular.module('app.home')

.controller('HomeController', ['$rootScope', '$scope', 'StatisticsService', 'HomepageService',
    function($rootScope, $scope, StatisticsService, HomepageService)  {
        $rootScope.loadingLogin = false;

        $scope.game_counts = StatisticsService.getGamesCounts();
        $scope.game_points = StatisticsService.getGamesPoints();
        $scope.friends_count = StatisticsService.getFriendsCounts();
        $scope.notification_counts = StatisticsService.getNotificationCounts();

        $scope.tournament = false;

        $rootScope.$on("newFriendNotification", function() { $scope.friends_count = parseInt($scope.friends_count) + 1 });

        HomepageService.getAllTournaments(
            function(tournamentList) {
                if(tournamentList.length > 0) {
                    $scope.tournament = tournamentList[0];
                }

                $scope.tournamentList = tournamentList;
            },
            function(response) {
                // TODO
                console.error("Deal with error")
            }
        )
    }
]);
