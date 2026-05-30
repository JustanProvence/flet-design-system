"""
Toggle and Selection Components for Flet.

Provides the DesignSwitch and DesignCheckbox classes, establishing standardized
colors and text styles for toggle controls.
"""

import flet as ft
from design_system.tokens.manager import tokens


class DesignSwitch(ft.Switch):
    """
    Token-driven Custom Switch Component.

    Extends ft.Switch to map active/inactive track and thumb colors
    to central design system parameters automatically.
    """

    def __init__(
        self,
        label: str = None,
        value: bool = False,
        dark: bool = False,
        on_change=None,
        **kwargs
    ):
        """
        Initializes a DesignSwitch component.

        Args:
            label (str, optional): Accompanying text label. Defaults to None.
            value (bool, optional): Initial switch state. Defaults to False.
            dark (bool, optional): Theme mode state flag. Defaults to False.
            on_change (function, optional): State change callback handler. Defaults to None.
        """
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
            label_text_style=ft.TextStyle(
                color=text_color,
                size=tokens.get_font_size("md"),
                font_family=tokens.get_font_family("body")
            ),
            **kwargs
        )


class DesignCheckbox(ft.Checkbox):
    """
    Token-driven Custom Checkbox Component.

    Extends ft.Checkbox to map borders and active fill state colors.
    """

    def __init__(
        self,
        label: str = None,
        value: bool = False,
        dark: bool = False,
        on_change=None,
        **kwargs
    ):
        """
        Initializes a DesignCheckbox component.

        Args:
            label (str, optional): Accompanying text label. Defaults to None.
            value (bool, optional): Initial checkbox selected state. Defaults to False.
            dark (bool, optional): Theme mode state flag. Defaults to False.
            on_change (function, optional): State change callback handler. Defaults to None.
        """
        self.dark = dark

        active_color = tokens.get_color("primary", self.dark)
        text_color = tokens.get_color("text-primary", self.dark)

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
