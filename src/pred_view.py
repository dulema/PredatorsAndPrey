import predpreyalgorithm as ppa
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


def best_prey_loop():
	critter_attr = []
	labels_top = ["pred", "pred", "prey", "prey", "plant", "plant", "hunger"]
        labels_bottom = ["distance", "direction", "distance", "direction","distance", "direction",""]
	graph.delete(ALL)
	critter_tuple = int(pred_dist.get()), int(pred_dir.get()), int(prey_dist.get()), int(prey_dir.get()), int(plant_dist.get()), int(plant_dir.get()), int(hunger.get())
	print(ppa.best_pred)
	if critter_tuple in ppa.best_pred:
		critter_attr = ppa.best_pred[critter_tuple]
		y_base = 200
        	j = 10
        	for i in range(len(critter_attr)):
                	graph.create_polygon(j, y_base,j, y_base - critter_attr[i], j+30, y_base - critter_attr[i],j+30, y_base, fill="red")
                	graph.create_text(j+15, y_base - critter_attr[i] - 10, text=str(critter_attr[i]))
			graph.create_text(j+15,y_base + 10,text=labels_top[i])
                	graph.create_text(j+15,y_base + 20,text=labels_bottom[i])
                	j = j + 80
	else:
		graph.create_text(150,100,text="No Histogram for this set of Inputs")





labels_top = ["pred", "pred", "prey", "prey", "plant", "plant", "hunger"]
labels_bottom = ["distance", "direction", "distance", "direction","distance", "direction",""]
critter_view_window = Tk()
critter_view_window.wm_title("Best Predator View")
graph = Canvas(critter_view_window, width = 550, height = 250)
graph.grid(row=0, column=0, columnspan=15, padx=10)
pred_dist = Scale(critter_view_window,from_=0, to=2, orient=VERTICAL)
pred_dist.grid(row=1, column=0, sticky = N)
pred_dist.set("1")
pred_dir = Scale(critter_view_window,from_=0, to=6, orient=VERTICAL)
pred_dir.grid(row=1, column=2, sticky = N)
pred_dir.set("3") 
prey_dist = Scale(critter_view_window,from_=0, to=2, orient=VERTICAL)
prey_dist.grid(row=1, column=4, sticky = N)
prey_dist.set("3")
prey_dir = Scale(critter_view_window,from_=0, to=6, orient=VERTICAL)
prey_dir.grid(row=1, column=6, sticky = N)
prey_dir.set("3") 
plant_dist = Scale(critter_view_window,from_=0, to=2, orient=VERTICAL)
plant_dist.grid(row=1, column=8, sticky = N)
plant_dist.set("1") 
plant_dir = Scale(critter_view_window,from_=0, to=6, orient=VERTICAL)
plant_dir.grid(row=1, column=10, sticky = N)
plant_dir.set("3") 
hunger = Scale(critter_view_window,from_=0, to=2, orient=VERTICAL)
hunger.grid(row=1, column=12, sticky = N)
hunger.set("1")
display = Button(critter_view_window, text="Display Graph", command=best_prey_loop)
display.grid(row=1, column= 15, sticky=S+E)


critter_view_window.mainloop()
