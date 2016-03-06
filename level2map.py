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

# Start off with some defaults
dictTest = {
    "height": -1,
    "width": -1,

    "tilewidth": -1,
    "tileheight": -1,

    "version": 1,
    "nextobjectid": 1,
    "orientation": "orthogonal",
    "renderorder": "right-down",

    "layers": [{
        "data": [],  # we fill this up...

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
        "columns": 8,
        "firstgid": 1,
        "image": "",
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
        dataFolder = sys.argv[2]
        #texturePackerSheet = sys.argv[3]
        tileSize = int(sys.argv[3])

        splitTilesFolder = '.temp/'
        tileSheetFileName = 'tileSheet.png'

        try:
            os.makedirs(dataFolder)
            os.makedirs(splitTilesFolder)
        except OSError as exception:
            pass

        # Need to clear out the temp folder
        os.system('rm .temp/*.png')

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
                    # texturePacker needs leading zeros to properly put tiles
                    # in order
                    fileName = str(tileNameIndex).zfill(4)

                    tile.save(splitTilesFolder + '/%s.png' % (fileName))
                    uniqueTiles[tileHash] = [tileNameIndex, tile]
                    tileNameIndex += 1
                else:
                    pass

                tileIndex = uniqueTiles[tileHash][0]

                # Only using 1 layer
                dictTest['tilewidth'] = tileSize
                dictTest['tileheight'] = tileSize
                dictTest['width'] = numCols
                dictTest['height'] = numRows
                dictTest['layers'][0]['width'] = numCols
                dictTest['layers'][0]['height'] = numRows
                dictTest['layers'][0]['data'].append(tileIndex)
                # //'layers'][0]['data'].append(tileIndex)
                dictTest['tilesets'][0]['image'] = tileSheetFileName

        print("Unique Tiles Found: %s" % (len(uniqueTiles)))
        
        # write out Tiled data file
        obj = open('data/data.json', 'wb')
        jsonOut = json.dumps(dictTest)
        obj.write(jsonOut)
        obj.close()

        texturePackerCommand = ''.join(['TexturePacker ',
                                        ' --sheet ', dataFolder, '/', tileSheetFileName, ' ',
                                        splitTilesFolder,
                                        ' --trim-mode None',
                                        ' --shape-padding 0',
                                        ' --border-padding 0',
                                        ' --size-constraints POT',
                                        ' --basic-sort-by Name --algorithm Basic'
                                        ' --quiet'
                                        ])

        os.system(texturePackerCommand)
        os.system('rm out.plist')

if __name__ == "__main__":
    sys.exit(main())
