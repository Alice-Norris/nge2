from nge_classes import Book, Character
from nge_librarian import Librarian
from tkinter import Toplevel, PhotoImage, BitmapImage, Canvas, NW
from random import randint

NGE_BLK = 3
NGE_DKG = 2
NGE_LTG = 1
NGE_WHT = 0

col_to_dat_dict = {
  "#000000" : NGE_BLK,
  "#555555" : NGE_DKG,
  "#aaaaaa" : NGE_LTG,
  "#ffffff" : NGE_WHT
}

dat_to_col_dict = {
  NGE_BLK : "#000000",
  NGE_DKG : "#555555",
  NGE_LTG : "#aaaaaa",
  NGE_WHT : "#ffffff"
}

def str_to_char(char_str):
  (char_id, char_name, char_data) = char_str.split('*')
  char_id = int(char_id)
  char_data = [int(x) for x in char_data.split(',')]
  char = Character(char_id, char_name)
  char.data = char_data
  return char
def randomize(book: Book):
  char_list = book.sheets[0].char_list
  for character in char_list:
    for index, pixel in enumerate(character.data):
      character.data[index] = randint(0,3)
  print("lmao")

def active_color_name(cls):
  return(cls.ui_col_dict[cls.active_color])

def update_char(draw_canvas: Canvas):
  window = draw_canvas.nametowidget('.nge')
  images = window.images
  char_num = window.getvar("active_char")
  char_data = window.char_data_list[char_num]
  for index, pixel in enumerate(char_data):
    rect_id = draw_canvas.find_withtag("rect" + str(index))[0]
    color_str = draw_canvas.itemcget(rect_id, 'fill')
    if pixel != col_to_dat_dict[color_str]:
      char_data[index] = col_to_dat_dict[color_str]
  new_img_data = create_img_data(char_data)
  img_name = "img" + str(char_num)
  images[img_name].configure(data=new_img_data)


def nge_open(librarian: Librarian, active_book: Book, file_buffer):
  librarian.load(file_buffer)
  active_book = librarian.borrow()

def nge_save_as(librarian: Librarian, file_buffer):
  librarian.save(file_buffer)

def chg_sel(id: str):
  id = id[3:]
  
  if id.find('.') != -1:
    sh_id, ch_id = id.split('.')
    active_sheet = int(sh_id[2:])
    active_char = int(ch_id[2:])
  else:
    sh_id = int(id[2:])
    active_sheet = sh_id

# Loads images upon startup.
def load_imgs(root: Toplevel):
  images = {}
  img_names = [
    "pencil.xbm",
    "bucket.xbm",
    "eraser.xbm",
    "line.xbm",
    "wht.pgm",
    "ltg.pgm",
    "dkg.pgm",
    "blk.pgm",
    "book.png",
    "sheet.png",
    "character.png",
    "sheet_add.png",
    "sheet_rm.png",
    "char_add.png",
    "char_rm.png",
    "draw_bg.png",
    "sheet_bg.png"
  ]
  
  for filename in img_names:
    name, ext = filename.split('.')
    if ext == "xbm":
      images[name] = BitmapImage(master=root, name=name, file=filename, background="#D9D9D9", foreground="#000000")
    elif ext == "pgm":
      images[name] = PhotoImage(master=root, name=name, file=filename)
    elif ext == "png":
      images[name] = PhotoImage(master=root, name=name, file=filename, format="PNG")

  return images

# Creates image data, used by draw_sheet_canv
def create_img_data(char_data: list):
  img_hdr = bytes("P6\n48 48\n3\n", encoding='utf-8')
  img_data = b''
  for row in range(len(char_data) // 8):
    start = row * 8
    end = start + 8
    pix_row = char_data[start:end]
    row_bytes = b''
    for p in pix_row:
      invert_pix = abs(p-3)
      row_bytes += bytes([invert_pix] * 3) * 6
    row_bytes = row_bytes * 6
    img_data += row_bytes
  return img_hdr + img_data
