'use strict';
angular.module('app.games')

.directive('gameMode', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/games/views/_gameMode.html',
      replace: true,
      scope: { classic: '=' }
    };
});
