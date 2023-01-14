from tkinter.ttk import Frame, Label, LabelFrame
from tkinter import StringVar, IntVar
from nge_widget_configs import info_lbl_frame_cfgs, info_lbl_cfgs
from nge_classes import Book

class InfoFrame(Frame):
  book = None
  root = None
  lbl_frames = {}
  lbls = {}
  var_lbls = {}

  def __init__(cls, parent):
    Frame.__init__(cls, parent, **{"name" : "info_frame", "class_" : "Frame", "borderwidth" : 2, "relief" : "groove" })
    cls.grid(**{"sticky" : "NSEW", "column" : 0, "row" : 2})
    cls.root = cls.winfo_toplevel()
    cls.book = parent.book
    cls.mk_widgets()
    cls.set_vars()

  def mk_widgets(cls):
    for lbl_frame_opts in info_lbl_frame_cfgs:
      lbl_frame_cfg = lbl_frame_opts[0]
      lbl_frame_grid = lbl_frame_opts[1]
      lbl_name = lbl_frame_cfg["name"]

      lbl_frame_cfg["master"] = cls
      lbl_frame = LabelFrame(**lbl_frame_cfg)

      cls.lbl_frames[lbl_name] = lbl_frame
      lbl_frame.grid(**lbl_frame_grid)
    
    for lbl_opts in info_lbl_cfgs:
      lbl_cfg = lbl_opts[0]
      lbl_grid = lbl_opts[1]

      lbl_name = lbl_cfg["name"]
      parent_path = lbl_grid["in_"]
      lbl_cfg["master"] = cls.nametowidget(parent_path)
      lbl = Label(**lbl_cfg)
      cls.lbls[lbl_name] = lbl
      lbl.grid(**lbl_grid)

  def set_vars(cls):
    num_sheets = len(cls.book.sheets)
    sheet = cls.book[0]
    num_chars = len(cls.book[0].char_list)
    char = cls.book[0][0]
    cls.book_name_var = StringVar(master=cls, name='book_name_var', value=cls.book.name)
    cls.sheet_num_var = IntVar(master=cls, name='sheet_num_var', value=len(cls.book.sheets))
    cls.sheet_name_var = StringVar(master=cls, name='sheet_name_var', value=cls.book[0].name)
    cls.sheet_id_var = IntVar(master=cls, name='sheet_id_var', value=cls.book[0][0].id)
    cls.sheet_id_var.trace_add('write', cls.update_sheet_vars)
    cls.char_num_var = IntVar(master=cls, name='char_num_var', value=len(cls.book[0].char_list))
    cls.char_name_var = StringVar(master=cls, name='char_name_var', value=cls.book[0][0].name)
    cls.char_id_var = IntVar(master=cls, name='char_id_var', value=cls.book[0][0].id)

  def update_sheet_vars(cls, *args):
    sh_id = cls.sheet_id_var.get()
    cls.sheet_num_var.set(len(cls.book.sheets))
    sheet = cls.book.sheet_by_id(sh_id)
    cls.sheet_name_var.set(sheet.name)
    cls.char_num_var.set(len(sheet.char_list))
  
  def update_char_vars(cls, *args):
    sh_id = cls.sheet_id_var.get()
    ch_id = cls.char_id_var.get()
    char_name = cls.book[sh_id].char_by_id[ch_id].name
    cls.char_name_var.set(char_name)