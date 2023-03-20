import pygame, math, sys, time, numpy as np, random

# Changes since demo:
# - added colormode
# - sender cancels if mouse still on body

pygame.init(); print()
screen = pygame.display.set_mode(size=(1000, 600), flags=pygame.RESIZABLE)
pygame.display.set_caption('Into Orbit I (v0.0.1)')
try:
    Icon = pygame.image.load(rf'{sys.path[0]}\intoorbit.png')
    pygame.display.set_icon(Icon)
except:
    print("Couldn't find icon.")

def randomHex():
    Hex = [hex(random.randint(0,255))[2::] for _ in '123']
    return f'#{"0"*(len(Hex[0])<2)+Hex[0]}{"0"*(len(Hex[1])<2)+Hex[1]}{"0"*(len(Hex[2])<2)+Hex[2]}'

def velo2color(velo):
    speeeeeed = math.sqrt(velo.dot(velo))
    c1 = np.array((0, 255, 0))
    c2 = np.array((255, 0, 0))
    k = min(60, speeeeeed)/60
    return c1*(1-k) + c2*k

def pos2color(pos):
    x, y = pos

    xc1 = np.array((255, 0, 0))
    xc2 = np.array((0, 255, 0))
    yc1 = np.array((0, 0, 255))
    yc2 = np.array((255, 255, 00))

    width, height = screen.get_size()

    kx = min(width, abs(x))/width
    ky = min(height, abs(y))/height

    c1 = xc1*(1-kx) + xc2*kx
    c2 = yc1*(1-ky) + yc2*ky

    return c1*0.5 + c2*0.5

def G(m, M, d):
    return 6.67e-11 * m * M / (d**2/10000)

def distBetween(body1, body2):
    vec = body2.pos - body1.pos
    dist = math.sqrt(vec.dot(vec))
    return dist

class Sender():
    def __init__(self, pos, size) -> None:
        self.pos = pos
        self.r = size
    
    def send(self, mousepos) -> None:
        vec = self.pos - mousepos
        bodies.append(Body(orbitMass, orbitRadius, vec/2, self.pos, randomHex()))

class Body():
    def __init__(self, mass, size, velo, pos, color) -> None:
        self.m = mass
        self.r = size
        self.velo = velo
        self.pos = pos
        self.color = color

colormode = 1

mainMass = 3e11
orbitMass = 1

mainRadius = 25
orbitRadius = 10
senderRadius = 10

mainColor = '#ffffff'
orbitColor = '#8ec7d2'
senderColor = '#0d6986'
senderLineColor = '#ededed'
backgroundColor = '#383838'

celestial = Body(mainMass, mainRadius, None, None, mainColor)
bodies = []

oldtime = time.time()

sender = None
keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(size=event.size, flags=pygame.RESIZABLE)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = np.array(pygame.mouse.get_pos(), dtype=float)
            
            sender = Sender(pos, senderRadius)

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = np.array(pygame.mouse.get_pos(), dtype=float)

            vec = pos - sender.pos

            if math.sqrt(vec.dot(vec)) > senderRadius:
                sender.send(pos)

            sender = None

        elif event.type == pygame.KEYDOWN:
            
            if event.key in keys:
                colormode = keys.index(event.key) + 1

    width, height = screen.get_size()
    screenCenter = (width/2, height/2)

    screen.fill(backgroundColor)

    celestial.pos = np.array(screenCenter, dtype=float)
    pygame.draw.circle(screen, mainColor, celestial.pos, celestial.r)

    currenttime = time.time()
    dt = (currenttime - oldtime)*10
    oldtime = currenttime

    removeBodies = []
    for body in bodies:
        vec = celestial.pos - body.pos
        d = distBetween(body, celestial)
        acc = vec * G(body.m, celestial.m, d) / d
        body.velo += dt * acc
        body.pos += dt * body.velo

        if d < mainRadius or d > 1e6:
            removeBodies.append(body)
            continue

        if colormode == 1: clr = orbitColor
        elif colormode == 2: clr = body.color
        elif colormode == 3: clr = velo2color(body.velo)
        elif colormode == 4: clr = pos2color(body.pos)
        elif colormode == 5: clr = randomHex()

        try:
            pygame.draw.circle(screen, clr, body.pos, body.r)
        except: print(repr(clr)); sys.exit()

    for body in removeBodies:
        bodies.remove(body)
    
    if sender:
        pygame.draw.line(screen, senderLineColor, sender.pos, pygame.mouse.get_pos(), 2)
        pygame.draw.circle(screen, senderColor, sender.pos, sender.r)
    
    pygame.display.flip()
