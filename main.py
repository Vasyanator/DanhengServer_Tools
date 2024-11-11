# main.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import os
import locale as pylocale  # Renamed to avoid conflict with locales directory
import importlib

from process_handbook import process_handbook

# Import tab classes
import tab_planars_gen
import tab_items
#import tab_spawn
#import tab_mazes
import tab_avatars
import tab_rogue_buffs.rogue_buffs_main as rogue_buffs_main
#import tab_commands
import tab_opencommand

program_name = "DanghengServer Tools"
program_version = "V0.6"

def load_localization():
    lang, encoding = pylocale.getdefaultlocale()
    lang = lang[:2]  # Get two-letter language code
    try:
        localization = importlib.import_module(f"locales.{lang}")
    except ImportError:
        localization = importlib.import_module("locales.en")  # Default to English
    return localization

def main():
    localization = load_localization()
    main_locale = localization.main
    planars_tab_locale = localization.planars_tab
    avatars_tab_locale = localization.avatars_tab
    items_tab_locale = localization.items_tab
    rogue_buffs_tab_locale = localization.rogue_buffs_tab
    spawn_tab_locale = localization.spawn_tab
    mazes_tab_locale = localization.mazes_tab
    commands_tab_locale = localization.commands_tab
    opencommand_tab_locale = localization.opencommand_tab
    # Check if file exists
    filename = "Handbook.txt"
    while True:
        if not os.path.exists(filename):
            # Prompt user to select a file
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            messagebox.showwarning(main_locale['file_not_found_title'],
                                   main_locale['file_not_found_message'].format(filename=filename))
            filename = filedialog.askopenfilename(title=main_locale['select_data_file_title'],
                                                  filetypes=((main_locale['text_files'], "*.txt"),
                                                             (main_locale['all_files'], "*.*")))
            if not filename:
                messagebox.showerror(main_locale['no_file_selected_title'],
                                     main_locale['no_file_selected_message'])
                return
            root.destroy()
        # Read the first line of the file
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
            # Additional check to ensure file is not empty
            if not first_line:
                raise Exception("Empty File")
        except Exception as e:
            # Could not read the file, prompt again
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(main_locale['file_error_title'],
                                 main_locale['file_error_message'].format(filename=filename))
            filename = filedialog.askopenfilename(title=main_locale['select_data_file_title'],
                                                  filetypes=((main_locale['text_files'], "*.txt"),
                                                             (main_locale['all_files'], "*.*")))
            if not filename:
                messagebox.showerror(main_locale['no_file_selected_title'],
                                     main_locale['no_file_selected_message'])
                return
            root.destroy()
            continue

        # Check if first line starts with "# Lunar Core" and ends with "Handbook"
        print(first_line)
        if "Handbook generated in" in first_line:
            # Extract version
            # handbook_version = first_line[len("# Lunar Core"):].strip()
            # if handbook_version.endswith("Handbook"):
                # handbook_version = handbook_version[:-len("Handbook")].strip()
            break
        else:
            # First line does not match, prompt user to select another file
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(main_locale['invalid_file_title'],
                                 main_locale['invalid_file_message'].format(filename=filename))
            filename = filedialog.askopenfilename(title=main_locale['select_data_file_title'],
                                                  filetypes=((main_locale['text_files'], "*.txt"),
                                                             (main_locale['all_files'], "*.*")))
            if not filename:
                messagebox.showerror(main_locale['no_file_selected_title'],
                                     main_locale['no_file_selected_message'])
                return
            root.destroy()

    # Process the file
    handbook_data = process_handbook(filename, program_version)
    avatars_list = handbook_data.avatars_list
    relics_list = handbook_data.relics_list
    rogue_buffs_su = handbook_data.rogue_buffs_su
    rogue_buffs_food = handbook_data.rogue_buffs_food
    rogue_buffs_various = handbook_data.rogue_buffs_various
    rogue_buffs_from_entities = handbook_data.rogue_buffs_from_entities
    rogue_buffs_other = handbook_data.rogue_buffs_other
    rogue_buffs_unknown = handbook_data.rogue_buffs_unknown
    rogue_miracles = handbook_data.rogue_miracles
    # props_list = handbook_data.props_list
    # npc_monsters_list = handbook_data.npc_monsters_list
    # battle_stages = handbook_data.battle_stages
    # battle_monsters_list = handbook_data.battle_monsters_list
    # mazes_list = handbook_data.mazes_list
    lightcones_list = handbook_data.lightcones_list
    materials_list = handbook_data.materials_list
    base_materials_list = handbook_data.base_materials_list
    unknown_items_list = handbook_data.unknown_items_list
    other_items_list = handbook_data.other_items_list

    # Create main application window
    root = tk.Tk()
    root.title(main_locale['window_title'].format(program_name=program_name, program_version=program_version))
    root.state('zoomed')

    # Initialize shared variables
    give_command = tk.StringVar()
    autocopy_var = tk.BooleanVar()
    autocopy_var.set(True)

    # Create the notebook
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Create a CommandManager or similar to handle command updates
    command_manager = CommandManager(root, give_command, autocopy_var, main_locale)

    # Create and add tabs
    tabs = []
    # Relic Generation Tab
    planars_tab = tab_planars_gen.PlanarsTab(notebook, relics_list, command_manager, planars_tab_locale)
    notebook.add(planars_tab.frame, text=main_locale['tab_relic_generation'])
    tabs.append(planars_tab)

    # Items Tab
    items_tab = tab_items.ItemsTab(
        notebook,
        base_materials=base_materials_list,
        lightcones=lightcones_list,
        materials=materials_list,
        other_items=other_items_list,
        unknown_items=unknown_items_list,
        command_manager=command_manager,
        localization=items_tab_locale
    )
    notebook.add(items_tab.frame, text=main_locale['tab_items'])
    tabs.append(items_tab)

    rogue_tab = rogue_buffs_main.RogueBuffsTab(
        notebook, 
        rogue_buffs_su=rogue_buffs_su,
        rogue_buffs_food=rogue_buffs_food,
        rogue_buffs_various=rogue_buffs_various,
        rogue_buffs_from_entities=rogue_buffs_from_entities,
        rogue_buffs_other=rogue_buffs_other,
        rogue_buffs_unknown=rogue_buffs_unknown,
        rogue_miracles=rogue_miracles,
        command_manager=command_manager,
        localization=rogue_buffs_tab_locale,
        
        )
    notebook.add(rogue_tab.frame, text=main_locale['tab_rogue'])
    tabs.append(rogue_tab)

    # Spawn Tab
   # spawn_tab = tab_spawn.SpawnTab(
   #     notebook,
   #     props_list=props_list,
   #     npc_monsters_list=npc_monsters_list,
   #     battle_stages=battle_stages,
   #     battle_monsters_list=battle_monsters_list,
   #     command_manager=command_manager,
   #     localization=spawn_tab_locale
   # )
   # notebook.add(spawn_tab.frame, text=main_locale['tab_spawn'])
   # tabs.append(spawn_tab)

    # Mazes Tab
   # mazes_tab = tab_mazes.MazesTab(notebook, mazes_list, command_manager, mazes_tab_locale)
   # notebook.add(mazes_tab.frame, text=main_locale['tab_mazes'])
   # tabs.append(mazes_tab)

    # Avatars Tab
    avatars_tab = tab_avatars.AvatarsTab(notebook, avatars_list, command_manager, avatars_tab_locale)
    notebook.add(avatars_tab.frame, text=main_locale['tab_avatars'])
    tabs.append(avatars_tab)

    # Commands Tab
   # commands_tab = tab_commands.CommandsTab(notebook, command_manager=command_manager, localization=commands_tab_locale)
   # notebook.add(commands_tab.frame, text=main_locale['tab_commands'])
   # tabs.append(commands_tab)

    # OpenCommand Tab
    opencommand_tab = tab_opencommand.OpenCommandTab(notebook, localization=opencommand_tab_locale)
    notebook.add(opencommand_tab.frame, text=main_locale['tab_opencommand_plugin'])
    tabs.append(opencommand_tab)

    # Command Entry and copy button
    command_frame = tk.Frame(root)
    command_frame.pack(side=tk.BOTTOM, pady=10)

    command_entry = tk.Entry(command_frame, textvariable=give_command, font=('Arial', 12), width=50)
    command_entry.pack()

    # Autocopy checkbox
    autocopy_check = tk.Checkbutton(command_frame, text=main_locale['autocopy_label'], variable=autocopy_var)
    autocopy_check.pack()

    # Copy button
    copy_button = tk.Button(command_frame, text=main_locale['copy_button_label'], command=command_manager.copy_to_clipboard)
    copy_button.pack()

    root.mainloop()

class CommandManager:
    def __init__(self, root, give_command_var, autocopy_var, localization):
        self.root = root
        self.give_command = give_command_var
        self.autocopy_var = autocopy_var
        self.localization = localization

    def update_command(self, command):
        self.give_command.set(command)
        if self.autocopy_var.get():
            self.copy_to_clipboard()

    def copy_to_clipboard(self):
        command = self.give_command.get()
        if command:
            self.root.clipboard_clear()
            self.root.clipboard_append(command)
            self.root.update()  # Now it stays on the clipboard after the window is closed
            if not self.autocopy_var.get():
                messagebox.showinfo(self.localization['copied_title'], self.localization['command_copied_message'])
        else:
            if not self.autocopy_var.get():
                messagebox.showwarning(self.localization['no_command_title'], self.localization['no_command_message'])

if __name__ == '__main__':
    main()
