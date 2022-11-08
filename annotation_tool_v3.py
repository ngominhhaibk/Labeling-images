from __future__ import division
from PIL import Image as PImage, ImageTk
import os
import sys
import glob
import random
import shutil
import tkinter as tk
import cv2
if(sys.version_info[0] == 2):
    from Tkinter import *
    import tkMessageBox
elif(sys.version_info[0] == 3):
    from tkinter import *
    from tkinter import messagebox as tkMessageBox

binary_label = ['No         ', 'Yes']    
binary_value = ['0','1']        # No/Yes


# image sizes for the examples
SIZE = 256, 256

class LabelTool():
    def __init__(self, master):
        # set up the main frame
        self.curimg_h = 0
        self.curimg_w = 0

        self.cur_car = 0
        self.cur_motorbike = 0
        self.cur_bike = 0
        self.cur_catcar = 0
        self.cur_sedan = 0
        self.cur_suv = 0
        self.cur_minivan = 0
        self.cur_microbus = 0
        self.cur_car24 = 0
        self.cur_bus = 0
        self.cur_truck = 0
        self.cur_police = 0
        self.cur_ambulance = 0
        self.cur_firetruck = 0
        self.cur_taxi = 0
        self.cur_others = 0
        
        self.cur_toyota = 0
        self.cur_ford = 0
        self.cur_kia = 0
        self.cur_mazda = 0
        self.cur_honda = 0
        self.cur_huyndai = 0
        self.cur_mercedes = 0
        self.cur_vinfast = 0
        self.cur_audi =0 
        self.cur_bmw = 0
        self.cur_chevrolet = 0
        self.cur_isuzu = 0
        self.cur_lexus = 0
        self.cur_nissan = 0
        self.cur_peugeot = 0
        self.cur_porsche = 0
        self.cur_suzuki = 0
        self.cur_volkswagen = 0
        self.cur_volvo = 0
        self.cur_minicooper = 0
        self.cur_others2 = 0
        

        self.black = 0
        self.white = 0
        self.silver = 0
        self.gray = 0
        self.red = 0
        self.green = 0
        self.blue = 0
        self.brown = 0
        self.yellow = 0
        self.others3 = 0

        
        self.parent = master
        self.parent.title("Annotation Tool")
        self.frame = Frame(self.parent, bg='LightBlue')
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width = FALSE, height = FALSE)
        #self.parent.resizable(0,0)

        # initialize global state
        self.imageDir = ''
        self.imageList= []
        self.egDir = ''
        self.egList = []
        self.outDir = ''
        self.cur = 0
        self.total = 0
        self.category = 0
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None

        # initialize mouse state
        self.STATE = {}
        self.STATE['click'] = 0
        self.STATE['x'], self.STATE['y'] = 0, 0


        # ----------------- GUI stuff ---------------------
        # dir entry & load
        self.label = Label(self.frame, text = "Image Dir:")
        self.label.grid(row = 0, column = 0, sticky = E)
        self.entry = Entry(self.frame)
        self.entry.focus_set()
        self.entry.bind('<Return>', self.loadEntry)
        self.entry.grid(row = 0, column = 1, sticky = W+E)
        self.ldBtn = Button(self.frame, text = "Load", command = self.loadDir)
        self.ldBtn.grid(row = 0, column = 3, sticky = W+E)
        
        #yes/no label:
        for i in range(len(binary_label)):
            self.chooselbl = Label(self.frame, text = binary_label[i], bg='LightBlue')
            self.chooselbl.grid(row = 1, column = i+3, sticky = W+N)
    
        #   Car:
        self.tkvar_car = StringVar(self.parent)
        self.cur_car = 0
        self.tkvar_car.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Car", bg='LightBlue')
        self.chooselbl.grid(row = 2, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_car, value = binary_value[i], command = self.car_click)
            self.rdbtn.grid(row = 2, column = i+3, sticky = W+N)

        #   Motorbike:
        self.tkvar_motorbike = StringVar(self.parent)
        self.cur_motorbike = 0
        self.tkvar_motorbike.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Motorbike", bg='LightBlue')
        self.chooselbl.grid(row = 3, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_motorbike, 
            value = binary_value[i], command = self.motorbike_click)
            self.rdbtn.grid(row = 3, column = i+3, sticky = W+N)
        
        #   Bike:
        self.tkvar_bike = StringVar(self.parent)
        self.cur_bike = 0
        self.tkvar_bike.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Bikes", bg='LightBlue')
        self.chooselbl.grid(row = 4, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_bike, 
            value = binary_value[i], command = self.bike_click)
            self.rdbtn.grid(row = 4, column = i+3, sticky = W+N)
            
        # Categories of car
        self.chooselbl = Label(self.frame, text = "Categories", bg='LightBlue', anchor = CENTER)
        self.chooselbl.grid(row = 5, column = 3, sticky=W+N)

        
        #   Sedan:
        self.tkvar_sedan = StringVar(self.parent)
        self.cur_sedan = 0
        self.tkvar_sedan.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Sedan", bg='LightBlue')
        self.chooselbl.grid(row = 6, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_sedan, 
            value = binary_value[i], command = self.sedan_click)
            self.rdbtn.grid(row = 6, column = i+3, sticky = W+N)
        
        #   suv:
        self.tkvar_suv = StringVar(self.parent)
        self.cur_suv = 0
        self.tkvar_suv.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "SUV", bg='LightBlue')
        self.chooselbl.grid(row = 7, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_suv, 
            value = binary_value[i], command = self.suv_click)
            self.rdbtn.grid(row = 7, column = i+3, sticky = W+N)
        
        #   Minivan:
        self.tkvar_minivan = StringVar(self.parent)
        self.cur_minivan = 0
        self.tkvar_minivan.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Minivan", bg='LightBlue')
        self.chooselbl.grid(row = 8, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_minivan, 
            value = binary_value[i], command = self.minivan_click)
            self.rdbtn.grid(row = 8, column = i+3, sticky = W+N)
        
        #   Microbus:
        self.tkvar_microbus = StringVar(self.parent)
        self.cur_microbus = 0
        self.tkvar_microbus.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Microbus", bg='LightBlue')
        self.chooselbl.grid(row = 9, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_microbus, 
            value = binary_value[i], command = self.microbus_click)
            self.rdbtn.grid(row = 9, column = i+3, sticky = W+N)
            
        #   Car >= 24 seats:
        self.tkvar_car24 = StringVar(self.parent)
        self.cur_car24 = 0
        self.tkvar_car24.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Car>=24seats", bg='LightBlue')
        self.chooselbl.grid(row = 10, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_car24, 
            value = binary_value[i], command = self.car24_click)
            self.rdbtn.grid(row = 10, column = i+3, sticky = W+N)

        #   Bus:
        self.tkvar_bus = StringVar(self.parent)
        self.cur_bus = 0
        self.tkvar_bus.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Bus", bg='LightBlue')
        self.chooselbl.grid(row = 11, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_bus, 
            value = binary_value[i], command = self.bus_click)
            self.rdbtn.grid(row = 11, column = i+3, sticky = W+N)
            
        #   Truck:
        self.tkvar_truck = StringVar(self.parent)
        self.cur_truck = 0
        self.tkvar_truck.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Truck", bg='LightBlue')
        self.chooselbl.grid(row = 12, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_truck, 
            value = binary_value[i], command = self.truck_click)
            self.rdbtn.grid(row = 12, column = i+3, sticky = W+N)
        
        #   Police:
        self.tkvar_police = StringVar(self.parent)
        self.cur_police = 0
        self.tkvar_police.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Police", bg='LightBlue')
        self.chooselbl.grid(row = 13, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_police, 
            value = binary_value[i], command = self.police_click)
            self.rdbtn.grid(row = 13, column = i+3, sticky = W+N)
            
        #   Ambulance:
        self.tkvar_ambulance = StringVar(self.parent)
        self.cur_ambulance = 0
        self.tkvar_ambulance.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Ambulance", bg='LightBlue')
        self.chooselbl.grid(row = 14, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_ambulance, 
            value = binary_value[i], command = self.ambulance_click)
            self.rdbtn.grid(row = 14, column = i+3, sticky = W+N)
        
        #   Fire Truck:
        self.tkvar_firetruck = StringVar(self.parent)
        self.cur_firetruck = 0
        self.tkvar_firetruck.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Fire Truck", bg='LightBlue')
        self.chooselbl.grid(row = 15, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_firetruck, 
            value = binary_value[i], command = self.firetruck_click)
            self.rdbtn.grid(row = 15, column = i+3, sticky = W+N)

        #   Taxi:
        self.tkvar_taxi = StringVar(self.parent)
        self.cur_taxi = 0
        self.tkvar_taxi.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Taxi", bg='LightBlue')
        self.chooselbl.grid(row = 16, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_taxi, 
            value = binary_value[i], command = self.taxi_click)
            self.rdbtn.grid(row = 16, column = i+3, sticky = W+N)
            
        #   Others:
        self.tkvar_others = StringVar(self.parent)
        self.cur_others = 0
        self.tkvar_others.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Others", bg='LightBlue')
        self.chooselbl.grid(row = 17, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_others, 
            value = binary_value[i], command = self.others_click)
            self.rdbtn.grid(row = 17, column = i+3, sticky = W+N)
        
        # Space
        self.chooselbl = Label(self.frame, text = "        ", bg='LightBlue')
        self.chooselbl.grid(row = 1, column = 5, sticky=W+N)
        
        #   Make:
        self.chooselbl = Label(self.frame, text = "Make       ", bg='LightBlue')
        self.chooselbl.grid(row = 1, column = 7, sticky=W+N)

        # no/yes label
        for i in range(len(binary_label)):
            self.chooselbl = Label(self.frame, text = binary_label[i], bg='LightBlue')
            self.chooselbl.grid(row = 1, column = i+8, sticky = W+N)
            
        #   Audi:
        self.tkvar_audi = StringVar(self.parent)
        self.cur_audi = 0
        self.tkvar_audi.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Audi", bg='LightBlue')
        self.chooselbl.grid(row = 2, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_audi, 
            value = binary_value[i], command = self.audi_click)
            self.rdbtn.grid(row = 2, column = i+8, sticky = W+N)
        
        #   BMW:
        self.tkvar_bmw = StringVar(self.parent)
        self.cur_bmw = 0
        self.tkvar_bmw.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "BMW", bg='LightBlue')
        self.chooselbl.grid(row = 3, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_bmw, 
            value = binary_value[i], command = self.bmw_click)
            self.rdbtn.grid(row = 3, column = i+8, sticky = W+N)
        
        #   Chevrolet:
        self.tkvar_chevrolet = StringVar(self.parent)
        self.cur_chevrolet = 0
        self.tkvar_chevrolet.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Chevrolet", bg='LightBlue')
        self.chooselbl.grid(row = 4, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_chevrolet, 
            value = binary_value[i], command = self.chevrolet_click)
            self.rdbtn.grid(row = 4, column = i+8, sticky = W+N)
        
        #   Ford:
        self.tkvar_ford = StringVar(self.parent)
        self.cur_ford = 0
        self.tkvar_ford.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Ford", bg='LightBlue')
        self.chooselbl.grid(row = 5, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_ford, 
            value = binary_value[i], command = self.ford_click)
            self.rdbtn.grid(row = 5, column = i+8, sticky = W+N)
        
        #   Honda:
        self.tkvar_honda = StringVar(self.parent)
        self.cur_honda = 0
        self.tkvar_honda.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Honda", bg='LightBlue')
        self.chooselbl.grid(row = 6, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_honda, 
            value = binary_value[i], command = self.honda_click)
            self.rdbtn.grid(row = 6, column = i+8, sticky = W+N)
            
        #   Huyndai:
        self.tkvar_huyndai = StringVar(self.parent)
        self.cur_huyndai = 0
        self.tkvar_huyndai.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Hyundai", bg='LightBlue')
        self.chooselbl.grid(row = 7, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_huyndai, 
            value = binary_value[i], command = self.huyndai_click)
            self.rdbtn.grid(row = 7, column = i+8, sticky = W+N)
            
        #   Isuzu:
        self.tkvar_isuzu = StringVar(self.parent)
        self.cur_isuzu = 0
        self.tkvar_isuzu.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Isuzu", bg='LightBlue')
        self.chooselbl.grid(row = 8, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_isuzu, 
            value = binary_value[i], command = self.isuzu_click)
            self.rdbtn.grid(row = 8, column = i+8, sticky = W+N)
        
        #   Kia:
        self.tkvar_kia = StringVar(self.parent)
        self.cur_kia = 0
        self.tkvar_kia.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Kia", bg='LightBlue')
        self.chooselbl.grid(row = 9, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_kia, 
            value = binary_value[i], command = self.kia_click)
            self.rdbtn.grid(row = 9, column = i+8, sticky = W+N)
            
        #   Lexus:
        self.tkvar_lexus = StringVar(self.parent)
        self.cur_lexus = 0
        self.tkvar_lexus.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Lexus", bg='LightBlue')
        self.chooselbl.grid(row = 10, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_lexus, 
            value = binary_value[i], command = self.lexus_click)
            self.rdbtn.grid(row = 10, column = i+8, sticky = W+N)
    
        #   Mazda:
        self.tkvar_mazda = StringVar(self.parent)
        self.cur_mazda = 0
        self.tkvar_mazda.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Mazda", bg='LightBlue')
        self.chooselbl.grid(row = 11, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_mazda, 
            value = binary_value[i], command = self.mazda_click)
            self.rdbtn.grid(row = 11, column = i+8, sticky = W+N)
    
        #   Mercedes:
        self.tkvar_mercedes = StringVar(self.parent)
        self.cur_mercedes = 0
        self.tkvar_mercedes.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Mercedes", bg='LightBlue')
        self.chooselbl.grid(row = 12, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_mercedes, 
            value = binary_value[i], command = self.mercedes_click)
            self.rdbtn.grid(row = 12, column = i+8, sticky = W+N)
        
        #   Mini Cooper:
        self.tkvar_minicooper = StringVar(self.parent)
        self.cur_minicooper = 0
        self.tkvar_minicooper.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Mini Cooper", bg='LightBlue')
        self.chooselbl.grid(row = 13, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_minicooper, 
            value = binary_value[i], command = self.minicooper_click)
            self.rdbtn.grid(row = 13, column = i+8, sticky = W+N)
            
        #   Mitsubishi:
        self.tkvar_mitsubishi = StringVar(self.parent)
        self.cur_mitsubishi = 0
        self.tkvar_mitsubishi.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Mitsubishi", bg='LightBlue')
        self.chooselbl.grid(row = 14, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_mitsubishi, 
            value = binary_value[i], command = self.mitsubishi_click)
            self.rdbtn.grid(row = 14, column = i+8, sticky = W+N)
        
        #   Nissan:
        self.tkvar_nissan = StringVar(self.parent)
        self.cur_nissan = 0
        self.tkvar_nissan.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Nissan", bg='LightBlue')
        self.chooselbl.grid(row = 15, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_nissan, 
            value = binary_value[i], command = self.nissan_click)
            self.rdbtn.grid(row = 15, column = i+8, sticky = W+N)
            
        #   Peugeot:
        self.tkvar_peugeot = StringVar(self.parent)
        self.cur_peugeot = 0
        self.tkvar_peugeot.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Peugeot", bg='LightBlue')
        self.chooselbl.grid(row = 16, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_peugeot, 
            value = binary_value[i], command = self.peugeot_click)
            self.rdbtn.grid(row = 16, column = i+8, sticky = W+N)
            
        #   Porsche:
        self.tkvar_porsche = StringVar(self.parent)
        self.cur_porsche = 0
        self.tkvar_porsche.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Porsche", bg='LightBlue')
        self.chooselbl.grid(row = 17, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_porsche, 
            value = binary_value[i], command = self.porsche_click)
            self.rdbtn.grid(row = 17, column = i+8, sticky = W+N)
            
        #   Suzuki
        self.tkvar_suzuki = StringVar(self.parent)
        self.cur_suzuki = 0
        self.tkvar_suzuki.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Suzuki", bg='LightBlue')
        self.chooselbl.grid(row = 18, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_suzuki, 
            value = binary_value[i], command = self.suzuki_click)
            self.rdbtn.grid(row = 18, column = i+8, sticky = W+N)
            
        #   Toyota:
        self.tkvar_toyota = StringVar(self.parent)
        self.cur_toyota = 0
        self.tkvar_toyota.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Toyota", bg='LightBlue')
        self.chooselbl.grid(row = 19, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_toyota, 
            value = binary_value[i], command = self.toyota_click)
            self.rdbtn.grid(row = 19, column = i+8, sticky = W+N)
        
        #   Vinfast:
        self.tkvar_vinfast = StringVar(self.parent)
        self.cur_vinfast = 0
        self.tkvar_vinfast.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Vinfast", bg='LightBlue')
        self.chooselbl.grid(row = 20, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_vinfast, 
            value = binary_value[i], command = self.vinfast_click)
            self.rdbtn.grid(row = 20, column = i+8, sticky = W+N)
            
        #   Volkswagen:
        self.tkvar_volkswagen = StringVar(self.parent)
        self.cur_volkswagen = 0
        self.tkvar_volkswagen.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Volkswagen", bg='LightBlue')
        self.chooselbl.grid(row = 21, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_volkswagen, 
            value = binary_value[i], command = self.volkswagen_click)
            self.rdbtn.grid(row = 21, column = i+8, sticky = W+N)
            
        #   Volvo:
        self.tkvar_volvo = StringVar(self.parent)
        self.cur_volvo = 0
        self.tkvar_volvo.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Volvo", bg='LightBlue')
        self.chooselbl.grid(row = 22, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_volvo, 
            value = binary_value[i], command = self.volvo_click)
            self.rdbtn.grid(row = 22, column = i+8, sticky = W+N)

        #   Others Car:
        self.tkvar_others2 = StringVar(self.parent)
        self.cur_others2 = 0
        self.tkvar_others2.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Others", bg='LightBlue')
        self.chooselbl.grid(row = 23, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_others2, 
            value = binary_value[i], command = self.others2_click)
            self.rdbtn.grid(row = 23, column = i+8, sticky = W+N)
          
        # Space
        self.chooselbl = Label(self.frame, text = "        ", bg='LightBlue')
        self.chooselbl.grid(row = 1, column = 10, sticky=W+N)
        
        #   Color:
        self.chooselbl = Label(self.frame, text = "Color       ", bg='LightBlue')
        self.chooselbl.grid(row = 1, column = 13, sticky=W+N)

        # no/yes label
        for i in range(len(binary_label)):
            self.chooselbl = Label(self.frame, text = binary_label[i], bg='LightBlue')
            self.chooselbl.grid(row = 1, column = i+14, sticky = W+N)
            
        #   Black:
        self.tkvar_black = StringVar(self.parent)
        self.black = 0
        self.tkvar_black.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Black", bg='LightBlue')
        self.chooselbl.grid(row = 2, column = 13, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_black, 
            value = binary_value[i], command = self.black_click)
            self.rdbtn.grid(row = 2, column = i + 14, sticky = W+N)
            
        #   Blue:
        self.tkvar_blue = StringVar(self.parent)
        self.blue = 0
        self.tkvar_blue.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Blue", bg='LightBlue')
        self.chooselbl.grid(row = 3, column = 13, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_blue, 
            value = binary_value[i], command = self.blue_click)
            self.rdbtn.grid(row = 3, column = i + 14, sticky = W+N)
        
        #   Brown:
        self.tkvar_brown = StringVar(self.parent)
        self.brown = 0
        self.tkvar_brown.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Brown", bg='LightBlue')
        self.chooselbl.grid(row = 4, column = 13, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_brown, 
            value = binary_value[i], command = self.brown_click)
            self.rdbtn.grid(row = 4, column = i + 14, sticky = W+N)
            
        #   Gray:
        self.tkvar_gray = StringVar(self.parent)
        self.gray = 0
        self.tkvar_gray.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Gray", bg='LightBlue')
        self.chooselbl.grid(row = 5, column = 13, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_gray, 
            value = binary_value[i], command = self.gray_click)
            self.rdbtn.grid(row = 5, column = i + 14, sticky = W+N)
            
        #   Green:
        self.tkvar_green = StringVar(self.parent)
        self.green = 0
        self.tkvar_green.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Green", bg='LightBlue')
        self.chooselbl.grid(row = 6, column = 13, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_green, 
            value = binary_value[i], command = self.green_click)
            self.rdbtn.grid(row = 6, column = i + 14, sticky = W+N)
        
        #   Red:
        self.tkvar_red = StringVar(self.parent)
        self.red = 0
        self.tkvar_red.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Red", bg='LightBlue')
        self.chooselbl.grid(row = 7, column = 13, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_red, 
            value = binary_value[i], command = self.red_click)
            self.rdbtn.grid(row = 7, column = i + 14, sticky = W+N)
        
        #   Silver
        self.tkvar_silver = StringVar(self.parent)
        self.silver = 0
        self.tkvar_silver.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Silver", bg='LightBlue')
        self.chooselbl.grid(row = 8, column = 13, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_silver, 
            value = binary_value[i], command = self.silver_click)
            self.rdbtn.grid(row = 8, column = i+14, sticky = W+N)

        #   White
        self.tkvar_white = StringVar(self.parent)
        self.white = 0
        self.tkvar_white.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "White", bg='LightBlue')
        self.chooselbl.grid(row = 9, column = 13, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_white, 
            value = binary_value[i], command = self.white_click)
            self.rdbtn.grid(row = 9, column = i+14, sticky = W+N)
            
        #   Yellow
        self.tkvar_yellow = StringVar(self.parent)
        self.yellow = 0
        self.tkvar_yellow.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Yellow", bg='LightBlue')
        self.chooselbl.grid(row = 10, column = 13, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_yellow, 
            value = binary_value[i], command = self.yellow_click)
            self.rdbtn.grid(row = 10, column = i+14, sticky = W+N)
        
            
        #   Other color:
        self.tkvar_others3 = StringVar(self.parent)
        self.others3 = 0
        self.tkvar_others3.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Others", bg='LightBlue')
        self.chooselbl.grid(row = 11, column = 13, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_others3, 
            value = binary_value[i], command = self.others3_click)
            self.rdbtn.grid(row = 11, column = i + 14, sticky = W+N)

        # # Creating a text box widget
        # self.canvas1 = Canvas(self.frame)
        # self.canvas1.grid(row = 15, column = 1, rowspan = 5,sticky = W+N)
        # self.label3 = tk.Label(self.canvas1, text= '',font=('helvetica', 20))
        
        
        # main panel for labeling
        self.mainPanel = Canvas(self.frame, cursor='tcross')
        self.parent.bind("<Left>", self.prevImage) # press 'a' to go backward
        self.parent.bind("<Right>", self.nextImage) # press 'd' to go forward
        self.mainPanel.grid(row = 1, column = 1, rowspan = 10, sticky = W+N)

        # control panel for image navigation
        #self.ctrPanel = Frame(self.frame)
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row = 30, column = 1, columnspan = 2, sticky = W+S)
        #self.ctrPanel.pack(padx = 30, pady = 1)
        self.prevBtn = Button(self.ctrPanel, text='<< Prev', width = 10, command = self.prevImage)
        self.prevBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.nextBtn = Button(self.ctrPanel, text='Next >>', width = 10, command = self.nextImage)
        self.nextBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.progLabel = Label(self.ctrPanel, text = "Progress:     /    ")
        self.progLabel.pack(side = LEFT, padx = 5)
        self.tmpLabel = tk.Label(self.ctrPanel, text = "Go to Image No.")
        self.tmpLabel.pack(side = LEFT, padx = 5)
        self.v = StringVar(self.ctrPanel)
        self.idxEntry = Entry(self.ctrPanel, width = 5,textvariable=self.v)
        self.idxEntry.pack(side = LEFT)
        # self.idxEntry = Text(self.ctrPanel, height = 5,width = 5)
        # self.idxEntry.grid(row=0, column=5)
        
        self.goBtn = Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        self.goBtn.pack(side = LEFT)
        self.delBtn = Button(self.ctrPanel, text = 'Delete', command = self.deleteImage)
        self.delBtn.pack(side = LEFT)

        self.frame.columnconfigure(1, weight = 1)
        #self.frame.rowconfigure(4, weight = 1)

    def loadEntry(self,event):
        self.loadDir()

    def loadDir(self, dbg = False):
        if not dbg:
            try:
                s = self.entry.get()
                self.parent.focus()
                self.category = s
            except ValueError as ve:
                tkMessageBox.showerror("Error!", message = "The folder should be numbers")
                return
        #print(os.getcwd())
        if not os.path.isdir('E:/CMC/Scrap_Car_2/audi_a1/%s' % self.category):
           tkMessageBox.showerror("Error!", message = "The specified dir doesn't exist!")
           return
        # get image list
        self.imageDir = os.path.join(r'E:/CMC/Scrap_Car_2/audi_a1/', '%s' %(self.category))
        self.imageList = glob.glob(os.path.join(self.imageDir, '*.jpg'))
        if len(self.imageList) == 0:
            print('No .jpg images found in the specified dir!')
            tkMessageBox.showerror("Error!", message = "No .jpg images found in the specified dir!")
            return

        # default to the 1st image in the collection
        self.cur = 0
        self.total = len(self.imageList)

         # set up output dir
        if not os.path.exists('E:/CMC/Scrap_Car_2_Labels/audi_a1'):
            os.mkdir('E:/CMC/Scrap_Car_2_Labels/audi_a1') # Create Labels2 directory
        self.outDir = os.path.join(r'E:/CMC/Scrap_Car_2_Labels/audi_a1', '%s' %(self.category))
        
        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)
        self.loadImage()
        print('%d images loaded from %s' %(self.total, s))

    def loadImage(self):
        # load image
        # path = "E:/CMC/Scrap_Car/toyota"
        # dir_list = os.listdir(path)
        # for i in range(len(dir_list)):
        imagepath = self.imageList[self.cur]
        self.img = PImage.open(imagepath)
        self.curimg_w, self.curimg_h = self.img.size
        aspect_h = int(self.curimg_h/300)
        if self.curimg_h>300:
            aspect_w = int(self.curimg_w/aspect_h)         
            self.img = self.img.resize((aspect_w, 300))
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.mainPanel.config(width = max(self.tkimg.width(), 300), height = max(self.tkimg.height(), 300))
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW)
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor="nw")
        #print(self.tkimg)
        #print(self.img)
        message_text = ''
        ## load labels
        # self.imagename = os.path.split(imagepath)[-1].split('.')[0]
        self.imagename = os.path.splitext(os.path.basename(imagepath))[0]
        labelname = self.imagename + '.txt'
        self.labelfilename = os.path.join(self.outDir, labelname)
        self.imagefilename = os.path.join(self.imageDir, self.imagename+".jpg")
        
        #   Name Image
        self.chooselbl = Label(self.frame, text = self.imagename, bg='LightBlue')
        self.chooselbl.grid(row = 11, column = 1 , sticky=W+N)
        
        
        if os.path.exists(self.labelfilename):
            with open(self.labelfilename) as f:
                temp_data_str=f.read().replace("\n","")
            temp_data=temp_data_str.split(",")
            print(temp_data)

            self.cur_car = binary_value.index(temp_data[0])
            self.tkvar_car.set(temp_data[0])

            self.cur_motorbike = binary_value.index(temp_data[1])
            self.tkvar_motorbike.set(temp_data[1])

            self.cur_bike = binary_value.index(temp_data[2])
            self.tkvar_bike.set(temp_data[2])

            self.cur_sedan = binary_value.index(temp_data[3])
            self.tkvar_sedan.set(temp_data[3])
            
            self.cur_suv = binary_value.index(temp_data[4])
            self.tkvar_suv.set(temp_data[4])
            
            self.cur_minivan = binary_value.index(temp_data[5])
            self.tkvar_minivan.set(temp_data[5])
            
            self.cur_microbus = binary_value.index(temp_data[6])
            self.tkvar_microbus.set(temp_data[6])
            
            self.cur_car24 = binary_value.index(temp_data[7])
            self.tkvar_car24.set(temp_data[7])
            
            self.cur_bus = binary_value.index(temp_data[8])
            self.tkvar_bus.set(temp_data[8])
        
            self.cur_truck = binary_value.index(temp_data[9])
            self.tkvar_truck.set(temp_data[9])
            
            self.cur_police = binary_value.index(temp_data[10])
            self.tkvar_police.set(temp_data[10])
            
            self.cur_ambulance = binary_value.index(temp_data[11])
            self.tkvar_ambulance.set(temp_data[11])
            
            self.cur_firetruck = binary_value.index(temp_data[12])
            self.tkvar_firetruck.set(temp_data[12])   
            
            self.cur_taxi = binary_value.index(temp_data[13])
            self.tkvar_taxi.set(temp_data[13]) 
            
            self.cur_others = binary_value.index(temp_data[14])
            self.tkvar_others.set(temp_data[14])     
            
            self.cur_audi = binary_value.index(temp_data[15])
            self.tkvar_audi.set(temp_data[15]) 
            
            self.cur_bmw = binary_value.index(temp_data[16])
            self.tkvar_bmw.set(temp_data[16]) 
            
            self.cur_chevrolet = binary_value.index(temp_data[17])
            self.tkvar_chevrolet.set(temp_data[17]) 
            
            self.cur_ford = binary_value.index(temp_data[18])
            self.tkvar_ford.set(temp_data[18]) 
            
            self.cur_honda = binary_value.index(temp_data[19])
            self.tkvar_honda.set(temp_data[19])    
            
            self.cur_huyndai = binary_value.index(temp_data[20])
            self.tkvar_huyndai.set(temp_data[20])
            
            self.cur_isuzu = binary_value.index(temp_data[21])
            self.tkvar_isuzu.set(temp_data[21])
            
            self.cur_kia = binary_value.index(temp_data[22])
            self.tkvar_kia.set(temp_data[22])
            
            self.cur_lexus = binary_value.index(temp_data[23])
            self.tkvar_lexus.set(temp_data[23])
            
            self.cur_mazda = binary_value.index(temp_data[24])
            self.tkvar_mazda.set(temp_data[24])         
            
            self.cur_mercedes = binary_value.index(temp_data[25])
            self.tkvar_mercedes.set(temp_data[25])
            
            self.cur_minicooper = binary_value.index(temp_data[26])
            self.tkvar_minicooper.set(temp_data[26])
            
            self.cur_mitsubishi = binary_value.index(temp_data[27])
            self.tkvar_mitsubishi.set(temp_data[27])
            
            self.cur_nissan = binary_value.index(temp_data[28])
            self.tkvar_nissan.set(temp_data[28])
            
            self.cur_peugeot = binary_value.index(temp_data[29])
            self.tkvar_peugeot.set(temp_data[29])
            
            self.cur_porsche = binary_value.index(temp_data[30])
            self.tkvar_porsche.set(temp_data[30])
            
            self.cur_suzuki = binary_value.index(temp_data[31])
            self.tkvar_suzuki.set(temp_data[31])
            
            self.cur_toyota = binary_value.index(temp_data[32])
            self.tkvar_toyota.set(temp_data[32])  
            
            self.cur_vinfast = binary_value.index(temp_data[33])
            self.tkvar_vinfast.set(temp_data[33])
            
            self.cur_volkswagen = binary_value.index(temp_data[34])
            self.tkvar_volkswagen.set(temp_data[34])
            
            self.cur_volvo = binary_value.index(temp_data[35])
            self.tkvar_volvo.set(temp_data[35])
            
            self.cur_others2 = binary_value.index(temp_data[36])
            self.tkvar_others2.set(temp_data[36])  
            
            
            self.black = binary_value.index(temp_data[37])
            self.tkvar_black.set(temp_data[37])
            
            self.blue = binary_value.index(temp_data[38])
            self.tkvar_blue.set(temp_data[38])
            
            self.brown = binary_value.index(temp_data[39])
            self.tkvar_brown.set(temp_data[39])
            
            self.gray = binary_value.index(temp_data[40])
            self.tkvar_gray.set(temp_data[40])
            
            self.green = binary_value.index(temp_data[41])
            self.tkvar_green.set(temp_data[41])
            
            self.red = binary_value.index(temp_data[42])
            self.tkvar_red.set(temp_data[42])
            
            self.silver = binary_value.index(temp_data[43])
            self.tkvar_silver.set(temp_data[43])
            
            self.white = binary_value.index(temp_data[44])
            self.tkvar_white.set(temp_data[44])     
            
            self.yellow = binary_value.index(temp_data[45])
            self.tkvar_yellow.set(temp_data[45]) 
            
            self.other = binary_value.index(temp_data[46])
            self.tkvar_others3.set(temp_data[46])
                   

        self.progLabel.config(text = "%04d/%04d" %(self.cur, self.total))

    def saveImage(self):
        with open(self.labelfilename, 'w') as f:
            f.write(self.tkvar_car.get()+','+self.tkvar_motorbike.get()+','+self.tkvar_bike.get()
            +','+self.tkvar_sedan.get()+','+self.tkvar_suv.get()+','+self.tkvar_minivan.get()+','+self.tkvar_microbus.get()
            +','+self.tkvar_car24.get()+','+self.tkvar_bus.get()+','+self.tkvar_truck.get()+','+self.tkvar_police.get()+','+self.tkvar_ambulance.get()
            +','+self.tkvar_firetruck.get()+','+self.tkvar_taxi.get()+','+self.tkvar_others.get()
            
            +','+self.tkvar_audi.get()+','+self.tkvar_bmw.get()
            +','+self.tkvar_chevrolet.get()+','+self.tkvar_ford.get()+','+self.tkvar_honda.get()+','+self.tkvar_huyndai.get()+','+self.tkvar_isuzu.get()
            +','+self.tkvar_kia.get()+','+self.tkvar_lexus.get()+','+self.tkvar_mazda.get()+','+self.tkvar_mercedes.get()+','+self.tkvar_minicooper.get()
            +','+self.tkvar_mitsubishi.get()+','+self.tkvar_nissan.get()+','+self.tkvar_peugeot.get()+','+self.tkvar_porsche.get()
            +','+self.tkvar_suzuki.get()+','+self.tkvar_toyota.get()+','+self.tkvar_vinfast.get()+','+self.tkvar_volkswagen.get()
            +','+self.tkvar_volvo.get()+','+self.tkvar_others2.get()
            
            +','+self.tkvar_black.get()+','+self.tkvar_blue.get()+','+self.tkvar_brown.get()+','+self.tkvar_gray.get()+','+self.tkvar_green.get()
            +','+self.tkvar_red.get()+','+self.tkvar_silver.get()+','+self.tkvar_white.get()+','+self.tkvar_yellow.get()+','+self.tkvar_others3.get())
        print('Image No. %d saved' %(self.cur))
        
        # # Copy image 
        # source = self.imageList[self.cur]
        # destination = r"E:/CMC/Data Car/Car_from_bonbanh"
        # try:
        #     shutil.copy(source, destination)
        #     print("File copied successfully.")
        # # If source and destination are same
        # except shutil.SameFileError:
        #     print("Source and destination represents the same file.")
        
        # # If there is any permission issue
        # except PermissionError:
        #     print("Permission denied.")
        # # For other errors
        # except:
        #     print("Error occurred while copying file.")
            
            
    def prevImage(self, event = None):
        self.saveImage()
        if self.cur > 0:
            self.cur -= 1
            self.loadImage()
        else:
            tkMessageBox.showerror("Information!", message = "This is first image")

    def nextImage(self, event = None):
        self.saveImage()
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()
        else:
            tkMessageBox.showerror("Information!", message = "All images annotated")

    def gotoImage(self):
        print("Image No:",self.idxEntry.get())
        idx = int(self.idxEntry.get())
        if 1 <= idx and idx <= self.total:
            self.saveImage()
            self.cur = idx
            self.loadImage()

    def deleteImage(self):
        self.saveImage()    
        # Chuyển label đó vào file Deleted
        shutil.move(self.labelfilename, os.path.join('E:/CMC/Scrap_Car_2_Deleted_Labels/audi_a1',self.labelfilename.split('/')[0]))
        # Chuyển ảnh gốc vào file Deleted
        shutil.move(self.imagefilename, os.path.join('E:/CMC/Scrap_Car_2_Deleted_Images/audi_a1',self.imagefilename.split('/')[0]))
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()
        else:
            tkMessageBox.showerror("Information!", message = "All images annotated")


    def car_click(self, *args):
        cur_car = self.tkvar_car.get()
        self.cur_car = binary_value.index(cur_car)

    def motorbike_click(self, *args):
        cur_motorbike = self.tkvar_motorbike.get()
        self.cur_motorbike = binary_value.index(cur_motorbike)

    def bike_click(self, *args):
        cur_bike = self.tkvar_bike.get()
        self.cur_bike = binary_value.index(cur_bike)
    
    def sedan_click(self, *args):
        cur_sedan = self.tkvar_sedan.get()
        self.cur_sedan = binary_value.index(cur_sedan)
    
    def suv_click(self, *args):
        cur_suv = self.tkvar_suv.get()
        self.cur_suv = binary_value.index(cur_suv)

    def minivan_click(self, *args):
        cur_minivan = self.tkvar_minivan.get()
        self.cur_minivan = binary_value.index(cur_minivan)

    def microbus_click(self, *args):
        cur_microbus = self.tkvar_microbus.get()
        self.cur_microbus = binary_value.index(cur_microbus)
    
    def car24_click(self, *args):
        cur_car24 = self.tkvar_car24.get()
        self.cur_car24 = binary_value.index(cur_car24)
 
    def bus_click(self, *args):
        cur_bus = self.tkvar_bus.get()
        self.cur_bus = binary_value.index(cur_bus)     
        
    def truck_click(self, *args):
        cur_truck = self.tkvar_truck.get()
        self.cur_truck = binary_value.index(cur_truck)  
 
    def police_click(self, *args):
        cur_police = self.tkvar_police.get()
        self.cur_police = binary_value.index(cur_police)

    def ambulance_click(self, *args):
        cur_ambulance = self.tkvar_ambulance.get()
        self.cur_ambulance = binary_value.index(cur_ambulance)   

    def firetruck_click(self, *args):
        cur_firetruck = self.tkvar_firetruck.get()
        self.cur_firetruck = binary_value.index(cur_firetruck) 

    def taxi_click(self, *args):
        cur_taxi = self.tkvar_taxi.get()
        self.cur_taxi = binary_value.index(cur_taxi)

    def others_click(self, *args):
        cur_others = self.tkvar_others.get()
        self.cur_others = binary_value.index(cur_others)

    def toyota_click(self, *args):
        cur_toyota = self.tkvar_toyota.get()
        self.cur_toyota = binary_value.index(cur_toyota)
        
    def ford_click(self, *args):
        cur_ford = self.tkvar_ford.get()
        self.cur_ford = binary_value.index(cur_ford)
        
    def kia_click(self, *args):
        cur_kia = self.tkvar_kia.get()
        self.cur_kia = binary_value.index(cur_kia)

    def mazda_click(self, *args):
        cur_mazda = self.tkvar_mazda.get()
        self.cur_mazda = binary_value.index(cur_mazda)

    def honda_click(self, *args):
        cur_honda = self.tkvar_honda.get()
        self.cur_honda = binary_value.index(cur_honda)
        
    def huyndai_click(self, *args):
        cur_huyndai = self.tkvar_huyndai.get()
        self.cur_huyndai = binary_value.index(cur_huyndai)
        
    def mercedes_click(self, *args):
        cur_mercedes = self.tkvar_mercedes.get()
        self.cur_mercedes = binary_value.index(cur_mercedes)
        
    def audi_click(self, *args):
        cur_audi = self.tkvar_audi.get()
        self.cur_audi = binary_value.index(cur_audi)
        
    def bmw_click(self, *args):
        cur_bmw = self.tkvar_bmw.get()
        self.cur_bmw = binary_value.index(cur_bmw)
        
    def chevrolet_click(self, *args):
        cur_chevrolet = self.tkvar_chevrolet.get()
        self.cur_chevrolet = binary_value.index(cur_chevrolet)
        
    def isuzu_click(self, *args):
        cur_isuzu = self.tkvar_isuzu.get()
        self.cur_isuzu = binary_value.index(cur_isuzu)
            
    def lexus_click(self, *args):
        cur_lexus = self.tkvar_lexus.get()
        self.cur_lexus = binary_value.index(cur_lexus)
            
    def minicooper_click(self, *args):
        cur_minicooper = self.tkvar_minicooper.get()
        self.cur_minicooper = binary_value.index(cur_minicooper)
        
    def mitsubishi_click(self, *args):
        cur_mitsubishi = self.tkvar_mitsubishi.get()
        self.cur_mitsubishi = binary_value.index(cur_mitsubishi)
        
    def nissan_click(self, *args):
        cur_nissan = self.tkvar_nissan.get()
        self.cur_nissan = binary_value.index(cur_nissan)
        
    def peugeot_click(self, *args):
        cur_peugeot = self.tkvar_peugeot.get()
        self.cur_peugeot = binary_value.index(cur_peugeot)
    
    def porsche_click(self, *args):
        cur_porsche = self.tkvar_porsche.get()
        self.cur_porsche = binary_value.index(cur_porsche)
        
    def suzuki_click(self, *args):
        cur_suzuki = self.tkvar_suzuki.get()
        self.cur_suzuki = binary_value.index(cur_suzuki)
        
    def vinfast_click(self, *args):
        cur_vinfast = self.tkvar_vinfast.get()
        self.cur_vinfast = binary_value.index(cur_vinfast)
        
    def volkswagen_click(self, *args):
        cur_volkswagen = self.tkvar_volkswagen.get()
        self.cur_volkswagen = binary_value.index(cur_volkswagen)
    
    def volvo_click(self, *args):
        cur_volvo = self.tkvar_volvo.get()
        self.cur_volvo = binary_value.index(cur_volvo)
    
    def others2_click(self, *args):
        cur_others2 = self.tkvar_others2.get()
        self.cur_others2 = binary_value.index(cur_others2)
        
    
    def black_click(self, *args):
        black = self.tkvar_black.get()
        self.black = binary_value.index(black)
    
    def white_click(self, *args):
        white = self.tkvar_white.get()
        self.white = binary_value.index(white)
    
    def silver_click(self, *args):
        silver = self.tkvar_silver.get()
        self.silver = binary_value.index(silver)
        
    def gray_click(self, *args):
        gray = self.tkvar_gray.get()
        self.gray = binary_value.index(gray)
    
    def red_click(self, *args):
        red = self.tkvar_red.get()
        self.red = binary_value.index(red)
    
    def green_click(self, *args):
        green = self.tkvar_green.get()
        self.green = binary_value.index(green)
    
    def blue_click(self, *args):
        blue = self.tkvar_blue.get()
        self.blue = binary_value.index(blue)
    
    def brown_click(self, *args):
        brown = self.tkvar_brown.get()
        self.brown = binary_value.index(brown)
    
    def yellow_click(self, *args):
        yellow = self.tkvar_yellow.get()
        self.yellow = binary_value.index(yellow)
    
    def others3_click(self, *args):
        others3 = self.tkvar_others3.get()
        self.others3 = binary_value.index(others3)


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(5, minsize=100)
    tool = LabelTool(root)
    root.resizable(width =  True, height = True)
    root.mainloop()