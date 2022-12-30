from nge_interface import userInterface
from tkinter import Tk, messagebox
from tkinter.ttk import Style
import gui_logic as GL
from nge_librarian import Librarian
from nge_logic import NGE_Logic
from enum import Enum

class FileType(Enum):
  GB = 1
  CGB = 2

class NGE:
  current_file = b'\x01unnamed\x01unnamed \x19\x00\x17\x04'
  interface = None
  librarian = None
  program = None

  def __init__(cls):
    cls.root = Tk(className="nge")
    GL.set_style(cls.root)
    cls.librarian = Librarian()
    cls.program = NGE_Logic(cls.librarian, cls.root)
    cls.interface = userInterface(cls.root, cls.program)
    cls.setup()
    cls.add_bindings()
    
  def setup(cls):
    draw_canvas = cls.root.nametowidget('.draw_frame.draw_canvas')
    sheet_canvas = cls.root.nametowidget('.sheet_frame.sheet_canvas') 
    hex_hdr_txt = cls.root.nametowidget('.hex_frame.hex_txt_header')
    hex_dat_txt = cls.root.nametowidget('.hex_frame.hex_txt_data')
    treeview = cls.root.nametowidget('.tree_frame.file_tree_view')
    tree_scroll = cls.root.nametowidget('.tree_frame.tree_scrollbar')
    index = cls.librarian.request_index()
    char_list = cls.librarian.char_list(cls.program.active_sheet)
    GL.grid_setup(draw_canvas, 8, 8, False)
    GL.draw_sheet_canv(cls.program.images, sheet_canvas, char_list)
    GL.grid_setup(sheet_canvas, 16, 8, True)
    GL.hex_row_setup(hex_hdr_txt)
    GL.hex_text_setup(hex_dat_txt)
    GL.treeview_setup(treeview, tree_scroll, index, cls.program.images)
   
  def add_bindings(cls):
    hex_txt = cls.root.nametowidget('.hex_frame.hex_txt_header')
    hex_hdr = cls.root.nametowidget('.hex_frame.hex_txt_data')
    GL.txt_binds(hex_txt, hex_hdr)
    cls.root.bind_class('tool_btn', '<ButtonRelease-1>', cls.interface.tool_btn_callback)
    cls.root.bind_class('color_btn','<Button-1>', cls.interface.color_btn_callback)
    draw_canvas = cls.root.nametowidget('.draw_frame.draw_canvas')
    sheet_canvas = cls.root.nametowidget('.sheet_frame.sheet_canvas')
    draw_canvas.bind('<Button-1>', cls.interface.draw_canvas_callback)
    sheet_canvas.bind('<Button-1>', cls.interface.sheet_canvas_callback)
NGE = NGE()

NGE.root.mainloop()
