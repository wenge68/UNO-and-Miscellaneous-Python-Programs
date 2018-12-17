from tkinter import *
import random

class GUIDie(Canvas):
    '''6-sided Die class for GUI'''

    def __init__(self,master,valueList=[1,2,3,4,5,6],colorList=['black']*6):
        '''GUIDie(master,[valueList,colorList]) -> GUIDie
        creates a GUI 6-sided die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        # create a 60x60 white canvas with a 5-pixel grooved border
        Canvas.__init__(self,master,width=60,height=60,bg='white',\
                        bd=5,relief=GROOVE)
        # store the valuelist and colorlist
        self.valueList = valueList
        self.colorList = colorList
        # initialize the top value
        self.top = 1

    def get_top(self):
        '''GUIDie.get_top() -> int
        returns the value on the die'''
        return self.valueList[self.top-1]

    def roll(self):
        '''GUIDie.roll()
        rolls the die'''
        self.top = random.randrange(1,7)
        self.draw()

    def draw(self):
        '''GUIDie.draw()
        draws the pips on the die'''
        # clear old pips first
        self.erase()
        # location of which pips should be drawn
        pipList = [[(1,1)],
                   [(0,0),(2,2)],
                   [(0,0),(1,1),(2,2)],
                   [(0,0),(0,2),(2,0),(2,2)],
                   [(0,0),(0,2),(1,1),(2,0),(2,2)],
                   [(0,0),(0,2),(1,0),(1,2),(2,0),(2,2)]]
        for location in pipList[self.top-1]:
            self.draw_pip(location,self.colorList[self.top-1])

    def draw_pip(self,location,color):
        '''GUIDie.draw_pip(location,color)
        draws a pip at (row,col) given by location, with given color'''
        (centerx,centery) = (17+20*location[1],17+20*location[0])  # center
        self.create_oval(centerx-5,centery-5,centerx+5,centery+5,fill=color)

    def erase(self):
        '''GUIDie.erase()
        erases all the pips'''
        pipList = self.find_all()
        for pip in pipList:
            self.delete(pip)

class ShotPutFrame(Frame):
    '''frame for a game of shot put'''

    def __init__(self,master,name):
        '''ShotPutFrame(master,name) -> ShotPutFrame
        creates a new shot put frame
        name is the name of the player'''
        # set up Frame object
        Frame.__init__(self,master)
        self.grid()
        # label for player's name
        self.nameLabel = Label(self,text=name,font=('Arial',18))
        self.nameLabel.grid(columnspan=2,sticky=W)
        # set up score and rerolls
        self.name = name
        self.attemptNum = 1
        self.score = 0
        self.highScore = 0
        self.gameround = 0
        self.scoreLabel = Label(self,text='Attempt #' + str(self.attemptNum) + ' Score: 0',font=('Arial',18))
        self.scoreLabel.grid(row=0,column=2,columnspan=4)
        self.highScoreLabel = Label(self,text='High Score ' + str(self.highScore),font=('Arial',18))
        self.highScoreLabel.grid(row=0,column=6,columnspan=2,sticky=E)
        # initialize game data
        # set up dice
        self.dice = []
        for n in range(8):
            self.dice.append(GUIDie(self,[1,2,3,4,5,6],['red']+['black']*5))
            self.dice[n].grid(row=1,column=n)
        # set up buttons
        self.rollButton = Button(self,text='Roll',command=self.roll)
        self.rollButton.grid(row=2)
        self.stopButton = Button(self,text='Stop',state=DISABLED,command=self.stop)
        self.stopButton.grid(row=3)

    def roll(self):
        '''ShotPutFrame.roll()
        handler method for the roll button click'''
        self.dice[self.gameround].roll()
        if self.dice[self.gameround].get_top() != 1:
            self.score +=  self.dice[self.gameround].get_top()
            self.scoreLabel['text'] = 'Attempt #' + str(self.attemptNum)+' Score: '+str(self.score)
            self.gameround += 1  # go to next round
            if self.gameround < 8:  # move buttons to next pair of dice
                self.rollButton.grid(row=2,column=self.gameround)
                self.stopButton.grid(row=3,column=self.gameround)
                if self.gameround == 0:
                    self.rollButton['state'] = ACTIVE
                    self.stopButton['state'] = DISABLED
                else:
                    self.rollButton['state'] = ACTIVE
                    self.stopButton['state'] = ACTIVE
            else: #New attempt or game over
                self.gameround = 0
                self.rollButton.grid(row=2,column=self.gameround)
                self.stopButton.grid(row=3,column=self.gameround)
                self.rollButton['state'] = ACTIVE
                self.stopButton['state'] = DISABLED
                if self.score > self.highScore:
                    self.highScore = self.score
                if self.attemptNum != 3:
                    self.attemptNum += 1
                    self.score = 0
                    self.scoreLabel['text'] = 'Attempt #' + str(self.attemptNum)+' Score: '+str(self.score)
                    self.highScoreLabel['text'] = 'High Score ' + str(self.highScore)
                    for die in self.dice:
                        die.erase()
                else: 
                    self.rollButton.grid_remove()
                    self.stopButton.grid_remove()
                    self.scoreLabel['text'] = 'Game Over'
                    self.highScoreLabel['text'] = 'High Score ' + str(self.highScore)
        else:
            self.score = 0
            self.scoreLabel['text'] = 'FOULED ATTEMPT'
            self.stopButton['text'] = 'Foul'
            self.rollButton['state'] = DISABLED
            self.stopButton['state'] = ACTIVE

    def stop(self):
        '''ShotPutFrame.stop()
        handler method for the stop button click'''
        self.gameround = 0
        self.rollButton.grid(row=2,column=self.gameround)
        self.stopButton.grid(row=3,column=self.gameround)
        self.rollButton['state'] = ACTIVE
        self.stopButton['state'] = DISABLED
        self.stopButton['text'] = 'Stop'
        if self.score > self.highScore:
            self.highScore = self.score
        if self.attemptNum != 3:
            self.attemptNum += 1
            self.score = 0
            self.scoreLabel['text'] = 'Attempt #' + str(self.attemptNum)+' Score: '+str(self.score)
            self.highScoreLabel['text'] = 'High Score ' + str(self.highScore)
            for die in self.dice:
                die.erase()
        else: 
            self.rollButton.grid_remove()
            self.stopButton.grid_remove()
            self.scoreLabel['text'] = 'Game Over'
            self.highScoreLabel['text'] = 'High Score ' + str(self.highScore)
        self.rollButton['state'] = ACTIVE
name = input("Enter your name: ")
root = Tk()
root.title('Shot Put')
game = ShotPutFrame(root,name)
game.mainloop()