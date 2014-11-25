'use strict';
angular.module('app.home')

.directive('allTournamentsNextFixture', function() {
    return {
        restrict: 'E',
        templateUrl: 'scripts/home/views/allTournamentsNextFixture.html',
        replace: true,
        controller: ['$scope', 'StatisticsService', function($scope, StatisticsService) {
            StatisticsService.getAllTournamentsNextFixture(function(tournaments) {
                console.info("next")
                console.info(tournaments)
                $scope.tournaments_next = tournaments; // I don't know why but if they have the same name it's like they are sharing the variable
               });
        }]
    }
})

.directive('allTournamentsCurrentOrLastFixture', function() {
    return {
        restrict: 'E',
        templateUrl: 'scripts/home/views/allTournamentsCurrentOrLastFixture.html',
        replace: true,
        controller: ['$scope', 'StatisticsService', function($scope, StatisticsService) {
            StatisticsService.getAllTournamentsCurrentOrLastFixture(function(tournaments) {
                console.info("current or last")
                console.info(tournaments)                
                $scope.tournaments = tournaments;
               });
        }]
    }
});
