import string
def split_list(alist, wanted_parts):
    '''split_list(alist, wanted_parts) -> list
    splits a larger list into wanted_parts number of smaller lists'''
    length = len(alist)#get length of list 
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]#return list that contains smaller lists
def encipher_fence(plainText,numRails):
    '''encipher_fence(plaintext,numRails) -> str
    encodes plaintext using the railfence cipher
    numRails is the number of rails'''
    RailDict=dict()#create dictionary whose keys are number of the rail and whose values are the enchiphered rails themselves 
    railCounter = 0#this variable is used to create rails until numRails is reached and append these rails to the RailDict
    while railCounter < numRails:
        EncipheredStringList=[]#this contains the enciphered string as a list for this rail number
        for letter in range(railCounter, len(plainText), numRails):#loop through the plaintext from the starting point to the ending point by the numRails
            EncipheredStringList.append(plainText[letter])#append each of these characters to the enciphered string list
        RailDict[railCounter]=EncipheredStringList#after the enciphered string list is created for that rail number append the enciphered string list to the dictionary at the value of the rail counter
        railCounter+=1#increment the rail counter
    ListOfKeys=list(RailDict.keys())#create list of the dictionary's keys
    ListOfKeys.reverse()#reverse the list because the rails are added to the final string in reverse  order
    FinalReturnStringList=[]#this is the final list of the rails added together in reverse order
    for key in ListOfKeys:
        RailDictList=RailDict[key]#get the enciphered string list at the value key 
        RailDictString=''.join(RailDictList)#convert this list to a string
        FinalReturnStringList.append(RailDictString)#append the string to the final list
    FinalReturnableString=''.join(FinalReturnStringList)#convert the final list to a string
    return FinalReturnableString
def decipher_fence(cipherText,numRails):
    '''decipher_fence(ciphertext,numRails) -> str
    returns decoding of ciphertext using railfence cipher
    with numRails rails'''
    CipherTextList = list(cipherText)#convert the cipherText to a list
    RailList=[]#create a list that will contain all the seperated rails
    if len(cipherText)%numRails==0:#if the ciphertext can be split evenly by the number of rails, it is really easy to seperate the cipher text into rails
        RailList=split_list(CipherTextList, numRails)#the rail list contains numRails number of smaller rail lists
        RailList.reverse()#sort them
    else:#if the number rails does not divide the cipher text evenly, it is very difficult to seperate the rails
        RailRemainder = len(cipherText)%numRails#first find the remainder when dividing the length of the cipher text by the number of rails
        NumberOfCharactersInRegRail = len(cipherText)//numRails#this is the number of characters in a regular rail
        RailNumDict = dict()#this dictionary contains the number of characters in each of the rails
        RailRemainderCount=RailRemainder
        for railIndex in range(0,numRails):#for every rail 
            if RailRemainderCount > 0:#if the remainder count is still greater than 0
                RailRemainderCount-=1#decrement
                RailNumDict[railIndex]=NumberOfCharactersInRegRail+1#the rail at railIndex will have the number of characters in a regular rail in addition to 1
            else:#if remainder has already been accounted for by adding to the lengths of the other rails
                RailNumDict[railIndex]=NumberOfCharactersInRegRail#the rail at railIndex only has the regular number of characters
        RailNumList=list(RailNumDict.keys())#this list contains the rail number keys(0,1,2,etc.)
        RailNumList.sort()#sort them
        BackCipherTextPlace=len(cipherText)#the back index for extracting rails from the cipher text
        FrontCipherTextPlace=len(cipherText)#the front index for extracting rails from the cipher text
        for railNum in RailNumList:#for every rail number
            FrontCipherTextPlace = BackCipherTextPlace-RailNumDict[railNum]#the front index is the back index minus the number of characters in that rail
            thisRail=cipherText[FrontCipherTextPlace:BackCipherTextPlace]#the current rail is substring of the cipher text between the front and back indices
            BackCipherTextPlace=FrontCipherTextPlace#now that this substring has been extracted the back index must become the front index to prepare for the next extraction 
            RailList.append(list(thisRail))#append thisRail to the RailList as a string
    RailCounter = 0#this will allow me to loop through the characters in all the rails
    RailMax = 0#this will be the length of the longest rail
    DecipheredStringList=[]#this is the deciphered string list
    for rail in RailList:#finds the length of the longest rail
        if len(rail)>RailMax:
            RailMax=len(rail)
    while RailCounter<RailMax:#while the rail counter is less than the longest rail length
        for rail in RailList:#for every rail in the rail list
            try:#we need to used try and except because this will fail when the rail counter exceeds the length of the shorter rails
                DecipheredStringList.append(rail[RailCounter])#append the character of the rail at the RailCounter index
            except:
                continue
        RailCounter+=1#increment the RailCounter to append the next set of characters from the rails to the deciphered string list
    FinalDecipheredStringReturnable=''.join(DecipheredStringList)#convert the deciphered list into a string
    return FinalDecipheredStringReturnable
def decode_text(cipherText,wordfilename):
    '''decode_text(ciphertext,wordfilename) -> str
    attempts to decode ciphertext using railfence cipher
    wordfilename is a file with a list of valid words'''
    fhand = open(wordfilename,'r')#open the file
    ListOfWords=[]
    for line in fhand:#read all the words into the list
        line=line.strip()
        ListOfWords.append(line)
    fhand.close()#close the file 
    maxRailWordCountNum=0#number of english words in the deciphering with the most english words
    maxRailNum=0#the number of rails that led to the maxRailWordCountNum
    for railNum in range (1,11):#for all rail numbers between 1 and 11 (including 1 and not including 11)
        englishWordCounter=0 #the number of english words in the deciphering made with the rail number
        maybePlainText=decipher_fence(cipherText,railNum)#decipher the cipher text
        translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) 
        cleanMaybePlainText=maybePlainText.translate(translator).lower()#replace punctuation with blank spaces and make lower case
        maybePlainTextList=cleanMaybePlainText.split()#split the clean maybe plain text into words
        for maybeWord in maybePlainTextList:#for all the words in the maybe plain text, check if they are in the ListOfWords and increment the english word counter if so
            if maybeWord=="i":
                englishWordCounter+=1
            if maybeWord in ListOfWords:
                 englishWordCounter+=1               
        if englishWordCounter>maxRailWordCountNum:#if the number of english words in this deciphering is greater than the current max
            maxRailWordCountNum=englishWordCounter#change the current max
            maxRailNum=railNum#change the rail number that leads to the current max
    return decipher_fence(cipherText, maxRailNum)
print(decode_text("hsi pmmiti ssa al","wordlist.txt"))





