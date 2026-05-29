"""
Design Tokens Manager for Flet.

Provides the TokenManager class to load, parse, and resolve global primitive
and theme-specific semantic/component design tokens from a central JSON file.
"""

import os
import json
import flet as ft

class TokenManager:
    """
    Manages and resolves three-layer design tokens.

    Loads raw design token specifications from a JSON file and dynamically resolves
    semantic color lookups based on active theme states (light/dark mode) as well
    as layout spacing, corner border-radiuses, and typography configurations.
    """

    def __init__(self, json_path=None):
        """
        Initializes the TokenManager and loads design token dictionary.

        Args:
            json_path (str, optional): Absolute path to the tokens JSON file.
                Defaults to locating 'tokens.json' in the same directory.
        """
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
        """
        Returns raw primitive hex code, or name itself if not found.

        Args:
            name (str): Key of the primitive color (e.g., 'blue-600').

        Returns:
            str: Resolved hex color string or fallback.
        """
        return self.global_tokens["colors"].get(name, name)
        
    def get_color(self, name: str, dark: bool = False) -> str:
        """
        Resolves a semantic color name to a primitive hex color code.

        Checks the active theme context, resolves the mapped primitive value,
        and falls back to primitive color direct matching if no semantic match exists.

        Args:
            name (str): Semantic color name (e.g., 'primary', 'surface').
            dark (bool): Active dark mode state flags.

        Returns:
            str: Hex color string.
        """
        theme_dict = self.dark_tokens if dark else self.light_tokens
        
        # Check semantic colors first
        val = theme_dict["colors"].get(name)
        if val is not None:
            return self.get_color_primitive(val)
            
        # Fallback to primitive color directly if specified as a primitive
        return self.get_color_primitive(name)
        
    def get_spacing(self, name: str) -> int:
        """
        Returns a layout spacing value in pixels.

        Args:
            name (str): Spacing key (e.g., 'xs', 'md', 'xl').

        Returns:
            int: Size of the gap in pixels.
        """
        return self.global_tokens["spacing"].get(name, 0)
        
    def get_radius(self, name: str) -> int:
        """
        Returns a border-radius value in pixels.

        Args:
            name (str): Border radius key (e.g., 'xs', 'md', 'full').

        Returns:
            int: Border rounding radius in pixels.
        """
        return self.global_tokens["radius"].get(name, 0)
        
    def get_font_family(self, name: str) -> str:
        """
        Returns a font family string.

        Args:
            name (str): Font family key ('heading', 'body', 'monospace').

        Returns:
            str: Fallback system-safe font family string.
        """
        return self.global_tokens["typography"]["font-family"].get(name, "System-UI")
        
    def get_font_size(self, name: str) -> int:
        """
        Returns a typography font size in pixels.

        Args:
            name (str): Font size scale key (e.g., 'xs', 'md', 'display').

        Returns:
            int: Font size in pixels.
        """
        return self.global_tokens["typography"]["font-size"].get(name, 14)
        
    def get_font_weight(self, name: str) -> ft.FontWeight:
        """
        Returns the Flet Font Weight enum corresponding to the scale token.

        Args:
            name (str): Font weight key (e.g., 'normal', 'semibold', 'bold').

        Returns:
            ft.FontWeight: Matching Flet FontWeight constant.
        """
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
