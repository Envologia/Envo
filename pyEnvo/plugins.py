# Envo Userbot
# Created by @envologia

import importlib
import os
from pathlib import Path

def load_plugins(envo):
    plugin_path = "plugins"
    for plugin_file in Path(plugin_path).glob("*.py"):
        plugin_name = plugin_file.stem
        try:
            plugin = importlib.import_module(f"{plugin_path}.{plugin_name}")
            if hasattr(plugin, "register"):
                plugin.register(envo)
                print(f"Loaded plugin: {plugin_name}")
        except Exception as e:
            print(f"Failed to load plugin {plugin_name}: {e}")
