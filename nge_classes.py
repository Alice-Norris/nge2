class Character:
  id = None
  name = None
  data = None
  def __init__(cls, id: int, name:str="unnamed"):
    cls.data = [0] * 64
    cls.id = id
    cls.name = name

class Sheet:
  char_list = None
  id = None
  name = None
  def __init__(cls, id: int, name:str="unnamed"):
    cls.name = name
    cls.id = id
    cls.char_list = []
    while len(cls.char_list) < 128:
      char_id = len(cls.char_list)
      cls.char_list.append(Character(char_id))

  def __getitem__(cls, key):
    if isinstance(key, int):
      return cls.char_list[key]

  def add_char(cls, name:str="unnamed"):
    id = len(cls.char_list)
    cls.char_list.append(Character(id, name))

class Book:
  sheets = None
  def __init__ (cls, name:str="unnamed"):
      cls.name = name
      cls.sheets = []
      print("lmao")
  
  def add_sheet(cls, name:str="unnamed"):
    id = len(cls.sheets)
    cls.sheets.append(Sheet(id, name))