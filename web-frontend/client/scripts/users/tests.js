'use strict';

 describe('user authentication', function() {

    beforeEach(angular.mock.module('app'));

    it('should get login success', inject(['AuthenticationService',
        function(AuthenticationService) {
            AuthenticationService.login('nico', 'password');
        }])
    );
})
