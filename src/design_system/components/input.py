import flet as ft
from design_system.tokens.manager import tokens

class DesignTextField(ft.TextField):
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
