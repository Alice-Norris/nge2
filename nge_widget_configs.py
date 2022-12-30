from tkinter import Toplevel, VERTICAL
from gui_logic import chg_cursor
frame_cfgs = [
  {
    "name" : "draw_frame",
    "class_" : "Frame",
    "height" : 320,
    "width"  : 360,
    "borderwidth" : 2,
    "relief" : "groove",
  },  
  {
    "sticky" : "NESW",
    "column" : 0,
    "row" : 0
  },
  {
    "name" : "sheet_frame",
    "class_" : "Frame",
    "height" : 256,
    "width"  : 512,
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
    "name" : "tree_frame",
    "class_" : "Frame",
    "height" : 328,
    "width"  : 328,
    "borderwidth" : 2,
    "relief" : "groove"
  },
  {
    "sticky" : "NSEW",
    "column" : 0,
    "row" : 1
  },
  {
    "name" : "hex_frame",
    "class_" : "Frame",
    "height" : 328,
    "width"  : 328,
    "borderwidth" : 2,
    "relief" : "groove"
  },
  {
    "sticky" : "NSEW",
    "column" : 1,
    "row" : 1
  },
  {
    "name" : "info_frame",
    "class_" : "Frame",
    "height" : 328,
    "width" : 328,
    "borderwidth" : 2,
    "relief" : "groove"
  },
  {
    "sticky" : "NESW",
    "column" : 2,
    "row" : 1
  }
]

### End Frame Configurations and Grids ###

### Configuration and Gridding for Subframes ###

subframe_cfgs = [
    {
      "master" : ".draw_frame",
      "class_" : "Subframe",
      "name" : "draw_btn_frame",
      "width" : 32,
      "height" : 320
    },
    {
      "sticky" : "NESW",
      "column" : 0,
      "in_" : '.draw_frame'
    },
    {
      "master" : ".tree_frame",
      "class_" : "Subframe",
      "name" : "tree_btn_frame",
      "width" : 38,
      "height" : 320
    },
    {
      "sticky" : "NS",
      "column" : 2,
      "row" : 0,
      "in_" : '.tree_frame'
    }
]

### End Subframe Configurations and Grids ###

### Canvas configurations and Grids ###
canvas_cfgs = [
  {
    "name" : "draw_canvas",
    "background" : "#FFFFFF",
    "width" : 329,
    "height" : 329 
  },
  {
    "column": 1,
    "row" : 0,
    "rowspan": 4,
    "sticky" : "N",
    "in_" : ".draw_frame"
  },
  {
    "name" : "sheet_canvas",
    "background" : "#FFFFFF",
    "cursor" : "cross",
    "width" : 657,
    "height" : 329
  },
  {
    "column" : 0,
    "row": 0,
    "sticky" : "N",
    "in_" : ".sheet_frame"
  }
]

### End Canvas Configurations and Grids ###

### Treeview Configurations and Grids ###
view_cfg = [
    {
      "name" : "file_tree_view",
      "show" : "tree",
      "style" : "NGE.Treeview",
      "selectmode" : "browse",
      "height" : 21,
    },
    {
      "sticky" : "NSEW",
      "in_" : ".tree_frame",
      "column" : 0,
      "row" : 0
    }
]
### End Treeview Configuration and Grids ###

### Button Configurations and Grids ###
btn_cfgs = [
  {
    "name" : "pencil_btn",
    "class_" : "tool_btn",
    "style" : "NGE.tool_btn",
    "image" : "pencil"
  },
  {
    "sticky" : "N",
    "in_" : ".draw_frame.draw_btn_frame",
    "column" : 0,
    "row" : 0
  },
  {
    "name" : "bucket_btn",
    "class_" : "tool_btn",
    "style" : "NGE.tool_btn",
    "image" : "bucket"
  },
  {
    "sticky" : "N",
    "in_" : ".draw_frame.draw_btn_frame",
    "column" : 0,
    "row" : 1
  },
  {
    "name" : "eraser_btn",
    "class_" : "tool_btn",
    "style" : "NGE.tool_btn",
    "image" : "eraser"
  },
  {
    "sticky" : "N",
    "in_" : ".draw_frame.draw_btn_frame",
    "column" : 0,
    "row" : 2
  },
  {
    "name" : "line_btn",
    "class_" : "tool_btn",
    "style" : "NGE.tool_btn",
    "image" : "line"
  },
  {
    "sticky" : "N",
    "in_" : ".draw_frame.draw_btn_frame",
    "column" : 0,
    "row" : 3
  },
  {
    "name" : "wht_btn",
    "class_" : "color_btn",
    "style" : "NGE.tool_btn",
    "image" : "wht"
  },
  {
    "sticky" : "N",
    "in_" : ".draw_frame.draw_btn_frame",
    "column" : 0,
    "row" : 4
  },
  {
    "name" : "ltg_btn",
    "class_" : "color_btn",
    "style" : "NGE.tool_btn",
    "image" : "ltg"
  },
  {
    "sticky" : "N",
    "in_" : ".draw_frame.draw_btn_frame",
    "column" : 0,
    "row" : 5
  },
  {
    "name" : "dkg_btn",
    "class_" : "color_btn",
    "style" : "NGE.tool_btn",
    "image" : "dkg"
  },
  {
    "sticky" : "N",
    "in_" : ".draw_frame.draw_btn_frame",
    "column" : 0,
    "row" : 6
  },
  {
    "name" : "blk_btn",
    "class_" : "color_btn",
    "style" : "NGE.tool_btn",
    "image" : "blk"
  },
  {
    "sticky" : "N",
    "in_" : ".draw_frame.draw_btn_frame",
    "column" : 0,
    "row" : 7
  }
]
### End Button Configurations and Grids ###

### Treeview Button Configurations and Grids ###
treeview_btn_cfgs = [
  {
    "name" : "add_sh",
    "image" : "sheet_add",
    "style" : "TButton"
  },
  {
    "sticky" : "N",
    "in_": ".tree_frame.tree_btn_frame",
    "column" : 0,
    "row" : 0
  },
  {
    "name" : "rm_sh",
    "image" : "sheet_rm",
    "style" : "TButton"
  },
  {
    "sticky" : "N",
    "in_": ".tree_frame.tree_btn_frame",
    "column" : 0,
    "row" : 1
  },
  {
    "name" : "add_ch",
    "image" : "char_add",
    "style" : "TButton"
  },
  {
    "sticky" : "N",
    "in_": ".tree_frame.tree_btn_frame",
    "column" : 0,
    "row" : 2
  },
    {
    "name" : "rm_ch",
    "image" : "char_rm",
    "style" : "TButton"
  },
  {
    "sticky" : "N",
    "in_": ".tree_frame.tree_btn_frame",
    "column" : 0,
    "row" : 3
  }
]
### Scrollbar Configurations and Grids ###
scrollbar_cfgs = [
  {
    "name" : "hex_scrollbar",
    "class_" : "Scrollbar",
    "orient" : VERTICAL
  },
  {
    "sticky" : "NSEW",
    "in_" : ".hex_frame",
    "column" : 2,
    "row" : 0
  },
  {
    "name" : "tree_scrollbar",
    "class_" : "Scrollbar",
    "orient" : VERTICAL
  },
  {
    "sticky" : "NS",
    "in_" : ".tree_frame",
    "column" : 1,
    "row" : 0
  }
]
### End Scrollbar Configs and Grids ###

### Text Configurations and Grids ###
txt_cfgs = [
  {
    "name" : "hex_txt_header",
    "width" : 4
  },
  {
    "sticky": "NESW",
    "in_" : ".hex_frame",
    "column" : 0,
    "row" : 0
  },
  {
    "name" : "hex_txt_data",
    "width" : 32,
  },
  {
    "sticky": "NESW",
    "in_" : ".hex_frame",
    "column" : 1,
    "row" : 0
  }
]
### End Text Configurations and Grids ###