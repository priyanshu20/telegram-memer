from PIL import Image, ImageDraw, ImageFont
import textwrap


def memeMaker(template, top_lines, bottom_lines, cid):
    template = template
    top_lines = top_lines
    bottom_lines = bottom_lines
    image = Image.open(f"./templates/{template}")
    drawer = ImageDraw.Draw(image)
    iwidth, iheight = image.size
    max_font_factor = 10
    k = 10
    # CALCULATING FONT
    for line in top_lines:
        while True:
            font = ImageFont.truetype(font="./impact.ttf", size=iheight//k)
            char_width, char_height = font.getsize('P')
            chars_per_line = iwidth//char_width
            _top_lines = textwrap.wrap(line, width=chars_per_line)
            if(len(_top_lines) == 1):
                break
            else:
                k += 1
        max_font_factor = max(max_font_factor, k)

    # TOP_LINES
    y = 30
    font = ImageFont.truetype(
        font="./impact.ttf", size=iheight//max_font_factor)
    for line in top_lines:
        line = line.upper()
        line_width, line_height = font.getsize(line)
        x = (iwidth-line_width)/2
        print(x)
        drawer.text((x, y), line, fill='yellow', font=font)
        y += line_height

    # BOTTOM_LINES
    y = iheight - char_height * len(bottom_lines) - 15
    for line in bottom_lines:
        line = line.upper()
        line_width, line_height = font.getsize(line)
        x = (iwidth - line_width)/2
        drawer.text((x, y), line, fill='yellow', font=font)
        y += line_height

    image.save(f'{cid}.png')


if __name__ == "__main__":
    memeMaker("fulao.jpg", ["pehli line", "Dusri lines ka text yeh raha ",
                            "teesri mei toh atank hi chaa gya matlab itna sara text"], ["Jyada gaand na fulao", "tumhari ma chod denge"], "420")
