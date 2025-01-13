#include <dlfcn.h>

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <unicodeobject.h>

#include <foo.h>


static PyObject *
foo_impl(PyObject *self, PyObject *args)
{
    int a, b;
    if (!PyArg_ParseTuple(args, "i|i:foo", &a, &b)) {
        return NULL;
    }

    int result = sum(a, b);

    return PyLong_FromLong(result);
}


static PyMethodDef uses_library_methods[] = {
    {"foo", foo_impl, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL} /* sentinel */
};


static struct PyModuleDef uses_library_module = {
    PyModuleDef_HEAD_INIT,
    "uses_library", /* m_name */
    NULL, /* m_doc */
    -1, /* m_size */
    uses_library_methods, /* m_methods */
};


PyMODINIT_FUNC
PyInit_uses_library(void)
{
    return PyModule_Create(&uses_library_module);
}
