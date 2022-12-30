#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string>
#include <cstddef>
#include <iostream>
class Book {

};

static PyObject* file_write(PyObject *self, PyObject *book);
static PyObject* convert_book(PyObject* self, PyObject *book);

static PyMethodDef FileOpsMethods[] = {
  {"file_write", file_write, METH_VARARGS,
   "Write a file."},
  {
    "convert_book", convert_book, METH_VARARGS,
    "Convert Book object to a C++ object"
  }
};

static struct PyModuleDef fileops = {
  PyModuleDef_HEAD_INIT,
  "fileops",
  NULL,
  -1,
  FileOpsMethods
};

PyMODINIT_FUNC PyInit_fileops(void) {
  return PyModule_Create(&fileops);
};

static PyObject* file_write(PyObject *self, PyObject *book) {
  // std::string book_name = " ";
  // uint8_t num_sheets = 0;
  // std::string sheet_names[num_sheets];
  // uint8_t** char_num_lists[num_sheets];
  // std::string char_name_lists[num_sheets];
  // uint8_t** char_dat_lists[num_sheets];

  // if (!PyArg_ParseTuple(args, ))
  // if (!PyArg_ParseTuple(book, ))
}

int main(int argc, char *argv[]){
  wchar_t* program = Py_DecodeLocale(argv[0], NULL);
  if (program == NULL) {
    std::cerr << "Fatal Error: cannot decode locale!" << std::endl;
    exit(1);
  }

  if (PyImport_AppendInittab("fileops", PyInit_fileops) == -1) {
    std::cerr << "Error: Could not extend modules table" << std::endl;
    exit(1);
  }

  Py_SetProgramName(program);

  Py_Initialize();

  PyObject* fileopsmodule = PyImport_ImportModule("fileops");

  if (!fileopsmodule) {
    PyErr_Print();
    std::cerr << "Could not import modle 'fileops'";
  }
}