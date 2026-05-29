import os
import json
import flet as ft

class TokenManager:
    def __init__(self, json_path=None):
        if json_path is None:
            # Locate tokens.json relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(current_dir, "tokens.json")
            
        with open(json_path, "r") as f:
            self._data = json.load(f)
            
        self.global_tokens = self._data["global"]
        self.light_tokens = self._data["light"]
        self.dark_tokens = self._data["dark"]
        
    def get_color_primitive(self, name: str) -> str:
        """Returns raw primitive hex code, or name itself if it is already hex or not found."""
        return self.global_tokens["colors"].get(name, name)
        
    def get_color(self, name: str, dark: bool = False) -> str:
        """Resolves a semantic color name to a primitive hex color code."""
        theme_dict = self.dark_tokens if dark else self.light_tokens
        
        # Check semantic colors first
        val = theme_dict["colors"].get(name)
        if val is not None:
            return self.get_color_primitive(val)
            
        # Fallback to primitive color directly if specified as a primitive
        return self.get_color_primitive(name)
        
    def get_spacing(self, name: str) -> int:
        """Returns spacing value in pixels."""
        return self.global_tokens["spacing"].get(name, 0)
        
    def get_radius(self, name: str) -> int:
        """Returns border-radius value in pixels."""
        return self.global_tokens["radius"].get(name, 0)
        
    def get_font_family(self, name: str) -> str:
        """Returns font family string."""
        return self.global_tokens["typography"]["font-family"].get(name, "System-UI")
        
    def get_font_size(self, name: str) -> int:
        """Returns font size in pixels."""
        return self.global_tokens["typography"]["font-size"].get(name, 14)
        
    def get_font_weight(self, name: str) -> ft.FontWeight:
        """Returns Flet Font Weight enum."""
        val = self.global_tokens["typography"]["font-weight"].get(name, "normal")
        # Map string keys to Flet FontWeight constants
        mapping = {
            "light": ft.FontWeight.W_300,
            "normal": ft.FontWeight.NORMAL,
            "medium": ft.FontWeight.W_500,
            "semibold": ft.FontWeight.W_600,
            "bold": ft.FontWeight.BOLD
        }
        return mapping.get(val, ft.FontWeight.NORMAL)

# Instantiated default token manager for import simplicity
tokens = TokenManager()
