'use strict';
angular.module('app.core')

.directive('counter', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/core/views/counter.html',
      replace: true,
      scope: { player: '=' },
      controller: function($scope) {
        if(!!!$scope.player.initial_points) {
          $scope.player.initial_points = 0;
        }

        $scope.up = function() {
          $scope.player.initial_points++;
        }

        $scope.down = function() {
          $scope.player.initial_points--;
        }
      }
    };
})

.directive('cloak', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/core/views/loadingCloak.html',
      replace: true,
      scope: { loading: '=', left: '=' },
      controller: function($scope) {
      }
    };
})

.directive('chartLine', function() {
    return {
      restrict: 'A',
      scope: { data: '=' },
      link: function($scope, ele, attrs) {
          var ctx = ele[0].getContext("2d")
          var myLineChart = new Chart(ctx).Line($scope.data);
      }
    };
});
