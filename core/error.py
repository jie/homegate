#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


class Error(Exception):

    def __init__(self, **kwargs):
        self.code = -9999
        self.msg = 'system_error'
        self.kwargs = kwargs

    def __str__(self):
        kwargs = self.kwargs if len(self.kwargs) else 'None'
        message = "code:{code}, msg:{msg}, args:{kwargs}".format(
            code=self.code, msg=self.msg, kwargs=kwargs
        )
        return message

    def __rep__(self):
        return self.__str__()


class SysError(Error):

    def __init__(self, **kwargs):
        super(SysError, self).__init__(**kwargs)


class LogicError(Error):

    def __init__(self, **kwargs):
        super(LogicError, self).__init__(**kwargs)


class ArgumentError(LogicError):

    def __init__(self, **kwargs):
        super(ArgumentError, self).__init__(**kwargs)
        self.code = -1000
        self.msg = 'args error: %s' % kwargs.get('name')


class UserNotFound(LogicError):

    def __init__(self, **kwargs):
        super(UserNotFound, self).__init__(**kwargs)
        self.code = -1001
        self.msg = 'user not found'


class UsernameExisted(LogicError):

    def __init__(self, **kwargs):
        super(UsernameExisted, self).__init__(**kwargs)
        self.code = -1002
        self.msg = 'username existed'


class VerifyPasswordError(LogicError):

    def __init__(self, **kwargs):
        super(VerifyPasswordError, self).__init__(**kwargs)
        self.code = -1003
        self.msg = 'verify password error'


class RepeatPasswordError(LogicError):

    def __init__(self, **kwargs):
        super(RepeatPasswordError, self).__init__(**kwargs)
        self.code = -1003
        self.msg = 'repeat password error'


class SessionRequiredError(LogicError):

    def __init__(self, **kwargs):
        super(SessionRequiredError, self).__init__(**kwargs)
        self.code = -1004
        self.msg = 'user must login'


class AvatarUploadError(LogicError):

    def __init__(self, **kwargs):
        super(AvatarUploadError, self).__init__(**kwargs)
        self.code = -1010
        self.msg = 'upload avatar failed'


class TokenCheckError(LogicError):

    def __init__(self, **kwargs):
        super(TokenCheckError, self).__init__(**kwargs)
        self.code = -2000
        self.msg = 'token check failed'


class MailgunResponseError(LogicError):

    def __init__(self, **kwargs):
        super(MailgunResponseError, self).__init__(**kwargs)
        self.code = -2001
        self.msg = 'mailgun response error'


class MailgunConnectError(LogicError):

    def __init__(self, **kwargs):
        super(MailgunConnectError, self).__init__(**kwargs)
        self.code = -2002
        self.msg = 'mailgun connect error'


class VerifyEmailTokenError(LogicError):

    def __init__(self, **kwargs):
        super(VerifyEmailTokenError, self).__init__(**kwargs)
        self.code = -2003
        self.msg = 'verify email error'


class ChecktModifyUserinfoDateError(LogicError):

    def __init__(self, **kwargs):
        super(ChecktModifyUserinfoDateError, self).__init__(**kwargs)
        self.code = -2004
        self.msg = 'User data can only be modified once a week at most'
