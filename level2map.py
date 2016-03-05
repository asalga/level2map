"""
    Purpose of this script is to convert a map from vgmaps
    into a unique set of tiles and an atlas.
"""

import sys
import hashlib
import getopt
import os
import json
from PIL import Image


# Start off with some defaults
dictTest = {
    "height": 15,
    "width": 213,

    "tilewidth": 16,
    "version": 1,

    "layers": [{
        "data": [],
        
        "height": 15,
        "width": 213,

        "name": "Tile Layer 1",
        "opacity": 1,
        "type": "tilelayer",
        "visible": True,
        
        "x": 0,
        "y": 0
    }],
    "nextobjectid": 1,
    "orientation": "orthogonal",
    "renderorder": "right-down",
    "tileheight": 16,

    "tilesets": [{
        "columns": 8,
        "firstgid": 1,
        "image": "pythonMap2Atlas/tpTest.png",
        "imageheight": 128,
        "imagewidth": 128,
        "margin": 0,
        "name": "tpTest",
                "spacing": 0,
                "tilecount": 64,
                "tileheight": 16,
                "tilewidth": 16
    }]
}


def main(argv=None):

    if len(sys.argv) == 4:

        rawMap = Image.open(sys.argv[1])
        outputDir = sys.argv[2]
        tileSize = int(sys.argv[3])

        try:
            os.makedirs(outputDir)
        except OSError as exception:
            pass

        # Start with 1 since Tiled program uses 0 as empty cell
        tileNameIndex = 1

        rawMapWidth, rawMapHeight = rawMap.size

        print('Raw map dimensions: [%s, %s]' % (rawMapWidth, rawMapHeight))

        uniqueTiles = {}

        row = 0
        col = 0

        numCols = rawMapWidth / tileSize
        numRows = rawMapHeight / tileSize

        # dictTest['layers'][0]['data'] = [5,1,5,1,5,1]

        print('Total Tiles: %s' %
              str(rawMapWidth / tileSize * rawMapHeight * tileSize)
              )

        
        for y in range(0, numRows):
            for x in range(0, numCols):

                xCoord = x * tileSize
                yCoord = y * tileSize

                tile = rawMap.crop(
                    (xCoord, yCoord, xCoord + tileSize, yCoord + tileSize)
                )

                # Create hash for tile
                tileString = str(list(tile.getdata()))[1:-1]
                tileHash = hashlib.md5(tileString).hexdigest()

                if not tileHash in uniqueTiles:
                    fileName = str(tileNameIndex).zfill(4)

                    # if tileNameIndex < 10
                    #     fileName = 
                    # else if tileNameIndex < 100
                    #     fileName = str(tileNameIndex).zfill(3)
                    # else if tileNameIndex < 1000
                    #     fileName = str(tileNameIndex).zfill(2)

                    tile.save(outputDir + '/%s.png' % (fileName))
                    uniqueTiles[tileHash] = [tileNameIndex, tile]
                    tileNameIndex += 1
                else:
                    pass

                tileIndex = uniqueTiles[tileHash][0]
                dictTest['layers'][0]['data'].append(tileIndex)

        # print("Unique Tiles Found: %s" % (len(uniqueTiles)))
        print("Finished Script")

        # write out data
        obj = open('../mytest.json', 'wb')
        jsonOut = json.dumps(dictTest)
        obj.write(jsonOut)
        obj.close()

if __name__ == "__main__":
    sys.exit(main())
