import sublime
import sublime_plugin
import json
import os

class ReplaceListener(sublime_plugin.EventListener):
    def __init__(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))

        # Define the file path
        file_path = os.path.join(current_dir, 'packages', 'wybe.json')

        with open(file_path, 'r', encoding='utf-8') as f:
            self.current_map = json.load(f)
            

    def on_modified(self, view):
        cursor_pos = view.sel()[0].begin()

        last_two_chars = view.substr(sublime.Region(cursor_pos - 2, cursor_pos))
        
        if last_two_chars in self.current_map.keys():
            view.run_command('undo')
            view.run_command('insert', {'characters': self.current_map[last_two_chars]})