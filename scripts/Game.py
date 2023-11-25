import pygame
import Data
import Player
from math import *

screen = pygame.display.set_mode(Data.screenSize, flags = pygame.NOFRAME)
pygame.display.set_caption("Raycasters2005") #Здесь будет название игры, которого пока что нет
#gameIcon = pygame.image.load("images/icon.png")
#pygame.display.set_icon(gameIcon) #Здесь будет иконка игры
textures = {
"1" : pygame.image.load("images/1.jpg"),
"2" : pygame.image.load("images/2.jpg"),
"3" : pygame.image.load("images/3.jpg"),
"4" : pygame.image.load("images/4.jpg")}
#background1 = pygame.image.load("images/background1.jpeg")
#background2 = pygame.image.load("images/background1.jpeg")


gameRunning = True
gameClock = pygame.time.Clock()
pygame.mouse.set_visible(False)



def Movement(backgroundPosition):
    keyPressed = pygame.key.get_pressed()
    horizontalInput = -int(keyPressed[Data.keys["left"]]) + int(keyPressed[Data.keys["right"]])
    verticalInput = -int(keyPressed[Data.keys["forward"]]) + int(keyPressed[Data.keys["back"]])
    rightPlayerDirection = [sin(Player.rotation), -cos(Player.rotation)]
    forwardPlayerDirection = [cos(Player.rotation), sin(Player.rotation)]
    moveVector = [rightPlayerDirection[0] * -horizontalInput + forwardPlayerDirection[0] * -verticalInput, rightPlayerDirection[1] * -horizontalInput + forwardPlayerDirection[1] * -verticalInput]

    if moveVector[0] != 0 and moveVector[1] != 0:
        magnitude = (moveVector[0] ** 2 + moveVector[1] ** 2) ** 0.5
        moveVector = [moveVector[0] / magnitude, moveVector[1] / magnitude]
    Player.position[0] += moveVector[0] * Player.movementSpeed
    Player.position[1] += moveVector[1] * Player.movementSpeed

    mouseRel = pygame.mouse.get_rel()
    mouseDirection = mouseRel[0]
    pygame.mouse.set_pos(Data.screenWidth // 2, Data.screenHeight // 2)
    Player.rotation += (mouseDirection) / Player.rotationSpeed
    #backgroundPosition = -Player.rotation * 700
    #screen.blit(background1, (backgroundPosition, 0))
    #screen.blit(background2, (backgroundPosition + 2716, 0))

def Raycast(ray, ox, oy, xm, ym):
    rayAngle = ray * Data.paddingOfRays + Player.rotation
    x, dx = (xm + Data.blockSize, 1) if cos(rayAngle) >= 0 else (xm, -1)
    magnitude = [10 ** 10, 10 ** 10]
    for i in range(0, int(Data.depthOfField), Data.blockSize):
        if cos(rayAngle) != 0:
            magnitude[0] = (x - ox) / cos(rayAngle)
        yv = oy + magnitude[0] * sin(rayAngle)
        rounded = ((x + dx) // Data.blockSize * Data.blockSize, yv // Data.blockSize * Data.blockSize)
        currentTextureV = 0
        if rounded in Data.worldMap:
            currentTextureV = Data.worldMap[rounded]
            break
        x += dx * Data.blockSize

    y, dy = (ym + Data.blockSize, 1) if sin(rayAngle) >= 0 else (ym, -1)
    for i in range(0, Data.screenHeight, Data.blockSize):
        if sin(rayAngle) != 0:
            magnitude[1] = (y - oy) / sin(rayAngle)
        xh = ox + magnitude[1] * cos(rayAngle)
        rounded = (xh // Data.blockSize * Data.blockSize, (y + dy) // Data.blockSize * Data.blockSize)
        currentTextureH = 0
        if rounded in Data.worldMap:
            currentTextureH = Data.worldMap[rounded]
            break
        y += dy * Data.blockSize

    #if currentTextureH != 0 or currentTextureV != 0:
    depth, offset, currentTexture = (magnitude[0], yv, currentTextureV) if magnitude[0] < magnitude[1] else (magnitude[1], xh, currentTextureH)

    offset = int(offset) % Data.blockSize
    depth = depth * cos(Player.rotation - rayAngle)
    proectionHeight = Data.blockSize * Data.distanceFromScreen / depth * Data.proectionCoefficient

    wallColumn = textures[currentTexture].subsurface(offset * Data.textureScale, 0, Data.textureScale, Data.textureHeight)
    wallColumn = pygame.transform.scale(wallColumn, (Data.rayThickness + 1, proectionHeight))
    screen.blit(wallColumn, (ray * Data.rayThickness + Data.screenWidth / 2, Data.screenHeight // 2 - proectionHeight // 2))


def Draw():
    ox, oy = Player.position[0], Player.position[1]
    xm, ym = (ox // Data.blockSize * Data.blockSize, oy // Data.blockSize * Data.blockSize)
    for ray in range(-Data.accuracyOfDraw // 2, Data.accuracyOfDraw // 2):
        Raycast(ray, ox, oy, xm, ym)

#Отрисовка мини карты
    pygame.draw.rect(screen, "black", (0, 0, Data.blockSize * len(Data.map[0]) / Data.miniMapScale, Data.blockSize * len(Data.map[0]) / Data.miniMapScale))
    for y in range(len(Data.map)):
        for x in range(len(Data.map[0])):
            if Data.map[y][x] != " ":
                pygame.draw.rect(screen, "white",(x * Data.blockSize / Data.miniMapScale, y * Data.blockSize / Data.miniMapScale, Data.blockSize / Data.miniMapScale, Data.blockSize / Data.miniMapScale))

    pygame.draw.circle(screen,"blue", (Player.position[0] / Data.miniMapScale, Player.position[1] / Data.miniMapScale), 4)



while gameRunning:
    Movement(backgroundPosition=0)
    Draw()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            gameRunning = False

    screen.fill("black")
    gameClock.tick(Data.fps)