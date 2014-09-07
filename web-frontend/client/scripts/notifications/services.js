'use strict';
angular.module('app.notifications')

.factory('NotificationService', ['$http', 'SETTINGS','Session', '$rootScope',
    function($http, SETTINGS, Session, $rootScope) {
      return {
          getFriendNotifications : function(){
            var notifications = Session.get('friend_notifications');
            if(notifications) {
              return JSON.parse(notifications);
            }

            return [];
          },
          getGameNotifications : function(){
            var notifications = Session.get('game_notifications');
            if(notifications) {
              return JSON.parse(notifications);
            }

            return [];
          },
          removeFriendNotification : function(notification) {
            var notifications = this.getFriendNotifications();

            this.removeNotification(notifications, notification)

            Session.create('friend_notifications', JSON.stringify(notifications));

            $rootScope.$broadcast("notificationsUpdated");
            return notifications;
          },
          removeGameNotification : function(notification) {
            var notifications = this.getGameNotifications();

            this.removeNotification(notifications, notification)

            Session.create('game_notifications', JSON.stringify(notifications));

            $rootScope.$broadcast("notificationsUpdated");
            return notifications;
          },
          removeNotification: function(notifications, notification) {

            var n;
            for(var i in notifications) {
              n = notifications[i];
              if(n.id == notification.id) {
                break;
              }
            }

            if(n.id == notification.id) {
              notifications.splice(i, 1);
            }

          },
          updateNotification: function(notification_pk, notification_type) {
            $http.put(SETTINGS.url.updateNotification(notification_pk, notification_type));
          }
      }
    }
]);
