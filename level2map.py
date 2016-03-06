"""
    Purpose of this script is to convert a map from vgmaps
    into a unique set of tiles and an atlas.
"""

import sys
import os
import hashlib
import getopt
import json
from PIL import Image

# Start off with some defaults. Any -1 or null value will be
# populated by our script before writing out the data file.
dataForTiled = {
    "height": -1,
    "width": -1,
    "tilewidth": -1,
    "tileheight": -1,

    "version": 1,
    "nextobjectid": 1,
    "orientation": "orthogonal",
    "renderorder": "right-down",

    "layers": [{
        # we fill this up with data
        "data": [],

        "height": -1,
        "width": -1,

        "name": "Tile Layer 1",
        "opacity": 1,
        "type": "tilelayer",
        "visible": True,

        "x": 0,
        "y": 0
    }],

    "tilesets": [{
        "name": "null",
        "image": "null",
        "firstgid": 1,
        "spacing": 0,
        "margin": 0,
        "tileheight": -1,
        "tilewidth": -1,
        "tilecount": -1,

        "imageheight": 128,
        "imagewidth": 128,

        "columns": 8
    }]
}

# given 126, this returns 128


def nextPOT(v):
    math.trunc(math.pow(2, math.ceil(math.log(v) / math.log(2))))


def main(argv=None):

    if len(sys.argv) == 4:

        rawMap = Image.open(sys.argv[1])
        dataFolder = sys.argv[2]
        tileSize = int(sys.argv[3])

        splitTilesFolder = '.temp/'
        tileSheetFileName = 'tileSheet.png'
        dataFileName = 'data.json'
        # texPackDatFile = 'tpData.plist'

        texPathDataPath = ''.join([dataFolder, '/', 'tpData.plist'])
        texPackSheetPath = ''.join([dataFolder, '/', tileSheetFileName])

        try:
            os.makedirs(dataFolder)
            os.makedirs(splitTilesFolder)
        except OSError as exception:
            pass

        # Clear out the temp folder in case we had other tiles there
        os.system(''.join(['rm ', splitTilesFolder, '*.png']))

        # Start with 1 since Tiled program uses 0 as empty cell
        tileNameIndex = 1

        rawMapWidth, rawMapHeight = rawMap.size

        # print('Raw map dimensions: [%s, %s]' % (rawMapWidth, rawMapHeight))
        uniqueTiles = {}

        row = 0
        col = 0

        numCols = rawMapWidth / tileSize
        numRows = rawMapHeight / tileSize

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
                    # texturePacker needs leading zeros to put tiles in
                    # ascending order
                    fileName = str(tileNameIndex).zfill(4)

                    tile.save(splitTilesFolder + '/%s.png' % (fileName))
                    uniqueTiles[tileHash] = [tileNameIndex, tile]
                    tileNameIndex += 1
                else:
                    pass

                tileIndex = uniqueTiles[tileHash][0]
                dataForTiled['layers'][0]['data'].append(tileIndex)

        # Finish populating the rest of the necessary Tiled data
        dataForTiled['tilewidth'] = tileSize
        dataForTiled['tileheight'] = tileSize
        dataForTiled['width'] = numCols
        dataForTiled['height'] = numRows
        dataForTiled['layers'][0]['width'] = numCols
        dataForTiled['layers'][0]['height'] = numRows
        dataForTiled['tilesets'][0]['image'] = tileSheetFileName
        dataForTiled['tilesets'][0]['name'] = ''.join(['tileSheet_', sys.argv[1]])
        dataForTiled['tilesets'][0]['tileheight'] = tileSize
        dataForTiled['tilesets'][0]['tilewidth'] = tileSize
        dataForTiled['tilesets'][0]['tilecount'] = len(uniqueTiles)

        # We can use this as long we are using size-constraint in TexturePacker command
        # print nextPOT
        # Get data from plist
        texPackDatFile = open(texPathDataPath, 'r')
        


        # Need to get the dimensions from texutrePacker plist file

        # print("Unique Tiles Found: %s" % (len(uniqueTiles)))

        # Creates the tilesheet and texturePacker data file
        texturePackerCommand = ''.join(['TexturePacker ',
                                        ' --sheet ', texPackSheetPath,
                                        ' --data ', texPathDataPath,
                                        ' ', splitTilesFolder,
                                        ' --trim-mode None',
                                        ' --format json-array',
                                        ' --shape-padding 0',
                                        ' --border-padding 0',
                                        # ' --force-squared ',
                                        ' --size-constraints POT',
                                        ' --basic-sort-by Name --algorithm Basic'
                                        ' --quiet'
                                        ])

        os.system(texturePackerCommand)

        # Write the data file for Tiled
        tiledFile = ''.join([dataFolder, '/', dataFileName])
        obj = open(tiledFile, 'wb')
        jsonOut = json.dumps(dataForTiled)
        obj.write(jsonOut)
        obj.close()

if __name__ == "__main__":
    sys.exit(main())
