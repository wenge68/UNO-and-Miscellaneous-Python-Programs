import random


class Die:
    '''Die class'''

    def __init__(self,sides=6):
        '''Die(sides)
        creates a new Die object
        int sides is the number of sides
        (default is 6)
        -or- sides is a list/tuple of sides'''
        # if an integer, create a die with sides
        #  from 1 to sides
        if isinstance(sides,int):
            self.numSides = sides
            self.sides = list(range(1,sides+1))
        else:  # use the list/tuple provided 
            self.numSides = len(sides)
            self.sides = list(sides)
        # roll the die to get a random side on top to start
        self.roll()

    def __str__(self):
        '''str(Die) -> str
        string representation of Die'''
        return 'A '+str(self.numSides)+'-sided die with '+\
               str(self.get_top())+' on top'

    def roll(self):
        '''Die.roll()
        rolls the die'''
        # pick a random side and put it on top
        self.top = self.sides[random.randrange(self.numSides)]

    def get_top(self):
        '''Die.get_top() -> object
        returns top of Die'''
        return self.top

    def set_top(self,value):
        '''Die.set_top(value)
        sets the top of the Die to value
        Does nothing if value is illegal'''
        if value in self.sides:
            self.top = value

### end Die class ###

class DinoDie(Die):
    '''implements one die for Dino Hunt'''
    def __init__(self, color):
        '''DinoDie(color) creates a new DinoDie object
        color is the color of the DinoDie 
        this color determines the sides of the die'''
        if color == "green":
            Die.__init__(self, ["dino", "dino", "dino", "foot", "foot", "leaf"])
        if color == "yellow":
            Die.__init__(self, ["dino", "dino", "foot", "foot", "leaf", "leaf"])
        if color == "red":
            Die.__init__(self, ["dino", "foot", "foot", "leaf", "leaf", "leaf"])
        self.color = color
    def __str__(self):
        '''str(DinoDie) -> str
        string representation of DinoDie'''
        top = self.get_top()
        return "A " + self.color + " Dino die with a " + top + " on top."
class DinoPlayer:
    '''implements a player of Dino Hunt'''
    def __init__(self, name):
        '''DinoPlayer creates a new DinoPlayer object
        name is the name of the DinoPlayer'''
        self.name = name
        self.score = 0
    def __str__(self):
        '''str(DinoPlayer) -> str
        string representation of DinoPlayer'''
        return self.name + " has " + str(self.score)+" points."
    def take_turn(self):
        '''take_turn() 
        player plays a turn'''
        rolls = []
        dieList = []
        for i in range(6):
            dieList.append(DinoDie("green"))
        for i in range(4):
            dieList.append(DinoDie("yellow"))
        for i in range(3):
            dieList.append(DinoDie("red"))
        print (self.name + " it's your turn.")
        self.print_die_list(dieList)
        rollAgain = True
        while len(dieList) != 0 and rollAgain:
            if len(dieList) > 3:
                randomDies = []
                input("Press enter to select and roll your dice.")
                for i in range(3):
                    randomIndex = random.randint(0, len(dieList) - 1)
                    dieList[randomIndex].roll()
                    randomDies.append(dieList[randomIndex])
                    if dieList[randomIndex].get_top() == "foot" or dieList[randomIndex].get_top() == "dino":
                        dieList.pop(randomIndex)
                for die in randomDies:
                    rolls.append(die.get_top())
            else:
                input("Press enter to roll the dice that have been selected.")
                randomDies = dieList 
                for die in randomDies:
                    die.roll()
                for i in range(len(dieList)):
                    if dieList[i].get_top() == "foot" or dieList[i].get_top() == "dino":
                        dieList.pop(i)
            for die in randomDies:
                print(die)
            feetNum = self.calculate_feet(rolls)
            dinoNum = self.calculate_dino(rolls)
            if feetNum >= 3:
                print("Too bad, you got stomped!")
                rolls = []
                break
            print ("This turn so far: " + str(dinoNum) +" dinos and " + str(feetNum) + " feet.")
            self.print_die_list(dieList)
            rollAgainInput = input("Do you want to roll again? y/n")
            if rollAgainInput == "y":
                rollAgain = True
            else:
                rollAgain = False
        self.score += self.calculate_dino(rolls)
    def print_die_list(self, dieList):
        '''print_die_list(dieList)
        prints the dieList'''
        print("You have " + str(len(dieList)) + " dice remaining.")
        green = 0
        red = 0
        yellow = 0
        for die in dieList:
            dieColor = die.color
            if dieColor == "green":
                green+=1
            if dieColor == "red":
                red+=1
            if dieColor == "yellow":
                yellow+=1
        print(str(green) + " green, " + str(yellow) + " yellow, " + str(red) + " red.")
    def calculate_feet(self, rolls):
        '''calculate_feet(rolls) -> int
        returns the number of feet in a list of rolls'''
        feetNum = 0
        for roll in rolls:
            if roll == "foot":
                feetNum += 1
        return feetNum
    def calculate_dino(self, rolls):
        '''calculate_dino(rolls) -> int
        returns the number of dino in a list of rolls'''
        dinoNum = 0
        for roll in rolls:
            if roll == "dino":
                dinoNum += 1
        return dinoNum
    def get_score(self):
        return self.score

def play_dino_hunt(numPlayers,numRounds):
    '''play_dino_hunt(numPlayer,numRounds)
    plays a game of Dino Hunt
      numPlayers is the number of players
      numRounds is the number of turns per player'''
    ### you need to add the code ###
    players = []
    for i in range(numPlayers):
        playerName = input("What is player #" + str(i + 1) +'s name?')
        players.append(DinoPlayer(playerName))
    roundNum = 1
    while roundNum <= numRounds:
        print ("Round # " + str(roundNum))
        for player in players:
            print(player)
        for player in players:
            player.take_turn()
        roundNum += 1
    maxScore = None
    maxScorePlayer = None
    for player in players:
        playerScore = player.get_score()
        if maxScore == None or playerScore > maxScore:
            maxScore = playerScore
            maxScorePlayer = player
    print("We have a winner!")
    print(maxScorePlayer)
play_dino_hunt(2, 2)
