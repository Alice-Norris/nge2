from nge_interface import userInterface
from tkinter import IntVar, StringVar, BooleanVar, filedialog
from tkinter.ttk import Frame
from nge_librarian import Librarian
from enum import Enum
from nge_logic import load_imgs, col_to_dat_dict
import nge_gui_logic as gui
from nge_classes import Character
class FileType(Enum):
  GB = 1
  CGB = 2

class NGE(Frame):
  current_file = b'\x01unnamed\x01unnamed \x19\x00\x17\x04'
  interface = None
  librarian = None
  program = None
  prev_sheet = None
  prev_char = None

  def __init__(cls, master=None):
    Frame.__init__(cls, name="nge")
    cls.grid()
    cls.root = cls.winfo_toplevel()
    gui.set_style(cls.root)
    cls.librarian = Librarian()
    cls.active_book = cls.librarian.borrow()
    cls.active_sheet = IntVar(master = cls.root, name="active_sheet", value=0)
    cls.active_char = IntVar(master = cls.root, name="active_char", value=0)
    cls.set_txt_vars()
    cls.fg_col = StringVar(master = cls.root, name="fg_color", value='None')
    cls.bg_col = StringVar(master=cls.root, name="bg_color", value='None')
    cls.active_tool = StringVar(master=cls.root, name = "active_tool", value=None)
    cls.char_edited = BooleanVar(master=cls.root, name = "char_edited", value=False)
    cls.char_exists = BooleanVar(master=cls.root, name='char_exists', value=False)
    cls.images = load_imgs(cls.root, cls.active_book, cls.active_sheet.get())
    cls.interface = userInterface(cls, cls.active_book)
    
    cls.update_widgets = {
      'draw_canvas' : cls.root.nametowidget('nge.draw_frame.draw_canvas'),
      'sheet_canvas' : cls.root.nametowidget('nge.sheet_frame.sheet_canvas'),
      'hex_txt' : cls.root.nametowidget('.nge.hex_frame.hex_txt'),
      'file_tree_view' : cls.root.nametowidget('.nge.tree_frame.file_tree_view')
    }

  # Called when char data changes due to drawing on
  # the draw canvas
  def char_data_chg(cls, event):
    draw_canvas = cls.update_widgets['draw_canvas']
    curr_sheet = cls.active_sheet.get()
    curr_char = cls.active_char.get()
    char_data = cls.active_book.sheets[curr_sheet].char_list[curr_char].data
    rects = [draw_canvas.find_all()]
    for index, rect in rects:
      pixel_val = col_to_dat_dict[draw_canvas.itemcget(rect, 'fill')]
      char_data[index] = pixel_val
    img = cls.images['img' + str(cls.active_char.get())]
    char_data = cls.get_char_data
    gui.update_after_draw(draw_canvas, cls.active_book, img)

  def char_chg(cls, event):
    sheet_num = cls.getvar('active_sheet')
    char_num = event.state
    active_char = cls.active_char.get()
    cls.char_id_var.set(char_num)
    sheet = cls.active_book.sheets[sheet_num]
    curr_char = None
    if active_char != char_num:
      cls.prev_char = active_char
      cls.active_char.set(char_num)
      if [char_num == char.id for char in sheet.char_list]:
        cls.char_exists.set(True)
        for char in sheet.char_list:
          if char.id == char_num:
            curr_char = char
        cls.char_name_var.set(curr_char.name)
        cls.char_id_var.set(curr_char.id)
        gui.update_draw_canvas(cls.update_widgets["draw_canvas"], curr_char.data)
      else:
        cls.char_exists.set(False)
        cls.setvar('char_name_var', 'N/A')
        cls.setvar('char_id_var', 'N/A')  
      
      gui.update_sheet_sel(cls.update_widgets['sheet_canvas'])
      gui.update_txt_sel(cls.update_widgets['hex_txt'])
      gui.update_tree_sel(cls.update_widgets['file_tree_view'])

  def sheet_chg(cls, event):
    sheet_num = event.state
    if cls.active_sheet.get() != sheet_num:
      cls.prev_sheet = cls.active_sheet.get()
      cls.active_sheet.set(sheet_num)
  
  def sheet_add(cls, event):
    pass

  def sheet_rem(cls, event):
    pass

  def char_add(cls, *args):
    result = cls.root.tk.getvar('charstr')
    char_info = result.split('*')
    img = cls.images['img' + str(char_info[0])]
    char_info[2] = [int(x) for x in char_info[2].split(',')]
    num_chars = len(cls.active_book.sheets[cls.getvar('active_sheet')].char_list)
    cls.setvar('num_char_var', num_chars)
    gui.tree_char_add(cls.update_widgets['file_tree_view'], char_info)
    gui.update_char_img(char_info[2], cls.images['img'+str(char_info[0])])
    gui.sheet_canv_add(cls.update_widgets['sheet_canvas'], char_info, img)

  def char_rem(cls, event):
    pass
  
  def tool_chg(cls, *args):
    if cls.active_tool != cls.tool_var.get():
      cls.active_tool = cls.tool_var.get()
    draw_canvas = cls.root.nametowidget('.nge.draw_frame.draw_canvas')
    prev_tool = cls.prev_tool
    if prev_tool != None:
      old_btn_path = '.nge.draw_frame.draw_btn_frame.'+prev_tool+'_btn'
      old_btn = cls.root.nametowidget(old_btn_path)
      old_btn.configure(style='nge.tool_btn')
    gui.chg_cursor(draw_canvas, cls.active_tool)

  def save_as_callback(cls):
    file_buff = filedialog.asksaveasfile(
      mode='wb',
      defaultextension=".nge",
      filetypes=[('NGE File', '*.nge')],
      title="Save as..."
    )
    cls.librarian.save(file_buff)

  def open_callback(cls):
    file_buff = filedialog.askopenfile(
      mode='rb',
      defaultextension=".nge",
      filetypes=[('NGE File', '*.nge')],
      title="Open File"
    )
    cls.librarian.load(file_buff)
    cls.active_book = cls.librarian.borrow()
    cls.update_txt_vars()
  
  def get_char_data(cls):
    sheet_num = cls.active_sheet.get()
    char_num = cls.active_char.get()
    char_list = cls.active_book.sheets[sheet_num].char_list
    if cls.root.getvar('char_exists'):
      return char_list[char_num].data
    else:
      return None

  def set_txt_vars(cls):
    char_num = cls.active_char.get()
    sheet_num = cls.active_sheet.get()
    sheet = cls.active_book.sheets[sheet_num]
    char = sheet.char_list[char_num]
    cls.book_name_var = StringVar(name='book_name_var', value=cls.active_book.name)
    cls.sheet_num_var = IntVar(name='sheet_num_var', value=len(cls.active_book.sheets))
    cls.sheet_name_var = StringVar(name='sheet_name_var', value=sheet.name)
    cls.sheet_id_var = IntVar(name='sheet_id_var', value=sheet.id)
    cls.num_char_var = IntVar(name='num_char_var', value=len(sheet.char_list))
    cls.char_name_var = StringVar(name='char_name_var', value=char.name)
    cls.char_id_var = IntVar(name='char_id_var', value=char.id)

nge = NGE()
nge.master.title('NGE')
nge.root.mainloop()
