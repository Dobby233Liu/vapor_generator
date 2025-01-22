import enum
from typing import Generator, List, Tuple
import PIL.Image, PIL.ImageOps
import itertools
import io


def break_into_chunks(size: int, max_size: int) -> Generator[int, None, None]:
    """
    Breaks a size into chunks of at most max_size
    """

    if size < 0:
        raise ValueError("Size must be non-negative")
    if size <= max_size:
        yield size
        return

    while size > max_size:
        yield max_size
        size -= max_size
    if size > 0:
        yield size

def make_code_seq(start: int, size: int, max_size: int) -> bytes:
    """
    Makes a sequence of bytes representing the given size
    """

    if size < 0:
        raise ValueError("Size must be non-negative")
    if size <= max_size:
        return bytes([start + size])

    return bytes([start + i for i in break_into_chunks(size, max_size)])


BLACK_START = b'U'[0]
BLACK_MAX_SIZE = b'y'[0] - BLACK_START
def make_black_code(size: int, optimize: bool = False):
    return make_code_seq(BLACK_START, size, BLACK_MAX_SIZE)
BLACK_END = make_black_code(BLACK_MAX_SIZE, True)[0]

WHITE_START = b'('[0]
WHITE_MAX_SIZE = b'R'[0] - WHITE_START
# Apparently Toby's compressor assumes this is the maximum size
WHITE_MAX_SIZE_TOBY = b'L'[0] - WHITE_START
def make_white_code(size: int, optimize: bool = False):
    return make_code_seq(WHITE_START, size, WHITE_MAX_SIZE if optimize else WHITE_MAX_SIZE_TOBY)
WHITE_END = make_white_code(WHITE_MAX_SIZE, True)[0]

TERMINATE_LINE = b'}'
TERMINATE_DATA = b'~'
TERMINATE_DATA_TOBY = b'~~~'

class _DustParticleType(enum.IntEnum):
    # Note that this must map to corresponding colors in PIL's 1-bit color mode
    Black = 0
    White = 0xFF


def _compress(im: PIL.Image.Image, optimize=False) -> Generator[bytes, None, None]:
    assert im.mode == "1"
    assert im.width > 0

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

        # For the last line, TERMINATE_DATA is enough to make the read loop stop
        if not optimize or line != (im.height - 1):
            yield TERMINATE_LINE

    if not optimize:
        yield TERMINATE_DATA_TOBY
    else:
        yield TERMINATE_DATA

def compress(im: PIL.Image.Image, optimize=False) -> bytes:
    """
    Compresses an image to vapor data
    """

    im_gray = PIL.ImageOps.grayscale(im).convert("1")
    return bytes(byte for chunk in _compress(im_gray, optimize=optimize) for byte in chunk)


def _decompress_to_particles(data: io.BytesIO) -> Generator[List[Tuple[_DustParticleType, int]], None, None]:
    if isinstance(data, bytes):
        data = io.BytesIO(data)

    line = []
    while (char := data.read(1)[0]) and char != TERMINATE_DATA[0]:
        if char >= BLACK_START and char <= BLACK_END:
            line.append((_DustParticleType.Black, char - BLACK_START))
        elif char >= WHITE_START and char <= WHITE_END:
            line.append((_DustParticleType.White, char - WHITE_START))
        elif char == BLACK_START - 1 or char == WHITE_START - 1:
            # These technically aren't invalid (handled by Undertale), but would imply
            # -1 length!?
            # Toby code sucks, let's just ignore this
            pass
        elif char == TERMINATE_LINE[0]:
            yield line
            line = []
        else:
            raise ValueError("Invalid character")
    if len(line) > 0:
        yield line

def _decompress_to_pixels(data: io.BytesIO) -> Generator[List[_DustParticleType], None, None]:
    for line_parts in _decompress_to_particles(data):
        line_pixels = []
        for (part_type, part_width) in line_parts:
            line_pixels.extend([part_type] * part_width)
        yield line_pixels

def decompress(data: bytes|io.BytesIO) -> PIL.Image.Image:
    """
    Decompresses vapor data to an image
    """

    result_pixels = list(_decompress_to_pixels(data))

    height = len(result_pixels)
    assert height > 0
    width = max(len(line) for line in result_pixels)
    assert width > 0

    # pad lines to the right width
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
