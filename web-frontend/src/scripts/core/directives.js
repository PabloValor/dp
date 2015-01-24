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
      scope: { loading: '=', left: '@' },
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

.directive('phrases', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/core/views/phrases.html',
      replace: true,
      scope: { bambino: '@' },
      controller: function($scope) {
        var phrases = [
                  { text: 'Esto es in-cre-i-ble, acá falta Spilber (sic) nomás...de ciencia ficción!!!', author: 'Bambino Veira' },
                  { text: 'Para mi, el fútbol es belleza.', author: 'Bambino Veira' },
                  { text: 'La base está.', author: 'Bambino Veira' },
                  { text: 'Estamos motivados.', author: 'Bambino Veira' },
                  { text: 'El fútbol, como la vida, es un estado de ánimo.', author: 'Bambino Veira' },
                  { text: 'Que lindo, que lindo...', author: 'Bambino Veira' } ];

        var i = _.random(0, phrases.length - 1);
        $scope.phrase = phrases[i];
      }
    };
})

.directive('backgroundFootball', function() {
    return {
      restrict: 'A',
       link: function ($scope, element) {

        var i = _.random(1, 4);
        element.addClass('bg_' + i);
      }
    }
})

.directive('navHeader', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/core/views/header.html',
      controller: ['$scope', '$rootScope', '$location', 'socket', 'logger', 'UserService', 'NotificationService', 'AuthenticationService',
      function($scope, $rootScope, $location, socket, logger, UserService, NotificationService, AuthenticationService) {
        function setNotificationCount() {
          $scope.notification_count = $scope.game_notifications.length + $scope.friend_notifications.length;
        }

        // These are call to the Session
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
              $scope.game_notifications = NotificationService.getGameNotifications();
              $scope.friend_notifications = NotificationService.getFriendNotifications();
              setNotificationCount();
        });

        var getFriendNotificationMessage = function(notification) {
          var message;
          switch(notification.notification_type) {
              case '1':
               message = notification.sender.username + ' quiere ser tu amigo!';
               break;
              case '2':
               message = notification.sender.username + ' es tu amigo!';
               break;
          }

          return message;
        };
        
        var getGameNotificationMessage = function(notification) {
          var message;
          switch(notification.notification_type) {
              case '1':
               message = notification.sender.username + ' te invito jugar al torneo ' + notification.game_name;
               break;
              case '2':
               message = notification.sender.username + ' acepto jugar al torneo ' +  notification.game_name;
               break;
              case '3':
               message = notification.sender.username + ' rechazo jugar al torneo ' + notification.game_name;
               break;
              case '4':
               message = notification.sender.username + ' solicita que lo invites de vuelta al torneo ' + notification.game_name
               break;
          }

          return message;
        };
        
        var listen = function(token) {
          socket.on(token, function (notification) {
              var notification_message;
              if(!!notification.game_name) {
                  $rootScope.$broadcast("newGameNotification", notification);
                  notification_message = getGameNotificationMessage(notification);
                  NotificationService.addGameNotification(notification);
              } else {
                  $rootScope.$broadcast("newFriendNotification");                  
                  notification_message = getFriendNotificationMessage(notification);
                  NotificationService.addFriendNotification(notification);
              }

              console.error(notification);
              logger.log(notification_message);
              setNotificationCount();
          });
        };

        var token = UserService.getToken();
        if(token) {
          listen(token);
        } else {
          $rootScope.$on("userLoginSuccess", 
            function() {
              token = UserService.getToken();
              listen(token);
            });
        }

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

        $scope.getFriendNotificationMessage = getFriendNotificationMessage;
        $scope.getGameNotificationMessage = getGameNotificationMessage;

        $scope.logout = function() {
            AuthenticationService.logout();
            $location.path('/');
        };

      }]
    };
});

