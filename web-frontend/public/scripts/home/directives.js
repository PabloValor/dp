'use strict';
angular.module('app.home')

.directive('allTournamentsCurrentFixture', function() {
    return {
        restrict: 'E',
        templateUrl: 'scripts/home/views/allTournamentsCurrentFixture.html',
        replace: true,
        controller: ['$scope', 'StatisticsService', function($scope, StatisticsService) {
            StatisticsService.getAllTournamentsCurrentFixture(function(tournaments) {
                $scope.tournaments = tournaments;
                console.info(tournaments);
            });
        }]
    }
});
