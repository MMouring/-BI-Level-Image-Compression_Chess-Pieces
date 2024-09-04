#!/usr/bin/python3
import csv
import math
import random

def main():
    placeCounter = 0
    with open('..\\images\\32crop_csv.csv', 'r') as f:
        reader = csv.reader(f)
        imageList = list(reader)    #READ THE INFORMATION FROM THE .CSV FILE AND STORE IN A LIST
                                    #print(len(imageList)) Y
                                    #print(len(imageList[0])) X
    xValue = len(imageList[0])      #GET THE LENGTH OF THE X AXIS
    yValue = len(imageList)         #GET THE LENGTH OF THE Y AXIS
    exploration = [['BU' for x in range(xValue)] for y in range(yValue)]    #INTIALIZE A LIST WITH THE SAME DIMENSIONS OF THE IMAGE FOR TRACKING
                                                                            #EXPLORATION
       
    #THE NUMBER OF TIMES THE CHESS PIECES WILL MOVE
    numOfRuns = 550000

    #THE NUMBER OF PIECES ON THE BOARD
    numOfPieces = 16

    #KEEP TRACK OF PIECE CURRENT LOCATION
    pieceLoc = [[0 for x in range(2)] for y in range(numOfPieces)]
    
    #RECORDS FOR RECORDING THE DIRECTIONS AND COORDINATES OF EACH CHAIN
    bishopRecords = ['' for x in range(numOfPieces // 2)]
    rookRecords = ['' for x in range(numOfPieces // 2)]
    completeRookRecords = []
    completeBishopRecords = []

    #CHESS PIECES CAN MOVE IN THREE RELATIVE DIRECTIONS, FORWARD, RIGHT, LEFT
    relativeDirection = [0, 1, 2]

    #STANDARD MOVE OPTIONS
    fourStandard = [[0 for x in range(2)] for y in range(4)]    

    #RELATIVE MOVE OPTIONS
    threeRelative = [[0 for x in range(2)]for y in range(3)]    

    #THE FOLLOWING VARIABLES ARE USED TO KEEP TRACK OF THE FACE OF EACH PIECE
    forward = [0 for x in range(numOfPieces)]
    relativeFront = [0 for x in range(numOfPieces)]
    relativeForward = [0 for x in range(numOfPieces)]

    #CONTROLS THE TYPE OF MOVEMENT OPTIONS A PIECE CAN MAKE (STND || REL)
    control = ['' for x in range(numOfPieces)]

    #CONTROL THE DIRECTION THAT PIECE WILL MOVE AS DEFAULT
    directionControl = ['' for x in range(numOfPieces)]

    #THE NAME OF EACH PIECE( 0 - (1/2) :ROOK && (1/2) - LEN(-1) :BISHOP)
    pieceName = ['' for x in range(numOfPieces)]  

    #SET THE NAMES OF EACH PIECE AND ESTABLISH THEIR INITIAL DEFAULT MOVE TYPE
    for x in range(numOfPieces):
        if x < (numOfPieces // 2):
            pieceName[x] = 'rook'
        elif x >= (numOfPieces // 2):
            pieceName[x] = 'bishop'
        directionControl[x] = 'UpC'            
    #PLACE PIECES ON STARTING LOCATIONS
    for i in range(numOfPieces):
        #ROOK PIECES PLACEMENT
        if i == 0:
            #ROW 1
            pieceLoc[i][0] = math.floor(xValue * .2)        #X
            pieceLoc[i][1] = 0                              #Y
        elif i == 1:
            #ROW 1
            pieceLoc[i][0] = math.floor((xValue * .2) * 4)  #X
            pieceLoc[i][1] = 0                              #Y
        elif i == 2:
            #ROW 2
            pieceLoc[i][0] = math.floor(xValue * .2)        #X
            pieceLoc[i][1] = math.floor(yValue * .3)        #Y
        elif i == 3:
            #ROW 2
            pieceLoc[i][0] = math.floor((xValue * .2) * 4)  #X
            pieceLoc[i][1] = math.floor(yValue * .3)        #Y
        elif i == 4:
            #ROW 3
            pieceLoc[i][0] = math.floor(xValue * .2)        #X
            pieceLoc[i][1] = math.floor(yValue * .66)       #Y
        elif i == 5:
            #ROW 3
            pieceLoc[i][0] = math.floor((xValue * .2) * 4)  #X
            pieceLoc[i][1] = math.floor(yValue * .66)       #Y
        elif i == 6:
            #ROW 4
            pieceLoc[i][0] = math.floor(xValue * .2)        #X
            pieceLoc[i][1] = yValue - 1                     #Y
        elif i == 7:
            #ROW 4
            pieceLoc[i][0] = math.floor((xValue * .2) * 4)  #X
            pieceLoc[i][1] = yValue - 1                     #Y
        #BISHOP PIECES PLACEMENT
        elif i == 8:
            #ROW 1
            pieceLoc[i][0] = math.floor((xValue * .2) * 2)  #X
            pieceLoc[i][1] = 0                              #Y
        elif i == 9:
            #ROW 1
            pieceLoc[i][0] = math.floor((xValue * .2) * 3)  #X
            pieceLoc[i][1] = 0                              #Y
        elif i == 10:
            #ROW 2
            pieceLoc[i][0] = math.floor((xValue * .2) * 2)  #X
            pieceLoc[i][1] = math.floor(yValue * .3)        #Y
        elif i == 11:
            #ROW 2
            pieceLoc[i][0] = math.floor((xValue * .2) * 3)  #X
            pieceLoc[i][1] = math.floor(yValue * .3)        #Y
        elif i == 12:
            #ROW 3
            pieceLoc[i][0] = math.floor((xValue * .2) * 2)  #X
            pieceLoc[i][1] = math.floor(yValue * .66)       #Y
        elif i == 13:
            #ROW 3
            pieceLoc[i][0] = math.floor((xValue * .2) * 3)  #X
            pieceLoc[i][1] = math.floor(yValue * .66)       #Y
        elif i == 14:
            #ROW 4
            pieceLoc[i][0] = math.floor((xValue * .2) * 2)  #X
            pieceLoc[i][1] = yValue - 1                     #Y
        elif i == 15:
            #ROW 4
            pieceLoc[i][0] = math.floor((xValue * .2) * 3)  #X
            pieceLoc[i][1] = yValue - 1                     #Y

        #CHECK THE LOCATION OF THE NEWLY PLACED PIECES
        x = pieceLoc[i][0]
        y = pieceLoc[i][1]        
        get_first_coord(i, x, y, rookRecords, bishopRecords, pieceName, imageList, exploration, control, pieceLoc)        
    #BEGIN MOVING THE PIECES AROUND THE BOARD
    for n in range(numOfRuns):
        #MOVE EACH PIECE
        for i in range(numOfPieces):
            if control[i] == 'new':
                #STANDARD MOVEMENT PHASE SEARCHING FOR A COORDINATE
                standard_move(i, x, y, imageList, exploration, pieceLoc, forward, directionControl, fourStandard, pieceName)
            elif control[i] == 'first':
                #STANDARD MOVEMENT PHASE SEARCHING FOR A DIRECTION OFF OF A COORDINATE
                standard_move(i, x, y, imageList, exploration, pieceLoc, forward, directionControl, fourStandard, pieceName)
            elif control[i] == 'relative':
                #FIND THE FRONT OF THE PIECE AND GET RELATIVE LOCATIONS                
                establish_relative_front(i, forward, relativeDirection, relativeFront)
                relative_move(i, x, y, threeRelative, imageList, exploration, pieceLoc,relativeDirection, relativeFront, forward, relativeForward, directionControl, pieceName)
            #CHECK THE LOCATION OF THE PIECE'S NEW LOCATION
            check_location(i, x, y, rookRecords, bishopRecords, imageList, exploration, control, pieceLoc, pieceName, forward, relativeForward, numOfPieces, completeRookRecords, completeBishopRecords)


    ##DISPLAY FOR VALIDATION
    #for y in range(len(exploration)):
    #    print('[ ', end='')
    #    for x in range(len(exploration[y])):
    #        print(exploration[y][x], end=' ')        
    #    print(']\t', end='')
    #    print('[ ', end='')
    #    for x in range(len(exploration[y])):
    #        print(imageList[y][x], end=' ')
    #    print(']')
    ##END THE DISPLAY
    
    check_records(i, pieceName, rookRecords, completeRookRecords, bishopRecords, completeBishopRecords)
    ##DISPLAY THE RECORDS
    #for records in range(len(completeRookRecords)):
    #    print(completeRookRecords[records])
    #print('-------------------')
    #for records in range(len(completeBishopRecords)):
    #    print(completeBishopRecords[records])

    #RECREATE THE IMAGE
    recreate_image(completeRookRecords, completeBishopRecords, xValue, yValue)
    print('Check your written files. Process Completed')


#CHECK FOR A 1 ON THE FIRST LOCATION
def get_first_coord(i, x, y, rookRecords, bishopRecords, pieceName, imageList, exploration, control, pieceLoc):        
    if imageList[y][x] == '0':        
        exploration[y][x] = 'BT'
        control[i] = 'new'
        return
    elif imageList[y][x] == '1':        
        exploration[y][x] = 'WT'
        control[i] = 'first'
        xBinary = '{0:010b}'.format(x)
        yBinary = '{0:010b}'.format(y)
        subRecord = xBinary + yBinary
        #subRecord = str(x) + ' / ' +  str(y) + ' '
        write_to_records(pieceName, i, rookRecords, bishopRecords, subRecord)
        return

#END THE CHECK FOR FIRST LOCATIONS

#CHECK THE LOCATION OF THE PIECE
def check_location(i, x, y, rookRecords, bishopRecords, imageList, exploration, control, pieceLoc, pieceName, forward, relativeForward, numOfPieces, completeRookRecords, completeBishopRecords):
    x = pieceLoc[i][0]
    y = pieceLoc[i][1]
    if imageList[y][x] == '0':
        exploration[y][x] = 'BT'
        check_records(i, pieceName, rookRecords, completeRookRecords, bishopRecords, completeBishopRecords)
        control[i] = 'new'
    elif imageList[y][x] == '1':
        explored = False
        while explored == False:
            if exploration[y][x] == 'WT' or exploration[y][x] == 'BT':
                check_records(i, pieceName, rookRecords, completeRookRecords, bishopRecords, completeBishopRecords)
                control[i] = 'new'
                explored = True
                break
            else:
                exploration[y][x] = 'WT'
                if control[i] == 'new':
                    check_records(i, pieceName, rookRecords, completeRookRecords, bishopRecords, completeBishopRecords)
                    xBinary = '{0:010b}'.format(x)
                    yBinary = '{0:010b}'.format(y)
                    subRecord = xBinary + yBinary
                    #subRecord = str(x) + ' / ' +  str(y) + ' '
                    write_to_records(pieceName, i, rookRecords, bishopRecords, subRecord)
                    control[i] = 'first'
                    explored = True
                    break
                elif control[i] == 'first':
                    stndBinary = '{0:03b}'.format(forward[i])
                    subRecord = stndBinary
                    write_to_records(pieceName, i, rookRecords, bishopRecords, subRecord)
                    control[i] = 'relative'
                    explored = True
                    break
                elif control[i] == 'relative':
                    relBinary = '{0:03b}'.format(relativeForward[i])
                    subRecord = relBinary
                    write_to_records(pieceName, i, rookRecords, bishopRecords, subRecord)
                    control[i] = 'relative'
                    explored = True
                    break
#END THE CHECK FOR LOCATION

#WRITE TO THE CORRECT RECORDS
def write_to_records(pieceName, i, rookRecords, bishopRecords, subRecord):
    if pieceName[i] == 'rook':
        rookRecords[i] += subRecord        
    elif pieceName[i] == 'bishop':
        if i == 8:
            bishopRecords[0] += subRecord  
        elif i == 9:
            bishopRecords[1] += subRecord                        
        elif i == 10:
            bishopRecords[2] += subRecord            
        elif i == 11:
            bishopRecords[3] += subRecord                        
        elif i == 12:
            bishopRecords[4] += subRecord                        
        elif i == 13:
            bishopRecords[5] += subRecord                       
        elif i == 14:
            bishopRecords[6] += subRecord            
        elif i == 15:
            bishopRecords[7] += subRecord                         
#END WRITING TO THE CORRECT RECORDS

#CHECK THE STATUS AND PIECE THAT HAS A RECORD THAT NEEDS TO BE STORED
def check_records(i, pieceName, rookRecords, completeRookRecords, bishopRecords, completeBishopRecords):
    if pieceName[i] == 'rook':
        if rookRecords[i] != '':
            completeRookRecords.append(rookRecords[i])
            rookRecords[i] = ''
    elif pieceName[i] == 'bishop':
        if i == 8:
            if bishopRecords[0] != '':
                completeBishopRecords.append(bishopRecords[0])
                bishopRecords[0] = ''                  
        elif i == 9:
            if bishopRecords[1] != '':
                completeBishopRecords.append(bishopRecords[1])
                bishopRecords[1] = ''
        elif i == 10:
            if bishopRecords[2] != '':
                completeBishopRecords.append(bishopRecords[2])
                bishopRecords[2] = ''
        elif i == 11:
            if bishopRecords[3] != '':
                completeBishopRecords.append(bishopRecords[3])
                bishopRecords[3] = ''
        elif i == 12:
            if bishopRecords[4] != '':
                completeBishopRecords.append(bishopRecords[4])
                bishopRecords[4] = ''
        elif i == 13:
            if bishopRecords[5] != '':
                completeBishopRecords.append(bishopRecords[5])
                bishopRecords[5] = ''
        elif i == 14:
            if bishopRecords[6] != '':
                completeBishopRecords.append(bishopRecords[6])
                bishopRecords[6] = ''
        elif i == 15:
            if bishopRecords[7] != '':
                completeBishopRecords.append(bishopRecords[7])
                bishopRecords[7] = ''

#END RECORD STATUS CHECK

#ESTABLISH THE RELATIVE DIRECTION OF AN AGENT
def establish_relative_front(i, forward, relativeDirection, relativeFront):
    if forward[i] == 0:
        relativeDirection[0] = 3
        relativeDirection[1] = 0
        relativeDirection[2] = 1
        relativeFront[i] = relativeDirection[1]
    elif forward[i] == 1:
        relativeDirection[0] = 0
        relativeDirection[1] = 1
        relativeDirection[2] = 2
        relativeFront[i] = relativeDirection[1]
    elif forward[i] == 2:
        relativeDirection[0] = 1
        relativeDirection[1] = 2
        relativeDirection[2] = 3
        relativeFront[i] = relativeDirection[1]
    elif forward[i] == 3:
        relativeDirection[0] = 2
        relativeDirection[1] = 3
        relativeDirection[2] = 0
        relativeFront[i] = relativeDirection[1]
    else:
        print('Something went wrong finding the relative front')
#END ESTABLISHING THE RELATIVE DIRECTION OF AN AGENT

#STANDARD MOVEMENT
def standard_move(i, x, y, imageList, exploration, pieceLoc, forward, directionControl, fourStandard, pieceName):
    matchFound = False
    if pieceName[i] == 'rook':
        rook_four_move_opt(i, fourStandard, pieceLoc, exploration)
    elif pieceName[i] == 'bishop':
        bishop_four_move_opt(i, fourStandard, pieceLoc, exploration)
    while matchFound == False:
        for f in range(4):
            x2 = fourStandard[f][0]
            y2 = fourStandard[f][1]
            if x2 != 2001 and y2 != 2001:
                if imageList[y2][x2] == '1' and exploration[y2][x2] == 'BU':
                    pieceLoc[i][0] = x2
                    pieceLoc[i][1] = y2
                    if f == 0:
                        #THEN ROOK MOVED UP
                        forward[i] = 0
                    elif f == 1:
                        #THEN ROOK MOVED RIGHT
                        forward[i] = 1
                    elif f == 2:
                        #THEN ROOK MOVED DOWN
                        forward[i] = 2
                    elif f == 3:
                        #THEN ROOK MOVED LEFT
                        forward[i] = 3
                    matchFound = True
                    break
        if matchFound == True:
            break
        elif matchFound == False:
            ranNum = random.randint(0, 3)
            pieceLoc[i][0] = fourStandard[ranNum][0]
            pieceLoc[i][1] = fourStandard[ranNum][1]
            if fourStandard[ranNum][0] == 2001 and fourStandard[ranNum][1] == 2001:
                while fourStandard[ranNum][0] == 2001 and fourStandard[ranNum][1] == 2001:
                    ranNum = random.randint(0, 3)
                    pieceLoc[i][0] = fourStandard[ranNum][0]
                    pieceLoc[i][1] = fourStandard[ranNum][1]                    
            x = pieceLoc[i][0]
            y = pieceLoc[i][1]
            if ranNum == 0:
               #THEN ROOK MOVED UP
               forward[i] = 0
            elif ranNum == 1:
               #THEN ROOK MOVED RIGHT
               forward[i] = 1
            elif ranNum == 2:
               #THEN ROOK MOVED DOWN
               forward[i] = 2
            elif ranNum == 3:
               #THEN ROOK MOVED LEFT
               forward[i] = 3
            matchFound = True
            break
#END STANDARD MOVEMENT

#RELATIVE MOVEMENT
def relative_move(i, x, y, threeRelative, imageList, exploration, pieceLoc,relativeDirection, relativeFront, forward, relativeForward, directionControl, pieceName):
    matchFound = False
    if pieceName[i] == 'rook':
        rook_three_move_opt(i, threeRelative, pieceLoc, exploration, relativeDirection)
    elif pieceName[i] == 'bishop':
        bishop_three_move_opt(i, threeRelative, pieceLoc, exploration, relativeDirection)
    while matchFound == False:
        for f in range(3):
            x2 = threeRelative[f][0]
            y2 = threeRelative[f][1]
            if x2 != 2001 and y2 != 2001:
                if imageList[y2][x2] == '1' and exploration[y2][x2] == 'BU' and relativeFront[i] == relativeDirection[f]:
                    pieceLoc[i][0] = x2
                    pieceLoc[i][1] = y2
                    relativeForward[i] = 0
                    forward[i] = relativeDirection[f]
                    matchFound = True
                    break
        if matchFound == True:
            break
        elif matchFound == False:
            for f in range(3):
                x2 = threeRelative[f][0]
                y2 = threeRelative[f][1]
                if x2 != 2001 and y2 != 2001:
                    if imageList[y2][x2] == '1' and exploration[y2][x2] == 'BU':
                        pieceLoc[i][0] = x2
                        pieceLoc[i][1] = y2
                        if relativeFront[i] == relativeDirection[f]:
                            relativeForward[i] = 0
                            forward[i] = relativeDirection[f]
                        elif relativeDirection[f] == relativeDirection[0]:
                            relativeForward[i] = 2
                            forward[i] = relativeDirection[f]
                        elif relativeDirection[f] == relativeDirection[2]:
                            relativeForward[i] = 1
                            forward[i] = relativeDirection[f]
                        matchFound = True
                        break
        if matchFound == True:
            break
        elif matchFound == False:
            ranNum = random.randint(0, 2)
            pieceLoc[i][0] = threeRelative[ranNum][0]
            pieceLoc[i][1] = threeRelative[ranNum][1]
            if threeRelative[ranNum][0] == 2001 and threeRelative[ranNum][1] == 2001:
                while threeRelative[ranNum][0] == 2001 and threeRelative[ranNum][1] == 2001:
                    ranNum = random.randint(0, 2)
                    pieceLoc[i][0] = threeRelative[ranNum][0]
                    pieceLoc[i][1] = threeRelative[ranNum][1]
            if relativeFront[i] == relativeDirection[ranNum]:
                relativeForward[i] = 0
                forward[i] = relativeDirection[ranNum]
            elif relativeDirection[ranNum] == relativeDirection[0]:
                relativeForward[i] = 2
                forward[i] = relativeDirection[f]
            elif relativeDirection[f] == relativeDirection[2]:
                relativeForward[i] = 1
                forward[i] = relativeDirection[f]
            matchFound = True
            break
#END RELATIVE MOVEMENT

#GET THE FOUR POSSIBLE MOVE LOCATIONS FOR STANDARD ROOK
def rook_four_move_opt(i, fourStandard, pieceLoc, exploration):
    j = pieceLoc[i][0]
    k = pieceLoc[i][1]

    for f in range(4):
        if f == 0:
            #GET UP LOCATION
            if k - 1 >= 0:
                fourStandard[f][0] = j
                fourStandard[f][1] = k - 1
            else:
                fourStandard[f][0] = 2001
                fourStandard[f][1] = 2001
        elif f == 1:
            #GET RIGHT LOCATION
            if j + 1 < len(exploration[0]):
                fourStandard[f][0] = j + 1
                fourStandard[f][1] = k
            else:
                fourStandard[f][0] = 2001
                fourStandard[f][1] = 2001
        elif f == 2:
            #GET DOWN LOCATION
            if k + 1 < len(exploration):
                fourStandard[f][0] = j
                fourStandard[f][1] = k + 1
            else:
                fourStandard[f][0] = 2001
                fourStandard[f][1] = 2001
        elif f == 3:
            #GET LEFT POSITION
            if j - 1 >= 0:
                fourStandard[f][0] = j - 1 
                fourStandard[f][1] = k
            else:
                fourStandard[f][0] = 2001
                fourStandard[f][1] = 2001
        else:
            print('There was an unexpected error')
#END GETTING THE POSSIBLE ROOK MOVE LOCATIONS

#GET THE THREE POSSIBLE MOVE LOCATIONS FOR RELATIVE ROOK
def rook_three_move_opt(i, threeRelative, pieceLoc, exploration, relativeDirection):
    j = pieceLoc[i][0]
    k = pieceLoc[i][1]
    for f in range(3):
        if relativeDirection[f] == 0:
            #THEN RELATIVE COLLECT UP
            if k - 1 >= 0:
                threeRelative[f][0] = j
                threeRelative[f][1] = k - 1
            else:
                threeRelative[f][0] = 2001
                threeRelative[f][1] = 2001
        elif relativeDirection[f] == 1:
            #THEN RELATIVE COLLECT RIGHT
            if j + 1 < len(exploration[0]):
                threeRelative[f][0] = j + 1
                threeRelative[f][1] = k
            else:
                threeRelative[f][0] = 2001
                threeRelative[f][1] = 2001
        elif relativeDirection[f] == 2:
            #THEN RELATIVE COLLECT DOWN
            if k + 1 < len(exploration):
                threeRelative[f][0] = j
                threeRelative[f][1] = k + 1
            else:
                threeRelative[f][0] = 2001
                threeRelative[f][1] = 2001
        elif relativeDirection[f] == 3:
            #THEN RELATIVE COLLECT LEFT
            if j - 1 >= 0:
                threeRelative[f][0] = j - 1
                threeRelative[f][1] = k
            else:
                threeRelative[f][0] = 2001
                threeRelative[f][1] = 2001
        else:
            print('There is an issue in getting the relative directions')
#END GETTING THE POSSIBLE ROOK RELATIVE LOCATIONS

#GET THE FOUR POSSIBLE MOVE LOCATIONS FOR STANDARD BISHOP
def bishop_four_move_opt(i, fourStandard, pieceLoc, exploration):
    j = pieceLoc[i][0]
    k = pieceLoc[i][1]

    for f in range(4):
        if f == 0:
            #GET UP-RIGHT LOCATION
            if j + 1 < len(exploration[0]) and k - 1 >= 0:
                fourStandard[f][0] = j + 1
                fourStandard[f][1] = k - 1
            else:
                fourStandard[f][0] = 2001
                fourStandard[f][1] = 2001
        elif f == 1:
            #GET DOWN-RIGHT LOCATION
            if j + 1 < len(exploration[0]) and k + 1 < len(exploration):
                fourStandard[f][0] = j + 1
                fourStandard[f][1] = k + 1
            else:
                fourStandard[f][0] = 2001
                fourStandard[f][1] = 2001
        elif f == 2:
            #GET DOWN-LEFT LOCATION
            if j - 1 >= 0 and k + 1 < len(exploration):
                fourStandard[f][0] = j - 1
                fourStandard[f][1] = k + 1
            else:
                fourStandard[f][0] = 2001
                fourStandard[f][1] = 2001
        elif f == 3:
            #GET UP-LEFT POSITION
            if j - 1 >= 0 and k - 1 >= 0:
                fourStandard[f][0] = j - 1 
                fourStandard[f][1] = k - 1
            else:
                fourStandard[f][0] = 2001
                fourStandard[f][1] = 2001
        else:
            print('There was an unexpected error')
#END GETTING THE POSSILE BISHOP MOVE LOCATIONS

#GET THE THREE POSSIBLE MOVE OPTIONS FOR RELATIVE BISHOP
def bishop_three_move_opt(i, threeRelative, pieceLoc, exploration, relativeDirection):
    j = pieceLoc[i][0]
    k = pieceLoc[i][1]
    for f in range(3):
        if relativeDirection[f] == 0:
            #THEN RELATIVE COLLECT UP-RIGHT
            if j + 1 < len(exploration[0]) and k - 1 >= 0:
                threeRelative[f][0] = j + 1
                threeRelative[f][1] = k - 1
            else:
                threeRelative[f][0] = 2001
                threeRelative[f][1] = 2001
        elif relativeDirection[f] == 1:
            #THEN RELATIVE COLLECT DOWN-RIGHT
            if j + 1 < len(exploration[0]) and k + 1 < len(exploration):
                threeRelative[f][0] = j + 1
                threeRelative[f][1] = k + 1
            else:
                threeRelative[f][0] = 2001
                threeRelative[f][1] = 2001
        elif relativeDirection[f] == 2:
            #THEN RELATIVE COLLECT DOWN-LEFT
            if j - 1 >= 0 and k + 1 < len(exploration):
                threeRelative[f][0] = j - 1
                threeRelative[f][1] = k + 1
            else:
                threeRelative[f][0] = 2001
                threeRelative[f][1] = 2001
        elif relativeDirection[f] == 3:
            #THEN RELATIVE COLLECT LEFT
            if j - 1 >= 0 and k - 1 >= 0:
                threeRelative[f][0] = j - 1
                threeRelative[f][1] = k - 1
            else:
                threeRelative[f][0] = 2001
                threeRelative[f][1] = 2001
        else:
            print('There is an issue in getting the relative directions')
#END GETTING THE POSSIBLE BISHOP RELATIVE LOCATIONS

#WRITE VARIOUS COORDINATES AND DIRECTIONS TO TEXT FILES
def write_to_files():
    pass
#END WRITE TO TEXT FILES

#RECREATE THE IMAGE USING THE STRINGS COLLECTED BY THE PIECES
def recreate_image(completeRookRecords, completeBishopRecords, xValue, yValue):
    newImage = [[0 for x in range(xValue)] for y in range(yValue)]
    segment = ''
    counter, x, y, lastDirection = 0, 0, 0, 0
    threeRelative = [[0 for x in range(2)]for y in range(3)]
    relativeOptions = [0, 0, 0]
    #BREAK DOWN THE ROOK RECORDS FIRST
    for g in range(len(completeRookRecords)):
        counter = 0
        segment = str(completeRookRecords[g])
        while counter < len(completeRookRecords[g]):
            #GET COORDINATE
            if counter == 0:                
                x = int(segment[counter:10], 2)                
                counter += 10                
            if counter == 10:
                y = int(segment[counter:counter+10], 2)
                newImage[y][x] = 1
                counter += 10
            if counter >= len(completeRookRecords[g]):
                break
            #GET FIRST DIRECTION
            if counter == 20:
                if segment[counter:counter+3] == '000':
                    #UP
                    y = y - 1
                    newImage[y][x] = 1
                    lastDirection = 0
                elif segment[counter:counter+3] == '001':
                    #RIGHT
                    x = x + 1
                    newImage[y][x] = 1
                    lastDirection = 1
                elif segment[counter:counter+3] == '010':
                    #DOWN
                    y = y + 1
                    newImage[y][x] = 1
                    lastDirection = 2
                elif segment[counter:counter+3] == '011':
                    #LEFT
                    x = x - 1
                    newImage[y][x] = 1
                    lastDirection = 3
                counter += 3
            if counter >= len(completeRookRecords[g]):
                break
            if counter >= 23:
                while counter != len(completeRookRecords[g]):
                    if counter == len(completeRookRecords[g]):
                        break
                    if lastDirection == 0:
                         relativeOptions[0] = 3
                         relativeOptions[1] = 0
                         relativeOptions[2] = 1
                    elif lastDirection == 1:
                        relativeOptions[0] = 0
                        relativeOptions[1] = 1
                        relativeOptions[2] = 2
                    elif lastDirection == 2:
                        relativeOptions[0] = 1
                        relativeOptions[1] = 2
                        relativeOptions[2] = 3
                    elif lastDirection == 3:
                        relativeOptions[0] = 2
                        relativeOptions[1] = 3
                        relativeOptions[2] = 0
                    for f in range(3):
                        if relativeOptions[f] == 0:
                            #UP
                            threeRelative[f][0] = x
                            threeRelative[f][1] = y - 1
                        elif relativeOptions[f] == 1:
                            #RIGHT
                            threeRelative[f][0] = x + 1
                            threeRelative[f][1] = y
                        elif relativeOptions[f] == 2:
                            #DOWN
                            threeRelative[f][0] = x
                            threeRelative[f][1] = y + 1
                        elif relativeOptions[f] == 3:
                            #LEFT
                            threeRelative[f][0] = x - 1
                            threeRelative[f][1] = y
                    if counter >= len(completeRookRecords[g]):
                        break
                    if segment[counter:counter+3] == '000':
                        x = threeRelative[1][0]
                        y = threeRelative[1][1]
                        newImage[y][x] = 1
                        lastDirection = relativeOptions[1]
                    elif segment[counter:counter+3] == '001':                        
                        x = threeRelative[2][0]
                        y = threeRelative[2][1]
                        newImage[y][x] = 1
                        lastDirection = relativeOptions[2]
                    elif segment[counter:counter+3] == '010':                        
                        x = threeRelative[0][0]
                        y = threeRelative[0][1]
                        newImage[y][x] = 1
                        lastDirection = relativeOptions[0]                 
                    counter += 3
                    if counter >= len(completeRookRecords[g]):
                        break
        counter = 0
    #END ROOK RECREATE

    #BEGIN BISHOP RECORD BREAK DOWN
    for g in range(len(completeBishopRecords)):
        counter = 0
        segment = str(completeBishopRecords[g])
        while counter < len(completeBishopRecords[g]):
            #GET COORDINATE
            if counter == 0:                
                x = int(segment[counter:10], 2)                
                counter += 10                
            if counter == 10:
                y = int(segment[counter:counter+10], 2)
                newImage[y][x] = 1
                counter += 10
            if counter >= len(completeBishopRecords[g]):
                break
            #GET FIRST DIRECTION
            if counter == 20:
                if segment[counter:counter+3] == '000':
                    #UP-RIGHT
                    x = x + 1
                    y = y - 1
                    newImage[y][x] = 1
                    lastDirection = 0
                elif segment[counter:counter+3] == '001':
                    #DOWN-RIGHT
                    x = x + 1
                    y = y + 1
                    newImage[y][x] = 1
                    lastDirection = 1
                elif segment[counter:counter+3] == '010':
                    #DOWN-LEFT
                    x = x - 1
                    y = y + 1
                    newImage[y][x] = 1
                    lastDirection = 2
                elif segment[counter:counter+3] == '011':
                    #UP-LEFT
                    x = x - 1
                    y = y - 1
                    newImage[y][x] = 1
                    lastDirection = 3
                counter += 3
            if counter >= len(completeBishopRecords[g]):
                break
            if counter >= 23:
                while counter != len(completeBishopRecords[g]):
                    if counter == len(completeBishopRecords[g]):
                        break
                    if lastDirection == 0:
                         relativeOptions[0] = 3
                         relativeOptions[1] = 0
                         relativeOptions[2] = 1
                    elif lastDirection == 1:
                        relativeOptions[0] = 0
                        relativeOptions[1] = 1
                        relativeOptions[2] = 2
                    elif lastDirection == 2:
                        relativeOptions[0] = 1
                        relativeOptions[1] = 2
                        relativeOptions[2] = 3
                    elif lastDirection == 3:
                        relativeOptions[0] = 2
                        relativeOptions[1] = 3
                        relativeOptions[2] = 0
                    for f in range(3):
                        if relativeOptions[f] == 0:
                            #UP-RIGHT
                            threeRelative[f][0] = x + 1
                            threeRelative[f][1] = y - 1
                        elif relativeOptions[f] == 1:
                            #DOWN-RIGHT
                            threeRelative[f][0] = x + 1
                            threeRelative[f][1] = y + 1
                        elif relativeOptions[f] == 2:
                            #DOWN-LEFT
                            threeRelative[f][0] = x - 1
                            threeRelative[f][1] = y + 1
                        elif relativeOptions[f] == 3:
                            #UP-LEFT
                            threeRelative[f][0] = x - 1
                            threeRelative[f][1] = y - 1
                    if counter >= len(completeBishopRecords[g]):
                        break
                    if segment[counter:counter+3] == '000':
                        x = threeRelative[1][0]
                        y = threeRelative[1][1]
                        newImage[y][x] = 1
                        lastDirection = relativeOptions[1]
                    elif segment[counter:counter+3] == '001':                        
                        x = threeRelative[2][0]
                        y = threeRelative[2][1]
                        newImage[y][x] = 1
                        lastDirection = relativeOptions[2]
                    elif segment[counter:counter+3] == '010':                        
                        x = threeRelative[0][0]
                        y = threeRelative[0][1]
                        newImage[y][x] = 1
                        lastDirection = relativeOptions[0]                 
                    counter += 3
                    if counter >= len(completeBishopRecords[g]):
                        break
        counter = 0
    #END BISHOP RECREATE
    file = open('..\\images\\testOutput.csv', 'w', newline='')
    csv_file = csv.writer(file)
    csv_file.writerows(newImage)

#END IMAGE RECREATION

if __name__ == '__main__': main()