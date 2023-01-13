from tkinter.ttk import Frame, Label, LabelFrame
from tkinter import StringVar, IntVar
from nge_widget_configs import info_frame_cfgs
from nge_classes import Book

class InfoFrame(Frame):
  book = None
  root = None
  frames = None

  def __init__(cls, parent):
    Frame.__init__(cls, parent, **{"name" : "info_frame", "class_" : "Frame", "borderwidth" : 2, "relief" : "groove" })
    cls.root = cls.winfo_toplevel()
    cls.book = parent.book
    cls.grid(**{"sticky" : "NSEW", "column" : 0, "row" : 2})
    cfg_iter = iter(info_frame_cfgs.items())
    while (cfg := next(cfg_iter, None)) is not None:
      constr = None
      opts = cfg[1]
      if cfg[0] == "labelframe":
        constr = LabelFrame
      elif cfg[0] == "label":
        constr = Label

      opt_iter = iter(opts)
      while (opt := next(opt_iter, None)) is not None:
        if constr == LabelFrame:
          opt[0]["master"] = cls
          widget = constr(**opt[0])
          widget.grid_propagate(0)
          widget.grid(**opt[1])
        else:
          opt[0]["master"] = cls.nametowidget(opt[1]["in_"])
          widget = constr(**opt[0])
          widget.grid(**opt[1])
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