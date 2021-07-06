import numpy as np
from random import randint
import serial

class CheckersAI():

    def __init__(self):
        self.resetQueens()
        self.resetTaken()
        #self.port = serial.Serial("COM8", baudrate=460800)
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


    def getMatrix(self, matrix):
        self.matrix = matrix

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
                score = score - 2
            if new_pos[1] > 0 and new_pos[1] < 7 and new_pos[0] > 0:
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        if a == 0 and b == 0:
                            continue
                        else:
                            if new_board[new_pos[0] + a][new_pos[1] + b] in self.mySide:
                                score = score + 2
                            if new_board[new_pos[0] + a][new_pos[1] + b] in self.enSide:
                                score = score - 3
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
                string = "m{}{}gm{}{}r".format(my_multi[0][0], my_multi[0][1], my_multi[len(my_multi) - 1][0], my_multi[len(my_multi) - 1][1]) + string
                #self.port.write(string.encode())
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
                    string = "m{}{}gm{}{}rm{}{}gm{}{}rm{}{}gm{}{}rd".format(strike[0][0],strike[0][1],take_pos1[0],take_pos1[1],queen_pos[0], queen_pos[1],strike[1][0],strike[1][1],take[0],take[1],take_pos2[0],take[1])
                    #self.port.write(string.encode())
                    print(string)
                else:
                    string = "m{}{}gm{}{}rm{}{}gm{}{}rd".format(strike[0][0], strike[0][1], strike[1][0], strike[1][1], take[0], take[1], take_pos[0], take_pos[1])
                    #self.port.write(string.encode())
                    print(string)
        elif len(final_queen) > 0:
            ind = randint(0, len(final_queen) - 1)
            move = final_queen[ind]
            queen_pos = self.getNewQueenPos()
            take_pos = self.getNewTakenPos()
            string = "m{}{}gm{}{}rm{}{}gm{}{}rd".format(move[0][0],move[0][1],take_pos[0],take_pos[1],queen_pos[0],queen_pos[1], move[1][0], move[1][1])
            #self.port.write(string.encode())
            print(string)
        else:
            final_moves = self.optimise(final_moves)
            move = final_moves[0]
            string = "m{}{}gm{}{}rd".format(move[0][0], move[0][1], move[1][0], move[1][1])
            #self.port.write(string.encode())
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

        if new_pos[0] == 6:
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
                mystrikes.append([pawn_pos[0] + 2, pawn_pos[1] + 2])
                totake.append([pawn_pos[0] + 1, pawn_pos[1] + 1])
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

ai = CheckersAI()
ai.getMatrix([[0, 1, 0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0], [3, 0, 3, 0, 3, 0, 3, 0], [0, 3, 0, 3, 0, 3, 0, 3], [3, 0, 3, 0, 3, 0, 3, 0]])
ai.getMoves()

ai.makeChains()
