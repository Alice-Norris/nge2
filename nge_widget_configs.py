from tkinter import VERTICAL, W
import nge_gui_logic as gui
frame_cfgs = [
  {
    "master" : ".nge",
    "name" : "draw_frame",
    "class_" : "Frame",
    "height" : 400,
    "width"  : 438,
    "borderwidth" : 2,
    "relief" : "groove",
  },  
  {
    "sticky" : "NESW",
    "column" : 0,
    "row" : 0
  },
  {
    "master" : ".nge",
    "name" : "sheet_frame",
    "class_" : "Frame",
    "height" : 393,
    "width"  : 792,
    "borderwidth" : 2,
    "relief" : "groove"
  },
  {
    "sticky" : "NESW",
    "columnspan" : 2,
    "column" : 1,
    "row" : 0
  },
  {
    "master" : ".nge",
    "name" : "tree_frame",
    "class_" : "Frame",
    "height" : 348,
    "width"  : 340,
    "borderwidth" : 2,
    "relief" : "groove"
  },
  {
    "sticky" : "NSEW",
    "column" : 2,
    "row" : 1
  },
  {
    "master" : ".nge",
    "name" : "hex_frame",
    "class_" : "Frame",
    "height" : 328,
    "width"  : 450,
    "borderwidth" : 2,
    "relief" : "groove"
  },
  {
    "sticky" : "NSEW",
    "column" : 1,
    "row" : 1
  },
  {
    "master" : ".nge",
    "name" : "info_frame",
    "class_" : "Frame",
    "height" : 328,
    "width" : 384,
    "borderwidth" : 2,
    "relief" : "groove"
  },
  {
    "sticky" : "NSEW",
    "column" : 0,
    "row" : 1
  }
]

### End Frame Configurations and Grids ###

### Configuration and Gridding for Subframes ###

subframe_cfgs = [
    {
      "master" : ".nge.draw_frame",
      "class_" : "Subframe",
      "name" : "draw_btn_frame",
      "width" : 32,
      "height" : 320
    },
    {
      "sticky" : "NESW",
      "column" : 0,
    },
    {
      "master" : ".nge.tree_frame",
      "class_" : "Subframe",
      "name" : "tree_btn_frame",
      "width" : 32,
      "height" : 320
    },
    {
      "sticky" : "NS",
      "column" : 0,
      "row" : 0,
    }
]

### End Subframe Configurations and Grids ###

### Canvas configurations and Grids ###
canvas_cfgs = [
  {
    "master" : ".nge.draw_frame",
    "name" : "draw_canvas",
    "background" : "#ffffff",
    "width" : 393,
    "height" : 393 
  },
  {
    "column": 1,
    "row" : 0,
    "rowspan": 4,
    "sticky" : "N",

  },
  {
    "master" : ".nge.sheet_frame",
    "name" : "sheet_canvas",
    "background" : "#ffffff",
    "cursor" : "cross",
    "width" : 786,
    "height" : 393
  },
  {
    "column" : 0,
    "row": 0,
    "sticky" : "N",

  },
  {
    "master" : ".nge.draw_frame.draw_btn_frame",
    "name" : "col_palette",
    "background" : "#ffffff",
    "relief" : "groove",
    "bd" : 1,
    "width" : 33,
    "height" : 127
  },
  {
    "column" : 0,
    "row" : 5,
    "columnspan" : 2,
    "sticky" : "ew",

  },
  {
    "master" : ".nge.draw_frame.draw_btn_frame",
    "name" : "fg_color",
    "background" : "#ffffff",
    "relief" : "groove",
    "bd" : 1,
    "width" : 15,
    "height" : 15
  },
  {
    "column" : 0,
    "row" : 6,
    "sticky" : "nsew",

  },
  {
    "master" : ".nge.draw_frame.draw_btn_frame",
    "name" : "bg_color",
    "background" : "#ffffff",
    "relief" : "groove",
    "bd" : 1,
    "width" : 15,
    "height" : 15
  },
  {
    "column" : 1,
    "row" : 6,
    "sticky" : "nsew",

  }
]

### Treeview Configurations and Grids ###
treeview_cfg = [
    {
      "master" : ".nge.tree_frame",
      "name" : "file_tree_view",
      "show" : "tree",
      "style" : "NGE.fileview",
      "selectmode" : "browse",
      "height" : 13,
    },
    {
      "sticky" : "NSEW",
      "column" : 1,
      "row" : 0
    }
]
### End Treeview Configuration and Grids ###

### Tool Button Configurations and Grids ###
tool_btn_cfgs = [
  {
    "master" : ".nge.draw_frame.draw_btn_frame",
    "name" : "pencil_btn",
    "class_" : "tool_btn",
    "style" : "NGE.tool_btn",
    "image" : "pencil"
  },
  {
    "sticky" : "N",
    "column" : 0,
    "columnspan" : 2,
    "row" : 0
  },
  {
    "master" : ".nge.draw_frame.draw_btn_frame",
    "name" : "bucket_btn",
    "class_" : "tool_btn",
    "style" : "NGE.tool_btn",
    "image" : "bucket"
  },
  {
    "sticky" : "N",
    "column" : 0,
    "columnspan" : 2,
    "row" : 1
  },
  {
    "master" : ".nge.draw_frame.draw_btn_frame",
    "name" : "eraser_btn",
    "class_" : "tool_btn",
    "style" : "NGE.tool_btn",
    "image" : "eraser"
  },
  {
    "sticky" : "N",
    "column" : 0,
    "columnspan" : 2,
    "row" : 2
  },
  {
    "master" : ".nge.draw_frame.draw_btn_frame",
    "name" : "line_btn",
    "class_" : "tool_btn",
    "style" : "NGE.tool_btn",
    "image" : "line",

  },
  {
    "sticky" : "N",
    "column" : 0,
    "columnspan" : 2,
    "row" : 3
  }
]
### End Tool Button Configurations and Grids ###

### Color Button Configurations and Grids ###
col_btn_cfgs = [
 {
    "name" : "wht_btn",
    "class_" : "color_btn",
    "style" : "NGE.color_btn",
    "image" : "wht"
  },
  {
    "sticky" : "N",
    "column" : 0,
    "row" : 4
  },
  {
    "name" : "ltg_btn",
    "class_" : "color_btn",
    "style" : "NGE.color_btn",
    "image" : "ltg"
  },
  {
    "sticky" : "N",
    "column" : 0,
    "row" : 5
  },
  {
    "name" : "dkg_btn",
    "class_" : "color_btn",
    "style" : "NGE.color_btn",
    "image" : "dkg"
  },
  {
    "sticky" : "N",
    "column" : 0,
    "row" : 6
  },
  {
    "name" : "blk_btn",
    "class_" : "color_btn",
    "style" : "NGE.color_btn",
    "image" : "blk"
  },
  {
    "sticky" : "N",
    "column" : 0,
    "row" : 7
  }
]
### End Color Button Configurations and Grids ###

### Treeview Button Configurations and Grids ###
treeview_btn_cfgs = [
  {
    "master" : ".nge.tree_frame.tree_btn_frame",
    "name" : "add_sh",
    "image" : "sheet_add",
    "style" : "TButton"
  },
  {
    "sticky" : "N",
    "column" : 0,
    "row" : 0
  },
  {
    "master" : ".nge.tree_frame.tree_btn_frame",
    "name" : "rem_sh",
    "image" : "sheet_rm",
    "style" : "TButton"
  },
  {
    "sticky" : "N",
    "column" : 0,
    "row" : 1
  },
  {
    "master" : ".nge.tree_frame.tree_btn_frame",
    "name" : "add_ch",
    "image" : "char_add",
    "style" : "TButton"
  },
  {
    "sticky" : "N",
    "column" : 0,
    "row" : 2
  },
  {
    "master" : ".nge.tree_frame.tree_btn_frame",
    "name" : "rem_ch",
    "image" : "char_rm",
    "style" : "TButton"
  },
  {
    "sticky" : "N",
    "column" : 0,
    "row" : 3
  }
]
### End Treeview Button Configurations and Grids ###

### Scrollbar Configurations and Grids ###
scrollbar_cfgs = [
  {
    "master" : ".nge.hex_frame",
    "name" : "hex_scrollbar",
    "class_" : "Scrollbar",
    "orient" : VERTICAL,
  },
  {
    "sticky" : "NSEW",
    "column" : 2,
    "row" : 0
  },
  {
    "master" : ".nge.tree_frame",
    "name" : "tree_scrollbar",
    "class_" : "Scrollbar",
    "orient" : VERTICAL
  },
  {
    "sticky" : "NS",
    "column" : 2,
    "row" : 0
  }
]
### End Scrollbar Configs and Grids ###

### Text Configurations and Grids ###
txt_cfgs = [
  {
    "master" : ".nge.hex_frame",
    "name" : "hex_txt",
    "width" : 53,
    "height" : 18
  },
  {
    "sticky": "NESW",
    "column" : 1,
    "row" : 0
  },
]
### End Text Configurations and Grids ###

### Begin Info Label Configurations and Grids ###
lbl_frame_cfgs = [
  {
    "master" : ".nge.info_frame",
    "name" : "book_label_frame",
    "text" : "Book:",
    "relief" : "groove",
    "width" : 420,
    "height" : 112,
    "labelanchor" : "n" 
  },
  {
    "column" : 0,
    "row" : 0
  },
  {
    "master" : ".nge.info_frame",
    "name" : "sheet_label_frame",
    "text" : "Active Sheet:",
    "relief" : "groove",
    "width" : 420,
    "height" : 112,
    "labelanchor" : "n" 
  },
  {
    "column" : 0,
    "row" : 1
  },
    {
    "master" : ".nge.info_frame",
    "name" : "char_label_frame",
    "text" : "Active Character:",
    "relief" : "groove",
    "width" : 420,
    "height" : 112,
    "labelanchor" : "n" 
  },
  {
    "column" : 0,
    "row" : 2
  }
]

lbl_cfgs = [
  {
    "master" : ".nge.info_frame.book_label_frame",
    "name" : "book_name",
    "text" : "Book Name:"
  },
  {
    "sticky" : "W",
    "column" : 0,
    "row" : 0
  },
  {
    "master" : ".nge.info_frame.book_label_frame",
    "name" : "num_sheets",
    "text" : "Number of Sheets:"
  },
  {
    "sticky" : "W",
    "column" : 0,
    "row" : 1
  },
  {
    "master" : ".nge.info_frame.sheet_label_frame",
    "name" : "sheet_name",
    "text" : "Sheet Name:"
  },
  {
    "sticky" : "W",
    "column" : 0,
    "row" : 0
  },
  {
    "master" : ".nge.info_frame.sheet_label_frame",
    "name" : "sheet_id",
    "text" : "Sheet ID:"
  },
  {
    "sticky" : "W",
    "column" : 0,
    "row" : 1
  },
  {
    "master" : ".nge.info_frame.sheet_label_frame",
    "name" : "num_chars",
    "text" : "Number of Characters:"
  },
  {
    "sticky" : "W",
    "column" : 0,
    "row" : 2
  },
  {
    "master" : ".nge.info_frame.char_label_frame",
    "name" : "char_name",
    "text" : "Character Name:"
  },
  {
    "sticky" : "W",
    "column" : 0,
    "row" : 0
  },
  {
    "master" : ".nge.info_frame.char_label_frame",
    "name" : "char_id",
    "text" : "Character ID:"
  },
  {
    "sticky" : "W",
    "column" : 0,
    "row" : 1
  },
]