# Snake Game!

# Imports modules
import pygame
import sys
import random
import time


# Allows use to find the highscore.txt file from any directory
from pathlib import Path

check_errors = pygame.init()

# Checking if the check initialization errors has anything at all
if check_errors[1] > 0:
    print("(!) Had {0} initializing errors, exiting...".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialized!")
# (5,0)

# Setting up the screen for our game or play surface
playSurface = pygame.display.set_mode((720, 460))
pygame.display.set_caption("Snake game!")

# Separating the scoreboard

# Game layout dimensions
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 460
HUD_HEIGHT = 80

# Adding some color variables
red = pygame.Color(255, 0, 0) #game over
green = pygame.Color(0, 255, 0) #snake
black = pygame.Color(0, 0, 0) #score
white = pygame.Color(255, 255, 255) #background
brown = pygame.Color(165,42,42) #food
gold = pygame.Color(255, 215, 0)


# Frame controller or timer that runs in the background. Frames per second controller
fpsController = pygame.time.Clock()

# Creating variables for snake and food
# Snake position on the initial play. Where do you want the snake to start from
snakePos = [100, 100]
snakeBody = [[100, 100], [90, 100], [80, 100]]

# Food position
# foodPos = [
#     random.randrange(0, SCREEN_WIDTH // 10) * 10, 
#     random.randrange(HUD_HEIGHT // 10, SCREEN_HEIGHT // 10) * 10
#     ]
# foodPos = generateFood(snakeBody)
foodSpawn = True


# Direction
direction = "RIGHT"
changeto = direction

# Scoreboard
score = 0

highScoreFile = Path(__file__).resolve().parent / "highscore.txt"

try:
    with open(highScoreFile, "r") as file:
        highScore = int(file.read())
except (FileNotFoundError, ValueError):
    highScore = 0


# Setting the difficulty
difficulty = "MEDIUM"
difficultySpeeds = {
    "EASY": 10,
    "MEDIUM": 15,
    "HARD": 25
}



# ALL FUNCTIONS

# Game Over Function
def gameOver(level):
    # Creating the font
    myFont = pygame.font.SysFont('monaco', 72) #SysFont give you the name of the font as the first argument and the size as the second argument
    GOsurf = myFont.render('Game Over!', True, red) #now that we have the font we have to render it to a surface. We do that through the render function. This function needs three arguments (text, antialias can be a number or boolean, the color, background color default is none)
    GOrect = GOsurf.get_rect() #gets the rectangular component of the surface
    GOrect.midtop = (360, 100) #This is going to be a tuple and we have to specify the x and y coordinates. This needs to be divided by 2 of the surface for the x and the y coord will be much less
    playSurface.blit(GOsurf, GOrect)
    showScore(level=level, gameIsOver=True)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    # restartGame()
                    return "RESTART"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_m:
                    return "MENU"

        fpsController.tick(60)

        biFont = pygame.font.SysFont('monaco', 24) 
        RGsurf = biFont.render('Press R to Restart', True, black)
        RGrect = RGsurf.get_rect()
        RGrect.midtop = (360, 180)

        PEsurf = biFont.render('Press ESC to Quit', True, black)
        PErect = PEsurf.get_rect()
        PErect.midtop = (360, 220)

        MSurf = biFont.render('Press M for Main Menu', True, black)
        MRect = MSurf.get_rect()
        MRect.midtop = (360, 260)

        # Drawing the instructions
        playSurface.blit(RGsurf, RGrect)
        playSurface.blit(PEsurf, PErect)
        playSurface.blit(MSurf, MRect)

        # Updating the code
        pygame.display.flip()

        # mainMenu()

    
# Scoreboard function
def showScore(level=1, gameIsOver=False):
    # HUD for the scoreboard
    pygame.draw.rect(
        playSurface, 
        black, 
        pygame.Rect(0, 0,SCREEN_WIDTH, HUD_HEIGHT)
        )

    # Drawing the gold highligh
    if gameIsOver:
            pygame.draw.rect(
                playSurface,
                gold,
                pygame.Rect(25, 15, 150, 45)
            )

    # Changes the score color depending on whether the game is over
    scoreColor = black if gameIsOver else white

    sFont = pygame.font.SysFont('monaco', 24)
    # if gameIsOver:
    #     scoreColor = black
    # else:
    #     scoreColor = white
    Ssurf = sFont.render('Score: {0}'.format(score), True, scoreColor)
    Srect = Ssurf.get_rect()
    Srect.midtop = (100, 25)
    playSurface.blit(Ssurf, Srect)


    HSSurf = sFont.render('Highscore: {0}'.format(highScore), True, white)
    HSRect = HSSurf.get_rect()
    HSRect.midtop = (350, 25)
    playSurface.blit(HSSurf, HSRect)

    levelSurface = sFont.render ('Level: {0}'.format(level), True, white)
    levelRect = levelSurface.get_rect()
    levelRect.midtop = (600, 25)
    playSurface.blit(levelSurface, levelRect)

def youWin(level):
    winFont = pygame.font.SysFont('monaco', 72)
    winSurf = winFont.render("YOU WIN!", True, gold)
    winRect = winSurf.get_rect()
    winRect.midtop = (360, 100)

    playSurface.fill(black)
    
    RFont = pygame.font.SysFont('monaco', 24)
    RSurf = RFont.render("Press R to Restart", True, white)
    RRect = RSurf.get_rect()
    RRect.midtop = (360, 200)
    
            
    MSurf = RFont.render("Press M for Main Menu", True, white)
    MRect = MSurf.get_rect()
    MRect.midtop = (360, 240)
    
    QSurf = RFont.render("Press ESC to Quit", True, white)
    QRect = QSurf.get_rect()
    QRect.midtop = (360, 280)

    playSurface.blit(winSurf, winRect)
    playSurface.blit(RSurf, RRect)
    playSurface.blit(MSurf, MRect)
    playSurface.blit(QSurf, QRect)

    showScore(level=level)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
    
                if event.key == pygame.K_r:
                    # restartGame()
                    return "RESTART"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_m:
                    return "MENU"
        
        fpsController.tick(60)

        

#Main Menu Function 

def helpScreen():
    helpFont = pygame.font.SysFont('monaco', 40)
    instructionalFont = pygame.font.SysFont('monaco', 22)

    titleSurface = helpFont.render("HOW TO PLAY", True, green)
    titleRect = titleSurface.get_rect()
    titleRect.center = (360, 80)

    
    

    # Using a list to store multiple lines of text
    instructions = [
        "Use Arrow Keys or WASD to move",
        "Eat the food to grow and earn points",
        "Avoid walls and your own tail",
        "Press ESC to return to Menu"
    ]

    playSurface.fill(black)

    playSurface.blit(titleSurface, titleRect)
    

    for index, instructions in enumerate(instructions):
        instructionSurface = instructionalFont.render(
            instructions, True, white
        )

        instructionRect = instructionSurface.get_rect()
        instructionRect.center = (360, 160 + index *45)

        playSurface.blit(instructionSurface, instructionRect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

    
        fpsController.tick(60)

def settingsScreen():

    difficultyOptions = ["EASY", "MEDIUM", "HARD"]
    
    selectedDifficulty = difficultyOptions.index(difficulty)       

    settingsFont = pygame.font.SysFont('monaco', 40)
    optionFont = pygame.font.SysFont('monaco', 24)

    settingsSurf = settingsFont.render("SETTINGS", True, green)
    settingsRect = settingsSurf.get_rect()
    settingsRect.center = (360, 80)



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # This can be ran instead of doing them separately
                    return difficultyOptions[selectedDifficulty]
                    
                elif event.key == pygame.K_ESCAPE:
                    return

                elif event.key == pygame.K_DOWN:
                    selectedDifficulty = (selectedDifficulty + 1) % len(difficultyOptions)
                    # print("Selected:", difficultyOptions[selectedDifficulty])
                elif event.key == pygame.K_UP:
                    selectedDifficulty = (selectedDifficulty -1) % len(difficultyOptions)
                    # print("Selected:", difficultyOptions[selectedDifficulty])
        
        playSurface.fill(black)   
        playSurface.blit(settingsSurf, settingsRect)   

        # Highlight the selected difficulty
        for index, option in enumerate(difficultyOptions):
            if index == selectedDifficulty:
                textColor = green
            else:
                textColor = white

            optionSurface = optionFont.render(option, True, textColor)
            optionRect = optionSurface.get_rect()
            optionRect.center = (360, 180 + index * 50)

            playSurface.blit(optionSurface, optionRect)

        pygame.display.flip()
        fpsController.tick(60)

def mainMenu():

    # Global vaariables
    global difficulty

    # Creating the game menu
    menuFont = pygame.font.SysFont('monaco', 50)
    optionFont = pygame.font.SysFont('monaco', 24)

    titleSurface = menuFont.render("SNAKE GAME", True, green)
    titleRect = titleSurface.get_rect()
    titleRect.center = (360, 150)


    menuOptions = ["PLAY", "SETTINGS", "HELP", "QUIT"]
    selectedOption = 0

    while True:
        # Check keyboard input first
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    if menuOptions[selectedOption] == "PLAY":
                        return

                    elif menuOptions[selectedOption] == "SETTINGS":
                        chosenDifficulty = settingsScreen()

                        if chosenDifficulty is not None:
                            difficulty = chosenDifficulty

                        # print("Current difficulty", difficulty)

                    elif menuOptions[selectedOption] == "HELP":
                        helpScreen()

                    elif menuOptions[selectedOption] == "QUIT":
                        pygame.quit()
                        sys.exit()

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                elif event.key == pygame.K_DOWN:
                    selectedOption = (selectedOption + 1) % len(menuOptions)
                    # print("Selected:", menuOptions[selectedOption])
                elif event.key == pygame.K_UP:
                    selectedOption = (selectedOption -1) % len(menuOptions)
                    # print("Selected:", menuOptions[selectedOption])

        # Clear the screen
        playSurface.fill(black)

        # Draw the title
        playSurface.blit(titleSurface, titleRect)

        # Draw the menu options
        
    
    # Creating four separat text surfaces by using a for loop
        for index, option in enumerate(menuOptions):
            if index == selectedOption:
                textColor = green
            else:
                textColor = white

            optionSurface = optionFont.render(option, True, textColor)
            optionRect = optionSurface.get_rect()

            optionRect.center = (360, 220 + index * 45)

            playSurface.blit(optionSurface, optionRect)
    
        pygame.display.flip()
        fpsController.tick(60)

def generateFood(snakeBody):
        foodPos =[
            random.randrange(0, SCREEN_WIDTH // 10) * 10, 
            random.randrange(HUD_HEIGHT // 10, SCREEN_HEIGHT // 10) * 10
            ]
        while foodPos in snakeBody:
            foodPos =[
                random.randrange(0, SCREEN_WIDTH // 10) * 10, 
                random.randrange(HUD_HEIGHT // 10, SCREEN_HEIGHT // 10) * 10
                ]
        return foodPos

foodPos = generateFood(snakeBody)

def gameLoop():
    global changeto, direction, snakePos, snakeBody
    global foodPos, foodSpawn, score, highScore
    
    isPaused = False
 # The current level  divided by the score
    level = (score // 5) +1
   
    pauseFont = pygame.font.SysFont("Arial", 40)
    pauseText = pauseFont.render("PAUSED", True, red)
    pauseRect = pauseText.get_rect(center=(360, 230))

    totalSquares = (
    (SCREEN_WIDTH // 10) *
    ((SCREEN_HEIGHT - HUD_HEIGHT) // 10)
)

    while True:
        # Events are special occassions where things actually happen. Hit keys, clicks of mouse. 
        # Main Logic

        # Accepting the inputs to the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    changeto = 'RIGHT'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    changeto = 'LEFT'
                if event.key == pygame.K_UP or event.key == ord('w'):
                    changeto = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    changeto = 'DOWN'
                if event.key == pygame.K_p:
                     isPaused = not isPaused
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                
    
        # Validating the changes to our direction. Checking for the condition
        if changeto == 'RIGHT' and not direction == 'LEFT':
            direction = 'RIGHT'
        if changeto == 'LEFT' and not direction == 'RIGHT':
            direction = 'LEFT'
        if changeto == 'UP' and not direction == 'DOWN':
            direction = 'UP'
        if changeto == 'DOWN' and not direction == 'UP':
            direction = 'DOWN'
        

        if not isPaused:
        # Updating the snake position [x,y]
            if direction == 'RIGHT':
                snakePos[0] += 10
            if direction == 'LEFT':
                snakePos[0] -= 10
            if direction == 'UP':
                snakePos[1] -= 10
            if direction == 'DOWN':
                snakePos[1] += 10
        
            # Creating the snake body and the food position addng
            snakeBody.insert(0, list(snakePos))
            if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
                score += 1

                

                if score > highScore:
                    highScore = score
                    with open(highScoreFile, "w") as file:
                        file.write(str(highScore))
        
                foodSpawn = False
            else:
                snakeBody.pop()

                # IF you win the game
            if len(snakeBody) == totalSquares:
            
                result = youWin(level)
                if result == "RESTART":
                    return "RESTART"
                elif result == "MENU":
                    return "MENU"
            # Positioning of the food
            if foodSpawn == False:
                foodPos = generateFood(snakeBody)
            foodSpawn = True
        
            # Drawing the snake body and food
            # replacing the background with white
            playSurface.fill(white)
            
        
            # Drawing the snake body
            for pos in snakeBody:
                pygame.draw.rect(
                    playSurface, 
                    green, 
                    pygame.Rect(pos[0],pos[1], 10, 10)
                    )
        
            # Drawing the food
            pygame.draw.rect(playSurface, brown, 
            pygame.Rect(foodPos[0],foodPos[1], 10, 10))

           
            # Checking for the boundaries
            if snakePos[0] > 710 or snakePos[0] < 0:
                result = gameOver(level)
                if result == "RESTART":
                    return "RESTART"
                elif result == "MENU":
                    return "MENU"
            if snakePos[1] > 450 or snakePos[1] < HUD_HEIGHT:
                result = gameOver(level)
                if result == "RESTART":
                    return "RESTART"
                elif result == "MENU":
                    return "MENU"
        
            # Checks to see if the head touches the tail
            for block in snakeBody[1:]:
                if snakePos[0] == block[0] and snakePos[1] == block[1]:
                    result = gameOver(level)
                    if result == "RESTART":
                        return "RESTART"
                    elif result == "MENU":
                        return "MENU"
        

        

        # Increasing speed by 2FPS everytime the player advances a level
        speedIncrease = (level -1) * 2 
        gameSpeed = difficultySpeeds[difficulty] + speedIncrease

        if isPaused:
            playSurface.blit(pauseText, pauseRect)
        
        showScore(level=level)
        pygame.display.flip() #updates the geame
        fpsController.tick(gameSpeed)

# resets snake's starting position, food, score and direction
def restartGame():
    global snakePos, snakeBody, foodPos
    global foodSpawn, direction, changeto, score

    # Snake Position
    snakePos = [100, 100]
    snakeBody = [[100, 100], [90, 100], [80, 100]]

    # Food Position
    foodPos = generateFood(snakeBody)
    foodSpawn = True

    # Direction
    direction = 'RIGHT'
    changeto = direction

    # Score
    score = 0

while True:
    mainMenu()

    while True:
        restartGame()
        result = gameLoop()

        if result == "MENU":
            break


