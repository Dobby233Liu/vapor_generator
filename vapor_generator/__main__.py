import argparse
import PIL.Image
from . import new_vaporizer

def compress(args):
    with PIL.Image.open(args.input) as im:
        args.output.write(new_vaporizer.compress(im))

def decompress(args):
    with new_vaporizer.decompress(args.input) as im:
        im.save(args.output)

parser = argparse.ArgumentParser(
                prog="vapor_generator",
                description="(De)compressor for the basic ASCII-based RLE used by Undertale's obj_vaporized_new.")
subparser = parser.add_subparsers(help="Commands", required=True)

parser_generate = subparser.add_parser("compress", help="Compresses an image to a vapor data file.")
parser_generate.add_argument("input", type=argparse.FileType("rb"), help="The input image file")
parser_generate.add_argument("output", type=argparse.FileType("wb"), help="The output data file")
parser_generate.set_defaults(func=compress)

parser_parse = subparser.add_parser("decompress", help="Decompresses a vapor data file to an image.")
parser_parse.add_argument("input", type=argparse.FileType("rb"), help="The input data file")
parser_parse.add_argument("output", type=argparse.FileType("wb"), help="The output image file")
parser_parse.set_defaults(func=decompress)

args = parser.parse_args()
args.func(args)