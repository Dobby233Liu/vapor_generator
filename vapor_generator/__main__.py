import argparse
import PIL.Image
from . import new_vaporizer

def generate(args):
    with PIL.Image.open(args.input) as im:
        args.output.write(new_vaporizer.generate(im))

def parse(args):
    with new_vaporizer.parse(args.input) as im:
        im.save(args.output)

parser = argparse.ArgumentParser(
                prog="vapor_generator",
                description="Tool for dealing with vapor data for Undertale's obj_vaporized_new.")
subparser = parser.add_subparsers(help="Commands", required=True)

parser_generate = subparser.add_parser("generate", help="Generate a new vapor data file.")
parser_generate.add_argument("input", type=argparse.FileType("rb"), help="The input image file")
parser_generate.add_argument("output", type=argparse.FileType("wb"), help="The output data file")
parser_generate.set_defaults(func=generate)

parser_parse = subparser.add_parser("parse", help="Create an image from a vapor data file.")
parser_parse.add_argument("input", type=argparse.FileType("rb"), help="The input data file")
parser_parse.add_argument("output", type=argparse.FileType("wb"), help="The output image file")
parser_parse.set_defaults(func=parse)

args = parser.parse_args()
args.func(args)