# -----------------Imports-----------------
import customtkinter
import shared.customtk as customtk
import tkinter as tk
import os, random
import json
import time
import shared.functions as ext_funcs
from colorama import init as colorama_init
from termcolor import colored
from PIL import Image, ImageTk, ImageColor
from shared.transforms import RGBTransform
from datetime import datetime
from functools import partial
from tkVideoPlayer import TkinterVideo
from tkinter import messagebox
from shared.action_history import dll as action_history
import asyncio
# -------------------End-------------------

force_disease = 'angelman'
debug = False
dont_render_video = False

if not debug:
    from ollama import AsyncClient
    from shared.tkgif import GifLabel

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
# --------------------End-------------------

#-----------------Load Content--------------
# Load drugs and tests, imaging, etc...
with open('content\\drugs\\drugs.json') as drugs_file:
    drug_dict = json.load(drugs_file)

with open('content\\tests\\tests.json') as tests_file:
    test_dict = json.load(tests_file)

with open('content\\imaging\\imaging.json') as imaging_file:
    imaging_dict = json.load(imaging_file)

drug_list = []; test_list  = []; imaging_list = []
for var, dictionary in zip([drug_list, test_list, imaging_list], [drug_dict, test_dict, imaging_dict]):
    for i in dictionary:
        var.append(i)

# Load settings
root = customtkinter.CTk()
root.title("CliniSim")
root.attributes('-fullscreen', True)

screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

# -----------------UI Initialize-----------------
canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.pack()

background_image = customtk.create_tk_image('assets\\backgrounds\\ccc.png', 1205, 1080)
canvas.create_image(408, 0, anchor=tk.NW, image=background_image)

# -----------------Patient Intialize-----------------
disease_id = random.choice(os.listdir("content\\diseases")) # Select a random patient
if force_disease != None:
    disease_id = force_disease
disease_json = json.load(open(f"content\\diseases\\{disease_id}\\{disease_id}.json")) # Parse JSON to Dictionary
patient = disease_json["Patient"]
print(colored(" INFO ", 'black', 'on_yellow'),  f"Selected Patient: {patient['name']} [ID: {disease_id}] from path" , colored(f"'content\\diseases\\{disease_id}\\{disease_id}.json'", 'dark_grey'))

# Load Animation
if not dont_render_video:
    video_player = TkinterVideo(canvas, borderwidth=0, bg='Black', fg='black', consistant_frame_rate=True)
    video_player.set_size((1205, 980))
    video_player.place(x=408, y=100, anchor=tk.NW)
    video_player.bind("<<Loaded>>", lambda e: e.widget.config(width=1205, height=980))
    #video_player.bind("<<SecondChanged>>", lambda e: print(video_player.current_frame_number()))
    video_player.load(f"content\\diseases\\{disease_id}\\test.mp4")

    def start_video():
        video_player.seek(0)
        video_player.play()
        root.after(7000, start_video)
        video_player.update_idletasks()

    start_video()

static_img = customtk.create_tk_image('assets\\static\\static_v3.png', screen_width, screen_height)
canvas.create_image(0, 0, anchor=tk.NW, image=static_img)

color_static = Image.open("assets\\static\\color.png")
color_static = color_static.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
alpha = color_static.split()[-1]
color_static = color_static.convert("RGB")
color_static = RGBTransform().mix_with(ImageColor.getcolor(primary_color, "RGB"),factor=1).applied_to(color_static)
color_static.putalpha(alpha)
color_static = ImageTk.PhotoImage(color_static)
canvas.create_image(0, 0 ,anchor=tk.NW, image=color_static)

drawer_width = 215; drawer_height = 42
drawer_edge_1 = customtk.create_tk_image("assets\\icons\\drawer.png", drawer_height, drawer_height)
drawer_edge_2 = customtk.create_tk_image("assets\\icons\\drawer.png", drawer_height, drawer_height, flip=1)
canvas.create_rectangle((screen_width-drawer_width)//2, 0, (screen_width+drawer_width)//2, drawer_height, fill='#f3f3f3', width=0)
canvas.create_image((screen_width-drawer_width)//2, 0 ,anchor=tk.NE, image=drawer_edge_1)
canvas.create_image((screen_width+drawer_width)//2, 0 ,anchor=tk.NW, image=drawer_edge_2)

time_limit = settings['time_limit']
time_elapsed = 0

def update_timer():
    global time_elapsed
    time_elapsed += 1
    ScoreL.configure(text='🕑 '+time.strftime('%M:%S', time.gmtime(time_elapsed)))
    if time_elapsed < time_limit:
        # schedule next update 1 second later
        canvas.after(1000, update_timer)
    else:
        messagebox.showerror("Time's Up!", "Time's Up!\n\nPatient was not revived on time.")
        quit()

ScoreL = tk.Label(canvas, text='🕑 '+time.strftime('%M:%S', time.gmtime(time_elapsed)), bg='#f3f3f3', fg='Grey30', font=("Alte Haas Grotesk", 15, 'bold'), justify='left')
ScoreL.place(x=((screen_width-drawer_width)//2) - 12, y=5, anchor=tk.NW)
canvas.after(1000, update_timer)

eye_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\eye.png"),
                                dark_image=Image.open("assets\\icons\\eye.png"),
                                size=(20, 20))

canvas.create_line(((screen_width)//2)-26, 4, ((screen_width)//2)-26, drawer_height-4, fill='#e3e3e3', width=4)

# ------------------------End------------------------

# -------------------Update Profile------------------
canvas.create_line(150, 65, 387, 65, fill='White', width=1); canvas.create_line(150, 105, 387, 105, fill='White', width=1)
canvas.create_text(152, 71, text=patient['name'], font=('Alte Haas Grotesk', 17, 'bold'), fill='Grey30', anchor=tk.NW)
patient_headshot = customtk.create_tk_image(f"content\\diseases\\{disease_id}\\avatar.png", 100, 100)
canvas.create_image(30, 66, image=patient_headshot, anchor=tk.NW)
canvas.create_text(205, 126, text=patient['age'], font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey30', anchor=tk.W, justify='left')
canvas.create_text(233, 159, text=patient['gender'], font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey30', anchor=tk.W, justify='left')
canvas.create_text(88, 189, text=patient['case'], font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey30', anchor=tk.NW, justify='left', width=300)
# ------------------------End------------------------

# -----------------Profile and History Buttons-----------------
full_profile_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\full_profile.png"),
                                  dark_image=Image.open("assets\\icons\\full_profile.png"),
                                  size=(20, 20))

full_profile_button = customtkinter.CTkButton(master=canvas, image=full_profile_icon, text='View Full Profile', compound=tk.LEFT, font=('Alte Haas Grotesk', 15, 'bold'), width=387, height=33, corner_radius=8, bg_color='White', border_color='White', command= lambda: ext_funcs.open_pdf('Patient Profile', f'content\\diseases\\{disease_id}\\profile.pdf', p_height=1250))
full_profile_button.place(x=12, y=265)

medical_records_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\medical_records.png"),
                                  dark_image=Image.open("assets\\icons\\medical_records.png"),
                                  size=(20, 20))

medical_records_button = customtkinter.CTkButton(master=canvas, image=medical_records_icon, text='View Action History', compound=tk.LEFT, font=('Alte Haas Grotesk', 15, 'bold'), width=387, height=33, corner_radius=8, bg_color='White', border_color='White', command=lambda: ext_funcs.show_action_history(disease_json['Expected Procedure']))
medical_records_button.place(x=12, y=305)

canvas.create_line(13, 350, 397, 350, fill='#e7e7e7', width=4)
# -----------------------------End-----------------------------

# --------------------------Chat Log---------------------------
start_chatting_icon_tk = customtk.create_tk_image('assets\\icons\\start_chatting.png', 135, 133)
start_chatting_icon = canvas.create_image(207, 804, anchor=tk.CENTER, image=start_chatting_icon_tk)
chat_log = []
ollama_log = settings['ollama_log']
ollama_log[0]["content"] = disease_json["Initial_prompt"]
# -----------------------------End-----------------------------

# -----------------------Chat Rendering------------------------
can_scroll = False; scroll_index = 0
existing_chat_canvas = None

clip_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\clipboard.png"),
                                  dark_image=Image.open("assets\\icons\\clipboard.png"),
                                  size=(20, 20))

def render_chat(stride=0):
    # Redraw Canvas
    global chat_canvas, existing_chat_canvas, can_scroll, scroll_index

    #print(scroll_index, can_scroll, existing_chat_canvas, stride)
    '''if scroll_index == 0 and existing_chat_canvas == None:
        pass
    elif can_scroll == True and stride > 0:
        scroll_index = scroll_index + stride
    elif scroll_index > 0 and stride < 0:
        scroll_index = scroll_index + stride
    else:
        return None'''

    if existing_chat_canvas != None:
        try:
            existing_chat_canvas.destroy()
        except Exception:
            pass

    chat_canvas = tk.Canvas(root, width=351, height=483, highlightthickness=0, background='#e7e7e7')
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
        start_x = 333; start_y = 470

    for index in index_slice:
        if start_x == 333:
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
            clip_button = customtkinter.CTkButton(master=chat_canvas, image=clip_icon, text='', width=15, height=31, corner_radius=8, anchor=tk.CENTER, bg_color='#e7e7e7', fg_color='#e7e7e7', hover_color='#404040', command= lambda their_message_text=chat_log[index]: add_to_clip(their_message_text)) 
            clip_button.place(x=start_x+their_message_width+15, y=start_y-their_message_height, anchor=tk.NW)
            start_x = 333; start_y = start_y - their_message_height - y_spacing
            can_scroll = False
    chat_canvas.update_idletasks()

if not debug:
    async def chat_with_ollama(message):
        response = await AsyncClient().chat(model='llama3.2', messages=ollama_log+[{'role': 'user', 'content': message}])
        ollama_log.extend([
            {'role': 'user', 'content': message},
            {'role': 'assistant', 'content': response.message.content}])
        return response['message']['content']
    
    can_send_message = True
    def bot_reply(message):
        global ind, can_send_message, chat_log
        chat_log[0] = message
        #print(chat_log)
        render_chat()
        can_send_message = True

    def wait_for_message():
        chat_log.insert(0, '       ')
        render_chat()
        gif_label = GifLabel(chat_canvas, bd=0)
        gif_label.place(x=20, y=462, anchor=tk.SW)
        gif_label.load("assets\\icons\\waiting_2.gif")
        chat_canvas.after(1600, lambda: bot_reply(asyncio.run(chat_with_ollama(chat_log[1]))))

def send_message(message):
    if debug:
        return
    global chat_log, can_send_message
    if can_send_message == True:
        can_send_message = False
        chat_msg_var.set("")
        chat_log.insert(0, message)
        render_chat()
        chat_canvas.after(500, wait_for_message)
# -----------------------------End-----------------------------

# -----------------------Initialize Chat-----------------------
chat_msg_var=tk.StringVar()
chat_entry = customtkinter.CTkEntry(master=canvas, textvariable=chat_msg_var, placeholder_text=" Ask about anything...", corner_radius=8, width=346, height=38, bg_color='White', font=('Alte Haas Grotesk', 15, 'bold'), text_color='Grey30')
chat_msg_var.set(" Ask about anything...")
chat_entry.place(x=12, y=1033)

send_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\send.png"),
                                  dark_image=Image.open("assets\\icons\\send.png"),
                                  size=(17, 17))

send_button = customtkinter.CTkButton(master=canvas, image=send_icon, text='', width=35, height=37, corner_radius=8, bg_color='White', border_color='White', fg_color='Grey30', hover_color='Grey25', command=lambda: send_message(chat_msg_var.get()))
send_button.place(x=363, y=1033)

scroll_up_button = customtkinter.CTkButton(master=root, text='▲', width=20, height=20, corner_radius=5, bg_color='#e7e7e7', border_color='#e7e7e7', anchor='center', border_spacing=0, border_width=0, fg_color='Grey30', hover_color='Grey25', command=lambda: render_chat(1))
scroll_up_button.place(x=376, y=538)

scroll_down_button = customtkinter.CTkButton(master=root, text='▼', width=20, height=20, corner_radius=5, bg_color='#e7e7e7', border_color='#e7e7e7', anchor='center', border_spacing=0, border_width=0, fg_color='Grey30', hover_color='Grey25', command=lambda: render_chat(-1))
scroll_down_button.place(x=376, y=1004)
# -----------------------------End-----------------------------

# ----------------------Custom Clipboard-----------------------
my_clips = ["You can leave notes here or clip a chat..."] # This stores all the clips

clipboard_up_button = customtkinter.CTkButton(master=root, text='▲', width=20, height=20, corner_radius=5, bg_color='#e7e7e7', border_color='#e7e7e7', anchor='center', border_spacing=0, border_width=0, fg_color='Grey30', hover_color='Grey25', command= lambda: navigate_notes('up'))
clipboard_up_button.place(x=376, y=362)

clipboard_down_button = customtkinter.CTkButton(master=root, text='+', width=20, height=20, corner_radius=5, bg_color='#e7e7e7', border_color='#e7e7e7', anchor='center', border_spacing=0, border_width=0, fg_color='Grey30', hover_color='Grey25', command= lambda: navigate_notes('down'))
clipboard_down_button.place(x=376, y=458)

clipboard_icon = Image.open("assets\\icons\\clipboard.png")
clipboard_icon = clipboard_icon.resize((20, 20), Image.Resampling.LANCZOS)
alpha = clipboard_icon.split()[-1]
clipboard_icon = clipboard_icon.convert("RGB")
clipboard_icon = RGBTransform().mix_with(ImageColor.getcolor('#404040', "RGB"),factor=1).applied_to(clipboard_icon)
clipboard_icon.putalpha(alpha)
clipboard_icon = ImageTk.PhotoImage(clipboard_icon)
canvas.create_image(387, 412, image=clipboard_icon, anchor=tk.CENTER)

clip_label = tk.Label(master=canvas, text='1', bg='#e7e7e7', fg='#404040', borderwidth=0, font=('Alte Haas Grotesk', 10, 'bold'), justify='center')
clip_label.place(x=387, y=432, anchor=tk.CENTER)

clip_entry = customtkinter.CTkTextbox(master=root, corner_radius=0, width=355, height=111, bg_color='#e7e7e7', fg_color='#e7e7e7', font=('Alte Haas Grotesk', 15, 'bold'), text_color='Grey50', activate_scrollbars=True, wrap=tk.WORD)

def on_entry_click(event):
   if clip_entry.get('1.0', tk.END).strip() == "You can leave notes here or clip a chat...":
      clip_entry.delete('1.0', tk.END)
      clip_entry.configure(text_color="Grey30")

def on_focus_out(event):
   if clip_entry.get('1.0', tk.END).strip() == "":
      clip_entry.insert('1.0', "You can leave notes here or clip a chat...")
      clip_entry.configure(text_color="Grey50")

clip_entry.insert(tk.END, "You can leave notes here or clip a chat...")
clip_entry.bind("<FocusIn>", on_entry_click)
clip_entry.bind("<FocusOut>", on_focus_out)

clip_entry.place(x=18, y=365)

current_index = 0
def navigate_notes(direction):
    global current_index, clip_entry

    my_clips[current_index] =  clip_entry.get('1.0', tk.END)

    if direction == "up":
        if current_index > 0:
            current_index -= 1
        else:
            return None
    elif direction == "down":
        if current_index < len(my_clips) - 1:
            current_index += 1
        else:
            my_clips.append("")  # Create a new note
            current_index += 1
    elif isinstance(direction, int):
        current_index = direction

    if current_index == len(my_clips) - 1:
        clipboard_down_button.configure(text='+')
    else:
        clipboard_down_button.configure(text='▼')
    
    clip_label.config(text=str(current_index+1))
    clip_entry.configure(text_color="Grey30")
    clip_entry.delete('1.0', tk.END)
    clip_entry.insert('1.0', my_clips[current_index].strip())

def add_to_clip(text):
    my_clips.append(text)
    navigate_notes(len(my_clips) - 1)
# -----------------------------End-----------------------------

search_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\search.png"),
                                  dark_image=Image.open("assets\\icons\\search.png"),
                                  size=(17, 17))

def create_scroll_canvas(tabview, tabname, array, type):
    list_canvas = tk.Canvas(tabview.tab(tabname), width=252, height=187, highlightthickness=0, background=tabview_1.cget('fg_color')[0])
    list_canvas.place(x=0, y=0)
    scroll_bar = customtkinter.CTkScrollbar(tabview.tab(tabname), command=list_canvas.yview, height=195)
    list_canvas.config(yscrollcommand=scroll_bar.set)
    scroll_bar.place(x=254, y=-4)
    y = 0  # Initial y pos
    mapping = {}
    specifics = disease_json.get(tabname, {})
    if array == test_list:
        mapping = test_dict 
    elif array == imaging_list:
        mapping = imaging_dict
    mapping.update(specifics)

    for entry in array:
        attributes = mapping.get(entry, [])
        if type == 'test':
            image_path = ''; image_note = 'No further info was attached with this image.'
            try:
                image_path = attributes[0]
                image_note = attributes[1]
            except Exception:
                pass
            button = customtkinter.CTkButton(master=list_canvas, text=entry, font=('Alte Haas Grotesk', 15, 'bold'), width=252, height=33, corner_radius=7, bg_color=tabview_1.cget('fg_color')[0], command=lambda path=image_path, note=image_note, entry=entry: ext_funcs.infer_image(path, entry, attached_note=note))
        elif type == 'drug':
            button = customtkinter.CTkButton(master=list_canvas, text=entry, font=('Alte Haas Grotesk', 15, 'bold'), width=252, height=33, corner_radius=7, bg_color=tabview_1.cget('fg_color')[0], command=partial(update_calibrate_tab, entry))
        list_canvas.create_window(0, y, window=button, anchor=tk.NW)
        y = y + 38
    list_canvas.configure(scrollregion=list_canvas.bbox("all"))
    return list_canvas

# ------------------------Important Checks----------------------
physical_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\measurement.png"),
                                  dark_image=Image.open("assets\\icons\\measurement.png"),
                                  size=(20, 20))

physical_button = customtkinter.CTkButton(master=canvas, image=physical_icon, text='Physical Assessment', compound=tk.LEFT, font=('Alte Haas Grotesk', 15, 'bold'), width=287, height=33, corner_radius=8, bg_color='White', border_color='White', command = lambda: ext_funcs.physical_assessment(disease_json["Features"]))
physical_button.place(x=1624, y=48)

vitals_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\vitals.png"),
                                  dark_image=Image.open("assets\\icons\\vitals.png"),
                                  size=(20, 20))

vitals_button = customtkinter.CTkButton(master=canvas, image=vitals_icon, text='Vitals Check', compound=tk.LEFT, font=('Alte Haas Grotesk', 15, 'bold'), width=287, height=33, corner_radius=8, bg_color='White', border_color='White', command= lambda: ext_funcs.check_vitals(patient['vitals']))
vitals_button.place(x=1624, y=88)

canvas.create_line(1624, 133, 1911, 133, fill='#e7e7e7', width=4)
# -----------------------------End------------------------------

# -----------------------Drug Search Column---------------------
tabview_1 = customtkinter.CTkTabview(master=canvas, width=280, height=240, bg_color='White', corner_radius=7)
tabview_1._segmented_button.configure(font=('Alte Haas Grotesk', 15, 'bold'))
tabview_1.place(x=1628, y=223)
tabview_1.add("All"); tabview_1.add("Search Results")

drug_search_entry = customtkinter.CTkEntry(master=canvas, placeholder_text="Search for a drug...", corner_radius=8, width=221, height=32, bg_color='White', font=('Alte Haas Grotesk', 13))
drug_search_entry.place(x=1628, y=190)

cur_search_window = None
def drug_search_fn(term):
    global cur_search_window
    if cur_search_window != None:
        cur_search_window.destroy()
    cur_search_window = create_scroll_canvas(tabview_1, "Search Results", ext_funcs.search_list(term, drug_list), 'drug')
    tabview_1.set("Search Results")


drug_search_button = customtkinter.CTkButton(master=canvas, image=search_icon, text='', width=50, height=33, corner_radius=8, bg_color='White', border_color='White', command=lambda: drug_search_fn(drug_search_entry.get()))
drug_search_button.place(x=1854, y=189)
# -----------------------------End------------------------------

# -------------------------Desc Column--------------------------
prescribe_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\administer.png"),
                                dark_image=Image.open("assets\\icons\\administer.png"),
                                size=(20, 20))

prescribe_button = customtkinter.CTkButton(master=canvas, image=prescribe_icon, text='Prescribe', compound=tk.LEFT, font=('Alte Haas Grotesk', 15, 'bold'), width=280, height=33, corner_radius=8, bg_color='White', border_color='White')
prescribe_button.place(x=1628, y=638)

drug_name_label = customtkinter.CTkLabel(master=canvas, text="None", font=('Alte Haas Grotesk', 12, 'bold'), width=162, height=23, corner_radius=6, bg_color='White', fg_color="#e7e7e7", text_color='Grey25')
drug_name_label.place(x=1745, y=527, anchor=tk.NW)

prescribe_button.configure(command= lambda: ext_funcs.prescribe(drug_name_label.cget('text')))

drug_desc_label = customtkinter.CTkLabel(master=canvas, text="Select a drug to view its description.", font=('Alte Haas Grotesk', 12), width=160, height=74, bg_color='White', fg_color="White", wraplength=162, justify='left', anchor=tk.NW, text_color='Grey20')
drug_desc_label.place(x=1747, y=554, anchor=tk.NW)

none_tk_image = customtk.create_tk_image('assets\\icons\\none.png', 80, 80)

drug_image = tk.Label(canvas, background='White', fg='White', borderwidth=0, image=none_tk_image)
drug_image.place(x=1642, y=539, anchor=tk.NW)

def update_calibrate_tab(drug):
    global drug_tk_image
    drug_tk_image = customtk.create_tk_image(f'content\\drugs\\{drug}.png', 80, 80)
    drug_image.config(image=drug_tk_image)
    drug_name_label.configure(text=drug)
    drug_desc_label.configure(text=drug_dict[drug])

create_scroll_canvas(tabview_1, "All", drug_list, 'drug')
# -----------------------------End------------------------------

# -----------------------Test Search Column---------------------
tabview_2 = customtkinter.CTkTabview(master=canvas, width=280, height=240, bg_color='White', corner_radius=7)
tabview_2._segmented_button.configure(font=('Alte Haas Grotesk', 15, 'bold'))
tabview_2.place(x=1628, y=780)
tabview_2.add("Imaging"); tabview_2.add("Tests")

test_search_entry = customtkinter.CTkEntry(master=canvas, placeholder_text="Search for a test...", corner_radius=8, width=221, height=32, bg_color='White', font=('Alte Haas Grotesk', 13))
test_search_entry.place(x=1628, y=747)

test_search_button = customtkinter.CTkButton(master=canvas, image=search_icon, text='', width=50, height=33, corner_radius=8, bg_color='White', border_color='White')
test_search_button.place(x=1854, y=746)

create_scroll_canvas(tabview_2, "Tests", test_list, 'test')
create_scroll_canvas(tabview_2, "Imaging", imaging_list, 'test')
# -----------------------------End------------------------------

# --------------------------Diagnose----------------------------
diag_entry = customtkinter.CTkEntry(master=canvas, placeholder_text=" Diagnose...", corner_radius=8, width=242, height=38, bg_color='White', font=('Alte Haas Grotesk', 15, 'bold'), text_color='Grey30')
diag_entry.place(x=1628, y=1033)

diag_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\check.png"),
                                  dark_image=Image.open("assets\\icons\\check.png"),
                                  size=(17, 17))
def incorrect_guess(val):
    if val.replace(' ', '') == '':

        action_history.append(["Incorrectly Diagnosed", 'No input'])
    else:
        action_history.append(["Incorrectly Diagnosed", val])
    messagebox.showerror("Incorrect diagnosis!", "Incorrect diagnosis!\n\nThat is not the right answer!")

def correct_guess():
    if disease_json['Disease'] == 'Marfan Syndrome':
        ext_funcs.calc_systemic_score(disease_json['Disease'], disease_json['Systemic Score'])
    else:
        messagebox.showinfo("Correctly Diagnosed!", f"Congratulations!\n\nYou have correctly identified {disease_json['Disease']}.\n\nYou may now end the simulation.")

diag_button = customtkinter.CTkButton(master=canvas, image=diag_icon, text='', width=35, height=37, corner_radius=8, bg_color='White', border_color='White', fg_color='Grey30', hover_color='Grey25', command= lambda: correct_guess() if (diag_entry.get().lower)() in disease_json['Guesses'] else incorrect_guess(diag_entry.get()))
diag_button.place(x=1874, y=1033)
# -----------------------------End------------------------------

async def final_score():
    global score
    if debug:
        ext_funcs.show_final_score(random.randint(0, 100), 'This is a test.')
        return None
    
    dll_e_string = '\n'.join([' | '.join(map(str, sublist)) for sublist in disease_json['Expected Procedure']])
    dll_m_string = '\n'.join([' | '.join(map(str, sublist)) for sublist in action_history.to_list()])

    message = {'role': 'user', 'content': f'I want you to compare these 2 operational procedures for {disease_json["Disease"]} diagnosis. This is the expected procedure of diagnosis: \n{dll_e_string}\n\n And the following procedure is the what the user has performed: \n{dll_m_string}\n\n Compare these two and give a score out of 100 for the user on how accurate their replication of the actual procedure is. Reply with ONLY the score and feedback/explanation. Provide a feedback and explanation of why you gave that score in the following format: "<score>.<feedback>", for example "70.<your feedback>". Nothing else should be said in your message. You may not be so generous in your grading and you must give the user a low score if user performs poorly. However, make sure your feedback is positive and be uplifting to the user. You shall not use any special characters, however you may use the hyphen (-) as bullet points. You can address the user by saying second person pronouns like "you". Make sure your feedback is neatly formatted in bullet points (-). Do not use any formatting language or syntaxes like < > because your reponse is going to be shown as very raw text. IMPORTANT NOTE: Do not consider the first simulation started block in the procedure. It simply exists to mark the beginning of the procedure. Do not get confused or mix up between the expected procedure and users own procedure.'
            }
    response = await AsyncClient().chat(model='llama3.2', messages=[message])
    
    print(response['message']['content'])
    score = int(response['message']['content'][:2])
    comment = response['message']['content'][3:]

    ext_funcs.show_final_score(score, comment)

finish_button = customtkinter.CTkButton(canvas, height=30, corner_radius=10, text='Finish', font=('Alte Haas Grotesk', 15, 'bold'), text_color='White', width=70, command=lambda: asyncio.run(final_score()))
finish_button.place(x=((screen_width+drawer_width)//2)+12, y=5, anchor=tk.NE)
halt_button = customtkinter.CTkButton(canvas, height=30, corner_radius=10, text='Halt', font=('Alte Haas Grotesk', 15, 'bold'), text_color='White', width=60, fg_color='IndianRed2', hover_color='IndianRed4', command=quit)
halt_button.place(x=((screen_width+drawer_width)//2)-63, y=5, anchor=tk.NE)

root.mainloop()