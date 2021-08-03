"""
Bienvenido a la configuracion de la aplicacion.
Aqui, puede ver la informacion de usuarios, y ver
las ventas desde diferentes formatos.
"""

import json
from tkinter import *
from tkinter import messagebox
from idlelib.textview import view_text
from tools.database import *
from tools.windowmanager import *
from tools.users import check, get_admin_pwd

# annotation stuff
from typing import Callable, Optional

DB, CUR = getDatabase("WaterDB.sqlite")

class GUI:
    """
    GUI class for this feature.
    """

    def __init__(self, root: Tk) -> None:
        "constructor method."
        # handle the root internally
        self.root = root
        windowTitle(self.root, "App de configuracion")
        # generate the menu directly
        if get_admin_pwd() is not None:
            # there is an admin password, ask for it
            self.ensureAdmin(next_page=lambda: self.go("get-in"))
        else:
            # just advice of the vulnerability and go ahead
            messagebox.showwarning("Advertencia: Cuenta de Administrador desprotegida", """La cuenta del administrador no tiene
actualmente una clave de acceso. Esto puede ser riesgoso,
pues cualquier usuario podra ingresar a las opciones
y privilegios del administrador.""")
            self.go("get-in-directly")

    def ensureAdmin(self, next_page: Optional[Callable] = None) -> Optional[bool]:
        "get sure the admin is here..."
        self.adminport = Frame(self.root)
        self.adminport.grid()
        entry_var = StringVar()
        # we need a door helper
        def submit():
            if len(entry_var.get().strip()) < 1:
                messagebox.showerror("Error", "Contraseña vacia.")
            if check(entry_var):
                # go to the next place
                if next_page is not None:
                    # it is a function, go there
                    next_page()
                else:
                    # just get back
                    return True
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")
                return False
        # create the widgets
        door_l = Label(self.adminport, text="Ingrese contraseña del administrador del programa:",
        font=("Calibri", "14", "bold")).grid(row=0, column=0, sticky="ew")
        door_e = Entry(self.adminport, textvariable=entry_var, width=40,
        show="*", font=("Calibri", "14", "normal")).grid(row=0, column=1, sticky="ew")
        skip = Button(self.adminport, text="Cancelar y salir", command=self.root.quit, bg="red",
        fg="white", font=("Calibri", "14", "bold")).grid(row=1, column=0, sticky="ew")
        submit = Button(self.adminport, text="Ingresar", command=submit, bg="green",
        fg="white", font=("Calibri", "14", "bold")).grid(row=1, column=1, sticky="ew")

    def showUsers(self) -> None:
        "show the users"
        user_map = {}
        try:
            with open("C:/Program Files/Control de Agua/tools/users.json", "r") as f:
                user_map = json.loads(f.read())
        except Exception as e:
            if len(open("C:/Program Files/Control de Agua/tools/users.json", "r").read().strip()) < 1:
                open("C:/Program Files/Control de Agua/tools/users.json", "w").write("{}")
            else:
                messagebox.showwarning("?", f"error: {str(e)}")
        s = ""
        for k, v in user_map.items():
            s += f"- {k}: {v}\n"
        view_text(self.root, "Usuarios y contraseñas registradas", s)

    def notDefined(self, arg: str) -> None:
        "default for not-implemented or not-defined features."
        messagebox.showinfo(str(NotImplemented), f"Funcion/elemento sin definir: <{arg}>")

    def menu(self) -> None:
        "generate the menu gui."
        # use a frame to pack all the menu stuff
        self.welcome = Frame(self.root)
        self.welcome.grid()
        # use __doc__ for the description
        descr = Label(self.welcome, text=__doc__, bg="white", fg="black",
        font=("Calibri", "14", "normal")).grid(row=0, column=0, sticky="ew")
        # user registry function
        new_usr = Button(self.welcome, text="Nuevo usuario", bg="whitesmoke", fg="black", font=("Calibri", "14", "bold"),
        command=lambda: self.go("home -> register")).grid(row=1, column=0, sticky="ew")
        # view the registered users
        view_usrs = Button(self.welcome, text="Ver lista de usuarios", bg="whitesmoke", fg="black",
        font=("Calibri", "14", "bold"), command=lambda: self.go("view users")).grid(row=2, column=0, sticky="ew")
        # view a report
        view_report = Button(self.welcome, text="Ver registro de ventas", bg="whitesmoke", fg="black",
        font=("Calibri", "14", "bold"), command=lambda: self.go("view registry")).grid(row=3, column=0, sticky="ew")
        # exit button
        get_out = Button(self.welcome, text="Salir de la pagina", bg="red", fg="white",
        font=("Calibri", "14", "bold"), command=self.root.quit).grid(row=4, column=0, sticky="ew")

    def reg_page(self) -> None:
        "generate a register page."
        self.regframe = Frame(self.root)
        self.regframe.grid()
        self.new_name = StringVar()
        self.new_pwd = StringVar()
        name_l = Label(self.regframe, text="Introduzca nombre completo (sin acentos):", font=("Calibri", "13", "bold"), bg="whitesmoke",
        fg="black").grid(row=0, column=0, sticky="ew")
        name_e = Entry(self.regframe, width=30, textvariable=self.new_name,
        font=("Calibri", "13", "normal")).grid(row=0, column=1, sticky="ew")
        name_l = Label(self.regframe, text="Introduzca una contraseña para relacionar con la cuenta:",
        font=("Calibri", "13", "bold"), bg="whitesmoke", fg="black").grid(row=1, column=0, sticky="ew")
        name_e = Entry(self.regframe, width=30, textvariable=self.new_pwd,
        font=("Calibri", "13", "normal"), show="*").grid(row=1, column=1, sticky="ew")
        skip = Button(self.regframe, text="Cancelar", font=("Calibri", "13", "bold"), bg="red", fg="white",
        command=lambda: self.go("register -> home")).grid(row=2, column=0, sticky="ew")
        send_b = Button(self.regframe, text="Registrar", font=("Calibri", "13", "bold"), bg="green", fg="white",
        command=self.register_internal).grid(row=2, column=1, sticky="ew")
    
    def see_registry(self) -> None:
        """
        See the sales registry. This giant function will prompt for an initial date
        and a final date (I mean, a period to search) and then it will return a
        formatted output.
        """
        self.sales_f = Frame(self.root)
        self.sales_f.grid()
        first_date_l = Label(self.sales_f, text="Introduzca una primera fecha para buscar:", bg="whitesmoke", fg="black",
        font=("Calibri", "13", "bold")).grid(row=0, column=0, sticky="ew")

    def register_internal(self) -> None:
        "make a database registry for the latest user."
        try:
            new_usr = self.new_name.get().strip()
            new_id = self.new_pwd.get().strip()
            if len(new_usr) < 1: raise ValueError(f'Expected non-empty strings, got ""')
            # update
            to_save = []
            with open("C:/Program Files/Control de Agua/tools/users.json", "r") as f:
                to_save.append(json.loads(f.read()))
            to_save[0][new_usr.lower()] = new_id
            with open("C:/Program Files/Control de Agua/tools/users.json", "w") as f:
                f.write(json.dumps(to_save[0]))
        except Exception as e:
            if len(open("C:/Program Files/Control de Agua/tools/users.json", "r").read().strip()) < 1:
                open("C:/Program Files/Control de Agua/tools/users.json", "w").write("{}")
            messagebox.showerror("Error al registrar", f"""Ha sucedido un error al registrar al usuario. Puede que
haya dejado la entrada totalmente vacia o haya agregado algun caracter no
permitido. Verifique e intente de nuevo.

(Error: '{str(e)}')""")
            return None
        # success message
        messagebox.showinfo("Proceso completado", f"""El proceso se ha completado exitosamente. Se le redirigira a la pagina de inicio.

Datos del registro:
- Usuario: {new_usr} ({new_usr.lower()})
- Contraseña: {new_id}""")
        self.go("register -> home")

    def go(self, arg: str) -> None:
        "point to any place in the gui."
        if arg == "home -> register":
            # go to the register page
            self.welcome.grid_remove()
            self.reg_page()
        elif arg == "register -> home":
            # go back to home
            self.regframe.grid_remove()
            self.menu()
        elif arg == "view users":
            self.showUsers()
        elif arg == "get-in":
            self.adminport.grid_remove()
            self.menu()
        elif arg == "get-in-directly":
            # same than "get-in", but overriding
            # the grid_remove (basically because
            # the door is not "activated")
            self.menu()
        elif arg == "view registry":
            self.see_registry()
        else:
            self.notDefined(arg)

# run the main loop
root = Tk()
gui = GUI(root)
root.mainloop()
