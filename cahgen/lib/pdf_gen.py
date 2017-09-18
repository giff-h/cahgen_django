from configparser import ConfigParser
from copy import deepcopy

from reportlab.lib.colors import black, white, getAllNamedColors, HexColor, Color
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from .img_size import get_image_size


class PackProfile:
    colors = getAllNamedColors()

    def __init__(self, name, color):
        self.name = name
        self.color = color
        if isinstance(color, str):
            if color == '':
                self.color = None
            elif color.startswith('#'):
                try:
                    self.color = HexColor(color)
                except ValueError:
                    raise Exception("Not a valid hex color: " + color)

            else:
                if color in PackProfile.colors:
                    self.color = PackProfile.colors[color]
                else:
                    raise Exception("Not a color: " + color)

        elif not isinstance(color, Color):
            raise TypeError("Invalid color parameter: ", type(color))

    @staticmethod
    def available_colors(contains=''):
        return sorted(color for color in PackProfile.colors.keys() if contains in color)

    @staticmethod
    def load(filename):
        config = ConfigParser()
        config.read(filename)
        if "PROFILE" in config:
            profile = config["PROFILE"]
            return PackProfile(profile.get("name", ''), profile.get("color", None))
        else:
            return None

    @staticmethod
    def write_sample(filename):
        config = ConfigParser()
        config["PROFILE"] = {"name": "Sample Pack",
                             "color": "crimson"}
        with open(filename, mode='w') as file:
            config.write(file)


class _PDFWriter:
    GRID_DRAW_ON_PAGES = 1
    GRID_DRAW_SEPARATE = 2

    MULTI_PACKS_SORT = 1
    MULTI_PACKS_COLLATE = 2
    MULTI_PACKS_SMART_STACK = 3

    page_width, page_height = letter
    title_front_fs = 7
    default_font = "Helvetica-Bold"

    def __init__(self, filename, card_width, card_height, card_side_margin, card_tb_margin, front_fs, back_fs,
                 game_title, icon_fn, icon_width, duplex, text_color, font):
        self.filename = filename
        self.card_width = card_width
        self.card_height = card_height
        self.card_margin_x = card_side_margin
        self.card_margin_y = card_tb_margin
        self.game_title = game_title
        self.icon_fn = icon_fn
        self.icon_width = icon_width
        self.duplex = duplex
        self.text_color = text_color
        self.font = font

        self.front_style = deepcopy(getSampleStyleSheet()["Normal"])
        self.front_style.fontSize = front_fs
        self.front_style.leading = round(front_fs * 1.2)
        self.front_style.textColor = text_color

        self.back_style = deepcopy(getSampleStyleSheet()["Normal"])
        self.back_style.fontName = "Helvetica-Bold"
        self.back_style.fontSize = back_fs
        self.back_style.leading = round(back_fs * 1.2)
        self.back_style.textColor = text_color

        self.cards_high = 0
        self.cards_wide = 0
        self.page_margin_x = 0.0
        self.page_margin_y = 0.0
        self.grid_size = 0
        self.icon_height = 0

        self.blank = ''
        self.back_paragraph = None
        self.bp_size = 0

        self.packs = []
        self.file = None

        self._process_grid()
        self._process_back_p()
        self._process_icon()

    def _process_grid(self):
        self.card_width *= inch
        self.card_height *= inch

        self.cards_wide = int(self.page_width // self.card_width)
        self.cards_high = int(self.page_height // self.card_height)

        self.page_margin_x = (self.page_width - self.card_width * self.cards_wide) / 2
        self.page_margin_y = (self.page_height - self.card_height * self.cards_high) / 2

        self.grid_size = self.cards_wide * self.cards_high

    def _process_back_p(self):
        self.back_paragraph = Paragraph('\n'.join(self.game_title.split()), self.back_style)
        self.bp_size = self.back_paragraph.wrap(self.card_width - 2 * self.card_margin_x,
                                                self.card_height - 2 * self.card_margin_y)[1]

    def _process_icon(self):
        if self.icon_fn:
            src_img = get_image_size(self.icon_fn)
            if src_img:
                src_img_w, src_img_h = src_img
                self.icon_height = round(self.icon_width * src_img_h / src_img_w)
            else:
                self.icon_height = self.icon_width
        else:
            self.icon_height = self.icon_width

    @staticmethod
    def _process_card(card):
        return card.strip()

    @staticmethod
    def _card_not_special(card):
        return not card.startswith("//") and card != "\n"

    @staticmethod
    def _process_profile(profile):
        if profile:
            if isinstance(profile, (list, tuple)):
                if len(profile) == 1:
                    profile = PackProfile.load(profile[0])
                elif len(profile) == 2:
                    profile = PackProfile(*profile)
                else:
                    return TypeError("profile needs to be length 1 or 2, or a string, or a PackProfile")
            elif isinstance(profile, str):
                profile = PackProfile.load(profile)
            elif not isinstance(profile, PackProfile):
                raise TypeError("profile needs to be a PackProfile or a tuple")
        return profile

    @staticmethod
    def _contrast(color):
        red, green, blue = color.bitmap_rgb()
        gray = red * 0.299 + green * 0.587 + blue * 0.114
        return black if gray > 186 else white

    def _card_draw(self, row, column):
        start_x = self.page_margin_x + self.card_width * column
        start_y = self.page_height - (self.page_margin_y + self.card_height * row)

        end_x = start_x + self.card_width
        end_y = start_y - self.card_height

        start_x += self.card_margin_x
        start_y -= self.card_margin_y

        end_x -= self.card_margin_x
        end_y += self.card_margin_y

        return start_x, start_y, end_x, end_y

    def _draw_grid(self):
        self.file.setStrokeColor(self.text_color)
        for x in range(self.cards_wide + 1):
            line_x = self.page_margin_x + self.card_width * x
            line_y_b = self.page_margin_y
            line_y_e = self.page_height - self.page_margin_y
            self.file.line(line_x, line_y_b, line_x, line_y_e)
        for y in range(self.cards_high + 1):
            line_x_b = self.page_margin_x
            line_x_e = self.page_width - self.page_margin_x
            line_y = self.page_margin_y + self.card_height * y
            self.file.line(line_x_b, line_y, line_x_e, line_y)

    def _draw_front(self, page):
        self.file.setFillColor(self.text_color)
        self._draw_grid()
        self.file.setFont(self.font, self.title_front_fs)

        for row_i in range(0, len(page), self.cards_wide):
            row = page[row_i:row_i + self.cards_wide]
            for i in range(len(row)):
                content = row[i][0]
                start_x, start_y, end_x, end_y = self._card_draw(row_i // self.cards_wide, i)

                self.file.drawImage(self.icon_fn, start_x, end_y, self.icon_width, self.icon_height)
                self.file.drawString(start_x + self.icon_width + 5,
                                     end_y + self.icon_height // 2 - self.title_front_fs // 2,
                                     self.game_title)

                card_p = Paragraph(content, self.front_style)
                size = card_p.wrap(abs(end_x - start_x), abs(end_y - start_y))
                card_p.drawOn(self.file, start_x, start_y - size[1])

        self.file.showPage()

    def _draw_back(self, page):
        self.file.setFont(self.font, int(self.card_margin_y) - 1)

        for row_i in range(0, len(page), self.cards_wide):
            row = page[row_i:row_i + self.cards_wide]
            for i in range(len(row)):
                profile = row[i][1]
                start_x, start_y, end_x, end_y = self._card_draw(row_i // self.cards_wide, self.cards_wide - (i+1))

                self.back_paragraph.drawOn(self.file, start_x, start_y - self.bp_size)

                if profile and profile.color:
                    self.file.setFillColor(profile.color)
                    self.file.rect(start_x - self.card_margin_x, end_y - self.card_margin_y,
                                   self.card_width, self.card_margin_y,
                                   stroke=0, fill=1)
                    self.file.setFillColor(self._contrast(profile.color))
                    if profile.name:
                        self.file.drawString(start_x, end_y - round(self.card_margin_y * 0.8), profile.name)

        self.file.showPage()

    def _draw_page(self, page):
        if not isinstance(self.file, Canvas):
            return None

        self._draw_front(page)
        if self.duplex:
            self._draw_back(page)

    def _fill_page(self, color):
        self.file.setFillColor(color)
        self.file.rect(self.page_margin_x, self.page_margin_y,
                       self.page_width - 2 * self.page_margin_x, self.page_height - 2 * self.page_margin_y,
                       stroke=0, fill=1)

    def _process_pack(self, pack):
        for card in pack:
            card = self._process_card(card)
            if card and self._card_not_special(card):
                card = self._process_pack_card(card)
                yield card if card.startswith("<b>") else "<b>{}</b>".format(card)

    def _process_pack_card(self, card):
        return card

    def _card_generator(self):
        for pack, profile in self.packs:
            for card in self._process_pack(pack):
                yield card, profile

    def _page_generator(self):
        card_gen = self._card_generator()
        page = []
        try:
            while True:
                page = []
                for _ in range(self.grid_size):
                    page.append(next(card_gen))
                yield page
        except StopIteration:
            if page:
                yield page

    def add_pack(self, pack, profile):
        profile = self._process_profile(profile)
        self.packs.append((pack, profile))

    def write(self):
        self.file = Canvas(self.filename, pagesize=letter)
        for page in self._page_generator():
            self._draw_page(page)
        self.file.save()


class WhiteCardWriter(_PDFWriter):
    style = deepcopy(getSampleStyleSheet()["Normal"])

    def __init__(self, filename, card_width, card_height, card_side_margin, card_tb_margin, front_fs, back_fs,
                 game_title, icon_fn, icon_width, duplex, font=_PDFWriter.default_font):
        super(WhiteCardWriter, self).__init__(filename, card_width, card_height, card_side_margin, card_tb_margin,
                                              front_fs, back_fs, game_title, icon_fn, icon_width, duplex, black, font)
        # _PDFWriter.__init__(self, filename, card_width, card_height, card_side_margin, card_tb_margin,
        #                     front_fs, back_fs, game_title, icon_fn, icon_width, duplex, black, font)

    # def _process_pack(self, pack):
    #     for card in pack:
    #         card = self._process_card(card)
    #         if card and self._card_not_special(card):
    #             yield card if card.startswith("<b>") else "<b>{}</b>".format(card)


class BlackCardWriter(_PDFWriter):
    style = deepcopy(getSampleStyleSheet()["Normal"])

    def __init__(self, filename, card_width, card_height, card_side_margin, card_tb_margin, front_fs, back_fs,
                 game_title, icon_fn, icon_width, duplex, blank, font=_PDFWriter.default_font):
        super(BlackCardWriter, self).__init__(filename, card_width, card_height, card_side_margin, card_tb_margin,
                                              front_fs, back_fs, game_title, icon_fn, icon_width, duplex, white, font)
        # _PDFWriter.__init__(self, filename, card_width, card_height, card_side_margin, card_tb_margin,
        #                     front_fs, back_fs, game_title, icon_fn, icon_width, duplex, white, font)

        self.blank = "_" * blank

    # def _process_pack(self, pack):
    #     for card in pack:
    #         card = self._process_card(card)
    #         if card and self._card_not_special(card):
    #             if self.blank:
    #                 processed = self.blank if card.startswith("_") else ""
    #                 processed += self.blank.join([x for x in card.split("_") if x])
    #                 card = processed + self.blank if card.endswith("_") else processed
    #             yield card if card.startswith("<b>") else "<b>{}</b>".format(card)

    def _process_pack_card(self, card):
        if self.blank:
            processed = self.blank if card.startswith("_") else ""
            processed += self.blank.join([x for x in card.split("_") if x])
            return processed + self.blank if card.endswith("_") else processed

    def _draw_front(self, page):
        self._fill_page(black)
        super(BlackCardWriter, self)._draw_front(page)
        # _PDFWriter._draw_front(self, page)

    def _draw_back(self, page):
        self._fill_page(black)
        super(BlackCardWriter, self)._draw_back(page)
        # _PDFWriter._draw_back(self, page)


class CardBackWriter(_PDFWriter):
    def __init__(self, filename, card_width, card_height, card_side_margin, card_tb_margin, font_size,
                 game_title, profile, is_black_card, font=_PDFWriter.default_font):
        super(CardBackWriter, self).__init__(filename, card_width, card_height, card_side_margin, card_tb_margin, 0,
                                             font_size, game_title, '', 0, False, white if is_black_card else black,
                                             font)
        # _PDFWriter.__init__(self, filename, card_width, card_height, card_side_margin, card_tb_margin, 0, font_size,
        #                     game_title, '', 0, False, white if is_black_card else black, font)

        self.profile = self._process_profile(profile)
        self.is_black_card = is_black_card

        self.write()

    def _process_pack(self, pack):
        return range(self.grid_size)

    def _draw_page(self, page):
        if not isinstance(self.file, Canvas):
            return None

        if self.is_black_card:
            self._fill_page(black)
        self._draw_back(page)

    def write(self):
        self.add_pack([], self.profile)
        super(CardBackWriter, self).write()
        # _PDFWriter.write(self)


if __name__ == '__main__':
    pass
