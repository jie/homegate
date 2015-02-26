(function(angular) {
    'use strict';
    angular.module('homegateApp', ['ngRoute', 'ngResource', 'pascalprecht.translate'])
        .config(function($translateProvider) {
            $translateProvider.translations('cn', {
                USERNAME: '用户名',
                PASSWORD: '密码',
                REPEAT_PASSWORD: '重复密码',
                EMAIL: '电子邮箱',
                SIGNUP: '注册',
                SIGNIN: '登陆',
                PLEASE_ENTER_A_USERNAME: '请填写您的用户名',
                PLEASE_ENTER_A_EMAIL: '请填写您的电子邮箱地址',
                PLEASE_ENTER_A_PASSWORD: '请填写您的登陆密码',
                PLEASE_ENTER_REPEAT_PASSWORD: '请重复您填写的登录密码',
                YOUR_PASSWORD_MUST_BE_AT_LEAST_6_CHARACTERS: '您的密码长度必须大于6位',
                REMEMBER_ME: '保持登录'
            });
            $translateProvider.translations('en', {
                USERNAME: 'Username',
                PASSWORD: 'Password',
                REPEAT_PASSWORD: 'Repeat Password',
                EMAIL: 'Email',
                SIGNUP: 'Signup',
                SIGNIN: 'Signin',
                PLEASE_ENTER_A_USERNAME: 'Please enter a username',
                PLEASE_ENTER_A_EMAIL: 'Please enter a username',
                PLEASE_ENTER_A_PASSWORD: 'Please enter a password',
                PLEASE_ENTER_REPEAT_PASSWORD: 'Please repeat the password',
                YOUR_PASSWORD_MUST_BE_AT_LEAST_6_CHARACTERS: 'Your password must be at least 6 characters',
                REMEMBER_ME: 'remember me'
            });
            $translateProvider.preferredLanguage('cn');
        })

    .controller('MainController', function($scope, $route, $routeParams, $location) {
        $scope.$route = $route;
        $scope.$location = $location;
        $scope.$routeParams = $routeParams;
    })

    .controller('SigninController', function($scope, $routeParams) {
        $scope.name = "SigninController";
        $scope.params = $routeParams;
        $('.ui.checkbox').checkbox()
    })

    .controller('SignupController', function($scope, $routeParams, $translate, $http) {
        $scope.name = "SignupController";
        $scope.params = $routeParams;
        $scope.userdata = {};
        $scope.notify = {'status': 'hidden'};
        $scope.user = null;

        var formSettings = {
            onSuccess: function() {

                $http.post('/api/user/signup', $scope.userdata)
                    .success(
                        function(data, status, headers, config) {
                            console.log(data);
                            if(data.status==0){
                                $scope.notify = data;
                            }
                        })
                    .error(
                        function(data, status, headers, config) {

                        });
            },
            onFailure: function() {
                $('.form .ui.message').addClass('error');
            }
        }

        var submitFormValidator = {
            username: {
                identifier: 'username',
                rules: [{
                    type: 'empty',
                    prompt: $translate.instant('PLEASE_ENTER_A_USERNAME')
                }]
            },
            email: {
                identifier: 'email',
                rules: [{
                    type: 'email',
                    prompt: $translate.instant('PLEASE_ENTER_A_EMAIL')
                }]
            },
            password: {
                identifier: 'password',
                rules: [{
                    type: 'empty',
                    prompt: $translate.instant('PLEASE_ENTER_A_PASSWORD')
                }, {
                    type: 'length[6]',
                    prompt: $translate.instant('YOUR_PASSWORD_MUST_BE_AT_LEAST_6_CHARACTERS')
                }]
            },
            repeat_password: {
                identifier: 'repeat_password',
                rules: [{
                    type: 'empty',
                    prompt: $translate.instant('PLEASE_ENTER_A_PASSWORD')
                }, {
                    type: 'length[6]',
                    prompt: $translate.instant('YOUR_PASSWORD_MUST_BE_AT_LEAST_6_CHARACTERS')
                }]
            },
        }

        $('.ui.form').form(submitFormValidator, formSettings);
    })

    .controller('DashboardController', function($scope, $routeParams) {
        $scope.name = "DashboardController";
        $scope.params = $routeParams;
    })

    .config(function($routeProvider, $locationProvider) {
        $routeProvider
            .when('/account/signup', {
                templateUrl: '/account/signup',
                controller: 'SignupController',
                resolve: {
                    // I will cause a 1 second delay
                    delay: function($q, $timeout) {
                        var delay = $q.defer();
                        $timeout(delay.resolve, 500);
                        return delay.promise;
                    }
                }
            })
            .when('/account/signin', {
                templateUrl: '/account/signin',
                controller: 'SigninController',
                resolve: {
                    // I will cause a 1 second delay
                    delay: function($q, $timeout) {
                        var delay = $q.defer();
                        $timeout(delay.resolve, 500);
                        return delay.promise;
                    }
                }
            })
            .when('/dashboard', {
                templateUrl: '/dashboard',
                controller: 'DashboardController',
                resolve: {
                    // I will cause a 1 second delay
                    delay: function($q, $timeout) {
                        var delay = $q.defer();
                        $timeout(delay.resolve, 500);
                        return delay.promise;
                    }
                }
            })
            // configure html5 to get links working on jsfiddle
            // $locationProvider.html5Mode(true);
    })
})(window.angular);
