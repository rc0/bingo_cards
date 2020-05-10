
import generate
import cairo
import time

start_time = int(time.time())

W = (210 / 25.4) * 72
H = (297 / 25.4) * 72
surface = cairo.PDFSurface(f"output/cards_{start_time:d}.pdf", W, H)
cx = cairo.Context(surface)
pt_mm = 72 / 25.4
cx.scale(pt_mm, pt_mm)
cx.set_source_rgba(0.0, 0.0, 0.0, 1.0)
cx.set_line_width(0.3)
cx.set_line_cap(cairo.LINE_CAP_ROUND)
label_face = cairo.ToyFontFace("Fira Mono Medium", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
the_face = cairo.ToyFontFace("Fira Sans Book", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

top_margin = 25.0
left_margin = 16.0
col_shift = 9.0
row_shift = 10.0
card_shift = 45.0
bank_shift = 100.0

page_number_x = 98
page_number_y = 285

# ought to compute font metrics to do these properly!
deltax = -1.5
deltay = -7

label_sep = 1.0

for page in range(6):
    cx.set_font_face(the_face)
    cx.set_font_size(4)
    cx.move_to(page_number_x, page_number_y)
    cx.show_text(f"Page {page+1:d}")
    for bank in [0,1]:
        cx.set_font_face(the_face)
        cx.set_font_size(6)
        foo = (1000 + (page * 2) + bank)
        seed = [start_time, foo]
        cards = generate.generate_cards(seed)
        for card in range(6):
            for row in range(3):
                for col in range(9):
                    val = cards[card, row, col]
                    if val > 0:
                        x = left_margin + (bank * bank_shift) + (col * col_shift)
                        y = top_margin + (card * card_shift) + (row * row_shift)
                        cx.move_to(x, y)
                        cx.show_text(f"{val:2d}")
            for col in range(10):
                x = deltax + left_margin + (bank * bank_shift) + (col * col_shift)
                y0 = deltay + top_margin + (card * card_shift)
                y1 = y0 + (3 * row_shift)
                cx.move_to(x, y0)
                cx.line_to(x, y1)
            for row in range(4):
                x0 = deltax + left_margin + (bank * bank_shift)
                x1 = x0 + (9 * col_shift)
                y = deltay + top_margin + (card * card_shift) + (row * row_shift)
                cx.move_to(x0, y)
                cx.line_to(x1, y)
            cx.stroke()
        # labelling
        cx.set_font_face(label_face)
        cx.set_font_size(2.5)
        for card in range(6):
            label = f"{seed[0]:10d} {seed[1]:5d}  {(card+1):1d}"
            x = deltax + left_margin + (bank * bank_shift)
            y = deltay + top_margin + (card * card_shift) + (3 * row_shift)
            cx.save()
            cx.translate(x, y)
            cx.rotate(-3.1415926535/2.0)
            cx.move_to(0,-label_sep)
            cx.show_text(label)
            cx.restore()

    cx.show_page()

