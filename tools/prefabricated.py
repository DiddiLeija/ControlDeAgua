"Prefabicated Tkinter stuff for my GUIs."

__all__ = ("get_listbox", "get_menubutton")

from tkinter import *

# annotation stuff
from typing import List, Tuple

# Listbox builder
def get_listbox(
    root: Frame,
    options: List[str],
    row: int = 0,
    column: int = 0,
    sticky: str = "ew"
) -> Listbox:
    """
    Generate a tkinter.ListBox from a custom
    list / tuple of strings ("options").

    The root object ("root") must be a tkinter.Frame
    that has been set up with the grid() method.

    "row", "column" and "sticky" are just arguments for
    the grid() method applied to the list box object.
    """
    def get_type(req: str) -> type:
        "function to get a type from undefined classes (I mean, defined on a function - but not imported)."
        if req == "dict_keys":
            # return the dict.keys() type
            return type({"a": 1}.keys())
        elif req == "dict_values":
            # return the dict.values() type
            return type({"b": 1}.values())
        else:
            # return the type of <<None>>
            return type(None)
    # check some of the args (by assertion)
    if isinstance(root, Tk) and not isinstance(root, Frame):
        messagebox.showwarning("Advertencia al desarrollador", f"""El programa ha lanzado una advertencia. Por favor
reporte esto al desarrollador del producto.

    On 'tools.prefabicated.get_listbox', argument
    'root' is recommended to be an instance of 'tkinter.Frame',
    not 'tkinter.Tk'. When this warning is ignored, many bugs
    might be reported.

    If you are not the developer of this product, please
    report this to the author of the product.

- Test results:
  - 'root' expected class: '_tkinter.Frame' -> 'tkinter.Frame'
  - 'root' real class: {root.__class__}""")
    else:
        assert isinstance(root, Frame)
    try:
        assert isinstance(options, list) or isinstance(options, tuple)
    except AssertionError:
        # it might be a dict keys() or values()
        assert isinstance(options, get_type("dict_keys")) or isinstance(options, get_type("dict_values"))
    assert isinstance(row, int)
    assert isinstance(column, int)
    assert isinstance(sticky, str)
    # generate the list box
    index = 1
    lb = Listbox(root)
    # add the options
    for option in options:
        lb.insert(index, option.strip())
        index += 1
    # grid the object
    lb.grid(row=row, column=column, sticky=sticky)
    return lb

#####################################################################################################################

# Menubutton builder
def get_menubutton(
    root: Frame,
    options: List[str],
    variable: Var,
    row: int = 0,
    column: int = 0,
    sticky: str = "ew"
) -> Tuple[Menubutton, VariableCollector]:
    """
    Generate a tkinter MenuButton. Follow a similar process than
    get_listbox().
    """
    def get_type(req: str) -> type:
        "function to get a type from undefined classes (I mean, defined inside a function but not imported at all)."
        if req == "dict_keys":
            # return the dict.keys() type
            return type({"a": 1}.keys())
        elif req == "dict_values":
            # return the dict.values() type
            return type({"b": 1}.values())
        else:
            # return the type of <<None>>
            return type(None)
    # check some of the args (by assertion)
    if isinstance(root, Tk) and not isinstance(root, Frame):
        messagebox.showwarning("Advertencia al desarrollador", f"""El programa ha lanzado una advertencia. Por favor
reporte esto al desarrollador del producto.

    On 'tools.prefabicated.get_listbox', argument
    'root' is recommended to be an instance of 'tkinter.Frame',
    not 'tkinter.Tk'. When this warning is ignored, many bugs
    might be reported.

    If you are not the developer of this product, please
    report this to the author of the product.

- Test results:
  - 'root' expected class: '_tkinter.Frame' -> 'tkinter.Frame'
  - 'root' real class: {root.__class__}""")
    else:
        assert isinstance(root, Frame)
    try:
        assert isinstance(options, list) or isinstance(options, tuple)
    except AssertionError:
        # it might be a dict keys() or values()
        assert isinstance(options, get_type("dict_keys")) or isinstance(options, get_type("dict_values"))
    assert isinstance(row, int)
    assert isinstance(column, int)
    assert isinstance(sticky, str)

    # generate the menu button using a menu widget
    index = 1
    mb = Menubutton(root, text="Seleccione una opcion")
    mn = Menu(mb, tearoff=0)
    
    # add the options to the Menu widget
    for option in options:
        mn.add_radiobutton(label=option.strip(), variable=variable, value=index)
        index += 1
    
    # grid the Menubutton
    mb["menu"] = mn
    mb.grid(row=row, column=column, sticky=sticky)
    return mb
