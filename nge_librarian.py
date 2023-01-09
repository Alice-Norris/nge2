from nge_classes import Book, Sheet, Character
from nge_file_ops import read_file, write_file
from pathlib import Path
from copy import copy

####                    THE LIBRARIAN                    ####
# The Librarian is the class that manages all other objects #
# Only one should be created, and only one should be used   #
# Hands data to the user interface upon request.            #
#############################################################

class Librarian:
    __instance = None
    __current_book = None
    def __init__(cls):
        if Librarian.__instance != None:
            raise Exception("Only one librarian allowed. You've done something wrong.")
        else:
            Librarian.__instance = cls
            cls.__current_book = Book()
            cls.__current_book.add_sheet()
            cls.__current_sheet = cls.__current_book.sheets[0]

    # def save(cls, filepath: Path, filename: str):
    #   write_file(filepath, filename, cls.__current_book)

    # def load(cls, filepath: Path, filename: str):
    #   cls.__current_book = read_file(filepath, filename)

    def load(cls, file_buffer):
      cls.__current_book = copy(read_file(file_buffer))
      print("lmao")

    def save(cls, file_buffer, book: Book):
      write_file(file_buffer, book)

    def sheet_name_list(cls):
      sheet_list = []
      for sheet in cls.__current_book.sheets:
        sheet_list.append(sheet.name)
      return sheet_list

    def char_name_list(cls):
      name_list = []
      for char in cls.__current_sheet.char_list:
        name_list.append(char.name)
      return name_list

    def book_name(cls):
      return cls.__current_book.name

    def request_index(cls):
      book = cls.__current_book
      index = { book.name : {} }
      sheet_dict = index[book.name]
      for sheet in book.sheets:
        char_names = []
        for char in sheet.char_list:
          char_names.append(char.name)
        sheet_dict[sheet.name] = char_names
      return index

    def borrow(cls):
      return cls.__current_book
    
    def add_sheet(cls, sheet_name: str):
      new_sheet = cls.__current_book.add_sheet(sheet_name)
      return new_sheet
    
    def add_char(cls, char_name: str, id: int=None):
      new_char = cls.__current_sheet.add_char(char_name, id)
      return new_char