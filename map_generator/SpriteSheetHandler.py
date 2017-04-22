from PIL import Image


class SpriteSheetReader:
    """ Handle reading from tileset. """

    def __init__(self, image_name, tile_tags, tile_size=16, margin=0):
        self.spriteSheet = Image.open(image_name)
        self.tile_tags = tile_tags
        self.tileSize = tile_size
        self.margin = margin

    def get_tile(self, tag):
        tile_x = self.tile_tags[tag][0]
        tile_y = self.tile_tags[tag][1]

        pos_x = (self.tileSize * tile_x) + (self.margin * (tile_x + 1))
        pos_y = (self.tileSize * tile_y) + (self.margin * (tile_y + 1))
        box = (pos_x, pos_y, pos_x + self.tileSize, pos_y + self.tileSize)

        return self.spriteSheet.crop(box)


class SpriteSheetWriter:
    """ Handle tilemap creation. """

    def __init__(self, tile_size, size_x, size_y):
        self.tileSize = tile_size
        self.size_x = size_x * tile_size
        self.size_y = size_y * tile_size
        self.spritesheet = Image.new("RGBA", (self.size_x, self.size_y), (0, 0, 0, 0))
        self.tileX = 0
        self.tileY = 0
        self.margin = 0
        self.pos_x = 0
        self.pos_y = 0

    def get_cur_pos(self):
        self.pos_x = (self.tileSize * self.tileX) + (self.margin * (self.tileX + 1))
        self.pos_y = (self.tileSize * self.tileY) + (self.margin * (self.tileY + 1))
        if self.pos_x + self.tileSize > self.size_x:
            self.tileX = 0
            self.tileY = self.tileY + 1
            self.get_cur_pos()
        if (self.pos_y + self.tileSize) > self.size_y:
            raise Exception('Image does not fit within spritesheet!')

    def add_image(self, image, rotation=0):
        if rotation % 90:
            raise Exception("Given rotation can't be used : {}".format(rotation))

        self.get_cur_pos()
        destBox = (self.pos_x, self.pos_y, self.pos_x + image.size[0], self.pos_y + image.size[1])
        self.spritesheet.paste(image.rotate(rotation), destBox)
        self.tileX = self.tileX + 1

    def get_img(self):
        return self.spritesheet
