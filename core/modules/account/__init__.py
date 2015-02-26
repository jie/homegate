#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import handlers
from core.module import BaseModule


class Module(BaseModule):

    module_name = 'account'
    template_prefix = 'account'

    handlers = [
        {
            'name': 'signin',
            'url': 'signin',
            'handler': handlers.SigninHandler
        },
        {
            'name': 'signup',
            'url': 'signup',
            'handler': handlers.SignupHandler
        },
        {
            'name': 'signout',
            'url': 'signout',
            'handler': handlers.SignoutHandler
        },
        {
            'name': 'settings',
            'url': 'settings',
            'handler': handlers.SettingsHandler
        },
        {
            'name': 'messages',
            'url': 'messages',
            'handler': handlers.MessagesHandler
        },
        {
            'name': 'message_detail',
            'url': 'message_detail',
            'handler': handlers.MessageDetailHandler
        },
        {
            'name': 'avatar',
            'url': 'avatar',
            'handler': handlers.AvatarHandler
        },
        {
            'name': 'tiny_avatar',
            'url': 'tiny_avatar',
            'handler': handlers.TinyAvatarHandler
        },
        {
            'name': 'send_verify_email',
            'url': 'send_verify_email',
            'handler': handlers.SendVerifyEmailHandler
        },
        {
            'name': 'verify_email',
            'url': 'verify_email',
            'handler': handlers.VerifyEmailHandler
        },
        {
            'name': 'update_userinfo',
            'url': 'update_userinfo',
            'handler': handlers.UpdateUserinfoHandler
        },
        {
            'name': 'change_password',
            'url': 'change_password',
            'handler': handlers.ChangePasswordHandler
        },
        {
            'name': 'reset_password',
            'url': 'reset_password',
            'handler': handlers.ResetPasswordHandler
        },
        {
            'name': 'forget_password',
            'url': 'forget_password',
            'handler': handlers.ForgetPasswordHandler
        }
    ]
