from tkinter import Text, Canvas, Toplevel, NW, RAISED, SUNKEN, CENTER, PhotoImage
from tkinter.ttk import Scrollbar, Treeview, Style, Label, Frame
from math import floor
import nge_logic as prog
from nge_classes import Book, AddCharDialog

# Sets style
def set_style(root: Toplevel):
  #creating style and theme for this application
  style = Style(root)
  style.theme_create("NGE", "default")
  style.theme_use("NGE")

  #gathering required default layouts for modification
  default_btn_layout = style.layout("TButton")
  default_lbl_layout = style.layout("TLabel")
  default_tree_layout = style.layout("Treeview")
  #setting up layouts for custom themed widgets
  style.layout("hex_lbl", default_lbl_layout)
  style.layout("tool_btn", default_btn_layout)
  style.layout("sel_tool_btn", default_btn_layout)
  style.layout("sel_color_btn", default_btn_layout)
  style.layout("color_btn", default_btn_layout)
  #style.layout("sel_hex_lbl", default_lbl_layout)
  style.layout("fileview", default_tree_layout)

  # Configuring styles
  style.configure("hex_lbl", padding=0, font='TkFixedFont', 
                  background="#ffffff", foreground="#000000")
  #style.configure("sel_hex_lbl", background="#0000ff", foreground="#ffffff")
  style.configure("tool_btn", relief="raised", padding=2)
  style.configure("sel_tool_btn", relief="sunken", padding=2)
  style.configure("color_btn", relief="raised", padding=2)
  style.configure("sel_color_btn", relief="sunken", padding=2)
  style.configure("fileview", background='#ffffff', rowheight = 24)
  #setting up default button click animation
  style.map("TButton", relief=[("pressed", SUNKEN), ("!pressed", RAISED)])
  style.map("fileview", background=[("selected", "#cccccc")])
