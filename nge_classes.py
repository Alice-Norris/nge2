from tkinter import Toplevel, PhotoImage
from tkinter.ttk import Label, Entry, Button, Treeview, Scrollbar

class Character:
  id = None
  name = None
  data = None
  def __init__(cls, id: int, name:str="unnamed"):
    cls.data = [0] * 64
    cls.id = id
    cls.name = name
  
  def __str__(cls):
    char_str = str(cls.id) + '*' + cls.name + '*'
    for index, pixel in enumerate(cls.data):
      if index + 1 < len(cls.data):
        char_str += str(pixel) + ','
      else:
        char_str += str(pixel)
    return char_str

class Sheet:
  char_list = None
  id = None
  name = None
  def __init__(cls, id: int, name:str="unnamed"):
    cls.name = name
    cls.id = id
    cls.char_list = []
    cls.char_list.append(Character(len(cls.char_list)))

  def __getitem__(cls, key):
    if isinstance(key, int):
      return cls.char_list[key]

  def add_char(cls, name:str="unnamed", id:int=None):
    if id == None:
      id = len(cls.char_list)
    new_char = Character(id, name)
    cls.char_list.append(new_char)
    return new_char
  
  def rem_char(cls, id: int):
    for char in cls.char_list:
      if char.id == id:
        cls.char_list.pop(char)

  def char_by_id(cls, id:int):
    for char in cls.char_list:
      if char.id == id:
        return char
    return None

class Book:
  sheets = None
  def __init__ (cls, name:str="unnamed"):
      cls.name = name
      cls.sheets = []
      print("lmao")
  
  def __getitem__(cls, key):
    if isinstance(key, int):
      return cls.sheets[key]

  def add_sheet(cls, name:str="unnamed"):
    id = len(cls.sheets)
    new_sheet = Sheet(id, name)
    cls.sheets.append(new_sheet)
    return new_sheet

  def rem_sheet(cls, sh_id):
    cls.sheets.pop(sh_id)

  def sheet_by_id(cls, id:int):
    for sheet in cls.sheets:
      if sheet.id == id:
        return sheet
    return None

class AddDialog:
  def __init__(cls, parent, name: str=None):
    cls.root = Toplevel(parent, name=name)
    cls.user_input = None
    cls.prompt = Label(cls.root, name='prompt')
    cls.entry = Entry(cls.root, width=8)
    cls.valid_label = Label(cls.root, name='validation_fail', foreground='#ff0000')
    cls.ok_btn = Button(cls.root, text='ok')
    cls.cancel_btn = Button(cls.root, text='cancel', command=cls.cancel)
    cls.grid()
    cls.entry.focus_set()

  def grid(cls):
    cls.prompt.grid(row=0, column=0)
    cls.entry.grid(row=0, column=1)
    cls.valid_label.grid(row=1, column=0, columnspan=2)
    cls.ok_btn.grid(row=2, column=0)
    cls.cancel_btn.grid(row=2, column=1)
    cls.root.grid()

  def cancel(cls):
    cls.root.destroy()

class RemDialog:
  def __init__(cls, parent, name: str=None):
    cls.root = Toplevel(master=parent, name=name)
    cls.user_input = None
    cls.parent = parent
    cls.prompt = Label(cls.root, name='prompt')
    cls.treeview = Treeview(cls.root)
    cls.tree_scroll = Scrollbar(cls.root)
    cls.ok_btn = Button(cls.root, text='ok')
    cls.cancel_btn = Button(cls.root, text='cancel', command=cls.cancel)
    cls.grid()

  def grid(cls):
    cls.prompt.grid(row=0, column=0)
    cls.treeview.grid(row=1, column=0)
    cls.tree_scroll.grid(row=1, column=1, sticky='nsw')
    cls.ok_btn.grid(row=2, column=0)
    cls.cancel_btn.grid(row=2, column=1)
    cls.root.grid()

  def cancel(cls):
    cls.root.destroy()

class AddSheetDialog(AddDialog):
  def __init__(cls, parent):
    super().__init__(parent, 'add_sh_dialog')
    cls.sh_id = parent.getvar('sheet_id_var')
    cls.book = parent.book
    cls.sheet_names = [sheet.name for sheet in cls.book.sheets]
    cls.root.title='Add Sheet'
    cls.name_valid = False
    cls.prompt.configure(text='New Sheet Name\n(8 characters max):')
    valid_callback = (cls.entry.register(cls.sheet_name_valid), '%d', '%P', '%S')
    cls.ok_btn.configure(command=cls.ok)
    cls.entry.configure(validatecommand=valid_callback, validate='key')
    cls.entry.bind('<Key-Return>', cls.ok)

  def ok(cls, *args):
    if cls.name_valid:
      user_input = cls.entry.get()
      sheet = cls.book.add_sheet(user_input)
      cls.root.master.children["tree_frame"].event_generate('<<Sheet-Add>>', state=sheet.id)
      cls.root.destroy()


  def sheet_name_valid(cls, action: int, result: str='', new_input: str=''):
    cls.name_valid = False
    if len(result) == 0 and action != 1:
      cls.valid_label.configure(text='Name cannot be empty!')
      return True
    if len(result) > 8 and action != 0:
      cls.valid_label.configure(text='Name too long!')
      return False
    elif result in cls.sheet_names:
      cls.valid_label.configure(text='Sheet already exists!')
      return True
    else:
      cls.name_valid = True
      cls.valid_label.configure(text='')
      return True

class RemSheetDialog(RemDialog):
  def __init__(cls, parent):
    super().__init__(parent, 'rem_sh_dialog')
    cls.book = parent.book
    cls.root.title = 'Remove Sheet'
    cls.prompt.configure(text='Select sheet to remove:')
    cls.treeview.configure(selectmode='browse', style='nge.fileview')
    for sheet in cls.parent.active_book.sheets:
      cls.treeview.insert('', 'end', iid='sh'+str(sheet.id), text=sheet.name, image=cls.parent.images["sheet"])
    cls.ok_btn.configure(command=cls.ok)

  def ok(cls, *args):
    sel = cls.treeview.selection()
    if len(sel) != 0:
      sh_id = int(sel[0][2:])
      cls.librarian.rem_sheet(sh_id)
    cls.root.master.children["tree_frame"].event_generate('<<Sheet-Rem>>')
    cls.root.destroy()


class AddCharDialog(AddDialog):
  def __init__(cls, parent, char_num: int=None):
    super().__init__(parent, 'add_ch_dialog')
    cls.sh_id = parent.getvar('sheet_id_var')
    cls.book = parent.book
    cls.char_names = [char.name for char in cls.book[cls.sh_id].char_list]
    cls.id = char_num
    cls.root.title='Add Character'
    cls.name_valid = False
    cls._after_id = None
    cls.prompt.configure(text='New Character Name\n(8 characters max):')
    valid_callback = (cls.entry.register(cls.char_name_valid), '%d', '%P', '%S')
    cls.ok_btn.configure(command=cls.ok)
    cls.entry.configure(validatecommand=valid_callback, validate='key')
    cls.entry.bind('<Key-Return>', cls.ok)

  def ok(cls, *args):
    if cls.name_valid:
      user_input = cls.entry.get()
      new_char = cls.book[cls.sh_id].add_char(user_input, cls.id)
      cls.root.master.children["tree_frame"].event_generate('<<Char-Add>>')
      cls.root.master.children["sheet_frame"].event_generate('<<Char-Add>>', state=new_char.id, data='add')
      cls.root.master.children["hex_frame"].event_generate('<<Char-Add>>', state=new_char.id)
      cls.root.destroy()


  def char_name_valid(cls, action: int, result: str='', new_input: str=''):
    cls.name_valid = False
    if len(result) == 0 and action != 1:
      cls.valid_label.configure(text='Name cannot be empty!')
      return True
    if len(result) > 8 and action != 0:
      cls.valid_label.configure(text='Name too long!')
      return False
    elif result in cls.char_names:
      cls.valid_label.configure(text='Character already exists!')
      return True
    else:
      cls.name_valid = True
      cls.valid_label.configure(text='')
      return True

class RemCharDialog(RemDialog):
  def __init__(cls, parent):
    cls.sh_id = parent.getvar('sheet_id_var')
    super().__init__(parent, 'rem_ch_dialog')
    cls.book=parent.book
    cls.root.title = 'Remove Character'
    cls.prompt.configure(text='Select character to remove:')
    cls.treeview.configure(selectmode='browse', style='nge.fileview')
    sheet = cls.parent.book.sheet_by_id(cls.sh_id)
    for char in sheet.char_list:
      cls.treeview.insert('', 'end', iid='ch'+str(char.id), text=char.name, image=cls.parent.images["character"])
    cls.ok_btn.configure(command=cls.ok)

  def ok(cls, *args):
    sel = cls.treeview.selection()
    if len(sel) != 0:
      ch_id = int(sel[0][2:])
      cls.book[cls.sh_id].rem_char(ch_id)
      cls.root.master.children["tree_frame"].event_generate('<<Char-Rem>>')
      cls.root.master.children["sheet_frame"].event_generate('<<Char-Rem>>', state=ch_id, data='rem')
      cls.root.master.children["hex_frame"].event_generate('<<Char-Rem>>', state=ch_id)
      cls.root.destroy()
