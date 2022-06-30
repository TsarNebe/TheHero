from settings import *


class NewGame:

    ETHNICITY, CLASS_, NAME = '', '', ''
    check, name_for_loading = '', ''

    class_new_game = True
    BLOCK, INBOX = False, False

    def __init__(self, *groups):
        self.pos_y_e, self.pos_y_c = 70, 560

        self.bg = Obj(IMG_NEW_GAME['bg'], 0, 0, *groups)

        self.ethnicity = []
        self.class_ = []

        self.boxes = [
            Obj(IMG_NEW_GAME['HERALDRY_BOX'], 0, 111, *groups),
            Obj(IMG_NEW_GAME['BOX_STATUS'], 8, 632, *groups),
            pg.Rect(183, 942, 376, 35)
        ]

        self.interactive_ = [
            Obj(IMG_NEW_GAME['select'], LIMBO, self.pos_y_e, *groups),
            Obj(IMG_NEW_GAME['select'], LIMBO, self.pos_y_c, *groups),
            Obj(IMG_NEW_GAME['interactive'], LIMBO, LIMBO, *groups),
        ]

        self.max_records = Obj(IMG_NEW_GAME['max_records'], 0, LIMBO, *groups)
        self.add_icon = Obj(IMG_NEW_GAME['add'], 559, 942, *groups)
        self.return_icon = Obj(IMG_MENU['return'], 100, 942, *groups)

        self.index_list_class = LIST_CLASSES[0]

    def _select_guides(self, pos_mouse):

        self._list_ethnicity_and_classes(self.ethnicity[0], 'dark-elf', 'info_dark', pos_mouse)
        self._list_ethnicity_and_classes(self.ethnicity[1], 'forest-elf', 'info_forest', pos_mouse)
        self._list_ethnicity_and_classes(self.ethnicity[2], 'grey-elf', 'info_grey', pos_mouse)

    def _return_menu(self, pos_mouse):

        if self.return_icon.rect.collidepoint(pos_mouse):
            self.class_new_game = False
            self._reset_changes()

    def _add_record(self, pos_mouse):
        """
        SELECT NAME AND ADD BOX
        RETURN THE REGISTRATION TO ADD NAME AND CLICK ON ICON
        """
        if not self.BLOCK:

            if self.add_icon.rect.collidepoint(pos_mouse) and (len(self.NAME) >= MIN_CHARACTERS_NAME):

                features = self.NAME + '\n' + self.ETHNICITY + '\n' + self.CLASS_ + '\n' + '1'

                with open(FOLDER['save'] + self.NAME, 'w') as new_record:
                    new_record.write(features)
                click_sound.play()

                sleep(1)

                self.check = 'loading'
                self.name_for_loading = self.NAME

    def _active_input_box(self, pos_mouse):

        if not self.BLOCK:

            if self.boxes[2].collidepoint(pos_mouse):
                self.INBOX = True, click_sound.play()
            else:
                self.INBOX = False

            COLORS['ACTIVE'] = COLORS['WHITE'] if self.INBOX else COLORS['BLACK']

    def _receives_character_name(self, event):
        """
        NAME RECEIVES THE PRESSED CHARACTERS, REMOVED FROM THE KEY/EVENT.UNICODE
        PREVENTS TEXT FROM BEING GREATER THAN MAX_C CHARACTERS
        """
        if not self.BLOCK:

            if event.type == pg.KEYDOWN and self.INBOX:

                if len(self.ETHNICITY) > 2 < len(self.CLASS_):
                    if event.key == pg.KSCAN_UNKNOWN:
                        self.NAME = ''
                    if event.key == pg.K_BACKSPACE:
                        self.NAME = self.NAME[:-1]
                    else:
                        self.NAME += str(event.unicode).replace('\r', '').replace('\t', '').strip().casefold()

        self.NAME = self.NAME[:-1] if len(self.NAME) >= MAX_CHARACTERS_NAME else self.NAME

    def _interactive(self, pos_mouse):
        """
        RETURNS IMAGE SWITCH ON MOUSE COLLIDE
        """
        mouse_collision_catching_x_y(
            LIMBO, self.ethnicity + self.class_, self.interactive_[2], pos_mouse)

        mouse_collision_changing_image(
            self.return_icon, pos_mouse, IMG_MENU['select_return'], IMG_MENU['return'])

        mouse_collision_changing_image(
            self.add_icon, pos_mouse, IMG_LOAD['select_add'], IMG_NEW_GAME['add'], check=False)

    def _draw_box(self):
        """
        BOX DRAWING TO ADD NAME
        DRAW THE TEXT, BOX -> INSIDE THE SCREEN_MAIN
        """
        if self.INBOX and len(self.NAME) >= MIN_CHARACTERS_NAME:
            self.add_icon.image = pg.image.load(IMG_LOAD['select_add'])
        else:
            self.add_icon.image = pg.image.load(IMG_NEW_GAME['add'])

        # DRAW USER TEXT INPUT
        draw_texts(
            MAIN_SCREEN, self.NAME.title(), X=self.boxes[2].x + 5, Y=self.boxes[2].y + 5, size=25,
            color=COLORS['BLACK'])

        # DRAW THE BOX FOR TEXT INPUT
        pg.draw.rect(MAIN_SCREEN, COLORS['ACTIVE'], self.boxes[2], 2)

    def _check_max_records(self):
        """
        CHECK LIMIT OF RECORDS AND RETURN LOCK FOLLOWED BY INSTRUCTIONS
        """
        if self.class_new_game and len([x for x in listdir(FOLDER['save'])]) >= MAX_RECORDS:
            self.BLOCK = True
            self.max_records.rect.y = 0

        else:
            self.BLOCK = False
            self.max_records.rect.y = LIMBO

    def _draw_subtitles(self):

        pos_x_txt = [75, 324, 573]
        pos_x_rect = [0, 249, 498]
        pos_y_etn, pos_y_clas = 70, 560

        for item in range(3):

            # TEXT AND BOX FOR ETHNICITIES
            draw_texts(
                MAIN_SCREEN, f'{list_ethnicities[item]}'.title(), pos_x_txt[item], pos_y_etn + 10, size=20)

            self.ethnicity.append(DrawStatusBar(249, 41, 0, 249, rect=(pos_x_rect[item], pos_y_etn)))

            # TEXT AND BOX FOR CLASSES
            draw_texts(
                MAIN_SCREEN, f'{self.index_list_class[item]}'.title(), pos_x_txt[item] + 20, pos_y_clas + 10, size=20)

            self.class_.append(DrawStatusBar(249, 41, 0, 249, rect=(pos_x_rect[item], pos_y_clas)))

    def _draw_info_ethnicity(self):

        try:
            info =\
                'dark' if 'dark' in self.ETHNICITY else\
                'forest' if 'forest' in self.ETHNICITY else\
                'grey' if 'grey' in self.ETHNICITY else None

            y = 240
            for line in INFO_HERALDRY[info][LANGUAGE].replace('\n', '').split('\r'):
                draw_texts(MAIN_SCREEN, f'{line}', 0, y, color=COLORS['BLACK'])

                y += 30 if len(INFO_HERALDRY[info][LANGUAGE]) < 600 else 15

        except Exception as erro:
            return f'{erro.args}'

    def _draw_info_classes(self):
        try:

            idd = 'ed_' if 'dark' in self.ETHNICITY else 'ef_' if 'forest' in self.ETHNICITY else 'eg_'
            list_with_attributes = DARK_ELF if idd == 'ed_' else FOREST_ELF if idd == 'ef_' else GREY_ELF

            # TITLE
            draw_texts(MAIN_SCREEN, f'{"Status":^35}{"Skills":^35}', 190, 620, color=COLORS['BLACK'], size=20)

            # ATTRIBUTES
            y = 680
            for index, status in enumerate(BASIC_ATTRIBUTES):

                draw_texts(
                    MAIN_SCREEN, f'{status.title():<} - {list_with_attributes[self.CLASS_][index]:>.1f}',
                    210, y, color=COLORS['BLACK'], size=20)

                y += 30

            # SPRITE OF CLASS
            sprite = pg.image.load(IMG_CLASSES[idd + self.CLASS_])
            MAIN_SCREEN.blit(sprite, (25, 680))

        except Exception as erro:
            return f'{erro.args}'

        # SKILLS
        y = 680
        for line in INFO_SKILLS[idd[1:] + self.CLASS_][LANGUAGE].replace('\n', '').split('\r'):
            draw_texts(MAIN_SCREEN, f'{line}', 375, y, color=COLORS['BLACK'])

            y += 20

    def _list_ethnicity_and_classes(self, var_ethnicity, name_ethnicity: str, bg_ethnicity: str, pos_mouse):

        classes = LIST_CLASSES[0] if 'dark' in name_ethnicity else LIST_CLASSES[1]

        if var_ethnicity.rect.collidepoint(pos_mouse):
            self._reset_changes()

            self.interactive_[0].rect.x = var_ethnicity.rect.x
            self.boxes[0].image = pg.image.load(IMG_NEW_GAME[bg_ethnicity])

            self.index_list_class = classes
            self.ETHNICITY = name_ethnicity.casefold()

        if self.interactive_[0].rect.x == var_ethnicity.rect.x:

            for index in range(3):

                if self.class_[index].rect.collidepoint(pos_mouse):
                    self.CLASS_ = classes[index].casefold()

    def _reset_changes(self):

        self.NAME, self.ETHNICITY, self.CLASS_ = '', '', ''

        for index in range(1):
            self.interactive_[index].rect.x = LIMBO
            self.boxes[0].image = pg.image.load(IMG_NEW_GAME['HERALDRY_BOX'])

    def events_new_game(self, event):

        pos_mouse = pg.mouse.get_pos()

        if event.type == pg.MOUSEBUTTONDOWN:
            self._return_menu(pos_mouse)
            self._select_guides(pos_mouse)
            self._active_input_box(pos_mouse)
            self._add_record(pos_mouse)

        if event.type == pg.MOUSEMOTION:
            self._interactive(pos_mouse)

        self._receives_character_name(event)

    def update(self, *args, **kwargs):

        self._check_max_records()
        self._draw_box()
        self._draw_subtitles()
        self._draw_info_ethnicity()
        self._draw_info_classes()

        draw_texts(MAIN_SCREEN, f'{title_new_game[0]}', 300 + len(title_new_game[0]), 15, size=27)
        draw_texts(MAIN_SCREEN, f'{title_new_game[1]}', 300 + len(title_new_game[1]), 510, size=27)

