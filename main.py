import tkinter as tk
from PIL import Image, ImageTk, ImageColor
import tkinter.messagebox as messagebox
from shared.transforms import RGBTransform
import shared.customtk as customtk
import json
import os
import sys

root = tk.Tk()
root.title("CliniSim")
root.attributes('-fullscreen', True)
# icon = tk.PhotoImage(file='images\\icon.png')
# root.iconphoto(True, icon)

screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

background_image = Image.open('assets\\backgrounds\\sample.jpg')
background_image = background_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
background_image = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.pack()

canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

def show_info(text, color):
    canvas.delete('drawerinfo')
    canvas.create_text(screen_width-5, 34, text=text, font=('Helvetica', '10', 'bold'), fill=color, anchor=tk.NE, tags='drawerinfo')

drawer_icon = Image.open("assets\\icons\\drawer.png")
drawer_icon = drawer_icon.resize((169, 38), Image.Resampling.LANCZOS)
alpha = drawer_icon.split()[-1]
drawer_icon = drawer_icon.convert("RGB")
drawer_icon = RGBTransform().mix_with(ImageColor.getcolor('#232323', "RGB"),factor=1).applied_to(drawer_icon)
drawer_icon.putalpha(alpha)
drawer_icon = ImageTk.PhotoImage(drawer_icon)
canvas.create_image(screen_width+55, -6 ,anchor=tk.NE, image=drawer_icon)

close = customtk.create_tk_image('assets\\icons\\close_small.jpg', 19, 19)
minimize = customtk.create_tk_image('assets\\icons\\minimize_small.jpg', 19, 19)
test = customtk.create_tk_image('assets\\icons\\test_small.jpg', 19, 19)

close_button = tk.Button(canvas, image=close, bd=0, highlightthickness= 0, bg="#232323", relief=tk.SUNKEN, highlightcolor='#232323', activebackground='#232323', command=lambda: customtk.quit_confirm(root))
close_button.image = close; close_button.place(x=screen_width-5, y=5, width=20, height=20, anchor=tk.NE)

minimize_button = tk.Button(canvas, image=minimize, bd=0, highlightthickness= 0, bg="#232323", relief=tk.SUNKEN, highlightcolor='#232323', activebackground='#232323', command=root.iconify)
minimize_button.image = minimize; minimize_button.place(x=screen_width-35, y=5, width=20, height=20, anchor=tk.NE)

test_button = tk.Button(canvas, image=test, bd=0, highlightthickness= 0, bg="#232323", relief=tk.SUNKEN, highlightcolor='#232323', activebackground='#232323')
test_button.image = test; test_button.place(x=screen_width-65, y=5, width=20, height=20, anchor=tk.NE)

close_button.bind('<Enter>', lambda x: show_info('Close', 'IndianRed2')); close_button.bind('<Leave>', lambda x: show_info('', 'IndianRed2'))
minimize_button.bind('<Enter>', lambda x: show_info('Minimize', 'Gold')); minimize_button.bind('<Leave>', lambda x: show_info('', 'Gold'))
test_button.bind('<Enter>', lambda x: show_info('Configure/Launcher', 'Pale Green')); test_button.bind('<Leave>', lambda x: show_info('', 'Pale Green'))

static_img = customtk.create_tk_image('assets\\static\\static_v1.png', 1920, 1080)
canvas.create_image(0, 0, anchor=tk.NW, image=static_img)

start_chatting_icon_tk = customtk.create_tk_image('assets\\icons\\start_chatting.png', 135, 133)
start_chatting_icon = canvas.create_image(260, 790, anchor=tk.CENTER, image=start_chatting_icon_tk)
img = customtk.create_image_button(root, 'assets\\icons\\send.png', 433, 1022, 22, 22, bg='#3e3e3e', active_bg='#3e3e3e', disable_btn_press_anim=True)

chat_msg_var=tk.StringVar()
chat_entry = tk.Entry(canvas, textvariable=chat_msg_var, font=('Alte Haas Grotesk', 15, 'bold'), width=31, background='#ffffff', bd=0, fg='#4f4f4f')
chat_entry.place(x=39, y=1019)

root.mainloop()