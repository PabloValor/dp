'use strict';
angular.module('app.home')

.directive('allTournamentsNextFixture', function() {
    return {
        restrict: 'E',
        templateUrl: 'scripts/home/views/allTournamentsNextFixture.html',
        replace: true,
        scope: { tournament: '=' },
        controller: ['$scope', 'TournamentService', function($scope, TournamentService) {
            TournamentService.getAllTournamentsNextFixture(
                function(tournamentFixtureList) {
                    console.info(tournamentFixtureList)
                    $scope.tournamentFixtureList = tournamentFixtureList; // I don't know why but if they have the same name it's like they are sharing the variable
               }, 
                function(response) {
                    console.error("Deal with error");
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
            TournamentService.getAllTournamentsCurrentOrLastFixture(
                function(tournamentFixtureList) {
                    console.info(tournamentFixtureList)                
                    $scope.tournamentFixtureList = tournamentFixtureList;
                },
                function(response) {
                    console.error("Deal with error");
                });
        }]
    }
})

.directive('tournamentStats', function() {
    return {
        restrict: 'E',
        templateUrl: 'scripts/games/views/_tournamentTable.html',
        replace: true,
        scope: { tournament: '='},
        controller: ['$scope', 'TournamentService', function($scope, TournamentService) {
            function setTournamentTable() {
                TournamentService.getTournamentStats(
                    $scope.tournament.id, 
                    function(tournamentStats) {
                        console.info("Tournament Stats")
                        console.info(tournamentStats)                
                        $scope.tournamentStats = tournamentStats;
                        console.info(tournamentStats.teams);
                        $scope.table = tournamentStats.teams.map(
                            function(team) { 
                                var stats = team.stats;
                                return { name: team.name,
                                         points: (stats.d + (stats.w * 3)),
                                         played: (stats.d + stats.l + stats.w),
                                         win: stats.w,
                                         lose: stats.l,
                                         draw: stats.d
                                       };
                            });
                    },
                    function(response) {
                        console.error("Deal with error");
                    });            
            }

            $scope.title = "Posiciones";
            $scope.largeTable = true;
            $scope.$watch('tournament', function (newVal) { setTournamentTable(); });
        }]
    }
})

.directive('allNews', function() {
    return {
        restrict: 'E',
        templateUrl: 'scripts/home/views/allNews.html',
        replace: true,
        scope: { tournament: '='},
        controller: ['$scope', '$sce', 'HomepageService', function($scope, $sce, HomepageService) {
            $scope.renderHtml = function(html_code)
            {
                return $sce.trustAsHtml(html_code);
            };
            
            HomepageService.getAllNews(
                function(newsList) {
                    $scope.newsList = newsList;
                },
                function(response) {
                    console.error("Deal with error");
                });
        }]
    }
})
;
