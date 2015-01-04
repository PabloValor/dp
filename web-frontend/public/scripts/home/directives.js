'use strict';
angular.module('app.home')

.directive('allTournamentsNextFixture', function() {
    return {
        restrict: 'E',
        templateUrl: 'scripts/home/views/allTournamentsNextFixture.html',
        replace: true,
        scope: { tournament: '=' },
        controller: ['$scope', 'TournamentService', function($scope, TournamentService) {
            TournamentService.getAllTournamentsNextFixture(function(tournamentFixtureList) {
                console.info("next")
                console.info(tournamentFixtureList)
                $scope.tournamentFixtureList = tournamentFixtureList; // I don't know why but if they have the same name it's like they are sharing the variable
               });
        }]
    }
})

.directive('allTournamentsCurrentOrLastFixture', function() {
    return {
        restrict: 'E',
        templateUrl: 'scripts/home/views/allTournamentsCurrentOrLastFixture.html',
        replace: true,
        scope: { tournament: '='},
        controller: ['$scope', 'TournamentService', function($scope, TournamentService) {
            TournamentService.getAllTournamentsCurrentOrLastFixture(function(tournamentFixtureList) {
                console.info("current or last")
                console.info(tournamentFixtureList)                
                $scope.tournamentFixtureList = tournamentFixtureList;
               });
        }]
    }
});
