# import customtkinter
import shared.customtk as customtk
import tkinter as tk
from shared.tkgif import GifLabel

def create_top_level(title, width=600, height=600, load_captions=['Loading', 2000], bg_color='#f0f0f0'):
    image_toplevel = tk.Toplevel(); image_toplevel.wm_attributes('-toolwindow', 'true')
    image_toplevel.title(title)
    image_toplevel.config(bg=bg_color)
    screen_width = image_toplevel.winfo_screenwidth(); screen_height = image_toplevel.winfo_screenheight()
    x = screen_width / 2 - width / 2; y = screen_height / 2 - height / 2
    image_toplevel.geometry('%dx%d+%d+%d' % (width, height, x, y))
    image_toplevel.resizable(False, False)
    image_toplevel.attributes('-topmost', True)

    if load_captions != None:
        gif_label = GifLabel(image_toplevel, bd=0)
        gif_label.place(x=width/2, y=(height/2)-40, anchor=tk.CENTER)
        gif_label.load("assets\\icons\\loading.gif")
        load_caption = tk.Label(image_toplevel, text='', font=('Alte Haas Grotesk', 14), bg='#f0f0f0', fg='grey30', borderwidth=0)
        load_caption.place(x=width/2, y=(height/2)+55, anchor=tk.CENTER)

        def update_label(index=0):
            if index < len(load_captions):
                load_caption.config(text=load_captions[index])
                delay = load_captions[index + 1]
                load_caption.after(delay, update_label, index + 2)
            else:
                for widget in image_toplevel.winfo_children():
                    widget.destroy()
                image_toplevel.canvas = tk.Canvas(image_toplevel, width=width, height=height, highlightthickness=0)
                image_toplevel.canvas.place(x=0, y=0)
                image_toplevel.quit()

        update_label()
        image_toplevel.mainloop() 

    return image_toplevel

def check_vitals(vitals):
    my_top = create_top_level('Vitals Check', 600, 600, ['Please Wait...', 500, 'Checking Body Vitals...', 2000, 'Processing...', 1000])
    vitals_overlay = customtk.create_tk_image('assets\\static\\vitals_overlay.png', 600, 600)
    my_top.canvas.create_image(0, 0, anchor=tk.NW, image=vitals_overlay)
    my_top.canvas.image = vitals_overlay
    pos_dict = {"Temp":[280, 254], "Pulse":[746, 254], "SPO2":[277, 545], "BP":[746, 545], "Resp":[272, 834]}
    for key, (x, y) in pos_dict.items():
        value = vitals.get(key, "N/A")
        my_top.canvas.create_text(x*0.6, y*0.6, text=value, font=('Alte Haas Grotesk', 12, 'bold'), fill='grey30', anchor='nw')

def get_label_height(text, width, font=('Alte Haas Grotesk', 12)):
    root = tk.Tk() 
    root.withdraw()  

    label = tk.Label(root, text=text, font=font, wraplength=width)
    label.update_idletasks()
    height = label.winfo_reqheight() 
    label.destroy()
    root.destroy()

    return height

def view_image(img_path, size_x=None, size_y=None, attached_note=None, load_captions=['Please Wait...', 500, 'Retrieving Image...', 2000, 'Processing...', 1000]):
    my_image = customtk.create_tk_image(img_path)
    my_top = create_top_level('Vitals Check', my_image.width() if size_x == None else size_x, my_image.height() if size_y == None else size_y, load_captions)
    my_top.canvas.create_image(0, 0, anchor=tk.NW, image=my_image)
    my_top.canvas.image = my_image