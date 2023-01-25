from openpyxl import load_workbook
from PIL import Image, ImageDraw, ImageFont

def excel_to_art(excel_file, img_file, start_cell='A1', end_cell='Z100', img_size=(800, 600), font_size = 8, include_borders = False):
    wb = load_workbook(excel_file)
    sheet = wb.active
    rows = sheet[start_cell:end_cell]
    img = Image.new('RGB', img_size, color = 'white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", font_size)
    x_offset = 5
    y_offset = 5
    max_width = 0
    max_height = 0
    padding = 2
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            text_width, text_height = draw.textsize(str(cell.value), font)
            max_width = max(max_width, text_width)
            max_height = max(max_height, text_height)
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            if include_borders:
                x = x_offset + j * (max_width + 10)
                y = y_offset + i * (max_height + 5)
                left = x - padding
                top = y - padding
                right = x + max_width + padding
                bottom = y + max_height + padding
                draw.rectangle([left, top, right, bottom], fill='white', outline ='black')
                draw.text((x, y), str(cell.value), font=font, fill='black')
            else:
                x = x_offset + j * (max_width + 20)
                y = y_offset + i * (max_height + 5)
                draw.text((x, y), str(cell.value), font=font, fill='black')
    img.save(img_file)


