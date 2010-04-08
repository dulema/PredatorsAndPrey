from Tkinter import *
from tkFileDialog import *
import webbrowser


def receive_gen_and_speed():
	print gen_num.get(), speed_slider.get()

def animate():
	playing_field.create_text(12,21, text="V", fill="green")
	playing_field.create_text(192,282, text="Y", fill="red")
	playing_field.create_text(372,427, text="D", fill="blue")
	draw_root()

def README_display():
	webbrowser.open("help.html")

def About_display():
	webbrowser.open("about.html")

def open_critters():
	open_critter_file = askopenfilename()
	print open_critter_file

def save_critters():
	save_critter_file = asksaveasfilename()
	print save_critter_file

def reset():
	playing_field.delete(ALL)
	gen_num.set("10")
	speed_slider.set(0)
	draw_map()
	draw_root()

def draw_root():
	gen_num_label.grid(row=0, column=0, sticky=S)
	gen_num_input.grid(row=1, column=0, sticky=N)
	speed_slider_label.grid(row=2, column=0, sticky=S)
	speed_slider.grid(row=3, column=0, sticky=N)
	set_gen_and_speed_button.grid(row=4, column=0, sticky=N)
	animate_button.grid(row=10, column=0, sticky=S)
	key_title_label.grid(row=5, column=0)
	key_pred_label.grid(row=6, column=0, sticky=S)
	key_prey_label.grid(row=7, column=0)
	key_veg_label.grid(row=8, column=0, sticky=N)
	playing_field.grid(row=0, column=1, rowspan=17, padx=10, pady=10)

def draw_map():
	y = 0
	for i in range(16):
    		if (i % 2 == 1):
        		x = 13
        		for j in range(15):       
            			playing_field.create_polygon(x,y+12, x+12,y, x+24,y+12, x+24,y+29, x+12,y+41, x,y+29, fill='', outline="black")
            			x = x + 24
    		else:
        		x = 1
        		for j in range(16):       
            			playing_field.create_polygon(x,y+12, x+12,y, x+24,y+12, x+24,y+29, x+12,y+41, x,y+29, fill='', outline="black")
            			x = x + 24
    		y = y + 29

	


root = Tk()
root.wm_title("Pred/Prey Animator")
root.geometry("%dx%d%+d%+d" % (600, 500, 0, 0))
playing_field = Canvas(root, width=400, height=500)



menu = Menu(root)
root.config(menu=menu)
file_menu = Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Reset", command=reset)
file_menu.add_command(label="Open", command=open_critters)
file_menu.add_command(label="Save", command=save_critters)
file_menu.add_separator()
file_menu.add_command(label="Close", command=playing_field.quit)
help_menu = Menu(menu)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="README", command=README_display)
help_menu.add_command(label="About...", command=About_display)



speed_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL)
speed_slider_label = Label(root, text="Speed of Animation")



gen_num = StringVar()
gen_num_label = Label(root, text="Number of Generations")
gen_num_input = Entry(root, textvariable=gen_num)
gen_num.set("10")
set_gen_and_speed_button = Button(root, text="Set Parameters", command=receive_gen_and_speed)
animate_button = Button(root, text="Animate", command=animate)
key_title_label = Label(root, text="Map Icon Key")
key_pred_label = Label(root, text="Predator = D")
key_prey_label = Label(root, text="Prey = Y")
key_veg_label = Label(root, text="Vegetation = V")



draw_map()
draw_root()
root.mainloop()
