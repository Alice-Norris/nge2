from tkinter.ttk import Frame, Button
from tkinter import Canvas, NW, PhotoImage
from nge_logic import dat_to_col_dict, create_img_data
from nge_widget_configs import sheet_canvas_cfg
from nge_classes import AddCharDialog, Book

class SheetFrame(Frame):
  sheet_canv = None
  curr_sel = None
  images = {}

  def __init__(cls, parent, sh_var, ch_var):
    Frame.__init__(cls, parent, **{ "name" : "sheet_frame", "class_" : "Frame", "height" : 400, "width"  : 792, "borderwidth" : 2, "relief" : "groove"})
    cls.grid(**{ "sticky" : "NESW", "columnspan" : 2, "column" : 1, "row" : 1 })
    cls.root = cls.winfo_toplevel()
    cls.book = parent.book
    ch_var.trace_add('write', cls.update_sheet_sel)
    sh_var.trace_add('write', cls.update_sheet)
    cls.mk_widgets()
    cls.sheet_grid_setup()
    char_mod_call = cls.register(cls.update_char_img)
    cls.tk.call('bind', cls, '<<Char-Data-Mod>>', char_mod_call)
    mod_ch_call = cls.register(cls.mod_char)
    cls.tk.call('bind', cls, '<<Char-Add>>', mod_ch_call + ' %s %d')
    cls.tk.call('bind', cls, '<<Char-Rem>>', mod_ch_call + ' %s %d')
    upd_sel_call = cls.register(cls.update_sheet_sel)
    cls.tk.call('bind', cls, '<<Char-Change>>', upd_sel_call)
  
  def mk_widgets(cls):
    sheet_cfg = sheet_canvas_cfg[0]
    sheet_grid = sheet_canvas_cfg[1]

    sheet_cfg["master"] = cls
    cls.sheet_canv = Canvas(**sheet_cfg)
    cls.sheet_canv.grid(**sheet_grid)
    
  def create_sheet_imgs(cls):
    for char in cls.book[0].char_list:
      img_data = create_img_data(char.data)
      img_name = "i" + str(char.id)
      cls.images[img_name] = PhotoImage(master=cls, data=img_data, format="PPM")
    img_list = cls.images.keys()
    for x in range(128):
      img_name = "i" + str(x)
      if img_name not in img_list:
        img_data = create_img_data([0]*64)
        cls.images[img_name] = PhotoImage(master=cls, data=img_data, format="PPM")

  def sheet_grid_setup(cls):
    cls.create_sheet_imgs()
    img_grids = []
    sh_id = cls.getvar('sheet_id_var')
    for char in cls.book.sheets[sh_id].char_list:
      img_grids.append(char.id)
    for grid in range(128):
      (y, x) = divmod(grid, 16)
      start_x = x * 49 + 2
      start_y = y * 49 + 2      
      if grid in img_grids:
        img_name = 'i' + str(grid)
        img = cls.images[img_name]
        cls.sheet_canv.create_image(start_x+1, start_y+1, image=img, tag=img_name, anchor=NW)
        cls.sheet_canv.tag_bind(img_name, '<ButtonRelease-1>', cls.sheet_click)
      else:
        r_tag = 'r' + str(grid)
        cls.sheet_canv.create_rectangle(start_x, start_y, start_x+49, start_y+49, fill='#ffffff', tag=r_tag, stipple='gray50')
        cls.sheet_canv.tag_bind(r_tag, '<Double-ButtonRelease-1>', cls.sheet_dbl_click)
    cls.sheet_canv.create_rectangle(2, 2, 51, 51, outline='#ff0000', tag='select_rect', width=2)
    cls.sheet_canv.tag_raise('select_rect')
    cls.curr_sel = 0

  def sheet_click(cls, event):
    ch_num = int(cls.sheet_canv.gettags('current')[0][1:])
    cls.setvar('char_id_var', ch_num)

  def sheet_dbl_click(cls, event):
    obj_tag = event.widget.itemconfig('current', 'tags')[-1].split(' ')[0]
    char_num = int(obj_tag[1:])
    AddCharDialog(event.widget.nametowidget('.nge'), char_num)

  def update_sheet_sel(cls, *args):
    ch_id = cls.getvar('char_id_var')
    old_coords = cls.sheet_canv.coords('select_rect')
    new_coords = cls.sheet_canv.coords('i'+str(ch_id))
    diff_x = new_coords[0] - old_coords[0]
    diff_y = new_coords[1] - old_coords[1]
    cls.sheet_canv.move('select_rect', diff_x, diff_y)
    cls.sheet_canv.tag_raise('select_rect', cls.sheet_canv.find_all()[-1])
  
  def update_char_img(cls):
    sh_id = cls.getvar('sheet_id_var')
    ch_id = cls.getvar('char_id_var')
    char_data = cls.book[sh_id].char_by_id(ch_id).data
    img_data = create_img_data(char_data)
    cls.images["i" + str(ch_id)].configure(data=img_data)

  def update_sheet(cls, *args):
    cls.sheet_canv.delete(cls.sheet_canv.find_all())
    cls.sheet_grid_setup()

  def mod_char(cls, mod_id, action):
    r_tag = 'r' + mod_id
    i_tag = 'i' + mod_id
    if action == 'add':
      coords = cls.sheet_canv.coords(r_tag)
      cls.sheet_canv.delete(r_tag)
      img = cls.images[i_tag]
      cls.sheet_canv.create_image(coords[0]+1, coords[1]+1, image=img, tag=i_tag, anchor=NW)
      cls.sheet_canv.tag_bind(i_tag, '<ButtonRelease-1>', cls.sheet_click)
    if action =='rem':
      coords = cls.sheet_canv.coords('i' + mod_id)
      cls.sheet_canv.delete('i'+mod_id)
      cls.sheet_canv.create_rectangle(coords[0]-1, coords[1]-1, coords[0]+49, coords[1]+49, fill='#ffffff', tag=r_tag, stipple='gray50')
      cls.sheet_canv.tag_bind(r_tag, '<Double-ButtonRelease-1>', cls.sheet_dbl_click)