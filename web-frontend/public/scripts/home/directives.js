'use strict';
angular.module('app.home')

.directive('allTournamentsNextFixture', function() {
    return {
        restrict: 'E',
        templateUrl: 'scripts/home/views/allTournamentsNextFixture.html',
        replace: true,
        controller: ['$scope', 'StatisticsService', function($scope, StatisticsService) {
            StatisticsService.getAllTournamentsNextFixture(function(tournaments) {
                $scope.tournaments = tournaments;
                console.info(tournaments);
            });
        }]
    }
});
