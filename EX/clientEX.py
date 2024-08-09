# Client Code
import socket
from threading import Thread
from tkinter import *
import random

# ip="127.0.0.1"
# ip = "localhost"
ip = "192.168.1.4"
port=5000

def start_client():
    global client_socket
    while True:
        try:
            msg_data = client_socket.recv(1024).decode("utf-8")
            if msg_data:
                msg, username, icon, color = msg_data.split('||')
                full_msg = f'{icon} {username}: {msg}'
                display_msg(full_msg, color)
            else:
                break
        except:
            break
    client_socket.close()

def display_msg(msg, color):
    txt_chat.config(state=NORMAL)
    txt_chat.tag_configure(color, foreground=color)
    if username in msg:
        txt_chat.insert(END, msg + "\n", ('right', color))
    else:
        txt_chat.insert(END, msg + "\n", color)
    txt_chat.config(state=DISABLED)

def send_msg():
    msg = txt_input.get()
    txt_input.delete(0, END)
    full_msg = f'{msg}||{username}||{icon}||{color}'
    display_msg(f'{icon} {username}: {msg}', color)
    try:
        client_socket.send(full_msg.encode("utf-8"))
    except:
        pass

def on_enter(event=None):
    send_msg()

def login():
    global username, icon, color, client_socket, client_thread
    username = entry_username.get()
    icon = entry_icon.get()
    color = random.choice(colors)
    
    login_frame.pack_forget()
    chat_frame.pack()
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    
    client_thread = Thread(target=start_client)
    client_thread.start()

def logout():
    global client_socket, client_thread
    client_socket.close()
    chat_frame.pack_forget()
    login_frame.pack()


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))
client_thread = Thread(target=start_client)

colors = ['red', 'green', 'blue', 'orange', 'purple', 'pink']

root = Tk()
root.title("Client")
# root.configure(bg="lightgray")
# root.geometry('1280x850')
# root.resizable(width=FALSE, height=FALSE)

login_frame = Frame(root)
login_frame.pack()

label_username = Label(login_frame, text="Username:")
label_username.pack(pady=5)

entry_username = Entry(login_frame)
entry_username.pack(pady=5)

label_icon = Label(login_frame, text="Icon:")
label_icon.pack(pady=5)

entry_icon = Entry(login_frame)
entry_icon.pack(pady=5)

btn_login = Button(login_frame, text="Login", command=login)
btn_login.pack(pady=5)

chat_frame = Frame(root)
# chat_frame.pack(fill=BOTH, expand=True)

scrollbar = Scrollbar(chat_frame)
scrollbar.pack(side=RIGHT, fill=Y)

txt_chat = Text(chat_frame, state=DISABLED, yscrollcommand=scrollbar.set, bg = "lightgray")
txt_chat.pack(fill=BOTH, expand=True)

scrollbar.config(command=txt_chat.yview)

for color in colors:
    txt_chat.tag_configure(color, foreground=color)

txt_chat.tag_configure('right', justify='right')
txt_chat.tag_configure('left', justify='left')

txt_input = Entry(chat_frame, width=50)
txt_input.pack(fill=X, padx=10)
txt_input.bind("<Return>", on_enter)

btn_send = Button(chat_frame, text="Send", command=send_msg)
btn_send.pack(side=LEFT, padx=10, pady=10)

btn_logout = Button(chat_frame, text="Logout", command=logout)
btn_logout.pack(side=RIGHT, padx=10, pady=10)

client_thread = Thread(target=start_client)

root.mainloop()
