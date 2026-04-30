import yaml
import os

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance
        
    def load_config(self):
        try:
            # Look for config in absolute or relative path
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "settings.yaml")
            with open(config_path, "r") as f:
                self.settings = yaml.safe_load(f)
        except Exception as e:
            self.settings = {
                "simulation": {"num_agents": 8, "num_impostors": 2, "max_rounds": 5},
                "llm": {"base_url": "http://localhost:11434", "model_name": "mistral", "timeout": 30, "max_retries": 3},
                "game": {"suspicion_decay_rate": 0.05, "kill_cooldown_ticks": 10, "discussion_duration_ticks": 5, "memory_max_observations": 50}
            }

    def get(self, key, default=None):
        keys = key.split('.')
        val = self.settings
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val
