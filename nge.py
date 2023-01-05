from nge_interface import userInterface
from tkinter import IntVar, StringVar, BooleanVar, filedialog
from tkinter.ttk import Frame
import nge_gui_logic as GL
from nge_librarian import Librarian
from enum import Enum
from nge_logic import load_imgs, randomize, update_char, nge_save_as
import nge_gui_logic as gui
class FileType(Enum):
  GB = 1
  CGB = 2

class NGE(Frame):
  current_file = b'\x01unnamed\x01unnamed \x19\x00\x17\x04'
  interface = None
  librarian = None
  program = None

  def __init__(cls, master=None):
    Frame.__init__(cls, name="nge")
    cls.grid()
    cls.root = cls.winfo_toplevel()
    GL.set_style(cls.root)
    cls.librarian = Librarian()
    cls.active_book = cls.librarian.borrow()
    
    cls.sheet_var = IntVar(master = cls.root, name="active_sheet", value=0)
    cls.char_var = IntVar(master = cls.root, name="active_char", value=0)
    cls.fg_col_var = StringVar(master = cls.root, name="fg_color", value='None')
    cls.bg_col_var = StringVar(master=cls.root, name="bg_color", value='None')
    cls.tool_var = StringVar(master=cls.root, name = "active_tool", value=None)
    cls.char_edited = BooleanVar(master=cls.root, name = "char_edited", value=False)
    
    cls.images = load_imgs(cls.root, cls.active_book, cls.sheet_var.get())
    cls.update_char_data_list()
    
    cls.interface = userInterface(cls, cls.char_data_list)

    cls.update_widgets = {
      'draw_canvas' : cls.root.nametowidget('nge.draw_frame.draw_canvas'),
      'sheet_canvas' : cls.root.nametowidget('nge.sheet_frame.sheet_canvas'),
      'hex_txt' : cls.root.nametowidget('.nge.hex_frame.hex_txt'),
      'file_tree_view' : cls.root.nametowidget('.nge.tree_frame.file_tree_view')
    }

  def update_char_data_list(cls):
    sheet_num = cls.sheet_var.get()
    new_char_list = []
    for char in cls.active_book.sheets[sheet_num].char_list:
      new_char_list.append(char.data)
    cls.char_data_list = new_char_list

  def char_chg(cls, *args):
    if cls.active_char != cls.char_var.get():
      cls.active_char = cls.char_var.get()
      gui.gui_update(cls.update_widgets)

  def sheet_chg(cls, *args):
    if cls.active_sheet != cls.sheet_var.get():
      cls.active_sheet = cls.sheet_var.get()
      cls.char_var.set(0)
      cls.update_char_data_list()

  def tool_chg(cls, *args):
    if cls.active_tool != cls.tool_var.get():
      cls.active_tool = cls.tool_var.get()
    draw_canvas = cls.root.nametowidget('.nge.draw_frame.draw_canvas')
    prev_tool = cls.prev_tool
    if prev_tool != None:
      old_btn_path = '.nge.draw_frame.draw_btn_frame.'+prev_tool+'_btn'
      old_btn = cls.root.nametowidget(old_btn_path)
      old_btn.configure(style='nge.tool_btn')
    gui.chg_cursor(draw_canvas, cls.active_tool)

  def char_update(cls, *args):
    hex_txt = cls.nametowidget('.nge.hex_frame.hex_txt')
    char_num = cls.active_char
    char_data = cls.char_data_list[char_num]
    gui.char_to_hex(char_data)
    gui.update_draw_canvas
    update_char(cls.update_widgets["draw_canvas"])
    gui.update_hex_txt(hex_txt, char_num, char_data)
    gui.update_txt_sel(hex_txt)
    cls.char_edited.set(False)

  def save_as_callback(cls):
    file_buff = filedialog.asksaveasfile(
      mode='wb',
      defaultextension=".nge",
      filetypes=[('NGE File', '*.nge')],
      title="Save as..."
    )
    for sheet in cls.active_book.sheets:
      for index, character in enumerate(sheet.char_list):
        character.data = cls.char_data_list[index]
    cls.librarian.save(file_buff, cls.active_book)

  def open_callback(cls):
    file_buff = filedialog.askopenfile(
      mode='rb',
      defaultextension=".nge",
      filetypes=[('NGE File', '*.nge')],
      title="Open File"
    )
    cls.librarian.load(file_buff)
    cls.active_book = cls.librarian.borrow()
    cls.interface.setup_widgets()
    
nge = NGE()
nge.master.title('NGE')
nge.root.mainloop()
