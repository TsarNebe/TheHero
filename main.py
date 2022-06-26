from settings import *
from menu import Menu
from newgame import NewGame
from load import Load
from options import Options
from character import Character
from game import Game


class RoadMapMenu:
    class_road_map_menu = True

    group_sprites_options = GROUPS['options']
    group_sprites_load = GROUPS['load']
    group_sprites_new_game = GROUPS['new']
    group_sprites_menu = GROUPS['menu']

    menu_ = Menu(group_sprites_menu)
    new = NewGame(group_sprites_new_game)
    load = Load(group_sprites_load)
    options = Options(group_sprites_options)

    def draw(self, main_screen):
        loading = self.new.check + self.load.check

        if loading == '' and self.class_road_map_menu:

            if self.menu_.class_menu:
                self.group_sprites_menu.draw(main_screen)
                self.menu_.update()

            elif self.menu_.check == 'new' and self.new.class_new_game:
                self.group_sprites_new_game.draw(main_screen)
                self.new.update()

            elif self.menu_.check == 'load' and self.load.class_load:
                self.group_sprites_load.draw(main_screen)
                self.load.update()

            elif self.menu_.check == 'options' and self.options.class_options:
                self.group_sprites_options.draw(main_screen)
                self.options.update()

            else:
                self.menu_.class_menu = True
                self.new.class_new_game = True
                self.load.class_load = True
                self.options.class_options = True

        else:
            self.class_road_map_menu = False

    def events(self, event):
        if self.class_road_map_menu:

            if self.menu_.class_menu:
                self.menu_.events_menu(event)

            elif self.menu_.check == 'new' and self.new.class_new_game:
                self.new.events_new_game(event)

            elif self.menu_.check == 'load' and self.load.class_load:
                self.load.events_load(event)

            elif self.menu_.check == 'options' and self.options.class_options:
                self.options.events_options(event)


class RoadMapGame:

    @staticmethod
    def name_for_loading(name):
        for index, item in enumerate(check_records(FOLDER['save'])):
            if str(name) in item[0].casefold():
                return index
        return 0

    class_road_map_game = True

    group_sprites_char = GROUPS['char']
    group_sprites_opponent = GROUPS['opponent']
    group_sprites_game_interface = GROUPS['game']

    game_interface = Game(group_sprites_game_interface)
    character = Character(group_sprites_char)
    index = 0

    def draw(self, main_screen):

        if self.class_road_map_game:

            if self.game_interface.class_game:
                self.group_sprites_game_interface.draw(main_screen)
                self.game_interface.update()

                self.character.index = self.name_for_loading(self.index)
                self.character.update()

            else:
                self.character.save()
                save_log()

    def events(self, event):
        if self.class_road_map_game:

            self.game_interface.events_game(event)


##########################################################################################

road_map_menu = RoadMapMenu()
road_map_game = RoadMapGame()


def draw():
    if road_map_menu.class_road_map_menu:
        road_map_menu.draw(MAIN_SCREEN)

    elif road_map_game.class_road_map_game:

        road_map_game.index = road_map_menu.load.name_for_loading + road_map_menu.new.name_for_loading
        road_map_game.draw(MAIN_SCREEN)

    else:
        road_map_menu.class_road_map_menu = True
        road_map_game.class_road_map_game = True


def events():
    for event in pg.event.get():

        if event.type == pg.QUIT:
            save_log()

        if road_map_menu.class_road_map_menu:
            road_map_menu.events(event)

        elif road_map_game.class_road_map_game:
            road_map_game.events(event)


def update():
    FRAMES.tick(road_map_menu.options.MAX_FRAMES)
    draw()
    events()
    pg.display.update()


if __name__ == '__main__':
    while True:
        update()
