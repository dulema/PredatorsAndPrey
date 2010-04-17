import menu
import predpreyalgorithm
from Tkinter import *
from tkFileDialog import *
import webbrowser
import time
from PIL import ImageTk


#Grock Mutate Parameters, i.e. Number of Generations, Predators and Prey
def receive_mutate_parameters():
	#Use gen_num.get(), pred_num.get(), prey_num.get()
	#validate here
	pass

#Erases playing_field and then loops through critter dictionary and plant
#array and calls fill+map to place appropriate letter in appropriate
#hexagon
def updatePlayingField(world, round_score):
	playing_field.delete(ALL)
	for critter, location in world.critters.iteritems():
		fill_map(critter.type, location)
	for i in world.plants:
		fill_map("V", i)
	draw_map()
	root.update()
	time.sleep(0.1)


#Command intiated by clicking the Animate button. Calls score in PredPreyAlgo
#update the playing_field.
def animate():	
	predpreyalgorithm.score((predpreyalgorithm.best_pred, predpreyalgorithm.best_prey, updatePlayingField))
	draw_map()
	#validate here

def README_display():
	webbrowser.open("../docs/help.html")

def About_display():
	webbrowser.open("../docs/about.html")

#Open pre-saved set of Predators
def open_pred():
	open_pred_file = askopenfilename(initialdir="critters/")	
	return open_pred_file

#Save a set of Predators
def save_pred():
	save_pred_file = asksaveasfilename(defaultextension=".pred",initialdir="critters/")
	return save_pred_file

#Open a re-saved set of prey
def open_prey():
	open_prey_file = askopenfilename(initialdir="critters/")
	return open_prey_file

#Save a set of Prey
def save_prey():
	save_prey_file = asksaveasfilename(defaultextension=".prey",initialdir="critters/")
	return save_prey_file

#Reset all values to default and clear the Playing Field
def reset():
	playing_field.delete(ALL)
	gen_num.set("10")
	speed_slider.set(0)
	pred_num.set("1")
	prey_num.set("20")
	map_size.set("23")
	pct_pred_slider.set("10")
	pct_prey_slider.set("30")
	prey_num.set("20")
	pct_veg_slider.set("20")
	draw_map()




#Draw the map of hexagons on the playing_field
def draw_map():
	size = map_size.get()
	size = int(size)
	y = 0
	for i in range(size):
    		if (i % 2 == 1):
        		x = 13
        		for j in range(size):       
            			playing_field.create_polygon(x,y+12, x+12,y, x+24,y+12, x+24,y+29, x+12,y+41, x,y+29, fill='', outline="black")
            			x = x + 24
    		else:
        		x = 1
        		for j in range(size):       
            			playing_field.create_polygon(x,y+12, x+12,y, x+24,y+12, x+24,y+29, x+12,y+41, x,y+29, fill='', outline="black")
            			x = x + 24
    		y = y + 29


#Given an x and y coordixnate and text, this can draw the text on the map
def fill_map(thing, location):
	x=location[0]
	y=location[1]
	
	temp = ImageTk.PhotoImage(file="PredPreyImages/PeterM_Tree.png")
	playing_field.create_image(13,20, image=temp)
	
	picture = None
	if(thing == "V"):
		critter = thing
		color = "SeaGreen"
		#picture = ImageTk.PhotoImage(file="PredPreyImages/PeterM_Tree.png")
		picture = vegetation
	elif(thing == "Predator"):
		critter = "D"
		color = "Red"
		#picture = ImageTk.PhotoImage(file="PredPreyImages/Telemachos_wolf_head_silhouette.png")
		picture = wolf
	elif(thing == "Prey"):
		critter = "Y"
		color = "Blue"
		#picture = ImageTk.PhotoImage(file="PredPreyImages/creohn_Sheep_in_gray.png")
		picture = sheep	

	if(y%2 == 1):
		#playing_field.create_text(13+12+x*24,20+y*29, text=critter, fill=color)
		playing_field.create_image(13+12+x*24,20+y*29, image=picture)
	else:
		#playing_field.create_text(1+12+x*24,20+y*29, text=critter, fill=color)
		playing_field.create_image(1+12+x*24,20+y*29, image=picture)
	


#Main part of program. This section instatiates and places everything on the root
if __name__ == "__main__":
	root = Tk()
	root.wm_title("Pred/Prey Animator")
	yscrollbar = Scrollbar(root, orient=VERTICAL)
	yscrollbar.grid(row=0, column=2, sticky=N+S+W+E, rowspan=17)
	xscrollbar = Scrollbar(root, orient=HORIZONTAL)
	xscrollbar.grid(row=18, column=1, sticky=N+S+W+E)
	playing_field = Canvas(root, width=600, height=600, yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set, scrollregion=(0, 0, 3000, 3000))
	
	yscrollbar.config(command=playing_field.yview)
	xscrollbar.config(command=playing_field.xview)


	#Menu Section
	menu = Menu(root)
	root.config(menu=menu)
	file_menu = Menu(menu)
	menu.add_cascade(label="File", menu=file_menu)
	file_menu.add_command(label="Reset", command=reset)
	file_menu.add_separator()
	file_menu.add_command(label="Open Predators", command=open_pred)
	file_menu.add_command(label="Open Prey", command=open_prey)
	file_menu.add_separator()
	file_menu.add_command(label="Save Predators", command=save_pred)
	file_menu.add_command(label="Save Prey", command=save_prey)
	file_menu.add_separator()
	file_menu.add_command(label="Close", command=playing_field.quit)
	help_menu = Menu(menu)
	menu.add_cascade(label="Help", menu=help_menu)
	help_menu.add_command(label="README", command=README_display)
	help_menu.add_command(label="About...", command=About_display)


	#Slider Section
	speed_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL)
	speed_slider_label = Label(root, text="Speed of Animation")
	pct_pred_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL)
	pct_pred_slider_label = Label(root, text="Percentage of Map with Predators")#validate here
	pct_pred_slider.set("10")
	pct_prey_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL)
	pct_prey_slider_label = Label(root, text="Percentage of Map with Prey")#validate here
	pct_prey_slider.set("30")
	pct_veg_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL)
	pct_veg_slider_label = Label(root, text="Percentage of Map with Vegetation")
	pct_veg_slider.set("20")
	pct_pdf_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL)
	pct_pdf_slider_label = Label(root, text="Percentage of Genes Mutated")
	pct_pdf_slider.set("40")


	#Integer Input Section
	gen_num = StringVar()
	pred_num = StringVar()
	prey_num = StringVar()
	map_size = StringVar()
	gen_num_label = Label(root, text="Number of Generations")
	gen_num_input = Entry(root, textvariable=gen_num)#validate here
	gen_num.set("10")
	pred_num_label = Label(root, text="Number of Predators")
	pred_num_input = Entry(root, textvariable=pred_num)#validate here
	pred_num.set("1")
	prey_num_label = Label(root, text="Number of Prey")
	prey_num_input = Entry(root, textvariable=prey_num)#validate here
	prey_num.set("20")
	mutate_button = Button(root, text="Mutate", command=receive_mutate_parameters)
	map_size_label = Label(root, text="Size of Map")
	map_size_input = Entry(root, textvariable=map_size)
	map_size.set("23")


	#Playing_Field Legend Section
	key_title_label = Label(root, text="Map Icon Key")
	key_pred_label = Label(root, text="	  Predator =>")
	key_prey_label = Label(root, text="	      Prey =>")
	key_veg_label = Label(root, text="	Vegetation =>")
	animate_button = Button(root, text="Animate", command=animate)



	#Grid Section
	#The following code tells each widget where to be placed on the root
	gen_num_label.grid(row=0, column=0, sticky=S)
	gen_num_input.grid(row=1, column=0, sticky=N)
	pred_num_label.grid(row=2, column=0, sticky=S)
	pred_num_input.grid(row=3, column=0, sticky=N)
	prey_num_label.grid(row=4, column=0, sticky=S)
	prey_num_input.grid(row=5, column=0, sticky=N)
	pct_pred_slider_label.grid(row=6, column=0, sticky=S)
	pct_pred_slider.grid(row=7, column=0, sticky=N)
	pct_prey_slider_label.grid(row=8, column=0, sticky=S)
	pct_prey_slider.grid(row=9, column=0, sticky=N)
	pct_veg_slider_label.grid(row=10, column=0, sticky=S)
	pct_veg_slider.grid(row=11, column=0, sticky=N)
	pct_pdf_slider_label.grid(row=12, column=0, sticky=S)
	pct_pdf_slider.grid(row=13, column=0, sticky=N)
	mutate_button.grid(row=17, column=0, sticky=N)
	key_title_label.grid(row=0, column=4, sticky=E)
	key_pred_label.grid(row=1, column=4)
	key_prey_label.grid(row=2, column=4)
	key_veg_label.grid(row=3, column=4)
	speed_slider_label.grid(row=13, column=4, sticky=S)
	speed_slider.grid(row=14, column=4, sticky=N)
	map_size_label.grid(row=15, column=4, sticky=S)
	map_size_input.grid(row=16, column=4, sticky=N)
	animate_button.grid(row=17, column=4, sticky=N)
	playing_field.grid(row=0, column=1, rowspan=17, padx=5)


	vegetation = ImageTk.PhotoImage(file="PredPreyImages/PeterM_Tree.png")
	#wolf = ImageTk.PhotoImage(file="PredPreyImages/Telemachos_wolf_head_silhouette.png")
	wolf = ImageTk.PhotoImage(file="PredPreyImages/Gerald_G_Wolf_Head_(Stylized).png")
	sheep = ImageTk.PhotoImage(file="PredPreyImages/creohn_Sheep_in_gray.png")
	

	wolf_canvas = Canvas(root,width=30,height=30)
	wolf_canvas.create_image(15,15, image=wolf)
	wolf_canvas.grid(row=1,column=5, sticky=S+W)
	sheep_canvas = Canvas(root,width=30,height=30)
	sheep_canvas.create_image(15,15, image=sheep)
	sheep_canvas.grid(row=2,column=5, sticky=S+W)
	veg_canvas = Canvas(root,width=30,height=30)
	veg_canvas.create_image(15,15, image=vegetation)
	veg_canvas.grid(row=3,column=5, sticky=S+W)

	#Do Work
	#Place everything on the root
	draw_map()
	root.mainloop()
