import socket
from threading import Thread
from tkinter import *

# ip = "10.210.70.252"
ip = "192.168.1.4"
ip = "localhost"
port = 5000

def start_server():
    server_socket.bind((ip, port))
    server_socket.listen(5)

    while True:
        client_socket, client_address = server_socket.accept()
        clients[client_address] = client_socket  
        Thread(target=handle_client, args=(client_socket, client_address)).start()

def handle_client(client_socket, client_address):
    while True:
        try:
            msg_data = client_socket.recv(1024).decode("utf-8")
            if msg_data:
                msg, username, icon, color = msg_data.split('||')
                full_msg = f'{icon} {username} ({client_address[0]}): {msg}'
                display_msg(full_msg, 'left', color)
                broadcast(msg_data, client_socket)
            else:
                break
        except:
            break
    client_socket.close()

def display_msg(msg, justify, color):
    txt_chat.config(state=NORMAL)
    txt_chat.tag_configure(color, foreground=color)
    txt_chat.config(bg='black')
    txt_chat.insert(END, msg + "\n", (justify, color))
    txt_chat.config(state=DISABLED)

def broadcast(msg, sender_socket):
    closed_clients = []
    for client_address, client_socket in clients.items():
        if sender_socket is None or client_socket != sender_socket:
            try:
                client_socket.send(msg.encode("utf-8"))
            except socket.error:
                closed_clients.append(client_address)

    for client_address in closed_clients:
        del clients[client_address]

def on_enter(event=None):
    send_msg()

def send_msg():
    msg = txt_input.get()
    txt_input.delete(0, END)
    full_msg = f'Machine spirit: {msg}'
    display_msg(full_msg, 'right', 'blue')
    broadcast(f'{msg}||Server||🔧||blue', None)

root = Tk()
root.wm_iconbitmap("AnyConv.com__images.ico")
root.title("Mechanicus")

txt_chat = Text(root, state=DISABLED, bg='grey',width=80, height=20)
txt_chat.grid(row=0, column=0, padx=10, pady=10)
txt_chat.tag_configure('right', justify='right')
txt_chat.tag_configure('left', justify='left')

txt_input = Entry(root, width=50)
txt_input.grid(row=1, column=0, padx=10, pady=10)
txt_input.bind("<Return>", on_enter)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = {}

server_thread = Thread(target=start_server)
server_thread.start()

root.mainloop()

