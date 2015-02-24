'use strict';
angular.module('app.friends')


.factory('FriendsService', ['$http', '$rootScope','SETTINGS', 'Data',  'NotificationService',
    function($http, $rootScope, SETTINGS, Data, NotificationService) {
    return {
        getFriends: function(f_success, f_error) {
            if(!!Data.friends) {
                f_success(Data.friends);
                return;
            } 

            $http.get(SETTINGS.url.playerFriends())
                .success(function(response) {
                    console.log(response);

                    Data.friends = response;

                    if(!!f_success) {
                        f_success(response);
                    }
                })
                .error(function(response) {
                    console.log(response);

                    if(!!f_error) {
                        f_error(response);
                    }
                });
        },
        makeFriend : function(player_id, f_success, f_error) {
            $http.post(SETTINGS.url.playerMakeFriend(), { 'friend': player_id })
                .success(function(response) {
                    console.log(response);

                    if(!!f_success) {
                        f_success(response);
                    }
                })
                .error(function(response) {
                    console.log(response);

                    if(!!f_error) {
                        f_error(response);
                    }
                });
        },
        updateFriendship : function(player_id, status, f_success, f_error) {
            $http.put(SETTINGS.url.playerUpdateFriendship(player_id), { 'status': status })
                .success(function(response) {
                    console.log(response);

                    if(!!f_success) {
                        if(status) {
                            $rootScope.$broadcast("haveNewFriend");
                        }
                        f_success(response);
                    }
                })
                .error(function(response) {
                    console.log(response);

                    if(!!f_error) {
                        f_error(response);
                    }
                });
        }, 
        clearCache : function() {
            delete Data.friends;
        },
        getFriendNotification : function(friend_username) {
          var friend_notifications = NotificationService.getFriendNotifications();
          var friend_notification;

          for(var i in friend_notifications) {
            friend_notification = friend_notifications[i];
            if(friend_notification.sender.username == friend_username) {
              return friend_notification;
            }
          }

          return null;
        }
    };
}]);
