from SpamBot import nora
from SpamBot.plugins import ALL_MODULES
import importlib
import logging

for module in ALL_MODULES:
    imported_module = importlib.import_module("SpamBot.plugins." + module)
    importlib.reload(imported_module)

if __name__ == "__main__":
    nora.run()
