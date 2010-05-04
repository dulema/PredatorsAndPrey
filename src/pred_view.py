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


def best_pred_loop(x):
        critter_attr = []
        labels_top = ["pred", "pred", "prey", "prey", "plant", "plant", "hunger"]
        labels_bottom = ["distance", "direction", "distance", "direction","distance", "direction",""]
        graph.delete(ALL)
        critter_tuple = int(pred_dist.get()), int(pred_dir.get()), int(prey_dist.get()), int(prey_dir.get()), int(plant_dist.get()), int(plant_dir.get()), int(hunger.get())
        #print(ppa.best_pred)
        if critter_tuple in ppa.best_pred:
                critter_attr = ppa.best_pred[critter_tuple]
                normalize = sum(critter_attr)
                y_base = 250
                j = 30
                graph.create_line(20,y_base, 550,y_base)
                graph.create_line(20,y_base, 20,40)
                point = 0
                for k in range(6):
                        point_name = k*10
                        point = point_name * 4
                        graph.create_text(8,(y_base - point), text=str(point_name))
                        graph.create_line(18,y_base - point,22,y_base - point)
                for i in range(len(critter_attr)):
                        bar = (float(critter_attr[i])/float(normalize))*100
                        bar_name = int(bar)
                        bar = (int(bar)*4)+1
                        graph.create_polygon(j, y_base,j, y_base - bar, j+30, y_base - bar,j+30, y_base, fill="red")
                        graph.create_text(j+15, y_base - bar - 10, text=str(bar_name))
                        graph.create_text(j+15,y_base + 10,text=labels_top[i])
                        graph.create_text(j+15,y_base + 20,text=labels_bottom[i])
                        j = j + 80
        else:
                graph.create_text(150,100,text="No Histogram for this set of Inputs")




def button_run():
        global graph, pred_dist, pred_dir, prey_dist, prey_dir, plant_dist, plant_dir, hunger
        labels_top = ["pred", "pred", "prey", "prey", "plant", "plant", "hunger"]
        labels_bottom = ["distance", "direction", "distance", "direction","distance", "direction",""]
        pred_view_window = Tk()
        pred_view_window.wm_title("Best Predator View")
        graph = Canvas(pred_view_window, width = 550, height = 300)
        graph.grid(row=0, column=0, columnspan=15, padx=10)
        pred_dist = Scale(pred_view_window,from_=0, to=len(ppa.DEFAULT_SETTINGS["distancechunks"]), orient=VERTICAL, command=best_pred_loop)
        pred_dist.grid(row=1, column=1, sticky = N)
        pred_dist.set("1")
        pred_dir = Scale(pred_view_window,from_=0, to=6, orient=VERTICAL, command=best_pred_loop)
        pred_dir.grid(row=1, column=3, sticky = N)
        pred_dir.set("3") 
        prey_dist = Scale(pred_view_window,from_=0, to=len(ppa.DEFAULT_SETTINGS["distancechunks"]), orient=VERTICAL, command=best_pred_loop)
        prey_dist.grid(row=1, column=5, sticky = N)
        prey_dist.set("3")
        prey_dir = Scale(pred_view_window,from_=0, to=6, orient=VERTICAL, command=best_pred_loop)
        prey_dir.grid(row=1, column=7, sticky = N)
        prey_dir.set("3") 
        plant_dist = Scale(pred_view_window,from_=0, to=len(ppa.DEFAULT_SETTINGS["distancechunks"]), orient=VERTICAL, command=best_pred_loop)
        plant_dist.grid(row=1, column=9, sticky = N+E)
        plant_dist.set("1") 
        plant_dir = Scale(pred_view_window,from_=0, to=6, orient=VERTICAL, command=best_pred_loop)
        plant_dir.grid(row=1, column=11, sticky = N+E)
        plant_dir.set("3") 
        hunger = Scale(pred_view_window,from_=0, to=len(ppa.DEFAULT_SETTINGS["hungerchunks"]), orient=VERTICAL, command=best_pred_loop)
        hunger.grid(row=1, column=13, sticky = N+E)
        hunger.set("1")
        exit_button = Button(pred_view_window, text="Quit", command=pred_view_window.destroy)
        exit_button.grid(row=1, column=15)

#pred_view_window.mainloop()


