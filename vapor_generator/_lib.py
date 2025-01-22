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
BLACK_MAX_SIZE = b'y'[0] - BLACK_START
def make_black_code(size: int, optimize: bool = False):
    return make_code_seq(BLACK_START, size, BLACK_MAX_SIZE)
BLACK_END = make_black_code(BLACK_MAX_SIZE, True)[0]

WHITE_START = b'('[0]
WHITE_MAX_SIZE = b'R'[0] - WHITE_START
# Apparently Toby's compressor doesn't support the full range of white codes
WHITE_MAX_SIZE_TOBY = b'L'[0] - WHITE_START
def make_white_code(size: int, optimize: bool = False):
    return make_code_seq(WHITE_START, size, WHITE_MAX_SIZE if optimize else WHITE_MAX_SIZE_TOBY)
WHITE_END = make_white_code(WHITE_MAX_SIZE, True)[0]

TERMINATE_LINE = b'}'
TERMINATE_DATA = b'~'
TERMINATE_DATA_TOBY = b'~~~'

class _DustParticleType(enum.IntEnum):
    Black = 0
    White = 0xFF


def _compress(im: PIL.Image.Image, optimize=False):
    assert im.mode == "1"

    for line in range(im.height):
        part_type = None
        part_width = 0

        def make_part():
            nonlocal part_type
            match part_type:
                case _DustParticleType.Black:
                    return make_black_code(part_width, optimize)
                case _DustParticleType.White:
                    return make_white_code(part_width, optimize)
                case _:
                    assert False

        for x in range(im.width):
            part_type_here = im.getpixel((x, line))
            assert part_type_here in _DustParticleType

            if part_type is None:
                part_type = part_type_here
            elif part_type != part_type_here:
                yield make_part()
                part_type = part_type_here
                part_width = 0
            part_width += 1

        assert part_type != None
        # drop the last particle if its black; that's gonna be skipped by the
        # vanilla vaporizer anyway
        if not optimize or part_type != _DustParticleType.Black:
            yield make_part()

        if not optimize or line != (im.height - 1):
            yield TERMINATE_LINE

    if not optimize:
        yield TERMINATE_DATA_TOBY
    else:
        yield TERMINATE_DATA

def compress(im: PIL.Image.Image, optimize=False):
    data_io = io.BytesIO()
    im_gray = PIL.ImageOps.grayscale(im).convert("1")
    for chunk in _compress(im_gray, optimize=optimize):
        data_io.write(chunk)
    return data_io.getvalue()


def _decompress_to_particles(data: io.BytesIO):
    if isinstance(data, bytes):
        data = io.BytesIO(data)
    line = []
    while (char := data.read(1)[0]) and char != TERMINATE_DATA[0]:
        if char >= BLACK_START and char <= BLACK_END:
            line.append((_DustParticleType.Black, char - BLACK_START))
        # There shouldn't be any issues using the bigger white range, I THINK?
        elif char >= WHITE_START and char <= WHITE_END:
            line.append((_DustParticleType.White, char - WHITE_START))
        elif char == TERMINATE_LINE[0]:
            yield line
            line = []
        else:
            raise ValueError("Invalid character")
    if len(line) > 0:
        yield line

def _decompress_to_pixels(data: io.BytesIO):
    for line_parts in _decompress_to_particles(data):
        line_pixels = []
        for (part_type, part_width) in line_parts:
            line_pixels.extend([part_type] * part_width)
        yield line_pixels

def decompress(data: bytes|io.BytesIO):
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
