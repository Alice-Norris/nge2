from tkinter.ttk import Frame, Button
from tkinter import Canvas, StringVar, IntVar
from nge_logic import dat_to_col_dict
from nge_logic import col_to_dat_dict
from nge_widget_configs import draw_frame_cfgs
from nge_classes import Book
from math import ceil, sqrt
class DrawFrame(Frame):
  draw_canv = None
  fg_canv = None
  bg_canv = None
  col_pal = None
  def __init__(cls, parent, sh_var, ch_var):
    Frame.__init__(cls, parent, **{"name" : "draw_frame", "class_" : "Frame", "height" : 400, "width"  : 440, "borderwidth" : 2, "relief" : "groove"})
    cls.root = cls.winfo_toplevel()
    cls.book = parent.book
    ch_var.trace_add('write', cls.update_draw_canvas)
    cls.start_x = IntVar(master = cls, name = 'start_x', value = None)
    cls.start_y = IntVar(master = cls, name = 'start_y', value = None)
    cls.active_tool = StringVar(master=cls.root, name = "active_tool", value=None)
    cls.fg_col = StringVar(master=cls.root, name="fg_col", value='#000000')
    cls.bg_col = StringVar(master=cls.root, name="bg_col", value='#ffffff')
    cls.grid(**{ "sticky" : "NESW", "column" : 0, "row" : 1 })
    cfg_iter = iter(draw_frame_cfgs.items())
    while (cfg := next(cfg_iter, None)) is not None:
      constr = None
      opts = cfg[1]
      if cfg[0] == "frame":
        constr = Frame
      elif cfg[0] == "canvas":
        constr = Canvas
      elif cfg[0] == "btn":
        constr = Button
      
      opt_iter = iter(opts)
      while (opt := next(opt_iter, None)) is not None:
        opt[0]["master"] = cls
        widget = constr(**opt[0])
        if opt[0]["name"] == 'draw_canvas':
          cls.draw_canv = widget
        if opt[0]["name"] == 'fg_color':
          cls.fg_canv = widget
        if opt[0]["name"] == 'bg_color':
          cls.bg_canv = widget
        if opt[0]["name"] == 'col_palette':
          cls.col_pal = widget

        widget.grid(**opt[1])
    
    cls.draw_grid_setup()
    cls.col_palette_setup()
    cls.bind_class('tool_btn', '<ButtonRelease-1>', cls.chg_tool)

  def draw_grid_setup(cls):
    for y in range(8):
      for x in range(8):
        x_coord = x * 49 + 3
        y_coord = y * 49 + 3
        rect_name = 'rect' + str(x+y*8)
        cls.draw_canv.create_rectangle(x_coord, y_coord, x_coord+47, y_coord+47, tag=rect_name, outline="#ffffff", fill="#ffffff")
        cls.draw_canv.tag_bind(rect_name, '<Enter>', cls.draw_canvas_tool_click, add='+')
        cls.draw_canv.tag_bind(rect_name, '<Motion>', cls.draw_canvas_tool_click, add='+')
        cls.draw_canv.tag_bind(rect_name, '<B1-Motion>', cls.draw_canvas_tool_click, add='+')
        cls.draw_canv.tag_bind(rect_name, '<B3-Motion>', cls.draw_canvas_tool_click, add='+')
        cls.draw_canv.tag_bind(rect_name, '<ButtonRelease-1>', cls.draw_canvas_tool_click, add='+')
        cls.draw_canv.tag_bind(rect_name, '<ButtonRelease-3>', cls.draw_canvas_tool_click, add='+')
        cls.draw_canv.tag_bind(rect_name, '<Button-1>', cls.draw_canvas_tool_click, add='+')
        cls.draw_canv.tag_bind(rect_name, '<Button-3>', cls.draw_canvas_tool_click, add='+')

  def col_palette_setup(cls):
    cls.col_pal.create_rectangle(2, 2, 38, 38, outline="#000000", fill="#ffffff", tag='col_btn')
    cls.col_pal.create_rectangle(2, 38, 38, 76, outline="#000000", fill="#aaaaaa", tag='col_btn')
    cls.col_pal.create_rectangle(2, 75, 38, 113, outline="#000000", fill="#555555", tag='col_btn')
    cls.col_pal.create_rectangle(2, 112, 38, 150, outline="#000000", fill="#000000", tag='col_btn')
    chg_col_call = cls.col_pal.register(cls.chg_col)
    cls.col_pal.tag_bind('col_btn', '<ButtonRelease-1>', cls.chg_col)
    cls.col_pal.tag_bind('col_btn', '<ButtonRelease-3>', cls.chg_col)

  def chg_tool(cls, event):
    old_tool_str = cls.active_tool.get()
    new_tool_str = event.widget._name[:-4]
    if old_tool_str != '':
      old_btn = cls.nametowidget('.nge.draw_frame.' + old_tool_str + '_btn')
      old_btn.configure(style='nge.tool_btn')
    if old_tool_str != new_tool_str:
      cls.active_tool.set(new_tool_str)
      new_btn = cls.nametowidget('.nge.draw_frame.' + new_tool_str + '_btn')
      new_btn.configure(style='nge.sel_tool_btn')
      src_img = "@./" + new_tool_str + "_cur.xbm"
      mask_img = new_tool_str + "_cur-mask.xbm"
      cls.draw_canv.configure(cursor=(src_img, mask_img, '#44ccaa', '#44ccaa'))

  def chg_col(cls, event):
    col_palette = event.widget
    col = col_palette.itemcget('current', 'fill')
    col_canv = None
    
    if event.num == 1 and cls.getvar('fg_col') != col:
      cls.setvar('fg_col', col)
      col_canv = cls.fg_canv
    elif event.num == 3 and cls.getvar('bg_col') != col:
      cls.setvar('bg_col', col)
      col_canv = cls.bg_canv
    
    if col_canv != None:
      col_canv.configure(background=col)

  def update_draw_canvas(cls, *args):
    sh_id = cls.getvar('sheet_id_var')
    ch_id = cls.getvar('char_id_var')
    char_data = cls.book[sh_id].char_by_id(ch_id).data
    for index, obj_id in enumerate(cls.draw_canv.find_all()):
      col = dat_to_col_dict[char_data[index]]
      cls.draw_canv.itemconfig(obj_id, fill=col, outline=col)
  
  def draw_canvas_tool_click(cls, event):
    obj = cls.draw_canv.find_closest(event.x, event.y)
    tool = cls.getvar('active_tool')
    m1 = False
    m2 = False
    if event.state & 0x0100 > 0:
      m1 = True
    elif event.state & 0x0400 > 0:
      m2 = True
    if tool == 'pencil' and (m1 or m2):
      cls.pencil_click(obj, m1, m2)
    elif tool == 'eraser' and (m1 or m2 ):
      cls.eraser_click(obj)
    elif tool == 'line' and ((event.type in ['4', '5'] and event.num in [1, 3]) or (event.type == '6' and (m1 or m2))):
      cls.line_click(obj, event)
    elif tool == 'bucket':
      cls.bucket_click(obj, m1, m2)
    else:
      return
    cls.update_char({'mute' : False})

  # Called when the pencil tool is active and the draw canvas is clicked
  def pencil_click(cls, obj, mouse1, mouse2):
    if mouse1 == True:
      color = cls.getvar('fg_col')
      cls.draw_canv.itemconfigure(obj, fill=color, outline=color)
    elif mouse2 == True:
      color = cls.getvar('bg_col')
      cls.draw_canv.itemconfigure(obj, fill=color, outline=color)
    
  # As above, for eraser
  def eraser_click(cls, obj):#canvas: Canvas, x: int, y: int):
    cls.draw_canv.itemconfigure(obj, fill='#ffffff', outline='#ffffff')

  # As above, for line tool
  def line_click(cls, obj, event):#canvas: Canvas, color: str, x: int, y: int):
    if event.type == '4' and (event.num == 1 or event.num == 3):
      cls.setvar('start_x', event.x)
      cls.setvar('start_y', event.y)
    elif event.type == '6' and (event.state % 0x0100 > 0 or event.state % 0x0400 > 0):
      cls.draw_canv.delete('ind_line')
      cls.draw_canv.create_line(cls.getvar('start_x'), cls.getvar('start_y'), event.x, event.y, fill='#44ccaa', tag='ind_line', width=3)
    elif event.type == '5' and event.num in [1, 3]:
      grid_ids = []
      known_bad = []
      coords = cls.draw_canv.coords('ind_line')
      #start grid
      grid_ids.append(int(coords[0] // 50 + (coords[1] // 50) * 8))
      start_center = ((grid_ids[0] % 8) * 49) + 26, ((grid_ids[0] // 8) * 49) + 26
      print('lmao')
      #end grid
      grid_ids.append(int(coords[2] // 50 + (coords[3] // 50) * 8))
      end_center = ((grid_ids[-1] % 8) * 49) + 26, ((grid_ids[-1] // 8) * 49) + 26
      lin_dist = sqrt(((end_center[0] - start_center[0]) ** 2) + ((end_center[1] - start_center[1]) ** 2))
      curr_grid = grid_ids[0]
      
      while curr_grid != grid_ids[-1]:
        
        new_neighbors = []
        for x in [-9, -8, -7, -1, 1, 7, 8, 9]:
          neighbor = curr_grid + x
          if neighbor == grid_ids[-1]:
            new_neighbors.append(neighbor)
            break
          col_check = abs(curr_grid % 8 - neighbor % 8)
          row_check = abs(curr_grid // 8 - neighbor // 8)
          if not (col_check >  1 or row_check > 1) and neighbor in range(0, 63) and neighbor not in known_bad:  
            new_neighbors.append(curr_grid + x)
          elif neighbor not in known_bad:
            known_bad.append(neighbor)

        if grid_ids[-1] in new_neighbors:
          break

        shortest_dist = lin_dist
        best_candidate = None
        while len(new_neighbors) > 0:
          candidate = new_neighbors.pop(0)
          coords = cls.draw_canv.coords('rect' + str(candidate))
          center = ((candidate % 8) * 49) + 26, ((candidate // 8) * 49) + 26
          test_dist = sqrt(((end_center[0] - center[0]) ** 2) + ((end_center[1] - center[1]) ** 2))
          if test_dist < shortest_dist:
            shortest_dist = test_dist
            best_candidate = candidate
            print('lmao')
          elif candidate not in known_bad:
            known_bad.append(candidate)

        if best_candidate not in grid_ids:
          grid_ids.insert(-1, best_candidate)
        curr_grid = best_candidate
      
      for grid in grid_ids:
        col = None
        if event.num == 1:
          col = cls.getvar('fg_col')
        if event.num == 3:
          col = cls.getvar('bg_col')
        cls.draw_canv.itemconfig('rect' + str(grid), fill=col, outline=col)
      cls.draw_canv.delete('ind_line')

  def bucket_click(cls, obj, m1, m2):
    grid_ids = []
    known_bad = []
    start_grid = cls.draw_canv.find_withtag('current')[0]
    grid_ids.append(start_grid)
    target_col = cls.draw_canv.itemcget(cls.draw_canv.find_withtag(grid_ids[0]), 'fill')
    id_index = 0
    while True:
      new_neighbors = []
      for grid in grid_ids[id_index:]:
        if grid >= 9 and grid-8 not in known_bad:
          new_neighbors.append(grid-8)
        if grid % 8 != 0 and grid+1 not in known_bad:
          new_neighbors.append(grid+1)
        if grid <= 57 and grid+8 not in known_bad:
          new_neighbors.append(grid+8)
        if grid %8 != 1 and grid-1 not in known_bad:
          new_neighbors.append(grid-1)
        id_index += 1

      while len(new_neighbors) > 0:
        candidate = new_neighbors.pop(0)
        neighbor_fill = cls.draw_canv.itemcget(candidate, 'fill')
        if neighbor_fill == target_col and candidate not in grid_ids:
          grid_ids.append(candidate)
        else:
          known_bad.append(candidate)

      if id_index >= len(grid_ids):
        break
    
    for id in grid_ids:
      if m1:
        color = cls.getvar('fg_col')
        cls.draw_canv.itemconfig(id, fill = color, outline = color)
      if m2:
        color = cls.getvar('bg_col')
        cls.draw_canv.itemconfig(id, fill = color, outline = color)
  
  def update_char(cls, *args):
    sh_num = cls.getvar('sheet_id_var')
    ch_num = cls.getvar('char_id_var')
    char = cls.book.sheets[sh_num].char_by_id(ch_num)
    canv_pix = cls.draw_canv.find_all()
    for index, pixel in enumerate(char.data):
      fill_col = cls.draw_canv.itemcget(canv_pix[index], 'fill')
      char.data[index] = col_to_dat_dict[fill_col]
    cls.master.children["hex_frame"].event_generate('<<Char-Data-Mod>>')
    cls.master.children["sheet_frame"].event_generate('<<Char-Data-Mod>>')
