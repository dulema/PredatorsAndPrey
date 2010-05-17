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
from functools import partial
from subprocess import call
import tkSimpleDialog
import pickle

try:
        import psyco
        psyco.full()
except ImportError:
        print("Install Python Psyco For Increased Performance.\nAnimate\n")


canvas_items = []
settings = predpreyalgorithm.DEFAULT_SETTINGS


#Changes the Mutate Button into a progress indicator
def change_to_progress_bar(currentgen,totalgens, pred_score, prey_score):
        if currentgen == totalgens:
                mutate_button.config(state = NORMAL)
                mutate_button.config(text = "Mutate")
        else:
                mutate_button.config(text = "Current/Total Generations\n" + str(currentgen) + "/" + str(totalgens))

#Grock mutate parameters from settings file and call predpreyalgo to start mutation
def receive_mutate_parameters():
        if validate() == 0:
                pass
        else:
                tempStr = []
                try:
                        settingsFile = open('settings.txt', 'r')
                except IOError:
                        print 'Cannot Open Settings'
                else:
                        settings = pickle.load(settingsFile)
                        pass
                
                mutate_button.config(state = DISABLED)
                import thread
                thread.start_new_thread(predpreyalgorithm.mutate,(int(gen_num.get()),{}, change_to_progress_bar))


#Scales the canvas from 50% to 150% of its original state
def scale_canvas():
        scale_factor = float(scale_slider.get())
        for i in canvas_items:
                playing_field.scale(i,0,0,scale_factor,scale_factor)

#Function that receives current state of the map from Critter.py and calls fill_map to draw appropriate playing_field
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
        speed = float((101 - float(speed_slider.get())) / 500)
        time.sleep(speed)


#Command intiated by clicking the Animate button. Calls score in PredPreyAlgo to
#update the playing_field.
def animate():
        if validate() == 0:
                pass
        else:
                scorealgorithm.calcscore(hooker = updatePlayingField)
                time.sleep(5)
                playing_field.delete(ALL)
                draw_map()
                scale_canvas()  
                root.update()

#Instatiates the Predator version of Critter View
def pred_view():
        import pred_view
        pred_view.button_run()

#Instatiates the Prey version of Critter View 
def prey_view():
        import prey_view
        prey_view.button_run()
         


def README_display():
        ufa1 = location[:-4] + "/docs/help.html"
        osblindufa1 = os.path.abspath(ufa1)
        print(ufa1)
        webbrowser.open(osblindufa1)

def About_display():
        ufa2 = location[:-4] + "/docs/about.html"
        osblindufa2 = os.path.abspath(ufa2)
        webbrowser.open(osblindufa2)

#Open pre-saved set of Predators
def open_pred():
        open_pred_file = askopenfilename(initialdir="critters/")        
        predpreyalgorithm.best_pred = pickle.load(file(open_pred_file, 'r'))

#Save a set of Predators
def save_pred():
        save_pred_file = asksaveasfilename(defaultextension=".pred",initialdir="critters/")
        pickle.dump(predpreyalgorithm.best_pred, file(save_pred_file, 'w'))

#Open a re-saved set of prey
def open_prey():
        open_prey_file = askopenfilename(initialdir="critters/")        
        predpreyalgorithm.best_prey = pickle.load(file(open_prey_file, 'r')) 

#Save a set of Prey
def save_prey():
        save_prey_file = asksaveasfilename(defaultextension=".prey",initialdir="critters/")
        pickle.dump(predpreyalgorithm.best_prey, file(save_prey_file, 'w'))

#Reset all values to default and clear the Playing Field
def reset_settings():
        playing_field.delete(ALL)
        gen_num.set("10")
        speed_slider.set(50)
        pred_num.set("1")
        prey_num.set("20")
        map_size.set("20")
        prey_num.set("20")
        scale_slider.set("1.0")
        draw_map()

#Resets the best_pred dictionary in predpreyalgo
def reset_best_pred():
        predpreyalgorithm.best_pred = {}

#Resets the best_prey dictionary in predpreyalgo
def reset_best_prey():
        predpreyalgorithm.best_prey = {}


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
                                hexagon = playing_field.create_polygon(x,y+12, x+12,y, x+24,y+12, x+24,y+29, x+12,y+41, x,y+29, fill='', outline="gray")
                                canvas_items.append(hexagon)
                                x = x + 24
                else:
                        x = 1
                        for j in range(size):       
                                hexagon = playing_field.create_polygon(x,y+12, x+12,y, x+24,y+12, x+24,y+29, x+12,y+41, x,y+29, fill='', outline="gray")
                                canvas_items.append(hexagon)
                                x = x + 24
                y = y + 29


#Given an x and y coordixnate and text, this places the pictures on the map
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

class MyDialog(tkSimpleDialog.Dialog):
    def body(self, master):
        Label(master, text="sight").grid(row=0)
        Label(master, text="mapsize:").grid(row=1)
        Label(master, text="plantpercent:").grid(row=2)
        Label(master, text="preypercent:").grid(row=3)
        Label(master, text="predpercent:").grid(row=4)
        Label(master, text="plantbites:").grid(row=5)
        Label(master, text="maxhunger:").grid(row=6)
        Label(master, text="pdfpercent:").grid(row=7)
        Label(master, text="mutationincrement:").grid(row=8)
        Label(master, text="distancechunks:").grid(row=9)
        Label(master, text="hungerchunks:").grid(row=10)

	sightin = StringVar()
	sightin.set("20")
	mapsizein = StringVar()
	mapsizein.set("20")
	plantpctin = StringVar()
	plantpctin.set("5")
	preypctin = StringVar()
	preypctin.set("5")
	predpctin = StringVar()
	predpctin.set("3")
	plantbitein = StringVar()
	plantbitein.set("3")
	maxhungerin = StringVar()
	maxhungerin.set("20")
	pdfpctin = StringVar()
	pdfpctin.set("2")
	mutateincin = StringVar()
	mutateincin.set("0.3")
	distchunkin = StringVar()
	distchunkin.set("3,9,18")
	hungerchunkin = StringVar()
	hungerchunkin.set("3,9,18")
	
	
        self.e1 = Entry(master, textvariable=sightin)
        self.e2 = Entry(master, textvariable=mapsizein)
        self.e3 = Entry(master, textvariable=plantpctin)
        self.e4 = Entry(master, textvariable=preypctin)
        self.e5 = Entry(master, textvariable = predpctin)
        self.e6 = Entry(master, textvariable = plantbitein)
        self.e7 = Entry(master, textvariable = maxhungerin)
        self.e8 = Entry(master, textvariable = pdfpctin)
        self.e9 = Entry(master, textvariable = mutateincin)
        self.e10 = Entry(master,textvariable = distchunkin)
        self.e11 = Entry(master,textvariable = hungerchunkin)
        
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)
        self.e5.grid(row=4, column=1)
        self.e6.grid(row=5, column=1)
        self.e7.grid(row=6, column=1)
        self.e8.grid(row=7, column=1)
        self.e9.grid(row=8, column=1)
        self.e10.grid(row=9, column=1)
        self.e11.grid(row=10, column=1)

        return self.e1 # initial focus

    def apply(self):
        settings["sight"] = int(self.e1.get())
        settings["mapsize"] = int(self.e2.get())
        settings["plantpercent"] = float((float(self.e3.get())/100))
        settings["preypercent"] = float((float(self.e4.get())/100))
        settings["predpercent"] = float((float(self.e5.get())/100))
        settings["plantbites"] = int(self.e6.get())
        settings["maxhunger"] = int(self.e7.get())
        settings["pdfpercent"] = float((float(self.e8.get())/100))
        settings["mutationincrement"] = float(self.e9.get())

        rawdistancechunks = self.e10.get()
        rawhungerchunks = self.e11.get()
        settings["distancechunks"] = map(lambda x : int(x), rawdistancechunks.split(','))
        settings["hungerchunks"] = map(lambda x : int(x), rawhungerchunks.split(','))
	#print(settings)

        pickle.dump(settings, file("settings.txt", 'w'))

def display_conf():
        d = MyDialog(root)

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
                map_size.set("20")
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
        file_menu.add_command(label="Reset Settings", command=reset_settings)
        file_menu.add_command(label="Reset Best Predators", command=reset_best_pred)
        file_menu.add_command(label="Reset Best Prey", command=reset_best_prey)
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
        #global mutate_button
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
