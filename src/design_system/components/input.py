"""
TextField Component for Flet.

Provides the DesignTextField class wrapping Flet's TextField and establishing
consistent styling for labels, borders, errors, and custom prefix/suffix icons.
"""

import flet as ft
from design_system.tokens.manager import tokens

class DesignTextField(ft.TextField):
    """
    Token-driven Custom TextField Component.

    Extends ft.TextField to resolve input border colors, active focus colors,
    placeholder hints, and label typographies dynamically.
    """

    def __init__(
        self,
        label: str = None,
        hint_text: str = None,
        dark: bool = False,
        is_password: bool = False,
        can_reveal_password: bool = False,
        error_text: str = None,
        prefix_icon: ft.IconData = None,
        suffix_icon: ft.IconData = None,
        on_change = None,
        on_submit = None,
        **kwargs
    ):
        """
        Initializes a DesignTextField component.

        Args:
            label (str, optional): Floating label text. Defaults to None.
            hint_text (str, optional): Input placeholder hint text. Defaults to None.
            dark (bool, optional): Theme mode state flag. Defaults to False.
            is_password (bool, optional): Mask input values as password text.
                Defaults to False.
            can_reveal_password (bool, optional): Expose eye icon to show password.
                Defaults to False.
            error_text (str, optional): Red-accented error message to display beneath input.
                Defaults to None.
            prefix_icon (ft.IconData, optional): Icon enum to render at start of field.
                Defaults to None.
            suffix_icon (ft.IconData, optional): Icon enum to render at end of field.
                Defaults to None.
            on_change (function, optional): Value changed callback handler. Defaults to None.
            on_submit (function, optional): Field submitted/enter key handler. Defaults to None.
        """
        self.dark = dark
        
        # Resolve theme colors
        border_color = tokens.get_color("border", self.dark)
        focused_border_color = tokens.get_color("primary", self.dark)
        text_color = tokens.get_color("text-primary", self.dark)
        hint_color = tokens.get_color("text-secondary", self.dark)
        
        # Setup icons
        prefix = ft.Icon(name=prefix_icon, color=hint_color, size=18) if prefix_icon else None
        suffix = ft.Icon(name=suffix_icon, color=hint_color, size=18) if suffix_icon else None

        super().__init__(
            label=label,
            hint_text=hint_text,
            password=is_password,
            can_reveal_password=can_reveal_password,
            error_text=error_text,
            prefix=prefix,
            suffix=suffix,
            on_change=on_change,
            on_submit=on_submit,
            
            # Colors
            color=text_color,
            cursor_color=focused_border_color,
            border_color=border_color,
            focused_border_color=focused_border_color,
            hint_style=ft.TextStyle(
                color=hint_color,
                size=tokens.get_font_size("sm"),
                font_family=tokens.get_font_family("body")
            ),
            label_style=ft.TextStyle(
                color=hint_color,
                size=tokens.get_font_size("sm"),
                font_family=tokens.get_font_family("body")
            ),
            text_style=ft.TextStyle(
                size=tokens.get_font_size("md"),
                font_family=tokens.get_font_family("body")
            ),
            
            # Styling
            border_radius=tokens.get_radius("sm"),
            content_padding=tokens.get_spacing("md"),
            bgcolor=tokens.get_color("surface", self.dark),
            filled=True,
            **kwargs
        )
