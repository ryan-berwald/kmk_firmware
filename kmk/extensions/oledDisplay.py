import displayio
from adafruit_displayio_ssd1306 import SSD1306
from busio import I2C
from kmk.extensions import Extension
from kmk.kmktime import sleep_ms
import struct
try:
    from bitmaptools import readinto as _bitmap_readinto
except ImportError:
    _bitmap_readinto = None  # pylint: disable=invalid-name
import sys

class bmpInfo:
    def __init__(self, _path = "images\\f.bmp"):
        self.path = _path
        self.palette = self.getColorPalette()
        with open(_path, "rb") as bmp:
            bmp.read(10)
            self.dataOffset = struct.unpack('I', bmp.read(4))
            self.DIBHeaderSize = struct.unpack('I', bmp.read(4))
            self.width = struct.unpack('I', bmp.read(4))
            self.height = struct.unpack('I', bmp.read(4))
            self.colorPlanes = struct.unpack('H', bmp.read(2))
            self.bitsPerPixel = struct.unpack('H', bmp.read(2))
            self.compressionMethod = struct.unpack('I', bmp.read(4))
            bmp.read(4)
            bmp.read(4)
            bmp.read(4)
            bmp.read(4)
            self.numColors = struct.unpack('I', bmp.read(4))
        self.bitmap = createBitmap()


    def display(self):
        print("Data offset: %s" % self.dataOffset)
        print("DIB Header: %s" % self.DIBHeaderSize)
        print("Width: %s" % self.width)
        print("Height: %s" % self.height)
        print("Color Planes: %s" % self.colorPlanes)
        print("Bits Per Pixel: %s" % self.bitsPerPixel)
        print("Compression Method: %s" % self.compressionMethod)
        print("Number of Colors: %s" % self.numColors)
        print("Palette: %s" % self.palette)
        print("Bitmap: %s" % self.bitmap)

    def getColorPalette(self):
        palette = displayio.Palette(self.numColors)
        with open(self.path, "rb") as f:
            f.seek(self.dataOffset - (self.numColors * 4))
            for val in range(self.numColors):
                try:
                    c_bytes = f.read(4)
                    palette[val] = b''.join([c_bytes[3:], c_bytes[2:3], c_bytes[1:2]])
                except Exception as e:
                    print(e)
        return palette

    def createBitmap(self):
        minimum_color_depth = 1
        while colors > 2 ** minimum_color_depth:
            minimum_color_depth *= 2

        if sys.maxsize > 1073741823:
            # pylint: disable=import-outside-toplevel, relative-beyond-top-level
            from .negative_height_check import negative_height_check
            # convert unsigned int to signed int when height is negative
            self.height = negative_height_check(self.height)

        file = open(self.path)
        bitmap = bitmap(self.width, abs(self.height), self.palette)
        file.seek(self.dataOffset)
        line_size = self.width // (8 // self.colorPlanes)
        if self.width % (8 // self.colorPlanes) != 0:
            line_size += 1
        if line_size % 4 != 0:
            line_size += 4 - line_size % 4

        mask = (1 << self.colorPlanes) - 1
        if self.height > 0:
            range1 = self.height - 1
            range2 = -1
            range3 = -1
        else:
            range1 = 0
            range2 = abs(self.height)
            range3 = 1

        if self.compressionMethod == 0:

            if _bitmap_readinto:
                _bitmap_readinto(
                    bitmap,
                    file,
                    bits_per_pixel=self.colorPlanes,
                    element_size=4,
                    reverse_pixels_in_element=True,
                    reverse_rows=True,
                )

            else:  # use the standard file.readinto
                chunk = bytearray(line_size)
                for y in range(range1, range2, range3):
                    file.readinto(chunk)
                    pixels_per_byte = 8 // self.colorPlanes
                    offset = y * self.width

                    for x in range(self.width):
                        i = x // pixels_per_byte
                        pixel = (
                            chunk[i] >> (8 - color_depth * (x % pixels_per_byte + 1))
                        ) & mask
                        bitmap[offset + x] = pixel
        elif compression in (1, 2):
            decode_rle(
                bitmap=bitmap,
                file=file,
                compression=self.compressionMethod,
                y_range=(range1, range2, range3),
                width=self.width,
            )
        return bitmap

class oled(Extension):
    def __init__(self, SDA, SCL, _text, _width=128, _height=32):
        releaseDisp()
        self.oText = _text
        self.width = _width
        self.height = _height
        self.border = 5
        self.display = SSD1306(displayio.I2CDisplay(I2C(SDA, SCL), device_address=0x3C), width=self.width, height=self.height)
        self.prevTime = 0

    def updateOLED(self):
        try:
            bmpinfo = bmpInfo("images\\f.bmp")
            bmpinfo.display()
        except Exception as e:
            print(e)


        bmp = displayio.Bitmap(128, 32, colors)
        # make the color at 0 index transparent.
        palette.make_transparent(0)
        # Create the sprite TileGrid
        sprite1 = displayio.TileGrid(
            bmp,
            pixel_shader=palette,
            width=1,
            height=1,
            tile_width=128,
            tile_height=32,
            default_tile=0,
        )

        sprite_group = displayio.Group()
        self.display.show(sprite_group)
        sprite_group.append(sprite)

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        return

    def before_matrix_scan(self, sandbox):
        return

    def after_matrix_scan(self, sandbox):
        self.updateOLED()
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return

def releaseDisp():
        displayio.release_displays()