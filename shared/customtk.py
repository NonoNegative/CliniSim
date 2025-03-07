import tkinter as tk
from PIL import Image, ImageTk, ImageColor
import tkinter.messagebox as messagebox

def create_tk_image(img_path, size_x=None, size_y=None):
    image = Image.open(img_path)
    if size_x!=None and size_y!=None:
        image = image.resize((size_x, size_y), Image.Resampling.LANCZOS)
    image = ImageTk.PhotoImage(image)
    return image

def show_2_options(opt1, func1, opt2, func2):
    global option_toplevel
    try:
        option_toplevel.destroy()
    except Exception:
        pass
    option_toplevel = tk.Toplevel()
    option_toplevel.title("Choose an option")
    option_toplevel.config(bg="Grey20")
    screen_width = option_toplevel.winfo_screenwidth(); screen_height = option_toplevel.winfo_screenheight()
    width = 400; height = 100
    x = screen_width / 2 - width / 2; y = screen_height / 2 - height / 2
    option_toplevel.geometry('%dx%d+%d+%d' % (width, height, x, y))
    option_toplevel.resizable(False, False)
    button1 = tk.Button(option_toplevel, borderwidth=0, highlightthickness=0, text=opt1.upper(), relief='sunken', bg='grey25', activebackground='grey50', font=('Calibri', 11), justify='center', activeforeground='white', fg='grey80', command=func1)
    button1.place(x=0, y=10, width=400, height=35, anchor=tk.NW)
    button2 = tk.Button(option_toplevel, borderwidth=0, highlightthickness=0, text=opt2.upper(), relief='sunken', bg='grey25', activebackground='grey50', font=('Calibri', 11), justify='center', activeforeground='white', fg='grey80', command=func2)
    button2.place(x=0, y=55, width=400, height=35, anchor=tk.NW)
    def on_enter(btn):
        btn.config(bg='grey35', fg='white')
    def on_leave(btn):
        btn.config(bg='grey25', fg='grey80')
    button1.bind('<Enter>', lambda x: on_enter(button1)); button2.bind('<Enter>', lambda x: on_enter(button2))
    button1.bind('<Leave>', lambda x: on_leave(button1)); button2.bind('<Leave>', lambda x: on_leave(button2))

def quit_confirm(root):
    answer = messagebox.askyesno(title="Quit", message="Are you sure that you want to quit?")
    if answer:
        root.destroy()

def create_image_button(root, image_path, x, y, size_x, size_y, command=lambda *args: None, bg='#ffffff', active_bg='#ffffff', disable_btn_press_anim=False):
    img = create_tk_image(image_path, size_x, size_y)
    btn = tk.Button(root, image=img, bd=1, highlightthickness= 0, bg=bg, activebackground=active_bg, relief='flat', command= command)
    if disable_btn_press_anim == True:
        btn.config(borderwidth=0, relief='flat')
    btn.image = img ; btn.place(x=x, y=y, width=size_x, height=size_y, anchor=tk.NW)