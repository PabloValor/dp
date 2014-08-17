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

.directive('wizardForm', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/core/views/wizard_form.html',
      transclude: true,
      scope: { steps: '=', currentStep : '=', optionalStep: '=', action: '=', game: '=', selectedTournament: '='},
      link: function($scope, element, attrs) {
        $scope.lastStep = $scope.steps[$scope.steps.length - 1];
        $scope.nextStep = function() {
          var index = $scope.steps.indexOf($scope.currentStep);
          $scope.currentStep = $scope.steps[index + 1];
        };

        $scope.previousStep = function() {
          var index = $scope.steps.indexOf($scope.currentStep);
          $scope.currentStep = $scope.steps[index - 1];
        };

        $scope.setlastStep = function() {
          $scope.currentStep = $scope.lastStep;
        };

        $scope.finish = function() {
          $scope.action();
        }

        $scope.validate = function() {
          if($scope.currentStep.validate) {
            return $scope.currentStep.validate($scope);
          } else {
            return true;
          }
        }
      }
    };
})

;
