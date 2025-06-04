# xolo/core/utils.py
import yaml
from pathlib import Path

def load_config():

    """
    This function loads the config file and returns it as a dictionary to
    use the Variables as a GLOBAL VARIABLES to use in other modules and launchers

    """
    config_path = Path(__file__).resolve().parent.parent.parent / "config.yaml"
    with config_path.open("r") as f:
        return yaml.safe_load(f)
