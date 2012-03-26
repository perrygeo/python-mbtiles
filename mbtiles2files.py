from mbtiles import MbtileSet
import optparse

if __name__ == '__main__':
    parser = optparse.OptionParser(
            usage="\nOutputs png/json files from an mbtiles file\nmbtiles2files.py [options] -f <mbtiles file> -o <output dir>")
    parser.add_option('-f', '--file', help='Path to .mbtiles file', action='store', 
            dest='file', type='string')
    parser.add_option('-o', '--output', help='Output directory', action='store', 
            dest='output', type='string')
    parser.add_option('-i', '--invert', help='Invert Y axis (True = Top Y origin ala google and bing)', action='store_true', 
            dest='invert', default=False)
    (opts, args) = parser.parse_args()

    if not opts.file:
        parser.error("Please specify a valid .mbtiles file")
    if not opts.output:
        parser.error("Please specify and output directory")

    origin = "bottom"
    if opts.invert:
        origin = "top"

    tileset = MbtileSet(mbtiles=opts.file, outdir=opts.output, origin=origin)
    tileset.write_all()
