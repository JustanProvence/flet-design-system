import flet as ft
from design_system.tokens.manager import tokens

class DesignCard(ft.Container):
    def __init__(
        self,
        content: ft.Control,
        dark: bool = False,
        variant: str = "surface",  # surface, variant, outline
        padding_token: str = "lg",
        radius_token: str = "md",
        interactive: bool = False,
        on_click = None,
        **kwargs
    ):
        self.dark = dark
        self.variant = variant
        self.interactive = interactive
        self.click_handler = on_click
        
        # Determine background and border
        self._set_styles()
        
        # Elevation/Shadow config
        shadow_style = None
        if not interactive and variant == "surface":
            # Subtle default shadow for elevated standard cards
            shadow_style = ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color="#0D000000" if not dark else "#1A000000",
                offset=ft.Offset(0, 2),
            )

        super().__init__(
            content=content,
            bgcolor=self.bg_color,
            border=self.border_style,
            border_radius=tokens.get_radius(radius_token),
            padding=tokens.get_spacing(padding_token),
            shadow=shadow_style,
            on_click=self._handle_click if interactive else None,
            on_hover=self._handle_hover if interactive else None,
            animate=ft.animation.Animation(150, ft.AnimationCurve.EASE_OUT_QUAD) if interactive else None,
            **kwargs
        )

    def _set_styles(self):
        if self.variant == "surface":
            self.bg_color = tokens.get_color("surface", self.dark)
            self.border_style = None
            self.hover_bg_color = tokens.get_color("surface-variant", self.dark)
        elif self.variant == "variant":
            self.bg_color = tokens.get_color("surface-variant", self.dark)
            self.border_style = None
            self.hover_bg_color = tokens.get_color("border", self.dark)
        elif self.variant == "outline":
            self.bg_color = "transparent"
            self.border_style = ft.border.all(1, tokens.get_color("border", self.dark))
            self.hover_bg_color = tokens.get_color("surface-variant", self.dark)

    def _handle_hover(self, e):
        if e.data == "true":
            self.bgcolor = self.hover_bg_color
            self.shadow = ft.BoxShadow(
                spread_radius=1,
                blur_radius=12,
                color="#1F000000" if not self.dark else "#2A000000",
                offset=ft.Offset(0, 4),
            )
        else:
            self.bgcolor = self.bg_color
            self.shadow = None
        self.update()

    def _handle_click(self, e):
        if self.click_handler:
            self.click_handler(e)
