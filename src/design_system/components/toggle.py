import flet as ft
from design_system.tokens.manager import tokens

class DesignSwitch(ft.Switch):
    def __init__(
        self,
        label: str = None,
        value: bool = False,
        dark: bool = False,
        on_change = None,
        **kwargs
    ):
        self.dark = dark
        
        # Color resolution
        active_color = tokens.get_color("primary", self.dark)
        active_track_color = tokens.get_color("primary-container", self.dark)
        inactive_thumb_color = tokens.get_color("text-secondary", self.dark)
        inactive_track_color = tokens.get_color("border", self.dark)
        text_color = tokens.get_color("text-primary", self.dark)

        super().__init__(
            label=label,
            value=value,
            on_change=on_change,
            active_color=active_color,
            active_track_color=active_track_color,
            inactive_thumb_color=inactive_thumb_color,
            inactive_track_color=inactive_track_color,
            label_style=ft.TextStyle(
                color=text_color,
                size=tokens.get_font_size("md"),
                font_family=tokens.get_font_family("body")
            ),
            **kwargs
        )


class DesignCheckbox(ft.Checkbox):
    def __init__(
        self,
        label: str = None,
        value: bool = False,
        dark: bool = False,
        on_change = None,
        **kwargs
    ):
        self.dark = dark
        
        active_color = tokens.get_color("primary", self.dark)
        text_color = tokens.get_color("text-primary", self.dark)
        border_color = tokens.get_color("border", self.dark)

        super().__init__(
            label=label,
            value=value,
            on_change=on_change,
            active_color=active_color,
            fill_color={
                ft.ControlState.DEFAULT: "transparent",
                ft.ControlState.SELECTED: active_color,
            },
            check_color=tokens.get_color("text-on-primary", self.dark),
            label_style=ft.TextStyle(
                color=text_color,
                size=tokens.get_font_size("md"),
                font_family=tokens.get_font_family("body")
            ),
            # Border styling isn't fully exposed in older Flet, but we configure standard attributes
            **kwargs
        )
