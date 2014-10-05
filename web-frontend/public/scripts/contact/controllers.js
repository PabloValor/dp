'use strict';
angular.module('app.contact')

.controller('ContactController', ['$scope', 'ContactService',
    function($scope, ContactService)  {
	$scope.submit_contact = function() {
	    console.info($scope.email);
	    console.info($scope.subject);
	    console.info($scope.text);

	    ContactService.new($scope.email, $scope.subject, $scope.text)
	}
    }
]);

