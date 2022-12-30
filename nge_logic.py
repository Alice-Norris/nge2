from nge_classes import Book, Sheet
from gui_logic import select_char
from nge_librarian import Librarian
from tkinter import Toplevel, PhotoImage, BitmapImage, Canvas, NW
from random import randint
NGE_BLK = 3
NGE_DKG = 2
NGE_LTG = 1
NGE_WHT = 0


class NGE_Logic:
  active_book = None
  active_sheet = None
  active_char = None
  active_color = "#000000"
  active_tool = None
  
  ui_col_dict = {
    "#000000" : "blk",
    "#555555": "dkg",
    "#AAAAAA" : "ltg",
    "#FFFFFF" : "wht"
  }

  data_col_dict = {
    "#000000" : NGE_BLK,
    "#555555" : NGE_DKG,
    "#AAAAAA" : NGE_LTG,
    "#FFFFFF" : NGE_WHT
  }
  
  def __init__(cls, librarian: Librarian, root: Toplevel):
    cls.librarian = librarian
    cls.root = root
    cls.active_sheet = 0
    cls.active_char = 0
    cls.active_book = cls.librarian.borrow()
    cls.randomize()
    cls.images = {}
    cls.load_imgs(cls.root)

  def randomize(cls):
    char_list = cls.active_book.sheets[0].char_list
    for character in char_list:
      for index, pixel in enumerate(character.data):
        character.data[index] = randint(0,3)
    print("lmao")
  def active_color_name(cls):
    return(cls.ui_col_dict[cls.active_color])

  def update_char(cls, pixels: tuple, canvas: Canvas):
    char_data = cls.active_book.sheets[cls.active_sheet].char_list[cls.active_char].data
    img_name = "img" + str(cls.active_char)

    for pixel in pixels:  
      char_data[pixel] = cls.data_col_dict[cls.active_color]

    canvas = cls.root.nametowidget('.sheet_frame.sheet_canvas')
    image_obj = canvas.find_withtag(img_name)
    coords = canvas.coords(image_obj)
    print(img_name in cls.root.image_names())
    cls.update_char_img(img_name, char_data)
    obj_id = canvas.find_withtag(img_name)
    print("lmao")

  def update_char_img(cls, img_name, char_data: list): 
    img_hdr = bytes("P6\n40 40\n3\n", encoding='utf-8')
    img_data = cls.create_img_data(char_data)
    img_name = "img" + str(cls.active_char)
    cls.images[img_name] = PhotoImage(master=cls.root.winfo_toplevel(), name=img_name, data=img_hdr + img_data, format="PPM")

  def open(cls, file_buffer):
    cls.librarian.load(file_buffer)
    cls.active_book = cls.librarian.borrow()
  
  def save_as(cls, file_buffer):
    cls.librarian.save(file_buffer)

  def chg_sel(cls, id: str):
    id = id[3:]
    
    if id.find('.') != -1:
      sh_id, ch_id = id.split('.')
      cls.active_sheet = int(sh_id[2:])
      cls.active_char = int(ch_id[2:])
    else:
      sh_id = int(id[2:])
      cls.active_sheet = sh_id

  # Loads images upon startup.
  def load_imgs(cls, root: Toplevel):
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
      "char_rm.png"
    ]
    
    for filename in img_names:
      name, ext = filename.split('.')
      if ext == "xbm":
        cls.images[name] = BitmapImage(master=root, name=name, file=filename, background="#D9D9D9", foreground="#000000")
      elif ext == "pgm":
        cls.images[name] = PhotoImage(master=root, name=name, file=filename)
      elif ext == "png":
        cls.images[name] = PhotoImage(master=root, name=name, file=filename, format="PNG")
    
    char_list = cls.active_book.sheets[cls.active_sheet].char_list
    for char in char_list:
      img_hdr = bytes("P6\n40 40\n3\n", encoding='utf-8')
      img_data = cls.create_img_data(char.data)
      img_name = "img" + str(char.id)
      cls.images[img_name] = PhotoImage(master=root, name=img_name, data=img_hdr + img_data, format="PPM")
    
    print(cls.root.image_names())

  def get_char_data(cls):
    char_data = cls.active_book.sheets[cls.active_sheet][cls.active_char].data
    return char_data
  
  # Creates image data, used by draw_sheet_canv
  def create_img_data(cls, char_data: list):
    img_data = b''
    for row in range(len(char_data) // 8):
      start = row * 8
      end = start + 8
      pix_row = char_data[start:end]
      row_bytes = b''
      for p in pix_row:
        invert_pix = abs(p-3)
        row_bytes += bytes([invert_pix] * 3) * 5
      row_bytes = row_bytes * 5
      img_data += row_bytes
    return img_data
