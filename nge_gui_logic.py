from tkinter import Text, Canvas, Toplevel, NW, RAISED, SUNKEN, CENTER, PhotoImage
from tkinter.ttk import Scrollbar, Treeview, Style, Label, Frame, Button

from math import floor
import nge_logic as prog

# Sets style
def set_style(root: Toplevel):
  #creating style and theme for this application
  style = Style(root)
  style.theme_create("NGE", "default")
  style.theme_use("NGE")

  #gathering required default layouts for modification
  default_btn_layout = style.layout("TButton")
  default_lbl_layout = style.layout("TLabel")
  default_tree_layout = style.layout("Treeview")
  #setting up layouts for custom themed widgets
  style.layout("hex_lbl", default_lbl_layout)
  style.layout("tool_btn", default_btn_layout)
  style.layout("sel_tool_btn", default_btn_layout)
  style.layout("sel_color_btn", default_btn_layout)
  style.layout("color_btn", default_btn_layout)
  style.layout("sel_hex_lbl", default_lbl_layout)
  style.layout("fileview", default_tree_layout)

  # Configuring styles
  style.configure("hex_lbl", padding=0, font='TkFixedFont', 
                  background="#ffffff", foreground="#000000")
  style.configure("sel_hex_lbl", background="#0000ff", foreground="#ffffff")
  style.configure("tool_btn", relief="raised", padding=2)
  style.configure("sel_tool_btn", relief="sunken", padding=2)
  style.configure("color_btn", relief="raised", padding=2)
  style.configure("sel_color_btn", relief="sunken", padding=2)
  style.configure("fileview", background='#ffffff', rowheight = 24)
  #setting up default button click animation
  style.map("TButton", relief=[("pressed", SUNKEN), ("!pressed", RAISED)])
  style.map("fileview", background=[("selected", "#cccccc")])

def gui_update(widgets: dict):
  update_sheet_sel(widgets["sheet_canvas"])
  update_txt_sel(widgets["hex_txt"])
  update_draw_canvas(widgets["draw_canvas"])
  update_tree_sel(widgets["file_tree_view"])

# Sets up grid of rectangles for draw canvas.
# Each rectangle is tagged with "rect" followed by a number
def draw_grid_setup(draw_canvas: Canvas):
  bg_img = draw_canvas.nametowidget('.nge').images["draw_bg"]
  draw_canvas.create_image((1, 1), image=bg_img, anchor=NW)
  grid_tag = 0
  for y in range(8):
    y_coord = y * 49
    y_start = 0
    y_end = 386
    for x in range(8):
      x_coord = x * 49
      x_start = 0
      x_end = 386
      rect_name = 'rect' + str(x+y*8)
      draw_canvas.create_rectangle(x_coord+2, y_coord+2, x_coord+49, y_coord+49, tag=rect_name, outline="#ffffff", fill="#ffffff")
      draw_canvas.create_text((x_coord+2 + x_coord+49) / 2, (y_coord+2 + y_coord+49) / 2, text=str(x+y*8))

# Sets up grid of rectangles for sheet canvas.
# Sets up images based on current file, then draws the rectangles over them.
# Each image is tagged "img" followed by a number.
# Each rectangle is tagged with 'rect' followed by a number.
def sheet_grid_setup(sheet_canvas):
  bg_img = sheet_canvas.nametowidget('.nge').images["sheet_bg"]
  imgs = sheet_canvas.nametowidget('.nge').images
  img_keys = imgs.keys()
  for y in range(8):
    for x in range(16):
      img_name = "img"+str(y*16+x)
      if img_name in img_keys:
        img = imgs["img" + str(y*16+x)]
        sheet_canvas.create_image(x*49+2, y*49+2, image=img, tag=img_name, anchor=NW)
    sheet_canvas.create_image((1, 1), image=bg_img, tag="sheet_bg", anchor=NW)
  sheet_canvas.create_rectangle(1, 1, 50, 50, outline='#ff0000', tag='select_rect', width=3)

def col_palette_setup(canvas: Canvas):
  canvas.create_rectangle(2, 2, 34, 34, outline="#000000", fill="#ffffff")
  canvas.create_rectangle(2, 33, 34, 65, outline="#000000", fill="#aaaaaa")
  canvas.create_rectangle(2, 64, 34, 96, outline="#000000", fill="#555555")
  canvas.create_rectangle(2, 96, 34, 128, outline="#000000", fill="#000000")

def hex_txt_setup(txt: Text):
  char_data_list = txt.nametowidget('.nge').char_data_list
  for char_num, char_data in enumerate(char_data_list):
    lbl_index = str(char_num+1) + '.0'
    txt_index = str(char_num+1) + '.4'
    hdr = '0x' + str(format(char_num, '02x')).upper()+'|'
    dat = char_to_hex(char_data) + '\n'
    char_label = Label(txt, text=hdr, style="nge.hex_lbl", name = "lbl"+str(char_num+1))
    txt.window_create(lbl_index, window=char_label, align=CENTER)
    if char_num < 127:
     txt.insert(txt_index, dat)
    else:
      txt.insert(txt_index, dat.strip())

# Setting up treeview to quickly select sheets and chars.
def treeview_setup(treeview: Treeview, scrollbar: Scrollbar):
  window_frame = treeview.nametowidget('.nge')
  imgs = window_frame.images
  book = window_frame.active_book
  treeview.configure({"yscrollcommand" : scrollbar.set})
  bk_id = "bk"
  treeview.insert(parent="", iid=bk_id, index="end", open=True, image=imgs["book"], text=book.name)
  for sheet in book.sheets:
    sh_id = bk_id + ".sh" + str(sheet.id)
    treeview.insert(parent=bk_id, iid=sh_id, index="end", image=imgs["sheet"], text=sheet.name)
    char_list = sheet.char_list
    for char in char_list:
      ch_id = sh_id + ".ch" + str(char.id)
      treeview.insert(parent=sh_id, iid = ch_id, index="end", image=imgs["character"], text=char.name)

def info_frame_setup(infoframe: Frame):
  book_lbl_frame = infoframe.nametowidget('.info_frame.book_label_frame')
  sheet_lbl_frame = infoframe.nametowidget('.info_frame.sheet_label_frame')
  char_lbl_frame = infoframe.nametowidget('.info_frame.char_label_frame')
# Changes cursor over draw canvas when a tool is selected
# Cursor replacement must follow this format:
# cursor=("@./filename.xbm", "filenamemask.xbm", "#000000", "#FFFFFF"))
def chg_cursor(canvas: Canvas, tool: str):
  src_img = "@./" + tool + "_cur.xbm"
  mask_img = tool + "_cur-mask.xbm"
  canvas.configure(cursor=(src_img, mask_img, '#44ccaa', '#44ccaa'))
  
# When the draw_canvas is clicked with a drawing tool,
# Figures out which one it is and acts accordingly.
def draw_canvas_tool_click(event):
  draw_canvas = event.widget
  window = draw_canvas.nametowidget('.nge')
  tool = window.active_tool
  color = None
  if event.num == 1:
    color = window.getvar('fg_color')
  elif event.num == 3:
    color = window.getvar('bg_color')
  
  if tool == 'pencil':
    pencil_click(event, color)
  if tool == 'eraser':
    eraser_click()
  if tool == 'line':
    line_click()
  if tool == 'bucket':
    bucket_click(event, color)


# Called when the pencil tool is active and the draw canvas is clicked
def pencil_click(event, color: str):
  grid_num = coords_to_index(event.x, event.y, 8)
  rect = event.widget.find_withtag('rect' + str(grid_num))
  event.widget.itemconfigure(rect, fill=color, outline=color)
  event.widget.setvar('char_edited', True)
# As above, for eraser

def eraser_click():#canvas: Canvas, x: int, y: int):
  # rect_id = str(x // 40) + '.' + str(y // 40)
  # canvas.itemconfig(rect_id, {"fill" : "#ffffff"})
  pass

# As above, for line tool
def line_click():#canvas: Canvas, color: str, x: int, y: int):
  # rect_id = str(x // 40) + '.' + str(y // 40)
  # canvas.itemconfig(rect_id, {"fill" : color})
  pass

# As above, for bucket tool
def bucket_click(event, color: str):
  draw_canv = event.widget
  grid_ids = []
  
  start_grid = 'rect' + str(coords_to_index(event.x, event.y, 8))
  grid_ids.append(start_grid)
  target_col = draw_canv.itemcget(draw_canv.find_withtag(grid_ids[0]), 'fill')
  id_index = 0
  while True:
    new_neighbors = []
    for grid in grid_ids[id_index:]:
      grid_num = int(grid[4:])
      if (grid_num - 8) >= 0 and grid_num // 8 > 0:
        new_neighbors.append('rect'+str(grid_num-8))
      if (grid_num + 1) <= 63 and grid_num % 8 != 7:
        new_neighbors.append('rect'+str(grid_num+1))
      if (grid_num + 8) <= 63 and grid_num % 8 < 7:
        new_neighbors.append('rect'+str(grid_num+8))
      if (grid_num - 1) >= 0 and grid_num% 8 != 0:
        new_neighbors.append('rect'+str(grid_num-1))
      id_index += 1

    while len(new_neighbors) > 0:
      candidate = new_neighbors.pop(0)
      neighbor_fill = draw_canv.itemcget(candidate, 'fill')
      if neighbor_fill == target_col and candidate not in grid_ids:
        grid_ids.append(candidate)

    if id_index >= len(grid_ids):
      print('lmao')
      break
  
  for id in grid_ids:
    draw_canv.itemconfig(id, fill = color, outline = color)
    draw_canv.setvar('char_edited', True)
    

def update_hex_txt(hex_txt: Text, char_num: int, data: list):
  char_hex = char_to_hex(data)
  index_line = str(char_num+1)
  hex_txt.delete(index_line + '.1', index_line+'.54')
  hex_txt.insert(index_line +'.1', char_hex, ("char" + str(char_num)))

def update_draw_canvas(draw_canvas: Canvas):
  window = draw_canvas.nametowidget('.nge')
  char_data = window.char_data_list[window.active_char]
  for index, pixel in enumerate(char_data):
    rect_tag = "rect" + str(index)
    color_str = prog.dat_to_col_dict[pixel]
    draw_canvas.itemconfig(rect_tag, fill=color_str, outline=color_str)

def char_to_hex(char_data):
  char_hex = ""
  for x in range(8):
    upperbyte = ""
    lowerbyte = ""
    row = char_data[x*8: x*8 +8]
    for pixel in row:
      upperbyte += str(pixel % 2)
      lowerbyte += str(pixel // 2)
    upperbyte = int(upperbyte, base=2)
    lowerbyte = int(lowerbyte, base=2)
    char_hex += "{0:02x} {1:02x} ".format(upperbyte, lowerbyte).upper()
  return char_hex.strip()

def hex_txt_scroll(cls, event):
  hex_scroll = cls.root.nametowidget('.hex_frame.hex_scrollbar')
  hex_dat_txt = cls.root.nametowidget('.hex_frame.hex_dat_txt')
  hex_hdr_txt = cls.root.nametowidget('.hex_frame.hex_hdr_txt')
  hex_dat_txt.state("active")
  hex_hdr_txt.state("active")

### Finds and corrects
def set_parent(root: Frame, config: dict):
  parent_name = config["master"]
  parent = root.nametowidget(parent_name)
  config["master"] = root.nametowidget(parent_name)

def coords_to_index(x: int, y: int, num_col):
  x_grid = floor(x / 49.25)
  y_grid = floor(y / 49.25)
  index = (x_grid + y_grid * num_col)
  return index

def update_sheet_sel(sheet_canvas):
  root = sheet_canvas.nametowidget('.nge')
  active_char = sheet_canvas.nametowidget('.nge').active_char
  old_coords = sheet_canvas.coords("select_rect")
  new_coords = sheet_canvas.coords("img" + str(active_char))  
  delta_pos = ((new_coords[0] - old_coords[0])-1, (new_coords[1] - old_coords[1])-1)
  sheet_canvas.move("select_rect", delta_pos[0], delta_pos[1])
  
def update_txt_sel(hex_txt):
  prev_char = hex_txt.nametowidget('.nge').prev_char
  active_char = hex_txt.nametowidget('.nge').active_char
  curr_sel = hex_txt.tag_ranges('active_char')
  if len(curr_sel) != 0:
    hex_txt.tag_remove('active_char', curr_sel[0], curr_sel[1])
    lbl_path = '.nge.hex_frame.hex_txt.lbl' + str(prev_char+1)
    hex_txt.nametowidget(lbl_path).config(background='#ffffff')
  
  start = str(active_char + 1) + '.0'
  end = str(active_char + 1) + '.53'
  
  hex_txt.tag_add('active_char', start, end)
  hex_txt.tag_config('active_char', background="#cccccc")
  
  lbl_path = '.nge.hex_frame.hex_txt.lbl' + str(active_char+1)
  hex_txt.nametowidget(lbl_path).config(background = '#cccccc')
  
  hex_txt.see(start)

def update_tree_sel(treeview):
  window = treeview.nametowidget('.nge')
  if window.prev_char != None:
    prev_id = 'bk.sh' + str(window.active_sheet) + '.ch'+str(window.prev_char)
    treeview.selection_remove(prev_id)
  act_id = 'bk.sh' + str(window.active_sheet) + '.ch' + str(window.active_char)
  treeview.selection_add(act_id)
  treeview.see(act_id)

