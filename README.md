## level2map
Purpose of this repository is to convert a single image of a 2D level into a complete map (tilesheet image anlong with data file).

Levels can be downloaded from [http://vgmaps.com/].

## Procedure
#### 1. Download a map
  vgmaps.com is a perfect source
  
#### 2. Cleaning the level with Image Editor
The map you downloaded may have stichting issues. For example, a row of pixels may have been duplicated. The level2map tool is very basic, so removing these artefacts is necessary.
 
#### 3. Run level2map
```sh
$ python level2map.py level.png outputDir/ data/myJson.json outputSheet.png 16
```
The tool will scan the image and find all unique tiles and place them in tileOutputDir.

### 4.Run TexturePacker
level2map will have created ordered tiles starting from 00001.png. Use texturePacker to pack them into a single image.
```sh
TexturePacker --sheet outputSheet.png inputDir/ --trim-mode None \
--shape-padding 0 --border-padding 0 --size-constraints POT \
--basic-sort-by Name --algorithm Basic
```
### 5. Open Tiled
Open Tiled and load the data file from level2map.

### Version
1.0
