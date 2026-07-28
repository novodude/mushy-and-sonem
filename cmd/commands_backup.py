import importlib
import os

def get_command_modules():
    """Dynamically import all command modules in the cmd/ directory."""
    command_modules = []
    for filename in os.listdir("cmd"):
        if filename.endswith(".py") and filename != "__init__.py" and filename != "commands.py":
            module_name = f"cmd.{filename[:-3]}"
            command_modules.append(module_name)
    return command_modules

async def commands_setup(bot):
    """Load all command modules and run their setup functions."""
    command_modules = get_command_modules()
    for module_name in command_modules:
        module = importlib.import_module(module_name)
        setup_func_name = f"{module_name.split('.')[-1]}_setup"
        if hasattr(module, setup_func_name):
            await getattr(module, setup_func_name)(bot)