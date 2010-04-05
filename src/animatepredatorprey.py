from Tkinter import *

#Reads in the number of generations user wished to run.
#Prints it at the moment. Will pass into another function.
def receive_gen():
	print gen_num.get()

#Command for the animate button which will get the ball rolling
#for the whole program
def animate():
	print "Number of generations ", gen_num.get(), " Speed ", speed_slider.get()

#Create a Tk window and edit its title and size
root = Tk()
root.wm_title("Pred/Prey Animator")
root.geometry("%dx%d%+d%+d" % (600, 500, 0, 0))
playing_field = Canvas(root, width=400, height=500)


#Create the top menu bar
menu = Menu(root)
root.config(menu=menu)
file_menu = Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Reset")
file_menu.add_command(label="Open")
file_menu.add_command(label="Save")
file_menu.add_separator()
file_menu.add_command(label="Close", command=playing_field.quit)
help_menu = Menu(menu)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="README")
help_menu.add_command(label="About...")


#Create slider for speed of animation
speed_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL)
speed_slider_label = Label(root, text="Speed of Animation")


#Create Input Box and Map Legend
gen_num = StringVar()
gen_num_label = Label(root, text="Number of Generations")
gen_num_input = Entry(root, textvariable=gen_num)
gen_num.set("10")
animate_button = Button(root, text="Animate", command=animate)
key_title_label = Label(root, text="Map Icon Key")
key_pred_label = Label(root, text="Predator = D")
key_prey_label = Label(root, text="Prey = Y")
key_veg_label = Label(root, text="Vegetation = V")


#Create the canvas for the field animation
y = 0
for i in range(16):
    if (i % 2 == 1):
        x = 13
        for j in range(15):       
            playing_field.create_polygon(x,y+12, x+12,y, x+24,y+12, x+24,y+29, x+12,y+41, x,y+29, fill='', outline="red")
            x = x + 24
    else:
        x = 1
        for j in range(16):       
            playing_field.create_polygon(x,y+12, x+12,y, x+24,y+12, x+24,y+29, x+12,y+41, x,y+29, fill='', outline="red")
            x = x + 24
    y = y + 29




#Place everything on the root window
gen_num_label.grid(row=0, column=0, sticky=S)
gen_num_input.grid(row=1, column=0, sticky=N)
speed_slider_label.grid(row=2, column=0, sticky=S)
speed_slider.grid(row=3, column=0, sticky=N)
animate_button.grid(row=10, column=0, sticky=S)
key_title_label.grid(row=5, column=0)
key_pred_label.grid(row=6, column=0, sticky=S)
key_prey_label.grid(row=7, column=0)
key_veg_label.grid(row=8, column=0, sticky=N)
playing_field.grid(row=0, column=1, rowspan=17, padx=10, pady=10)

#Do Work
root.mainloop()
