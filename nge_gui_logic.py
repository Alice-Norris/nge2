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



# Changes cursor over draw canvas when a tool is selected
# Cursor replacement must follow this format:
# cursor=("@./filename.xbm", "filenamemask.xbm", "#000000", "#FFFFFF"))
  
# When the draw_canvas is clicked with a drawing tool,
# Figures out which one it is and acts accordingly.



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
  cls.update_hex_txt(hex_txt, char_data)

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


###      Individual Update Functions       ###
# These functions update individual widgets! #
##############################################

# Updates the image of the character on the sheet canvas.
# Called by sync_char_data after drawing

# Updates the hex of the active character in the hex_txt widget.
# Called by sync_char_data after drawing.


# Updates the selected text in the hex widget. 
# Called when changing characters or sheets.


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