import shelve
import os
import json

from user_settings.keys import *



username = os.getlogin()
userprofile_path = f"C:\\Users\\{username}"

# Hidden configs
default_config_folder_path = f"{userprofile_path}\\AppData\\Local\\PI_ATE"
default_config_file_path = f"{default_config_folder_path}\\user_settings"
default_config_file_dat =  f"{default_config_file_path}.dat"

def default_config_folder_exists()->bool:
    """Return True if the default settings folder in Appdata exists"""
    if os.path.exists(default_config_folder_path):
        return True
    else:
        create_default_config_folder()
        return False
        
def create_default_config_folder():
    """Create a folder for the default settings in AppData."""
    os.mkdir(default_config_folder_path)

def default_config_file_exists()->bool:
    """Return True if the default settings file in Appdata exists."""
    if os.path.exists(default_config_file_dat):
        return True
    else:
        return False

def get_default_config_file():
    """Return the whole shelf file of the default config."""
    
    with shelve.open(default_config_file_path) as file:
        shelf_file = file
    return shelf_file

def write_to_default_config(key:SaveFileKeys, value):
    """Write a variable to the default config file."""
    with shelve.open(default_config_file_path) as config:
        config[key] = value


def read_from_default_config(key:str, default_value):
    """Read a value from the default config file.
    
    If there is an error while reading, 
    return the default value instead."""
    with shelve.open(default_config_file_path) as config:
        try:
            val = config[key]
        except:
            val = default_value
    
    return val
###############################################################################
# Configs in %USERPROFILE%/Documents
user_settings_path = f"{userprofile_path}\\Documents\\PI_ATE"
line_settings_filepath = f"{user_settings_path}\\line_settings.json"
load_settings_filepath = f"{user_settings_path}\\load_settings.json"
line_ramp_settings_filepath = f"{user_settings_path}\\line_ramp_settings.json"
soak_settings_filepath = f"{user_settings_path}\\soak_settings.json"
test_items_filepath = f"{user_settings_path}\\test_items.json"
i2c_command_list_filepath = f"{user_settings_path}\\i2c_command_list.json"
equipment_setup_filepath = f"{user_settings_path}\\equipment_setup.json"

if not os.path.exists(user_settings_path):
    os.mkdir(user_settings_path)

def save_equipment_setup(config_dict: dict):
    """Save equipment setup to both AppData shelve and user Documents JSON."""
    try:
        write_to_default_config(SaveFileKeys.DEFAULT_EQUIPMENT_SETUP, config_dict)
    except Exception as e:
        print(f"Error saving equipment setup to default config shelve: {e}")
        
    try:
        if not os.path.exists(user_settings_path):
            os.makedirs(user_settings_path, exist_ok=True)
        with open(equipment_setup_filepath, "w") as f:
            json.dump(config_dict, f, indent=4)
    except Exception as e:
        print(f"Error saving equipment setup to JSON: {e}")

def load_equipment_setup():
    """Load equipment setup from JSON file, falling back to AppData shelve."""
    if os.path.exists(equipment_setup_filepath):
        try:
            with open(equipment_setup_filepath, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading equipment setup JSON: {e}")
            
    try:
        config = read_from_default_config(SaveFileKeys.DEFAULT_EQUIPMENT_SETUP, default_value=None)
        if config:
            return config
    except Exception as e:
        print(f"Error reading equipment setup from shelve: {e}")
        
    return None

# TODO: rename
default_config_folder_exists()