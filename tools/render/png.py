"""A PNG writer and a scanline polygon rasterizer, in the standard library alone.

The repository takes no runtime dependency it did not review, and an image writer is small enough that
vendoring one would cost more than writing it. Everything here is RGB8: a canvas is a bytearray of
`width * height * 3`, and `write_png` deflates it into the one chunk sequence a decoder needs."""
import struct
import zlib


class Canvas:
    """An RGB byte canvas with the three drawing operations an isometric render needs: a filled convex
    polygon, a line, and a run of text from the built-in 5x7 face."""

    def __init__(self, width, height, background=(255, 255, 255)):
        self.width = width
        self.height = height
        self.pixels = bytearray(bytes(background) * (width * height))

    def set(self, x, y, colour):
        if 0 <= x < self.width and 0 <= y < self.height:
            offset = (y * self.width + x) * 3
            self.pixels[offset:offset + 3] = bytes(colour)

    def fill_polygon(self, points, colour, alpha=1.0):
        """Scanline-fill a polygon. Points are (x, y) floats; the even-odd rule decides the interior, so a
        self-intersecting outline fills the way a rasterizer would rather than raising.

        `alpha` below 1 mixes the colour into what is already on the canvas instead of replacing it. The
        mix is a per-channel table built once for the whole polygon, so a translucent face costs one table
        lookup a byte rather than a multiply."""
        if len(points) < 3:
            return
        ys = [p[1] for p in points]
        top = max(0, int(min(ys)))
        bottom = min(self.height - 1, int(max(ys)) + 1)
        rgb = bytes(colour)
        mix = None if alpha >= 1 else [
            bytes(int(channel * alpha + under * (1 - alpha)) for under in range(256))
            for channel in colour]
        for y in range(top, bottom + 1):
            centre = y + 0.5
            crossings = []
            for i in range(len(points)):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % len(points)]
                if (y0 <= centre < y1) or (y1 <= centre < y0):
                    crossings.append(x0 + (centre - y0) * (x1 - x0) / (y1 - y0))
            crossings.sort()
            for i in range(0, len(crossings) - 1, 2):
                left = max(0, int(crossings[i] + 0.5))
                right = min(self.width, int(crossings[i + 1] + 0.5))
                if right > left:
                    offset = (y * self.width + left) * 3
                    width = (right - left) * 3
                    if mix is None:
                        self.pixels[offset:offset + width] = rgb * (right - left)
                    else:
                        self.pixels[offset:offset + width] = bytes(
                            mix[i % 3][under]
                            for i, under in enumerate(self.pixels[offset:offset + width]))

    def line(self, x0, y0, x1, y1, colour):
        steps = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for i in range(steps + 1):
            t = i / steps
            self.set(int(round(x0 + (x1 - x0) * t)), int(round(y0 + (y1 - y0) * t)), colour)

    def rect(self, x0, y0, x1, y1, colour):
        self.fill_polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], colour)

    def text(self, x, y, message, colour=(0, 0, 0), scale=2):
        """The 5x7 face below, left-aligned at (x, y), one pixel of tracking per scale unit."""
        cursor = x
        for char in message.upper():
            glyph = FONT.get(char, FONT["?"])
            for row, bits in enumerate(glyph):
                for col in range(5):
                    if bits & (1 << (4 - col)):
                        for dy in range(scale):
                            for dx in range(scale):
                                self.set(cursor + col * scale + dx, y + row * scale + dy, colour)
            cursor += 6 * scale

    def text_width(self, message, scale=2):
        return len(message) * 6 * scale


def write_png(path, canvas):
    raw = bytearray()
    stride = canvas.width * 3
    for y in range(canvas.height):
        raw.append(0)                                     # filter: none
        raw += canvas.pixels[y * stride:(y + 1) * stride]

    def chunk(tag, payload):
        return (struct.pack(">I", len(payload)) + tag + payload
                + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF))

    with open(path, "wb") as out:
        out.write(b"\x89PNG\r\n\x1a\n")
        out.write(chunk(b"IHDR", struct.pack(">IIBBBBB", canvas.width, canvas.height, 8, 2, 0, 0, 0)))
        out.write(chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
        out.write(chunk(b"IEND", b""))


def shade(colour, factor):
    """One colour under a face's light. Above 1 lightens toward white rather than clipping to it, so a
    lit face of a pale block stays distinguishable from its neighbour."""
    if factor <= 1:
        return tuple(max(0, min(255, int(c * factor))) for c in colour)
    return tuple(max(0, min(255, int(c + (255 - c) * (factor - 1)))) for c in colour)


def desaturate(colour, amount):
    """One colour pulled toward its own grey, `amount` 0 leaving it alone and 1 flattening it to
    luminance. What it buys is a second axis beside brightness: mass drawn at full value but no chroma
    still reads as ground, and whatever keeps its chroma reads as the subject."""
    grey = 0.299 * colour[0] + 0.587 * colour[1] + 0.114 * colour[2]
    return tuple(max(0, min(255, int(c + (grey - c) * amount))) for c in colour)


def hex_rgb(text):
    text = text.lstrip("#")
    return (int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16))


# A 5x7 bitmap face — one tuple of seven row-bitmasks per character, high bit leftmost.
FONT = {
    " ": (0, 0, 0, 0, 0, 0, 0),
    "A": (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "B": (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    "C": (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    "D": (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    "E": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    "F": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    "G": (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    "H": (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "I": (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "J": (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    "K": (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    "L": (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    "M": (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    "N": (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    "O": (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "P": (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    "Q": (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    "R": (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    "S": (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    "T": (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    "U": (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "V": (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    "W": (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11),
    "X": (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    "Y": (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    "Z": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    "0": (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    "1": (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "2": (0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F),
    "3": (0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E),
    "4": (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    "5": (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    "6": (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    "7": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    "8": (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    "9": (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
    "-": (0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00),
    "+": (0x00, 0x04, 0x04, 0x1F, 0x04, 0x04, 0x00),
    ".": (0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C),
    ",": (0x00, 0x00, 0x00, 0x00, 0x0C, 0x04, 0x08),
    ":": (0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x0C, 0x00),
    "/": (0x01, 0x02, 0x02, 0x04, 0x08, 0x08, 0x10),
    "(": (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ")": (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    "x": (0x00, 0x00, 0x0A, 0x04, 0x0A, 0x00, 0x00),
    "?": (0x0E, 0x11, 0x01, 0x02, 0x04, 0x00, 0x04),
    "!": (0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04),
    "'": (0x04, 0x04, 0x08, 0x00, 0x00, 0x00, 0x00),
    "=": (0x00, 0x00, 0x1F, 0x00, 0x1F, 0x00, 0x00),
    "#": (0x0A, 0x1F, 0x0A, 0x0A, 0x0A, 0x1F, 0x0A),
    "%": (0x18, 0x19, 0x02, 0x04, 0x08, 0x13, 0x03),
    "@": (0x0E, 0x11, 0x17, 0x15, 0x17, 0x10, 0x0E),
}
