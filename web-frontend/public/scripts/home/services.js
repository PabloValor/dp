'use strict';
angular.module('app.home')
    .factory('StatisticsService', ['$http', 'Session', 'SETTINGS', 'NotificationService',  function($http, Session, SETTINGS, NotificationService) {
    return {
        getGamesCounts : function(){
            return Session.get('games_count');
        },
        getGamesPoints : function(){
            return Session.get('games_points');
        },
        getFriendsCounts: function(){
            return Session.get('friends_count');
        },
        getNotificationCounts: function(){
            var friend_notifications = NotificationService.getFriendNotifications();
            var game_notifications = NotificationService.getGameNotifications();
                
            return friend_notifications.length + game_notifications.length
        },
        getAllTournaments: function(f_s, f_e) {
            return $http.get(SETTINGS.url.allTournaments())
                .success(function(response) {
                    f_s(response);
                })
                .error(function(response) {
                    f_e(response);
                });
        },        
        getAllTournamentsNextFixture: function(f) {
            return $http.get(SETTINGS.url.allTournamentsNextFixture())
                .success(function(response) {
                    f(response);
                })
                .error(function(response) {
                    f(response);
                });
        },
        getAllTournamentsCurrentOrLastFixture: function(f) {
            return $http.get(SETTINGS.url.allTournamentsCurrentOrLastFixture())
                .success(function(response) {
                    f(response);
                })
                .error(function(response) {
                    f(response);
                });
        }        
        
    }
}])

