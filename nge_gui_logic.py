from tkinter import Text, Canvas, Toplevel, NW, RAISED, SUNKEN, CENTER, PhotoImage
from tkinter.ttk import Scrollbar, Treeview, Style, Label, Frame
from math import floor
import nge_logic as prog
from nge_classes import Book, AddCharDialog

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

# Sets up grid of rectangles for draw canvas.
# Each rectangle is tagged with "rect" followed by a number
def draw_grid_setup(draw_canvas: Canvas):
  grid_tag = 0
  for y in range(8):
    for x in range(8):
      x_coord = x * 49 + 3
      y_coord = y * 49 + 3
      rect_name = 'rect' + str(x+y*8)
      draw_canvas.create_rectangle(x_coord, y_coord, x_coord+47, y_coord+47, tag=rect_name, outline="#ffffff", fill="#ffffff")

# Sets up grid of rectangles for sheet canvas.
# Sets up images based on current file, then draws the rectangles over them.
# Each image is tagged "img" followed by a number.
# Each rectangle is tagged with 'rect' followed by a number.
def sheet_grid_setup(sheet_canvas):
  window = sheet_canvas.nametowidget('.nge')
  sheet_num = window.getvar('active_sheet')
  imgs = window.images
  char_list = window.active_book.sheets[sheet_num].char_list
  for y in range(8):
    for x in range(16):
      start_x = x * 49+2
      start_y = y * 49+2
      if len(char_list) > y*16+x:
        img_name = "img"+str(y*16+x)
        if img_name in imgs.keys():
          img = imgs["img" + str(y*16+x)]
          sheet_canvas.create_image(start_x, start_y, image=img, tag=img_name, anchor=NW)
          sheet_canvas.tag_bind(img_name, '<ButtonRelease-1>', sheet_img_click)
      else:
        rect_tag = 'rect'+str(y*16+x)
        sheet_canvas.create_rectangle(start_x, start_y, start_x+49, start_y+49, fill='#ffffff', tag=rect_tag, stipple='gray50')
        sheet_canvas.tag_bind(rect_tag, '<Double-ButtonRelease-1>', sheet_img_dbl_click)
  sheet_canvas.create_rectangle(2, 2, 51, 51, outline='#ff0000', tag='select_rect', width=2)

def col_palette_setup(canvas: Canvas):
  canvas.create_rectangle(2, 2, 34, 34, outline="#000000", fill="#ffffff")
  canvas.create_rectangle(2, 33, 34, 65, outline="#000000", fill="#aaaaaa")
  canvas.create_rectangle(2, 64, 34, 96, outline="#000000", fill="#555555")
  canvas.create_rectangle(2, 96, 34, 128, outline="#000000", fill="#000000")

def hex_txt_setup(txt: Text):
  book = txt.nametowidget('.nge').active_book
  sheet_num = txt.getvar('active_sheet')
  for x in range(128):
    lbl_index = str(x+1) + '.0'
    hdr = '0x' + str(format(x, '02x')).upper()+'|'
    hdr_name = "lbl" + str(x)
    char_label = Label(txt, text=hdr, style="nge.hex_lbl", name=hdr_name)
    txt.window_create(lbl_index, window=char_label, align=CENTER)
    if x < 127:
      txt.insert("end", '\n')
  for char_num, char in enumerate(book.sheets[sheet_num].char_list):
    txt_index = str(char_num+1) + '.4'
    char_data = char.data
    txt_tag = 'char' + str(char_num)
    dat = char_to_hex(char_data)
    txt.insert(txt_index, dat, txt_tag)

# Setting up treeview to quickly select sheets and chars.
def treeview_setup(treeview: Treeview, scrollbar: Scrollbar):
  window_frame = treeview.nametowidget('.nge')
  imgs = window_frame.images
  book = window_frame.active_book
  treeview.configure({"yscrollcommand" : scrollbar.set})
  treeview.insert(parent="", iid='book', index="end", open=True, image=imgs["book"], text=book.name)
  for sheet in book.sheets:
    sheet_tag = 'sh' + str(sheet.id)
    treeview.insert(parent='book', iid=sheet_tag, index="end", image=imgs["sheet"], tag=sheet_tag, text=sheet.name)
    treeview.tag_bind(sheet_tag, '<ButtonRelease-1>', tree_sheet_click)
    char_list = sheet.char_list
    for char in char_list:
      char_tag = sheet_tag + ".ch" + str(char.id)
      treeview.insert(parent=sheet_tag, iid=char_tag, index="end", image=imgs["character"], tag=char_tag, text=char.name)
      treeview.tag_bind(char_tag, '<ButtonRelease-1>', tree_char_click)

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
  draw_canvas.find_withtag('current')
  if draw_canvas.getvar('char_exists'):
    tool = draw_canvas.getvar('active_tool')
    color = None
    if event.num == 1:
      color = draw_canvas.getvar('fg_color')
    elif event.num == 3:
      color = draw_canvas.getvar('bg_color')

    if tool == 'pencil':
      pencil_click(event, color)
    elif tool == 'eraser':
      eraser_click()
    elif tool == 'line':
      line_click()
    elif tool == 'bucket':
      bucket_click(event, color)
    else:
      return
    event.widget.event_generate('<<Char-Data-Chg>>')

# Called when the pencil tool is active and the draw canvas is clicked
def pencil_click(event, color: str):
  obj = event.widget.find_withtag('current')
  event.widget.itemconfigure(obj, fill=color, outline=color)

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
  known_bad = []
  start_grid = draw_canv.find_withtag('current')[0]
  grid_ids.append(start_grid)
  target_col = draw_canv.itemcget(draw_canv.find_withtag(grid_ids[0]), 'fill')
  id_index = 0
  while True:
    new_neighbors = []
    for grid in grid_ids[id_index:]:
      if grid >= 9 and grid-8 not in known_bad:
        new_neighbors.append(grid-8)
      if grid % 8 != 0 and grid+1 not in known_bad:
        new_neighbors.append(grid+1)
      if grid <= 57 and grid+8 not in known_bad:
        new_neighbors.append(grid+8)
      if grid %8 != 1 and grid-1 not in known_bad:
        new_neighbors.append(grid-1)
      id_index += 1

    while len(new_neighbors) > 0:
      candidate = new_neighbors.pop(0)
      neighbor_fill = draw_canv.itemcget(candidate, 'fill')
      if neighbor_fill == target_col and candidate not in grid_ids:
        grid_ids.append(candidate)
      else:
        known_bad.append(candidate)

    if id_index >= len(grid_ids):
      break
  
  for id in grid_ids:
    draw_canv.itemconfig(id, fill = color, outline = color)
    draw_canv.setvar('char_edited', True)
    
def update_after_draw(draw_canvas: Canvas, book: Book, img: PhotoImage):
  act_sheet = draw_canvas.getvar('active_sheet')
  act_char = draw_canvas.getvar('active_char')
  char_data = book.sheets[act_sheet].char_list[act_char].data
  draw_rects = draw_canvas.find_all()
  for index, rect in enumerate(draw_rects):
    rect_col = draw_canvas.itemcget(rect, 'fill')
    pixel_col = prog.col_to_dat_dict[rect_col]
    char_data[index] = pixel_col
  update_char_img(char_data, img)
  hex_txt = draw_canvas.nametowidget('.nge.hex_frame.hex_txt')
  update_hex_txt(hex_txt, char_data)

def update_draw_canvas(draw_canvas: Canvas, char_data):
  window = draw_canvas.nametowidget('.nge')
  if not window.char_exists:
    draw_canvas.create_rectangle(1, 1, 393, 393, fill='#ffffff', tag='disable_fill')
    draw_canvas.create_rectangle(1, 1, 393, 393, fill='gray25', stipple='gray25', tag='disable_fill')
  else:
    if draw_canvas.find_withtag('disable_fill'):
      draw_canvas.delete('disable_fill')
    draw_canvas.configure(state='normal')
    for index, pixel in enumerate(char_data):
      rect_tag = "rect" + str(index)
      color_str = prog.dat_to_col_dict[pixel]
      draw_canvas.itemconfig(rect_tag, fill=color_str, outline=color_str)

def char_to_hex(char_data):
  char_hex = ""
  for x in range(8):
    upperbyte = ""
    lowerbyte = ""
    row = char_data[x*8: x*8+8]
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
  old_coords = sheet_canvas.coords("select_rect")
  new_coords = None
  char_num = sheet_canvas.getvar('active_char')
  if sheet_canvas.getvar('char_exists'):
    new_coords = sheet_canvas.coords("img" + str(char_num))
  else:
    new_coords = sheet_canvas.coords("rect" + str(char_num))
  delta_pos = ((new_coords[0] - old_coords[0]), (new_coords[1] - old_coords[1]))
  sheet_canvas.move("select_rect", delta_pos[0], delta_pos[1])
  
def update_tree_sel(treeview):
  window = treeview.nametowidget('.nge')
  if window.char_exists:
    sheet_num = window.active_sheet.get()
    char_num = window.active_char.get()
    id = 'sh' + str(sheet_num) + '.ch' + str(char_num)
    treeview.selection_set(id)
    treeview.see(id)
  else:
    treeview.selection_set()

def sheet_img_click(event):
  obj_tag = event.widget.itemconfig('current', 'tags')[-1].split(' ')[0]
  if 'img' in obj_tag:
    char_num = int(obj_tag[3:])
    event.widget.event_generate('<<Char-Change>>', state=char_num)
  elif 'rect' in obj_tag:
    char_num = int(obj_tag[4:])
    event.widget.event_generate('<<Char-Change>>', state=char_num)

def sheet_img_dbl_click(event):
  obj_tag = event.widget.itemconfig('current', 'tags')[-1].split(' ')[0]
  root = event.widget.winfo_toplevel()
  char_num = int(obj_tag[4:])
  AddCharDialog(event.widget.nametowidget('.nge'), char_num)

def tree_sheet_click(event):
  id = event.widget.selection()[0]
  sheet_num = id[2:]
  if sheet_num != event.widget.getvar('active_sheet'):
    event.widget.event_generate('<<Sheet-Change>>', state=sheet_num)

def tree_char_click(event):
  id = event.widget.selection()[0].split('.')
  sheet_num = id[0][2:]
  char_num = id[1][2:]
  if sheet_num != event.widget.getvar('active_sheet'):
    event.widget.event_generate('<<Sheet-Change>>', state=sheet_num)
  if char_num != event.widget.getvar('active_char'):
    event.widget.event_generate('<<Char-Change>>', state=char_num)

###      Individual Update Functions       ###
# These functions update individual widgets! #
##############################################

# Updates the image of the character on the sheet canvas.
# Called by sync_char_data after drawing
def update_char_img(char_data: list, img: PhotoImage):
  img_data = prog.create_img_data(char_data)
  img.configure(data=img_data)

# Updates the hex of the active character in the hex_txt widget.
# Called by sync_char_data after drawing.
def update_hex_txt(hex_txt: Text, data: list):
  if data is not None:
    char_num = hex_txt.getvar('active_char')
    char_hex = char_to_hex(data)
    index_line = str(char_num+1)
    hex_txt.delete(index_line + '.1', index_line+'.54')
    hex_txt.insert(index_line +'.1', char_hex, ("char" + str(char_num)))

# Updates the selected text in the hex widget. 
# Called when changing characters or sheets.
def update_txt_sel(hex_txt):
  prev_char = hex_txt.nametowidget('.nge').prev_char
  active_char = hex_txt.nametowidget('.nge').active_char.get()
  hex_txt.tag_config('char' + str(prev_char), background="#ffffff")
  hex_txt.children['lbl' + str(prev_char)].configure(background="#ffffff")
  hex_txt.tag_config('char' + str(active_char), background="#cccccc")
  hex_txt.children['lbl' + str(active_char)].configure(background="#cccccc")
  hex_txt.see(str(active_char+1) + '.0')

def tree_char_add(treeview, new_char):
  sheet_num = treeview.getvar('active_sheet')
  icon = treeview.nametowidget('.nge').images['character']
  parent_id = 'sh' + str(sheet_num)
  siblings = treeview.get_children(parent_id)
  pos = 'end'
  for index, sibling in enumerate(siblings):
    if int(new_char[0]) >= int(sibling[6:]):
      pos = index + 1
  item_id = parent_id + '.ch' + str(new_char[0])
  treeview.insert(parent=parent_id, index=pos, iid=item_id, image=icon, text=new_char[1])

def sheet_canv_add(sheet_canvas, new_char, img):
  rect_id = 'rect' + str(new_char[0])
  coords = sheet_canvas.coords(rect_id)
  img_name = 'img' + new_char[0]
  obj = sheet_canvas.delete(rect_id)
  sheet_canvas.create_image(coords[0]+1, coords[1]+1, image=img, tag=img_name, anchor=NW)
  sheet_canvas.tag_bind(img_name, '<ButtonRelease-1>', sheet_img_click)
  print('lmao')