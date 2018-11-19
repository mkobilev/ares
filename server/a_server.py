#coding: utf-8

from socket import *
import thread
import sys

from core import *




def validate():
    pass

def post_flag(name, key, flag):
    pass


def response(key):
    print 'Server response: ' + key
    return key


def handler(clientsock, addr):

    clientsock.send(response(hello+'\ncmd: '))
    #global game

    while 1:
        try:
            data = clientsock.recv(BUFF)
        except Exception as ex:
            print ex
            break

        if not data.rstrip().split():
            print 'null data'
            clientsock.send(response('\ncmd: '))
            continue

        # -- log --
        log = """
        #red return "\x1b[31mTest\x1b[0m"
        #\x1b[37;43mTest\x1b[0m
        #\x1b[4;35mTest\x1b[0m
        \x1b[1;31mСтрока\x1b[0m с
        \x1b[4;35;42mразными\x1b[0m \x1b[34;45mстилями\x1b[0m
        \x1b[1;33mоформления\x1b[0m
        """
        #print log

        print repr(addr) + ' recv:' + repr(data)
        #clientsock.send(response(data))
        #print repr(addr), ' sent:', repr(data)
        # -- log --

        # -- cmd --

        args = data.rstrip().split()

        if "reg" == args[0]:
            try:
                clientsock.send(response(game.add_user(args[1], args[2], addr)))
            except Exception as ex:
                print ex
                clientsock.send(response('bad data\ncmd: '))

        elif "close" == args[0]:
            clientsock.send(response('good buy!\ncmd: '))
            break

        elif "help" == args[0]:
            clientsock.send(response(help+'\ncmd: '))

        elif "hello" == args[0]:
            clientsock.send(response(hello+'\ncmd: '))

        elif "scoreboard" == args[0]:
            #{place}|{name}|{solved}|{score}|{bonus}|
            clientsock.send(response((scoreboard_title)))
            users = game.scoreboard()

            for i, user in enumerate(users):
                clientsock.send(response((scoreboard_user.format(place=i+1, name=user[0], solved=user[1],
                                                                 score=user[2], bonus=user[3]))))
            clientsock.send(response('\ncmd: '))
        elif "tasks" == args[0]:
            #{place}|{name}|{link}|{price}|
            clientsock.send(response((tasks_title)))
            tasks = game.get_tasks()

            for i, task in enumerate(tasks):
                clientsock.send(response((tasks_body.format(id=i+1, name=task[0], link=task[1], price=task[2]))))
            clientsock.send(response('\ncmd: '))
        elif "newtask" == args[0]:
            try:
                #(self, name=None, link=None, price=None, info=None, answer="1337")
                if game.add_task(args[1], args[2], args[3], args[4]):
                    clientsock.send(response('task successfully created\ncmd: '))
            except Exception as ex:
                print ex
                clientsock.send(response('error!\ncmd: '))

        elif "flag" == args[0]:
            try:
                flag = args[1]
                user = game.get_user_by_name(args[3])
                try:
                    task = game.get_task_by_name(args[2])
                    clientsock.send(response(user.post_flag(task, flag)))
                    clientsock.send(response('\ncmd: '))
                except Exception as ex:
                    clientsock.send(response(' Wronge taskname!\ncmd: '))
            except Exception as ex:
                clientsock.send(response(' Wronge username!\ncmd: '))

        elif "task" == args[0]:
            if not args[1]:
                print 'err'
                continue
            try:
                task = game.get_task_by_name(args[1])
                #(self, name=None, link=None, price=None, info=None, answer="1337")
                clientsock.send(response(task_body.format(name=task.name, info=task.info, link=task.link)))
                clientsock.send(response('\ncmd: '))
            except Exception as ex:
                print ex
                clientsock.send(response('error!\ncmd: '))

        elif "user" == args[0]:
            if len(args)<1:
                print 'err'
                continue
            try:
                user = game.get_user_by_name(args[1])
                #(self, name=None, link=None, price=None, info=None, answer="1337")
                clientsock.send(response(profile_body.format(name=user.name, place=game.get_user_place(user),
                                                             tasks=user.solved_tasks_str(), score=user.score,
                                                             bonus=user.bonus)))
                clientsock.send(response('\ncmd: '))
            except Exception as ex:
                print ex
                clientsock.send(response('errno[15550]\ncmd: !'))

        elif "save" == args[0]:
            try:
                game.save()
                clientsock.send(response('Game successfully saved!\ncmd: '))
            except Exception as ex:
                print ex

        else:
            clientsock.send(response('\ncmd: '))
        # -- cmd --


    clientsock.close()
    print addr, "- closed connection" #log on console

if __name__=='__main__':
#def start_serv(game):

    # server settings
    BUFF = 1024
    HOST = ""#'127.0.0.1'
    PORT = 1337

    ADDR = (HOST, PORT)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)

    #TODO pasrse params

    # --  game settings --
    game = Game().load('DEBUG_2013-11-12')
    # --  game settings --

    while 1:
        print 'waiting for connection... listening on port', PORT
        clientsock, addr = serversock.accept()
        print '...connected from:', addr
        thread.start_new_thread(handler, (clientsock, addr))