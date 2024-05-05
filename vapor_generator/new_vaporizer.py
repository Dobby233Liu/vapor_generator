import enum
import PIL.Image, PIL.ImageOps
import itertools
import io


def chunk_generator(size: int, max_size: int):
    while size > max_size:
        yield max_size
        size -= max_size
    if size > 0:
        yield size

def make_sequence(start: bytes, size: int, max_size: int):
    ret = b''
    for i in chunk_generator(size, max_size):
        ret += bytes([start[0] + i])
    return ret

BLACK_START = b'U'
BLACK_MAX_SIZE = 36
def make_black(size: int):
    return make_sequence(BLACK_START, size, BLACK_MAX_SIZE)
BLACK_END = make_black(BLACK_MAX_SIZE)

WHITE_START = b'('
WHITE_MAX_SIZE = 42
def make_white(size: int):
    return make_sequence(WHITE_START, size, WHITE_MAX_SIZE)
WHITE_END = make_white(WHITE_MAX_SIZE)

TERMINATE_LINE = b'}'
TERMINATE_DATA = b'~'

class _DustBlockType(enum.Enum):
    Black = enum.auto()
    White = enum.auto()


def generate(im: PIL.Image.Image):
    _im = im.convert("1")

    result = b''

    for line in range(_im.height):
        block_type = None
        block_width = 0
        def write_block():
            nonlocal result, block_type
            match block_type:
                case _DustBlockType.Black:
                    result += make_black(block_width)
                case _DustBlockType.White:
                    result += make_white(block_width)

        for x in range(_im.width):
            pixel = _im.getpixel((x, line))
            this_block_type = _DustBlockType.Black if pixel == 0 else _DustBlockType.White
            if block_type is None:
                block_type = this_block_type
            if block_type != this_block_type:
                write_block()
                block_type = this_block_type
                block_width = 0
            block_width += 1
        write_block()

        result += TERMINATE_LINE

    result += TERMINATE_DATA

    return result


def _parse_pixels(data: io.BytesIO):
    while (char := data.read(1)) != TERMINATE_DATA:
        def gen_line():
            nonlocal char
            while char != TERMINATE_LINE:
                if char >= BLACK_START and char <= BLACK_END:
                    for _ in range(char[0] - BLACK_START[0]):
                        yield 0
                elif char >= WHITE_START and char <= WHITE_END:
                    for _ in range(char[0] - WHITE_START[0]):
                        yield 1
                else:
                    raise ValueError("Invalid character")
                char = data.read(1)
        yield tuple(gen_line())

def parse(data: io.BytesIO):
    result_pixels = list(_parse_pixels(data))
    width = max(len(line) for line in result_pixels)
    height = len(result_pixels)
    result = PIL.Image.new("1", (width, height), 0)
    result.putdata(tuple(itertools.chain(*result_pixels)))
    return result