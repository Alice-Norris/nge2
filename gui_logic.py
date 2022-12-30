from tkinter import Text, Canvas, PhotoImage, BitmapImage, Toplevel, NW, RAISED, SUNKEN, Tk
from tkinter.ttk import Scrollbar, Treeview, Style
from nge_classes import Sheet

# Sets style
def set_style(root: Toplevel):
  style = Style(root)
  style.theme_create("NGE", "default")
  style.theme_use("NGE")
  default_btn_layout = style.layout("TButton")
  # Creating button layouts so we can modify theme
  # Setting padding and relief to both styles
  style.layout("tool_btn", default_btn_layout)
  style.configure("tool_btn", relief="raised", padding=3)
  style.layout("sel_tool_btn", default_btn_layout)
  style.configure("sel_tool_btn", relief="sunken", padding=3)
  style.map("TButton", relief=[("pressed", SUNKEN), ("!pressed", RAISED)])
  style.configure("TButton", relief=RAISED)
  style.configure("Treeview", width=240)
# Sets up grid of rectangles for sheet and draw canvases.
# Tag is the x- and y-coordinates, separated by '.', for
# When we know which part of the grid we want

def grid_setup(canvas, cols, rows, select_rect: bool):
  grid_tag = 0
  for y in range(rows):
    for x in range(cols):
      x_start = x*41
      y_start = y*41
      grid_tag_str = "rect" + str(grid_tag)
      canvas.create_rectangle(x_start+1, y_start+1, x_start+42, y_start+42, fill=None, tag=grid_tag_str)
      grid_tag += 1
  if select_rect:
    canvas.create_rectangle(1, 1, 42, 42, tag="select_rect", width=3, outline="#00ff00")
# Setting up hex_header display. Each row represents a character address.
def hex_row_setup(text: Text):
  x = 0
  while x < 128:
    header = '0x' + str(format(x, '02x')).upper()
    index = str(x+1) + '.0'
    text.insert(index, header)
    x += 1

# Setting up hex data display, representing character data in every row.
def hex_text_setup(text: Text):
  x = 0
  while x < 128:
    index = str(x+1) + '.0'
    if x < 127:
      text.insert(index, ('00 ' * 8) + '\n')
    elif x == 127:
      text.insert(index, ('00 ' * 8))
    x += 1

# Setting up treeview to quickly select sheets and chars.
def treeview_setup(treeview: Treeview, scrollbar: Scrollbar, index: dict, imgs: dict):
  treeview.configure({"yscrollcommand" : scrollbar.set})
  for bk_num, book in enumerate(index.items()):
    book_name = book[0]
    sheet_dict = book[1]
    bk_id = "bk"
    treeview.insert(parent="", iid=bk_id, index="end", open=True, image=imgs["book"], text=book_name)
    for sh_num, sheet in enumerate(sheet_dict.items()):
      sh_name = sheet[0]
      sh_id = bk_id + ".sh" + str(sh_num)
      treeview.insert(parent=bk_id, iid=sh_id, index="end", image=imgs["sheet"], text=sh_name)
      char_list = sheet[1]
      for ch_num, ch_name in enumerate(char_list):
        ch_id = sh_id + ".ch" + str(ch_num)
        treeview.insert(parent=sh_id, iid = ch_id, index="end", image=imgs["character"], text=ch_name)

# Keep texts from scrolling independently of each other
def txt_binds(txt1: Text, txt2: Text):
  scroll_up_cmd = {"sequence" : "<Button-4>", "func" : "break"}
  scroll_down_cmd = {"sequence" : "<Button-5>", "func" : "break"}
  txt1.bind(**scroll_up_cmd)
  txt2.bind(**scroll_up_cmd)
  txt1.bind(**scroll_down_cmd)
  txt2.bind(**scroll_down_cmd)

# Changes cursor over draw canvas when a tool is selected
def chg_cursor(tool: str, canvas: Canvas):
  src_img = "@./" + tool + "_cur.xbm"
  mask_img = tool + "_cur-mask.xbm"
  canvas.configure(cursor=(src_img, mask_img, "#000000", "#FFFFFF"))
  #canvas.configure(cursor=("@./erasercur2.xbm", "erasercur2mask.xbm", "#000000", "#FFFFFF"))

# Returns color equivalent when a color button is selected
def chg_color(color: str):
  col_dict = {
    "blk" : "#000000",
    "dkg" : "#555555",
    "ltg" : "#AAAAAA",
    "wht" : "#FFFFFF"
  }
  return col_dict[color]

# Scroll command for text scrollbar. Scrolls both txt values.
def dbl_scroll(txt1: Text, txt2: Text, *args):
  txt1.yview(*args)
  txt2.yview(*args)

# When the draw_canvas is clicked with a drawing tool,
# Figures out which one it is and acts accordingly.
def draw_canvas_tool_click(event, tool, color):
  canvas = event.widget
  if tool == 'pencil':
    return pencil_click(canvas, color, event.x, event.y)
  if tool == 'eraser':
    eraser_click(canvas, event.x, event.y)
  if tool == 'line':
    line_click(canvas, color, event.x, event.y)
  if tool == 'bucket':
    bucket_click(canvas, color, event.x, event.y)

# Called when the pencil tool is active and the draw canvas is clicked
def pencil_click(canvas: Canvas, color: str, x: int, y: int):
  pixel = x // 40 + (y // 40) * 8
  rect_tag = "rect" + str(pixel)
  canvas.itemconfig(rect_tag, {"fill" : color})
  return [pixel]

# As above, for eraser
def eraser_click(canvas: Canvas, x: int, y: int):
  rect_id = str(x // 40) + '.' + str(y // 40)
  canvas.itemconfig(rect_id, {"fill" : "#FFFFFF"})

# As above, for line tool
def line_click(canvas: Canvas, color: str, x: int, y: int):
  rect_id = str(x // 40) + '.' + str(y // 40)
  canvas.itemconfig(rect_id, {"fill" : color})

# As above, for bucket tool
def bucket_click(canvas: Canvas, color: str, x: int, y: int):
  rect_id = str(x // 40) + '.' + str(y // 40)
  canvas.itemconfig(rect_id, {"fill" : color})

# Changes active character when the sheet canvas is clicked.
def select_char(canvas, old_active_char, new_active_char):
  old_coords = canvas.coords("select_rect")
  new_coords = canvas.coords("rect" + str(new_active_char))
  delta_pos = ((new_coords[0] - old_coords[0]), (new_coords[1] - old_coords[1]))
  canvas.move("select_rect", delta_pos[0], delta_pos[1])

# Creates images for each character to be drawn on the sheet canvas.
def draw_sheet_canv(imgs: dict, canvas: Canvas, char_list: list):
  img_hdr = bytes("P6\n40 40\n3\n", encoding='utf-8')
  for img_num in range(128):
    x_grid = img_num % 16
    y_grid = img_num // 16
    img = imgs["img" + str(img_num)]
    img_tag = "img" + str(img_num)
    canvas.create_image(x_grid*41+2, y_grid*41+2, image=img, tag=img_tag, anchor=NW)

def update_draw_canvas(canvas: Canvas, char_data: list):
  ui_col_dict = {
    0 : "#ffffff",
    1 : "#AAAAAA",
    2 : "#555555",
    3 : "#000000",
  }
  for index, pixel in enumerate(char_data):
    color_str = ui_col_dict[pixel]
    canvas.itemconfig("rect" + str(index), fill=color_str)