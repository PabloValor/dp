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
})

.directive('navHeader', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/core/views/header.html',
      controller: ['$scope', '$rootScope', '$location', 'UserService', 'NotificationService', 
      function($scope, $rootScope, $location, UserService, NotificationService) {
        function setNotificationCount() {
          $scope.notification_count = $scope.game_notifications.length + $scope.friend_notifications.length;
        }

        $scope.username = UserService.getUsername();
        $scope.game_notifications = NotificationService.getGameNotifications();
        $scope.friend_notifications = NotificationService.getFriendNotifications();
        setNotificationCount() 

        $rootScope.$on("userLoginSuccess", 
          function() { 
              $scope.username = UserService.getUsername();
              $scope.game_notifications = NotificationService.getGameNotifications();
              $scope.friend_notifications = NotificationService.getFriendNotifications();
              setNotificationCount();
        });

        $rootScope.$on("notificationsUpdated", 
            function() {
              console.log("actualizando header");
              $scope.game_notifications = NotificationService.getGameNotifications();
              $scope.friend_notifications = NotificationService.getFriendNotifications();
              console.log($scope.game_notifications);
              setNotificationCount();
        });

        $scope.toFriendNotification = function(notification) {
          NotificationService.updateNotification(notification.id, 'friend'); // We don't care about the response
          $scope.friend_notifications = NotificationService.removeFriendNotification(notification);
          setNotificationCount();
          $location.path('/amigos');
        };

        $scope.toGameNotification = function(notification) {
          NotificationService.updateNotification(notification.id, 'game'); // We don't care about the response
          $scope.game_notifications = NotificationService.removeGameNotification(notification);
          setNotificationCount();
          $location.path('/torneos/detalle/' + notification.game_id);
        };

      }]
    };
});

