'use strict';
angular.module('app.contact')

.controller('ContactController', ['$scope', 'ContactService',
    function($scope, ContactService)  {
	$scope.contact_sent = false;
	$scope.submit_contact = function() {
	    $scope.contact_sent = true;
	    ContactService.new($scope.subject, $scope.text)
	}
    }
]);

