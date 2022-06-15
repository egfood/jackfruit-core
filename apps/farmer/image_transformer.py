from collections import namedtuple

from PIL import Image

Point = namedtuple('Point', ('x', 'y'))
RectangleSize = namedtuple('RectangleSize', ('height', 'width'))


class ImageTransformer:
    def __init__(self, path_to_img: str, new_width: int, new_height: int):
        self.path = path_to_img
        self.img = Image.open(self.path)
        self.new_width = new_width
        self.new_height = new_height

    def transform(self) -> None:
        if self.img.width != self.new_width and self.img.height != self.new_height:
            self._resize()
            # Needs to execute the _draw_to_rectangle() method after the _resize() method
            self._draw_to_rectangle()
            self._save()

    def _resize(self) -> None:
        proportional_size = self._get_proportional_size()
        self.img = self.img.resize((proportional_size.width, proportional_size.height))

    def _get_proportional_size(self) -> RectangleSize:
        proportional_height = self.new_height
        proportional_width = self.new_width
        if self.img.width > self.img.height:
            proportional_height = int(self.img.height * self.new_width / self.img.width)
        elif self.img.height > self.img.width:
            proportional_width = int(self.img.width * self.new_height / self.img.height)
        return RectangleSize(height=proportional_height, width=proportional_width)

    def _draw_to_rectangle(self) -> None:
        background = Image.new(self.img.mode, (self.new_width, self.new_height,), 'white')
        background.paste(self.img, self._get_img_start_position())
        self.img = background

    def _get_img_start_position(self) -> Point:
        return Point(
            x=self._get_coordinate(self.img.width, self.new_width),
            y=self._get_coordinate(self.img.height, self.new_height)
        )

    @staticmethod
    def _get_coordinate(old: int, new: int) -> int:
        resulting_coordinate = 0
        if new > old:
            resulting_coordinate = int((new - old) / 2)
        return resulting_coordinate

    def _save(self) -> None:
        self.img.save(self.path)
