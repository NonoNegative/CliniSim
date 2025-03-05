# -----------------Imports-----------------
import customtkinter
import shared.customtk as customtk
import tkinter as tk
import os, random
import json
from colorama import init as colorama_init
from termcolor import colored
from PIL import Image, ImageTk, ImageColor
from shared.transforms import RGBTransform
from datetime import datetime
from functools import partial
# -------------------End-------------------

print(colored(" START ", 'light_grey', 'on_dark_grey'), "Execution Timestamp:", colored(datetime.now(), 'dark_grey'))

# ---------------Load Settings------------
with open('settings.json') as my_settings_file:
    settings = json.load(my_settings_file)

# ------------------Theme------------------
colorama_init() # Initialize colorama for pretty printing
selected_color_theme = settings['theme'] # This is where the magic happens
customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
default_themes = {"blue":'#3B8ED0', "green":'#2CC985', "dark-blue":'#3A7EBF'}
if selected_color_theme in default_themes:
    customtkinter.set_default_color_theme(selected_color_theme)  # Default Themes: "blue" (standard), "green", "dark-blue"
    primary_color = default_themes[selected_color_theme] # Primary color of UI
    print(colored(" THEME ", 'white', 'on_magenta'),  f"Sucessfully Loaded: '{selected_color_theme.title()}' from default themes list.")
else:
    customtkinter.set_default_color_theme(f"themes\\{selected_color_theme}.json")  # Custom Themes: "themes\\xyz.json"
    theme_json = json.load(open(f"themes\\{selected_color_theme}.json"))
    primary_color = theme_json['CTkButton']['fg_color'][0] # Primary color of UI
    print(colored(" THEME ", 'light_grey', 'on_magenta'),  f"Sucessfully Loaded: '{selected_color_theme.title()}' from path" , colored(f"'themes\\{selected_color_theme}.json'", 'dark_grey'))
    del theme_json # Why waste memory?
# -------------------End-------------------

#-----------------Load Content-------------

# Load drugs and tests
drug_list = settings["drugs"]
test_list = settings["tests"]
with open('content\\medicines\\medicines.json') as file:
    drug_dict = json.load(file)

# Load settings

root = customtkinter.CTk()
root.title("CliniSim")
root.attributes('-fullscreen', True)

screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

# -----------------UI Initialize-----------------
canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.pack()

background_image = customtk.create_tk_image('assets\\backgrounds\\sample.jpg', screen_width, screen_height)
canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

static_img = customtk.create_tk_image('assets\\static\\static_v2.png', screen_width, screen_height)
canvas.create_image(0, 0, anchor=tk.NW, image=static_img)

color_static = Image.open("assets\\static\\color.png")
color_static = color_static.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
alpha = color_static.split()[-1]
color_static = color_static.convert("RGB")
color_static = RGBTransform().mix_with(ImageColor.getcolor(primary_color, "RGB"),factor=1).applied_to(color_static)
color_static.putalpha(alpha)
color_static = ImageTk.PhotoImage(color_static)
canvas.create_image(0, 0 ,anchor=tk.NW, image=color_static)
# ------------------------End------------------------

# -----------------Patient Intialize-----------------
patient = random.choice(os.listdir("content\\patients")) # Select a random patient
patient_id = int(patient.rstrip(".json"))
patient = json.load(open(f"content\\patients\\{patient}")) # Parse JSON to Dictionary
print(colored(" INFO ", 'black', 'on_yellow'),  f"Selected Patient: {patient['name']} [ID: {patient_id}] from path" , colored(f"'content\\patients\\{patient_id}.json'", 'dark_grey'))

# Update Profile
canvas.create_line(150, 65, 387, 65, fill='White', width=1); canvas.create_line(150, 105, 387, 105, fill='White', width=1)
canvas.create_text(152, 71, text=patient['name'], font=('Alte Haas Grotesk', 17, 'bold'), fill='Grey30', anchor=tk.NW)
patient_headshot = customtk.create_tk_image(f"content\\avatars\\{patient_id}.png", 100, 100)
canvas.create_image(30, 66, image=patient_headshot, anchor=tk.NW)
canvas.create_text(205, 126, text=patient['age'], font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey30', anchor=tk.W, justify='left')
canvas.create_text(233, 159, text=patient['gender'], font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey30', anchor=tk.W, justify='left')
canvas.create_text(88, 192, text=patient['case'], font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey30', anchor=tk.NW, justify='left', width=300)
# ------------------------End------------------------

# -----------------Profile and History Buttons-----------------
full_profile_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\full_profile.png"),
                                  dark_image=Image.open("assets\\icons\\full_profile.png"),
                                  size=(20, 20))

full_profile_button = customtkinter.CTkButton(master=canvas, image=full_profile_icon, text='View Full Profile', compound=tk.LEFT, font=('Alte Haas Grotesk', 15, 'bold'), width=387, height=33, corner_radius=8, bg_color='White', border_color='White')
full_profile_button.place(x=12, y=265)

medical_records_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\full_profile.png"),
                                  dark_image=Image.open("assets\\icons\\full_profile.png"),
                                  size=(20, 20))

medical_records_button = customtkinter.CTkButton(master=canvas, image=medical_records_icon, text='View Medical Records', compound=tk.LEFT, font=('Alte Haas Grotesk', 15, 'bold'), width=387, height=33, corner_radius=8, bg_color='White', border_color='White')
medical_records_button.place(x=12, y=305)

canvas.create_line(13, 350, 397, 350, fill='#e7e7e7', width=4)
# -----------------------------End-----------------------------

start_chatting_icon_tk = customtk.create_tk_image('assets\\icons\\start_chatting.png', 135, 133)
start_chatting_icon = canvas.create_image(207, 804, anchor=tk.CENTER, image=start_chatting_icon_tk)
chat_log = [
    "Hi!",
    "Hello! How's it going?",
    "I'm doing well, thanks for asking. How about you?",
    "I'm good too! Just busy with work.",
    "Ah, I get that. What are you working on?",
    "Just some coding projects. Nothing too exciting.",
    "That sounds interesting! What kind of projects?",
    "Mostly web development stuff. React and Django.",
    "Nice! I've been thinking about learning React.",
    "You should! It's pretty fun once you get the hang of it."
]

chat_log.reverse()

can_scroll = False; scroll_index = 0
existing_chat_canvas = None
def render_chat():

    # Redraw Canvas
    global chat_canvas, existing_chat_canvas, can_scroll
    if existing_chat_canvas != None:
        try:
            existing_chat_canvas.destroy()
        except Exception:
            pass
    chat_canvas = tk.Canvas(root, width=366, height=483, highlightthickness=0, background='#e7e7e7')
    chat_canvas.place(x=22,y=539)
    existing_chat_canvas = chat_canvas
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
        start_x = 18; start_y = 470
    else:
        start_x = 348; start_y = 470

    for index in index_slice:
        if start_x == 348:
            my_message = tk.Label(chat_canvas, text=chat_log[index], wraplength=275, font=('Alte Haas Grotesk', 11, 'bold'), bg=my_chat_bubble_color, fg=my_chat_text_color, justify='left', padx=0, pady=4)
            my_message.update(); my_message_height = my_message.winfo_reqheight(); my_message_width = my_message.winfo_reqwidth()
            if (start_y-my_message_height < y_bound):
                can_scroll = True
                my_message.destroy(); break
            chat_canvas.create_oval(start_x-8, start_y-1, start_x+8, start_y-17, fill=my_chat_bubble_color, outline=my_chat_bubble_color)
            chat_canvas.create_oval(start_x-my_message_width-8, start_y-1, start_x-my_message_width+8, start_y-17, fill=my_chat_bubble_color, outline=my_chat_bubble_color)
            chat_canvas.create_oval(start_x-my_message_width-8, start_y-my_message_height+16, start_x-my_message_width+8, start_y-my_message_height, fill=my_chat_bubble_color, outline=my_chat_bubble_color)
            chat_canvas.create_rectangle(start_x-my_message_width-8, start_y-8, start_x-my_message_width, start_y-my_message_height+8, fill=my_chat_bubble_color, outline=my_chat_bubble_color, width=0)
            chat_canvas.create_rectangle(start_x, start_y-8, start_x+9, start_y-my_message_height, fill=my_chat_bubble_color, outline=my_chat_bubble_color, width=0)
            chat_canvas.create_image(start_x+8, start_y-my_message_height, anchor=tk.NW, image=my_triangle_icon)
            my_message.place(x=start_x, y=start_y, anchor=tk.SE)
            start_x = 18; start_y = start_y - my_message_height - y_spacing
            can_scroll = False

        else:
            their_message = tk.Label(chat_canvas, text=chat_log[index], wraplength=275, font=('Alte Haas Grotesk', 11, 'bold'), bg=their_chat_bubble_color, fg=their_chat_text_color, justify='left', padx=0, pady=4)
            their_message.update(); their_message_height = their_message.winfo_reqheight(); their_message_width = their_message.winfo_reqwidth()
            if (start_y-their_message_height < y_bound):
                can_scroll = True
                their_message.destroy(); break
            chat_canvas.create_oval(start_x-8, start_y-1, start_x+8, start_y-17, fill=their_chat_bubble_color, outline=their_chat_bubble_color)
            chat_canvas.create_oval(start_x+their_message_width-8, start_y-1, start_x+their_message_width+8, start_y-17, fill=their_chat_bubble_color, outline=their_chat_bubble_color)
            chat_canvas.create_oval(start_x+their_message_width-8, start_y-their_message_height+16, start_x+their_message_width+8, start_y-their_message_height, fill=their_chat_bubble_color, outline=their_chat_bubble_color)
            chat_canvas.create_rectangle(start_x+their_message_width, start_y-8, start_x+their_message_width+9, start_y-their_message_height+8, fill=their_chat_bubble_color, outline=their_chat_bubble_color, width=0)
            chat_canvas.create_rectangle(start_x-8, start_y-8, start_x, start_y-their_message_height, fill=their_chat_bubble_color, outline=their_chat_bubble_color, width=0)
            chat_canvas.create_image(start_x-8, start_y-their_message_height, anchor=tk.NE, image=their_triangle_icon)
            their_message.place(x=start_x, y=start_y, anchor=tk.SW)
            start_x = 348; start_y = start_y - their_message_height - y_spacing
            can_scroll = False

render_chat()

chat_entry = customtkinter.CTkEntry(master=canvas, placeholder_text=" Ask about anything...", corner_radius=8, width=346, height=38, bg_color='White', font=('Alte Haas Grotesk', 15, 'bold'), text_color='Grey30')
chat_entry.place(x=12, y=1033)

send_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\send.png"),
                                  dark_image=Image.open("assets\\icons\\send.png"),
                                  size=(17, 17))

send_button = customtkinter.CTkButton(master=canvas, image=send_icon, text='', width=35, height=37, corner_radius=8, bg_color='White', border_color='White', fg_color='Grey30', hover_color='Grey25')
send_button.place(x=363, y=1033)

search_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\search.png"),
                                  dark_image=Image.open("assets\\icons\\search.png"),
                                  size=(17, 17))

drug_search_entry = customtkinter.CTkEntry(master=canvas, placeholder_text="Search for a drug...", corner_radius=8, width=221, height=32, bg_color='White', font=('Alte Haas Grotesk', 13))
drug_search_entry.place(x=1628, y=101)

drug_search_button = customtkinter.CTkButton(master=canvas, image=search_icon, text='', width=50, height=33, corner_radius=8, bg_color='White', border_color='White')
drug_search_button.place(x=1854, y=100)

tabview_1 = customtkinter.CTkTabview(master=canvas, width=280, height=240, bg_color='White', corner_radius=7)
tabview_1._segmented_button.configure(font=('Alte Haas Grotesk', 15, 'bold'))
tabview_1.place(x=1628, y=134)
tabview_1.add("All"); tabview_1.add("Search Results")

# Tab 1 ("All")
drug_list_canvas = tk.Canvas(tabview_1.tab("All"), width=252, height=187, highlightthickness=0, background=tabview_1.cget('fg_color')[0])
drug_list_canvas.place(x=0, y=0)
scroll_bar = customtkinter.CTkScrollbar(tabview_1.tab("All"), command=drug_list_canvas.yview, height=195)
drug_list_canvas.config(yscrollcommand=scroll_bar.set)
scroll_bar.place(x=254, y=-4)

def generate_tab_1():
    global drug_list_canvas
    y = 0  # Initial y pos
    for drug in drug_list:
        drug_button = customtkinter.CTkButton(master=drug_list_canvas, text=drug, font=('Alte Haas Grotesk', 15, 'bold'), width=252, height=33, corner_radius=7, bg_color=tabview_1.cget('fg_color')[0])
        drug_list_canvas.create_window(0, y, window=drug_button, anchor=tk.NW)
        y = y + 38
    root.update()
    drug_list_canvas.configure(scrollregion=drug_list_canvas.bbox("all"))

test_search_entry = customtkinter.CTkEntry(master=canvas, placeholder_text="Search fr a test...", corner_radius=8, width=221, height=32, bg_color='White', font=('Alte Haas Grotesk', 13))
test_search_entry.place(x=1628, y=438)

test_search_button = customtkinter.CTkButton(master=canvas, image=search_icon, text='', width=50, height=33, corner_radius=8, bg_color='White', border_color='White')
test_search_button.place(x=1854, y=437)

tabview_2 = customtkinter.CTkTabview(master=canvas, width=280, height=240, bg_color='White', corner_radius=7)
tabview_2._segmented_button.configure(font=('Alte Haas Grotesk', 15, 'bold'))
tabview_2.place(x=1628, y=471)
tabview_2.add("Tests"); tabview_2.add("Imaging")

# Tab 1 ("All")
test_list_canvas = tk.Canvas(tabview_2.tab("Tests"), width=252, height=187, highlightthickness=0, background=tabview_2.cget('fg_color')[0])
test_list_canvas.place(x=0, y=0)
scroll_bar_2 = customtkinter.CTkScrollbar(tabview_2.tab("Tests"), command=test_list_canvas.yview, height=195)
test_list_canvas.config(yscrollcommand=scroll_bar_2.set)
scroll_bar_2.place(x=254, y=-4)

def generate_tab_2():
    global test_list_canvas
    y = 0  # Initial y pos
    for test in test_list:
        test_button = customtkinter.CTkButton(master=test_list_canvas, text=test, font=('Alte Haas Grotesk', 15, 'bold'), width=252, height=33, corner_radius=7, bg_color=tabview_2.cget('fg_color')[0])
        test_list_canvas.create_window(0, y, window=test_button, anchor=tk.NW)
        y = y + 38
    root.update()
    test_list_canvas.configure(scrollregion=test_list_canvas.bbox("all"))

test_search_entry = customtkinter.CTkEntry(master=canvas, placeholder_text="Search for a test...", corner_radius=8, width=221, height=32, bg_color='White', font=('Alte Haas Grotesk', 13))
test_search_entry.place(x=1628, y=438)

test_search_button = customtkinter.CTkButton(master=canvas, image=search_icon, text='', width=50, height=33, corner_radius=8, bg_color='White', border_color='White')
test_search_button.place(x=1854, y=437)

scroll_up_button = customtkinter.CTkButton(master=canvas, text='▲', width=20, height=20, corner_radius=5, bg_color='#e7e7e7', border_color='#e7e7e7', anchor='center', border_spacing=0, border_width=0, fg_color='Grey30', hover_color='Grey25')
scroll_up_button.place(x=500, y=500)

scroll_down_button = customtkinter.CTkButton(master=canvas, text='▼', width=20, height=20, corner_radius=5, bg_color='#e7e7e7', border_color='#e7e7e7', anchor='center', border_spacing=0, border_width=0, fg_color='Grey30', hover_color='Grey25')
scroll_down_button.place(x=500, y=600)

generate_tab_1()
generate_tab_2()

root.mainloop()

