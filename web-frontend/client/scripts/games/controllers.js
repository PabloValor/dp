'use strict';
angular.module('app.games')

.controller('GameController', ['$scope', 'GameService', 
    function($scope, GameService)  {

        $scope.games = GameService.all();

    }
]);


