import socket
import threading
import pickle
import os

SERVER = '13.84.132.23'
PORT = 2200

s = socket.socket()
s.bind((SERVER, PORT))


def client(conn, player):
    global server_dict, P0_conn, P1_conn
    conn.send(pickle.dumps(player))
    if player == 0:
        P0_conn = conn
    else:
        P1_conn = conn

    while True:
        try:
            client_dict = pickle.loads(conn.recv(2048))

            if client_dict['status'] == 'reset' or client_dict['status'] == 'waiting':
                server_dict['winner'] = ''
                if player == 0:
                    server_dict['P0_play'] = ''
                    server_dict['P0_turn'] = True
                else:
                    server_dict['P1_play'] = ''
                    server_dict['P1_turn'] = True

            if client_dict['status'] == 'played':
                if player == 0:
                    server_dict['P0_play'] = client_dict['move']
                    server_dict['P0_turn'] = False
                else:
                    server_dict['P1_play'] = client_dict['move']
                    server_dict['P1_turn'] = False

            if server_dict['status'] == 'play':
                check_winner()

            send_message()

        except:
            print('Connection Lost with player: ', player)
            if player == 0:
                P0_conn = ''
                server_dict['P0_play'] = ''
                server_dict['P0_turn'] = True
            else:
                P1_conn = ''
                server_dict['P1_play'] = ''
                server_dict['P1_turn'] = True
            break

    conn.close()

def send_message():
    global server_dict
    if P0_conn != "":
        P0_conn.send(pickle.dumps(server_dict))
        print('sending to conn 0')
    if P1_conn != "":
        P1_conn.send(pickle.dumps(server_dict))
        print('sending to conn 1')

def check_winner():
    if server_dict['P0_play'] != '' and server_dict['P1_play'] != '':
        if server_dict['P0_play'] == server_dict['P1_play']:
            server_dict['winner'] = 't'
        elif server_dict['P0_play'] == 'r' and server_dict['P1_play'] == 's':
            server_dict['winner'] = 0
        elif server_dict['P0_play'] == 'r' and server_dict['P1_play'] == 'p':
            server_dict['winner'] = 1
        elif server_dict['P0_play'] == 'p' and server_dict['P1_play'] == 'r':
            server_dict['winner'] = 0
        elif server_dict['P0_play'] == 'p' and server_dict['P1_play'] == 's':
            server_dict['winner'] = 1
        elif server_dict['P0_play'] == 's' and server_dict['P1_play'] == 'p':
            server_dict['winner'] = 0
        elif server_dict['P0_play'] == 's' and server_dict['P1_play'] == 'r':
            server_dict['winner'] = 1



def connections():
    global server_dict, P0_conn, P1_conn
    s.listen()
    while True:
        conn, addr = s.accept()

        if P0_conn == '':
            p = 0
            server_dict['status'] = 'wait'
        elif P1_conn == '':
            p = 1
            server_dict['status'] = 'play'
        print("Connected to player:", p)
        thread = threading.Thread(target=client, args=(conn, p))
        thread.start()


# Server Start Up
print('Server Running')
P0_conn = ''
P1_conn = ''
server_dict = {'status': '',
               'P0_turn': True,
               'P0_play': '',
               'P1_turn': True,
               'P1_play': '',
               'winner': ''}
thread = threading.Thread(target=connections)
thread.start()
