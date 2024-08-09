import socket
from threading import Thread
from tkinter import *
import random

# ip = "10.210.70.252"
# ip = "10.160.85.44"
# ip ="192.168.1.4"
ip = "localhost"
port = 5000

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

def send_emoji(emoji_name):
    full_msg = f'{emojis[emoji_name]}||{username}||{icon}||{color}'
    display_msg(f'{icon} {username}: {emojis[emoji_name]}', color)
    try:
        client_socket.send(full_msg.encode("utf-8"))
    except:
        pass

def on_ctrl_space(event):
    if (event.state & 0x4) and (event.keysym == 'space'):
        txt_input.insert(INSERT, "\n")  # เมื่อกด Ctrl+Space จะเพิ่มขึ้นบรรทัดใหม่

def on_enter(event=None):
    send_msg()

def login():
    global username, icon, color, client_socket, client_thread
    username = entry_username.get()
    position = position_var.get()
    icon = f"{position}"
    color = random.choice(colors)

    root.title(f"Imperial - {username}")

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

root = Tk()
root.wm_iconbitmap("AnyConv.com__40k_imperial_aquila__transparent__by_fuguestock_d91enql-fullview.ico")
root.title("Imperial")
root.geometry("640x400")

login_frame = Frame(root)
login_frame.pack()

position_var = StringVar(root)
position_var.set("เลือกตำแหน่ง")

colors = ['red', 'green', 'blue', 'orange', 'purple', 'white']

emojis = {
    "ยิ้ม": "😊",
    "โกรธ": "😡",
    "ร้องไห้": "😢",
    "สงสัย": "❓",
    "ตกใจ": "😲",
    "หัวใจ": "❤️",
    "ยกนิ้ว": "👍",
}

option_menu = OptionMenu(login_frame, position_var, "โปรแกรมเมอร์", "วิศวกร", "ดีไซเนอร์", "ผู้ทดสอบ", "แฮ็กเกอร์")
option_menu.pack(pady=5)

label_username = Label(login_frame, text="ชื่อผู้ใช้:")
label_username.pack(pady=5)

entry_username = Entry(login_frame)
entry_username.pack(pady=5)

btn_login = Button(login_frame, text="เข้าสู่ระบบ", command=login, bg='#bca845')
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
txt_input.bind("<Control-space>", on_ctrl_space)  # ผูกกับฟังก์ชันเมื่อกด Ctrl+Space
txt_input.bind("<Return>", on_enter)

btn_send = Button(chat_frame, text="ส่ง", command=send_msg, width=20, height=2, bg='#bca845')
btn_send.pack(side=LEFT, padx=5, pady=5)

btn_smile = Button(chat_frame, text=emojis["ยิ้ม"], command=lambda: send_emoji("ยิ้ม"), width=3, height=1)
btn_smile.pack(side=LEFT)

btn_angry = Button(chat_frame, text=emojis["โกรธ"], command=lambda: send_emoji("โกรธ"), width=3, height=1)
btn_angry.pack(side=LEFT)

btn_cry = Button(chat_frame, text=emojis["ร้องไห้"], command=lambda: send_emoji("ร้องไห้"), width=3, height=1)
btn_cry.pack(side=LEFT)

btn_question = Button(chat_frame, text=emojis["สงสัย"], command=lambda: send_emoji("สงสัย"), width=3, height=1)
btn_question.pack(side=LEFT)

btn_surprised = Button(chat_frame, text=emojis["ตกใจ"], command=lambda: send_emoji("ตกใจ"), width=3, height=1)
btn_surprised.pack(side=LEFT)

btn_heart = Button(chat_frame, text=emojis["หัวใจ"], command=lambda: send_emoji("หัวใจ"), width=3, height=1)
btn_heart.pack(side=LEFT)

btn_thumbs_up = Button(chat_frame, text=emojis["ยกนิ้ว"], command=lambda: send_emoji("ยกนิ้ว"), width=3, height=1)
btn_thumbs_up.pack(side=LEFT)

btn_logout = Button(chat_frame, text="ออกจากระบบ", command=logout, width=10, height=1, bg='#bca845')
btn_logout.pack(side=RIGHT, padx=5)

root.mainloop()
