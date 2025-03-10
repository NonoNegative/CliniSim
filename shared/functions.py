import customtkinter
import shared.customtk as customtk
import tkinter as tk
from shared.tkgif import GifLabel
from datetime import datetime
from shared.CTkPDFViewer import *

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

font=('Alte Haas Grotesk', 12)
def get_label_height(text, width):
    root = tk.Tk() 
    root.withdraw()  

    label = tk.Label(root, text=text, font=font, wraplength=width)
    label.update_idletasks()
    height = label.winfo_reqheight() 
    label.destroy()
    root.destroy()

    return height

def infer_image(img_path, window_name, size_x=None, size_y=None, attached_note="No further info was attached with this image.", load_captions=['Please Wait...', 500, 'Retrieving Image...', 2000, 'Processing...', 1000]):
    my_image = customtk.create_tk_image(img_path, size_x, size_y)
    width = my_image.width(); height = my_image.height()
    dynamic_note_ht = get_label_height(attached_note, width=width-20)
    note_button_height = 30; entry_height = 40; buttons_height = 30; padding = 50
    extra_height = note_button_height + dynamic_note_ht + entry_height + buttons_height + padding
    my_top = create_top_level(window_name, my_image.width() if size_x == None else size_x, my_image.height() + extra_height if size_y == None else size_y + extra_height, load_captions)
    my_top.canvas.create_image(0, 0, anchor=tk.NW, image=my_image)
    my_top.canvas.image = my_image
    my_top.canvas.create_line(10, height+20, width-15, height+20, fill='#e3e3e3', width=4)
    note_button = customtkinter.CTkButton(my_top, height=20, corner_radius=7, text='Attached Note', font=('Alte Haas Grotesk', 15, 'bold'), text_color='White')
    note_button.place(x=width/2, y=height+20, anchor=tk.CENTER)
    note_label = tk.Label(master=my_top, text=attached_note, fg='Grey40', bg='#f0f0f0', font=font, wraplength=width-20, justify='center')
    note_label.place(x=width/2, y=height+35, anchor=tk.N)
    my_top.canvas.create_line(10, height+note_button_height+dynamic_note_ht+15, width-15, height+note_button_height+dynamic_note_ht+15, fill='#e3e3e3', width=4)
    height = height+note_button_height+dynamic_note_ht+30
    inference_entry = customtkinter.CTkEntry(master=my_top.canvas, placeholder_text=" Do you infer anything from this result?", corner_radius=8, width=width-20, height=entry_height, bg_color='White', font=('Alte Haas Grotesk', 15, 'bold'), text_color='Grey25', placeholder_text_color='Grey50')
    inference_entry.place(x=10, y=height, anchor=tk.NW)
    save_button = customtkinter.CTkButton(my_top, height=30, corner_radius=6, text='Save', font=('Alte Haas Grotesk', 15, 'bold'), text_color='White', width=100)
    save_button.place(x=width-10, y=height+entry_height+10, anchor=tk.NE)
    discard_button = customtkinter.CTkButton(my_top, height=30, corner_radius=6, text='Discard', font=('Alte Haas Grotesk', 15, 'bold'), text_color='White', width=100, fg_color='IndianRed2', hover_color='IndianRed4')
    discard_button.place(x=width-120, y=height+entry_height+10, anchor=tk.NE)
    my_top.canvas.create_text(12, height+entry_height+40, text="Timestamp: "+ str(datetime.now()), font=('Cascadia Code', 10), fill='Grey60', anchor=tk.SW)

def open_pdf(title, location, p_width=1000, p_height=1414):
    my_top = create_top_level(title, 1000, 900, load_captions=['Reading Document...', 1000, 'Opening in Viewer...', 400])
    pdf_frame = CTkPDFViewer(my_top, file=location, page_width=p_width, page_height=p_height)
    pdf_frame.pack(fill="both", expand=True, padx=10, pady=10)
    my_top.mainloop()


 