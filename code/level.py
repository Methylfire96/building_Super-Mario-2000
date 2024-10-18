import pygame

from settings import tile_size, screen_width
from support import import_csv_layout, import_cut_graphics
from tiles import Tile, StaticTile, Coins, AnimatedTile
from enemies import Enemies
from player import Player


class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0

        # player
        player_layout = import_csv_layout(level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)


        # bg_terrain setup
        bg_terrain_layout = import_csv_layout(level_data["bg_terrain"])
        self.bg_terrain_sprites = self.create_tile_group(bg_terrain_layout, "bg_terrain")

        # terrain setup
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        # coins
        coins_layout = import_csv_layout(level_data["coins"])
        self.coins_sprites = self.create_tile_group(coins_layout, "coins")

        # tube
        tube_layout = import_csv_layout(level_data["tube"])
        self.tube_sprites = self.create_tile_group(tube_layout, "tube")

        # enemies
        enemies_layout = import_csv_layout(level_data["enemies"])
        self.enemies_sprites = self.create_tile_group(enemies_layout, "enemies")

        # constraints
        constraints_layout = import_csv_layout(level_data["constraints"])
        self.constraints_sprites = self.create_tile_group(constraints_layout, "constraints")


    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == "bg_terrain":
                        bg_terrain_tile_list = import_cut_graphics("../graphics/images/terrain_tiles.png")
                        tile_surface = bg_terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == "terrain":
                        terrain_tile_list = import_cut_graphics("../graphics/images/terrain_tiles.png")
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == "coins":
                        sprite = AnimatedTile(tile_size, x, y ,"../graphics/images/gold")

                    if type == "tube":
                        tube_tile_list = import_cut_graphics("../graphics/images/tube.png")
                        tile_surface = tube_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == "enemies":
                        sprite = Enemies(tile_size, x, y)

                    if type == "constraints":
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)


        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == "0":
                    sprite = Player((x, y), self.display_surface)
                    self.player.add(sprite)

                if val == "2":
                    hat_surface = pygame.image.load("../graphics/images/mushroom.png").convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.tube_sprites.sprites() + self.coins_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.tube_sprites.sprites() + self.coins_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 6
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -6
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 6

    def enemies_collision_reverse(self):
        for enemies in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemies, self.constraints_sprites, False):
                enemies.reverse()

    def run(self):
        self.bg_terrain_sprites.update(self.world_shift)
        self.bg_terrain_sprites.draw(self.display_surface)

        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        self.tube_sprites.update(self.world_shift)
        self.tube_sprites.draw(self.display_surface)

        self.enemies_sprites.update(self.world_shift)
        self.constraints_sprites.update(self.world_shift)
        self.enemies_collision_reverse()
        self.enemies_sprites.draw(self.display_surface)

        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)


