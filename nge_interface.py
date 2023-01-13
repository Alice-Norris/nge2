from tkinter.ttk import Frame, Button, Treeview, Scrollbar, LabelFrame, Label
from nge_classes import AddSheetDialog, RemSheetDialog, AddCharDialog, RemCharDialog
from tkinter import Canvas, Text, Menu, FALSE
import nge_widget_configs as cfgs
import nge_gui_logic as gui

####  ("@./erasercur2.xbm", "erasercur2mask.xbm", "#000000", "#FFFFFF")

class userInterface:
  # Each entry consists of a name as a key and the frame
  # as its value. str:frame_name : ttk.Frame:frame
  widgets = {}

  def __init__ (cls, root):
    cls.root = root
    cls.create_widgets()
    #cls.setup_widgets()


  def create_widgets(cls):
    cls.mk_menu()
    cls.mk_draw_area(cfgs.draw_frame_cfgs)
    cls.mk_sheet_area(cfgs.sheet_frame_cfgs)
    cls.mk_info_area(cfgs.info_frame_cfgs)
    cls.mk_hex_area(cfgs.hex_frame_cfgs)
    cls.mk_tree_area(cfgs.tree_frame_cfgs)

  def mk_draw_area(cls, cfgs):
    cfg_iter = iter(cfgs["frame"])
    print('lmao')
    while (opts := next(cfg_iter, None)) is not None:
      cfg = opts[0]
      grid = opts[1]
  

      if cfg["name"] == "draw_frame":
        cfg["master"] = cls.root
        frame = Frame(**cfg)
        cls.draw_frame = frame
      else:
        cfg["master"] = cls.draw_frame
        frame = Frame(**cfg)

      frame.grid(**grid)
    
    cfg_iter = iter(cfgs["canvas"])
    while (opts := next(cfg_iter, None)) is not None:
      cfg = opts[0]
      grid = opts[1]
      
      cfg["master"] = cls.draw_frame

      canvas = Canvas(**cfg)
      canvas.grid(**grid)

    cfg_iter = iter(cfgs["btn"])
    while (opts := next(cfg_iter, None)) is not None:
      cfg = opts[0]
      grid = opts[1]

      cfg["master"] = cls.draw_frame

      btn = Button(**cfg)
      btn.grid(**grid)
    
    gui.draw_grid_setup(cls.draw_frame.children["draw_canvas"])
    gui.col_palette_setup(cls.draw_frame.children["col_palette"])
    cls.draw_frame.bind('<<Char-Change>>', gui.update_draw_canvas)

  
  def mk_sheet_area(cls, cfgs):
    frame_cfg = cfgs["frame"][0][0]
    frame_grid = cfgs["frame"][0][1]

    frame_cfg["master"] = cls.root
    
    frame = Frame(**frame_cfg)
    cls.sheet_frame = frame
    frame.grid(**frame_grid)

    canvas_cfg = cfgs["canvas"][0][0]
    canvas_grid = cfgs["canvas"][0][1]

    canvas_cfg["master"] = cls.sheet_frame

    canvas = Canvas(**canvas_cfg)
    canvas.grid(**canvas_grid)

    cls.sheet_canvas = cls.root.nametowidget('.nge.sheet_frame.sheet_canvas')
    gui.sheet_grid_setup(cls.sheet_canvas)

  def mk_info_area(cls, cfgs):
    cfg_iter = iter(cfgs["frame"])
    while ( opts := next(cfg_iter, None)) is not None:
      cfg = opts[0]
      grid = opts[1]

      cfg["master"] = cls.root
      
      frame = Frame(**cfg)
      cls.info_frame = frame
      frame.grid(**grid)

    cfg_iter = iter(cfgs["labelframe"])
    while (opts := next(cfg_iter, None)) is not None:
      cfg = opts[0]
      grid = opts[1]
    
      cfg["master"] = cls.info_frame

      labelframe = LabelFrame(**cfg)
      labelframe.grid(**grid)

    cfg_iter = iter(cfgs["label"])
    while (opts := next(cfg_iter, None)) is not None:
      cfg = opts[0]
      grid = opts[1]

      cfg["master"] = cls.info_frame
      
      label = Label(**cfg)
      label.grid(**grid)

  def mk_hex_area(cls, cfgs):
    frame_cfg = cfgs["frame"][0][0]
    frame_grid = cfgs["frame"][0][1]

    frame_cfg["master"] = cls.root

    frame = Frame(**frame_cfg)
    cls.hex_frame = frame
    frame.grid(**frame_grid)

    txt_cfg = cfgs["text"][0][0]
    txt_grid = cfgs["text"][0][1]

    txt_cfg["master"] = cls.hex_frame

    txt = Text(**txt_cfg)
    txt.grid(**txt_grid)

    scroll_cfg = cfgs["scrollbar"][0][0]
    scroll_grid = cfgs["scrollbar"][0][1]

    scroll_cfg["master"] = cls.hex_frame
    scroll = Scrollbar(**scroll_cfg)
    scroll.grid(**scroll_grid)

    gui.hex_txt_setup(cls.hex_frame.children["hex_txt"],
                      cls.hex_frame.children["hex_scrollbar"])

  def mk_tree_area(cls, cfgs):
    cfg_iter = iter(cfgs["frame"])
    while (opts := next(cfg_iter, None)) is not None:
      cfg = opts[0]
      grid = opts[1]

      if cfg["name"] == "tree_frame":
        cfg["master"] = cls.root
        frame = Frame(**cfg)
        cls.tree_frame = frame
        frame.grid(**grid)
      else:
        cfg["master"] = cls.tree_frame
        frame = Frame(**cfg)
        frame.grid(**grid)

    cfg_iter = iter(cfgs["treeview"])
    while (opts := next(cfg_iter, None)) is not None:
      cfg = opts[0]
      grid = opts[1]

      cfg["master"] = cls.tree_frame

      treeview = Treeview(**cfg)
      treeview.grid(**grid)
    
    cfg_iter = iter(cfgs["btn"])
    while (opts := next(cfg_iter, None)) is not None:
      cfg = opts[0]
      grid = opts[1]

      cfg["master"] = cls.tree_frame

      btn = Button(**cfg)
      btn.grid(**grid)
    
    cfg_iter = iter(cfgs["scrollbar"])
    while (opts := next(cfg_iter, None)) is not None:
      cfg = opts[0]
      grid = opts[1]

      cfg["master"] = cls.tree_frame

      scroll = Scrollbar(**cfg)
      scroll.grid(**grid)

    gui.treeview_setup(cls.tree_frame.children["file_treeview"],
                       cls.tree_frame.children["tree_scrollbar"])

  # # Creating frames for different program areas
  # def mk_frames(cls, canvas_cfgs: list):
  #   frame_iter = iter(canvas_cfgs)
    
  #   for frame_cfg in range(len(canvas_cfgs) // 2):
  #     cfg = next(frame_iter)
  #     grid_opts = next(frame_iter)
      
  #     gui.set_parent(cls.root, cfg)

  #     frame = Frame(**cfg)
  #     frame.grid_propagate(0)
  #     frame.grid(**grid_opts)

  # # Creating subframes, which go inside of frames for
  # # organization
  # def mk_subframes(cls, subframe_cfgs):
  #   subframe_iter = iter(subframe_cfgs)
    
  #   for dict in range(len(subframe_cfgs) // 2):
  #     subframe_cfg = next(subframe_iter)
  #     subframe_grid_opts = next(subframe_iter)
      
  #     gui.set_parent(cls.root, subframe_cfg)

  #     frame = Frame(**subframe_cfg)
  #     frame.grid(**subframe_grid_opts)

  # # Creating the sheet and draw canvases
  # def mk_canvases(cls, canvas_cfgs):
  #   canvas_iter = iter(canvas_cfgs)

  #   for dict in range(len(canvas_cfgs) // 2):
  #     canvas_cfg = next(canvas_iter)
  #     canvas_grid_opts = next(canvas_iter)
      
  #     gui.set_parent(cls.root, canvas_cfg)

  #     canvas = Canvas(**canvas_cfg)

  #     if canvas_cfg["name"] == "draw_canvas":
  #       canvas.bind('<ButtonRelease-1>', cls.draw_canvas_callback)
  #       canvas.bind('<ButtonRelease-3>', cls.draw_canvas_callback)
  #     elif canvas_cfg["name"] == "col_palette":
  #       canvas.bind('<ButtonRelease-1>', cls.fg_callback)
  #       canvas.bind('<ButtonRelease-3>', cls.bg_callback)
  #     canvas.grid(**canvas_grid_opts)

  # def mk_treeview(cls, treeview_cfg):
  #   treeview_iter = iter(treeview_cfg)
  #   for dict in range(len(treeview_cfg) // 2):
  #     treeview_cfg = next(treeview_iter)
  #     treeview_grid_opts = next(treeview_iter)
      
  #     gui.set_parent(cls.root, treeview_cfg)

  #     view = Treeview(**treeview_cfg)
  #     view.column("#0")
  #     view.grid(**treeview_grid_opts)

  # def mk_treeview_btns(cls, treeview_btn_cfgs):
  #   btn_iter = iter(treeview_btn_cfgs)

  #   for dict in range(len(cfgs.treeview_btn_cfgs) // 2):
  #     btn_cfg = next(btn_iter)
  #     btn_grid_opts = next(btn_iter)
  #     if btn_cfg["name"] == "add_sh":
  #       btn_cfg["command"] = cls.add_sh
  #     elif btn_cfg["name"] == "rem_sh":
  #       btn_cfg["command"] = cls.rem_sh
  #     elif btn_cfg["name"] == "add_ch":
  #       btn_cfg["command"] = cls.add_ch
  #     else:
  #       btn_cfg["command"] = cls.rem_ch

  #     gui.set_parent(cls.root, btn_cfg)

  #     btn = Button(**btn_cfg)
  #     btn.grid(**btn_grid_opts)

  # def mk_tool_btns(cls, tool_btn_cfgs):
  #   btn_iter = iter(tool_btn_cfgs)

  #   for dict in range(len(tool_btn_cfgs) // 2):
  #     btn_cfg = next(btn_iter)
  #     btn_grid_opts = next(btn_iter)

  #     gui.set_parent(cls.root, btn_cfg)

  #     #creating buttons
  #     btn = Button(**btn_cfg)
  #     btn.grid(**btn_grid_opts)

  #   cls.root.bind_class('tool_btn', '<ButtonRelease-1>', cls.tool_btn_callback)

  # def mk_scrollbars(cls, scrollbar_cfgs):
  #   scroll_iter = iter(scrollbar_cfgs)
    
  #   for dict in range(len(scrollbar_cfgs) // 2):
  #     scroll_cfg = next(scroll_iter)
  #     scroll_grid_opts = next(scroll_iter)
      
  #     gui.set_parent(cls.root, scroll_cfg)

  #     if scroll_cfg["name"] == "hex_scrollbar":
  #       scroll_cfg["command"] = cls.scroll_hex_txt
  #     scroll = Scrollbar(**scroll_cfg)
  #     scroll.grid(**scroll_grid_opts)

  # def mk_hex_txt(cls, txt_cfgs):
  #   txt_iter = iter(txt_cfgs)
  #   hex_scroll = cls.root.nametowidget('.nge.hex_frame.hex_scrollbar')
  #   for dict in range(len(txt_cfgs) // 2):
  #     txt_cfg = next(txt_iter)
  #     txt_grid_opts = next(txt_iter)
      
  #     gui.set_parent(cls.root, txt_cfg)

  #     txt_cfg["yscrollcommand"] = hex_scroll.set
  #     hex_txt = Text(**txt_cfg)
  #     hex_txt.grid(**txt_grid_opts)
  #     hex_txt.bind()

  # def mk_lbl_frames(cls, lbl_frame_cfgs):
  #   lbl_iter = iter(lbl_frame_cfgs)
  #   for dict in range(len(lbl_frame_cfgs) // 2):
  #     lbl_cfg = next(lbl_iter)
  #     lbl_grid_opts = next(lbl_iter)

  #     gui.set_parent(cls.root, lbl_cfg)

  #     lbl = LabelFrame(**lbl_cfg)
  #     lbl.grid_propagate(0)
  #     lbl.grid(**lbl_grid_opts)


  # def mk_lbls(cls, lbl_txt_cfgs, lbl_var_cfgs):
  #   cfg_lists = [lbl_txt_cfgs, lbl_var_cfgs]
  #   for cfg_list in cfg_lists:
  #     lbl_iter = iter(cfg_list)
  #     for dict in range(len(cfg_list) // 2):
  #       lbl_cfg = next(lbl_iter)
  #       lbl_grid_opts = next(lbl_iter)

  #       gui.set_parent(cls.root, lbl_cfg)

  #       lbl = Label(**lbl_cfg)

  #       lbl.grid(**lbl_grid_opts)

  def tool_btn_callback(cls, event):
    btn = event.widget
    new_tool = btn._name[:-4]
    curr_tool = btn.getvar('active_tool')
    if curr_tool != '':
      old_btn = btn.nametowidget('.nge.draw_frame.draw_btn_frame.'+curr_tool+'_btn')
      old_btn.configure(style='nge.tool_btn')
    if new_tool != curr_tool:  
      btn.configure(style='nge.sel_tool_btn')
      btn.setvar('active_tool', new_tool)
      gui.chg_cursor(btn.nametowidget('.nge.draw_frame.draw_canvas'), new_tool)
  
  def draw_canvas_callback(cls, event):
    gui.draw_canvas_tool_click(event)
    event.widget.event_generate('<<Char-Data-Update>>')

  def fg_callback(cls, event):
    canv = event.widget
    curr_col = canv.getvar('fg_color')
    fg_canv = canv.nametowidget('.nge.draw_frame.draw_btn_frame.fg_color')
    col_sq = canv.find_closest(event.x, event.y)
    new_col = canv.itemcget(col_sq, "fill")
    if new_col != curr_col:
      canv.setvar('fg_color', new_col)
      fg_canv.configure(background=new_col)
  
  def bg_callback(cls, event):
    canv = event.widget
    curr_col = canv.getvar('bg_color')
    bg_canv = canv.nametowidget('.nge.draw_frame.draw_btn_frame.bg_color')
    col_sq = canv.find_closest(event.x, event.y)
    new_col = canv.itemcget(col_sq, "fill")
    if new_col != curr_col:
      canv.setvar('bg_color', new_col)
      bg_canv.configure(background=new_col)

  def add_sh(cls):
    AddSheetDialog(cls.root)
    print('lmao')

  def rem_sh(cls):
    RemSheetDialog(cls.root)

  def add_ch(cls):
    AddCharDialog(cls.root)

  def rem_ch(cls):
    RemCharDialog(cls.root)