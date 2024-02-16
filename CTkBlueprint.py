import ast
import json
import os
import sys
import textwrap
import tkinter
import webbrowser
from json.decoder import JSONDecodeError

import customtkinter as ctk
from PIL import Image
from customtkinter import filedialog as fd

from assets.widgets.CTkColorPicker import AskColor
from assets.widgets.CTkMenuBar import CTkMenuBar, CustomDropdownMenu
from assets.widgets.ctk_scrollable_dropdown import CTkScrollableDropdown
from assets.widgets.spinBox import Spinbox

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

LOGO = f"{CURRENT_PATH}\\assets\\icons\\logo.ico"
EXPORT_LOGO = f"{CURRENT_PATH}\\assets\\icons\\python.ico"
ICONS = {
    "logo": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\logo.png"),
                         Image.open(f"{CURRENT_PATH}\\assets\\icons\\logo.png"), size=(36, 36)),
    "close": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\close.png"),
                          Image.open(f"{CURRENT_PATH}\\assets\\icons\\close.png"), size=(24, 24)),
    "download": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\download.png"),
                             Image.open(f"{CURRENT_PATH}\\assets\\icons\\download.png"), size=(24, 24)),
    "code": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\code.png"),
                         Image.open(f"{CURRENT_PATH}\\assets\\icons\\code.png"), size=(24, 24)),
    "preview": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\preview.png"),
                            Image.open(f"{CURRENT_PATH}\\assets\\icons\\preview.png"), size=(24, 24)),

    "FOLDER": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\folder_black.png"),
                           Image.open(f"{CURRENT_PATH}\\assets\\icons\\folder.png"), size=(20, 20)),

    "Button": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\btn.png"),
                           Image.open(f"{CURRENT_PATH}\\assets\\icons\\btn.png"), size=(24, 24)),
    "CheckBox": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\check.png"),
                             Image.open(f"{CURRENT_PATH}\\assets\\icons\\check.png"), size=(24, 24)),
    "ComboBox": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\combo.png"),
                             Image.open(f"{CURRENT_PATH}\\assets\\icons\\combo.png"), size=(24, 24)),
    "Frame": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\frame.png"),
                          Image.open(f"{CURRENT_PATH}\\assets\\icons\\frame.png"), size=(24, 24)),
    "Entry": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\entry.png"),
                          Image.open(f"{CURRENT_PATH}\\assets\\icons\\entry.png"), size=(24, 24)),
    "Label": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\label.png"),
                          Image.open(f"{CURRENT_PATH}\\assets\\icons\\label.png"), size=(24, 24)),
    "OptionMenu": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\option.png"),
                               Image.open(f"{CURRENT_PATH}\\assets\\icons\\option.png"), size=(24, 24)),
    "ProgressBar": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\progress.png"),
                                Image.open(f"{CURRENT_PATH}\\assets\\icons\\progress.png"), size=(24, 24)),
    "RadioButton": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\radio.png"),
                                Image.open(f"{CURRENT_PATH}\\assets\\icons\\radio.png"), size=(24, 24)),
    "Slider": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\slider.png"),
                           Image.open(f"{CURRENT_PATH}\\assets\\icons\\slider.png"), size=(24, 24)),
    "Switch": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\switch.png"),
                           Image.open(f"{CURRENT_PATH}\\assets\\icons\\switch.png"), size=(24, 24)),
    "TextBox": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\textbox.png"),
                            Image.open(f"{CURRENT_PATH}\\assets\\icons\\textbox.png"), size=(24, 24)),

    "duplicate": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\duplicate.png"),
                              Image.open(f"{CURRENT_PATH}\\assets\\icons\\duplicate.png"), size=(24, 24)),
    "delete": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\delete.png"),
                           Image.open(f"{CURRENT_PATH}\\assets\\icons\\delete.png"), size=(24, 24)),
    "move": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\move.png"),
                         Image.open(f"{CURRENT_PATH}\\assets\\icons\\move.png"), size=(24, 24)),
    "properties": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\properties.png"),
                               Image.open(f"{CURRENT_PATH}\\assets\\icons\\properties.png"), size=(24, 24))
}
FONTS = {
    "title": ("", 22, "bold"),
    "large": ("", 16, "normal"),
    "normal_bold": ("", 14, "bold"),
    "normal": ("", 14, "normal"),
    "small": ("", 13, "normal"),
}
DEFAULT_BTN = {
    "corner_radius": 2,
    "font": FONTS["normal"],
    "height": 30,
    "compound": "left",
    "anchor": "center"
}
WIDGET_BTN = {
    "font": FONTS["normal"],
    "fg_color": "transparent",
    "height": 35,
    "corner_radius": 2,
    "compound": "left",
    "anchor": "w"
}
CLOSE_BTN = {
    "width": 25,
    "height": 25,
    "image": ICONS["close"],
    "fg_color": "transparent",
    "hover": False
}
BTN_OPTION = {
    "compound": "left",
    "anchor": "w",
    "fg_color": "transparent",
    "text_color": ("black", "white"),
    "corner_radius": 5,
    "hover_color": ("gray65", "gray28")
}
SEC_BTN = {
    "fg_color": "transparent",
    "text_color": ("black", "white"),
    "border_width": 2
}
ARGUMENTS = {
    "size_options": ["width", "height", "corner_radius", "border_width", "border_spacing", "checkbox_width",
                     "checkbox_height", "radiobutton_width", "radiobutton_height", "border_width_unchecked",
                     "border_width_checked", "switch_width", "switch_height"],
    "color_options": ["bg_color", "fg_color", "hover_color", "border_color", "text_color",
                      "text_color_disabled",
                      "button_color", "button_hover_color", "dropdown_fg_color", "dropdown_hover_color",
                      "dropdown_text_color", "placeholder_text_color", "progress_color"],
    "pack_options": ["side", "fill", "anchor", "expand", "padx", "pady", "ipadx", "ipady"],
    "grid_options": ["row", "column", "rowspan", "columnspan", "padx", "pady", "sticky"],
    "content_options": ["text", "compound", "anchor", "state", "hover", "justify", "placeholder_text",
                        "values", "mode", "from_", "to", "number_of_steps", "wrap", "font"]
}
GEOMETRY_TYPE = "grid"


def load_default():
    with open(f"{CURRENT_PATH}\\assets\\default_theme.json", "r") as file:
        return json.load(file)


def duplicated_widget(root, prop_window, widget):
    options = {}
    for arg_type, arg_list in ARGUMENTS.items():
        for arg in arg_list:
            try:
                options[arg] = widget.cget(arg)
            except:
                pass

    widget_class = type(widget)
    new_widget = widget_class(widget.master)

    popup_menu = PopupMenu(root)
    new_widget.bind("<Button-3>", lambda event: do_popup(event, popup_menu), add="+")

    duplicate_btn = ctk.CTkButton(popup_menu.frame, text="Duplicate", **BTN_OPTION,
                                  command=lambda: duplicated_widget(root, prop_window, new_widget),
                                  image=ICONS["duplicate"])
    duplicate_btn.pack(expand=True, fill="x", padx=10, pady=(10, 0))
    delete_btn = ctk.CTkButton(popup_menu.frame, text="Delete", **BTN_OPTION,
                               command=lambda: delete_widget(prop_window, new_widget), image=ICONS["delete"])
    delete_btn.pack(expand=True, fill="x", padx=10, pady=5)
    movetop_btn = ctk.CTkButton(popup_menu.frame, text="Move to Top", **BTN_OPTION,
                                command=lambda: move_top(root.main_frame, new_widget),
                                image=ICONS["move"])
    movetop_btn.pack(expand=True, fill="x", padx=10, pady=5)
    properties_btn = ctk.CTkButton(popup_menu.frame, text="Properties", **BTN_OPTION,
                                   command=lambda: open_properties(root, new_widget),
                                   image=ICONS["properties"])
    properties_btn.pack(expand=True, fill="x", padx=10, pady=5)

    new_widget.configure(**options)
    if GEOMETRY_TYPE == "grid":
        grid_info = widget.grid_info()
        if 'row' in grid_info:
            del grid_info['row']
        elif 'column' in grid_info:
            del grid_info['column']
        elif 'in' in grid_info:
            del grid_info['in']
        new_widget.grid(**grid_info)
    elif GEOMETRY_TYPE == "pack":
        pack_info = widget.pack_info()
        new_widget.pack(**pack_info)


def delete_widget(prop_window, widget):
    prop_window.destroy()
    widget.destroy()


def open_properties(root, widget):
    properties = WidgetProperties(root, widget)
    properties.grid(row=1, column=2, padx=0, pady=(5, 0), sticky="nsew")


def move_top(frame, widget):
    widgets = frame.winfo_children()

    widgets.remove(widget)
    widgets.insert(0, widget)

    for w in widgets:
        if GEOMETRY_TYPE == "grid":
            w.grid_remove()
        elif GEOMETRY_TYPE == "pack":
            w.pack_forget()

    for i, w in enumerate(widgets):
        if GEOMETRY_TYPE == "grid":
            w.grid(row=i)
        elif GEOMETRY_TYPE == "pack":
            w.pack()


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_height = int((screen_width / 2) - (width / 2))
    window_width = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{window_height}+{window_width}")


def do_popup(event, frame):
    try:
        frame.popup(event.x_root, event.y_root)
    finally:
        frame.grab_release()


def open_links(url):
    webbrowser.open(url)


def delete_all(frame):
    widgets = frame.winfo_children()
    if widgets:
        for widget in widgets:
            widget.destroy()


def get_widget_options(widget, default_options):
    options = {}
    for arg_type, arg_list in ARGUMENTS.items():
        for arg in arg_list:
            try:
                if arg == "font":
                    font = widget.cget(arg)
                    options[arg] = str(font)
                else:
                    options[arg] = widget.cget(arg)
            except:
                pass

    default_widget_options = default_options[type(widget).__name__]
    for custom_key, custom_value in list(options.items()):
        if custom_key in default_widget_options and custom_value == default_widget_options[custom_key]:
            del options[custom_key]

    return options


def get_geometry_info(widget):
    geometry_info = None
    if GEOMETRY_TYPE == "grid":
        geometry_info = widget.grid_info()

        if 'in' in geometry_info:
            del geometry_info['in']
        if 'ipadx' in geometry_info:
            del geometry_info['ipadx']
        if 'ipady' in geometry_info:
            del geometry_info['ipady']
    elif GEOMETRY_TYPE == "pack":
        geometry_info = widget.pack_info()

        if 'in' in geometry_info:
            del geometry_info['in']
    return geometry_info


def get_widget_info(widget, default_options, master):
    get_name = widget.winfo_name()
    widget_name = get_name.replace("!", "")
    widget_type = type(widget).__name__
    widget_options = get_widget_options(widget, default_options)
    widget_grid = get_geometry_info(widget)

    widget_info = {
        "name": widget_name,
        "type": widget_type,
        "master": master,
        "options": widget_options,
        "grid": widget_grid
    }

    if 'font' in widget_options:
        widget_options['font'] = ast.literal_eval(widget_options['font'])

    return widget_info


def generate_code(widget_info):
    widget_name = widget_info['name']
    widget_type = widget_info['type']
    master = widget_info['master']
    options = widget_info['options']
    grid_info = widget_info['grid']

    return f"{widget_name} = ctk.{widget_type}({master}, **{options})\n{widget_name}.{GEOMETRY_TYPE}(**{grid_info})"


def export_code(root, title, geometry, save_to, icon=None):
    logo_path = os.path.normpath(f"{CURRENT_PATH}/icons/logo.ico")
    logo_path = logo_path.replace("\\", "/")
    icon = icon if icon else logo_path
    default_options = load_default()
    root_widgets_code = {}
    child_widgets_code = {}

    widgets = root.winfo_children()
    for widget in widgets:
        root_widget_info = get_widget_info(widget, default_options, "self")
        root_widgets_code[root_widget_info['name']] = generate_code(root_widget_info)

        if root_widget_info['name'].startswith("ctkframe"):
            child_widgets = widget.winfo_children()
            if child_widgets:
                for child_widget in child_widgets:
                    child_widget_info = get_widget_info(child_widget, default_options, root_widget_info['name'])
                    child_widgets_code[child_widget_info['name']] = generate_code(child_widget_info)

    root_widgets_string = '\n'.join(root_widgets_code.values())
    child_widgets_string = '\n'.join(child_widgets_code.values())

    code_template = f'''import customtkinter as ctk

ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("{title}")
        self.geometry("{geometry}")
        self.iconbitmap("{icon}")

        {textwrap.indent(root_widgets_string, ' ' * 8).lstrip()}
        {textwrap.indent(child_widgets_string, ' ' * 8).lstrip()}

app = App()
app.mainloop()
'''

    with open(save_to, "w") as file:
        file.write(code_template)


def preview(root, title, geometry):
    default_options = load_default()
    root_widgets_code = {}
    child_widgets_code = {}

    widgets = root.winfo_children()
    for widget in widgets:
        root_widget_info = get_widget_info(widget, default_options, "self")
        root_widgets_code[root_widget_info['name']] = generate_code(root_widget_info)

        if root_widget_info['name'].startswith("ctkframe"):
            child_widgets = widget.winfo_children()
            if child_widgets:
                for child_widget in child_widgets:
                    child_widget_info = get_widget_info(child_widget, default_options, root_widget_info['name'])
                    child_widgets_code[child_widget_info['name']] = generate_code(child_widget_info)

    root_widgets_string = '\n'.join(root_widgets_code.values())
    child_widgets_string = '\n'.join(child_widgets_code.values())

    code_template = f'''import customtkinter as ctk

ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("{title}")
        self.geometry("{geometry}")

        {textwrap.indent(root_widgets_string, ' ' * 8).lstrip()}
        {textwrap.indent(child_widgets_string, ' ' * 8).lstrip()}

app = App()
app.mainloop()
'''

    exec(code_template)


def close_project(root):
    for widget in root.winfo_children():
        widget.destroy()
    for job_id in root.tk.call('after', 'info'):
        root.after_cancel(job_id)
    root.destroy()

    os.system(f"{sys.executable} main.py")


class PopupMenu(ctk.CTkToplevel):
    def __init__(self,
                 master=None,
                 corner_radius=3,
                 border_width=1,
                 **kwargs):

        super().__init__(takefocus=1)

        self.y = None
        self.x = None
        self.focus()
        self.master_window = master
        self.corner = corner_radius
        self.border = border_width
        self.hidden = True

        if sys.platform.startswith("win"):
            self.after(100, lambda: self.overrideredirect(True))
            self.transparent_color = self._apply_appearance_mode(self._fg_color)
            self.attributes("-transparentcolor", self.transparent_color)
        elif sys.platform.startswith("darwin"):
            self.overrideredirect(True)
            self.transparent_color = 'systemTransparent'
            self.attributes("-transparent", True)
        else:
            self.attributes("-type", "splash")
            self.transparent_color = '#000001'
            self.corner = 0
            self.withdraw()

        self.frame = ctk.CTkFrame(self, bg_color=self.transparent_color, corner_radius=self.corner,
                                  border_width=self.border, **kwargs)
        self.frame.pack(expand=True, fill="both")

        self.master.bind("<ButtonPress>", lambda event: self._withdraw_off(), add="+")
        self.bind("<Button-1>", lambda event: self._withdraw(), add="+")
        self.master.bind("<Configure>", lambda event: self._withdraw(), add="+")

        self.resizable(width=False, height=False)
        self.transient(self.master_window)

        self.update_idletasks()

        self.withdraw()

    def _withdraw(self):
        self.withdraw()
        self.hidden = True

    def _withdraw_off(self):
        if self.hidden:
            self.withdraw()
        self.hidden = True

    def popup(self, x=None, y=None):
        self.x = x
        self.y = y
        self.deiconify()
        self.focus()
        self.geometry('+{}+{}'.format(self.x, self.y))
        self.hidden = False


class ExportWindow(ctk.CTkToplevel):
    WIDTH = 500
    HEIGHT = 280

    def __init__(self, root):
        super().__init__()

        self.title("Export to .py")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)

        center_window(self, self.WIDTH, self.HEIGHT)

        self.transient(root)
        self.after(250, lambda: self.iconbitmap(EXPORT_LOGO))
        self.after(100, self.lift)
        self.grab_set()

        self.main_frame = root.main_frame
        self.icon_path = None
        self.grid_columnconfigure(0, weight=1)

        name_label = ctk.CTkLabel(self, text="App Name", font=FONTS["normal"])
        name_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        self.name_value = ctk.CTkEntry(self, corner_radius=3, border_width=1, width=200, height=30)
        self.name_value.insert(0, "myApp")
        self.name_value.grid(row=0, column=1, padx=20, pady=(20, 5), sticky="ew")

        width_label = ctk.CTkLabel(self, text="Width", font=FONTS["normal"])
        width_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.width_value = Spinbox(self, min_value=100, max_value=10000, corner_radius=3, fg_color="transparent")
        self.width_value.set(500)
        self.width_value.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

        height_label = ctk.CTkLabel(self, text="Height", font=FONTS["normal"])
        height_label.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="w")
        self.height_value = Spinbox(self, min_value=100, max_value=10000, corner_radius=3, fg_color="transparent")
        self.height_value.set(250)
        self.height_value.grid(row=2, column=1, padx=20, pady=(5, 10), sticky="ew")

        icon_label = ctk.CTkLabel(self, text="Icon", font=FONTS["normal"])
        icon_label.grid(row=3, column=0, padx=20, pady=(5, 20), sticky="w")
        self.icon_value = ctk.CTkButton(self, text="Select icon", command=self.select_icon, **DEFAULT_BTN)
        self.icon_value.grid(row=3, column=1, padx=20, pady=(5, 20), sticky="ew")

        export_btn = ctk.CTkButton(self, text="Export", command=self.generate_py, **DEFAULT_BTN)
        export_btn.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def select_icon(self):
        file_path = fd.askopenfilename(defaultextension="ico", filetypes=[("ICO Files", "*.ico")])
        if file_path:
            file_name = os.path.basename(file_path)
            self.icon_value.configure(text=file_name)
            self.icon_path = file_path

    def generate_py(self):
        save_to = fd.asksaveasfilename(defaultextension="py", title="Export To", filetypes=[("Python Files", "*.py")],
                                       initialfile="main.py")

        if save_to:
            title = str(self.name_value.get())
            geometry = f"{self.width_value.get()}x{self.height_value.get()}"
            export_code(self.main_frame, title, geometry, self.icon_path, save_to)
        self.destroy()

    def on_closing(self):
        self.destroy()


class ConfigureWindow(ctk.CTkToplevel):
    WIDTH = 500
    HEIGHT = 280

    def __init__(self, root):
        super().__init__()

        self.title("Configure Window")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)

        center_window(self, self.WIDTH, self.HEIGHT)

        self.transient(root)
        self.after(100, self.lift)
        self.grab_set()

        self.main_frame = root.main_frame
        self.grid_columnconfigure(0, weight=1)

        row_label = ctk.CTkLabel(self, text="Row nr.", font=FONTS["normal"])
        row_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        self.row_entry = ctk.CTkEntry(self, corner_radius=3, border_width=1, width=200, height=30)
        self.row_entry.insert(0, "0")
        self.row_entry.grid(row=0, column=1, padx=20, pady=(20, 5), sticky="ew")

        weight_row_label = ctk.CTkLabel(self, text="Row Weight (0, 1)", font=FONTS["normal"])
        weight_row_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.row_weight = Spinbox(self, min_value=0, max_value=1, corner_radius=3, fg_color="transparent")
        self.row_weight.set(0)
        self.row_weight.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

        column_label = ctk.CTkLabel(self, text="Column nr.", font=FONTS["normal"])
        column_label.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="w")
        self.column_entry = ctk.CTkEntry(self, corner_radius=3, border_width=1, width=200, height=30)
        self.column_entry.insert(0, "0")
        self.column_entry.grid(row=2, column=1, padx=20, pady=(5, 10), sticky="ew")

        weight_column_label = ctk.CTkLabel(self, text="Column Weight (0, 1)", font=FONTS["normal"])
        weight_column_label.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="w")
        self.column_weight = Spinbox(self, min_value=0, max_value=1, corner_radius=3, fg_color="transparent")
        self.column_weight.set(0)
        self.column_weight.grid(row=3, column=1, padx=20, pady=(5, 10), sticky="ew")

        save_btn = ctk.CTkButton(self, text="Configure", command=self.configure_grid)
        save_btn.grid(row=4, column=0, padx=20, pady=(40, 20), sticky="e", columnspan=2)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def configure_grid(self):
        widget = self.main_frame
        row = self.row_entry.get()
        column = self.column_entry.get()
        weight_row = self.row_weight.get()
        weight_column = self.column_weight.get()
        widget.grid_rowconfigure(row, weight=weight_row)

        widget.grid_columnconfigure(column, weight=weight_column)

        self.on_closing()

    def on_closing(self):
        self.destroy()


class WidgetProperties(ctk.CTkFrame):
    WIDTH = 300
    HEIGHT = 720

    def __init__(self, master, widget=None):
        super().__init__(master, width=self.WIDTH)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_propagate(False)

        title = ctk.CTkLabel(self, text="Widget Parameters", font=FONTS["normal_bold"])
        title.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        close_btn = ctk.CTkButton(self, text="", command=self.close_frame, **CLOSE_BTN)
        close_btn.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        seg_button = ctk.CTkSegmentedButton(self, values=["Size", "Color", "Geometry", "Content"],
                                            command=self.toggle_frame)
        seg_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)
        seg_button.set("Size")

        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.grid(row=2, column=0, padx=2, pady=5, sticky="nsew", columnspan=2)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.master_widget = None
        self.spinbox = None
        self.content_widget = None
        self.color_widget = None
        self.save_btn = None
        self.reset_btn = None
        self.size_widget = None
        self.master_dict = {}
        self.widget = widget

        self.root = master

        self.size_options = {}
        self.color_options = {}
        self.grid_options = {}
        self.content_options = {}

        get_widgets = master.main_frame.winfo_children()

        current_master = master.main_frame
        self.master_dict["root"] = current_master

        for x in get_widgets:
            if x.winfo_name().startswith("!ctkframe"):
                widget_name = x.winfo_name()

                self.master_dict[widget_name] = x

        for option_type in ARGUMENTS:
            for option in ARGUMENTS[option_type]:
                try:
                    if option_type in ["pack_options", "grid_options"]:
                        if GEOMETRY_TYPE == "grid":
                            grid_info = self.widget.grid_info()
                            self.grid_options[option] = grid_info[option]
                        elif GEOMETRY_TYPE == "pack":
                            pack_info = self.widget.pack_info()
                            self.grid_options[option] = pack_info[option]
                    elif option_type == "content_options":
                        if option == "font":
                            font = self.widget.cget(option)
                            self.__dict__[option_type][option] = {"family": font[0], "size": font[1], "weight": font[2]}
                        else:
                            self.__dict__[option_type][option] = self.widget.cget(option)
                    else:
                        self.__dict__[option_type][option] = {"value": self.widget.cget(option)}
                except:
                    pass

        self.toggle_frame("Size")

    def set_widget(self, widget):
        self.widget = widget

    def toggle_frame(self, frame):
        widgets = self.main_frame.winfo_children()
        for widget in widgets:
            widget.grid_forget()

        try:
            self.reset_btn.grid_forget()
            self.save_btn.grid_forget()
        except AttributeError:
            pass

        if frame == "Size":
            self.size_widgets()
        elif frame == "Color":
            self.color_widgets()
        elif frame == "Geometry":
            self.geometry_widgets()
        elif frame == "Content":
            self.content_widgets()

    def size_widgets(self):
        self.size_widget = {}

        for index, (arg, value) in enumerate(self.size_options.items()):
            label = ctk.CTkLabel(self.main_frame, text=f"{arg.capitalize()}", font=FONTS["normal"])
            label.grid(row=index, column=0, padx=10, pady=10, sticky="w")
            spinbox = Spinbox(self.main_frame, min_value=1, max_value=1000)
            spinbox.grid(row=index, column=1, padx=10, pady=10, sticky="w")
            spinbox.set(value['value'])

            self.size_widget[arg] = {"spinbox": spinbox}

        self.save_btn = ctk.CTkButton(self, text="Apply", **DEFAULT_BTN, command=self.size_callback)
        self.save_btn.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def color_widgets(self):
        self.color_widget = {}

        for args, value in self.color_options.items():
            label = ctk.CTkLabel(self.main_frame, text=f"{args}: {value['value']}", font=FONTS["normal"])
            label.grid(padx=10, pady=5, sticky="w")
            button = ctk.CTkButton(self.main_frame, text="", **DEFAULT_BTN,
                                   fg_color=value['value'], hover=False)
            button.configure(command=lambda l=label, btn=button, arg=args: self.color_callback(l, btn, arg))
            button.grid(padx=10, pady=(5, 20), sticky="ew")

            self.color_widget[args] = {"button": button}

    def geometry_widgets(self):
        self.spinbox = {}
        grid_attr = ARGUMENTS["grid_options"]
        pack_attr = ARGUMENTS["pack_options"]

        if GEOMETRY_TYPE == "grid":
            for index, attribute in enumerate(grid_attr):
                label = ctk.CTkLabel(self.main_frame, text=attribute, font=FONTS["normal"])
                label.grid(row=index, column=0, padx=10, pady=5, sticky="w")
                if attribute == "sticky":
                    spinbox = ctk.CTkOptionMenu(self.main_frame,
                                                values=['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw', 'ns', 'ew',
                                                        'nsew'])
                    spinbox.grid(row=index, column=1, padx=10, pady=5, sticky="e")
                    CTkScrollableDropdown(spinbox, values=['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw', 'ns', 'ew',
                                                           'nsew'])
                    spinbox.set(self.grid_options[attribute])
                    if self.grid_options[attribute]:
                        spinbox.set(self.grid_options[attribute])
                elif attribute == "rowspan" or attribute == "columnspan":
                    spinbox = Spinbox(self.main_frame, min_value=1, max_value=100)
                    spinbox.grid(row=index, column=1, padx=10, pady=5, sticky="e")
                    spinbox.set(self.grid_options[attribute])

                else:
                    spinbox = Spinbox(self.main_frame, min_value=0, max_value=100)
                    spinbox.grid(row=index, column=1, padx=10, pady=5, sticky="e")
                    spinbox.set(self.grid_options[attribute])

                self.spinbox[attribute] = spinbox
        elif GEOMETRY_TYPE == "pack":
            for index, attribute in enumerate(pack_attr):
                label = ctk.CTkLabel(self.main_frame, text=attribute, font=FONTS["normal"])
                label.grid(row=index, column=0, padx=10, pady=5, sticky="w")
                if attribute == "anchor":
                    spinbox = ctk.CTkOptionMenu(self.main_frame,
                                                values=['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'center'])
                    CTkScrollableDropdown(spinbox, values=['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'center'])
                    spinbox.grid(row=index, column=1, padx=10, pady=5, sticky="e")
                    spinbox.set(self.grid_options[attribute])
                elif attribute == "side":
                    spinbox = ctk.CTkOptionMenu(self.main_frame,
                                                values=['left', 'top', 'right', 'bottom'])
                    CTkScrollableDropdown(spinbox, values=['left', 'top', 'right', 'bottom'])
                    spinbox.grid(row=index, column=1, padx=10, pady=5, sticky="e")
                    spinbox.set(self.grid_options[attribute])
                elif attribute == "expand":
                    spinbox = ctk.CTkCheckBox(self.main_frame, onvalue=True, offvalue=False, text="")
                    spinbox.grid(row=index, column=1, padx=10, pady=5, sticky="e")
                    if self.grid_options[attribute]:
                        spinbox.select()
                    else:
                        spinbox.deselect()
                elif attribute == "fill":
                    spinbox = ctk.CTkOptionMenu(self.main_frame,
                                                values=['x', 'y', 'both'])
                    spinbox.grid(row=index, column=1, padx=10, pady=5, sticky="e")
                    CTkScrollableDropdown(spinbox, values=['x', 'y', 'both'])
                    spinbox.set(self.grid_options[attribute])

                else:
                    spinbox = Spinbox(self.main_frame, min_value=0, max_value=100)
                    spinbox.grid(row=index, column=1, padx=10, pady=5, sticky="e")
                    spinbox.set(self.grid_options[attribute])

                self.spinbox[attribute] = spinbox

        self.save_btn = ctk.CTkButton(self, text="Apply", **DEFAULT_BTN, command=self.geometry_callback)
        self.save_btn.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def content_widgets(self):
        update_functions = {
            ctk.CTkEntry: self.update_entry,
            ctk.CTkCheckBox: self.update_checkbox,
            ctk.CTkOptionMenu: self.update_optionmenu,
            Spinbox: self.update_spinbox
        }
        attributes = {
            "text": (ctk.CTkEntry, {}),
            "image": (ctk.CTkButton, {"text": "Select image"}),
            "compound": (ctk.CTkOptionMenu, {"values": ["left", "top", "center", "right", "bottom"]}),
            "anchor": (ctk.CTkOptionMenu, {"values": ["center", "w", "e", "n", "s"]}),
            "state": (ctk.CTkOptionMenu, {"values": ["normal", "disabled"]}),
            "hover": (ctk.CTkCheckBox, {"text": "Hover OFF", "onvalue": True, "offvalue": False}),
            "justify": (ctk.CTkOptionMenu, {"values": ["center", "left", "right"]}),
            "placeholder_text": (ctk.CTkEntry, {}),
            "values": (ctk.CTkEntry, {}),
            "mode": (ctk.CTkOptionMenu, {"values": ["determinate", "indeterminate"]}),
            "from_": (Spinbox, {"min_value": 0, "max_value": 10000}),
            "to": (Spinbox, {"min_value": 0, "max_value": 10000}),
            "number_of_steps": (Spinbox, {"min_value": 0, "max_value": 10000}),
            "wrap": (ctk.CTkOptionMenu, {"values": ["char", "word", "none"]}),
            "font": {
                "family": (ctk.CTkOptionMenu, {"values": list(tkinter.font.families())}),
                "size": (Spinbox, {"min_value": 1, "max_value": 100}),
                "weight": (
                    ctk.CTkOptionMenu, {"values": ["normal", "bold", "italic", "roman", "underline", "overstrike"]})
            }
        }

        self.content_widget = {}

        master_values = list(self.master_dict.keys())
        master = str(self.widget.master)

        for m in master_values:
            if self.widget.winfo_name() == m:
                master_values.remove(m)

        master_label = ctk.CTkLabel(self.main_frame, text="Master")
        master_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.master_widget = ctk.CTkOptionMenu(self.main_frame, height=30, values=master_values)
        CTkScrollableDropdown(self.master_widget, values=master_values)
        self.master_widget.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="ew", columnspan=2)
        last_name = master.split('.')[-1]
        if last_name == "!ctkscrollableframe":
            last_name = "root"
        self.master_widget.set(last_name)

        if str(self.widget.winfo_name()).startswith("!ctkframe"):
            propagate_label = ctk.CTkLabel(self.main_frame, text="Propagate")
            propagate_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
            self.propagate_var = ctk.StringVar(value="off")
            propagate_value = ctk.CTkCheckBox(self.main_frame, text="Propagate OFF", onvalue="on", offvalue="off",
                                              command=self.set_propagate, variable=self.propagate_var)
            propagate_value.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        for index, attribute in enumerate(self.content_options.keys(), start=4):
            if attribute in attributes:
                if attribute == "font":
                    font_attributes = attributes[attribute]
                    for font_attr, (widget_class, widget_kwargs) in font_attributes.items():
                        label = ctk.CTkLabel(self.main_frame, text=f"{attribute.capitalize()} {font_attr.capitalize()}")
                        label.grid(row=index, column=0, padx=10, pady=10, sticky="w")
                        if font_attr in ["family", "weight"]:
                            widget = widget_class(self.main_frame, **widget_kwargs)
                            CTkScrollableDropdown(widget, **widget_kwargs)
                            widget.grid(row=index, column=1, padx=10, pady=10, sticky="e")
                        else:
                            widget = widget_class(self.main_frame, **widget_kwargs)
                            widget.grid(row=index, column=1, padx=10, pady=10, sticky="e")

                        default_value = self.content_options[attribute][font_attr]
                        update_function = update_functions.get(type(widget))
                        if update_function is not None:
                            update_function(widget, default_value)

                        self.content_widget[f"{attribute}_{font_attr}"] = widget
                        index += 1
                else:
                    widget_class, widget_kwargs = attributes[attribute]
                    label = ctk.CTkLabel(self.main_frame, text=attribute.capitalize())
                    label.grid(row=index, column=0, padx=10, pady=10, sticky="w")
                    widget = widget_class(self.main_frame, **widget_kwargs)
                    widget.grid(row=index, column=1, padx=10, pady=10, sticky="e")

                    default_value = self.content_options[attribute]
                    update_function = update_functions.get(type(widget))
                    if update_function is not None:
                        update_function(widget, default_value)

                    self.content_widget[attribute] = widget

        self.save_btn = ctk.CTkButton(self, text="Apply", **DEFAULT_BTN, command=self.content_callback)
        self.save_btn.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def set_propagate(self):
        if self.propagate_var.get() == "on":
            if GEOMETRY_TYPE == "grid":
                self.widget.grid_propagate(False)
            else:
                self.widget.pack_propagate(False)
        else:
            if GEOMETRY_TYPE == "grid":
                self.widget.grid_propagate(True)
            else:
                self.widget.pack_propagate(True)

    def content_callback(self):
        for attribute in self.content_options.keys():
            if attribute == "font":
                family = self.content_widget["font_family"].get()
                size = self.content_widget["font_size"].get()
                weight = self.content_widget["font_weight"].get()
                self.widget.configure(font=(family, size, weight))
                self.content_options[attribute] = {"family": family, "size": size, "weight": weight}
            else:
                new_value = self.content_widget[attribute].get()
                if attribute == "values":
                    options = []
                    values = new_value.split(',')
                    for value in values:
                        value = value.strip()
                        options.append(value)

                    self.widget.configure(values=options)
                    self.widget.set(options[0])
                elif attribute == "hover":
                    if new_value:
                        self.widget.configure(hover=False)
                    else:
                        self.widget.configure(hover=True)
                else:
                    self.widget.configure(**{attribute: new_value})

                self.content_options[attribute] = new_value

        master = self.master_widget.get()
        master = self.master_dict[master]
        self.widget = self.copy_widget(self.widget, master)

    def geometry_callback(self):
        grid_keys = ARGUMENTS["grid_options"]
        pack_keys = ARGUMENTS["pack_options"]

        if GEOMETRY_TYPE == "grid":
            for key in grid_keys:
                value = self.spinbox[key].get()
                self.grid_options[key] = value

            self.widget.grid(**self.grid_options)

        elif GEOMETRY_TYPE == "pack":
            for key in pack_keys:
                value = self.spinbox[key].get()
                self.grid_options[key] = value

            self.widget.pack(**self.grid_options)

    def color_callback(self, label, btn, arg):
        pick_color = AskColor()
        color = pick_color.get()
        color_map = {}

        keys = self.color_options.keys()
        for key in keys:
            color_map[key] = key

        if color:
            if arg in color_map:
                config_type = color_map[arg]
                label.configure(text=f"{config_type}: {color}")
                btn.configure(fg_color=color)
                self.widget.configure(**{config_type: color})
                self.color_options[config_type] = {"value": color}

    def size_callback(self):
        for arg in self.size_options:
            spinbox = self.size_widget[arg]["spinbox"]
            value = int(spinbox.get())
            self.widget.configure(**{arg: value})
            self.size_options[arg] = {"value": value}

    def copy_widget(self, old_widget, new_parent):
        new_widget = type(old_widget)(new_parent)

        copy_size = {}
        copy_color = {}
        copy_geometry = {}
        copy_content = {}

        for option_type in ARGUMENTS:
            for option in ARGUMENTS[option_type]:
                try:
                    if option_type in ["pack_options", "grid_options"]:
                        if GEOMETRY_TYPE == "pack":
                            pack_info = old_widget.pack_info()
                            copy_geometry[option] = pack_info[option]
                        elif GEOMETRY_TYPE == "grid":
                            grid_info = old_widget.grid_info()
                            copy_geometry[option] = grid_info[option]
                    elif option_type == "content_options":
                        if option == "font":
                            font = old_widget.cget(option)
                            copy_content[option] = (f"{font[0]}", font[1], f"{font[2]}")
                        else:
                            copy_content[option] = old_widget.cget(option)
                    elif option_type == "size_options":
                        copy_size[option] = old_widget.cget(option)
                    elif option_type == "color_options":
                        copy_color[option] = old_widget.cget(option)
                except:
                    pass

        config = {}
        config.update(copy_size)
        config.update(copy_color)
        config.update(copy_content)

        new_widget.configure(**config)

        if GEOMETRY_TYPE == "pack":
            new_widget.pack(**copy_geometry)
        elif GEOMETRY_TYPE == "grid":
            new_widget.grid(**copy_geometry)

        popup_menu = PopupMenu(self.root)
        new_widget.bind("<Button-3>", lambda event: do_popup(event, popup_menu), add="+")

        duplicate_btn = ctk.CTkButton(popup_menu.frame, text="Duplicate", **BTN_OPTION,
                                      command=lambda: duplicated_widget(self.root, self,
                                                                        new_widget),
                                      image=ICONS["duplicate"])
        duplicate_btn.pack(expand=True, fill="x", padx=10, pady=(10, 0))
        delete_btn = ctk.CTkButton(popup_menu.frame, text="Delete", **BTN_OPTION,
                                   command=lambda: delete_widget(self, new_widget),
                                   image=ICONS["delete"])
        delete_btn.pack(expand=True, fill="x", padx=10, pady=5)
        movetop_btn = ctk.CTkButton(popup_menu.frame, text="Move to Top", **BTN_OPTION,
                                    command=lambda: move_top(new_parent, new_widget),
                                    image=ICONS["move"])
        movetop_btn.pack(expand=True, fill="x", padx=10, pady=5)
        properties_btn = ctk.CTkButton(popup_menu.frame, text="Properties", **BTN_OPTION,
                                       command=lambda: open_properties(self.root, new_widget),
                                       image=ICONS["properties"])
        properties_btn.pack(expand=True, fill="x", padx=10, pady=5)

        self.after(500, old_widget.destroy)

        return new_widget

    @staticmethod
    def update_spinbox(widget, value):
        if value:
            widget.set(value)

    @staticmethod
    def update_optionmenu(widget, value):
        widget.set(value)

    @staticmethod
    def update_entry(widget, value):
        if value:
            widget.insert(0, value)

    @staticmethod
    def update_checkbox(widget, value):
        if value:
            widget.select()
        else:
            widget.deselect()

    def close_frame(self):
        self.grid_forget()


class CoreWidgets(ctk.CTkFrame):
    WIDTH = 300
    HEIGHT = 720

    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs, width=self.WIDTH, height=self.HEIGHT)
        self.root = master
        self.cols_spinbox = None
        self.rows_spinbox = None
        self.colsweight_spinbox = None
        self.rowsweight_spinbox = None
        self.current_frame = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        title = ctk.CTkLabel(self, text="Core Widgets", font=FONTS["large"])
        title.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        self.widget_widgets()

    def widget_widgets(self):
        self.main_frame.grid_columnconfigure(0, weight=1)

        widget_types = ["Button", "CheckBox", "ComboBox", "Entry", "Frame", "Label", "OptionMenu", "ProgressBar",
                        "RadioButton", "Slider", "Switch", "TextBox"]
        for widget_type in widget_types:
            widget = ctk.CTkButton(self.main_frame, text=widget_type, **WIDGET_BTN, image=ICONS[widget_type],
                                   command=lambda name=widget_type.lower(): self.on_click(name))
            widget.grid(sticky="ew", padx=5, pady=5)

    def on_click(self, widget: str):
        widget_map = {
            "button": ctk.CTkButton,
            "checkbox": ctk.CTkCheckBox,
            "combobox": ctk.CTkComboBox,
            "entry": ctk.CTkEntry,
            "frame": ctk.CTkFrame,
            "label": ctk.CTkLabel,
            "optionmenu": ctk.CTkOptionMenu,
            "progressbar": ctk.CTkProgressBar,
            "radiobutton": ctk.CTkRadioButton,
            "slider": ctk.CTkSlider,
            "switch": ctk.CTkSwitch,
            "textbox": ctk.CTkTextbox,
            "scrollableframe": ctk.CTkScrollableFrame,
            "segmentedbutton": ctk.CTkSegmentedButton,
            "tabview": ctk.CTkTabview,
        }

        if widget in widget_map:
            widget_class = widget_map[widget]
            widget_instance = widget_class(self.root.main_frame)
            try:
                widget_instance.configure(font=("Roboto", 13, "normal"))
            except ValueError:
                pass
            if GEOMETRY_TYPE == "grid":
                widget_instance.grid()
            elif GEOMETRY_TYPE == "pack":
                widget_instance.pack()

            if self.current_frame is not None:
                self.current_frame.destroy()

            self.current_frame = WidgetProperties(self.root, widget_instance)
            self.current_frame.grid(row=1, column=2, padx=0, pady=(5, 0), sticky="nsew")

            popup_menu = PopupMenu(self.root)
            widget_instance.bind("<Button-3>", lambda event: do_popup(event, popup_menu), add="+")

            duplicate_btn = ctk.CTkButton(popup_menu.frame, text="Duplicate", **BTN_OPTION,
                                          command=lambda: duplicated_widget(self.root, self.current_frame,
                                                                            widget_instance),
                                          image=ICONS["duplicate"])
            duplicate_btn.pack(expand=True, fill="x", padx=10, pady=(10, 0))
            delete_btn = ctk.CTkButton(popup_menu.frame, text="Delete", **BTN_OPTION,
                                       command=lambda: delete_widget(self.current_frame, widget_instance),
                                       image=ICONS["delete"])
            delete_btn.pack(expand=True, fill="x", padx=10, pady=5)
            movetop_btn = ctk.CTkButton(popup_menu.frame, text="Move to Top", **BTN_OPTION,
                                        command=lambda: move_top(self.root.main_frame, widget_instance),
                                        image=ICONS["move"])
            movetop_btn.pack(expand=True, fill="x", padx=10, pady=5)
            properties_btn = ctk.CTkButton(popup_menu.frame, text="Properties", **BTN_OPTION,
                                           command=lambda: open_properties(self.root, widget_instance),
                                           image=ICONS["properties"])
            properties_btn.pack(expand=True, fill="x", padx=10, pady=5)

    def close_frame(self):
        self.grid_forget()


class CreateNew(ctk.CTkFrame):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.master = master
        self.settings_file = f"{CURRENT_PATH}\\assets\\settings.json"
        default_value = {"recent_projects": []}
        if not os.path.exists(self.settings_file):
            with open(self.settings_file, "w", encoding="UTF-8") as file:
                json.dump(default_value, file, indent=4)

        with open(self.settings_file, "r") as file:
            try:
                settings = json.load(file)
                if not settings:
                    settings = default_value
                    with open(self.settings_file, "w") as f:
                        json.dump(settings, f, indent=4)
            except json.JSONDecodeError:
                settings = default_value
                with open(self.settings_file, "w") as f:
                    json.dump(settings, f, indent=4)

        title = ctk.CTkLabel(self, text="New Project", font=FONTS["title"])
        title.grid(row=0, column=0, sticky="w", padx=100, pady=(20, 0))

        frame = ctk.CTkFrame(self)
        frame.grid(row=1, column=0, sticky="nsew", padx=100, pady=20, columnspan=6)

        setup_label = ctk.CTkLabel(frame, text="Setup", font=FONTS["large"])
        setup_label.grid(row=0, column=0, sticky="w", padx=20, pady=10)

        name_label = ctk.CTkLabel(frame, text="Name:", font=FONTS["normal"])
        name_label.grid(row=1, column=0, sticky="w", padx=20, pady=10)
        self.name_entry = ctk.CTkEntry(frame, width=200)
        self.name_entry.insert(0, "pythonProject")
        self.name_entry.grid(row=1, column=1, sticky="w", padx=20, pady=10)

        location_label = ctk.CTkLabel(frame, text="Location:", font=FONTS["normal"])
        location_label.grid(row=2, column=0, sticky="w", padx=20, pady=(10, 20))
        self.path_entry = ctk.CTkEntry(frame, width=500)
        self.path_entry.insert(0, "C:\\myGUI.json")
        self.path_entry.configure(state="disabled")
        self.path_entry.grid(row=2, column=1, sticky="ew", padx=(20, 10), pady=(10, 20))

        select_btn = ctk.CTkButton(frame, text="",
                                   width=40, image=ICONS["FOLDER"], height=25, hover=False,
                                   command=self.select_folder_callback, **SEC_BTN)
        select_btn.grid(row=2, column=2, sticky="e", padx=(0, 20), pady=(10, 20))

        self.frame2 = ctk.CTkFrame(self)
        self.frame2.grid(row=2, column=0, sticky="nsew", padx=100, pady=20, columnspan=6)

        geometry_label = ctk.CTkLabel(self.frame2, text="Geometry Type", font=FONTS["large"])
        geometry_label.grid(row=0, column=0, sticky="w", padx=20, pady=10)

        self.option_var = ctk.StringVar(value="pack")

        option_2 = ctk.CTkRadioButton(self.frame2, text="Pack", variable=self.option_var, value="pack")
        option_2.grid(row=1, column=0, sticky="w", padx=20, pady=(20, 5))
        option_3 = ctk.CTkRadioButton(self.frame2, text="Grid", variable=self.option_var, value="grid")
        option_3.grid(row=2, column=0, sticky="w", padx=20, pady=(5, 20))

        create_btn = ctk.CTkButton(self, text="Create", command=self.create_callback, height=35)
        create_btn.grid(row=3, column=3, sticky="sw", padx=(0, 5), pady=(20, 40))

        cancel_btn = ctk.CTkButton(self, text="Cancel", command=self.cancel_callback, **SEC_BTN, height=35)
        cancel_btn.grid(row=3, column=4, sticky="se", padx=(5, 40), pady=(20, 40))

    def select_folder_callback(self):
        project_name = self.name_entry.get()
        folder_path = fd.asksaveasfilename(defaultextension="json", filetypes=[("JSON Files", "*.json")],
                                           initialfile=f"{project_name}.json")
        if folder_path:
            self.path_entry.configure(state="normal")
            self.path_entry.delete(0, 'end')
            self.path_entry.insert(0, folder_path)
            self.path_entry.configure(state="disabled")

    def create_callback(self):
        new_title = self.name_entry.get()
        new_path = self.path_entry.get()
        geometry_option = self.option_var.get()
        new_project = {
            "title": new_title,
            "geometry": geometry_option,
            "file_path": new_path
        }
        try:
            with open(self.settings_file, "r") as file:
                load_settings = json.load(file)

            load_settings["recent_projects"].append(new_project)

            with open(self.settings_file, "w") as file:
                json.dump(load_settings, file, indent=4)

        except JSONDecodeError:
            print("Failed to load or save the settings.")

        new_project = {
            "title": new_title,
            "geometry": geometry_option,
            "file_path": new_path,
            "root": {},
            "child": {}
        }

        with open(new_path, "w", encoding="UTF-8") as file:
            json.dump(new_project, file, indent=4)

        for widget in self.master.main_frame.winfo_children():
            widget.destroy()
        self.master.load_project(new_path)
        self.destroy()

    def cancel_callback(self):
        self.destroy()


class CTkBluePrint(ctk.CTk):
    WIDTH = 1440
    HEIGHT = 720

    def __init__(self, project_file):
        super().__init__()
        with open(project_file, "r") as f:
            project = json.load(f)

        self.project_title = project["title"]
        self.project_path = project["file_path"]
        global GEOMETRY_TYPE
        GEOMETRY_TYPE = project["geometry"]

        self.title(f"CTkBluePrint - {self.project_title}")
        self.iconbitmap(LOGO)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)

        center_window(self, self.WIDTH, self.HEIGHT)

        self.main_frame = None
        self.create_layout()

        # self.load_project(project_file)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.menu_widgets()
        self.main_widgets()

        CoreWidgets(master=self, corner_radius=0).grid(row=1, column=0, padx=0, pady=(5, 0), sticky="nsw")

    def menu_widgets(self):
        menu = CTkMenuBar(self, bg_color=("gray90", "gray13"), height=30, width=50, pady=5, padx=5)
        button_1 = menu.add_cascade("File")
        button_2 = menu.add_cascade("Edit")
        button_3 = menu.add_cascade("About")

        dropdown1 = CustomDropdownMenu(widget=button_1)
        dropdown1.add_option(option="New Project", command=self.create_new)
        dropdown1.add_option(option="Open", command=self.open_project_callback)
        dropdown1.add_option(option="Save",
                             command=lambda: self.save_project(self.project_title, GEOMETRY_TYPE, self.project_path))
        dropdown1.add_option(option="Save As", command=self.save_as_callback)
        dropdown1.add_option(option="Export .py", command=self.open_export_window)
        dropdown1.add_separator()
        dropdown1.add_option(option="Close Project", command=lambda: close_project(self))
        dropdown1.add_option(option="Exit", command=self.on_close)

        dropdown2 = CustomDropdownMenu(widget=button_2)
        dropdown2.add_option(option="Preview",
                             command=lambda: preview(self.main_frame, f"Preview - {self.project_title}", "1280x720"))
        dropdown2.add_option(option="Configure Window", command=lambda: ConfigureWindow(self))
        dropdown2.add_option(option="Delete All", command=lambda: delete_all(self.main_frame))

        dropdown3 = CustomDropdownMenu(widget=button_3)
        dropdown3.add_option(option="Github", command=lambda: open_links("https://github.com/iamironman0"))
        dropdown3.add_option(option="Ko-Fi", command=lambda: open_links("https://ko-fi.com/iamironman"))
        dropdown3.add_option(option="Help", command=lambda: open_links("https://github.com/iamironman0"))
        dropdown3.add_option(option="Version (20240120)", hover=False)

    def main_widgets(self):
        self.main_frame = ctk.CTkScrollableFrame(self, label_text="Editor", corner_radius=0, label_font=FONTS["large"],
                                                 fg_color="transparent")
        self.main_frame.grid(row=1, column=1, padx=5, pady=(5, 0), sticky="nsew")
        self.main_frame.place()

    def open_export_window(self):
        ExportWindow(self)

    def save_project(self, title, geometry_type, file_path):
        default_options = load_default()
        root_widgets_code = {}
        child_widgets_code = {}

        def process_widgets(widgets, parent_name, widgets_code):
            for widget in widgets:
                widget_info = get_widget_info(widget, default_options, parent_name)
                widgets_code[widget_info['name']] = generate_code(widget_info)

                if widget_info['name'].startswith("ctkframe"):
                    child_widgets = widget.winfo_children()
                    if child_widgets:
                        process_widgets(child_widgets, widget_info['name'], child_widgets_code)

        widgets = self.main_frame.winfo_children()
        process_widgets(widgets, "self.main_frame", root_widgets_code)

        project = {
            "title": title,
            "geometry": geometry_type,
            "file_path": file_path,
            "root": root_widgets_code,
            "child": child_widgets_code
        }
        with open(file_path, "w") as f:
            json.dump(project, f, indent=4)

    def open_project_callback(self):
        file = fd.askopenfilename(defaultextension="json", filetypes=[("JSON files", "*.json")], parent=self,
                                  title="Open Project")
        if file:
            self.load_project(file)

    def save_as_callback(self):
        file = fd.asksaveasfilename(defaultextension="json", filetypes=[("JSON files", "*.json")], parent=self,
                                    title="Save Project", initialfile=f"{self.project_title}.json")

        if file:
            self.save_project(self.project_title, GEOMETRY_TYPE, file)

    def load_project(self, file):
        with open(file, "r") as f:
            project = json.load(f)

        created_widgets = {'ctk': ctk, "self": self}

        current_frame = WidgetProperties(self)
        current_frame.grid(row=1, column=2, padx=0, pady=(5, 0), sticky="nsew")

        def bind_popup_menu(widget_instance, popup_menu):
            widget_instance.bind("<Button-3>",
                                 lambda event, widget=widget_instance, popup=popup_menu: do_popup(event,
                                                                                                  popup),
                                 add="+")

        def create_button(parent, text, command, image):
            btn = ctk.CTkButton(parent, text=text, **BTN_OPTION, command=command, image=image)
            btn.pack(expand=True, fill="x", padx=10, pady=(10, 5))

        def process_widgets(widgets_code):
            for widget_name, widget_code in widgets_code.items():
                exec(widget_code, created_widgets)
                widget_instance = created_widgets[widget_name]
                current_frame.set_widget(widget_instance)
                popup_menu = PopupMenu(self)
                bind_popup_menu(widget_instance, popup_menu)

                create_button(popup_menu.frame, "Duplicate",
                              lambda widget=widget_instance: duplicated_widget(self, current_frame,
                                                                               widget),
                              ICONS["duplicate"])
                create_button(popup_menu.frame, "Delete",
                              lambda widget=widget_instance: delete_widget(current_frame, widget),
                              ICONS["delete"])
                create_button(popup_menu.frame, "Move to Top",
                              lambda widget=widget_instance: move_top(self.main_frame, widget),
                              ICONS["move"])
                create_button(popup_menu.frame, "Properties",
                              lambda widget=widget_instance: open_properties(self, widget),
                              ICONS["properties"])

        process_widgets(project["root"])
        process_widgets(project["child"])

        self.project_title = project["title"]
        self.project_path = project["file_path"]
        global GEOMETRY_TYPE
        GEOMETRY_TYPE = project["geometry"]
        self.title(f"CTkBluePrint - {self.project_title}")

        current_frame.destroy()

    def create_new(self):
        CreateNew(self, corner_radius=0, fg_color="transparent").grid(row=0, column=0, sticky="nsew", padx=0, pady=0,
                                                                      columnspan=3, rowspan=2)

    def on_close(self):
        self.destroy()


if __name__ == "__main__":
    app = CTkBluePrint("C:/Users/rudyr/Downloads/pythonProject.json")
    app.mainloop()
