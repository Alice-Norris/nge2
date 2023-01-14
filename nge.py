from tkinter import filedialog, Menu
from tkinter.ttk import Frame, Menubutton
from nge_librarian import Librarian
from enum import Enum
from nge_logic import load_imgs
from nge_file_ops import write_file, read_file
import nge_gui_logic as gui
from nge_draw_frame import DrawFrame
from nge_sheet_frame import SheetFrame
from nge_info_frame import InfoFrame
from nge_hex_frame import HexFrame
from nge_tree_frame import TreeFrame
class FileType(Enum):
  GB = 1
  CGB = 2

class NGE(Frame):
  current_file = b'\x01unnamed\x01unnamed \x19\x00\x17\x04'
  librarian = None
  program = None
  prev_sheet = None
  prev_char = None
  frames = {}
  def __init__(cls, master=None):
    Frame.__init__(cls, name="nge")
    cls.grid()
    cls.root = cls.winfo_toplevel() 
    cls.mk_menu()
    gui.set_style(cls.root)
    cls.librarian = Librarian()
    cls.book = cls.librarian.borrow()
    cls.images = load_imgs(cls.root)

    cls.frames["info"] = InfoFrame(cls)

    sh_var = cls.frames["info"].sheet_id_var
    ch_var = cls.frames["info"].char_id_var
    cls.frames["draw"] = DrawFrame(cls, sh_var, ch_var)
    cls.frames["sheet"] = SheetFrame(cls, sh_var, ch_var)
    cls.frames["hex"] = HexFrame(cls, sh_var, ch_var)
    cls.frames["tree"] = TreeFrame(cls, sh_var, ch_var)

    info_frame = cls.frames["info"]
    info_frame.frames = cls.frames

  def save_as_callback(cls):
    file_buff = filedialog.asksaveasfile(
      mode='wb',
      defaultextension=".nge",
      filetypes=[('NGE File', '*.nge')],
      title="Save as..."
    )
    data = write_file(cls.book)
    file_buff.write(data)

  def open_callback(cls):
    file_buff = filedialog.askopenfile(
      mode='rb',
      defaultextension=".nge",
      filetypes=[('NGE File', '*.nge')],
      title="Open File"
    )
    cls.book = read_file(file_buff.name)
    print('lmao')
    cls.setvar('sheet_id_var', 0)
    cls.setvar('char_id_var', 0)
    sh_var = cls.frames["info"].sheet_id_var
    ch_var = cls.frames["info"].char_id_var
    cls.frames["draw"] = DrawFrame(cls, sh_var, ch_var)
    cls.frames["sheet"] = SheetFrame(cls, sh_var, ch_var)
    cls.frames["tree"] = TreeFrame(cls, sh_var, ch_var)
    cls.frames["hex"] = HexFrame(cls, sh_var, ch_var)
    print('lmao')

  def exit_nge(cls):
    cls.root.destroy()
    cls.quit()

  def mk_menu(cls):
    menu = Menu(cls)
    file_menu = Menu(menu, tearoff=0)
    file_menu.add_command(label='Open...', command=cls.open_callback)
    file_menu.add_command(label='Save As...', command=cls.save_as_callback)
    file_menu.add_command(label='Quit', command=cls.exit_nge)
    file_btn = Menubutton(cls, text='File', menu=file_menu)
    file_btn.grid(sticky = 'w')
    file_btn.menu=file_menu
    

nge = NGE()
nge.master.title('NGE')
nge.root.mainloop()