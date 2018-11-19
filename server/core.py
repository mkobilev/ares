#coding: utf-8
from ascii import *
import json
import random
import uuid
import os
import sys
import re
import datetime
from my_exceptions import ErrSaveToFile, BadUserName
from serialization import JsonSerializableObject


BASE_FOLDER = os.path.dirname(sys.argv[0])
GAMES_FOLDER = os.path.dirname(sys.argv[0]) + '/games/'


def gen_id():
    return str(uuid.uuid4())


class Game(JsonSerializableObject):

    def __init__(self, name=None):
        self.name = name if not name else datetime.datetime.now().strftime("%Y-%m-%d")
        self.tasks = []
        self.users = []
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.id = gen_id()
        self.ips = []
        self.users_names = []

    def parse_dict(self, name, value):
        if name == 'tasks':
            return Task().from_dict(value)
        elif name == 'users':
            return User().from_dict(value)
        return value

    def __unicode__(self):
        return (u'%s' % self.name).strip()

    def __str__(self):
        return unicode(self).encode('utf-8')

    __repr__ = __str__

    def save(self):
        if not os.path.exists(GAMES_FOLDER):
            os.makedirs(GAMES_FOLDER)
        try:
            file = open(GAMES_FOLDER + self.name+'_'+self.date+'.game', 'w')
            file.write(json.dumps(self.to_dict(), indent=4, sort_keys=True))
            file.close()
        except IOError, ex:
            raise ErrSaveToFile

    @classmethod
    def load(cls, filename):
        try:
            file = open(GAMES_FOLDER + filename + '.game', 'r')
            text = file.read()
            dict = json.loads(text)
            file.close()

            game = Game().from_dict(dict)

            #callback links
            return game
        except IOError, ex:
            print "error: ", ex



#       USERs

    def get_user_place(self, user):
        usrs = []
        sort = sorted(self.users, key=lambda x: x.score, reverse=True)
        return sort.index(user)+1

    def get_user_by_name(self, user_name=''):
        filtered = filter(lambda x: x.name == user_name, self.users)
        if not len(filtered):
            print 'BadUserName'
        return filtered[0]

    def add_user(self, name, key, ip):

        if name in self.users_names:
            return 'user already exists\ncmd: '
        elif ip in self.ips:
            return 'user with [ip] already exists ..\ncmd: '
        elif len(name) > 15:
            return 'max name length 15 char..\ncmd: '

        user = User(name, key, ip)
        self.users.append(user)
        self.users_names.append(name)
        self.ips.append(ip)
        user.score += 100
        user.bonus += user.bonus_info['pass']
        return 'user successfully created\ncmd: '

#       USERs

#       TASKs
    def get_task_by_name(self, task_name=''):
        filtered = filter(lambda x: x.name == task_name, self.tasks)
        if not len(filtered):
            raise BadUserName
        return filtered[0]

    #TODO N tasks view
    def get_tasks(self, n=None):
        tasks = []
        for task in self.tasks:
            #{name}|{link}|{info}|{price}|
            tsk = self.__str(task.name, task.link, task.price)
            tasks.append(tsk)
        try:
            a = sorted(tasks, key=lambda x: int(x[2]))
        except Exception as ex:
            print ex

        if a:
            return a
        else:
            return tasks

    #(self, name=None, link=None, price=None, info=None, answer="1337")
    def add_task(self, name, link, price, info):
        task = Task(name, link, price, info)
        self.tasks.append(task)
        return True

#       TASKs

    def __str(self, *args):
        out = []
        for data in args:
            try:
                out.append(' ' + str(data) + ' ' * (20 - (len(str(data)) + 1)))
            except Exception as ex:
                print "err:", ex

        return out

#TODO N taems view
    def scoreboard(self, n=None):
        usrs = []
        a = sorted(self.users, key=lambda x: x.score, reverse=True)
        for user in a:
            #{name}|{solved}|{score}|{bonus}|
            usr = self.__str(user.name, len(user.solved_tasks), user.score, user.bonus)
            usrs.append(usr)
        return usrs


class User(JsonSerializableObject):

    def __init__(self, name=None, key=None, ip=None):
        #self.game = game
        self.name = name
        self.key = key
        self.ip = ip
        self.id = gen_id()
        self.score = 0
        self.bonus = 0
        self.bonus_info = {'pass': self.CheckPassword(key)}
        self.solved_tasks = []

    def solved_tasks_str(self):
        solved = ""
        for task in self.solved_tasks:
            solved += task.name + '\t'+task.price+'\n\t'
        return solved

    def post_flag(self, task, flag, key):
        if self.key != key:
            return 'userkey is wrong!'
        elif task in self.solved_tasks and flag == task.answer:
            self.score -= 100
            self.bonus -= random.randrange(1337)
            return cowsay_m.format(str="Sorry, bro!")
        elif task not in self.solved_tasks and flag == task.answer and task.name != '1337':
            self.score += int(task.price)
            self.bonus += random.randrange(1337)
            self.solved_tasks.append(task)
            return cowsay_p.format(str="Congrats!")
        elif task.name=='1337':
            self.bonus += 1
            #self.solved_tasks.append(task)
            return cowsay_p.format(str="Congrats!")
        else:
            return cowsay.format(str="Unknown flag!")

    def parse_dict(self, name, value):
        return value

    def serialize_value(self, name, value):
        return value

    def CheckPassword(self, password):
        if password is None:
            return 0
        _strength = ['Blank', 'Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong']
        strength = [100, 200, 300, 400, 500, 600]
        score = 1

        if len(password) < 1:
            return strength[0]
        if len(password) < 4:
            return strength[1]

        if len(password) >=8:
            score = score + 1
        if len(password) >=10:
            score = score + 1

        if re.search('\d+',password):
            score = score + 1
        if re.search('[a-z]',password) and re.search('[A-Z]',password):
            score = score + 1
        if re.search('.[!,@,#,$,%,^,&,*,?,_,~,-,£,(,)]',password):
            score = score + 1

        return strength[score]

    def __unicode__(self):
        return (u'%s' % self.name).strip()

    def __str__(self):
        return unicode(self).encode('utf-8')

    __repr__ = __str__



class Task(JsonSerializableObject):

    def __init__(self, name=None, link=None, price=None, info=None, answer="1337"):
        self.name = name
        self.link = link
        self.id = gen_id()
        self.info = info
        self.price = price
        self.answer = answer

    def parse_dict(self, name, value):
        return value

    def serialize_value(self, name, value):
        return value

    def __unicode__(self):
        return (u'%s' % self.name).strip()

    def __str__(self):
        return unicode(self).encode('utf-8')

    __repr__ = __str__


