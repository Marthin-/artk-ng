import yaml

from map_generator.SpriteSheetHandler import SpriteSheetReader
from map_generator.SpriteSheetHandler import SpriteSheetWriter


class MapConverter:
    def __init__(self, filename=None):
        self.text_map = list()
        self.size_x = 0
        self.size_y = 0

        self.tiled_map = None
        self.final_map = None

        if filename:
            self.read_from_disk(filename)

    def read_from_disk(self, filename):
        with open(filename) as map_file:
            for line in map_file:
                self.text_map.append(line.replace('\n', ''))

    def convert(self, path_to_tileset):

        self._convert_to_tile()
        self._convert_to_image(path_to_tileset)

    def _convert_to_tile(self):

        self.size_y = len(self.text_map)
        self.tiled_map = list()

        for y, line in enumerate(self.text_map):
            tmp = list()
            for x, tile in enumerate(line):
                if tile == '\n':
                    pass
                elif tile == '^':
                    tmp.append('stairsUp')
                elif tile == 'v':
                    tmp.append('stairsDown')
                elif tile == 'T':
                    tmp.append('table')
                elif tile == '+':
                    tmp.append('door')
                elif tile == ' ':
                    tmp.append('floor')
                elif tile == '#':
                    tmp.append(self._get_wall(x, y))
                else:
                    print("Unknown tile at : [{}, {}]".format(x, y))

            self.size_x = max(self.size_x, len(line))
            self.tiled_map.append(tmp)
        for line in self.tiled_map:
            print(line)

    def _get_wall(self, x, y):

        wall_type = 0
        current_line = self.text_map[y]
        previous_line = self.text_map[y - 1] if y > 0 else None
        next_line = self.text_map[y + 1] if y + 1 < len(self.text_map) else None

        # UP
        if previous_line is not None and x < len(previous_line) and previous_line[x] == '#':
            wall_type += 1
        # RIGHT
        if x + 1 < len(current_line) and current_line[x + 1] == '#':
            wall_type += 2

        # BOTTOM
        if next_line is not None and x < len(next_line) and next_line[x] == '#':
            wall_type += 4

        # LEFT
        if x - 1 >= 0 and current_line[x - 1] == '#':
            wall_type += 8

        return "wall" + str(wall_type)

    def _convert_to_image(self, path_to_tileset):
        import os
        writer = None

        with open(path_to_tileset) as tileset:
            tileset_config = yaml.load(tileset)
            if tileset_config is not None:
                meta = tileset_config['Tileset']['Meta']

                path = os.path.join(os.path.dirname(path_to_tileset), meta['file'])
                if not os.path.exists(path):
                    raise Exception('Tileset does not exist')

                # Tileset writer & reader
                reader = SpriteSheetReader(path, tileset_config['Tileset']['Tiles'], meta['size'])
                writer = SpriteSheetWriter(meta['size'], self.size_x, self.size_y)

                for y, line in enumerate(self.tiled_map):
                    for x, tile in enumerate(line):
                        writer.add_image(reader.get_tile(tile))

        if not writer:
            raise Exception('Error during conversion to image')

        self.final_map = writer.get_img()

    def save_map(self, filename):
        if self.final_map:
            self.final_map.save(filename)
        else:
            raise Exception("There's no image to save :/")

    def show_map(self):
        if self.final_map:
            self.final_map.show()
        else:
            raise Exception("There's no image to show :/")
