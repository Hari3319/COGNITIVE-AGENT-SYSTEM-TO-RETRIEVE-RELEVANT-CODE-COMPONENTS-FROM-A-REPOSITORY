
from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
from tkinter.filedialog import askopenfilename
import pandas as pd 
import os
from PIL import ImageTk, Image
from CodeObject import *
from nltk.corpus import stopwords
from collections import Counter
import re, math
import matplotlib.pyplot as plt


main = tkinter.Tk()
main.title("Retrieve Relevant Code Components") #designing main screen
main.geometry("1300x1200")

pattern = r'[^A-Za-z ]'
regex = re.compile(pattern)
STOPWORDS = set(stopwords.words('english'))
WORD = re.compile(r'\w+')

global filename
code_array = []
train_vector = []
global predicted

def upload(event): #function to upload tweeter profile
    global filename
    filename = filedialog.askdirectory(initialdir=".")
    text.delete('1.0', END)
    text.insert(END,filename+" loaded\n");
    

def preprocess(event):
    code_array.clear()
    for root, dirs, files in os.walk(filename):
        for fdata in files:
            textdata = ''
            print('Reading Program '+fdata)
            with open(root+"/"+fdata, "r") as file:
                for line in file:
                    line = line.strip('\n')
                    line = line.strip()
                    line = regex.sub(' ', line)
                    textdata+=line.lower()+' '
                    for word in STOPWORDS:
                        token = ' ' + word + ' '
                        textdata = textdata.replace(token, ' ')
                        textdata = textdata.replace(' ', ' ')
            code = CodeObject()
            code.setName(fdata)
            code.setCode(textdata)
            code_array.append(code);
    text.insert(END,"Preprocessing Task Completed\n");
    text.insert(END,"Total Number of Programs in Repository = "+str(len(code_array)))

def code_to_vector(program):
     words = WORD.findall(program)
     return Counter(words)

def CodeToVector(event):
    vec = ''
    train_vector.clear()
    for code in code_array:
        vector = code_to_vector(code.getCode())
        vec+=code.getName()+' '+str(vector)+'\n'
        train_vector.append(vector);
            
    text.delete('1.0', END)
    text.insert(END,vec);
            
        
def predict(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator
    
def query(event):
    global predicted
    text.delete('1.0', END)
    query = query_field.get()
    output = ''
    if len(query) > 0:
        query = query.lower()
        predicted = 0
        test_vector = code_to_vector(query)
        for i in range(len(train_vector)):
            train_vectors = train_vector[i]
            program = code_array[i].getName()
            predict_score = predict(train_vectors,test_vector)
            if predict_score > 0:
                output+=program+' Predicted Score : '+str(predict_score)+'\n'
                predicted = predicted + 1
        if len(output) > 0:
            text.insert(END,'Below are the Retrieve Component For Given Query\n\n');
            text.insert(END,output);
        else:
            text.insert(END,'No predicted component found for given query')
    else:
        text.insert(END,'Query must not be empty')
                        
                
            

def graph(event):
    height = [len(train_vector), predicted]
    bars = ('Total Components', 'Predicted Components')
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.show()
     

def quit(event):
   main.destroy()    
    
    
font = ('times', 16, 'bold')
title = Label(main, text='Cognitive Agent System to Retrieve Relevant Code Components from a Repository')
title.config(bg='greenyellow', fg='dodger blue')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 14, 'bold')

querylabel = Label(main, text='Enter Query Here')
querylabel.place(x=300,y=120)
querylabel.config(font=font1)
query_field = Entry(main,width=50)
query_field.place(x=480,y=120)
query_field.config(font=font1)

font1 = ('times', 12, 'bold')
text=Text(main,height=17,width=150)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=50,y=170)
text.config(font=font1)


img = ImageTk.PhotoImage(Image.open("icons/b1.png"))
uploadButton = Button(main, text="", image = img)
uploadButton.place(x=50,y=530)
uploadButton.config(font=font1)
uploadButton.bind('<Button-1>',upload)

img1 = ImageTk.PhotoImage(Image.open("icons/b2.png"))
preprocessButton = Button(main, text="", image = img1)
preprocessButton.place(x=400,y=530)
preprocessButton.config(font=font1)
preprocessButton.bind('<Button-1>',preprocess)

img2 = ImageTk.PhotoImage(Image.open("icons/b3.png"))
codevecButton = Button(main, text="", image = img2)
codevecButton.place(x=750,y=530)
codevecButton.config(font=font1)
codevecButton.bind('<Button-1>',CodeToVector)

img3 = ImageTk.PhotoImage(Image.open("icons/b4.png"))
queryButton = Button(main, text="", image = img3)
queryButton.place(x=50,y=620)
queryButton.config(font=font1)
queryButton.bind('<Button-1>',query)

img4 = ImageTk.PhotoImage(Image.open("icons/b5.png"))
graphButton = Button(main, text="", image = img4)
graphButton.place(x=400,y=620)
graphButton.config(font=font1)
graphButton.bind('<Button-1>',graph)

img5 = ImageTk.PhotoImage(Image.open("icons/b6.png"))
quitButton = Button(main, text="", image = img5)
quitButton.place(x=750,y=620)
quitButton.config(font=font1)
quitButton.bind('<Button-1>',quit)



main.config(bg='LightSkyBlue')
main.mainloop()
