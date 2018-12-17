 import random
#Make a class for strats 
#Don't show the computer's cards 
class Domino:
	def __init__(self, leftNum, rightNum):
		self.leftNum = leftNum
		self.rightNum = rightNum
	def __str__(self):
		return str(self.leftNum) + "|" + str(self.rightNum)
	def how_match(self, chain):
		#Left -> 0
		#Right -> 1
		#Strats as tuples
		chainLeft = chain.get_left()
		chainRight = chain.get_right()
		strats = []
		if self.leftNum == chainLeft:
			strats.append((0, 0))
		else:
			strats.append(False)
		if self.leftNum == chainRight:
			strats.append((0, 1))
		else:
			strats.append(False)
		if self.rightNum == chainLeft:
			strats.append((1, 0))
		else:
			strats.append(False)
		if self.rightNum == chainRight:
			strats.append((1, 1))
		else:
			strats.append(False)
		return strats
class DominoChain:
	def __init__(self, domino):
		self.chain = [domino]
	def __str__(self):
		string = ''
		for domino in self.chain:
			string += str(domino) + '\n'
		return string
	def get_left(self):
		leftMostDomino = self.chain[0]
		leftNumLeftMostDomino = leftMostDomino.leftNum
		return leftNumLeftMostDomino
	def get_right(self):
		rightMostDomino = self.chain[len(self.chain)-1]
		rightNumRightMostDomino = rightMostDomino.rightNum
		return rightNumRightMostDomino
	def add_to_chain(self, domino, strat):
		if strat == (0,0):
			(domino.leftNum,domino.rightNum) = (domino.rightNum, domino.leftNum)
			self.chain.insert(0, domino)
		elif strat == (0,1):
			self.chain.append(domino)
		elif strat == (1,0):
			self.chain.insert(0, domino)
		elif strat == (1,1):
			(domino.leftNum,domino.rightNum) = (domino.rightNum, domino.leftNum)
			self.chain.append(domino)
class DominoPlayer:
	def __init__(self, name, dominoes):
		self.name = name
		self.dominoes = dominoes
	def __str__(self):
		return self.name + " has " + str(len(self.dominoes)) + " left."
	def get_dominoes(self):
		string = ''
		for domino in self.dominoes:
			string += str(domino) + '\n'
		return string
	def play_domino(self, domino, chain):
		strats = domino.how_match(chain)
		print ("Here are the possible moves with " + str(domino) + '.')
		strats = list(filter((False).__ne__, strats))
		for i in range(len(strats)):
			print ("Strategy #" + str(i) + ": " + str(strats[i]))
		choice = int(input("Choose a strategy: "))
		stratChoice = strats[choice]
		chain.add_to_chain(domino, stratChoice)
		self.dominoes.remove(domino)
	def take_turn(self, chain):
		matchingDominoes = []
		for domino in self.dominoes:
			strats = domino.how_match(chain)
			stratCount = 0
			for strat in strats:
				if strat == False:
					stratCount += 1
			if stratCount == 4:
				continue
			matchingDominoes.append(domino)
		if matchingDominoes != []:
			print ("You can play the following dominoes: ")
			for i in range(len(matchingDominoes)):
				domino = matchingDominoes[i]
				print (domino)
			choice = int(input("Choose a domino: "))
			dominoChoice = matchingDominoes[choice]
			self.play_domino(dominoChoice, chain)
			return True
		else:
			return False
	def has_won(self):
		if self.dominoes == []:
			return True
		else:
			return False
	def get_name(self):
		return self.name
class AIPlayer(DominoPlayer):
	def play_domino(self, domino, chain):
		strats = domino.how_match(chain)
		strats = list(filter((False).__ne__, strats))
		choice = random.randint(0, len(strats)-1)
		stratChoice = strats[choice]
		chain.add_to_chain(domino, stratChoice)
		self.dominoes.remove(domino)
	def take_turn(self, chain):
		matchingDominoes = []
		for domino in self.dominoes:
			strats = domino.how_match(chain)
			stratCount = 0
			for strat in strats:
				if strat == False:
					stratCount += 1
			if stratCount == 4:
				continue
			matchingDominoes.append(domino)
		if matchingDominoes != []:
			choice = random.randint(0, len(matchingDominoes)-1)
			dominoChoice = matchingDominoes[choice]
			self.play_domino(dominoChoice, chain)
			return True
		else:
			return False
def play_dominoes():
	dominoes = []
	for i in range(8):
		for j in range(8):
			dominoes.append(Domino(i,j))
	random.shuffle(dominoes)
	userName = input("What is your player name?")
	playerNames = [userName,"AI 1", "AI 2", "AI 3"]
	playerList = []
	x = 0
	y = 8
	firstUser = True
	for i in range(4):
		playerName = playerNames[i]
		playerDominoes = []
		for j in range(x,y):
			playerDominoes.append(dominoes[j])
		if firstUser:
			playerList.append(DominoPlayer(playerName, playerDominoes))
			firstUser = False
		else:
			playerList.append(AIPlayer(playerName, playerDominoes))
		x = y
		y = y + 8
	greaterBreak = False

	for player in playerList:
		playerDominoes = player.dominoes
		for domino in playerDominoes:
			if domino.leftNum == 6 and domino.rightNum == 6:
				playerDominoes.remove(domino)
				greaterBreak = True
				break
		if greaterBreak:
			break
	chain = DominoChain(Domino(6,6))
	print()
	blockCountList = []
	currentPlayerNum = random.randint(0, len(playerList)-1)
	lastMover = None
	while not playerList[0].has_won() or playerList[1].has_won() or playerList[2].has_won() or playerList[3].has_won() or blockCount != 4:
		print (chain)
		print ("Player #"+str(currentPlayerNum)+":")
		print (playerList[currentPlayerNum].get_dominoes())
		if not playerList[currentPlayerNum].take_turn(chain):
			blockCountList.append(1)
		else:
			lastMover = currentPlayerNum
			blockCountList.append(0)
		currentPlayerNum = (currentPlayerNum + 1) % 4
		if len(blockCountList)>=4:
			if sum(blockCountList[-4:])==4:
				print("The winner is " + playerList[lastMover].get_name()+'.')
				break
play_dominoes()


