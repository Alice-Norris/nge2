import tkinter as tk
from nge_classes import Book, Sheet, Character
from random import randint
class Application(tk.Frame):
  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.grid()
    self.root = self.winfo_toplevel()
    self.active_book = Book("test")
    self.book_randomize()
    self.createWidgets()
    self.draw_sheet_canvas(self.canvas)
    print(self.root.image_names())
    self.grid_setup(self.canvas)

  def createWidgets(self):
    args = {
      "name" : "sheet_canvas",
      "background" : "#FFFFFF",
      "cursor" : "cross",
      "width" : 641,
      "height" : 321
    }
    self.canvas = tk.Canvas(self, cnf=args)
    self.canvas.grid()
  def book_randomize(self):
    char_list = self.active_book.sheets[0].char_list
    for char in char_list:
      char_data = char.data
      for index, pixel, in enumerate(char_data):
        char_data[index] = randint(0,3)

  def grid_setup(self, canvas):
    x = 1
    y = 1
    xrow = 0
    ycol = 0
    height = int(canvas.cget('height'))
    width = int(canvas.cget('width'))
    
    while (y < height):
      x = 1
      while( x < width):
        id_str = str(xrow) + "." +str(ycol)
        canvas.create_rectangle(x, y, x + 40, y + 40, tag=id_str)
        x += 40
        xrow += 1
      y += 40
      xrow = 0
      ycol += 1
  
  def draw_sheet_canvas(self, canvas):
    char_list = self.active_book.sheets[0].char_list
    for index, char in enumerate(char_list):
      img_hdr = bytes("P6\n8 8\n3\n", encoding='utf-8')
      pix = char.data
      img_data = self.create_img_data(pix)
      x_sq = index % 16
      y_sq = index // 16
      id_str = str(x_sq) + '.' + str(y_sq)
      img_ptr = tk.PhotoImage(master=self.root, name=id_str, data=img_data, format="PPM")
      self.canvas.create_image(x_sq*40, y_sq*40, image=img_ptr, tag=id_str, anchor=tk.NW)
    print("lmao")

  def create_img_data(self, char_data: list):
    img_data = b''
    for row in range(len(char_data) // 8):
      start = row * 8
      end = start + 8
      pix_row = char_data[start:end]
      row_bytes = b''
      for p in pix_row:
        row_bytes += bytes([p] * 3) * 5
      row_bytes = row_bytes * 5
      img_data += row_bytes
    return img_data
    
app = Application()
app.master.title('Sample application')
app.mainloop()

