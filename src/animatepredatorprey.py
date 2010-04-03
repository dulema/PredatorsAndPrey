from Tkinter import *


def receive_gen():
	print gen_num.get()

def animate():
	print "Nothing Yet"

root = Tk()
root.wm_title("Pred/Prey Animator")


playing_field = Canvas(root)
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




gen_num = StringVar()

gen_num_label = Label(root, text="Number of Generations")
gen_num_input = Entry(root, textvariable=gen_num)
gen_num.set("10")
gen_num_button = Button(root, text="Enter", command=receive_gen)
animate_button = Button(root, text="Animate", command=animate)


key_title_label = Label(root, text="Map Icon Key")
key_pred_label = Label(root, text="Predator = D")
key_prey_label = Label(root, text="Prey = Y")
key_veg_label = Label(root, text="Vegetation = V")


y = 0
for i in range(10):
    if (i % 2 == 1):
        x = 13
        for j in range(18):       
            playing_field.create_polygon(x,y+12, x+12,y, x+24,y+12, x+24,y+29, x+12,y+41, x,y+29, fill='', outline="red")
            x = x + 24
    else:
        x = 1
        for j in range(19):       
            playing_field.create_polygon(x,y+12, x+12,y, x+24,y+12, x+24,y+29, x+12,y+41, x,y+29, fill='', outline="red")
            x = x + 24
    y = y + 29





gen_num_label.grid(row=0, column=0)
gen_num_input.grid(row=1, column=0)
gen_num_button.grid(row=2, column=0)
animate_button.grid(row=10, column=0)
key_title_label.grid(row=5, column=0)
key_pred_label.grid(row=6, column=0)
key_prey_label.grid(row=7, column=0)
key_veg_label.grid(row=8, column=0)
playing_field.grid(row=0, column=1, rowspan=11, padx=10, pady=10, sticky=N+S+E+W)


root.mainloop()
