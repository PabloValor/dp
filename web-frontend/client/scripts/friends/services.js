'use strict';
angular.module('app.friends')


.factory('FriendsService', ['$http', 'SETTINGS', 'Data',  function($http, SETTINGS, Data) {
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
        }

    };
}]);
