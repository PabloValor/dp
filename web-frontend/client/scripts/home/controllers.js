'use strict';
angular.module('app.home')

.controller('HeaderController', ['$scope', 'UserService', 
    function($scope, UserService)  {
        $scope.username = function() {
          return UserService.getUsername();
        };

        $scope.game_notifications = function() {
          return UserService.getGameNotifications();
        };

        $scope.friend_notifications = function() {
          return UserService.getFriendNotifications();
        };
    }
])
