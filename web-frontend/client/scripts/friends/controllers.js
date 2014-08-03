'use strict';
angular.module('app.friends')

.controller('FriendsController', ['$scope', 'UserService', 
    function($scope, UserService)  {
        UserService.getFriends(
                function(friends) {
                    $scope.friends = friends;
                    console.log(friends);
                },
                function(error) {
                    console.log(error);
                }
        );

        $scope.selectFriend = function(friend) {
          $scope.selectedFriend = friend;
        }
    }
])

.controller('FriendsSearchController', ['$scope', 'UserService', 
    function($scope, UserService)  {

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
      }

    }
])
