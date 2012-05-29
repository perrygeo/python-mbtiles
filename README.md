## python-mbtiles

Some python tools for working with [mbtiles](http://mapbox.com/mbtiles-spec/):

>MBTiles is a specification for storing tiled map data in SQLite databases
>for immediate use and for transfer. The files are designed for portability 
>of thousands, hundreds of thousands, or even millions of standard map tile 
>images in a single file.

### Similar projects

This is nothing more than an experiment at this point. For more full-featured libraries, you may also want to check out

* [mbutil](https://github.com/mapbox/mbutil)
* [landez](https://github.com/makinacorpus/landez)

### Project Goals

#### Python classes

Abstract the details of accessing utfgrid and image data from the sqlite datastore. See `mbtiles.py`

```python
tileset = MbtileSet(mbtiles='./data/road-trip-wilderness.mbtiles')
zoom, col, row = 6, 9, 40
tile = tileset.get_tile(zoom, col, row)
binary_png = tile.get_png()
text_json = tile.get_json()
```

#### Tile web server

Provide a fast, simple, non-blocking web server (using Tornado) to serve image and utfgrid data. You are able to pass a `callback` parameter on utfgrids for dynamic JSONP allowing easy cross-domain and framework-agnostic loading of utfgrid json tiles. See `serve_mbtiles.py`

```bash
python serve_mbtiles.py # runs on 8988
wget http://localhost:8988/test/6/9/40.png
wget http://localhost:8988/test/6/9/40.json
wget http://localhost:8988/test/6/9/40.json?callback=test
wget http://localhost:8988/test/6/9/23.json?origin=top # invert y-axis for top-origin tile scheme like Google, etc.
```

#### Covert mbtiles to png/json files

A script to convert mbtiles files into png/json files on the filesystem. This eliminates the single-file advantages of mbtiles but gains portability in that tiles can be served statically without a web server in front of it. See `mbtiles2files.py`.

```bash
# Bottom-origin tiles (TMS)
python mbtiles2files.py -f data/road-trip-wilderness.mbtiles -o /tmp/output
ls /tmp/output/6/9/40.*

# Invert to top-origin tiles (Google, OSM, etc.)
python mbtiles2files.py -f data/road-trip-wilderness.mbtiles -o /tmp/output --invert
ls /tmp/output/6/9/23.*
```
### Example


### Roadmap

* Make error handling more robust
* Config file for the server (port, list of mbtiles to serve)
* Handle jpg (coding was stupidly implemented assuming png)
* Test cases, docs
* setup.py file, cheesehop it, etc.
