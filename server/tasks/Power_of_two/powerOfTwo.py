#coding: utf-8
import random
import socket
import thread
import datetime
HOST = ''
PORT = 9092
KEY = 'flag{66bd8ec61345512d}'


def main(connect, address):
    print 'Client (IP: %s) connected!' % (str(address[0]) + ':' + str(address[1]))
    try:
        connect.send('Time for search power of 2!\n')
        task = TaskPowerOfTwo()
        start = datetime.datetime.now()
        connect.send(str(task.number) + '\n')
        cmd = ''
        while not cmd:
            cmd = connect.recv(1024)
        stop = datetime.datetime.now()
        try:
            number = int(cmd)
        except ValueError:
            number = -1
        if task.check_power(number):
            if (stop - start).seconds > 1:
                connect.send('The answer is correct, but too long! Try again!\n')
            else:
                connect.send(KEY)
        else:
            connect.send('Incorrect! Try again!\n')
        connect.close()
    except socket.error:
        pass


#                      Найти ближайшую к числу снизу степень 2
class TaskPowerOfTwo:
    def __init__(self):
        self.number = random.randint(3, 10000000)
        self.near_power = self.find_power()

    def find_power(self, number=None):
        num = number or self.number
        count = -1
        while num > 0:
            num /= 2
            count += 1
        return 2**count

    def check_power(self, power):
        return True if self.near_power == power else False

if __name__ == '__main__':
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        thread.start_new_thread(main, (conn, addr))