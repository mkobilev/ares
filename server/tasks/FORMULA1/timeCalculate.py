#coding: utf-8
import random
import re
import socket
import datetime
import thread
HOST = ''
PORT = 9091
KEY = 'flag{498a7547xf91f4f1}'


def main(connect, address):
    print 'Client (IP: %s) connected!' % (str(address[0]) + ':' + str(address[1]))
    try:
        connect.send('Time for FORMULA 1!\n')
        task = TaskTimeCalculate()
        start = datetime.datetime.now()
        connect.send(str(task.trace) + '\n')
        cmd = ''
        while not cmd:
            cmd = connect.recv(1024)
        stop = datetime.datetime.now()
        try:
            number = int(cmd)
        except ValueError:
            number = -1
        if task.time == number:
            if (stop - start).seconds > 1:
                connect.send('The answer is correct, but too long! Try again!\n')
            else:
                connect.send(KEY)
        else:
            connect.send('Incorrect! Try again!\n')
        connect.close()
    except socket.error:
        print 'Something wrong with %s:%s' % (address[0], address[1])


#  Дана трасса в формате |<скорость><_>(каждое нижнее подчеркивание - 50 км)| нужно расчитать за сколько минут
#  можно преодолеть трасу, если двигаться с заданными скоростями
#  пример трассы: |20_______|40________|20______|60_______|90______|40_|20__|
class TaskTimeCalculate:
    def __init__(self):
        self.trace = self.get_trace()
        self.time = self.time_calculate()

    @staticmethod
    def get_trace():
        trace = '|'
        for piece in range(random.randint(3, 10)):
            trace += str(random.choice((20, 40, 60, 90)))
            trace += '_' * random.randint(1, 10) + '|'
        return trace

    def time_calculate(self):
        trace_list = re.findall('(\d+)([_]+)', self.trace)
        time = 0
        for speed, distance in trace_list:
            time += (len(distance) * 50) / int(speed)
        return time

if __name__ == '__main__':
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        thread.start_new_thread(main, (conn, addr))