from nge_classes import Book

### Encoding for bytes conversions
utf8='utf-8'

### Read file
# def read_file(filepath: Path, filename: str):
def read_file(file_buffer):
  # Path to file
  # path = Path(filepath + filename + '.nge')

  # Checking if file exists
  # if not path.exists:
  #   print("invalid file!")
  #   raise(FileNotFoundError)
  
  #Open file in read binary mode
  # with open(path, mode='rb') as file:

    # Find file type, for future modesetting
    file_type = int.from_bytes(file_buffer.read(1), "big")
    
    # Reading book name from file
    book_name = file_buffer.read(8).decode(utf8).strip()

    # Creating new book
    book = Book(book_name)
    
    # Reading number of sheets from files
    num_sheets = int.from_bytes(file_buffer.read(1), "big")

    # List of sheet names, since all names are read at once.
    sheet_names = []

    # For each sheet...
    for x in range(num_sheets):
      # Read sheet name from file, strip whitespace, since all
      # Sheet names are eight characters long, padded with spaces.
      sheet_name = file_buffer.read(8).decode(utf8).strip()
      sheet_names.append(sheet_name)
    
    # Checking and clearing end of header byte
    if file_buffer.read(1) != b'\x19':
      print("Possibly corrupted file!")

    # For each sheet name, add sheet to book with that name
    for name in sheet_names:
      book.add_sheet(name)

    # For each sheet in the book...
    for sheet in book.sheets:
      # Read number of characters in sheet from file
      num_chars = int.from_bytes(file_buffer.read(1), "big")

      # Lists store char names(strings) and data (lists)
      char_name_list = []
      char_data_list = []
      
      # for each char that's supposed to exist...
      for x in range(num_chars):
        # read its name from the file, strip whitespace
        # and add to list of character names.
        char_name = file_buffer.read(8).decode(utf8).strip()
        char_name_list.append(char_name)

      # Until we have as much data as we're supposed to...
      while len(char_data_list) < num_chars:
        # Read 65 bytes. Character data terminated with \x94, 
        # which translates to 148
        char_bytes = file_buffer.read(65)

        # Convert to list
        char_data = list(char_bytes)
        
        # If the bytes don't end with the termination value,
        # Could be corrupted.
        if char_bytes[-1] != 148:
          print("Possibly corrupted file!")
        # add char data (without terminator) to list
        char_data_list.append(char_data[0:-1])

      # For each character we've found...
      for x in range(num_chars):
        # get the char from this sheet's list...
        char = sheet.char_list[x]
        # set the name and data!
        char.name = char_name_list[x]
        char.data = char_data_list[x]

      # Checking and clearing sheet terminator
      if file_buffer.read(1) != b'\x17':
        print("Possibly corrutped file!")

    # Checking and clearing file terminator
    if file_buffer.read(1) != b'\x04':
      print("Possibly corrupted file!")
    else: 
      return book
  
  # if old_book.name == new_book.name:
  #   print("Book Name Matches!")
  # else:
  #   print("!!!!! BAD MATCH ON BOOK NAME !!!!!")

  # for x in range(len(old_book.sheets)):
  #   if old_book.sheets[x].name.strip() == new_book.sheets[x].name:
  #     print("Sheet names match!")
  #   else:
  #     print("!!!!! BAD MATCH ON SHEET NAMES !!!!!")
    
  #   for y in range(len(old_book.sheets[x].char_list)):

  #     old_char_name = old_book.sheets[x].char_list[y].name.strip()
  #     new_char_name = new_book.sheets[x].char_list[y].name
  #     old_char_data = old_book.sheets[x].char_list[y].data
  #     new_char_data = new_book.sheets[x].char_list[y].data
  #     if old_char_name == new_char_name:
  #       print("Name matches!")
  #     else:
  #       print("!!!!! BAD MATCH ON CHAR NAME !!!!!")
      
  #     if old_char_data == new_char_data:
  #       print("Data matches!")
  #     else:
  #       print("!!!!! BAD MATCH ON DATA !!!!!")

### Write File
# def write_file(filepath: Path, filename: str, book: Book=None):
def write_file(file_buffer,  book: Book=None):
  # Holds a concatenated list of sheet names.
  sheet_name_bytes = b''
  # Holds file data
  file_data = b''

  # For each sheet...
  for sheet in book.sheets:
    # Pad sheet name to length eight...
    while len(sheet.name) < 8:
      sheet.name += (' ')
    
    # convert name to bytes equivalent...
    name_bytes = bytes(sheet.name, utf8)

    # add to sheet name list!
    sheet_name_bytes += name_bytes
    
    ### Removing all-zero characters from end of list
    ### (All-zero characters between others are saved)

    # Up to 128 times...
    for x in range(128):
      # Working from end of list...
      char = sheet.char_list[127-x]

      # If all entries are zero...
      if char.data.count(0) == 64:
        # ...remove from list
        sheet.char_list.pop(127-x)
      else:
        # ...or quit at the first non-zero character!
        break
    
    ### Cycling through sheets, creating sheet header and
    ### sheet data.
    # Number of objects in bytes, used in sheet header
    num_objs_bytes = bytes([len(sheet.char_list)])

    # Holds a concatenated list of character names
    char_names = b''

    # Holds character data for each sheet
    sheet_data = b''

    # For each character in the sheet...
    for char in sheet.char_list:

      #While sheet name is shorter than 8 characters...
      while len(char.name) < 8:
        # pad it with zeroes!
        char.name += ' '

      # Convert character name to bytes
      char_name_bytes = bytes(char.name, utf8)
      
      # Add converted name to list
      char_names += char_name_bytes
      
      # Convert the character data to bytes and add character termination:
      char_bytes = bytes(char.data) + b'\x94'

      # Add char_bytes to sheet data
      sheet_data+=char_bytes

    # Combine header and data into sheet_data
    # Header: (num objects + char_names) Data: (sheet_data + sheet_terminator)
    sheet_data = num_objs_bytes + char_names + sheet_data + b'\x17'

    # add sheet data to file
    file_data+=sheet_data

  ### Getting data for file header:
  # number of sheets
  num_sheets_bytes = bytes([len(book.sheets)])

  # name of file
  book_name = book.name
  while len(book_name) < 8:
    book_name += ' '
  
  book_name_bytes = bytes(book_name, utf8)

  ### Building header
  # (FileType + Filename + num sheets + sheet names + header termination)
  file_hdr = bytes(bytes([1]) + book_name_bytes + num_sheets_bytes + sheet_name_bytes + b'\x19')
  print(file_hdr)

  ### Building file data
  # (header) + (data) + (file termination)
  file_data = file_hdr + file_data + b'\x04'

  ### Writing to file
  # with open( book.name + '.nge', mode='wb') as file:
  #   file.write(file_data)
  file_buffer.write(file_data)
# active_book = Book("Test")

# def gen_string():
#   string = ''
#   for x in range(randint(2,8)):
#     string += choice(ascii_letters)
#   return string

# for x in range(randint(4,8)):
#   sheet_name = gen_string()
#   active_book.add_sheet(sheet_name)

# for sheet in active_book.sheets:
#   char_list = sheet.char_list
#   for x in range(16):
#     char = char_list[x]
#     if randint(0,1) == 1:
#       char.name = gen_string()
#       for index, pixel in enumerate(char.data):
#         char.data[index] = randint(0,3)
# print("lmao")  

# write_file(active_book)
# read_file(active_book.name, active_book)