from PIL import Image


class SpriteSheetReader:
    """ Handle reading in tileset. """

    def __init__(self, image_name, tile_size=16, margin=0):
        """
        Constructor in attributes
        :param image_name: Path to the tileset on disk
        :param tile_size: Size of the tileset
        :param margin: Optional margin between tiles in file
        """
        self.spriteSheet = Image.open(image_name)
        self.tileSize = tile_size
        self.margin = margin

    def get_tile(self, tile_x, tile_y):
        """
        Find the tile associate to given tag.
        :param tile_x: X position
        :param tile_y: Y position
        :return: Corresponding tile
        """

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

    def _get_cur_pos(self):
        """ Find the next correct position to put a new tile in self.spritesheet. """

        self.pos_x = (self.tileSize * self.tileX) + (self.margin * (self.tileX + 1))
        self.pos_y = (self.tileSize * self.tileY) + (self.margin * (self.tileY + 1))
        if self.pos_x + self.tileSize > self.size_x:
            self.tileX = 0
            self.tileY = self.tileY + 1
            self._get_cur_pos()
        if (self.pos_y + self.tileSize) > self.size_y:
            raise Exception('Image does not fit within spritesheet!')

    def next_line(self):
        """ Switch to the next line."""
        self.tileY += 1
        self.tileX = 0

    def add_tile(self, image, rotation=0):
        """
        Push image with optional rotation next to the last tile.
        Uses _get_cur_pos to find the current position
        :param image: tile to add
        :param rotation: optional rotation should be equal to 0 modulo 90
        """

        if rotation % 90:
            raise Exception("Given rotation can't be used : {}".format(rotation))

        self._get_cur_pos()
        dest_box = (self.pos_x, self.pos_y, self.pos_x + image.size[0], self.pos_y + image.size[1])
        self.spritesheet.paste(image.rotate(rotation), dest_box)
        self.tileX = self.tileX + 1

    def get_img(self):
        """
        :return Final image.
        """
        return self.spritesheet
