import customtkinter
import shared.customtk as customtk
import tkinter as tk
from shared.tkgif import GifLabel
from datetime import datetime
from shared.CTkPDFViewer import *
from tkinter import messagebox
from shared.action_history import dll as action_history

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
    action_history.append(["Checked Patient's Vitals"])
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

def infer_save(top_lvl, key, value):
    top_lvl.destroy()
    if value == '' or value == ' Do you infer anything from this result?':
        action_history.append([f'Analyzed {key} Results'])
    else:
        action_history.append([f'Analyzed {key} Results', value])
    messagebox.showinfo("Save successful", "Your inference has been recorded!")

def temp_untop(win, func):
    win.attributes('-topmost', False)
    if func() == True:
        win.attributes('-topmost', True)
        return True
    win.attributes('-topmost', True)

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
    save_button = customtkinter.CTkButton(my_top, height=30, corner_radius=6, text='Save', font=('Alte Haas Grotesk', 15, 'bold'), text_color='White', width=100, command= lambda: infer_save(my_top, window_name, inference_entry.get()))
    save_button.place(x=width-10, y=height+entry_height+10, anchor=tk.NE)
    discard_button = customtkinter.CTkButton(my_top, height=30, corner_radius=6, text='Discard', font=('Alte Haas Grotesk', 15, 'bold'), text_color='White', width=100, fg_color='IndianRed2', hover_color='IndianRed4', command = lambda: my_top.destroy() if temp_untop(my_top, lambda: messagebox.askyesno("Discard changes?", "Are you sure you want to discard your changes?")) else None)
    discard_button.place(x=width-120, y=height+entry_height+10, anchor=tk.NE)
    my_top.canvas.create_text(12, height+entry_height+40, text="Timestamp: "+ str(datetime.now()), font=('Cascadia Code', 10), fill='Grey60', anchor=tk.SW)

def open_pdf(title, location, p_width=1000, p_height=1414):
    action_history.append(["Viewed Patient Profile"])
    my_top = create_top_level(title, 1000, 900, load_captions=['Reading Document...', 1000, 'Opening in Viewer...', 400])
    pdf_frame = CTkPDFViewer(my_top, file=location, page_width=p_width, page_height=p_height)
    pdf_frame.pack(fill="both", expand=True, padx=10, pady=10)
    my_top.mainloop()    

def save_presc(my_top, drug, dose_val, dose_int):
    my_top.destroy()
    if dose_int == 'Select...' or dose_val.strip() == '':
        messagebox.showerror("Error!", "Invalid or empty parameters passed!")
    else:
        action_history.append([f'Prescribed {drug}', f'{dose_val} | {dose_int}'])
        messagebox.showinfo("Prescription successful", "Your prescription has been recorded!")

def prescribe(drug):

    if drug == "None":
        return None

    my_top = create_top_level(f'Prescription', 400, 205, load_captions=['Please wait...', 200])
    my_top.canvas.create_text(200, 30, text=f'Prescribe {drug}', font=("Century Gothic", 15, 'bold'), fill='Grey20')
    my_top.canvas.create_line(10, 60, 390, 60, fill='#3B8ED0', width=4)
    my_top.canvas.create_text(190, 90, text='Dosing Interval :', font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey50', anchor=tk.E)
    my_top.canvas.create_text(190, 125, text='Recommended Dose :', font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey50', anchor=tk.E)
    my_top.canvas.create_line(10, 150, 390, 150, fill='#3B8ED0', width=4)

    combobox_1 = customtkinter.CTkComboBox(
        my_top.canvas, values=[
                                "Once Daily (OD)",
                                "Twice Daily (BID)",
                                "Three Times Daily (TID)",
                                "Four Times Daily (QID)",
                                "Every 4 Hours (Q4H)",
                                "As Needed (PRN)"
                            ],
        width=160, height=25, font=('Alte Haas Grotesk', 12), state='readonly', corner_radius=7
    )
    combobox_1.place(x=200, y=90, anchor=tk.W)
    combobox_1.set("Select...")

    val_entry = customtkinter.CTkEntry(
        master=my_top.canvas, placeholder_text="Nil", corner_radius=7, width=160, height=25,
        bg_color='White', font=('Alte Haas Grotesk', 12)
    )
    val_entry.place(x=200, y=125, anchor=tk.W)

    save_button = customtkinter.CTkButton(
        my_top, height=30, corner_radius=6, text='Save', font=('Alte Haas Grotesk', 15, 'bold'),
        text_color='White', width=100, command=lambda: save_presc(my_top, drug, val_entry.get(), combobox_1.get())
    )
    save_button.place(x=390, y=165, anchor=tk.NE)

    discard_button = customtkinter.CTkButton(
        my_top, height=30, corner_radius=6, text='Close', font=('Alte Haas Grotesk', 15, 'bold'),
        text_color='White', width=100, fg_color='IndianRed2', hover_color='IndianRed4',
        command = lambda: my_top.destroy() if temp_untop(my_top, lambda: messagebox.askyesno("Discard changes?", "Are you sure you want to discard your changes?")) else None  # Use `command` instead of `function`
    )
    discard_button.place(x=280, y=165, anchor=tk.NE)

def physical_assessment(disease_features):
    action_history.append(['Physical Assessment', 'Examined the patient'])
    my_top = create_top_level('Physical Assessment Results', 800, 600, load_captions=['Assessing Patient...', 2000])
    scroll_bar = customtkinter.CTkScrollbar(my_top.canvas, command=my_top.canvas.yview, height=600)
    my_top.canvas.config(yscrollcommand=scroll_bar.set)
    scroll_bar.place(x=783, y=0)

    # Display the assessment on the canvas
    y_offset = 20
    my_top.canvas.create_line(20, y_offset, 780, y_offset, fill="#CCCCCC")
    y_offset += 40
    
    my_top.canvas.create_text(400, y_offset, text="Physical Assessment Results", font=("Montilla Ex ExtraBold DEMO", 20, "bold"), anchor='center', fill='Grey10')
    y_offset += 40
    
    my_top.canvas.create_line(20, y_offset, 780, y_offset, fill="#CCCCCC")
    y_offset += 40
    
    for category, features in disease_features.items():
        my_top.canvas.create_text(20, y_offset, text=category, font=("Montilla Ex ExtraBold DEMO", 14, "bold"), anchor='w', fill='Grey20')
        y_offset += 35
        
        for feature in features:
            my_top.canvas.create_text(40, y_offset, text=f"•   {feature}", font=("Alte Haas Grotesk", 12), anchor='w')
            y_offset += 30
        
        # Draw a single light separator line
        my_top.canvas.create_line(20, y_offset, 780, y_offset, fill="#CCCCCC")
        y_offset += 40
    
    my_top.canvas.config(scrollregion=(0, 0, 800, y_offset))

def calc_systemic_score(disease, systemic_scores):

    action_history.append(["Correctly Diagnosed", disease])
    messagebox.showinfo("Correctly Diagnosed!", f"Congratulations!\n\nYou have correctly identified {disease}.\n\nIt's now time to calculate the systemic score.")

    my_top = create_top_level('Systemic Scoring', 800, 850, load_captions=['Loading...', 1000])
    
    y_offset = 20
    my_top.canvas.create_line(20, y_offset, 780, y_offset, fill="#CCCCCC")
    y_offset += 40
    
    my_top.canvas.create_text(400, y_offset, text="Calculate Systemic Score", font=("Montilla Ex ExtraBold DEMO", 20, "bold"), anchor='center', fill='Grey10')
    y_offset += 40
    
    my_top.canvas.create_line(20, y_offset, 780, y_offset, fill="#CCCCCC")
    y_offset += 40

    score_vars = {}
    total_score = customtkinter.IntVar(value=0)
    
    def update_score():
        total = sum(value for key, value in systemic_scores.items() if score_vars[key].get())
        total_score.set(total)
    
    for category, score in systemic_scores.items():
        score_vars[category] = customtkinter.IntVar(value=0)
        checkbox = customtkinter.CTkCheckBox(my_top.canvas, text=category, variable=score_vars[category], command=update_score)
        my_top.canvas.create_window(30, y_offset, anchor='w', window=checkbox)
        y_offset += 35
    
    y_offset += 10
    my_top.canvas.create_line(20, y_offset, 780, y_offset, fill="#CCCCCC")
    y_offset += 20
    
    my_top.canvas.create_text(400, y_offset, text="Total Score:", font=("Montilla Ex ExtraBold DEMO", 14, "bold"), anchor='center', fill='grey30')
    total_label = customtkinter.CTkLabel(my_top.canvas, textvariable=total_score, font=("Alte Haas Grotesk", 16, "bold"))
    my_top.canvas.create_window(400, y_offset + 30, anchor='center', window=total_label)
    
    y_offset += 50
    my_top.canvas.create_line(20, y_offset, 780, y_offset, fill="#CCCCCC")

    save_button = customtkinter.CTkButton(
        my_top, height=30, corner_radius=6, text='Finalize', font=('Alte Haas Grotesk', 15, 'bold'),
        text_color='White', width=100, command=lambda: print(action_history.to_list())
    )
    save_button.place(x=405, y=830, anchor=tk.SW)

    discard_button = customtkinter.CTkButton(
        my_top, height=30, corner_radius=6, text='Discard', font=('Alte Haas Grotesk', 15, 'bold'),
        text_color='White', width=100, fg_color='IndianRed2', hover_color='IndianRed4',
        command=my_top.destroy  # Use command instead of function
    )
    discard_button.place(x=395, y=830, anchor=tk.SE)

def show_action_history():
    my_top = create_top_level('Action History', 1000, 950, load_captions=['Loading...', 500])
    tabview_1 = customtkinter.CTkTabview(master=my_top.canvas, width=960, height=930, bg_color='#f0f0f0', corner_radius=7)
    tabview_1._segmented_button.configure(font=('Alte Haas Grotesk', 15, 'bold'))
    tabview_1.place(x=20, y=0)
    tabview_1.add("Your Action History"); tabview_1.add("Operational Procedure")

    tab_1_canvas = tk.Canvas(tabview_1.tab("Your Action History"), width=960, height=930, highlightthickness=0, background=tabview_1.cget('fg_color')[0])
    tab_1_canvas.place(x=0, y=0)
    scroll_bar = customtkinter.CTkScrollbar(tabview_1.tab("Your Action History"), command=tab_1_canvas.yview, height=880)
    tab_1_canvas.config(yscrollcommand=scroll_bar.set)
    scroll_bar.place(x=930, y=-4)

    # Visualization of the linked list
    y_position = 40  # Initial Y position
    x_position = 470  # X position for buttons
    node = action_history.head  # Start from the head of the linked list

    tab_1_canvas.create_line(500, 0, 500, 40, width=4, fill=tabview_1.cget('fg_color')[0])

    while node:
        values = node.data  # Extract list from linked list node
        if values:
            element = customtkinter.CTkSegmentedButton(
                master=tab_1_canvas,
                values=values,
                font=('Alte Haas Grotesk', 14, 'bold'),
                corner_radius=7,
                height=40,
                state=tk.DISABLED,
                text_color_disabled='White',
                selected_color='Indianred2'
            )
            element.set(values[0])  # Set first element as selected value
            tab_1_canvas.create_window(x_position, y_position, window=element, anchor=tk.CENTER)
            
            # Draw an arrow to the next node
            if node.next:
                tab_1_canvas.create_line(
                    x_position, y_position + 20,  # Start of the arrow (right side of the button)
                    x_position, y_position + 80,  # Middle point of the arrow
                    arrow=tk.LAST, fill="black", width=4
                )
            
            y_position += 100  # Move down for the next element
        
        node = node.next  # Move to the next node

    tab_1_canvas.create_line(500, y_position, 500, y_position+10, width=4, fill=tabview_1.cget('fg_color')[0])
    
    my_top.update()
    tab_1_canvas.configure(scrollregion=tab_1_canvas.bbox("all"))

    tab_2_canvas = tk.Canvas(tabview_1.tab("Operational Procedure"), width=960, height=930, highlightthickness=0, background=tabview_1.cget('fg_color')[0])
    tab_2_canvas.place(x=0, y=0)
    scroll_bar_2 = customtkinter.CTkScrollbar(tabview_1.tab("Operational Procedure"), command=tab_2_canvas.yview, height=880)
    tab_2_canvas.config(yscrollcommand=scroll_bar_2.set)
    scroll_bar_2.place(x=930, y=-4)

def show_final_score(score):
    my_top = create_top_level('Final Score', 600, 700, load_captions=['Loading...', 500])
    my_top.canvas.create_text(300, 40, text="Your Final Score", font=("Montilla Ex ExtraBold DEMO", 20, "bold"), anchor='center', fill='Grey20')
    my_top.canvas.create_line(20, 70, 580, 70, fill='Grey60', width=3)
    if score <= 30:
        color = 'firebrick1'
    elif score > 30 and score <= 60:
        color = 'gold2'
    elif score > 60 and score <= 80:
        color = 'dark orange'
    else:
        color = 'SpringGreen2'
    my_top.canvas.create_oval(150, 120, 450, 420, fill='Grey80', width=0)
    my_top.canvas.create_arc(150, 120, 450, 420, fill=color, outline=color, width=0, start=90, extent=-int((score/100)*360))
    my_top.canvas.create_oval(180, 150, 420, 390, fill='White', width=0)
    my_top.canvas.create_text(300, 240, text=str(score), font=('The Bold Font', 40), fill='Grey30', anchor='center')
    my_top.canvas.create_line(255, 270, 345, 270, fill='Grey60', width=3)
    my_top.canvas.create_text(300, 300, text=100, font=('The Bold Font', 40), fill='Grey30', anchor='center')