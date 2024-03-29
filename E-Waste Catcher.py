import os, random 
from pygame import *
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20) 
init()

SIZE = width, height = 1000, 700 #the size of the screen
screen = display.set_mode(SIZE)
myClock = time.Clock()

BLACK = (0, 0, 0) #colors
GREY = (64, 64, 64)
POINTSCOLOR = (100, 149, 237)

STATE_MENU = 0 #6 states of the game
STATE_GAME = 1
STATE_HELP = 2
STATE_QUIT = 3
STATE_OVER = 4
STATE_PAUSE = 5
state = STATE_MENU

fontPoints = font.SysFont("Comic Sans MS", 55) #fonts
fontItems = font.SysFont("Comic Sans MS", 30)
fontScores = font.SysFont("Comic Sans MS", 20)
fontItems.set_bold(True) #bolds some of the fonts
fontPoints.set_bold(True)

menuBackground = image.load("menubackground.png") #loading a bunch of images
help = image.load("help.png")
gameBackground = image.load("gameBackground.png")
grey = image.load("grey.png")
pause = image.load("pause.png")
gameOver = image.load("gameover.png")
bin = image.load("bin.png")
bomb = image.load("bomb.png")
dvd = image.load("dvd.png")
phone = image.load("phone.png")
printer = image.load("printer.png")
checkmark = image.load("checkmark.png")
border = image.load("border.png")
border2 = image.load("border2.png")
border3 = image.load("border3.png")
heart = image.load("heart.png")

ding = mixer.Sound("ding.wav") #some sound effects
ding.set_volume(0.1)
bombSound = mixer.Sound("bombsound.wav")
bombSound.set_volume(0.2)
gameOverSound = mixer.Sound("gameover.wav")
gameOverSound.set_volume(0.1)
levelUp = mixer.Sound("levelup.wav")
loseLife = mixer.Sound("loselife.wav")
mixer.music.load("song.wav")

menuBackground = transform.scale(menuBackground, (width, height)) #transforming the images to be the desired size
help =  transform.scale(help, (width, height))
gameBackground = transform.scale(gameBackground, (width, height))
grey = transform.scale(grey, (width, height))
pause = transform.scale(pause, (379, 534))
gameOver = transform.scale(gameOver, (width, height))
border = transform.scale(border, (88, 60))
border2 = transform.scale(border2, (155, 68))
border3 = transform.scale(border3, (207, 72))
bin = transform.scale(bin, (150, 75))
objectLen = 100 #the width of the objects
listHeights = [84, 89, 98, 95] #the list of the objects' heights
bomb = transform.scale(bomb, (objectLen, listHeights[0]))
dvd = transform.scale(dvd, (objectLen, listHeights[1]))
phone = transform.scale(phone, (objectLen, listHeights[2]))
printer = transform.scale(printer, (objectLen, listHeights[3]))
checkmark = transform.scale(checkmark, (30, 31))
heart = transform.scale(heart, (32, 30))

leftRect = Rect(37, 23, 90, 62) #Rects for some of the buttons
middleRect = Rect(442, 130, 157, 70)
rightRect = Rect(880, 23, 93, 60)

difficulty = False #the user has not selected a difficulty
changeScore = False #the data file score has not been updated
greyBack = False #the grey background for pause state has not been applied
reset = False #the game has not been reset

def scoreboard(points): #the following function checks if the user achieved a new high score
    highscores = open("highscores.dat", "r") #reads from the file
    firstList = []
    secondList = []
    newScore = False #points is not greater than any of the high scores
    while True: #goes through the file one line at a time
        score = highscores.readline()        
        if score == "": #if the line is enpty, break out of the loop
            break            
        score = score.rstrip("\n") #removes the \n at the end of each line  
        if points <= int(score): #if the points are not greater than the high score, append them to the first list
            firstList.append(int(score))
        else: #if it is greater, append it to the second list
            if newScore == False: 
                secondList.append(points)
            secondList.append(int(score))
            newScore = True            
    highscores.close() #closes the file so it can run properly next time
    if newScore == True: #if the points is greater than one of the high scores
        highscores = open("highscores.dat", "w") #wipes the file data so we can update it
        for i in firstList: #writes the first list first
            highscores.write(str(i) + "\n")
        for i in range(len(secondList)-1): #and then the second list. The minus 1 is so that only 5 scores are written
            highscores.write(str(secondList[i]) + "\n")
        highscores.close() #closes the file
    changeScore = True #the scoreboard has been updated        
    return changeScore
    
def gameReset(): #resets the game (points set to zero, etc.)
    global itemsCaught, xCoords, yCoords, points, lives, speedIncrease
    points = 0
    yCoords = 0
    itemsCaught = 0
    speedIncrease = 0
    lives = 3    
    xCoords = random.randint(0, width - objectLen)    

def itemReset(): #respawns a new item
    global xCoords, yCoords, item
    xCoords = random.randint(0, width - objectLen)                
    yCoords = 0
    item = random.choice(newObjectList)

def collisionButtons(states, borderList, rectList): #if the user has pressed one of the buttons on screen
    global state
    for length in range(len(rectList)): #goes through the rects one at a time to see if the user hovers the mouse over it
        rect = rectList[length]
        if rect.collidepoint(x, y): #if the mouse is on top of a button, blit an image of a black border around it
            screen.blit(borderList[length], Rect(rectList[length]))            
            if button == 1: #if they click the button, change the state accordingly
                state = states[length]

def checkDifficulty(): #the following function checks which difficulty the user has selected
    global speed, difficulty, xValue, sPoints
    easyRect = Rect(358, 210, 65, 29) #the borders surrounding the difficulties
    mediumRect = Rect(469, 210, 100, 29)
    hardRect = Rect(623, 210, 60, 29)
    listPosition = [358-30, 469-30, 623-30] #the x position of the checkmark which I will draw next to the difficulty the user selects
    difficultyRects = [easyRect, mediumRect, hardRect] #put them in a list
    speeds =[20, 25, 30] #the speeds of each of the difficulties, also in a list
    speedPoints = [0, 20, 40] #more points for the higher difficulties
    for i in range(len(difficultyRects)): #goes through the list of difficulties to see if the user mouse hovers over them 
        rect = difficultyRects[i]
        if rect.collidepoint(x, y): #if the user mouse hovers over it, draw a checkmark to the left of it
            screen.blit(checkmark, (listPosition[i], 210))
            if button == 1: #if they click the difficulty, set the speed, and return the x-coords of where to draw the checkmark
                speed = speeds[i]
                difficulty = True #a difficulty has been selected
                xValue = listPosition[i]
                sPoints = speedPoints[i]

def checkPoints(item, sPoints): #check how many points the user has
    global points, itemsCaught, speedIncrease
    if item == bomb: #if the user catches a bomb
        points -= 500
        bombSound.play()
    else: #if the user catches anything other than a bomb
        points += 100 
        points += sPoints #sPoints is the extra points they get for higher difficulties
        ding.play()
        itemsCaught += 1
    if itemsCaught%10 == 0 and itemsCaught != 0: #if the amount of items caught divide by 10 has remainder 0 (every 10 items)
        speedIncrease += 2
        levelUp.play()

def drawMenu(): #state menu
    global reset, state, speed, difficulty, xValue, sPoints
    mixer.music.stop() #stops the music (if it was playing before) 
    screen.blit(menuBackground, (0 ,0, width, height)) #blit the menu image
    highscores = open("highscores.dat", "r") #opens the high scores (to display them on screen)
    newWidth = 0 #the height of the text will increase by this value, to make sure they are not on top of each other
    while True: 
        scores = highscores.readline() #reads the high scores, one line at a time
        if scores == "": #if the line is empty, break out of the loop
            break
        scores = scores.rstrip("\n") #remove the \n at the end of each line
        textScores = fontScores.render(str(scores), 1, GREY) #text for the points
        scoreWidth, scoreHeight = textScores.get_width(), textScores.get_height() #gets the width and height of the scores
        screen.blit(textScores, (width-scoreWidth-394, 340+newWidth, scoreWidth, scoreHeight)) #displays the scores within the nice box I created
        newWidth += scoreHeight #this value increases by the height of the score each time so that the texts aren't displayed on top of each other
    highscores.close() #closes the file 
    rectList = [leftRect, middleRect, rightRect]
    states = [STATE_HELP, STATE_GAME, STATE_QUIT]
    borderList = [border, border2, border]
    collisionButtons(states, borderList, rectList) #checks if buttons were clicked    
    checkDifficulty() #checks the difficulty
    if difficulty == True: #if a difficulty has been selected, blit a checkmark next to it
        screen.blit(checkmark, (xValue, 210))
    else: #if not then blit a checkmark next to the easy level. This makes sure a level is selected at the start
        screen.blit(checkmark, (328, 210))
    reset = False

def drawGame(): #the game!
    global itemsCaught, xCoords, yCoords, points, speedIncrease, state, item, speed, lives, sPoints, reset, changeScore
    if reset == False: #resets the game every time it is entered from another state
        reset = True
        mixer.music.play(-1)
        gameReset()
    mixer.music.unpause() #unpauses the game (if it was paused)
    binX = x-75
    if binX+150 >= width: #this makes sure the bin does not go off the screen
        binX = width-150
    if binX <= 0:
        binX = 0
    screen.blit(gameBackground, (0 ,0, width, height)) #blits the game background onto the screen
    binRect = screen.blit(bin, Rect(binX, 625, 150, 75)) 
    textPoints = fontPoints.render(str(points) + " pts", 1, POINTSCOLOR) #text for the points
    textWidth, textHeight = textPoints.get_width(), textPoints.get_height()    
    screen.blit(textPoints, (width-textWidth, 80, textWidth, textHeight))
    itemsText = fontItems.render("Items Caught: " + str(itemsCaught), 1, POINTSCOLOR)
    itemsWidth, itemsHeight = itemsText.get_width(), itemsText.get_height()
    screen.blit(itemsText, (width-itemsWidth, 155, itemsWidth, itemsHeight))    
    lengthHeart = 0 #this value increases so that the hearts are not drawn on top of each other
    for life in range(lives): #blits the number of hearts onto the screen
        screen.blit(heart, (36+lengthHeart, 92, 32, 30)) 
        lengthHeart += 32 
    rectList = [leftRect, rightRect]
    borderList = [border, border]
    states = [STATE_PAUSE, STATE_QUIT]
    position = objectList.index(item)
    objectHeight = listHeights[position]
    bombRect = Rect(xCoords, yCoords, objectLen, listHeights[0]) #the rects of the objects, I made them have the same width, but different heights
    dvdRect = Rect(xCoords, yCoords, objectLen, listHeights[1])
    phoneRect = Rect(xCoords, yCoords, objectLen, listHeights[2])
    printerRect = Rect(xCoords, yCoords, objectLen, listHeights[3])    
    objectRects = [bombRect, dvdRect, phoneRect, printerRect]
    itemRect = objectRects[position]
    if binRect.colliderect(itemRect): #if the user catches an item
        checkPoints(item, sPoints)
        itemReset()  
    else:
        screen.blit(item, (xCoords, yCoords, objectLen, 250)) #blits the item onto the screen
    collisionButtons(states, borderList, rectList)      
    if yCoords >= height: #if the item hits the ground
        if item != bomb: #if the item that fell to the ground is not a bomb, deduct a life
            lives -= 1 
            loseLife.play()
        xCoords = random.randint(0, width - objectLen)                
        yCoords = 0
        item = random.choice(newObjectList)
    if lives == 0: #if the user runs out of lives, display the game over sceen
        state = STATE_OVER
    if button == 3: #if the user clicks the right mouse button, pause the game
        state = STATE_PAUSE
    changeScore = False
    yCoords += speed + speedIncrease #makes the objects fall down    

def drawHelp(): #simple help screen, did all the images and stuff on MS Paint to save time
    global state
    screen.blit(help, (0 ,0, width, height))        
    rectList = [leftRect, rightRect]
    borderList = [border, border]
    states = [STATE_MENU, STATE_QUIT]
    collisionButtons(states, borderList, rectList)

def drawGameOver(): #game over
    global state, points, changeScore, reset
    mixer.music.stop() #stops the mmusic
    screen.blit(gameOver, (0, 0, width, height))
    textPoints = fontPoints.render(str(points) + " pts", 1, BLACK) #text for the points
    textWidth, textHeight = textPoints.get_width(), textPoints.get_height() #this gets the width and height of the text
    screen.blit(textPoints, (316+(368-textWidth)//2, 300, textWidth, textHeight)) #this makes sure that the text is centered
    states = [STATE_MENU, STATE_GAME, STATE_QUIT]
    leftSideRect = Rect(372, 408, 88, 60)
    rightSideRect = Rect(540, 408, 88, 60)
    borderList = [border, border, border]
    rectList = [leftSideRect, rightSideRect, rightRect]
    collisionButtons(states, borderList, rectList)
    if changeScore == False: #updates the high scores data file
        gameOverSound.play()
        changeScore = scoreboard(points)
    reset = False

def drawPause():
    global state, greyBack
    mixer.music.pause()    
    if greyBack == False: #I added a semi-transparent grey background. This makes sure it is only applied once. (If it is applied more than once, the screen gets darker every time)
        screen.blit(grey, (0, 0, width, height))
        greyBack = True
    screen.blit(pause, (310, 80, 379, 534))
    upRect = Rect(396, 150, 205, 71)
    midRect = Rect(397, 307, 205, 71)
    downRect = Rect(397, 465, 205, 71)
    states = [STATE_GAME, STATE_MENU, STATE_QUIT]
    borderList = [border3, border3, border3]
    rectList = [upRect, midRect, downRect]
    collisionButtons(states, borderList, rectList)     
    if state != STATE_PAUSE: #if the state is changed, the grey background is set to false again
        greyBack = False        

running = True #setting up some stuff
xValue = 0
xCoords = random.randint(0, width - objectLen)    
yCoords = 0
points = 0
itemsCaught = 0
sPoints = 0
speedIncrease = 0
lives = 3
speed = 20
objectList = [bomb, dvd, phone, printer]
newObjectList = [bomb, dvd, dvd, phone, phone, printer, printer] #this makes it so that the probability of a bomb dropping is half of the other items     
item = random.choice(newObjectList)

while running: #main game loop
    button = 0
    for e in event.get(): 
        if e.type == QUIT: 
            running = False
        if e.type == MOUSEBUTTONDOWN:
            x, y = e.pos
        if e.type == MOUSEBUTTONUP: #this makes it so that once the user lets go of the button, the effect of the button takes place 
            button = e.button            
        elif e.type == MOUSEMOTION:
            x, y = e.pos
            
    if state == STATE_MENU: #menu
        drawMenu()
    elif state == STATE_GAME: #game 
        drawGame()
    elif state == STATE_HELP: #help
        drawHelp()
    elif state == STATE_OVER: #game over
        drawGameOver()
    elif state == STATE_PAUSE: #pause
        drawPause()
    else:
        running = False
        
    display.flip()
    myClock.tick(60) #60 fps

quit() #quits 
