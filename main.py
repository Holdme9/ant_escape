#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image


class Pixel:
    """Класс, представляющий пиксель с глубиной цвета 1 бит."""
    def __init__(self):
        """Инициализирует объекты класса Pixel. По умолчанию,
        создаваемые пиксели имеют белый цвет."""
        self.is_white = True

    def change_color(self) -> None:
        """Меняет цвет пикселя на противоположный."""
        self.is_white = False if self.is_white else True


class Picture:
    """Класс, представляющий изображение."""
    def __init__(self, size):
        self.pixels = [[Pixel() for _ in range(size)] for __ in range(size)]

    def get_size(self) -> int:
        """Возвращает размер изображения в пикселях."""
        return len(self.pixels)

    def get_pixel(self, position: list[int, int]) -> Pixel:
        """Возвращает пиксель, находящийся в указанной позиции."""
        i, j = position
        return self.pixels[i][j]

    def create_img_and_count_black_pixels(self) -> int:
        """Создает изображение со следами муравья в формате .png
        и возвращает количество черных пикселей."""
        size = self.get_size()
        name = f'ant_{size}.png'
        image = Image.new('1', (size, size))
        counter = 0

        for i in range(size):
            for j in range(size):
                px = self.get_pixel([i, j])
                image.putpixel((j, i), px.is_white)
                if not px.is_white:
                    counter += 1

        image.save(name)
        return counter


class Ant:
    """Класс, представляющий муравья."""
    def __init__(self, pic: Picture):
        self.position = self.set_initial_position(img.get_size())
        self.direction = [-1, 0]
        self.img = img

    @staticmethod
    def set_initial_position(size) -> list[int, int]:
        """Устанавливает муравья в исходную позицию."""
        point = size // 2
        return [point, point]

    def change_position(self) -> None:
        """Меняет текущую позицию муравья."""
        pos = self.position
        pos[0] += self.direction[0]
        pos[1] += self.direction[1]

    def change_direction(self, px: Pixel) -> None:
        """Меняет направление движения муравья."""
        i, j = self.direction

        if (i == -1 and px.is_white) or (i == 1 and not px.is_white):
            self.direction = [0, 1]
        elif (i == -1 and not px.is_white) or (i == 1 and px.is_white):
            self.direction = [0, -1]
        elif (j == 1 and px.is_white) or (j == -1 and not px.is_white):
            self.direction = [1, 0]
        else:
            self.direction = [-1, 0]

    def move(self) -> None:
        """Определяет процесс перемещения муравья."""
        self.change_position()
        px = self.img.get_pixel(self.position)
        self.change_direction(px)
        px.change_color()

    def is_finished(self):
        """Возвращает True, если муравей добрался до края изображения
        и False в противном случае."""
        size = self.img.get_size()
        pos = self.position
        return 0 in pos or size-1 in pos

    def escape(self):
        """Запускает процесс перемещения муравья, пока он не дойдет до края изображения."""
        while not self.is_finished():
            self.move()


img = Picture(1024)
ant = Ant(img)
ant.escape()
black_pixels_num = img.create_img_and_count_black_pixels()
print(black_pixels_num)
