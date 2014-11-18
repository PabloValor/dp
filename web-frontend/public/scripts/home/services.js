'use strict';
angular.module('app.home')

.factory('StatisticsService', ['Session', 'NotificationService',  function(Session, NotificationService) {
    console.info("servicio");
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
            
            console.info(friend_notifications.length);
            return friend_notifications.length + game_notifications.length
        }
    }
}])

