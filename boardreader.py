import tkinter as tk
import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
import serial
from random import randint

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
        self.entry.delete(0, len(self.entry.get()) - 1)
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

        self.brightness = IntFrame(master, 0, 255, "brightness")

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
        self.button1 = tk.Button(self.master, text="UPDATE IMAGE AND GET MATRIX", command=self.updateImage)
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
    
    def increaseBrightness(self, img, value=0):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img

    def updateImage(self):
        #TAKING MULTIPLE PHOTOS
        cap = cv2.VideoCapture(1)
        res = np.array([])
        for a in range(0,50):
            ret, fimg = cap.read()
            fimg = self.increaseBrightness(fimg, self.brightness.counter.get())
            hsv = cv2.cvtColor(fimg, cv2.COLOR_BGR2HSV)
            lower_red = np.array([self.lower_hue.counter.get(), self.lower_sat.counter.get(), self.lower_val.counter.get()])
            upper_red = np.array([self.upper_hue.counter.get(), self.upper_sat.counter.get(), self.upper_val.counter.get()])
            mask = cv2.inRange(hsv, lower_red, upper_red)
            fres = cv2.bitwise_and(fimg,fimg, mask=mask)

            if res.size == 0:
                res = fres
                cv2.imshow("orginal", fimg)
            else:
                res = cv2.max(res, fres)
        cap.release()
        #DO IMAGE PROCESSING
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

        self.board_matrix = BoardMatrix.getBoardMatrix(points)
        print(self.board_matrix)
        cv2.imshow("points", bw)

class CheckersAI():

    def __init__(self):
        self.resetQueens()
        self.resetTaken()
        self.port = serial.Serial("COM9", baudrate=460800)
    mySide = [1, 2]
    enSide = [3, 4]

    taken = []
    queens = []

    matrix = []

    def resetTaken(self):
        self.taken = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    
    def getNewTakenPos(self):
        for r in range(8):
            for c in range(2):
                if self.taken[r][c] == 0:
                    self.taken[r][c] = 1
                    return [r, c+8]
    
    def resetQueens(self):
        self.queens = [1,1,1,1,1,1,1,1]

    def getNewQueenPos(self):
        for c in range(8):
            if self.queens[c] == 1:
                self.queens[c] = 0
                return [9, c]

    def optimise(self, final_moves):
        #best moves are the ones in which we stay next to our pawns and 1 space away in front of enemy pawns
        scored_moves = []
        for k in range(0,len(final_moves)):
            this_move = final_moves[k]
            new_pos = final_moves[k][1]
            new_board = list(self.matrix)
            new_board[this_move[1][0]][this_move[1][1]] = new_board[this_move[0][0]][this_move[0][1]]
            new_board[this_move[0][0]][this_move[0][1]] = 0

            score = 0
            if new_pos[0] == 1:
                score = score - 4
            if new_pos[1] > 0 and new_pos[1] < 7 and new_pos[0] > 0:
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        if a == 0 and b == 0:
                            continue
                        else:
                            if new_board[new_pos[0] + a][new_pos[1] + b] in self.mySide:
                                score = score + 2
                            if new_board[new_pos[0] + a][new_pos[1] + b] in self.enSide:
                                score = score - 6
            elif new_pos[1] > 1 and new_pos[1] < 6 and new_pos[0] < 6:
                if new_board[new_pos[0] + 2][new_pos[1] - 2] in self.enSide:
                    score = score + 1
                if new_board[new_pos[0] + 2][new_pos[1] + 2] in self.enSide:
                    score = score + 1
            elif new_pos[1] == 0 and new_pos[0] < 7:
                if new_board[new_pos[0] + 1][new_pos[1] + 1] in self.enSide:
                    score = score + 3
            elif new_pos[1] == 7 and new_pos[0] < 7:
                if new_board[new_pos[0] + 1][new_pos[1] - 1] in self.enSide:
                    score = score + 3
            scored_moves.append([score, this_move])
        def sortByFirstElem(elem):
            return elem[0]
        scored_moves.sort(key = sortByFirstElem, reverse = True)
        final_moves = []
        for m in range(0, len(scored_moves)):
            final_moves.append(scored_moves[m][1])

        return final_moves

    def getMatrix(self, matrix):
        self.matrix = matrix


    def getMoves(self):
        final_strikes = []
        final_totake = []
        final_queen = []
        final_moves = []
        final_multi = []
        for x in range(8):
            for y in range(8):
                mymoves = []
                mystrikes = []
                myqueen = []
                totake = []
                if self.matrix[y][x] == self.mySide[0]:
                    #first we check if we can make strikes
                    self.getStrikes([y,x], self.matrix, mystrikes, totake)
                    self.getQueen([y,x], self.matrix, myqueen)
                    self.getMove([y,x], self.matrix, mymoves)
                    for s in mystrikes:
                        final_strikes.append([[y,x],[s[0],s[1]]])
                    for t in totake:
                        final_totake.append([[y,x],[t[0],t[1]]])
                    for q in myqueen:
                        final_queen.append([[y,x],[q[0],q[1]]])
                    for m in mymoves:
                        final_moves.append([[y,x],[m[0],m[1]]])
                if self.matrix[y][x] == self.mySide[1]:
                    self.getQMove([y,x], self.matrix, mymoves, mystrikes, totake)
                    for s in mystrikes:
                        final_strikes.append([[y,x],[s[0],s[1]]])
                    for t in totake:
                        final_totake.append([[y,x],[t[0],t[1]]])
                    for q in myqueen:
                        final_queen.append([[y,x],[q[0],q[1]]])
                    for m in mymoves:
                        final_moves.append([[y,x],[m[0],m[1]]])

        for r in self.matrix:
            print(r)
        #przed robieniem wylosować bicie i dopiero dla niego robić wielokrotne
        if len(final_strikes) > 0:
            final_multi = self.getFinalMultipleStrikes(final_strikes)
            if len(final_multi) > 0:
                ind = randint(0, len(final_multi) - 1)
                my_multi = final_multi[ind]
                string = ""
                for m in range(1, len(my_multi)):
                    this_take = [int(my_multi[m-1][0] + (my_multi[m][0] - my_multi[m-1][0])/2), int(my_multi[m-1][1] + (my_multi[m][1] - my_multi[m-1][1])/2)]
                    to_dump = self.getNewTakenPos()
                    string = string + "m{}{}gm{}{}r".format(this_take[0], this_take[1], to_dump[0], to_dump[1])
                if my_multi[len(my_multi) - 1][0] == 7:
                    quen = self.getNewQueenPos()
                    rem = self.getNewTakenPos()
                    string = "m00m{}{}gm{}{}r".format(my_multi[0][0], my_multi[0][1], rem[0], rem[1]) + string + "m{}{}gm{}{}rd".format(quen[0],quen[1], my_multi[len(my_multi) - 1][0], my_multi[len(my_multi) - 1][1])
                else:
                    string = "m00m{}{}gm{}{}r".format(my_multi[0][0], my_multi[0][1], my_multi[len(my_multi) - 1][0], my_multi[len(my_multi) - 1][1]) + string + "d"
                self.port.write(string.encode())
                print(string)
            else:
                ind = randint(0, len(final_strikes) - 1)
                #musimy się poruszyć na miejsce pionka bijącego, chywcić go, na miejsce po zbiciu, i zabrać pionek zbity
                strike = final_strikes[ind]
                take = [int(strike[0][0] + (strike[1][0]-strike[0][0])/2), int(strike[0][1] + (strike[1][1]-strike[0][1])/2)]

                take_pos = self.getNewTakenPos()
                if strike[1][0] == 7:
                    take_pos1 = self.getNewTakenPos()
                    take_pos2 = self.getNewTakenPos()
                    queen_pos = self.getNewTakenPos()
                    string = "m00m{}{}gm{}{}rm{}{}gm{}{}rm{}{}gm{}{}rd".format(strike[0][0],strike[0][1],take_pos1[0],take_pos1[1],queen_pos[0], queen_pos[1],strike[1][0],strike[1][1],take[0],take[1],take_pos2[0],take[1])
                    self.port.write(string.encode())
                    print(string)
                else:
                    string = "m00m{}{}gm{}{}rm{}{}gm{}{}rd".format(strike[0][0], strike[0][1], strike[1][0], strike[1][1], take[0], take[1], take_pos[0], take_pos[1])
                    self.port.write(string.encode())
                    print(string)
        elif len(final_queen) > 0:
            ind = randint(0, len(final_queen) - 1)
            move = final_queen[ind]
            queen_pos = self.getNewQueenPos()
            take_pos = self.getNewTakenPos()
            string = "m00m{}{}gm{}{}rm{}{}gm{}{}rd".format(move[0][0],move[0][1],take_pos[0],take_pos[1],queen_pos[0],queen_pos[1], move[1][0], move[1][1])
            self.port.write(string.encode())
            print(string)
        else:
            final_moves = self.optimise(final_moves)
            move = final_moves[0]
            string = "m00m{}{}gm{}{}rd".format(move[0][0], move[0][1], move[1][0], move[1][1])
            self.port.write(string.encode())
            print(string)
    
    multiple_strikes = []
    def multipleStrikes(self, board, strike, totake):
        #strike [nasz pionek],[gdziebije]
        #totake [co bijemy]

        def getNewBoard(board, strike):
            new_board = list(board)
            new_board[strike[1][0]][strike[1][1]] = board[strike[0][0]][strike[0][1]]
            new_board[strike[0][0]][strike[0][1]] = 0
            new_board[totake[0]][totake[1]] = 0
            return new_board
        
        new_pos = [strike[1][0], strike[1][1]]
        new_board = getNewBoard(board, strike)

        if new_pos[0] == 6 or new_pos[0] == 7:
            return 

        if new_pos[1] < 2 or new_pos[1] > 5:
            if new_pos[1] < 2 and new_board[new_pos[0] + 1][new_pos[1] + 1] in self.enSide and new_board[new_pos[0] + 2][new_pos[1] + 2] == 0:
                this_strike = [[new_pos[0],new_pos[1]],[new_pos[0] + 2,new_pos[1] + 2]]
                this_take = [new_pos[0] + 1,new_pos[1] + 1]
                self.multiple_strikes.append(this_strike)
                self.multipleStrikes(new_board, this_strike, this_take)

            if new_pos[1] > 5 and new_board[new_pos[0] + 1][new_pos[1] - 1] in self.enSide and new_board[new_pos[0] + 2][new_pos[1] - 2] == 0:
                this_strike = [[new_pos[0],new_pos[1]],[new_pos[0] + 2,new_pos[1] - 2]]
                this_take = [new_pos[0] + 1,new_pos[1] - 1]
                self.multiple_strikes.append(this_strike)
                self.multipleStrikes(new_board, this_strike, this_take)

        else:
            if new_board[new_pos[0] + 1][new_pos[1] + 1] in self.enSide and new_board[new_pos[0] + 2][new_pos[1] + 2] == 0:
                this_strike = [[new_pos[0],new_pos[1]],[new_pos[0] + 2,new_pos[1] + 2]]
                this_take = [new_pos[0] + 1,new_pos[1] + 1]
                self.multiple_strikes.append(this_strike)
                self.multipleStrikes(new_board, this_strike, this_take)

            if new_board[new_pos[0] + 1][new_pos[1] - 1] in self.enSide and new_board[new_pos[0] + 2][new_pos[1] - 2] == 0:
                this_strike = [[new_pos[0],new_pos[1]],[new_pos[0] + 2,new_pos[1] - 2]]
                this_take = [new_pos[0] + 1,new_pos[1] - 1]
                self.multiple_strikes.append(this_strike)
                self.multipleStrikes(new_board, this_strike, this_take)

    def makeChains(self):
        def sortByVertical(elem):
            return elem[0][0]
        self.multiple_strikes.sort(key = sortByVertical)
        a = 0
        while True:
            if a >= len(self.multiple_strikes):
                break
            this_end = self.multiple_strikes[a]
            for k in range(a + 1, len(self.multiple_strikes)):
                r = self.multiple_strikes[k]
                if this_end[len(this_end) - 1] == r[0]:
                    new_entry = []
                    for p in this_end:
                        new_entry.append(p)
                    new_entry.append(r[1])
                    self.multiple_strikes.append(new_entry)
            
            a = a + 1
            if a == len(self.multiple_strikes):
                break
        
    
    def getFinalMultipleStrikes(self, final_strikes):
        final_multi = []
        for s in final_strikes:
            to_take = [int(s[0][0] + (s[1][0]-s[0][0])/2), int(s[0][1] + (s[1][1]-s[0][1])/2)]
            self.multipleStrikes(self.matrix, s, to_take)
            if len(self.multiple_strikes) > 0:
                self.makeChains()
                self.multiple_strikes.sort(key=len, reverse=True)
                new_entry = [[s[0][0],s[0][1]]]
                for m in self.multiple_strikes[0]:
                    new_entry.append(m)
                final_multi.append(new_entry)
                self.multiple_strikes = []
        return final_multi

            



            
    #use only for pawns
    def getStrikes(self, pawn_pos, board, mystrikes, totake):
        enSide = self.enSide
        out = False # zwraca true jesli znalazl jakies bicia
        #pawn_pos[0] - row
        #pawn_pos[1] - column
        
        #jezeli pionek jest zbyt blisko dolnej krawedzi planszy nie ma bicia
        if pawn_pos[0] == 6:
            return out

        if pawn_pos[1] == 0 or pawn_pos[1] == 1 or pawn_pos[1] == 6 or pawn_pos[1] == 7:
            #sprawdzamy czy pionek jest przy krawedzi planszy wtedy sprawdzamy tylko w jedne strone
            if (pawn_pos[1] == 0 or pawn_pos[1] == 1) and board[pawn_pos[0] + 1][pawn_pos[1] + 1] in enSide and board[pawn_pos[0] + 2][pawn_pos[1] + 2] == 0:
                mystrikes.append([pawn_pos[0] + 2, pawn_pos[1] + 2])
                totake.append([pawn_pos[0] + 1, pawn_pos[1] + 1])
                out = True
            if (pawn_pos[1] == 7 or pawn_pos[1] == 6) and board[pawn_pos[0] + 1][pawn_pos[1] - 1] in enSide and board[pawn_pos[0] + 2][pawn_pos[1] - 2] == 0:
                mystrikes.append([pawn_pos[0] + 2, pawn_pos[1] - 2])
                totake.append([pawn_pos[0] + 1, pawn_pos[1] - 1])
                out = True
            
        else:
            #sprawdzamy zwykle możliwosci bicia zwyklych pionkow
            if board[pawn_pos[0] + 1][pawn_pos[1] - 1] in enSide and board[pawn_pos[0] + 2][pawn_pos[1] - 2] == 0:
                mystrikes.append([pawn_pos[0] + 2, pawn_pos[1] - 2])
                totake.append([pawn_pos[0] + 1, pawn_pos[1] - 1])
                out = True

            if board[pawn_pos[0] + 1][pawn_pos[1] + 1] in enSide and board[pawn_pos[0] + 2][pawn_pos[1] + 2] == 0:
                mystrikes.append([pawn_pos[0] + 2, pawn_pos[1] + 2])
                totake.append([pawn_pos[0] + 1, pawn_pos[1] + 1])
                out = True

        return out

    def getQueen(self, pawn_pos, board, myqueen):
        out = False
        if pawn_pos[0] == 6:
            if pawn_pos[1] == 7 and board[7][6] == 0:
                myqueen.append([7,6])
                out = True
            if board[7][pawn_pos[1] + 1] == 0:
                myqueen.append([7, pawn_pos[1] + 1])
                out = True
            if board[7][pawn_pos[1] - 1] == 0:
                out = True
                myqueen.append([7, pawn_pos[1] - 1])
        else:
            return False
        return out

    def getMove(self, pawn_pos, board, mymoves):
        if pawn_pos[1] == 0 or pawn_pos[1] == 7:
            if pawn_pos[1] == 0 and board[pawn_pos[0] + 1][1] == 0:
                mymoves.append([pawn_pos[0] + 1, 1])
            if pawn_pos[1] == 7 and board[pawn_pos[0] + 1][6] == 0:
                mymoves.append([pawn_pos[0] + 1, 6])
        else:
            if board[pawn_pos[0] + 1][pawn_pos[1] + 1] == 0:
                mymoves.append([pawn_pos[0] + 1, pawn_pos[1] + 1])
            if board[pawn_pos[0] + 1][pawn_pos[1] - 1] == 0:
                mymoves.append([pawn_pos[0] + 1, pawn_pos[1] - 1])

    def getQMove(self, queen_pos, board, mymoves, strikes, totake):
        #bedziemy zwiekszac promien o 1 i sprawdzac wolne pola przy czym sprawdzamy czy dane pole jest w planszy
        for r in range(1, 7):
            this_pos = [queen_pos[0] + r, queen_pos[1] + r]
            if this_pos[0] < 0 or this_pos[0] > 7 or this_pos[1] < 0 or this_pos[1] > 7:
                continue
            #sprawdzamy bicie
            if this_pos[0] < 7 and this_pos[1] < 7:
                if board[this_pos[0]][this_pos[1]] in self.enSide and board[this_pos[0] + 1][this_pos[1] + 1] == 0:
                    strikes.append([this_pos[0] + 1,this_pos[1] + 1])
                    totake.append([this_pos[0],this_pos[1]])
                    break
            if board[this_pos[0]][this_pos[1]] == 0:
                mymoves.append(this_pos)
            else:
                break
        for r in range(1, 7):
            this_pos = [queen_pos[0] - r, queen_pos[1] + r]
            if this_pos[0] < 0 or this_pos[0] > 7 or this_pos[1] < 0 or this_pos[1] > 7:
                continue
            if this_pos[0] > 0 and this_pos[1] < 7:
                if board[this_pos[0]][this_pos[1]] in self.enSide and board[this_pos[0] - 1][this_pos[1] + 1] == 0:
                    strikes.append([this_pos[0] - 1,this_pos[1] + 1])
                    totake.append([this_pos[0],this_pos[1]])
                    break
            if board[this_pos[0]][this_pos[1]] == 0:
                mymoves.append(this_pos)
            else:
                break
        for r in range(1, 7):
            this_pos = [queen_pos[0] + r, queen_pos[1] - r]
            if this_pos[0] < 0 or this_pos[0] > 7 or this_pos[1] < 0 or this_pos[1] > 7:
                continue
            if this_pos[0] < 7 and this_pos[1] > 0:
                if board[this_pos[0]][this_pos[1]] in self.enSide and board[this_pos[0] + 1][this_pos[1] - 1] == 0:
                    strikes.append([this_pos[0] + 1,this_pos[1] - 1])
                    totake.append([this_pos[0],this_pos[1]])
                    break
            if board[this_pos[0]][this_pos[1]] == 0:
                mymoves.append(this_pos)
            else:
                break
        for r in range(1, 7):
            this_pos = [queen_pos[0] - r, queen_pos[1] - r]
            if this_pos[0] < 0 or this_pos[0] > 7 or this_pos[1] < 0 or this_pos[1] > 7:
                continue
            if this_pos[0] > 0 and this_pos[1] > 0:
                if board[this_pos[0]][this_pos[1]] in self.enSide and board[this_pos[0] - 1][this_pos[1] - 1] == 0:
                    strikes.append([this_pos[0] + 1,this_pos[1] + 1])
                    totake.append([this_pos[0],this_pos[1]])
                    break
            if board[this_pos[0]][this_pos[1]] == 0:
                mymoves.append(this_pos)
            else:
                break


#initialize
#   declare side                            X
#get move                                   X
#reset memory fo beaten and queen stack     X
#take pawn                                  X
#   check if in bounds                      X
#   check if there's pawn in fron           X
#   check if theres free space after pawn   X
#   check for multiple strikes
#get queen                                  X
#take multiple
#check if at end can take queen             X
#attack rule                                X
#move queen                                 X
#attack queen                               X
#damka po biciu na pole 7                   X


class PawnReader(tk.Frame):
    def __init__(self, master = None, default="70 100 80 255 0 255 7 7 2 1 24 14"):
        tk.Frame.__init__(self, master)
        self.master = master
        # self.matrix_load = LoadFrame(master, "Load Matrix", "[[[112, 72], [164, 73], [213, 75], [263, 76], [311, 78], [362, 78], [409, 79], [456, 80], [505, 81]], [[104, 101], [158, 103], [210, 104], [262, 105], [313, 107], [365, 108], [413, 108], [465, 108], [514, 109]], [[93, 132], [150, 134], [206, 135], [261, 136], [314, 139], [366, 139], [419, 140], [472, 139], [527, 141]], [[82, 171], [143, 170], [202, 170], [259, 171], [314, 172], [373, 174], [426, 174], [484, 174], [538, 175]], [[70, 208], [135, 208], [196, 210], [255, 209], [315, 211], [376, 213], [436, 214], [494, 214], [553, 215]], [[57, 250], [123, 251], [191, 251], [256, 254], [317, 253], [381, 254], [442, 255], [508, 255], [569, 255]], [[42, 300], [114, 302], [183, 301], [252, 301], [319, 302], [386, 302], [454, 303], [520, 304], [586, 306]], [[24, 356], [102, 357], [175, 356], [248, 358], [320, 357], [391, 359], [463, 357], [536, 360], [605, 356]], [[8, 421], [88, 421], [167, 419], [245, 420], [324, 424], [401, 423], [479, 423], [553, 425], [627, 421]]]")
        # self.matrix_load.setCommand(self.loadMatrix)
        self.settings_load = LoadFrame(master, "Load Settings", default=default)
        self.settings_load.setCommand(self.loadSettings)

        self.brightness = IntFrame(master, 0, 255, "brightness")

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


    def initSaveButtons(self):
        self.button1 = tk.Button(self.master, text="UPDATE IMAGE", command=self.updateImage)
        self.button1.pack()
        self.button2 = tk.Button(self.master, text="SAVE", command=self.saveSettings)
        self.button2.pack()

    #array interpreter
    # def loadMatrix(self):
    #     string = self.matrix_load.string.get()
    #     chars = ['[', ']', ',']
    #     for c in chars:
    #         string = string.replace(c, '')
    #     string = string.split()
    #     matrix = []
        
    #     if(len(string) != 0):
    #         for r in range(0,9):
    #             row = []
    #             for s in range(0,9):
    #                 row.append([ int(string[(r*18)+(s*2)]), int(string[(r*18)+(s*2)+1])])
    #             matrix.append(row)
    #         self.board_matrix = matrix

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
        print(string)

    def getPawns(self):
        #TAKING MULTIPLE PHOTOS
        cap = cv2.VideoCapture(1)
        ret, fimg = cap.read()
        fimg = self.increaseBrightness(fimg, self.brightness.counter.get())
        #cv2.imshow("orginal", fimg)
        cap.release()
        #IMG PROCESSING
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
        #cv2.imshow("pawn points", bw)
        self.pawns = points

    def increaseBrightness(self, img, value=0):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img


    def updateImage(self):
        #TAKING MULTIPLE PHOTOS
        cap = cv2.VideoCapture(1)
        time.sleep(2)
        ret, fimg = cap.read()
        fimg = self.increaseBrightness(fimg, self.brightness.counter.get())
        cv2.imshow("orginal", fimg)
        cap.release()
        hsv = cv2.cvtColor(fimg, cv2.COLOR_BGR2HSV)
        lower_color = np.array([self.lower_hue.counter.get(), self.lower_sat.counter.get(), self.lower_val.counter.get()])
        upper_color = np.array([self.upper_hue.counter.get(), self.upper_sat.counter.get(), self.upper_val.counter.get()])
        mask = cv2.inRange(hsv, lower_color, upper_color)
        res = cv2.bitwise_and(fimg,fimg, mask=mask)
        cv2.imshow("masked", res)
        res = cv2.GaussianBlur(res, (self.blur.integer.get(),self.blur.integer.get()), 0)
        m_kernel = np.ones((self.kernel.integer.get(),self.kernel.integer.get()), np.uint8) 

        res = cv2.erode(res, m_kernel, iterations=self.erosions.counter.get()) 
        res = cv2.dilate(res, m_kernel, iterations=self.dialations.counter.get()) 

        cv2.imshow('blured and eroded', res)
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
        cv2.imshow("", bw)
        self.pawns = points
        print(self.pawns)

class BoardReader(tk.Frame):
    def __init__(self, master = None):
            tk.Frame.__init__(self, master)
            self.master = master
            self.initButtons()

    def initButtons(self):
        start_setup = tk.Button(master=self.master, text="SETUP PARAMETERS", command=self.setupBoardReader)
        start_setup.pack()

        get_board = tk.Button(master=self.master, text="GET BOARD", command=self.GetPawnPositions)
        get_board.pack()

        self.text = tk.StringVar()
        
        self.entry = tk.Entry(master=self.master, textvariable = self.text, width=20)
        self.entry.pack()


        self.send = tk.Button(self.master, text = "SEND", command=self.sendToSerial)
        self.send.pack()

    def sendToSerial(self):
        self.checkers_ai.port.write(self.entry.get().encode())
        
    def GetPawnPositions(self):
        self.green_read.getPawns()
        self.blue_read.getPawns()
        self.yellow_read.getPawns()
        matrix = self.matrix_proc.board_matrix
        points1 = self.green_read.pawns
        points2 = self.blue_read.pawns
        points3 = self.yellow_read.pawns

        print("Zielone pionki: {}".format(self.green_read.pawns))
        print("Niebieskie pionki: {}".format(self.blue_read.pawns))
        print("Damki: {}".format(self.yellow_read.pawns))

        out = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        rows = "ABCDEFGH"
        def sortBySecond(elem):
                    return elem[1]
        def GetSide(out, points, value, queens = False):
            for p in points:
                for r in range(0,8):
                    minY = min(matrix[r], key=sortBySecond)[1]
                    maxY = max(matrix[r+1], key=sortBySecond)[1]
                    if p[1] >= minY and p[1] <= maxY:
                        for c in range(0,8):
                            x1 = [matrix[r][c][0], matrix[r+1][c][0]]
                            x2 = [matrix[r][c+1][0], matrix[r+1][c+1][0]]

                            if p[0] >= x1[0] and p[0] >= x1[1] and p[0] <= x2[0] and p[0] <= x2[1]:
                                if queens:
                                    out[r][c] = out[r][c] + value
                                else:
                                    out[r][c] = value
        GetSide(out, points1, 1)
        GetSide(out, points2, 3)
        GetSide(out, points3, 1, True)
        self.board = out
        self.checkers_ai.getMatrix(self.board)
        self.checkers_ai.getMoves()
        for r in self.board:
            print(r)

    def setupBoardReader(self):
        matrix_window = tk.Toplevel(self.master)
        matrix_window.title("Plansza")
        self.matrix_proc = MatrixProcessing(master=matrix_window, default="0 4 100 255 100 255 3 3 1 1 60")

        green_window = tk.Toplevel(self.master)
        green_window.title("Zeilone")
        self.green_read = PawnReader(master=green_window, default="40 90 80 255 0 255 7 7 1 2 24 ")

        blue_window = tk.Toplevel(self.master)
        blue_window.title("Niebieskie")
        self.blue_read = PawnReader(master=blue_window, default="100 120 80 255 0 255 7 7 1 2 24 ")

        yellow_window = tk.Toplevel(self.master)
        yellow_window.title("Zolte")
        self.yellow_read = PawnReader(master=yellow_window, default="20 44 150 255 150 255 3 3 1 2 40 ")

        self.checkers_ai = CheckersAI()






root = tk.Tk()

board_reader = BoardReader(root)
root.mainloop()

#dodać do PawnReaderów UpdateImage boolean wskazujący czy pokazywać zrzut ekranu
#dodać obsługę obrazu na żywo: w BoardReader funkcja TakePhoto i w PawnReaderze funkcja UpdateImage(img) //if(img = None) leć normalnie else z zrzutu