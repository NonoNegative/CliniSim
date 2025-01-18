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
chat_log = []

existing_chat_canvas = None
def render_chat(scroll_index=0):

    # Redraw Canvas
    global chat_canvas, existing_chat_canvas
    if existing_chat_canvas != None:
        try:
            existing_chat_canvas.destroy()
        except Exception:
            pass
    chat_canvas = tk.Canvas(root, width=443, height=456, highlightthickness=0)
    chat_canvas.place(x=27,y=550)
    existing_chat_canvas = chat_canvas
    chat_canvas.create_image(-27, -550, anchor=tk.NW, image=background_image)
    chat_canvas.create_image(-27, -550, anchor=tk.NW, image=static_img)
    global my_triangle_icon, their_triangle_icon
    canvas.delete(start_chatting_icon)

    # Config
    my_chat_bubble_color = '#0a7cee'; my_chat_text_color = '#ffffff'
    their_chat_bubble_color = '#ffffff'; their_chat_text_color = '#4f4f4f'
    y_bound = 0; y_spacing = 20

    triangle_icon = Image.open("assets\\icons\\triangle.png")
    triangle_icon = triangle_icon.resize((10, 10), Image.Resampling.LANCZOS)
    alpha = triangle_icon.split()[-1]
    triangle_icon = triangle_icon.convert("RGB")

    # My chat (Blue default)
    my_triangle_icon = RGBTransform().mix_with(ImageColor.getcolor(my_chat_bubble_color, "RGB"),factor=1).applied_to(triangle_icon)
    my_triangle_icon.putalpha(alpha)
    my_triangle_icon = my_triangle_icon.rotate(90)
    my_triangle_icon = ImageTk.PhotoImage(my_triangle_icon)

    # Their chat (White default)
    their_triangle_icon = RGBTransform().mix_with(ImageColor.getcolor(their_chat_bubble_color, "RGB"),factor=1).applied_to(triangle_icon)
    their_triangle_icon.putalpha(alpha)
    their_triangle_icon = ImageTk.PhotoImage(their_triangle_icon)

    # Some quick math
    index_slice = range(scroll_index, len(chat_log))
    if len(index_slice)%2 == 0: 
        start_x = 33; start_y = 440
    else:
        start_x = 413; start_y = 440

    for index in index_slice:
        if start_x == 413:
            my_message = tk.Label(chat_canvas, text=chat_log[index], wraplength=300, font=('Alte Haas Grotesk', 11, 'bold'), bg=my_chat_bubble_color, fg=my_chat_text_color, justify='left', padx=0, pady=4)
            my_message.update(); my_message_height = my_message.winfo_reqheight(); my_message_width = my_message.winfo_reqwidth()
            if (start_y-my_message_height < y_bound):
                my_message.destroy(); break
            chat_canvas.create_oval(start_x-8, start_y-1, start_x+8, start_y-17, fill=my_chat_bubble_color, outline=my_chat_bubble_color)
            chat_canvas.create_oval(start_x-my_message_width-8, start_y-1, start_x-my_message_width+8, start_y-17, fill=my_chat_bubble_color, outline=my_chat_bubble_color)
            chat_canvas.create_oval(start_x-my_message_width-8, start_y-my_message_height+16, start_x-my_message_width+8, start_y-my_message_height, fill=my_chat_bubble_color, outline=my_chat_bubble_color)
            chat_canvas.create_rectangle(start_x-my_message_width-8, start_y-8, start_x-my_message_width, start_y-my_message_height+8, fill=my_chat_bubble_color, outline=my_chat_bubble_color, width=0)
            chat_canvas.create_rectangle(start_x, start_y-8, start_x+9, start_y-my_message_height, fill=my_chat_bubble_color, outline=my_chat_bubble_color, width=0)
            chat_canvas.create_image(start_x+8, start_y-my_message_height, anchor=tk.NW, image=my_triangle_icon)
            my_message.place(x=start_x, y=start_y, anchor=tk.SE)
            start_x = 33; start_y = start_y - my_message_height - y_spacing

        else:
            their_message = tk.Label(chat_canvas, text=chat_log[index], wraplength=300, font=('Alte Haas Grotesk', 11, 'bold'), bg=their_chat_bubble_color, fg=their_chat_text_color, justify='right', padx=0, pady=4)
            their_message.update(); their_message_height = their_message.winfo_reqheight(); their_message_width = their_message.winfo_reqwidth()
            if (start_y-their_message_height < y_bound):
                their_message.destroy(); break
            chat_canvas.create_oval(start_x-8, start_y-1, start_x+8, start_y-17, fill=their_chat_bubble_color, outline=their_chat_bubble_color)
            chat_canvas.create_oval(start_x+their_message_width-8, start_y-1, start_x+their_message_width+8, start_y-17, fill=their_chat_bubble_color, outline=their_chat_bubble_color)
            chat_canvas.create_oval(start_x+their_message_width-8, start_y-their_message_height+16, start_x+their_message_width+8, start_y-their_message_height, fill=their_chat_bubble_color, outline=their_chat_bubble_color)
            chat_canvas.create_rectangle(start_x+their_message_width, start_y-8, start_x+their_message_width+9, start_y-their_message_height+8, fill=their_chat_bubble_color, outline=their_chat_bubble_color, width=0)
            chat_canvas.create_rectangle(start_x-8, start_y-8, start_x, start_y-their_message_height, fill=their_chat_bubble_color, outline=their_chat_bubble_color, width=0)
            chat_canvas.create_image(start_x-8, start_y-their_message_height, anchor=tk.NE, image=their_triangle_icon)
            their_message.place(x=start_x, y=start_y, anchor=tk.SW)
            start_x = 413; start_y = start_y - their_message_height - y_spacing

def send_message(message):
    global chat_log
    chat_log.insert(0, message)
    chat_log.insert(0, '    ')
    render_chat()

chat_msg_var=tk.StringVar()
chat_msg_var.set("Ask about anything...")
chat_entry = tk.Entry(canvas, textvariable=chat_msg_var, font=('Alte Haas Grotesk', 12, 'bold'), width=41, background='#ffffff', bd=0, fg='#4f4f4f')
chat_entry.place(x=43, y=1021)
send_message_button = customtk.create_image_button(root, 'assets\\icons\\send.png', 433, 1022, 22, 22, bg='#3e3e3e', active_bg='#3e3e3e', disable_btn_press_anim=True, command=lambda: send_message(chat_msg_var.get()))

root.mainloop()