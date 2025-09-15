import importlib
from pathlib import Path

dynamic_prompts = []


def prompt_plugin(func):
    dynamic_prompts.append(func)
    return func


class PluginManager:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins = {}

    def load_plugins(self):
        for file in self.plugin_dir.glob("*.py"):
            if file.name == "__init__.py":
                continue

            mod_name = file.stem
            try:
                mod = importlib.import_module(f"{mod_name}")
                info = getattr(mod, "info", lambda: {"map": mod_name})()
                key = info.get("map", mod_name)
                self.plugins[key] = mod
                if hasattr(mod, "init"):
                    mod.init()
            except Exception as e:
                print(f"[!] Failed to load {mod_name}: {e}")

    def exit_plugins(self):
        for key, mod in self.plugins.items():
            if hasattr(mod, "exit"):
                try:
                    mod.exit()
                except Exception as e:
                    print(f"[!] Plugin {key} exit() failed: {e}")

    def get_plugin(self, key):
        return self.plugins[key]

    def get_plugins(self):
        return self.plugins.values()
