import threading
import socket
import sys
import random
from threading import Timer, Thread, Event

# from Tools.scripts.mailerdaemon import x

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
list_clients = {}
# Bind the socket to the port
address = (192.168.42.15, 45870)
# print (sys.stderr, 'starting up on %s port %s' % 192.168.42.15)
sock.bind(address)


class perpetualTimer():

    def init(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()


class ServerManager:
    def init(self, sizX, sizY, numOfClients):
        self.sizX = sizX
        self.sizY = sizY
        self.snakes = {}
        #need to change
        self.filler = {0: [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]],
                       1: [[self.sizX - 1, 0], [self.sizX - 2, 0], [sizX - 3, 0], [sizX - 4, 0], [sizX - 5, 0]],
                       2: [[0, self.sizY - 5], [0, self.sizY - 4], [0, self.sizY - 3], [0, self.sizY - 2],
                           [0, self.sizY - 1]], 3: [[self.sizX - 1, self.sizY - 5], [self.sizX - 1, self.sizY - 4],
                                                    [self.sizX - 1, self.sizY - 3], [self.sizX - 1, self.sizY - 2],
                                                    [self.sizX - 1, self.sizY - 1]]}
        self.counter = 0
        self.numOfClients = numOfClients
        self.crown = []
        self.banana = []
        self.blocks = new_block()

        initboard()
        fill_snakes()
    #need explaine
    def new_block():
        block_list = []
        for i in range(0, 3):
            block_pos = [random.randrange(1, ((frame_size_x - 3) // 10)) * 10,
                         random.randrange(1, (frame_size_y // 10)) * 10]
            block_list.append(block_pos)
            block_pos = [block_pos[0] + 10, block_pos[1]]
            block_list.append(block_pos)
            block_pos = [block_pos[0] + 10, block_pos[1]]
            block_list.append(block_pos)
        for i in range(0, 3):
            block_pos = [random.randrange(1, ((frame_size_x) // 10)) * 10,
                         random.randrange(1, (frame_size_y // 10)) * 10]
            block_list.append(block_pos)
            block_pos = [block_pos[0], block_pos[1] + 10]
            block_list.append(block_pos)
            block_pos = [block_pos[0], block_pos[1] + 10]
            block_list.append(block_pos)
        return block_list
    #not needed any more
    def initboard(self):
        self.board = [[0 for i in range(self.sizX)] for j in range(self.sizY)]
        for i in range(0, self.sizX):
            self.board[0][i] = -1
        for i in range(0, self.sizY):
            self.board[i][0] = -1
        for i in range(0, self.sizX):
            self.board[self.sizY][i] = -1
        for i in range(0, self.sizY):
            self.board[i][self.sizX] = -1

    def fill_snakes(self):
        # add snakes
        for i in range(self.numOfClients):
            self.snakes.append(self.filler.get(i))

#need explaine
def send_start_message(game1):
    massge = "start#"
    for x, y in game1.snakes.items():
        massge = massge + str(x) + str(y) + "#"
    return massge + str(game1.sizX) + "#"+game1.blocks
    str(game1.sizy)


def eaten(id):
    ''' check if he ate'''
    return True


def send_update_message(game1):
    string = "update#"
    for i in range(len(game1.snakes)):
        string = string + str(i) + ","
        if(eaten(i)): string=string+"1"+","
        else: string=string+"0"+","
        string = string + str(game1.snake[i][0]) + "#"
    return string + str(game1.banana) + "#" + str(game1.crown)

#for clinte
def parss_ok_msg(data):
    my_id = data.split(",")[1]

#for clinte
def parss_start_msg(data):

    for i in range(1, data.count("#") - 3):  # posiible bad math
         snake_body_everyone[i - 1] = data.split("#")[i]
    frame_size_x = data.split("#")[data.count("#") - 2]
    frame_size_y = data.split("#")[data.count("#") - 1]

#for clinte TO DO for server too
def parss_update_msg(data):
    for i in range(1, data.count("#") - 4):  # posiible bad math
        snake_pos_everyone[i - 1] = data.split("#")[i]
    is_he_king = data.split("#")[data.count("#") - 2]
    block_list = data.split("#")[data.count("#") - 1]
    banana_list = data.split("#")[data.count("#") - 3]


def parse(data):
    if data.split('#')[0] == "update": update(data)
    if data.split('#')[0] == "start": start(data)
    if data.split("#")[0] == "ok": ok()
    #if data.split("#")[0] == "nop":
    #if data.split("#")[0] == "join": join()


def parse(data):
    if data.split('#')[0] == "update": update(data)
    if data.split('#')[0] == "start": start(data)
    if data.split("#")[0] == "ok": ok()
   # if data.split("#")[0] == "nop": nop()
    if data.split("#")[0] == "join": join(game1)


def join(game1):
    if game1.numOfClients <= 4:
        sock.sendto("ok," + str(game1.numOfClients), (address))
        game1.numOfClients = game1.numOfClients + 1
        game1.fill_snakes()
    else:
        sock.sendto("nop", (address)


def bind_socket(game1):
    while True:
        data, address = sock.recvfrom(1024)
        list_clients.append(address)
        parse(data)


def start_game(game1):
    string = send_start_message(game1)
    bind_socket(game1)
    t = perpetualTimer(0.3, update_game)


def update_game(game1):
    for i in list_clients:
        sock.sendto(send_message(), (i))


game1 = ServerManager(50, 50, 4)
open_game(game1)
