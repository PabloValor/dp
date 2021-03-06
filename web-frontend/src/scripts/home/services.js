'use strict';
angular.module('app.home')
.factory('StatisticsService', ['$http', 'Session', 'SETTINGS', 'NotificationService',  function($http, Session, SETTINGS, NotificationService) {
    return {
        setGameCounts : function(n) {
            Session.create('games_count', n);
        },
        getGamesCounts : function(){
            return Session.get('games_count');
        },
        getGamesPoints : function(){
            return Session.get('games_points');
        },
        setFriendsCounts : function(n) {
            Session.create('friends_count', n);
        },        
        getFriendsCounts: function(){
            return Session.get('friends_count');
        },
        getNotificationCounts: function(){
            var friend_notifications = NotificationService.getFriendNotifications();
            var game_notifications = NotificationService.getGameNotifications();
                
            return friend_notifications.length + game_notifications.length
        }
    }
    }])

.factory('HomepageService', ['$http', 'SETTINGS', 'Data',  
    function($http, SETTINGS, Data) {
    return {
        getAllTournaments: function(f_success, f_error) {
            if(!!Data.homepageTournaments) {
                f_success(Data.homepageTournaments);
                return;
            } 

            $http.get(SETTINGS.url.allTournamentsHomepage())
                .success(function(response) {
                    console.info('Tournaments Homepage')
                    console.info(response);

                    Data.homepageTournaments = response;                    

                    if(!!f_success) {
                        f_success(response);
                    }
                })
                .error(function(response) {
                    console.error('Tournaments Homepage')                    
                    console.error(response);

                    if(!!f_error) {
                        f_error(response);
                    }
                });
        },
        getAllNews: function(f_success, f_error) {
            if(!!Data.news) {
                f_success(Data.news);
                return;
            } 

            $http.get(SETTINGS.url.allNews())
                .success(function(response) {
                    console.info('News Homepage')
                    console.info(response);

                    Data.news = response;                    

                    if(!!f_success) {
                        f_success(response);
                    }
                })
                .error(function(response) {
                    console.error('News Homepage')                    
                    console.error(response);

                    if(!!f_error) {
                        f_error(response);
                    }
                });
        }        
    }
    }])
