import pygame
from support import import_folder


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        self.rect.x += shift


class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

 # offset einer variablen(x oder y), damit das objekt nicht links oben beginnt:
 #class BELIEBIGESOBJEKT(StaticTile):
    #def __init__(self, size, x, y):
        #super().__init__(size, x, y, pygame.image.load("../graphics/images/.../BELIEBIGESOBJEKT.png").convert_alpha())
        #offset_y = y + size
        #self.rect = self.image.get_rect(bottomleft =(x, offset_y))


class Coins(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load("../graphics/images/gold/0.png").convert_alpha())

 # für die AnimatedTiles class-definition,
 # kann ich bilder in einem ordner (in level, ist der pfad eingetragen) anzeigen.
class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift

 # normalerweise wird bei x =0, y =0 (obere linke ecke) dargestellt
 # ----> x, y veränderte angaben: (hier= mittige darstellung)
#class BELIEBIGESOBJEKT(AnimatedTile):
    #def __init__(self, size, x, y, path):
        #super().__init__(size, x, y, path)
        #center_x = x + int(size / 2)
        #center_y = y + int(size / 2)
        #self.rect = self.image.get_rect(center = (center_x, center_y))
