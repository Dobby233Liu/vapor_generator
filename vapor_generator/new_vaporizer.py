import enum
import PIL.Image, PIL.ImageOps
import itertools
import io


def break_into_chunks(size: int, max_size: int):
    while size > max_size:
        yield max_size
        size -= max_size
    if size > 0:
        yield size

def make_code_seq(start: bytes, size: int, max_size: int):
    ret = b''
    for i in break_into_chunks(size, max_size):
        ret += bytes([start[0] + i])
    return ret


BLACK_START = b'U'
BLACK_MAX_SIZE = 36
def make_black_code(size: int):
    return make_code_seq(BLACK_START, size, BLACK_MAX_SIZE)
BLACK_END = make_black_code(BLACK_MAX_SIZE)

WHITE_START = b'('
WHITE_MAX_SIZE = 42
def make_white_code(size: int):
    return make_code_seq(WHITE_START, size, WHITE_MAX_SIZE)
WHITE_END = make_white_code(WHITE_MAX_SIZE)

TERMINATE_LINE = b'}'
TERMINATE_DATA = b'~'

class _DustBlockType(enum.Enum):
    Black = enum.auto()
    White = enum.auto()


def _compress(im: PIL.Image.Image):
    _im = im.convert("1")

    for line in range(_im.height):
        block_type = None
        block_width = 0
        def make_block():
            nonlocal block_type
            match block_type:
                case _DustBlockType.Black:
                    return make_black_code(block_width)
                case _DustBlockType.White:
                    return make_white_code(block_width)

        for x in range(_im.width):
            pixel = _im.getpixel((x, line))
            this_block_type = _DustBlockType.Black if pixel == 0 else _DustBlockType.White
            if block_type is None:
                block_type = this_block_type
            if block_type != this_block_type:
                if block := make_block():
                    yield block
                block_type = this_block_type
                block_width = 0
            block_width += 1
        if block := make_block():
            yield block

        yield TERMINATE_LINE

    yield TERMINATE_DATA

def compress(im: PIL.Image.Image):
    data_io = io.BytesIO()
    for chunk in _compress(im):
        data_io.write(chunk)
    return data_io.getvalue()


def _decompress(data: io.BytesIO):
    line = []
    while (char := data.read(1)) and char != TERMINATE_DATA:
        if char >= BLACK_START and char <= BLACK_END:
            for _ in range(char[0] - BLACK_START[0]):
                line.append(0)
        elif char >= WHITE_START and char <= WHITE_END:
            for _ in range(char[0] - WHITE_START[0]):
                line.append(1)
        elif char == TERMINATE_LINE:
            yield line
            line = []
        else:
            raise ValueError("Invalid character")
    if len(line) > 0:
        yield line

def decompress(data: bytes|io.BytesIO):
    if isinstance(data, bytes):
        data = io.BytesIO(data)
    result_pixels = list(_decompress(data))

    width = max(len(line) for line in result_pixels)
    height = len(result_pixels)
    assert width > 0 and height > 0

    result = PIL.Image.new("1", (width, height), 0)
    result.putdata(tuple(itertools.chain(*result_pixels)))
    return result