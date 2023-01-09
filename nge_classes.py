from tkinter import Toplevel
from tkinter.ttk import Label, Entry, Button

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

class Book:
  sheets = None
  def __init__ (cls, name:str="unnamed"):
      cls.name = name
      cls.sheets = []
      print("lmao")
  
  def add_sheet(cls, name:str="unnamed"):
    id = len(cls.sheets)
    new_sheet = Sheet(id, name)
    cls.sheets.append(new_sheet)
    return new_sheet

class AddDialog:
  def __init__(cls, parent, name: str=None):
    cls.root = Toplevel(master=parent, name=name)
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

class AddSheetDialog(AddDialog):
  def __init__(cls, parent):
    super().__init__(parent, 'add_sh_dialog')
    cls.parent=parent
    cls.librarian = parent.librarian
    cls.root.title='Add Sheet'
    cls.name_valid = False
    cls._after_id = None
    cls.prompt.configure(text='New Sheet Name\n(8 characters max):')
    valid_callback = (cls.entry.register(cls.sheet_name_valid), '%d', '%P', '%S')
    cls.ok_btn.configure(command=cls.ok)
    cls.entry.configure(validatecommand=valid_callback, validate='key')
    cls.entry.bind('<Key-Return>', cls.ok)

  def ok(cls, *args):
    if cls.name_valid:
      user_input = cls.entry.get()
      cls.librarian.add_sheet(user_input)
      new_sheet_id = cls.parent.active_book.sheets[-1].id
      cls.root.destroy()
      cls.parent.event_generate('<<Sheet-Add>>', state=new_sheet_id)

  def sheet_name_valid(cls, action: int, result: str='', new_input: str=''):
    cls.name_valid = False
    if len(result) == 0 and action != 1:
      cls.valid_label.configure(text='Name cannot be empty!')
      return True
    if len(result) > 8 and action != 0:
      cls.valid_label.configure(text='Name too long!')
      return False
    elif result in cls.librarian.sheet_name_list():
      cls.valid_label.configure(text='Sheet already exists!')
      return True
    else:
      cls.name_valid = True
      cls.valid_label.configure(text='')
      return True

class RemSheetDialog:
  def __init__(cls, librarian):
    cls.root = Toplevel()

class AddCharDialog(AddDialog):
  def __init__(cls, parent, char_num: int=None):
    super().__init__(parent, 'add_ch_dialog')
    cls.parent = parent
    cls.librarian = parent.librarian
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
      new_char = cls.librarian.add_char(user_input, cls.id)
      new_char_str = str(new_char)
      cmd_str = 'set charstr "' + new_char_str + '"'
      cls.entry.tk.eval(cmd_str)
      cls.root.destroy()
      cls.parent.event_generate('<<Char-Add>>', data=new_char)

  def char_name_valid(cls, action: int, result: str='', new_input: str=''):
    cls.name_valid = False
    if len(result) == 0 and action != 1:
      cls.valid_label.configure(text='Name cannot be empty!')
      return True
    if len(result) > 8 and action != 0:
      cls.valid_label.configure(text='Name too long!')
      return False
    elif result in cls.librarian.char_name_list():
      cls.valid_label.configure(text='Character already exists!')
      return True
    else:
      cls.name_valid = True
      cls.valid_label.configure(text='')
      return True

class RemCharDialog:
  def __init__(cls, librarian):
    cls.root=Toplevel()