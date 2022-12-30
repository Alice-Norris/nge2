from tkinter.ttk import Frame, Button, Treeview, Scrollbar, Menubutton
from tkinter import Canvas, Text, Menu, HORIZONTAL, VERTICAL, Tk, RAISED, SUNKEN, FALSE, filedialog
from nge_widget_configs import frame_cfgs, subframe_cfgs, canvas_cfgs, view_cfg, btn_cfgs, scrollbar_cfgs, txt_cfgs, treeview_btn_cfgs
import gui_logic as GL
from nge_logic import NGE_Logic
####  ("@./erasercur2.xbm", "erasercur2mask.xbm", "#000000", "#FFFFFF")

class userInterface:
  # Each entry consists of a name as a key and the frame
  # as its value. str:frame_name : ttk.Frame:frame

  grid_opts = {}
  images = {}

  def __init__ (cls, root: Tk, logic: NGE_Logic):#, images: dict):
    cls.program = logic
    cls.root = root
    cls.root.title("Nintendo Graphics Editor")
    cls.mk_menus()
    cls.mk_frames()
    cls.mk_subframes()
    cls.mk_canvases()
    cls.mk_file_view()
    cls.mk_scrollbars()
    cls.mk_hex_txt()
    cls.mk_tool_btns()
    cls.mk_file_view_btns()

  def mk_menus(cls):
    window = cls.root.winfo_toplevel()
    menu = Menu(window)
    window.option_add('*tearOff', FALSE)
    window.config(menu=menu)
    file_menu = Menu(menu)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open...", command=cls.open_callback)
    file_menu.add_command(label="Save As...", command=cls.save_as_callback)
  # Creating frames for different program areas
  def mk_frames(cls):
    frame_iter = iter(frame_cfgs)

    for frame_cfg in range(len(frame_cfgs) // 2):
      cfg = next(frame_iter)
      grid_opts = next(frame_iter)

      cfg["master"] = cls.root
 
      frame = Frame(**cfg)
      frame.grid(**grid_opts)

  # Creating subframes, which go inside of frames for
  # organization
  def mk_subframes(cls):
    subframe_iter = iter(subframe_cfgs)
    
    for dict in range(len(subframe_cfgs) // 2):
      subframe_cfg = next(subframe_iter)
      subframe_grid_opts = next(subframe_iter)
      parent = cls.root.nametowidget(subframe_grid_opts["in_"])
      subframe_cfg["master"] = parent
      frame = Frame(**subframe_cfg)
      frame.grid(**subframe_grid_opts)

  # Creating the sheet and draw canvases
  def mk_canvases(cls):
    canvas_iter = iter(canvas_cfgs)

    for dict in range(len(canvas_cfgs) // 2):
      canvas_cfg = next(canvas_iter)
      canvas_grid_opts = next(canvas_iter)
      path = canvas_grid_opts["in_"]
      
      canvas_cfg["master"] = cls.root.nametowidget(path)

      canvas = Canvas(**canvas_cfg)
      canvas.grid(**canvas_grid_opts)

  def mk_file_view(cls):
    treeview_cfg = view_cfg[0]
    treeview_grid_opts = view_cfg[1]
    path = treeview_grid_opts["in_"]

    treeview_cfg["master"] = cls.root.nametowidget(path)
    
    view = Treeview(**treeview_cfg)
    view.column("#0")
    view.grid(**treeview_grid_opts)

    view.bind('<<TreeviewSelect>>', cls.file_view_sel_callback)

  
  def mk_file_view_btns(cls):
    btn_iter = iter(treeview_btn_cfgs)

    for dict in range(len(treeview_btn_cfgs) // 2):
      btn_cfg = next(btn_iter)
      btn_grid_opts = next(btn_iter)

      parent = cls.root.nametowidget(btn_grid_opts["in_"])
      btn_cfg["master"] = parent

      btn = Button(**btn_cfg)
      btn.grid(**btn_grid_opts)

  def mk_tool_btns(cls):
    btn_iter = iter(btn_cfgs)

    for dict in range(len(btn_cfgs) // 2):
      btn_cfg = next(btn_iter)
      btn_grid_opts = next(btn_iter)
      path = btn_grid_opts["in_"]

      btn_cfg["master"] = cls.root.nametowidget(path)

      #creating buttons
      btn = Button(**btn_cfg)
      btn.grid(**btn_grid_opts)
      
  def mk_scrollbars(cls):
    scroll_iter = iter(scrollbar_cfgs)
    
    for dict in range(len(scrollbar_cfgs) // 2):
      scroll_cfg = next(scroll_iter)
      scroll_grid_opts = next(scroll_iter)
      path =  scroll_grid_opts["in_"]

      scroll_cfg["master"] = cls.root.nametowidget(path)
 
      scroll = Scrollbar(**scroll_cfg)
      scroll.grid(**scroll_grid_opts)

  def mk_hex_txt(cls):
    txt_iter = iter(txt_cfgs)

    for dict in range(len(txt_cfgs) // 2):
      txt_cfg = next(txt_iter)
      txt_grid_opts = next(txt_iter)
      path = txt_grid_opts["in_"]

      txt_cfg["master"] = cls.root.nametowidget(path)
 
      hex_txt = Text(**txt_cfg)
      hex_txt.grid(**txt_grid_opts)

  # Handler Functions

  # change cursor when button clicked
  def tool_btn_callback(cls, event):
    old_btn = None
    if cls.program.active_tool is not None:
      old_btn = cls.root.nametowidget('.draw_frame.draw_btn_frame.' + cls.program.active_tool + '_btn')
      old_btn.configure(style='NGE.tool_btn')
    btn = event.widget
    btn.configure(style='NGE.sel_tool_btn')
    tool_str = btn._name[0:-4]
    draw_canvas = cls.root.nametowidget('draw_frame.draw_canvas')
    cls.program.active_tool = tool_str
    GL.chg_cursor(tool_str, draw_canvas)
    
    #canvas.configure(cursor=("@./erasercur2.xbm", "erasercur2mask.xbm", "#000000", "#FFFFFF"))

  def color_btn_callback(cls, event):
    if cls.program.active_color is not None:
      color_name = cls.program.active_color_name()
      old_btn = cls.root.nametowidget('.draw_frame.draw_btn_frame.' + color_name + '_btn')
      old_btn.configure(style='NGE.tool_btn')
    btn = event.widget
    btn.configure(style='NGE.sel_tool_btn')
    color_str = event.widget._name[0:-4]
    cls.program.active_color = GL.chg_color(color_str)

  def draw_canvas_callback(cls, event):
    tool = cls.program.active_tool
    color = cls.program.active_color
    pixels = GL.draw_canvas_tool_click(event, tool, color)
    sheet_canvas = cls.root.nametowidget(".sheet_frame.sheet_canvas")
    cls.program.update_char(pixels, sheet_canvas)

  def sheet_canvas_callback(cls, event):
    old_active_char = cls.program.active_char
    new_active_char = (event.x // 40) + (event.y // 40) * 16
    if old_active_char != new_active_char:
      cls.program.active_char = new_active_char
      char_data = cls.program.get_char_data()
      draw_canvas = cls.root.nametowidget('.draw_frame.draw_canvas')
      GL.update_draw_canvas(draw_canvas, char_data)
      GL.select_char(event.widget, old_active_char, new_active_char)

  def scroll_callback(cls, *args):
    hex_header_txt = cls.root.nametowidget('.hex_txt_header')
    hex_data_txt = cls.root.nametowidget('.hex_txt_data')
    GL.dbl_scroll(hex_header_txt, hex_data_txt, *args)

  def open_callback(cls):
    file_buff = filedialog.askopenfile(
      mode='rb',
      defaultextension=".nge",
      filetypes=[('NGE File', '*.nge')],
      title="Open File"
    )
    cls.program.open(file_buff)

  
  def save_as_callback(cls):
    file_buff = filedialog.asksaveasfile(
      mode='rb',
      defaultextension=".nge",
      filetypes=[('NGE File', '*.ngge')],
      title="Save as..."
    )
    cls.program.save_as(file_buff)

  def file_view_sel_callback(cls, event):
    treeview = event.widget
    item_id = treeview.selection()[0]
    cls.program.chg_sel(item_id)
    if item_id.find("ch") != -1:
      sheet_canvas = cls.root.nametowidget('.sheet_frame.sheet_canvas')
      ch_id = int(item_id[9:])
      GL.select_char(sheet_canvas, cls.program.active_char, ch_id)
      char_data = cls.program.get_char_data()
      draw_canvas = cls.root.nametowidget('.draw_frame.draw_canvas')
      GL.update_draw_canvas(draw_canvas, char_data)

    
  def add_sh_callback(cls):
    GL.add_sheet_dialog()