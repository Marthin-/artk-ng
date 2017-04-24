import yaml

from map_generator.SpriteSheetHandler import SpriteSheetReader
from map_generator.SpriteSheetHandler import SpriteSheetWriter


class MapConverter:
    """ Converts a text based map to it's image equivalent. """

    def __init__(self, filename=None):
        self.text_map = list()
        self.size_x = 0
        self.size_y = 0

        self.tiled_map = None
        self.final_map = None

        if filename:
            self.read_from_disk(filename)

    def read_from_disk(self, filename):
        """
        Read a text map from the disk.
        :param filename: Path to the map
        """

        with open(filename) as map_file:
            for line in map_file:
                self.text_map.append(line.replace('\n', ''))

    def convert(self, path_to_legend, path_to_tileset):
        """
        Converts the text map to image.
        :param path_to_tileset: A path to a yaml file describing the tileset to use and it's tags
        """

        self._convert_to_tile(path_to_legend)
        self._convert_to_image(path_to_tileset)

    def _convert_to_tile(self, path_to_legend):
        """ Converts ascii charaters to tileset tag. """

        self.size_y = len(self.text_map)
        self.tiled_map = list()

        with open(path_to_legend) as tileset:

            legend = yaml.load(tileset)['Legend']
            if legend is None:
                raise Exception("Error when opening legend file.")

            for y, line in enumerate(self.text_map):
                tmp = list()
                for x, tile in enumerate(line):
                    if tile == '\n':
                        pass
                    elif tile in legend.keys():
                        tmp.append(legend[tile])
                    else:
                        print("Unknown tile at : [{}, {}]".format(x, y))
                        tmp.append('default')

                self.size_x = max(self.size_x, len(line))
                self.tiled_map.append(tmp)

    def _get_wall(self, x, y):
        """
        Find the right id for the tile at given coordinates. In case of multiple sprites for on tag
        :param x: X coordinates
        :param y: Y coordinates
        """
        sprite_id = 0
        current_line = self.text_map[y]
        previous_line = self.text_map[y - 1] if y > 0 else None
        next_line = self.text_map[y + 1] if y + 1 < len(self.text_map) else None

        # UP
        if previous_line is not None and x < len(previous_line) and previous_line[x] == '#':
            sprite_id += 1
        # RIGHT
        if x + 1 < len(current_line) and current_line[x + 1] == '#':
            sprite_id += 2

        # BOTTOM
        if next_line is not None and x < len(next_line) and next_line[x] == '#':
            sprite_id += 4

        # LEFT
        if x - 1 >= 0 and current_line[x - 1] == '#':
            sprite_id += 8

        return sprite_id

    def _convert_to_image(self, path_to_tileset):
        """ 
        Convert tag representation of the map to image.
        :path_to_tileset Path to a yaml file describing the tileset to use and it's tags
        """

        import os
        writer = None

        with open(path_to_tileset) as tileset:
            tileset_config = yaml.load(tileset)
            if tileset_config is not None:
                meta = tileset_config['Tileset']['Meta']

                path = os.path.join(os.path.dirname(path_to_tileset), meta['file'])
                if not os.path.exists(path):
                    raise Exception('Tileset does not exist')

                tile_tags = tileset_config['Tileset']['Tiles']

                # Tileset writer & reader
                reader = SpriteSheetReader(path, meta['size'])
                writer = SpriteSheetWriter(meta['size'], self.size_x, self.size_y)

                for y, line in enumerate(self.tiled_map):
                    for x, tile in enumerate(line):

                        tag = tile_tags[tile]

                        if type(tag) is list:
                            coord = tag

                        else:  # multiple sprite for on tag
                            sprite_id = self._get_wall(x, y)
                            coord = tag[sprite_id]

                        writer.add_tile(reader.get_tile(coord[0], coord[1]))
                    writer.next_line()

        if not writer:
            raise Exception('Error during conversion to image')

        self.final_map = writer.get_img()

    def save_map(self, filename):
        """
        Save image map to the disk
        :param filename: Path to save image
        """

        if self.final_map:
            self.final_map.save(filename)
        else:
            raise Exception("There's no image to save :/")

    def show_map(self):
        """ Display map on screen. """

        if self.final_map:
            self.final_map.show()
        else:
            raise Exception("There's no image to show :/")
