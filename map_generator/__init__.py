"""
    The ``map_generator`` module
    ======================

    Convert an ascii map to an image

    Wall direction
    --------------
      1
    8 # 2
      4
    Sum the value of the current wall's neighbour to find the correct tile.
    Example:
        #
        # #   Sum = 3 --> tag: wall3
      

"""
