## python-mbtiles

Some python tools for working with [mbtiles](http://mapbox.com/mbtiles-spec/):

```
MBTiles is a specification for storing tiled map data in SQLite databases for immediate use and for transfer. The files are designed for portability of thousands, hundreds of thousands, or even millions of standard map tile images in a single file.
```

### This project has three goals:

1. Abstract the details of accessing utfgrid and image data from the sqlite datastore. See `mbtiles.py`
2. Provide a fast, simple, non-blocking web server (using Tornado) to serve image and utfgrid data. You are able to pass a `callback` parameter on utfgrids for dynamic JSONP allowing easy cross-domain and framework-agnostic loading of utfgrid json tiles. See `serve_mbtiles.py`
3. A script to convert mbtiles files into png/json files on the filesystem. This eliminates the single-file advantages of mbtiles but gains portability in that tiles can be served statically without a web server in front of it. See `mbtiles2files.py`.

### Roadmap
This is nothing more than an experiment at this point. I would, however, like to:

* Make error handling more robust
* Test cases
* setup.py file, cheeshop it, etc.
