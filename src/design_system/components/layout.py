import flet as ft
from design_system.tokens.manager import tokens

class DesignSection(ft.Column):
    def __init__(
        self,
        title: str,
        subtitle: str = None,
        controls: list = None,
        dark: bool = False,
        spacing_token: str = "md",
        **kwargs
    ):
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
    def __init__(self, size: str = "md", horizontal: bool = False, **kwargs):
        """A simple token-aware spacer.
        size can be: xs, sm, md, lg, xl, xxl, xxxl
        """
        pixel_size = tokens.get_spacing(size)
        super().__init__(
            width=pixel_size if horizontal else None,
            height=None if horizontal else pixel_size,
            bgcolor="transparent",
            **kwargs
        )
