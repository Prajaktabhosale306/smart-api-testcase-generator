import json
from typing import Any, Dict

class ProjectConfig:
    def __init__(self, config_file="project_config.json"):
        """
        Initializes the ProjectConfig object and loads the configuration from the specified file.
        """
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """
        Loads the configuration from the config file. If the file doesn't exist, returns default settings.
        """
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.get_default_config()

    def get_default_config(self) -> Dict[str, Any]:
        """
        Returns the default configuration if the config file doesn't exist.
        """
        return {
            "use_nlp": True,
            "nlp_engine": "basic",  # "basic" or "premium"
            "save_path": "./test_cases",
            "load_path": None
        }

    def save_config(self) -> None:
        """
        Saves the current configuration to the config file.
        """
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def set_config(self, key: str, value: Any) -> None:
        """
        Sets a configuration key-value pair.
        """
        self.config[key] = value
        self.save_config()

    def get_config(self, key: str) -> Any:
        """
        Gets the value of a configuration key.
        """
        return self.config.get(key)
