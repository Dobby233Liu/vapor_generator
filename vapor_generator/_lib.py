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

def make_code_seq(start: int, size: int, max_size: int):
    return bytes([start + i for i in break_into_chunks(size, max_size)])


BLACK_START = b'U'[0]
BLACK_MAX_SIZE = 36
def make_black_code(size: int):
    return make_code_seq(BLACK_START, size, BLACK_MAX_SIZE)
BLACK_END = make_black_code(BLACK_MAX_SIZE)[0]

WHITE_START = b'('[0]
WHITE_MAX_SIZE = 42
def make_white_code(size: int):
    return make_code_seq(WHITE_START, size, WHITE_MAX_SIZE)
WHITE_END = make_white_code(WHITE_MAX_SIZE)[0]

TERMINATE_LINE = b'}'
TERMINATE_DATA = b'~'

class _DustParticleType(enum.IntEnum):
    Black = 0
    White = 1


def _compress(im: PIL.Image.Image, optimize=False):
    assert im.mode == "1"

    for line in range(im.height):
        part_type = None
        part_width = 0

        def make_part():
            nonlocal part_type
            match part_type:
                case _DustParticleType.Black:
                    return make_black_code(part_width)
                case _DustParticleType.White:
                    return make_white_code(part_width)
                case _:
                    assert False

        for x in range(im.width):
            part_type_here = im.getpixel((x, line))
            assert part_type_here in _DustParticleType

            if part_type is None:
                part_type = part_type_here
            elif part_type != part_type_here:
                if part := make_part():
                    yield part
                part_type = part_type_here
                part_width = 0
            part_width += 1

        assert part_type != None
        # drop the last particle if its black; that's gonna be skipped by the
        # vanilla vaporizer anyway
        if not optimize or part_type != _DustParticleType.Black:
            if part := make_part():
                yield part

        yield TERMINATE_LINE

    yield TERMINATE_DATA

def compress(im: PIL.Image.Image, *args, optimize=False, **kwargs):
    data_io = io.BytesIO()
    for chunk in _compress(im.convert("1"), *args, optimize=optimize, **kwargs):
        data_io.write(chunk)
    return data_io.getvalue()


def _decompress_to_pixels(data: io.BytesIO):
    line = []
    while (char := data.read(1)[0]) and char != TERMINATE_DATA[0]:
        if char >= BLACK_START and char <= BLACK_END:
            for _ in range(char - BLACK_START):
                line.append(0)
        elif char >= WHITE_START and char <= WHITE_END:
            for _ in range(char - WHITE_START):
                line.append(1)
        elif char == TERMINATE_LINE[0]:
            yield line
            line = []
        else:
            raise ValueError("Invalid character")
    if len(line) > 0:
        yield line

def decompress(data: bytes|io.BytesIO):
    if isinstance(data, bytes):
        data = io.BytesIO(data)
    result_pixels = list(_decompress_to_pixels(data))

    width = max(len(line) for line in result_pixels)
    height = len(result_pixels)
    assert width > 0 and height > 0

    for i, line in enumerate(result_pixels):
        if len(line) < width:
            result_pixels[i] = line + [0] * (width - len(line))

    result = PIL.Image.new("1", (width, height), 0)
    result.putdata(tuple(itertools.chain(*result_pixels)))
    return result


# TODO: more?
__all__ = [
    "compress",
    "decompress",
]