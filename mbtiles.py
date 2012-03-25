import sqlite3
import sys
import zlib
import json
import os


class MbtileSet:

    def __init__(self, mbtiles, outdir=None):
        self.conn = sqlite3.connect(mbtiles)
        self.outdir = outdir

    def write_all(self):
        if not self.outdir:
            raise Exception("Must specify the outdir property to write_all")
        cur = self.conn.cursor()
        for row in cur.execute('select zoom_level, tile_column, tile_row from map'):
            z, x, y = row[:3]
            tile = Mbtile(z, x, y, self.conn)
            tile.write_png(self.outdir)
            tile.write_json(self.outdir)

    def get_tile(self, z, x, y):
        return Mbtile(z, x, y, self.conn)


class Mbtile:

    def __init__(self, z, x, y, conn):
        self.zoom = z
        self.col = x
        self.row = y
        self.conn = conn

    def get_png(self):
        c = self.conn.cursor()
        c.execute('''select tile_data from tiles 
                      where zoom_level = %s 
                      and tile_column = %s 
                      and tile_row = %s''' % (self.zoom,self.col,self.row))
        row = c.fetchone()
        if not row:
            return None

        return bytes(row[0])

    def get_json(self):
        c = self.conn.cursor()
        c2 = self.conn.cursor()
        c.execute('''select grid from grids 
                     where zoom_level = %s 
                     and tile_column = %s 
                     and tile_row = %s''' % (self.zoom,self.col,self.row))
        row = c.fetchone()
        if not row:
            return None

        bt = bytes(row[0])
        j = zlib.decompress(bt)
        tgd = json.loads(j)

        kq = '''
            SELECT
                keymap.key_name AS key_name,
                keymap.key_json AS key_json
            FROM map
            JOIN grid_utfgrid ON grid_utfgrid.grid_id = map.grid_id
            JOIN grid_key ON grid_key.grid_id = map.grid_id
            JOIN keymap ON grid_key.key_name = keymap.key_name
            WHERE zoom_level = %s AND tile_column = %s AND tile_row = %s;
        ''' % (self.zoom, self.col, self.row)
        keys = []
        for keyrow in c2.execute(kq):
            keyname, keydata = keyrow  
            keys.append((keyname, eval(keydata))) 
        datadict = dict(keys)
        tgd[u'data'] = datadict

        return json.dumps(tgd)

    def write_png(self, outdir):
        z, x, y = [str(i) for i in [self.zoom, self.col, self.row]] 
        pngdir = os.path.join(outdir, z, x) 
        try:
            os.makedirs(pngdir)
        except OSError:
            pass
        fh = open(os.path.join(pngdir, y + ".png"), 'wb')
        fh.write(self.get_png())
        fh.close()

    def write_json(self, outdir):
        z, x, y = [str(i) for i in [self.zoom, self.col, self.row]] 
        jsondir = os.path.join(outdir, z, x) 
        try:
            os.makedirs(jsondir)
        except OSError:
            pass
        fh = open(os.path.join(jsondir, y + ".json"), 'w')
        fh.write(self.get_json())
        fh.close()
