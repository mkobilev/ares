#coding: utf-8
import random
import socket
import thread
import json
import datetime
KEY = 'flag{4e75906c57a929eb}'
HOST = ""
PORT = 9090
FOODS = [
    'apple',
    'orange',
    'banana',
    'milk',
    'meat',
    'chicken',
    'mayo',
    'sausage',
    'strawberry',
    'bread',
    'juice',
    'tomato',
    'potato',
    'electricity',
    'oil',
    'petrol',
    'rubber',
    'paper',
    'paint',
    'ground',
    'dirt',
    'wood'
]
  
  
# Роботы любят играть в игру Вкусное/Невкусное (ну или съедобное/несъедобное)
# Так как роботов много и предпочтения со вкусами у всех разные (прям как у людей!)
# по правилам игры в начале ведущий робот сообщает те вещи которые он считает вкусными (передается список строк)
# Затем ведущий говорит название предмета, а игрок должен ответить, вкусный он (tasty) или невкусный (tasteless)
# Однако у всех современных роботов мощные процессоры, поэтому даже секунда на раздумья для них очень большой срок
# и если игрок долго думает над ответом робот-ведущий считает, что игрок не знает правильный ответ.
def main(connect, address):
    print 'Client (IP: %s) connected!' % (str(address[0]) + ':' + str(address[1]))
    try:
        connect.send('Time for Tasty or Tasteless!\nWhat I find tasty:')
        task = TaskTastyOrTasteless()
        connect.send(str(json.dumps(task.tasty)))
        for i in range(11):
            food = random.choice(FOODS)
            tasty = 'tasty' if food in task.tasty else 'tasteless'
            connect.send(food + '\n')
            start = datetime.datetime.now()
            cmd = ''
            while not cmd:
                cmd = connect.recv(1024).lower()
            stop = datetime.datetime.now()
            if cmd != tasty:
                connect.send('Incorrect!')
                break
            elif (stop - start).seconds > 1:
                connect.send('Too long!')
                break
        else:
            connect.send(KEY)  # Флаг нннада
        connect.close()
    except socket.error:
        print 'Something wrong with %s:%s' % (address[0], address[1])
  
  
class TaskTastyOrTasteless:
    def __init__(self):
        self.tasty = self.get_tasty()
  
    @staticmethod
    def get_tasty():
        tasty = []
        for i in range(11):
            food = random.choice(FOODS)
            if not food in tasty:
                tasty.append(food)
        return tasty
  
if __name__ == '__main__':
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        thread.start_new_thread(main, (conn, addr))