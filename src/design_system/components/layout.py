"""
Layout and Utility Components for Flet.

Provides structural building blocks like DesignSection (for grouping sections)
and DesignSpacer (for standardized horizontal and vertical layout gaps).
"""

import flet as ft
from design_system.tokens.manager import tokens

class DesignSection(ft.Column):
    """
    Token-driven Custom Layout Section Component.

    Extends ft.Column to establish a standardized, titled layout divider section,
    consistent headers, optional secondary subtitles, and proper spacing hierarchies.
    """

    def __init__(
        self,
        title: str,
        subtitle: str = None,
        controls: list = None,
        dark: bool = False,
        spacing_token: str = "md",
        **kwargs
    ):
        """
        Initializes a DesignSection layout block.

        Args:
            title (str): Bold section header title text.
            subtitle (str, optional): Smaller secondary descriptive caption text. Defaults to None.
            controls (list, optional): Content child controls to host in the section list.
                Defaults to None.
            dark (bool, optional): Theme mode state flag. Defaults to False.
            spacing_token (str, optional): Standard spacing token for spacing inside children.
                Defaults to 'md'.
        """
        self.dark = dark
        
        # Build section header
        header_controls = [
            ft.Text(
                value=title,
                size=tokens.get_font_size("lg"),
                weight=tokens.get_font_weight("bold"),
                color=tokens.get_color("text-primary", self.dark),
                font_family=tokens.get_font_family("heading"),
            )
        ]
        
        if subtitle:
            header_controls.append(
                ft.Text(
                    value=subtitle,
                    size=tokens.get_font_size("sm"),
                    color=tokens.get_color("text-secondary", self.dark),
                    font_family=tokens.get_font_family("body"),
                )
            )
            
        header = ft.Column(
            header_controls,
            spacing=tokens.get_spacing("xs"),
        )
        
        # Merge section header with content controls
        all_controls = [
            header,
            ft.Divider(height=1, color=tokens.get_color("border", self.dark)),
        ]
        
        if controls:
            all_controls.append(
                ft.Column(
                    controls,
                    spacing=tokens.get_spacing(spacing_token),
                )
            )
            
        super().__init__(
            controls=all_controls,
            spacing=tokens.get_spacing("md"),
            **kwargs
        )


class DesignSpacer(ft.Container):
    """
    Token-aware Standard Layout Spacer Component.

    Extends ft.Container to inject transparent padding space dynamically scaled to spacing tokens.
    """

    def __init__(self, size: str = "md", horizontal: bool = False, **kwargs):
        """
        Initializes a DesignSpacer layout gap.

        Args:
            size (str, optional): Spacing token key ('xs', 'sm', 'md', 'lg', 'xl', 'xxl', 'xxxl').
                Defaults to 'md'.
            horizontal (bool, optional): Creates horizontal gap if True, vertical gap if False.
                Defaults to False.
        """
        pixel_size = tokens.get_spacing(size)
        super().__init__(
            width=pixel_size if horizontal else None,
            height=None if horizontal else pixel_size,
            bgcolor="transparent",
            **kwargs
        )
