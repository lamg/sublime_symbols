import sublime
import sublime_plugin
import json
import os


def enabled_symbol_packages():
    settings = sublime.load_settings("SublimeSymbols.sublime-settings")
    symbol_packages = settings.get("enabled_symbol_packages", [])
    if symbol_packages == None:
        symbol_packages = ["wybe"]

    return symbol_packages


def load_symbol_packages(symbol_packages):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    symbol_packages_dir = os.path.join(current_dir, "packages")
    symbol_map = {}
    for package in symbol_packages:
        file_path = os.path.join(symbol_packages_dir, package + ".json")

        with open(file_path, "r", encoding="utf-8") as f:
            symbol_map = json.load(f)

        for key, value in symbol_map.items():
            symbol_map[key] = value

    return symbol_map


class ReplaceStringCommand(sublime_plugin.TextCommand):
    def run(self, edit, start, end, text):
        self.view.replace(edit, sublime.Region(start, end), text)


class ReplaceListener(sublime_plugin.EventListener):
    def __init__(self):
        enabled = enabled_symbol_packages()
        self.current_map = load_symbol_packages(enabled)

    def on_query_completions(self, view, prefix, locations):
        completions = [
            sublime.CompletionItem(
                k, completion=v, kind=sublime.KIND_SNIPPET, details=v, annotation=v
            )
            for k, v in self.current_map.items()
        ]
        return completions

    def on_modified(self, view: sublime.View):
        sel = view.sel()
        if len(sel) > 0:
            point = sel[0].begin()
            # Get the row and column of the current cursor position
            row, col = view.rowcol(point)

            # Get the line text
            line_region = view.line(point)
            current_line = view.substr(line_region)

            for suffix, replacement in self.current_map.items():
                if current_line.endswith(suffix):
                    view.run_command(
                        "replace_string",
                        {
                            "start": line_region.end() - len(suffix),
                            "end": line_region.end(),
                            "text": replacement,
                        },
                    )
