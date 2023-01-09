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

  def __init__ (cls, root, char_data_list):#, images: dict):
    cls.root = root
    cls.char_data_list = char_data_list
    cls.create_widgets()
    cls.setup_widgets()
    cls.root.setvar('fg_color', '#000000')
    cls.root.setvar('bg_color', '#ffffff')

  def create_widgets(cls):
    cls.mk_menu()
    cls.mk_frames(cfgs.frame_cfgs)
    cls.mk_subframes(cfgs.subframe_cfgs)
    cls.mk_canvases(cfgs.canvas_cfgs)
    cls.mk_treeview(cfgs.treeview_cfg)
    cls.mk_scrollbars(cfgs.scrollbar_cfgs)
    cls.mk_hex_txt(cfgs.txt_cfgs)
    cls.mk_tool_btns(cfgs.tool_btn_cfgs)
    cls.mk_treeview_btns(cfgs.treeview_btn_cfgs)
    cls.mk_lbl_frames(cfgs.lbl_frame_cfgs)
    cls.mk_lbls(cfgs.lbl_txt_cfgs, cfgs.lbl_var_cfgs)

  def setup_widgets(cls):
    draw_canvas = cls.root.nametowidget('.nge.draw_frame.draw_canvas')
    gui.draw_grid_setup(draw_canvas)
    
    sheet_canvas = cls.root.nametowidget('.nge.sheet_frame.sheet_canvas')
    gui.sheet_grid_setup(sheet_canvas)
    
    hex_txt = cls.root.nametowidget('.nge.hex_frame.hex_txt')
    gui.hex_txt_setup(hex_txt)

    col_palette = cls.root.nametowidget('.nge.draw_frame.draw_btn_frame.col_palette')
    gui.col_palette_setup(col_palette)

    treeview = cls.root.nametowidget('.nge.tree_frame.file_tree_view')
    treeview_scroll = cls.root.nametowidget('.nge.tree_frame.tree_scrollbar')
    gui.treeview_setup(treeview, treeview_scroll)

  def mk_menu(cls):
    window = cls.root.winfo_toplevel()
    menu = Menu()
    window.option_add('*tearOff', FALSE)
    window.config(menu=menu)
    file_menu = Menu(menu)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open...", command=cls.root.open_callback)
    file_menu.add_command(label="Save As...", command=cls.root.save_as_callback)
    file_menu.add_command(label="Quit")

  # Creating frames for different program areas
  def mk_frames(cls, canvas_cfgs: list):
    frame_iter = iter(canvas_cfgs)
    
    for frame_cfg in range(len(canvas_cfgs) // 2):
      cfg = next(frame_iter)
      grid_opts = next(frame_iter)
      
      gui.set_parent(cls.root, cfg)

      frame = Frame(**cfg)
      frame.grid_propagate(0)
      frame.grid(**grid_opts)

  # Creating subframes, which go inside of frames for
  # organization
  def mk_subframes(cls, subframe_cfgs):
    subframe_iter = iter(subframe_cfgs)
    
    for dict in range(len(subframe_cfgs) // 2):
      subframe_cfg = next(subframe_iter)
      subframe_grid_opts = next(subframe_iter)
      
      gui.set_parent(cls.root, subframe_cfg)

      frame = Frame(**subframe_cfg)
      frame.grid(**subframe_grid_opts)

  # Creating the sheet and draw canvases
  def mk_canvases(cls, canvas_cfgs):
    canvas_iter = iter(canvas_cfgs)

    for dict in range(len(canvas_cfgs) // 2):
      canvas_cfg = next(canvas_iter)
      canvas_grid_opts = next(canvas_iter)
      
      gui.set_parent(cls.root, canvas_cfg)

      canvas = Canvas(**canvas_cfg)

      if canvas_cfg["name"] == "draw_canvas":
        canvas.bind('<ButtonRelease-1>', cls.draw_canvas_callback)
        canvas.bind('<ButtonRelease-3>', cls.draw_canvas_callback)
      elif canvas_cfg["name"] == "col_palette":
        canvas.bind('<ButtonRelease-1>', cls.fg_callback)
        canvas.bind('<ButtonRelease-3>', cls.bg_callback)
      canvas.grid(**canvas_grid_opts)

  def mk_treeview(cls, treeview_cfg):
    treeview_iter = iter(treeview_cfg)
    for dict in range(len(treeview_cfg) // 2):
      treeview_cfg = next(treeview_iter)
      treeview_grid_opts = next(treeview_iter)
      
      gui.set_parent(cls.root, treeview_cfg)

      view = Treeview(**treeview_cfg)
      view.column("#0")
      view.grid(**treeview_grid_opts)

  def mk_treeview_btns(cls, treeview_btn_cfgs):
    btn_iter = iter(treeview_btn_cfgs)

    for dict in range(len(cfgs.treeview_btn_cfgs) // 2):
      btn_cfg = next(btn_iter)
      btn_grid_opts = next(btn_iter)
      if btn_cfg["name"] == "add_sh":
        btn_cfg["command"] = cls.add_sh
      elif btn_cfg["name"] == "rem_sh":
        btn_cfg["command"] = cls.rem_sh
      elif btn_cfg["name"] == "add_ch":
        btn_cfg["command"] = cls.add_ch
      else:
        btn_cfg["command"] = cls.rem_ch

      gui.set_parent(cls.root, btn_cfg)

      btn = Button(**btn_cfg)
      btn.grid(**btn_grid_opts)

  def mk_tool_btns(cls, tool_btn_cfgs):
    btn_iter = iter(tool_btn_cfgs)

    for dict in range(len(tool_btn_cfgs) // 2):
      btn_cfg = next(btn_iter)
      btn_grid_opts = next(btn_iter)

      gui.set_parent(cls.root, btn_cfg)

      #creating buttons
      btn = Button(**btn_cfg)
      btn.grid(**btn_grid_opts)

    cls.root.bind_class('tool_btn', '<ButtonRelease-1>', cls.tool_btn_callback)

  def mk_scrollbars(cls, scrollbar_cfgs):
    scroll_iter = iter(scrollbar_cfgs)
    
    for dict in range(len(scrollbar_cfgs) // 2):
      scroll_cfg = next(scroll_iter)
      scroll_grid_opts = next(scroll_iter)
      
      gui.set_parent(cls.root, scroll_cfg)

      if scroll_cfg["name"] == "hex_scrollbar":
        scroll_cfg["command"] = cls.scroll_hex_txt
      scroll = Scrollbar(**scroll_cfg)
      scroll.grid(**scroll_grid_opts)

  def mk_hex_txt(cls, txt_cfgs):
    txt_iter = iter(txt_cfgs)
    hex_scroll = cls.root.nametowidget('.nge.hex_frame.hex_scrollbar')
    for dict in range(len(txt_cfgs) // 2):
      txt_cfg = next(txt_iter)
      txt_grid_opts = next(txt_iter)
      
      gui.set_parent(cls.root, txt_cfg)

      txt_cfg["yscrollcommand"] = hex_scroll.set
      hex_txt = Text(**txt_cfg)
      hex_txt.grid(**txt_grid_opts)
      hex_txt.bind()

  def mk_lbl_frames(cls, lbl_frame_cfgs):
    lbl_iter = iter(lbl_frame_cfgs)
    for dict in range(len(lbl_frame_cfgs) // 2):
      lbl_cfg = next(lbl_iter)
      lbl_grid_opts = next(lbl_iter)

      gui.set_parent(cls.root, lbl_cfg)

      lbl = LabelFrame(**lbl_cfg)
      lbl.grid_propagate(0)
      lbl.grid(**lbl_grid_opts)


  def mk_lbls(cls, lbl_txt_cfgs, lbl_var_cfgs):
    cfg_lists = [lbl_txt_cfgs, lbl_var_cfgs]
    for cfg_list in cfg_lists:
      lbl_iter = iter(cfg_list)
      for dict in range(len(cfg_list) // 2):
        lbl_cfg = next(lbl_iter)
        lbl_grid_opts = next(lbl_iter)

        gui.set_parent(cls.root, lbl_cfg)

        lbl = Label(**lbl_cfg)

        lbl.grid(**lbl_grid_opts)


  def scroll_hex_txt(cls, *args):
    hex_scroll = cls.root.nametowidget('.nge.hex_frame.hex_scrollbar')
    hex_scroll.set(*args)

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