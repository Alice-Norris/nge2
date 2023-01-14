from tkinter.ttk import Scrollbar, Frame, Label
from tkinter import Text, CENTER
from nge_widget_configs import hex_scroll_cfg, hex_txt_cfg
from nge_classes import Book
from nge_logic import str_to_char

class HexFrame(Frame):
  hex_scroll = None
  hex_txt = None
  curr_sel = 0
  def __init__(cls, parent):
    Frame.__init__(cls, parent, **{"name" : "hex_frame", "class_" : "Frame", "borderwidth" : 2, "relief" : "groove"})
    cls.grid(**{"sticky" : "NSEW", "column" : 1, "row" : 2})
    cls.root = cls.winfo_toplevel()
    cls.book = parent.book
    
    cls.mk_widgets()

    cls.hex_txt_setup()
    upd_txt_call = cls.register(cls.update_hex_txt)
    cls.tk.call('bind', cls, '<<Char-Data-Mod>>', upd_txt_call)
    add_txt_call = cls.register(cls.add_hex_txt)
    cls.tk.call('bind', cls, '<<Char-Add>>', add_txt_call + ' %s')
    rem_txt_call = cls.register(cls.rem_hex_txt)
    cls.tk.call('bind', cls, '<<Char-Rem>>', rem_txt_call + ' %s')

  def mk_widgets(cls):
      hex_txt_cfg[0]["master"] = cls
      hex_scroll_cfg[0]["master"] = cls

      cls.hex_txt = Text(**hex_txt_cfg[0])
      cls.hex_txt.grid(**hex_txt_cfg[1])

      cls.hex_scroll = Scrollbar(**hex_scroll_cfg[0])
      cls.hex_scroll.grid(**hex_scroll_cfg[1])

      cls.hex_txt["yscrollcommand"] = cls.hex_scroll.set
      cls.hex_scroll["command"] = cls.hex_txt.yview

  def hex_txt_setup(cls):
    for x in range(128):
      lbl_index = str(x+1) + '.0'
      hdr = '0x' + str(format(x, '02x')).upper()+'|'
      hdr_name = "lbl" + str(x)
      char_label = Label(cls.hex_txt, text=hdr, style="nge.hex_lbl", name=hdr_name)
      cls.hex_txt.window_create(lbl_index, window=char_label, align=CENTER)
      if x < 127:
        cls.hex_txt.insert("end", '\n')
    for char in cls.book[0].char_list:
      txt_index = str(char.id+1) + '.4'
      txt_tag = 'char' + str(char.id)
      dat = cls.char_to_hex(char.data)
      cls.hex_txt.insert(txt_index, dat, txt_tag)
    cls.hex_txt.tag_config('char0', background='#cccccc')
    cls.hex_txt.children['lbl0'].configure(background = '#cccccc')

  def char_to_hex(cls, data):
    char_hex = ""
    for x in range(8):
      upperbyte = ""
      lowerbyte = ""
      row = data[x*8: x*8+8]
      for pixel in row:
        upperbyte += str(pixel % 2)
        lowerbyte += str(pixel // 2)
      upperbyte = int(upperbyte, base=2)
      lowerbyte = int(lowerbyte, base=2)
      char_hex += "{0:02x} {1:02x} ".format(upperbyte, lowerbyte).upper()
    return char_hex.strip()

  def reset_txt(cls):
    cls.hex_txt.delete('1.1', '127.54')

  def update_txt_sel(cls, *args):
    ch_id = cls.getvar('char_id_var')
    cls.hex_txt.tag_config('char' + str(cls.curr_sel), background='#ffffff')
    cls.hex_txt.children['lbl' + str(cls.curr_sel)].configure(background='#ffffff')
    cls.hex_txt.tag_config('char' + str(ch_id), background='#cccccc')
    cls.hex_txt.children['lbl' + str(ch_id)].configure(background='#cccccc')
    cls.curr_sel = ch_id

  def update_hex_txt(cls, *args):
    sh_id = cls.getvar('sheet_id_var')
    ch_id = cls.getvar('char_id_var')
    char_data = cls.book[sh_id].char_by_id(ch_id).data
    char_hex = cls.char_to_hex(char_data)
    index_line = str(ch_id+1)
    cls.hex_txt.delete(index_line + '.1', index_line+'.54')
    cls.hex_txt.insert(index_line +'.1', char_hex, ("char" + str(ch_id)))
  
  def add_hex_txt(cls, new_id):
    sh_id = cls.getvar('sheet_id_var')
    char = cls.book[sh_id].char_by_id(int(new_id))
    index = str(int(new_id)+1) + '.1'
    char_hex = cls.char_to_hex(char.data)
    cls.hex_txt.insert(index, char_hex, "char" + new_id)
  
  def rem_hex_txt(cls, event):
    line_index = str(event.state+1)
    cls.hex_txt.delete(line_index+'.1', line_index+'.54')

  def refresh_txt(cls, *args):
    sh_num = cls.getvar('sheet_id_var')
    sheet = cls.book[sh_num]
    for line_num in range(127):
      start_ind = str(line_num+1) + '.1'
      end_ind = str(line_num+1) + '.54'
      cls.hex_txt.delete(start_ind, end_ind)
      if sheet is not None:
        char = sheet.char_by_id(line_num)
        if char is not None:
          dat_txt = cls.char_to_hex(char.data)
          txt_tag = 'char' + str(line_num)
          cls.hex_txt.insert(start_ind, dat_txt, txt_tag)
