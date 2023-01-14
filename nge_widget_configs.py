from tkinter import VERTICAL
# Each of these variables contain configurations
# for each frame per widget type. In the case of
# more than one widget of a type in a frame, they
# are grouped as a list of tuples of dictionaries.
# The first entry in each tuple is the config for
# that widget, and the second is the grid options.

draw_subframe_cfg = ({
      "class_" : "Subframe",
      "name" : "draw_btn_frame",
      "width" : 40,
      "height" : 320
    },
    {
      "sticky" : "NESW",
      "column" : 0,
    })

draw_canvas_cfgs = [
  ({
    "name" : "draw_canvas",
    "background" : "#000000",
    "width" : 395,
    "height" : 395 
  },
  {
    "column": 1,
    "row" : 0,
    "rowspan": 4,
    "sticky" : "N",
  }),
  ({
    "name" : "col_palette",
    "background" : "#ffffff",
    "relief" : "groove",
    "bd" : 1,
    "width" : 37,
    "height" : 148
  },
  {
    "in_" : ".nge.draw_frame.draw_btn_frame",
    "column" : 0,
    "row" : 5,
    "columnspan" : 2,
    "sticky" : "ew",
  }),
  ({
    "name" : "fg_color",
    "background" : "#ffffff",
    "relief" : "groove",
    "bd" : 1,
    "width" : 15,
    "height" : 15
  },
  {
    "in_" : ".nge.draw_frame.draw_btn_frame",
    "column" : 0,
    "row" : 6,
    "sticky" : "nsew",
  }),
  ({
    "name" : "bg_color",
    "background" : "#ffffff",
    "relief" : "groove",
    "bd" : 1,
    "width" : 15,
    "height" : 15
  },
  {
    "in_" : ".nge.draw_frame.draw_btn_frame",
    "column" : 1,
    "row" : 6,
    "sticky" : "nsew",
  }),
]

draw_btn_cfgs = [
  ({
    "name" : "pencil_btn",
    "class_" : "tool_btn",
    "style" : "NGE.tool_btn",
    "image" : "pencil"
  },
  {
    "sticky" : "N",
    "in_" : ".nge.draw_frame.draw_btn_frame",
    "column" : 0,
    "columnspan" : 2,
    "row" : 0
  }),
  ({
    "name" : "bucket_btn",
    "class_" : "tool_btn",
    "style" : "NGE.tool_btn",
    "image" : "bucket"
  },
  {
    "sticky" : "N",
    "in_" : ".nge.draw_frame.draw_btn_frame",
    "column" : 0,
    "columnspan" : 2,
    "row" : 1
  }),
  ({
    "name" : "eraser_btn",
    "class_" : "tool_btn",
    "style" : "NGE.tool_btn",
    "image" : "eraser"
  },
  {
    "sticky" : "N",
    "in_" : ".nge.draw_frame.draw_btn_frame",
    "column" : 0,
    "columnspan" : 2,
    "row" : 2
  }),
  ({
    "name" : "line_btn",
    "class_" : "tool_btn",
    "style" : "NGE.tool_btn",
    "image" : "line",
  },
  {
    "sticky" : "N",
    "in_" : ".nge.draw_frame.draw_btn_frame",
    "column" : 0,
    "columnspan" : 2,
    "row" : 3
  })
]

sheet_canvas_cfg = ({
      "name" : "sheet_canvas",
      "background" : "#000000",
      "cursor" : "cross",
      "width" : 787,
      "height" : 395,
      "selectborderwidth" : 3,
      "selectforeground" : '#ff0000' 
    },
    {
      "column" : 0,
      "row": 0,
      "sticky" : "N",
    })

tree_subframe_cfg = ({
      "class_" : "Subframe",
      "name" : "tree_btn_frame",
      "width" : 32,
      "height" : 320
    },
    {
      "sticky" : "NS",
      "in_" : ".nge.tree_frame",
      "column" : 0,
      "row" : 0,
    })

tree_fileview_cfg = ({
      "name" : "file_treeview",
      "show" : "tree",
      "style" : "NGE.fileview",
      "selectmode" : "browse",
      "height" : 13,
    },
    {
      "sticky" : "NSEW",
      "column" : 1,
      "row" : 0
    })

tree_btn_cfgs = [
  ({
      "name" : "add_sh",
      "image" : "sheet_add",
      "style" : "TButton"
    },
    {
      "sticky" : "N",
      "in_" : ".nge.tree_frame.tree_btn_frame",
      "column" : 0,
      "row" : 0
  }),
  ({
      "name" : "rem_sh",
      "image" : "sheet_rm",
      "style" : "TButton"
    },
    {
      "sticky" : "N",
      "in_" : ".nge.tree_frame.tree_btn_frame",
      "column" : 0,
      "row" : 1
  }),
  ({
      "name" : "add_ch",
      "image" : "char_add",
      "style" : "TButton"
    },
    {
      "sticky" : "N",
      "in_" : ".nge.tree_frame.tree_btn_frame",
      "column" : 0,
      "row" : 2
  }),
  ({
      "name" : "rem_ch",
      "image" : "char_rm",
      "style" : "TButton"
    },
    {
      "sticky" : "N",
      "in_" : ".nge.tree_frame.tree_btn_frame",
      "column" : 0,
      "row" : 3
  })
]

tree_scroll_cfg = ({
      "name" : "tree_scrollbar",
      "class_" : "Scrollbar",
      "orient" : VERTICAL
    },
    {
      "sticky" : "NS",
      "column" : 2,
      "row" : 0
    })

hex_scroll_cfg = ({
    "name" : "hex_scrollbar",
    "class_" : "Scrollbar",
    "orient" : VERTICAL,
    },
    {
      "sticky" : "NS",
      "column" : 1,
      "row" : 0
    })

hex_txt_cfg = ({
    "name" : "hex_txt",
    "width" : 53,
    "relief" : "flat",
    "height" : 18
  },
  {
    "sticky" : "NS",
    "column" : 0,
    "row" : 0
  })

info_lbl_frame_cfgs = [
  ({
    "name" : "book_label_frame",
    "text" : "Book:",
    "relief" : "groove",
    "labelanchor" : "n" 
  },
  {
    "sticky" : "NSEW",
    "columnspan" : 4,
    "padx" : 6,
    "row" : 0
  }),
  ({
    "name" : "sheet_label_frame",
    "text" : "Active Sheet:",
    "relief" : "groove",
    "labelanchor" : "n" 
  },
  {
    "sticky" : "NSEW",
    "columnspan" : 2,
    "padx" : 6,
    "row" : 1
  }),
  ({
    "name" : "char_label_frame",
    "text" : "Active Character:",
    "relief" : "groove",
    "labelanchor" : "n" 
  },
  {
    "sticky" : "NSEW",
    "columnspan" : 2,
    "padx" : 6,
    "row" : 2
  })
]

info_lbl_cfgs = [
  ({
    "name" : "book_name_txt",
    "text" : 'Book Name: '
  },
  {
    "sticky" : 'ew',
    "in_" : ".nge.info_frame.book_label_frame",
    "column" : 0,
    "row" : 0
  }),
  ({

    "name" : "num_sheets_txt",
    "text" : "Number of Sheets: "
  },
  {
    "sticky" : 'ew',
    "in_" : ".nge.info_frame.book_label_frame",
    "column" : 0,
    "row" : 1
  }),
  ({
    "name" : "sheet_name_txt",
    "text" : "Sheet Name: "
  },
  {
    "sticky" : 'ew',
    "in_" : ".nge.info_frame.sheet_label_frame",
    "column" : 0,
    "row" : 0
  }),
  ({
    "name" : "sheet_id_txt",
    "text" : "Sheet ID: "
  },
  {
    "sticky" : 'ew',
    "in_" : ".nge.info_frame.sheet_label_frame",
    "column" : 0,
    "row" : 1
  }),
  ({
    "name" : "num_chars_txt",
    "text" :  "Number of Characters: "
  },
  {
    "sticky" : 'ew',
    "in_" : ".nge.info_frame.sheet_label_frame",
    "column" : 0,
    "row" : 2
  }),
  ({
  "name" : "char_name_txt",
  "text" :  'Character Name: '
  },
  {
    "sticky" : 'ew',
    "in_" : ".nge.info_frame.char_label_frame",
    "column" : 0,
    "row" : 0
  }),
  ({
    "name" : "char_id_txt",
    "text" : 'Character ID: '
  },
  {
    "sticky" : 'ew',
    "in_" : ".nge.info_frame.char_label_frame",
    "column" : 0,
    "row" : 1
  }),
  ({
    "name" : "book_name",
    "textvariable" : 'book_name_var'
  },
  {
    "sticky" : 'ew',
    "in_" : ".nge.info_frame.book_label_frame",
    "column" : 1,
    "row" : 0
  }),
  ({
    "name" : "num_sheets",
    "textvariable" : 'sheet_num_var'
  },
  {
    "sticky" : 'ew',
    "in_" : ".nge.info_frame.book_label_frame",
    "column" : 1,
    "row" : 1
  }),
  ({
    "name" : "sheet_name",
    "textvariable" : 'sheet_name_var'
  },
  {
    "sticky" : 'ew',
    "in_" : ".nge.info_frame.sheet_label_frame",
    "column" : 1,
    "row" : 0
  }),
  ({
    "name" : "sheet_id",
    "textvariable" : 'sheet_id_var'
  },
  {
    "sticky" : 'ew',
    "in_" : ".nge.info_frame.sheet_label_frame",
    "column" : 1,
    "row" : 1
  }),
  ({
    "name" : "num_chars",
    "textvariable" :  'char_num_var'
  },
  {
    "sticky" : 'ew',
    "in_" : ".nge.info_frame.sheet_label_frame",
    "column" : 1,
    "row" : 2
  }),
  ({
    "name" : "char_name",
    "textvariable" : 'char_name_var'
  },
  {
    "sticky" : 'ew',
    "in_" : ".nge.info_frame.char_label_frame",
    "column" : 1,
    "row" : 0
  }),
  ({
    "name" : "char_id",
    "textvariable" : 'char_id_var'
  },
  {
    "sticky" : 'ew',
    "in_" : ".nge.info_frame.char_label_frame",
    "column" : 1,
    "row" : 1
  })
]

