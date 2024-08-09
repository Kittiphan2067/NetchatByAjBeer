import socket
from threading import Thread
from tkinter import *
import random

ip="10.34.40.117"
# ip = "10.160.68.184"
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
    position = position_var.get()
    icon = f"{position}"  
    color = random.choice(colors)

    root.title(f"Client - {username}")

    login_frame.pack_forget()
    chat_frame.pack()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

    client_thread = Thread(target=start_client)
    client_thread.start()


def logout():
    global username, icon, color, client_socket, client_thread
    client_socket.close()
    chat_frame.pack_forget()
    login_frame.pack()
    username = ""
    icon = ""
    color = ""
    
    root.title("Client")


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))
client_thread = Thread(target=start_client)

colors = ['red', 'green', 'blue', 'orange']

root = Tk()
root.title("Client")
root.geometry("640x400")

login_frame = Frame(root)
login_frame.pack()

position_var = StringVar(root)
position_var.set("Select Position")

option_menu = OptionMenu(login_frame, position_var, "โปรแกรมเมอร์", "วิศวกร", "ดีไซเนอร์", "ผู้ทดสอบ", "แฮ็กเกอร์")
option_menu.pack(pady=5)

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

txt_chat = Text(chat_frame, state=DISABLED, bg='black', fg='white', width=80, height=20)
txt_chat.pack(padx=10, pady=10)

for color in colors:
    txt_chat.tag_configure(color, foreground=color)

txt_chat.tag_configure('right', justify='right')
txt_chat.tag_configure('left', justify='left')

txt_input = Entry(chat_frame, width=50)
txt_input.pack()
txt_input.bind("<Return>", on_enter)

btn_send = Button(chat_frame, text="Send", width=10, height=10, command=send_msg)
btn_send.pack(side=LEFT, padx=10, pady=10)

btn_logout = Button(chat_frame, text="Logout", width=10, height=10, command=logout)
btn_logout.pack(side=RIGHT, padx=10, pady=10)

client_thread = Thread(target=start_client)

root.mainloop()