from tkinter.ttk import Frame, Treeview, Button, Scrollbar
from nge_widget_configs import tree_fileview_cfg, tree_btn_cfgs, tree_subframe_cfg, tree_scroll_cfg
from nge_classes import Book, AddCharDialog, AddSheetDialog, RemCharDialog, RemSheetDialog

class TreeFrame(Frame):
  treeview = None
  tree_scroll = None
  tree_btns = {}
  btn_subframe = None

  def __init__(cls, parent, sh_var, ch_var):
    Frame.__init__(cls, parent, **{"name" : "tree_frame", "class_" : "Frame", "borderwidth" : 2, "relief" : "groove"})
    cls.grid(**{ "sticky" : "EW", "column" : 2, "row" : 2 })
    cls.root = cls.winfo_toplevel()
    cls.book = parent.book
    ch_var.trace_add('write', cls.update_tree_sel)
    
    cls.mk_widgets()
    cls.treeview_setup()
    upd_tree_sel = cls.register(cls.update_tree_sel)
    cls.tk.call("bind", cls, "<<Char-Change>>", upd_tree_sel + ' %s')
    upd_tree = cls.register(cls.update_tree)
    cls.tk.call("bind", cls, "<<Char-Add>>", upd_tree)
    cls.tk.call("bind", cls, "<<Char-Rem>>", upd_tree)
    cls.tk.call("bind", cls, "<<Sheet-Add>>", upd_tree)
    cls.tk.call("bind", cls, "<<Sheet-Rem>>", upd_tree)

  def mk_widgets(cls):
    subframe_cfg = tree_subframe_cfg[0]
    subframe_grid = tree_subframe_cfg[1]
    subframe_cfg["master"] = cls
    cls.btn_subframe = Frame(**subframe_cfg)
    cls.btn_subframe.grid(**subframe_grid)

    treeview_cfg = tree_fileview_cfg[0]
    treeview_grid = tree_fileview_cfg[1]
    treeview_cfg["master"] = cls
    cls.treeview = Treeview(**treeview_cfg)
    cls.treeview.grid(**treeview_grid)

    scroll_cfg = tree_scroll_cfg[0]
    scroll_grid = tree_scroll_cfg[1]
    scroll_cfg["master"] = cls
    cls.tree_scroll = Scrollbar(**scroll_cfg)
    cls.tree_scroll.grid(**scroll_grid)

    for btn_opts in tree_btn_cfgs:
      btn_cfg = btn_opts[0]
      btn_grid = btn_opts[1]

      btn_cfg["master"] = cls.btn_subframe
      cls.tree_btns[btn_cfg["name"]] = Button(**btn_cfg)
      cls.tree_btns[btn_cfg["name"]].grid(**btn_grid)

  def char_chg_det(cls, event):
    print('lmao')

  def treeview_setup(cls):
    window = cls.treeview.nametowidget('.nge')
    bk_icon = window.images["book"]
    sh_icon = window.images["sheet"]
    ch_icon = window.images["character"]
    cls.treeview["yscrollcommand"] = cls.tree_scroll.set
    cls.tree_scroll["command"] = cls.treeview.yview
    cls.treeview.insert(parent="", iid='book', index="end", open=True, image=bk_icon, text=cls.book.name)
    for sheet in cls.book.sheets:
      sheet_tag = 'sh' + str(sheet.id)
      cls.treeview.insert(parent='book', iid=sheet_tag, index="end", image=sh_icon, tag=sheet_tag, text=sheet.name)
      cls.treeview.tag_bind(sheet_tag, '<ButtonRelease-1>', cls.tree_sheet_click)
      char_list = sheet.char_list
      for char in char_list:
        char_tag = sheet_tag + ".ch" + str(char.id)
        cls.treeview.insert(parent=sheet_tag, iid=char_tag, index="end", image=ch_icon, tag=char_tag, text=char.name)
        cls.treeview.tag_bind(char_tag, '<ButtonRelease-1>', cls.tree_char_click)
    cls.treeview.selection_set('sh0.ch0')
    cls.treeview.see('sh0.ch0')

  def tree_char_click(cls, event):
    item_id = event.widget.selection()[0]
    (sh_id, ch_id) = (int(x[2:]) for x in item_id.split('.'))
    char_data = cls.book[sh_id].char_by_id(ch_id)
    if sh_id != cls.getvar('sheet_id_var'):
      cls.setvar('sheet_id_var', sh_id)
    if ch_id != cls.getvar('char_id_var'):
      cls.setvar('char_id_var', ch_id)
  
  def tree_sheet_click(cls, event):
    id = event.widget.selection()[0]
    sh_id = int(id[2:])
    if sh_id != cls.getvar('sheet_id_var'):
      children = cls.treeview.get_children('book')
      for child in children:
        if child != id:
          cls.treeview.item(child, open=False)
        if child == id:
          cls.treeview.item(child, open=True)
      cls.setvar('sheet_id_var', sh_id)
      cls.setvar('char_id_var', 0)

  def update_tree(cls):
    cls.treeview.delete('book')
    cls.treeview_setup()

  def update_tree_sel(cls, *args):
    sh_id = cls.getvar('sheet_id_var')
    ch_id = cls.getvar('char_id_var')
    item_id = 'sh' + str(sh_id) + '.ch' + str(ch_id)
    cls.treeview.selection_set(item_id)

  def add_sheet(cls):
    AddSheetDialog(cls.master)

  def rem_sheet(cls):
    RemSheetDialog(cls.master)

  def add_char(cls):
    AddCharDialog(cls.master)

  def rem_char(cls):
    RemCharDialog(cls.master)