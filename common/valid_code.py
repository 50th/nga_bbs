from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random


class ValidCodeHandler(object):
    """生成验证码"""
    def __init__(self, width=90, height=40):
        self.width = width
        self.height = height

    def get_valid_code(self):
        """生成验证码"""
        valid_code = ""
        for i in range(0, 4):
            k = random.randrange(0, 4)
            if k == 2:
                t = random.randrange(65, 91)
                t = chr(t)
            elif k == 3:
                t = random.randrange(97, 123)
                t = chr(t)
            else:
                t = str(random.randrange(0, 9))
            valid_code += t
        return valid_code

    def get_color(self):
        c1 = random.randint(0, 255)
        c2 = random.randint(0, 255)
        c3 = random.randint(0, 255)
        return (c1, c2, c3)

    def get_valid_img(self):
        """生成验证码图片"""
        img = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        font = ImageFont.truetype("/common/font/SIMLI.TTF", 25)
        draw = ImageDraw.Draw(img)
        valid_code = self.get_valid_code()
        draw.text((27, 2), valid_code, (123, 34, 21), font=font)

        for i in range(5):
            x1 = random.randint(0, 100)
            x2 = random.randint(0, 100)
            y1 = random.randint(0, 50)
            y2 = random.randint(0, 50)
            draw.line((x1, y1, x2, y2), )

        # 画点
        for i in range(30):
            draw.point([random.randint(0, 100), random.randint(0, 50)], fill=self.get_color())
            x = random.randint(0, 100)
            y = random.randint(0, 50)
            draw.arc((x, y, x + 4, y + 4), 0, 90, fill=self.get_color())

        f = BytesIO()
        img.save(f, "png")
        img_data = f.getvalue()
        f.close()
        return valid_code, img_data


if __name__ == '__main__':
    v = ValidCodeHandler(50,20)
    print(v.get_valid_img())
