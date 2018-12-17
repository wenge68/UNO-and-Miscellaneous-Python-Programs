import random
#fix reset decks in submission
#Fix print s
#PROOF READ ACTUAL SUBMISSION FOR WRITTEN ASSIGNMENT
#Make sure to convert any input to ints
class UnoCard:
    '''represents an Uno card
    attributes:
      rank: int from 0 to 9
      color: string'''

    def __init__(self,rank,color):
        '''UnoCard(rank,color) -> UnoCard
        creates an Uno card with the given rank and color'''
        self.rank = rank
        self.color = color

    def __str__(self):
        '''str(Unocard) -> str'''
        return(str(self.color)+' '+str(self.rank))

    def is_match(self,other):
        '''UnoCard.is_match(UnoCard) -> boolean
        returns True if the cards match in rank or color, False if not'''
        #check if IN list both ways or just ==
        if type(self.color) is list:
            return other.color in self.color or self.rank == other.rank
        if type(other.color) is list:
            return self.color in other.color or self.rank == other.rank
        return self.color == other.color or self.rank == other.rank 

class UnoDeck:
    '''represents a deck of Uno cards
    attribute:
      deck: list of UnoCards'''

    def __init__(self):
        '''UnoDeck() -> UnoDeck
        creates a new full Uno deck'''
        self.deck = []
        for color in ['red', 'blue', 'green', 'yellow']:
            self.deck.append(UnoCard(0,color))  # one 0 of each color
            for i in range(2):
                for n in range(1,10):  # two of each of 1-9 of each color
                    self.deck.append(UnoCard(str(n),color))
                self.deck.append(UnoCard("Skip", color))
                self.deck.append(UnoCard("Reverse", color))
                self.deck.append(UnoCard("Draw Two", color))
        self.deck.append(UnoCard("Wildcard", ['red','blue','green','yellow']))
        self.deck.append(UnoCard("Wildcard", ['red','blue','green','yellow']))
        self.deck.append(UnoCard("Wildcard", ['red','blue','green','yellow']))
        self.deck.append(UnoCard("Wildcard", ['red','blue','green','yellow']))
        self.deck.append(UnoCard("Wild Draw Four", ['red','blue','green','yellow']))
        self.deck.append(UnoCard("Wild Draw Four", ['red','blue','green','yellow']))
        self.deck.append(UnoCard("Wild Draw Four", ['red','blue','green','yellow']))
        self.deck.append(UnoCard("Wild Draw Four", ['red','blue','green','yellow']))
        random.shuffle(self.deck)  # shuffle the deck

    def __str__(self):
        '''str(Unodeck) -> str'''
        return 'An Uno deck with '+str(len(self.deck))+' cards remaining.'

    def is_empty(self):
        '''UnoDeck.is_empty() -> boolean
        returns True if the deck is empty, False otherwise'''
        return len(self.deck) == 0

    def deal_card(self):
        '''UnoDeck.deal_card() -> UnoCard
        deals a card from the deck and returns it
        (the dealt card is removed from the deck)'''
        return self.deck.pop()

    def reset_deck(self,pile):
        '''UnoDeck.reset_deck(pile)
        resets the deck from the pile'''
        self.deck = pile.reset_pile() # get cards from the pile
        random.shuffle(self.deck)  # shuffle the deck

class UnoPile:
    '''represents the discard pile in Uno
    attribute:
      pile: list of UnoCards'''

    def __init__(self,deck):
        '''UnoPile(deck) -> UnoPile
        creates a new pile by drawing a card from the deck'''
        card = deck.deal_card()
        self.pile = [card]  # all the cards in the pile

    def __str__(self):
        '''str(UnoPile) -> str'''
        return 'The pile has '+str(self.pile[-1])+' on top.'

    def top_card(self):
        '''UnoPile.top_card() -> UnoCard
        returns the top card in the pile'''
        return self.pile[-1]

    def add_card(self,card):
        '''UnoPile.add_card(card)
        adds the card to the top of the pile'''
        self.pile.append(card)

    def reset_pile(self):
        '''UnoPile.reset_pile() -> list
        removes all but the top card from the pile and
          returns the rest of the cards as a list of UnoCards'''
        newdeck = self.pile[:-1]
        self.pile = [self.pile[-1]]
        return newdeck

class UnoPlayer:
    '''represents a player of Uno
    attributes:
      name: a string with the player's name
      hand: a list of UnoCards'''

    def __init__(self,name,deck):
        '''UnoPlayer(name,deck) -> UnoPlayer
        creates a new player with a new 7-card hand'''
        self.name = name
        self.hand = [deck.deal_card() for i in range(7)]

    def __str__(self):
        '''str(UnoPlayer) -> UnoPlayer'''
        return str(self.name)+' has '+str(len(self.hand))+' cards.'

    def get_name(self):
        '''UnoPlayer.get_name() -> str
        returns the player's name'''
        return self.name

    def get_hand(self):
        '''get_hand(self) -> str
        returns a string representation of the hand, one card per line'''
        output = ''
        for card in self.hand:
            output += str(card) + '\n'
        return output

    def has_won(self):
        '''UnoPlayer.has_won() -> boolean
        returns True if the player's hand is empty (player has won)'''
        return len(self.hand) == 0

    def draw_card(self,deck):
        '''UnoPlayer.draw_card(deck) -> UnoCard
        draws a card, adds to the player's hand
          and returns the card drawn'''
        card = deck.deal_card()  # get card from the deck
        self.hand.append(card)   # add this card to the hand
        return card

    def play_card(self,card,pile):
        '''UnoPlayer.play_card(card,pile)
        plays a card from the player's hand to the pile
        CAUTION: does not check if the play is legal!'''
        if type(card.color) is list:
            wildColor = input("What color do you want to make the wild card? ")
            card.color = wildColor
        self.hand.remove(card)
        pile.add_card(card)
    def take_turn(self,deck,pile):
        '''UnoPlayer.take_turn(deck,pile)
        takes the player's turn in the game
          deck is an UnoDeck representing the current deck
          pile is an UnoPile representing the discard pile'''
        # print player info
        print(self.name+", it's your turn.")
        print(pile)
        print("Your hand: ")
        print(self.get_hand())
        # get a list of cards that can be played
        playedCard = None#The card that the person plays
        topcard = pile.top_card()
        matches = [card for card in self.hand if card.is_match(topcard)]
        if len(matches) > 0:  # can play
            for index in range(len(matches)):
                # print the playable cards with their number
                print(str(index+1) + ": " + str(matches[index]))
            # get player's choice of which card to play
            choice = 0
            while choice < 1 or choice > len(matches):
                choicestr = input("Which do you want to play? ")
                if choicestr.isdigit():
                    choice = int(choicestr)
            # play the chosen card from hand, add it to the pile
            numberOfColorMatches = 0
            for match in matches:
                if match.rank == "Wild Draw Four":
                    continue
                if type(topcard.color) is list:
                    if match.color in topcard.color:
                        numberOfColorMatches+=1
                elif type(match.color) is list:
                    if topcard.color in match.color:
                        numberOfColorMatches+=1
                else:
                    if topcard.color == match.color:
                        numberOfColorMatches+=1
            if matches[choice-1].rank == "Wild Draw Four" and numberOfColorMatches != 0:#make this to handle only when color matches
                badInput = True
                while badInput:
                    print ("You can only choose Wild Card Four's when you have no other color matches.")
                    choice = 0
                    while choice < 1 or choice > len(matches):
                        choicestr = input("Which do you want to play? ")
                        if choicestr.isdigit():
                            choice = int(choicestr)
                    if matches[choice-1].rank != "Wild Draw Four":
                        badInput = False

            self.play_card(matches[choice-1],pile)
            playedCard = matches[choice-1]
            if type(topcard.color) is list:
                topcard.color = ['red','blue','green','yellow']
        else:  # can't play
            print("You can't play, so you have to draw.")
            input("Press enter to draw.")
            # check if deck is empty -- if so, reset it
            if deck.is_empty():
                if type(topcard.color) is list:
                    topcard.color = ['red','blue','green','yellow']
                deck.reset_deck(pile)

            # draw a new card from the deck
            newcard = self.draw_card(deck)
            print("You drew: "+str(newcard))
            if newcard.is_match(topcard): # can be played
                print("Good -- you can play that!")
                self.play_card(newcard,pile)
                playedCard = newcard
            else:   # still can't play
                print("Sorry, you still can't play.")
                playedCard = False
            input("Press enter to continue.")
        return playedCard
class AIPlayer(UnoPlayer):
    def play_card(self,card,pile):
        '''UnoPlayer.play_card(card,pile)
        plays a card from the player's hand to the pile
        CAUTION: does not check if the play is legal!'''
        wildColorList = ['red', 'blue', 'green', 'yellow']
        if type(card.color) is list:
            wildColor = random.choice(wildColorList)
            card.color = wildColor
        self.hand.remove(card)
        pile.add_card(card)
    def take_turn(self,deck,pile):
        '''UnoPlayer.take_turn(deck,pile)
        takes the player's turn in the game
          deck is an UnoDeck representing the current deck
          pile is an UnoPile representing the discard pile'''
        # print player info
        print(self.name+", it's your turn.")
        print(pile)
        print("Your hand: ")
        print(UnoPlayer.get_hand(self))
        # get a list of cards that can be played
        playedCard = None#The card that the person plays
        topcard = pile.top_card()
        matches = [card for card in self.hand if card.is_match(topcard)]
        numberOfColorMatches = 0
        if len(matches) > 0:  # can play
            choice = random.randint(1, len(matches))
            for index in range(len(matches)):
                # print the playable cards with their number
                print(str(index+1) + ": " + str(matches[index]))
            # get player's choice of which card to play
            for match in matches:
                if match.rank == "Wild Draw Four":
                    continue
                if type(topcard.color) is list:
                    if match.color in topcard.color:
                        numberOfColorMatches+=1
                elif type(match.color) is list:
                    if topcard.color in match.color:
                        numberOfColorMatches+=1
                else:
                    if topcard.color == match.color:
                        numberOfColorMatches+=1
            while matches[choice-1].rank == "Wild Draw Four" and numberOfColorMatches != 0:#make this to handle only when color matches
                choice = random.randint(1, len(matches))
            self.play_card(matches[choice-1],pile)
            playedCard = matches[choice-1]
            if type(topcard.color) is list:
                topcard.color = ['red','blue','green','yellow']
        else:  # can't play
            print("You can't play, so you have to draw.")
            # check if deck is empty -- if so, reset it
            if deck.is_empty():
                if type(topcard.color) is list:
                    topcard.color = ['red','blue','green','yellow']
                deck.reset_deck(pile)
            # draw a new card from the deck
            newcard = self.draw_card(deck)
            print("You drew: "+str(newcard))
            if newcard.is_match(topcard): # can be played
                print("Good -- you can play that!")
                self.play_card(newcard,pile)
                playedCard = newcard
            else:   # still can't play
                print("Sorry, you still can't play.")
                playedCard = False
        return playedCard
def play_uno(numPlayers):
    '''play_uno(numPlayers)
    plays a game of Uno with numPlayers'''
    # set up full deck and initial discard pile
    #BAD DRAW LOOP IN BAD SPOT im not going to fix it because i'm too lazy
    # set up the players
    playerDictAINames = dict()
    for n in range(numPlayers):
        # get each player's name, then create an UnoPlayer
        name = input('Player #'+str(n+1)+', enter your name: ')
        aiOrNot = input("Do you want this player to be an ai?")
        playerDictAINames[name] = aiOrNot
    # randomly assign who goes first
    badDraw = True
    while badDraw:
        playerList = []
        deck = UnoDeck()
        pile = UnoPile(deck)
        for playerName in playerDictAINames:
            if playerDictAINames[playerName] == "yes":
                playerList.append(AIPlayer(playerName, deck))
            elif playerDictAINames[playerName] == "no":
                playerList.append(UnoPlayer(playerName, deck))
        currentPlayerNum = random.randrange(numPlayers)
        moveRotation = 1 #1 is forward, -1 is reverse, 2 is skip
        # play the game
        drawTwo = None
        drawFour = None
        #Do the appropriate actions if the top card is an action card
        topCard = pile.top_card()
        if topCard.rank == "Draw Two":
            drawTwo = currentPlayerNum
        elif topCard.rank == "Reverse":
            moveRotation *= -1
        elif topCard.rank == "Skip":
            currentPlayerNum = (currentPlayerNum + 1)%numPlayers
        elif topCard.rank == "Wildcard":
            if type(playerList[currentPlayerNum]) is AIPlayer:
                wildColorList = ['red', 'blue', 'green', 'yellow']
                wildColor = random.choice(wildColorList)
                topCard.color = wildColor
            else:
                wildColor = input("The top card is a wild card. What color does" + playerList[currentPlayerNum].get_name() +" want to make it? ")
                topCard.color = wildColor
        elif topCard.rank == "Wild Draw Four":
            continue
        badDraw = False 
    while True:
        # print the game status
        print('-------')
        for player in playerList:
            print(player)
        print('-------')
        # take a turn
        newPlayerNum = currentPlayerNum
        if (drawTwo == None or drawTwo != currentPlayerNum) and (drawFour == None or drawFour != currentPlayerNum):
            playedCard = playerList[currentPlayerNum].take_turn(deck,pile)
            if playedCard == False:
                pass
            else:
                #Check if they played a skip card
                if playedCard.rank == "Skip":
                    #Skip the next player
                    if moveRotation == -1:
                        newPlayerNum -=1
                    if moveRotation == 1:
                        newPlayerNum +=1
                #Check if they played a reverse card
                elif playedCard.rank == "Reverse":
                    #Change the rotation
                    moveRotation *= -1
                #Check if the
                elif playedCard.rank == "Draw Two":
                    drawTwo = (currentPlayerNum + moveRotation)%numPlayers
                elif playedCard.rank == "Wild   Draw Four":
                    drawFour = (currentPlayerNum + moveRotation)%numPlayers
        else:
            print(str(playerList[currentPlayerNum])+", it's your turn.")
            print(pile)
            if drawTwo == currentPlayerNum:
                if deck.is_empty():
                    if type(topcard.color) is list:
                        topcard.color = ['red','blue','green','yellow']
                    deck.reset_deck(pile)
                firstDraw = playerList[currentPlayerNum].draw_card(deck)
                if deck.is_empty():
                    if type(topcard.color) is list:
                        topcard.color = ['red','blue','green','yellow']
                    deck.reset_deck(pile)
                secondDraw = playerList[currentPlayerNum].draw_card(deck)
                print(playerList[currentPlayerNum].get_name()+" drew " + str(firstDraw) +" and " + str(secondDraw))
                drawTwo = None
            if drawFour == currentPlayerNum:
                if deck.is_empty():
                    if type(topcard.color) is list:
                        topcard.color = ['red','blue','green','yellow']
                    deck.reset_deck(pile)
                firstDraw = playerList[currentPlayerNum].draw_card(deck)
                if deck.is_empty():
                    if type(topcard.color) is list:
                        topcard.color = ['red','blue','green','yellow']
                    deck.reset_deck(pile)
                secondDraw = playerList[currentPlayerNum].draw_card(deck)
                if deck.is_empty():
                    if type(topcard.color) is list:
                        topcard.color = ['red','blue','green','yellow']
                    deck.reset_deck(pile)
                thirdDraw = playerList[currentPlayerNum].draw_card(deck)
                if deck.is_empty():
                    if type(topcard.color) is list:
                        topcard.color = ['red','blue','green','yellow']
                    deck.reset_deck(pile)
                fourthDraw = playerList[currentPlayerNum].draw_card(deck)
                print(playerList[currentPlayerNum].get_name()+" drew " + str(firstDraw) +" and " + str(secondDraw) +" and " + str(thirdDraw) +" and " + str(fourthDraw))
                drawFour = None
            
        # check for a winner
        if playerList[currentPlayerNum].has_won():
            print(playerList[currentPlayerNum].get_name()+" wins!")
            print("Thanks for playing!")
            break
        # go to the next player
        currentPlayerNum = (newPlayerNum + moveRotation) % numPlayers
play_uno(3)