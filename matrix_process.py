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

class LoadFrame(tk.Frame):

    def __init__(self, master = None, name="default", default=""):
        tk.Frame.__init__(self, master)
        self.master = master
        self.string = tk.StringVar()
        self.string.set(default)
        self.init_load(self.master, name, default)
    
    def init_load(self, command, name, default ):
        self.pack()

        self.label = tk.Label(self, text = name)
        self.label.pack(side = "left")

        self.button = tk.Button(self, text="LOAD")
        self.button.pack(side="right")

        self.entry = tk.Entry(self, textvariable=self.string)
        self.entry.pack()
        self.entry.insert(0, default)

    def setCommand(self, command):
        self.button.config(command = command)

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

class MatrixProcessing(tk.Frame):

    def __init__(self, master = None, default = ""):
        tk.Frame.__init__(self, master)
        self.master = master
        self.initLoadButtons(default)

        self.lower_hue = IntFrame(master, 0, 255, "lower hue")
        self.upper_hue = IntFrame(master, 0, 255, "upper hue")
        self.lower_sat = IntFrame(master, 0, 255, "lower sat")
        self.upper_sat = IntFrame(master, 0, 255, "upper sat")
        self.lower_val = IntFrame(master, 0, 255, "lower val")
        self.upper_val = IntFrame(master, 0, 255, "upper val")

        self.blur = EntryFrame(master, "Blur")
        self.kernel = EntryFrame(master, "Kernel")

        self.erosions = IntFrame(master, 0, 10, "Erosions")
        self.dialations = IntFrame(master, 0, 10, "Dialations")
        self.tresh = IntFrame(master, 0, 255, "Treshold")

        self.initSaveButtons()
        self.pack(side = tk.LEFT)

    #Tworzymy przyciski
    def initLoadButtons(self, default):

        self.load_frame = tk.Frame(self.master)
        self.load_frame.pack()

        self.load_string = tk.StringVar()

        self.load_entry = tk.Entry(self.load_frame, textvariable=self.load_string)
        self.load_entry.pack(side="left")
        self.load_entry.insert(0, default)

        self.load = tk.Button(self.load_frame, text="LOAD", command=self.loadSettings)
        self.load.pack()
                

    def initSaveButtons(self):
        self.button1 = tk.Button(self.master, text="UPDATE IMAGE", command=self.updateImage)
        self.button1.pack()
        self.button2 = tk.Button(self.master, text="SAVE", command=self.saveSettings)
        self.button2.pack()


    def loadSettings(self):
        values = self.load_string.get().split()
        self.lower_hue.loadValue(values[0])
        self.upper_hue.loadValue(values[1])
        self.lower_sat.loadValue(values[2])
        self.upper_sat.loadValue(values[3])
        self.lower_val.loadValue(values[4])
        self.upper_val.loadValue(values[5])
        self.blur.loadValue(values[6])
        self.kernel.loadValue(values[7])
        self.erosions.loadValue(values[8])
        self.dialations.loadValue(values[9])
        self.tresh.loadValue(values[10])

    def saveSettings(self):
        string = ""
        string += str(self.lower_hue.counter.get())
        string += " "
        string += str(self.upper_hue.counter.get())
        string += " "
        string += str(self.lower_sat.counter.get())
        string += " "
        string += str(self.upper_sat.counter.get())
        string += " "
        string += str(self.lower_val.counter.get())
        string += " "
        string += str(self.upper_val.counter.get())
        string += " "
        string += str(self.blur.integer.get())
        string += " "
        string += str(self.kernel.integer.get())
        string += " "
        string += str(self.erosions.counter.get())
        string += " "
        string += str(self.dialations.counter.get())
        string += " "
        string += str(self.tresh.counter.get())
        print(string)

    def updateImage(self):
        res = np.array([])
        for a in range(14,26):
            fimg = cv2.imread(r"..\mech_python\zdjecia\plansza{}.jpg".format(a))
            hsv = cv2.cvtColor(fimg, cv2.COLOR_BGR2HSV)
            lower_red = np.array([self.lower_hue.counter.get(), self.lower_sat.counter.get(), self.lower_val.counter.get()])
            upper_red = np.array([self.upper_hue.counter.get(), self.upper_sat.counter.get(), self.upper_val.counter.get()])
            mask = cv2.inRange(hsv, lower_red, upper_red)
            fres = cv2.bitwise_and(fimg,fimg, mask=mask)

            if res.size == 0:
                res = fres
            else:
                res = cv2.add(res, fres)


        res = cv2.GaussianBlur(res, (self.blur.integer.get(),self.blur.integer.get()), 0)
        m_kernel = np.ones((self.kernel.integer.get(),self.kernel.integer.get()), np.uint8) 

        res = cv2.erode(res, m_kernel, iterations=self.erosions.counter.get()) 
        res = cv2.dilate(res, m_kernel, iterations=self.dialations.counter.get()) 

        cv2.imshow('image', res)
        h, s, v = cv2.split(res)
        bw= cv2.threshold(v, self.tresh.counter.get(), 255, cv2.THRESH_BINARY)[1]

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

class PawnReader(tk.Frame):
    def __init__(self, master = None, default="70 100 80 255 0 255 7 7 2 1 24 14"):
        tk.Frame.__init__(self, master)
        self.master = master
        # self.matrix_load = LoadFrame(master, "Load Matrix", "[[[112, 72], [164, 73], [213, 75], [263, 76], [311, 78], [362, 78], [409, 79], [456, 80], [505, 81]], [[104, 101], [158, 103], [210, 104], [262, 105], [313, 107], [365, 108], [413, 108], [465, 108], [514, 109]], [[93, 132], [150, 134], [206, 135], [261, 136], [314, 139], [366, 139], [419, 140], [472, 139], [527, 141]], [[82, 171], [143, 170], [202, 170], [259, 171], [314, 172], [373, 174], [426, 174], [484, 174], [538, 175]], [[70, 208], [135, 208], [196, 210], [255, 209], [315, 211], [376, 213], [436, 214], [494, 214], [553, 215]], [[57, 250], [123, 251], [191, 251], [256, 254], [317, 253], [381, 254], [442, 255], [508, 255], [569, 255]], [[42, 300], [114, 302], [183, 301], [252, 301], [319, 302], [386, 302], [454, 303], [520, 304], [586, 306]], [[24, 356], [102, 357], [175, 356], [248, 358], [320, 357], [391, 359], [463, 357], [536, 360], [605, 356]], [[8, 421], [88, 421], [167, 419], [245, 420], [324, 424], [401, 423], [479, 423], [553, 425], [627, 421]]]")
        # self.matrix_load.setCommand(self.loadMatrix)
        self.settings_load = LoadFrame(master, "Load Settings", default=default)
        self.settings_load.setCommand(self.loadSettings)

        self.lower_hue = IntFrame(master, 0, 255, "lower hue")
        self.upper_hue = IntFrame(master, 0, 255, "upper hue")
        self.lower_sat = IntFrame(master, 0, 255, "lower sat")
        self.upper_sat = IntFrame(master, 0, 255, "upper sat")
        self.lower_val = IntFrame(master, 0, 255, "lower val")
        self.upper_val = IntFrame(master, 0, 255, "upper val")

        self.blur = EntryFrame(master, "Blur")
        self.kernel = EntryFrame(master, "Kernel")

        self.erosions = IntFrame(master, 0, 10, "Erosions")
        self.dialations = IntFrame(master, 0, 10, "Dialations")
        self.tresh = IntFrame(master, 0, 255, "Treshold")
        
        self.photo_number = IntFrame(self.master, 14, 27, "Folder Image")

        self.initSaveButtons()


    def initSaveButtons(self):
        self.button1 = tk.Button(self.master, text="UPDATE IMAGE", command=self.updateImage)
        self.button1.pack()
        self.button2 = tk.Button(self.master, text="SAVE", command=self.saveSettings)
        self.button2.pack()

    #array interpreter
    def loadMatrix(self):
        string = self.matrix_load.string.get()
        chars = ['[', ']', ',']
        for c in chars:
            string = string.replace(c, '')
        string = string.split()
        matrix = []
        
        if(len(string) != 0):
            for r in range(0,9):
                row = []
                for s in range(0,9):
                    row.append([ int(string[(r*18)+(s*2)]), int(string[(r*18)+(s*2)+1])])
                matrix.append(row)
            self.board_matrix = matrix

    def loadSettings(self):
        values = self.settings_load.string.get().split()
        self.lower_hue.loadValue(values[0])
        self.upper_hue.loadValue(values[1])
        self.lower_sat.loadValue(values[2])
        self.upper_sat.loadValue(values[3])
        self.lower_val.loadValue(values[4])
        self.upper_val.loadValue(values[5])
        self.blur.loadValue(values[6])
        self.kernel.loadValue(values[7])
        self.erosions.loadValue(values[8])
        self.dialations.loadValue(values[9])
        self.tresh.loadValue(values[10])
        self.photo_number.loadValue(values[11])
    #array saver
    def saveSettings(self):
        string = ""
        string += str(self.lower_hue.counter.get())
        string += " "
        string += str(self.upper_hue.counter.get())
        string += " "
        string += str(self.lower_sat.counter.get())
        string += " "
        string += str(self.upper_sat.counter.get())
        string += " "
        string += str(self.lower_val.counter.get())
        string += " "
        string += str(self.upper_val.counter.get())
        string += " "
        string += str(self.blur.integer.get())
        string += " "
        string += str(self.kernel.integer.get())
        string += " "
        string += str(self.erosions.counter.get())
        string += " "
        string += str(self.dialations.counter.get())
        string += " "
        string += str(self.tresh.counter.get())
        string += " "
        string += str(self.photo_number.counter.get())
        print(string)

    def updateImage(self):
        index = self.photo_number.counter.get()
        fimg = cv2.imread(r"..\mech_python\zdjecia\plansza{}.jpg".format(index))
        cv2.imshow("orginal", fimg)
        hsv = cv2.cvtColor(fimg, cv2.COLOR_BGR2HSV)
        lower_color = np.array([self.lower_hue.counter.get(), self.lower_sat.counter.get(), self.lower_val.counter.get()])
        upper_color = np.array([self.upper_hue.counter.get(), self.upper_sat.counter.get(), self.upper_val.counter.get()])
        mask = cv2.inRange(hsv, lower_color, upper_color)
        res = cv2.bitwise_and(fimg,fimg, mask=mask)
        #cv2.imshow("masked", res)
        res = cv2.GaussianBlur(res, (self.blur.integer.get(),self.blur.integer.get()), 0)
        m_kernel = np.ones((self.kernel.integer.get(),self.kernel.integer.get()), np.uint8) 

        res = cv2.erode(res, m_kernel, iterations=self.erosions.counter.get()) 
        res = cv2.dilate(res, m_kernel, iterations=self.dialations.counter.get()) 

        #cv2.imshow('blured and eroded', res)
        bw = cv2.threshold(res, self.tresh.counter.get(), 255, cv2.THRESH_BINARY)[1]
        bw = cv2.cvtColor(bw, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("black white", bw)
        points = []
        contours, hierarchy = cv2.findContours(bw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(bw, (cX, cY), 3, (80, 70, 40), -1)
            points.append([cX, cY])
        cv2.imshow("pawn points", bw)
        print(points)


root = tk.Tk()
root.title("Plansza")
matrix_proc = MatrixProcessing(master=root, default="0 4 100 255 120 255 3 3 1 1 60")


green_window = tk.Toplevel(root)
green_window.title("Zeilone")
green_read = PawnReader(master=green_window)

blue_window = tk.Toplevel(root)
blue_window.title("Niebieskie")
blue_read = PawnReader(master=blue_window, default="100 120 80 255 0 255 7 7 2 1 24 27")



root.mainloop()




