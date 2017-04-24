from map_generator.MapConverter import MapConverter

if __name__ == "__main__":
    custom_map = MapConverter("data/example_map.txt")
    custom_map.convert("data/legend.yaml", "data/tileset.yaml")
    custom_map.show_map()
    custom_map.save_map("./map.png")
