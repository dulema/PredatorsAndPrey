import menu
import predpreyalgorithm
import scorealgorithm
from Tkinter import *
from tkFileDialog import *
import webbrowser
import time
from PIL import ImageTk
import re
import tkMessageBox
import os
import sys
import Tkinter as tk#deniz, I don't know what this means, but its apparently needed


try:
        import psyco
        psyco.full()
except ImportError:
        print("Install Python Psyco For Increased Performance.\nAnimate\n")

canvas_items = []
settings = predpreyalgorithm.DEFAULT_SETTINGS
#Grock Mutate Parameters, i.e. Number of Generations, Predators and Prey
def receive_mutate_parameters():
        if validate() == 0:
                pass
        else:
		#deniz progress bar area, yell at me, no classes HAH
		#ccccccccccc
		pbar = Tk()
		pbar.wm_title("Generation Progress Bar")
		pbar.geometry("405x25+0+0")#widthxheightxoffsetxoffset, pixels

		space = " "#what gets added every increment
		s = ""#original progress bar
		label = tk.Label(pbar, text=s, bg='green3')#fill in blank text's background as green, looks like a bar
		label.pack(anchor='nw')#anchor the stuff to the northwest corner, it's "sticky"

		for k in range(100):
			s += space
			label.after(100,label.config(text=s))#increments every 100 milliseconds
			label.update()#needed for some strange reason
		pbar.mainloop()#I guess there can be more than one blah.mainloop()
		#ccccccccccc

		tempStr = []
		try:
                        settingsFile = open('settings.txt', 'r')
                except IOError:
                        print 'Cannot Open Settings'
                else:
                        for line in settingsFile:
                                tempStr.append(line)
                        settingsStr = ''.join(tempStr)
                        settings = eval(settingsStr)
                        pass


#Erases playing_field and then loops through critter dictionary and plant
#array and calls fill+map to place appropriate letter in appropriate
#hexagon
def scale_canvas():
        scale_factor = float(scale_slider.get())
        for i in canvas_items:
                playing_field.scale(i,0,0,scale_factor,scale_factor)


def updatePlayingField(world, round_score):
        global canvas_items
        canvas_items = []
        playing_field.delete(ALL)
        for critter, location in world.critters.iteritems():
                fill_map(critter.type, location)
        for i in world.plants:
                fill_map("V", i)
        draw_map()
        scale_canvas()
        root.update()
        speed = float(float(speed_slider.get()) / 500)
        time.sleep(speed)


#Command intiated by clicking the Animate button. Calls score in PredPreyAlgo
#update the playing_field.
def animate():
        if validate() == 0:
                pass
        else:
                scorealgorithm.calcscore(hooker = updatePlayingField)
                #draw_map()


def pred_view():
	pass


def prey_view():
        bar = [20, 55, 12, 22, 60, 29, 70]
        labels_top = ["pred", "pred", "prey", "prey", "plant", "plant", "hunger"]
        labels_bottom = ["distance", "direction", "distance", "direction","distance", "direction",""]
        critter_view_window = Tk()
        critter_view_window.wm_title("Critter View")
        graph = Canvas(critter_view_window, width = 550, height = 250)
        graph.grid(row=0, column=0, columnspan=15, padx=10)
        y_base = 200
        j = 10
        for i in range(len(bar)):
                graph.create_polygon(j, y_base,j, y_base - bar[i], j+30, y_base - bar[i],j+30, y_base, fill="red")
                graph.create_text(j+15, y_base - bar[i] - 10, text=str(bar[i]))
                graph.create_text(j+15,y_base + 10,text=labels_top[i])
                graph.create_text(j+15,y_base + 20,text=labels_bottom[i])
                j = j + 80
        
        pred_dist = Scale(critter_view_window,from_=1, to=25, orient=VERTICAL)
        pred_dist.grid(row=1, column=0, sticky = N) 
        pred_dir = Scale(critter_view_window,from_=1, to=25, orient=VERTICAL)
        pred_dir.grid(row=1, column=2, sticky = N) 
        prey_dist = Scale(critter_view_window,from_=1, to=25, orient=VERTICAL)
        prey_dist.grid(row=1, column=4, sticky = N)
        prey_dir = Scale(critter_view_window,from_=1, to=25, orient=VERTICAL)
        prey_dir.grid(row=1, column=6, sticky = N) 
        plant_dist = Scale(critter_view_window,from_=1, to=25, orient=VERTICAL)
        plant_dist.grid(row=1, column=8, sticky = N) 
        plant_dir = Scale(critter_view_window,from_=1, to=25, orient=VERTICAL)
        plant_dir.grid(row=1, column=10, sticky = N) 
        hunger = Scale(critter_view_window,from_=1, to=25, orient=VERTICAL)
        hunger.grid(row=1, column=12, sticky = N) 
        critter_view_window.mainloop()
        

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
        speed_slider.set(50)
        pred_num.set("1")
        prey_num.set("20")
        map_size.set("20")
        pct_pred_slider.set("1")
        pct_prey_slider.set("2")
        prey_num.set("20")
        pct_veg_slider.set("5")
        pct_pdf_slider.set("40")
        tree_life_slider.set("3")
        max_hunger_slider.set("20")
        sight_range_slider.set("10")
        draw_map()

#Draw the map of hexagons on the playing_field
def draw_map():
        global canvas_items
        size = map_size.get()
        size = int(size)
        y = 0
        for i in range(size):
                if (i % 2 == 1):
                        x = 13
                        for j in range(size):       
                                hexagon = playing_field.create_polygon(x,y+12, x+12,y, x+24,y+12, x+24,y+29, x+12,y+41, x,y+29, fill='', outline="black")
                                canvas_items.append(hexagon)
                                x = x + 24
                else:
                        x = 1
                        for j in range(size):       
                                hexagon = playing_field.create_polygon(x,y+12, x+12,y, x+24,y+12, x+24,y+29, x+12,y+41, x,y+29, fill='', outline="black")
                                canvas_items.append(hexagon)
                                x = x + 24
                y = y + 29


#Given an x and y coordixnate and text, this can draw the text on the map
def fill_map(thing, location):
        x=location[0]
        y=location[1]
        global canvas_items
        picture = None
        pic_scale = int((float(scale_slider.get()) - 0.5) * 10)
        if(thing == "V"):
                critter = thing
                color = "SeaGreen"
                picture = vegetation[pic_scale]
        elif(thing == "predator"):
                critter = "D"
                color = "Red"
                picture = wolf[pic_scale]
        elif(thing == "prey"):
                critter = "Y"
                color = "Blue"
                picture = sheep[pic_scale]      

        if(y%2 == 1):
                photo = playing_field.create_image(13+12+x*24,20+y*29, image=picture)
                canvas_items.append(photo)
        else:
                photo = playing_field.create_image(1+12+x*24,20+y*29, image=picture)
                canvas_items.append(photo)

def display_conf():
	if(os.name == "posix"):
		os.system("gedit settings.txt")
	elif(os.name == "nt"):
		os.system("notepad settings.txt")
	else:
		print("No Good")


def validate():
        wrongstuff = "\n"
        if re.match("^[0-9]+$",gen_num.get()) == None:#checks if a number, made of integers, was input
                wrongstuff = wrongstuff + "Number of generations\n"
                gen_num.set("10")
        if re.match("^[0-9]+$",pred_num.get()) == None:
                wrongstuff = wrongstuff + "Number of predators\n"
                pred_num.set("1")
        if re.match("^[0-9]+$",prey_num.get()) == None:
                wrongstuff = wrongstuff + "Number of prey\n"
                prey_num.set("20")
        if re.match("^[0-9]+$",map_size.get()) == None:
                wrongstuff = wrongstuff + "Size of map\n"
                map_size.set("23")
        if len(wrongstuff) > 1:
                tkMessageBox.showwarning("Fix Input","Fix the following:\n" + wrongstuff)
                return 0
        else:
                return 1


#Main part of program. This section instantiates and places everything on the root
if __name__ == "__main__":
        root = Tk()
        root.wm_title("Pred/Prey Animator")
        yscrollbar = Scrollbar(root, orient=VERTICAL)
        yscrollbar.grid(row=0, column=2, sticky=N+S+W+E, rowspan=17, padx=10)
        xscrollbar = Scrollbar(root, orient=HORIZONTAL)
        xscrollbar.grid(row=18, column=1, sticky=N+S+W+E)
        playing_field = Canvas(root, width=600, height=600, yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set, scrollregion=(0, 0, 3000, 3000))
        playing_field.scale(playing_field,.1,.1,10,10)
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
        speed_slider.set("50")
        scale_slider = Scale(root, from_=0.5, to=1.5, orient=HORIZONTAL, resolution=0.1)
        scale_label = Label(root, text="Scale of Playing Field")
        scale_slider.set("1.0")
        
        
        prey_view_button = Button(root, text="Best Prey View", command=prey_view)
	pred_view_button = Button(root, text="Best Predator View", command=pred_view)
	

        #Integer Input Section
        gen_num = StringVar()
        pred_num = StringVar()
        prey_num = StringVar()
        map_size = StringVar()
        gen_num_label = Label(root, text="Number of Generations")
        gen_num_input = Entry(root, textvariable=gen_num, width=10)
        gen_num.set("10")
        pred_num_label = Label(root, text="Number of Predators")
        pred_num_input = Entry(root, textvariable=pred_num, width=10)
        pred_num.set("1")
        prey_num_label = Label(root, text="Number of Prey")
        prey_num_input = Entry(root, textvariable=prey_num, width=10)
        prey_num.set("20")
        mutate_button = Button(root, text="Mutate", command=receive_mutate_parameters)
        map_size_label = Label(root, text="Size of Map")
        map_size_input = Entry(root, textvariable=map_size, width=10)
        map_size.set("20")

        #Playing_Field Legend Section
        key_title_label = Label(root, text="Map Icon Key")
        key_pred_label = Label(root, text="Predator =>")
        key_prey_label = Label(root, text="Prey =>")
        key_veg_label = Label(root, text="Vegetation =>")
        animate_button = Button(root, text="Animate", command=animate)
	edit_conf_button = Button(root, text="Edit Mutate Settings", command=display_conf)


        #Grid Section
        #The following code tells each widget where to be placed on the root
        
        
        mutate_button.grid(row=10, column=0, sticky=N)
	edit_conf_button.grid(row=8, column=0)
        prey_view_button.grid(row=17, column=0)
	pred_view_button.grid(row=16, column=0)
        key_title_label.grid(row=0, column=4, sticky=E)
        key_pred_label.grid(row=1, column=4)
        key_prey_label.grid(row=2, column=4)
        key_veg_label.grid(row=3, column=4)
        speed_slider_label.grid(row=13, column=4, sticky=S, columnspan=2)
        speed_slider.grid(row=14, column=4, sticky=N, columnspan=2)
        map_size_label.grid(row=6, column=0, sticky=S)
        map_size_input.grid(row=7, column=0, sticky=N)
        scale_label.grid(row=15,column=4, sticky=S, columnspan=2)
        scale_slider.grid(row=16,column=4, sticky=N, columnspan=2)
        animate_button.grid(row=17, column=4, sticky=N,columnspan=2)
        playing_field.grid(row=0, column=1, rowspan=17, padx=5)
        gen_num_label.grid(row=0, column=0, sticky=S)
        gen_num_input.grid(row=1, column=0, sticky=N)
        pred_num_label.grid(row=2, column=0, sticky=S)
        pred_num_input.grid(row=3, column=0, sticky=N)
        prey_num_label.grid(row=4, column=0, sticky=S)
        prey_num_input.grid(row=5, column=0, sticky=N)


        vegetation = []
        wolf = []
        sheep = []

        location = []
        #This Gets Current Directory (Windows)
        location = sys.path[0]

        for i in range(11):
                j = i*10 + 50

                veglocation = location + "/PredPreyImages/PeterM_Tree" + str(j) + ".png"
                wolflocation = location + "/PredPreyImages/Gerald_G_Wolf_Head_(Stylized)" + str(j) + ".png"
                sheeplocation = location + "/PredPreyImages/creohn_Sheep_in_gray" + str(j) + ".png"

                #Makes Path OS Blind
                osblindveglocation = os.path.abspath(veglocation)
                osblindwolflocation = os.path.abspath(wolflocation)
                osblindsheeplocation = os.path.abspath(sheeplocation)

                vegetation.append(ImageTk.PhotoImage(file=osblindveglocation))
                wolf.append(ImageTk.PhotoImage(file=osblindwolflocation))
                sheep.append(ImageTk.PhotoImage(file=osblindsheeplocation))

        wolf_canvas = Canvas(root,width=30,height=30)
        wolf_canvas.create_image(15,15, image=wolf[5])
        wolf_canvas.grid(row=1,column=5, sticky=S+W)
        sheep_canvas = Canvas(root,width=30,height=30)
        sheep_canvas.create_image(15,15, image=sheep[5])
        sheep_canvas.grid(row=2,column=5, sticky=S+W)
        veg_canvas = Canvas(root,width=30,height=30)
        veg_canvas.create_image(15,15, image=vegetation[5])
        veg_canvas.grid(row=3,column=5, sticky=S+W)

        #Do Work
        #Place everything on the root
        draw_map()
        root.mainloop()
