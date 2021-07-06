import tkinter as tk
import numpy as np
import cv2
import matplotlib.pyplot as plt

class IntFrame(tk.Frame):

    def __init__(self, master = None, from_=0, to=100, name="default"):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_int(from_, to, name)

    
    def init_int(self, from_, to, name):
        self.pack()

        self.counter = tk.IntVar(0)

        self.left_label = tk.Label(self, text = name)
        self.left_label.pack(side = "left")

        self.scale = tk.Scale(self, from_=from_, to=to, variable=self.counter, orient='horizontal', length=300)
        self.scale.pack(side="right")

    def loadValue(self, value):
        self.counter.set(value)
        self.scale.set(value)

class EntryFrame(tk.Frame):

    def __init__(self, master = None, name='default'):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_entry(name)

    
    def init_entry(self, name):
        self.pack()

        self.text = tk.StringVar()
        self.integer = tk.IntVar()
        self.integer.set(1)
        self.left_label = tk.Label(self, text = name)
        self.left_label.pack(side = "left")
        
        self.button = tk.Button(self, text = "Set", command=self.submit)
        self.button.pack(side="right")

        self.entry = tk.Entry(self, textvariable = self.text, width=5)
        self.entry.pack()

    
    def submit(self):
        self.integer.set(self.text.get())
        
    def loadValue(self, value):
        self.integer.set(value)
        self.entry.delete(0, last='end')
        self.entry.insert(0, str(value))

class BoardMatrix():

    @staticmethod
    def getBoardMatrix(points):
        def sortByFirst(elem):
            return elem[0]
        def sortBySecond(elem):
            return elem[1]

        points.sort(key = sortBySecond)
        matrix = []
        for r in range(0, 9):
            from_ = r*9
            to = 9+r*9
            matrix.append(points[from_:to])
            matrix[r].sort(key=sortByFirst)
        
        return matrix



root = tk.Tk()


load_frame = tk.Frame(root)
load_frame.pack()
load_string = tk.StringVar()
load_entry = tk.Entry(load_frame, textvariable=load_string)
load_entry.pack(side="left")
load_entry.insert(0, "0 4 100 255 120 255 3 3 1 1 60")
def loadSettings():
    values = load_string.get().split()
    lower_hue.loadValue(values[0])
    upper_hue.loadValue(values[1])
    lower_sat.loadValue(values[2])
    upper_sat.loadValue(values[3])
    lower_val.loadValue(values[4])
    upper_val.loadValue(values[5])
    blur.loadValue(values[6])
    kernel.loadValue(values[7])
    erosions.loadValue(values[8])
    dialations.loadValue(values[9])
    tresh.loadValue(values[10])
load = tk.Button(load_frame, text="LOAD", command=loadSettings)
load.pack(side="right")

lower_hue = IntFrame(root, 0, 255, "lower hue")
upper_hue = IntFrame(root, 0, 255, "upper hue")
lower_sat = IntFrame(root, 0, 255, "lower sat")
upper_sat = IntFrame(root, 0, 255, "upper sat")
lower_val = IntFrame(root, 0, 255, "lower val")
upper_val = IntFrame(root, 0, 255, "upper val")

blur = EntryFrame(root, "Blur")
kernel = EntryFrame(root, "Kernel")

erosions = IntFrame(root, 0, 10, "Erosions")
dialations = IntFrame(root, 0, 10, "Dialations")
tresh = IntFrame(root, 0, 255, "Treshold")

def updateImage():
    res = np.array([])
    for a in range(14,26):
        fimg = cv2.imread(r"..\mech_python\zdjecia\plansza{}.jpg".format(a))
        hsv = cv2.cvtColor(fimg, cv2.COLOR_BGR2HSV)
        lower_red = np.array([lower_hue.counter.get(), lower_sat.counter.get(), lower_val.counter.get()])
        upper_red = np.array([upper_hue.counter.get(), upper_sat.counter.get(), upper_val.counter.get()])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        fres = cv2.bitwise_and(fimg,fimg, mask=mask)

        if res.size == 0:
            res = fres
        else:
            res = cv2.add(res, fres)


    res = cv2.GaussianBlur(res, (blur.integer.get(),blur.integer.get()), 0)
    m_kernel = np.ones((kernel.integer.get(),kernel.integer.get()), np.uint8) 

    res = cv2.erode(res, m_kernel, iterations=erosions.counter.get()) 
    res = cv2.dilate(res, m_kernel, iterations=dialations.counter.get()) 

    cv2.imshow('image', res)
    h, s, v = cv2.split(res)
    bw= cv2.threshold(v, tresh.counter.get(), 255, cv2.THRESH_BINARY)[1]

    points = []
    contours, hierarchy = cv2.findContours(bw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(bw, (cX, cY), 3, (80, 70, 40), -1)
        points.append([cX, cY])

    matrix = BoardMatrix.getBoardMatrix(points)
    print(matrix)
    cv2.imshow("points", bw)


def saveSettings():
    string = ""
    string += str(lower_hue.counter.get())
    string += " "
    string += str(upper_hue.counter.get())
    string += " "
    string += str(lower_sat.counter.get())
    string += " "
    string += str(upper_sat.counter.get())
    string += " "
    string += str(lower_val.counter.get())
    string += " "
    string += str(upper_val.counter.get())
    string += " "
    string += str(blur.integer.get())
    string += " "
    string += str(kernel.integer.get())
    string += " "
    string += str(erosions.counter.get())
    string += " "
    string += str(dialations.counter.get())
    string += " "
    string += str(tresh.counter.get())
    print(string)

button1 = tk.Button(root, text="UPDATE IMAGE", command=updateImage)
button1.pack()
button2 = tk.Button(root, text="SAVE", command=saveSettings)
button2.pack()

root.mainloop()