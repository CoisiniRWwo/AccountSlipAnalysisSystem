from PIL import Image, ImageDraw, ImageFont
import random


def generate_captcha(length=4, size=(120, 40), font_size=25):
    # 生成随机字符
    chars = "0123456789abcdefghijklmnopqrstuvwxyz" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    captcha = ''.join(random.sample(chars, length))

    # 创建图片
    image = Image.new('RGB', size, (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 绘制字符
    font = ImageFont.truetype('arial.ttf', font_size)
    for i in range(length):
        draw.text((i * font_size + 10, 10), captcha[i], font=font, fill=get_random_color())

    # 绘制干扰点
    for i in range(200):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        draw.point((x, y), fill=get_random_color())

    return captcha, image


def get_random_color():
    return (random.randint(0, 220), random.randint(0, 220), random.randint(0, 220))


# 生成验证码
captcha, image = generate_captcha()

# 输出验证码字符
# print(captcha)

# 输出验证码图片
# image.show()
