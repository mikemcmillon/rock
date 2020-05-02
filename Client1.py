from Setup import *
import socket
import threading
import pickle

client_dict = {'player': '',
               'my_turn': False,
               'status': 'waiting',
               'move': ''}
server_dict = {'status': '',
               'P0_turn': True,
               'P0_play': '',
               'P1_turn': True,
               'P1_play': '',
               'winner': ''}

# Set up internet connection
try:
    SERVER = '13.84.132.23'
    PORT = 2200
    client = socket.socket()
    client.connect((SERVER, PORT))
    client_dict['player'] = pickle.loads(client.recv(1024))

except:
    print('Server Not Found')
    pygame.quit()
    quit()

def send_message():
    global playing
    try:
        client.send(pickle.dumps(client_dict))
    except:
        draw_text('', 190, 190, 270, 300)
        draw_text('Player 2 Left', 210, 200, 70, 20)
        draw_text('Click to', 210, 310, 70, 20)
        draw_text('Exit', 210, 360, 70, 20)
        pygame.display.update()
        playing = False
        pygame.quit()
        quit()

def recv_message():
    global server_dict, client_dict, playing
    while True:
        try:
            server_dict = pickle.loads(client.recv(2048))
            if client_dict['player'] == 0:
                client_dict['my_turn'] = server_dict['P0_turn']
            else:
                client_dict['my_turn'] = server_dict['P1_turn']

        except Exception as msg:
            break
    draw_text('', 190, 190, 270, 300)
    draw_text('Player 2 Left', 210, 200, 70, 20)
    draw_text('Click to', 210, 310, 70, 20)
    draw_text('Exit', 210, 360, 70, 20)
    pygame.display.update()
    pause()
    playing = False
    pygame.quit()
    quit()

def draw_screen():
    window.fill(CYAN)
    draw_text('Player 1', 10, 5, 170, 60)
    draw_text('vs', 300, 5, 50, 60)
    draw_text('Player 2', 470, 5, 170, 60)

    if client_dict['move'] == '':
        draw_text('Your Move', 200, 200, 230, 60)
    elif client_dict['move'] != '':
        draw_text('Waiting for', 200, 200, 230, 60)
        draw_text('Player 2', 250, 260, 180, 60)

    window.blit(rock, rectangles[0])
    window.blit(paper, rectangles[1])
    window.blit(scissors, rectangles[2])
    window.blit(rock, rectangles[3])
    window.blit(paper, rectangles[4])
    window.blit(scissors, rectangles[5])

    if client_dict['move'] == 'r':
        draw_circle(0)
    elif client_dict['move'] == 'p':
        draw_circle(1)
    elif client_dict['move'] == 's':
        draw_circle(2)

    if client_dict['player'] == 0 and client_dict['move'] != '':
        if server_dict['P1_play'] == 'r':
            draw_circle(3)
        elif server_dict['P1_play'] == 'p':
            draw_circle(4)
        elif server_dict['P1_play'] == 's':
            draw_circle(5)
    elif client_dict['player'] == 1 and client_dict['move'] != '':
        if server_dict['P0_play'] == 'r':
            draw_circle(3)
        elif server_dict['P0_play'] == 'p':
            draw_circle(4)
        elif server_dict['P0_play'] == 's':
            draw_circle(5)

    pygame.display.update()

    if server_dict['winner'] != '':
        draw_text('', 190, 190, 270, 300)
        if server_dict['winner'] == 't':
            draw_text('It\'s a TIE!', 210, 200, 70, 20)
            draw_text('Click to', 210, 310, 70, 20)
            draw_text('Continue', 210, 360, 70, 20)
        elif server_dict['winner'] == client_dict['player']:
            draw_text('You WON!!!', 210, 200, 70, 20)
            draw_text('Click to', 210, 310, 70, 20)
            draw_text('Continue', 210, 360, 70, 20)
        else:
            draw_text('You Lost :(', 210, 200, 70, 20)
            draw_text('Click to', 210, 310, 70, 20)
            draw_text('Continue', 210, 360, 70, 20)
        pygame.display.update()
        pause()


def draw_text(text, x, y, w, h):
    pygame.draw.rect(window, CYAN, (x, y, w, h))
    if len(text):
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(topleft = (x,y))
        window.blit(text_surface, text_rect)

def draw_circle(rps):
    if rps == 0:
        pygame.draw.circle(window, BLUE, (95, 155), 70, 2)
    elif rps == 1:
        pygame.draw.circle(window, BLUE, (95, 320), 70, 2)
    elif rps == 2:
        pygame.draw.circle(window, BLUE, (95, 485), 70, 2)
    elif rps == 3:
        pygame.draw.circle(window, BLUE, (555, 155), 70, 2)
    elif rps == 4:
        pygame.draw.circle(window, BLUE, (555, 320), 70, 2)
    elif rps == 5:
        pygame.draw.circle(window, BLUE, (555, 485), 70, 2)

def pause():
    keep_playing = False
    while not keep_playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                keep_playing = True
                draw_text('', 190, 190, 270, 300)
                client_dict['status'] = 'reset'
                client_dict['move'] = ''
                send_message()
                server_dict['winner'] = ''
                break

thread = threading.Thread(target=recv_message, args=(), daemon = True)
thread.start()
draw_screen()
send_message()
playing = True

while playing:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            playing = False
            break

        if client_dict['my_turn']:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for lcv in range(3):
                    if rectangles[lcv].collidepoint(event.pos):
                        client_dict['status'] = 'played'
                        if lcv == 0:
                            client_dict['move'] = 'r'
                        elif lcv == 1:
                            client_dict['move'] = 'p'
                        else:
                            client_dict['move'] = 's'
                        client_dict['my_turn'] = False
    if playing:
        draw_screen()
    send_message()

quit()
