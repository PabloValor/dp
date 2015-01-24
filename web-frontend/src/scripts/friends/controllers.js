'use strict';
angular.module('app.friends')

.controller('FriendsController', ['$scope', 'UserService', 'FriendsService', '$rootScope', 'NotificationService',
    function($scope, UserService, FriendsService, $rootScope, NotificationService)  {
        $rootScope.loadingInit = true;

        FriendsService.getFriends(
          function(players) {

              if(players.length > 0) {
                  $scope.friends = players.filter(function(p) { return p.is_friend });
                  $scope.friends_limbo = players.filter(function(p) { return p.is_limbo_friend });
                  $scope.friends_waiting_for_you = players.filter(function(p) { return p.is_waiting_for_you });
              } 

              $rootScope.loadingInit = false;
          },
          function(error) {
              console.log(error);
          }
        );

        $scope.selectFriend = function(friend) {
          $scope.selectedFriend = friend;
        }

        $scope.updateFriendship = function(status, friend) {
            friend.is_friend = status;

            if(status) {
              if($scope.friends.length == 0) {
                $scope.friends = [];
              }
              $scope.friends.push(friend);
             }

            var index = $scope.friends_waiting_for_you.indexOf(friend);
            $scope.friends_waiting_for_you.splice(index, 1);

            if($scope.friends_waiting_for_you.length == 0) {
              $scope.no_more_friends_waiting = true;
            }

            FriendsService.updateFriendship(friend.id, status, 
                function(response) {
                  FriendsService.clearCache();
                  UserService.clearCache();

                  var friend_notification = FriendsService.getFriendNotification(friend.username);
                  if(friend_notification != null) {
                    NotificationService.removeFriendNotification(friend_notification);
                    NotificationService.updateNotification(friend_notification.username, 'friend');
                  }
            });
        }
    }
])

.controller('FriendsSearchController', ['$scope', 'UserService', 'FriendsService',
    function($scope, UserService, FriendsService)  {
      $scope.intro = true;
      $scope.not_found = false;

      $scope.search = function() {
        $scope.intro = false;
        $scope.not_found = false;

        UserService.search($scope.username, 
          function(players) {
            $scope.players = players;

            if(players.length == 0) {
              $scope.not_found = "" + $scope.username; // New object
            }
          }, 
          function(response) {
            console.log("no funca el server");
          });
      };

      $scope.makeFriend = function(player) {
        FriendsService.makeFriend(player.id, 
          function(response) {
            player.is_limbo_friend = true;
            player.you_are_bad_friend = false;
            FriendsService.clearCache();
          }, 
          function(response) {
            console.log("no funca el server");
          });
      };

    }
])
