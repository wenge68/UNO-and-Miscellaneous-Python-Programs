from tkinter import *
import random
inBetweenFreeze = 1
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


class GUIFreezeableDie(GUIDie):
    '''a GUIDie that can be "frozen" so that it can't be rolled'''

    def __init__(self,master,valueList=[1,2,3,4,5,6],colorList=['black']*6):
        '''GUIFreezeableDie(master,[valueList,colorList]) -> GUIFreezeableDie
        creates a GUI 6-sided freeze-able die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        GUIDie.__init__(self,master,valueList,colorList)
        self.isFrozen = False  # die starts out unfrozen

    def is_frozen(self):
        '''GUIFreezeableDie.is_frozen() -> bool
        returns True if the die is frozen, False otherwise'''
        return self.isFrozen
    
    def toggle_freeze(self):
        '''GUIFreezeableDie.toggle_freeze()
        toggles the frozen status'''
        if self.is_frozen():
            self.isFrozen = False
            self.configure(background = "white")
        else:
            self.isFrozen = True
            self.configure(background = "grey")
        self.freezeButton['state'] = DISABLED
        global inBetweenFreeze
        inBetweenFreeze += 1
    def roll(self):
        '''GuiFreezeableDie.roll()
        overloads GUIDie.roll() to not allow a roll if frozen'''
        if not self.isFrozen:
            GUIDie.roll(self)
    def get_top(self):
        if self.isFrozen:
            return (self.valueList[self.top-1],False)
        else:
            return (self.valueList[self.top-1], True)
    def set_freeze_button(self, freezeButton):
        self.freezeButton = freezeButton
        self.freezeButton['state'] = DISABLED
class Discus(Frame):
    '''a small application to test the freezeable die'''

    def __init__(self,master, name):
        Frame.__init__(self,master)
        self.grid()

        self.dice = []
        self.buttons = []

        self.name = name
        self.attemptNum = 1
        self.score = 0
        self.highScore = 0

        self.nameLabel = Label(self,text=self.name,font=('Arial',18))
        self.nameLabel.grid(columnspan=2,sticky=W)
        self.scoreLabel = Label(self,text='Attempt #' + str(self.attemptNum) + ' Score: 0',font=('Arial',18))
        self.scoreLabel.grid(row=0,column=2,columnspan=4)
        self.highScoreLabel = Label(self,text='High Score ' + str(self.highScore),font=('Arial',18))
        self.highScoreLabel.grid(row=0,column=6,columnspan=2,sticky=E)

        for n in range(6):
            self.dice.append(GUIFreezeableDie(self,[1,2,3,4,5,6],['red', 'black', 'red', 'black', 'red', 'black']))
            self.dice[n].grid(row=1,column=n)
            self.buttons.append(Button(self,text='Freeze',command=self.dice[n].toggle_freeze))
            self.buttons[n].grid(row=2,column=n)
            self.dice[n].set_freeze_button(self.buttons[n])

        self.rollButton = Button(self,text='Roll',command=self.roll)
        self.rollButton.grid(row=1, column=6, columnspan=2)
        self.stopButton = Button(self,text='Stop',state=DISABLED,command=self.stop)
        self.stopButton.grid(row=2, column=6, columnspan=2)

        self.infoLabel = Label(self,text="Click roll button to start",font=('Arial',18))
        self.infoLabel.grid(row=3, column=0, columnspan=6)
    def roll(self):
        global inBetweenFreeze
        if inBetweenFreeze > 0:
            self.infoLabel['text'] = "Click stop to keep"
            inBetweenFreeze = 0
            results = []
            filteredResults = []
            for die in self.dice:
                die.roll()
                results.append(die.get_top())
            for result in results:
                if not result[1]:
                    continue
                elif (result[0]%2)!= 0:
                    continue
                filteredResults.append(result[0])
            self.score += sum(filteredResults)
            self.scoreLabel['text'] = 'Attempt #' + str(self.attemptNum) + ' Score: ' + str(self.score)
            if self.stopButton['state'] == DISABLED:
                for die in self.dice:
                    if die.get_top()[0]%2==0:
                        die.freezeButton['state'] = ACTIVE
                self.stopButton['state'] = ACTIVE
            else:
                for die in self.dice:
                    if die.get_top()[0]%2!=0:
                        die.freezeButton['state'] = DISABLED
                    else:
                        if not die.is_frozen():
                            die.freezeButton['state'] = ACTIVE
        else:
            self.infoLabel['text'] = "You must freeze a die to reroll"
        fouled = True
        for freezeButton in self.buttons:
            if freezeButton['state'] == ACTIVE:
                fouled = False
                break
        if fouled:
            self.score = 0
            self.stopButton['text'] = 'FOUL'
            self.rollButton['state'] = DISABLED
            self.scoreLabel['text'] = 'FOULED ATTEMPT'
            self.infoLabel['text'] = 'Click FOUL to continue'
    def stop(self):
        self.attemptNum += 1
        if self.score > self.highScore:
            self.highScore = self.score
        if self.attemptNum != 4:
            self.score = 0
            self.scoreLabel['text'] = 'Attempt #' + str(self.attemptNum)+' Score: '+str(self.score)
            self.highScoreLabel['text'] = 'High Score ' + str(self.highScore)
            self.infoLabel['text'] = 'Click roll button to start'
            for die in self.dice:
                die.erase()
                if die.is_frozen():
                    die.toggle_freeze()
                die.freezeButton['state'] = DISABLED
            if self.stopButton['text'] == "FOUL":
                self.stopButton['text'] = 'Stop'
                self.rollButton['state'] = ACTIVE
            self.stopButton['state'] = DISABLED
        else:
            self.rollButton.grid_remove()
            self.stopButton.grid_remove()
            self.infoLabel.grid_remove()
            self.scoreLabel['text'] = 'Game Over'
            self.highScoreLabel['text'] = 'High Score ' + str(self.highScore)
# test application
root = Tk()
test = Discus(root, "David")
root.mainloop()