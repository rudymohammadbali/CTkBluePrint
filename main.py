import json
import os
import subprocess
import sys
import tkinter
import webbrowser
from json.decoder import JSONDecodeError

import customtkinter as ctk
import pyperclip
from PIL import Image
from customtkinter import filedialog as fd

from CTkBlueprint import CTkBluePrint
from assets.widgets.ctk_scrollable_dropdown import CTkScrollableDropdown
from assets.widgets.spinBox import Spinbox

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
LOGO = f"{CURRENT_PATH}\\assets\\icons\\logo.ico"
ICONS = {
    "logo": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\logo.png"),
                         Image.open(f"{CURRENT_PATH}\\assets\\icons\\logo.png"), size=(36, 36)),
    "HELP": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\help_black.png"),
                         Image.open(f"{CURRENT_PATH}\\assets\\icons\\help.png"), size=(24, 24)),
    "DOTS": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\dots_black.png"),
                         Image.open(f"{CURRENT_PATH}\\assets\\icons\\dots.png"), size=(24, 24)),
    "FOLDER": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\folder_black.png"),
                           Image.open(f"{CURRENT_PATH}\\assets\\icons\\folder.png"), size=(20, 20)),

    "support": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\support_black.png"),
                            Image.open(f"{CURRENT_PATH}\\assets\\icons\\support_white.png"), size=(96, 96)),
    "user_manual": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\usermanual_black.png"),
                                Image.open(f"{CURRENT_PATH}\\assets\\icons\\usermanual_white.png"), size=(96, 96)),
    "youtube": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\youtube_black.png"),
                            Image.open(f"{CURRENT_PATH}\\assets\\icons\\youtube_white.png"), size=(96, 96)),
    "doc": ctk.CTkImage(Image.open(f"{CURRENT_PATH}\\assets\\icons\\doc_black.png"),
                        Image.open(f"{CURRENT_PATH}\\assets\\icons\\doc_white.png"), size=(96, 96))
}
FONTS = {
    "title": ("", 18, "bold"),
    "large": ("", 16, "normal"),
    "normal_bold": ("", 14, "bold"),
    "normal": ("", 14, "normal"),
    "small": ("", 12, "normal"),
}
SEC_BTN = {
    "fg_color": "transparent",
    "text_color": ("black", "white"),
    "border_width": 2
}
SIDEBAR_BTN = {
    "width": 260,
    "height": 40,
    "anchor": "w",
    "hover": False,
    "font": FONTS["large"],
    "text_color": ("black", "white")
}
BTN_OPTION = {
    "compound": "left",
    "anchor": "w",
    "fg_color": "transparent",
    "text_color": ("black", "white"),
    "corner_radius": 3
}
LEARN_BTN = {
    "width": 460,
    "height": 250,
    "fg_color": "transparent",
    "border_width": 2,
    "hover_color": ("#EBECF0", "#393B40"),
    "text_color": ("#000000", "#DFE1E5"),
    "compound": "top",
    "font": FONTS["large"]
}


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


def open_explorer(path):
    if os.path.exists(path):
        subprocess.Popen(r'explorer /select,"{}"'.format(path))
    else:
        print(f"Invalid path: '{path}'")


def run_designer(root, file_path):
    for widget in root.winfo_children():
        widget.destroy()
    for job_id in root.tk.call('after', 'info'):
        root.after_cancel(job_id)
    root.destroy()

    run_blueprint = CTkBluePrint(file_path)
    run_blueprint.mainloop()


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

        run_designer(self.master, new_path)

    def cancel_callback(self):
        self.destroy()


class StartPage(ctk.CTk):
    WIDTH = 1280
    HEIGHT = 720

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("Welcome to CTkBlueprint")
        self.iconbitmap(LOGO)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)
        center_window(self, self.WIDTH, self.HEIGHT)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.settings_file = f"{CURRENT_PATH}\\assets\\settings.json"
        self.settings = self.load_settings()
        self.app_settings = self.load_app_settings()

        self.change_appearance()

        self.create_main()

    def create_main(self):
        self.left_frame = ctk.CTkFrame(self, width=300)
        self.right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame1 = ctk.CTkFrame(self.right_frame)
        self.frame2 = ctk.CTkFrame(self.right_frame)

        self.theme_value = ctk.CTkOptionMenu(self.frame1, width=200, height=30)
        CTkScrollableDropdown(self.theme_value, values=["System", "Dark", "Light"])
        self.theme_value.set(self.app_settings.get("theme", "System"))
        self.color_value = ctk.CTkOptionMenu(self.frame1, width=200, height=30)
        CTkScrollableDropdown(self.color_value, values=["Blue", "Dark-Blue", "Green"])
        self.color_value.set(self.app_settings.get("color", "Blue"))
        self.font_value = ctk.CTkOptionMenu(self.frame1, width=200, height=30)
        CTkScrollableDropdown(self.font_value, values=list(tkinter.font.families()), width=250)
        self.font_value.set(self.app_settings.get("font", "Roboto"))
        self.scaling_value = ctk.CTkOptionMenu(self.frame1, width=200, height=30)
        CTkScrollableDropdown(self.scaling_value, values=["80%", "90%", "100%", "110%", "120%"])
        self.scaling_value.set(self.app_settings.get("scaling", "100%"))

        self.left_widgets()
        self.switch_page("projects")

    def left_widgets(self):
        self.left_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsw")
        self.left_frame.grid_rowconfigure(4, weight=1)
        logo_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=(20, 40), sticky="nsew")

        logo = ctk.CTkLabel(logo_frame, text="", image=ICONS["logo"])
        logo.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        logo_label = ctk.CTkLabel(logo_frame, text="CTkBluePrint", font=FONTS["title"])
        logo_label.grid(row=0, column=1, padx=10, pady=0, sticky="ew")
        version = ctk.CTkLabel(logo_frame, text="v2162024", font=FONTS["small"])
        version.grid(row=1, column=0, padx=10, pady=0, sticky="ne", columnspan=2)

        self.project_btn = ctk.CTkButton(self.left_frame, text="Projects",
                                         command=lambda: self.switch_page("projects"), **SIDEBAR_BTN)
        self.project_btn.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew")
        self.customize_btn = ctk.CTkButton(self.left_frame, text="Customize",
                                           command=lambda: self.switch_page("customize"), **SIDEBAR_BTN)
        self.customize_btn.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.learn_btn = ctk.CTkButton(self.left_frame, text="Learn", command=lambda: self.switch_page("learn"),
                                       **SIDEBAR_BTN)
        self.learn_btn.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="ew")

        help_btn = ctk.CTkButton(self.left_frame, text="Help", width=25, fg_color="transparent",
                                 image=ICONS["HELP"],
                                 command=lambda: open_links("https://github.com/iamironman0"), font=FONTS["normal"],
                                 text_color=("black", "white"))
        help_btn.grid(row=4, column=0, padx=20, pady=20, sticky="sew")

    def recent_widget(self):
        self.right_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)
        label = ctk.CTkLabel(self.right_frame, text="Recent", font=FONTS["large"])
        label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 40))
        btn4 = ctk.CTkButton(self.right_frame, text="New Project", command=self.create_new)
        btn4.grid(row=0, column=1, sticky="e", padx=5, pady=(20, 40))
        btn5 = ctk.CTkButton(self.right_frame, text="Open", **SEC_BTN, command=self.open_project)
        btn5.grid(row=0, column=2, sticky="e", padx=(5, 20), pady=(20, 40))

    def create_recent(self):
        self.recent_frame = ctk.CTkScrollableFrame(self.right_frame, fg_color="transparent")
        self.recent_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20, columnspan=3)
        self.recent_frame.grid_columnconfigure(0, weight=1)
        try:
            for project in self.settings["recent_projects"]:
                project_title = project["title"]
                project_geometry = project["geometry"]
                project_path = project["file_path"]

                proj_btn_frame = ctk.CTkFrame(self.recent_frame, height=80)
                proj_btn_frame.grid(sticky="ew", padx=20, pady=5, columnspan=3)
                proj_btn_frame.grid_columnconfigure(0, weight=1)

                project_title_label = ctk.CTkLabel(proj_btn_frame, text=project_title, font=("", 15, "bold"))
                project_title_label.grid(row=0, column=0, sticky='w', padx=20, pady=(10, 0))

                project_geometry_label = ctk.CTkLabel(proj_btn_frame, text=f"Geometry: {project_geometry}")
                project_geometry_label.grid(row=1, column=0, sticky='w', padx=20, pady=2)

                project_file_path_label = ctk.CTkLabel(proj_btn_frame, text=project_path)
                project_file_path_label.grid(row=2, column=0, sticky='w', padx=20, pady=(0, 10))

                options_button = ctk.CTkButton(proj_btn_frame, text='', width=25, image=ICONS["DOTS"],
                                               fg_color="transparent",
                                               hover=False, cursor="hand2")
                options_button.grid(row=0, column=1, rowspan=3, sticky='e', padx=20, pady=0)

                popup_menu = PopupMenu(self)
                options_button.bind("<Button-1>", lambda event, menu=popup_menu: do_popup(event, menu), add="+")

                btn1_menu = ctk.CTkButton(popup_menu.frame, text="Open Selected",
                                          **BTN_OPTION, command=lambda fp=project_path: run_designer(self, fp))
                btn1_menu.pack(expand=True, fill="x", padx=10, pady=(10, 5))
                btn2_menu = ctk.CTkButton(popup_menu.frame, text="Show in Explorer",
                                          command=lambda path=project_path: open_explorer(path), **BTN_OPTION)
                btn2_menu.pack(expand=True, fill="x", padx=10, pady=5)
                btn3_menu = ctk.CTkButton(popup_menu.frame, text="Copy Path",
                                          command=lambda text=project_path: pyperclip.copy(text), **BTN_OPTION)
                btn3_menu.pack(expand=True, fill="x", padx=10, pady=5)
                btn4_menu = ctk.CTkButton(popup_menu.frame, text="Remove from Recent Projects...",
                                          command=lambda title=project_title, path=project_path: self.remove_project(
                                              title, path), **BTN_OPTION)
                btn4_menu.pack(expand=True, fill="x", padx=10, pady=(5, 10))
        except JSONDecodeError as e:
            print(e)

    def customize_widget(self):
        self.right_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(3, weight=1)
        self.frame1.grid(row=1, column=0, sticky="nsew", padx=20, pady=10, columnspan=3)
        self.frame2.grid(row=2, column=0, sticky="nsew", padx=20, pady=10, columnspan=3)

        label = ctk.CTkLabel(self.right_frame, text="Preferences", font=FONTS["large"])
        label.grid(row=0, column=0, sticky="w", padx=20, pady=20)

        title_1 = ctk.CTkLabel(self.frame1, text="Appearance")
        title_1.grid(row=0, column=0, padx=10, pady=(10, 15), sticky="w")
        label_1 = ctk.CTkLabel(self.frame1, text="Theme")
        label_1.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")

        self.theme_value.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        label_2 = ctk.CTkLabel(self.frame1, text="Color")
        label_2.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        self.color_value.grid(row=1, column=3, padx=10, pady=10, sticky="ew")
        self.sync_value = ctk.CTkCheckBox(self.frame1, text="Sync with OS", onvalue=True, offvalue=False, hover=False)
        self.sync_value.grid(row=1, column=4, padx=10, pady=10, sticky="ew")
        if self.app_settings.get("sync", False):
            self.sync_value.select()
            self.theme_value.set("System")
            self.theme_value.configure(state="disabled")
        else:
            self.sync_value.deselect()

        self.sync_value.configure(command=lambda: self.sync_callback(self.sync_value.get()))

        label_3 = ctk.CTkLabel(self.frame1, text="Font")
        label_3.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="w")

        self.font_value.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        label_4 = ctk.CTkLabel(self.frame1, text="Size")
        label_4.grid(row=2, column=2, padx=10, pady=10, sticky="ew")
        self.size_value = Spinbox(self.frame1, min_value=8, max_value=72)
        self.size_value.grid(row=2, column=3, padx=10, pady=10, sticky="ew")
        self.size_value.set(self.app_settings.get("size", 13))

        label_5 = ctk.CTkLabel(self.frame1, text="Scaling")
        label_5.grid(row=3, column=0, padx=(20, 10), pady=(10, 20), sticky="w")

        self.scaling_value.grid(row=3, column=1, padx=10, pady=(10, 20), sticky="ew")

        title_2 = ctk.CTkLabel(self.frame2, text="Project")
        title_2.grid(row=0, column=0, padx=10, pady=(10, 15), sticky="w")
        self.reopen_value = ctk.CTkCheckBox(self.frame2, text="Reopen projects on startup", onvalue=True,
                                            offvalue=False, hover=False)
        self.reopen_value.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")
        if self.app_settings.get("reopen", False):
            self.reopen_value.select()
        else:
            self.reopen_value.deselect()

        self.open_in_value = ctk.StringVar(value=self.app_settings.get("open_in", "Current window"))

        label_6 = ctk.CTkLabel(self.frame2, text="Open project in")
        label_6.grid(row=2, column=0, padx=(20, 10), pady=(10, 20), sticky="w")
        radio_1 = ctk.CTkRadioButton(self.frame2, text="New window", variable=self.open_in_value, value="New window")
        radio_1.grid(row=2, column=1, padx=10, pady=(10, 20), sticky="ew")
        radio_2 = ctk.CTkRadioButton(self.frame2, text="Current window", variable=self.open_in_value,
                                     value="Current window")
        radio_2.grid(row=2, column=2, padx=10, pady=(10, 20), sticky="ew")
        radio_3 = ctk.CTkRadioButton(self.frame2, text="Ask", variable=self.open_in_value, value="Ask")
        radio_3.grid(row=2, column=3, padx=10, pady=(10, 20), sticky="ew")

        save_btn = ctk.CTkButton(self.right_frame, text="Apply", command=self.apply_callback)
        save_btn.grid(row=3, column=0, sticky="se", padx=(20, 5), pady=20)
        reset_btn = ctk.CTkButton(self.right_frame, text="Reset", **SEC_BTN, command=self.reset_callback)
        reset_btn.grid(row=3, column=1, sticky="se", padx=(5, 20), pady=20)

    def learn_widget(self):
        self.right_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.right_frame.grid_columnconfigure(0, weight=0)

        label = ctk.CTkLabel(self.right_frame, text="Learn More", font=FONTS["large"])
        label.grid(row=0, column=0, sticky="w", padx=20, pady=20)

        btn1 = ctk.CTkButton(self.right_frame, text="CTkBluePrint Support", image=ICONS["support"], **LEARN_BTN,
                             command=lambda: open_links(""))
        btn1.grid(row=1, column=0, padx=(20, 10), pady=20, sticky="w")

        btn2 = ctk.CTkButton(self.right_frame, text="User Manual", image=ICONS["user_manual"], **LEARN_BTN,
                             command=lambda: open_links(""))
        btn2.grid(row=1, column=1, padx=10, pady=20, sticky="ew")

        btn3 = ctk.CTkButton(self.right_frame, text="YouTube Tutorial", image=ICONS["youtube"], **LEARN_BTN,
                             command=lambda: open_links(""))
        btn3.grid(row=2, column=0, padx=(20, 10), pady=20, sticky="w")

        btn4 = ctk.CTkButton(self.right_frame, text="CTk Documentation", image=ICONS["doc"], **LEARN_BTN,
                             command=lambda: open_links("https://customtkinter.tomschimansky.com/documentation/"))
        btn4.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    def switch_page(self, page):
        for widgets in self.right_frame.winfo_children():
            widgets.grid_forget()
        self.right_frame.grid_forget()

        self.project_btn.configure(fg_color="transparent", text_color=("black", "white"))
        self.customize_btn.configure(fg_color="transparent", text_color=("black", "white"))
        self.learn_btn.configure(fg_color="transparent", text_color=("black", "white"))

        if page == "projects":
            self.project_btn.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"], text_color="white")
            self.recent_widget()
            self.create_recent()
        elif page == "customize":
            self.customize_btn.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"], text_color="white")
            self.customize_widget()
        elif page == "learn":
            self.learn_btn.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"], text_color="white")
            self.learn_widget()

    def sync_callback(self, value):
        if value:
            self.theme_value.set("System")
            self.theme_value.configure(state="disabled")
        else:
            self.theme_value.configure(state="normal")

    def reset_callback(self):
        data = {
            "theme": "system",
            "color": "blue",
            "sync": False,
            "font": "Roboto",
            "size": 13,
            "scaling": "100%",
            "reopen": False,
            "open_in": "Current window"
        }
        self.app_settings = data
        app_settings = self.load_settings()
        app_settings["app_settings"] = data

        with open(self.settings_file, "w") as file:
            json.dump(app_settings, file, indent=4)

        for widgets in self.winfo_children():
            try:
                widgets.grid_forget()
            except AttributeError:
                pass

        self.change_appearance()
        self.create_main()

    def apply_callback(self):
        get_data = {
            "theme": self.theme_value.get(),
            "color": self.color_value.get(),
            "sync": self.sync_value.get(),
            "font": self.font_value.get(),
            "size": self.size_value.get(),
            "scaling": self.scaling_value.get(),
            "reopen": self.reopen_value.get(),
            "open_in": self.open_in_value.get()
        }

        self.app_settings = get_data
        app_settings = self.load_settings()
        app_settings["app_settings"] = get_data

        with open(self.settings_file, "w") as file:
            json.dump(app_settings, file, indent=4)

        if get_data["sync"]:
            self.theme_value.configure(state="disabled")
        else:
            self.theme_value.configure(state="normal")

        for widgets in self.winfo_children():
            try:
                widgets.grid_forget()
            except AttributeError:
                pass

        self.change_appearance()
        self.create_main()

    def change_appearance(self):
        ctk.set_appearance_mode(self.app_settings["theme"])
        color_theme_files = {
            "blue": f"{CURRENT_PATH}\\assets\\blue.json",
            "dark-blue": f"{CURRENT_PATH}\\assets\\dark_blue.json",
            "green": f"{CURRENT_PATH}\\assets\\green.json"
        }

        color_theme_file = color_theme_files.get(self.app_settings["color"].lower())
        if color_theme_file:
            ctk.set_default_color_theme(color_theme_file)

        new_scaling_float = int(self.app_settings["scaling"].replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def open_project(self):
        file_path = fd.askopenfilename(title="Open Project", filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    settings = json.load(file)
            except Exception as e:
                print(f"Failed to load project file: {e}")
                return

            if not all(key in settings for key in ["title", "geometry", "file_path", "root", "child"]):
                print("Invalid project file")
                return

            new_project = {
                "title": settings["title"],
                "geometry": settings["geometry"],
                "file_path": settings["file_path"]
            }

            for i, existing_project in enumerate(self.settings["recent_projects"]):
                if existing_project["file_path"] == new_project["file_path"]:
                    self.settings["recent_projects"][i] = new_project
                    break
            else:
                self.settings["recent_projects"].append(new_project)

            with open(self.settings_file, "w") as file:
                json.dump(self.settings, file, indent=4)

            run_designer(self, file_path)
        else:
            print("Invalid project file")

    def create_new(self):
        CreateNew(self, corner_radius=0, fg_color="transparent").grid(row=0, column=0, sticky="nsew", padx=0, pady=0,
                                                                      columnspan=2)

    def remove_project(self, title, path):
        self.settings["recent_projects"] = [project for project in self.settings["recent_projects"] if
                                            project["title"] != title and project["file_path"] != path]

        with open(self.settings_file, "w") as file:
            json.dump(self.settings, file, indent=4)

        for widgets in self.recent_frame.winfo_children():
            widgets.destroy()

        self.create_recent()

    def load_app_settings(self):
        settings = self.settings.get("app_settings", {})
        keys = ["theme", "color", "sync", "font", "size", "scaling", "reopen", "open_in"]
        return {key: settings.get(key) for key in keys}

    def load_settings(self):
        default_json = {"recent_projects": [], "app_settings": {
            "theme": "system",
            "color": "blue",
            "sync": False,
            "font": "Roboto",
            "size": 13,
            "scaling": "100%",
            "reopen": True,
            "open_in": "Current window"}}
        settings = default_json

        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as file:
                try:
                    loaded_settings = json.load(file)
                    if loaded_settings:
                        settings = loaded_settings
                except json.JSONDecodeError as e:
                    print(e)

        with open(self.settings_file, "w", encoding="UTF-8") as file:
            json.dump(settings, file, indent=4)

        return settings


if __name__ == "__main__":
    app = StartPage()
    app.mainloop()
