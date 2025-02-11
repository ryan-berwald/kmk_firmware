import displayio
from adafruit_displayio_ssd1306 import SSD1306
from busio import I2C
from kmk.extensions import Extension
from kmk.kmktime import sleep_ms
import struct
from bitmaptools import readinto as _bitmap_readinto
from sys import maxsize

class bmpInfo:
    def __init__(self, _path = "images\\f.bmp"):
        self.path = _path
        with open(_path, "rb") as bmp:
            bmp.read(10)
            self.dataOffset = int.from_bytes(bmp.read(4), "little")
            self.DIBHeaderSize = int.from_bytes(bmp.read(4), "little")
            self.width = int.from_bytes(bmp.read(4), "little")
            self.height = int.from_bytes(bmp.read(4), "little")
            self.colorPlanes = int.from_bytes(bmp.read(2), "little")
            bmp.read(2)
            self.compressionMethod = int.from_bytes(bmp.read(4), "little")
            bmp.read(4)
            bmp.read(4)
            bmp.read(4)
            bmp.read(4)
            self.numColors = int.from_bytes(bmp.read(4), "little")
        self.palette = self.getColorPalette()
        self.bitmap = self.createBitmap()

    def display(self):
        print("Data offset: %s" % self.dataOffset)
        print("DIB Header: %s" % self.DIBHeaderSize)
        print("Width: %s" % self.width)
        print("Height: %s" % self.height)
        print("Color Planes: %s" % self.colorPlanes)
        print("Compression Method: %s" % self.compressionMethod)
        print("Number of Colors: %s" % self.numColors)
        print("Palette: %s" % self.palette[0])
        print("Bitmap: %s" % self.bitmap[0])

    def getColorPalette(self):
        palette = displayio.Palette(self.numColors)
        with open(self.path, "rb") as f:
            f.seek(self.dataOffset - (self.numColors * 4))
            for val in range(self.numColors):
                try:
                    c_bytes = f.read(4)
                    #print(b''.join([c_bytes[2:3], c_bytes[1:2], c_bytes[0:1], c_bytes[3:]]))
                    palette[val] = b''.join([c_bytes[2:3], c_bytes[1:2], c_bytes[0:1], c_bytes[3:]])
                except Exception as e:
                    print(e)
        return palette

    def createBitmap(self):
        minimum_color_depth = 1
        while self.numColors > 2 ** minimum_color_depth:
            minimum_color_depth *= 2

        file = open(self.path, mode="rb")
        bitmap = displayio.Bitmap(self.width, self.height, self.numColors)
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
                try:
                    _bitmap_readinto(bitmap, file, bits_per_pixel=self.colorPlanes, element_size=4, reverse_pixels_in_element=True, reverse_rows=True)
                except Exception as e:
                    print(repr(e))
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
    def __init__(self, SDA, SCL, toDisplay = "ACTIVE LAYER", oWidth=128, oHeight=32, tileWidth = 128, tileHeight = 32, gridWidth = 1, gridHeight = 1):
        releaseDisp()
        self._toDisplay = toDisplay
        self._display = SSD1306(displayio.I2CDisplay(I2C(SDA, SCL), device_address=0x3C), width=oWidth, height=oHeight)
        self._tileHeight = tileHeight
        self._tileWidth = tileWidth
        self._gridWidth = gridWidth
        self._gridHeight = gridHeight
        self._prevLayers = 0

    def updateOLED(self, sandbox):
        try:
            open(self._toDisplay, "rb")
            bmpinfo = bmpInfo(self._toDisplay)

            #bmpinfo.display()
            # make the color at 0 index transparent.
            bmpinfo.palette.make_transparent(0)
            # Create the sprite TileGrid
            sprite1 = displayio.TileGrid(
                bmpinfo.bitmap,
                pixel_shader=bmpinfo.palette,
                width=self._gridWidth,
                height=self._gridHeight,
                tile_width=self._tileWidth,
                tile_height=self._tileHeight,
                default_tile=0,
            )
            try:
                sprite_group = displayio.Group()
                self._display.show(sprite_group)
                sprite_group.append(sprite1)
            except Exception as e:
                print(e)
        except OSError as e:
            print("File does not exist, resorting to text!")
            import terminalio
            try:
                import label
            except Exception as e:
                print("You need to place the adafruit_displayio_text module in your lib folder")
            if self._toDisplay.upper() == "ACTIVE LAYER":
                print("Active Layer: %s" % sandbox.active_layers[0])
                text = "Active Layer: %s" % sandbox.active_layers[0]
            splash = displayio.Group()
            self._display.show(splash)
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=15)
            splash.append(text_area)

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        self.updateOLED(sandbox)
        return

    def before_matrix_scan(self, sandbox):
        if sandbox.active_layers[0] != self._prevLayers:
            print(sandbox.active_layers[0])
            self._prevLayers = sandbox.active_layers[0]
            self.updateOLED(sandbox)
        return

    def after_matrix_scan(self, sandbox):

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
