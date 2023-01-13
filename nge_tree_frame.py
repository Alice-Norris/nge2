from tkinter.ttk import Frame, Treeview, Button, Scrollbar
from nge_widget_configs import tree_frame_cfgs
from nge_classes import Book, AddCharDialog, AddSheetDialog, RemCharDialog, RemSheetDialog

class TreeFrame(Frame):
  treeview = None
  tree_scroll = None

  def __init__(cls, parent, sh_var, ch_var):
    Frame.__init__(cls, parent, **{"name" : "tree_frame", "class_" : "Frame", "borderwidth" : 2, "relief" : "groove"})
    cls.root = cls.winfo_toplevel()
    cls.book = parent.book
    ch_var.trace_add('write', cls.update_tree_sel)
    cls.grid(**{ "sticky" : "EW", "column" : 2, "row" : 2 })
    cfg_iter = iter(tree_frame_cfgs.items())
    while (cfg := next(cfg_iter, None)) is not None:
      constr = None
      opts = cfg[1]
      if cfg[0] == "frame":
        constr = Frame
      elif cfg[0] == "treeview":
        constr = Treeview
      elif cfg[0] == "btn":
        constr = Button
        opts[0][0]["command"] = cls.add_sheet
        opts[1][0]["command"] = cls.rem_sheet
        opts[2][0]["command"] = cls.add_char
        opts[3][0]["command"] = cls.rem_char
      elif cfg[0] == "scrollbar":
        constr = Scrollbar
      
      opt_iter = iter(opts)
      while (opt := next(opt_iter, None)) is not None:
        opt[0]["master"] = cls
        widget = constr(**opt[0])
        if opt[0]["name"] == 'file_treeview':
          cls.treeview = widget
        if opt[0]["name"] == 'tree_scrollbar':
          cls.tree_scroll = widget
        widget.grid(**opt[1])
    cls.treeview_setup()
    upd_tree_sel = cls.register(cls.update_tree_sel)
    cls.tk.call("bind", cls, "<<Char-Change>>", upd_tree_sel + ' %s')
    upd_tree = cls.register(cls.update_tree)
    cls.tk.call("bind", cls, "<<Char-Add>>", upd_tree)
    cls.tk.call("bind", cls, "<<Char-Rem>>", upd_tree)
    cls.tk.call("bind", cls, "<<Sheet-Add>>", upd_tree)
    cls.tk.call("bind", cls, "<<Sheet-Rem>>", upd_tree)

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