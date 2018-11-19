# coding=utf-8


class GameException(Exception):
    pass

class ErrSaveToFile(GameException):
    def __unicode__(self):
        return u'Save failed'

    def __str__(self):
        return unicode(self).encode('utf-8')


class BadUserName(GameException):
    def __unicode__(self):
        return u'Save failed'

    def __str__(self):
        return unicode(self).encode('utf-8')

