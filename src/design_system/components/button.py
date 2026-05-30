"""
Button Component for Flet.

Provides the DesignButton class, which wraps a Flet Container and builds a highly
reusable, state-aware button responding dynamically to hover and active states.
"""

import flet as ft
from design_system.tokens.manager import tokens

class DesignButton(ft.Container):
    """
    State-aware, token-driven Custom Button component.

    Extends ft.Container to implement rich design system behaviors (hover background transitions,
    border curves, active outline states, and support for contextual icon integration).
    """

    def __init__(
        self,
        text: str,
        on_click,
        variant: str = "primary",  # primary, secondary, outline, text, success, warning, danger
        dark: bool = False,
        disabled: bool = False,
        icon: ft.IconData = None,
        width: int = None,
        height: int = 40,
        **kwargs
    ):
        """
        Initializes a DesignButton component.

        Args:
            text (str): Inner button label string.
            on_click (function): Callback handler triggered on click.
            variant (str, optional): Semantic theme style (e.g., 'primary', 'secondary',
                'outline', 'text', 'success', 'warning', 'danger'). Defaults to 'primary'.
            dark (bool, optional): Theme mode state. Defaults to False.
            disabled (bool, optional): Initial disabled state flag. Defaults to False.
            icon (ft.IconData, optional): Icon enum to display next to the label. Defaults to None.
            width (int, optional): Hardcoded button width. Defaults to None (fluid).
            height (int, optional): Vertical button height. Defaults to 40.
        """
        self.text_val = text
        self.click_handler = on_click
        self.variant = variant
        self.dark = dark
        self.is_disabled = disabled
        self.icon_data = icon
        self.btn_width = width
        self.btn_height = height
        
        # Configure colors based on variant and dark mode
        self._set_colors()
        
        # Setup content (Row with text and optional icon)
        content_items = []
        if self.icon_data:
            content_items.append(
                ft.Icon(
                    self.icon_data,
                    color=self.fg_color,
                    size=16
                )
            )
        content_items.append(
            ft.Text(
                value=self.text_val,
                color=self.fg_color,
                size=tokens.get_font_size("sm"),
                weight=tokens.get_font_weight("semibold"),
                font_family=tokens.get_font_family("body")
            )
        )
        
        super().__init__(
            content=ft.Row(
                content_items,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=tokens.get_spacing("sm"),
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            width=self.btn_width,
            height=self.btn_height,
            bgcolor=self.bg_color,
            border=self.border_style,
            border_radius=tokens.get_radius("md"),
            padding=ft.Padding.symmetric(horizontal=tokens.get_spacing("lg")),
            alignment=ft.Alignment.CENTER,
            on_click=self._handle_click if not self.is_disabled else None,
            on_hover=self._handle_hover if not self.is_disabled else None,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT_QUAD),
            opacity=0.6 if self.is_disabled else 1.0,
            **kwargs
        )

    def _set_colors(self):
        """
        Internal utility mapping button tokens based on the current theme and variant.
        """
        # Default states
        self.border_style = None
        
        if self.variant == "primary":
            self.bg_color = tokens.get_color("primary", self.dark)
            self.hover_bg_color = tokens.get_color("primary-hover", self.dark)
            self.fg_color = tokens.get_color("text-on-primary", self.dark)
            
        elif self.variant == "secondary":
            self.bg_color = tokens.get_color("surface-variant", self.dark)
            # Hover is slightly darker/lighter depending on mode
            self.hover_bg_color = tokens.get_color("border", self.dark)
            self.fg_color = tokens.get_color("text-primary", self.dark)
            
        elif self.variant == "outline":
            self.bg_color = "transparent"
            self.hover_bg_color = tokens.get_color("surface-variant", self.dark)
            self.fg_color = tokens.get_color("primary", self.dark)
            self.border_style = ft.Border.all(1, tokens.get_color("border", self.dark))
            
        elif self.variant == "text":
            self.bg_color = "transparent"
            self.hover_bg_color = tokens.get_color("surface-variant", self.dark)
            self.fg_color = tokens.get_color("primary", self.dark)
            
        elif self.variant == "success":
            self.bg_color = tokens.get_color("success", self.dark)
            self.hover_bg_color = tokens.get_color_primitive("emerald-500") if self.dark else tokens.get_color_primitive("emerald-600")
            self.fg_color = tokens.get_color_primitive("white")
            
        elif self.variant == "warning":
            self.bg_color = tokens.get_color("warning", self.dark)
            self.hover_bg_color = tokens.get_color_primitive("amber-500") if self.dark else tokens.get_color_primitive("amber-600")
            self.fg_color = tokens.get_color_primitive("white") if not self.dark else tokens.get_color_primitive("black")
            
        elif self.variant == "danger":
            self.bg_color = tokens.get_color("danger", self.dark)
            self.hover_bg_color = tokens.get_color_primitive("rose-500") if self.dark else tokens.get_color_primitive("rose-600")
            self.fg_color = tokens.get_color_primitive("white")

    def _handle_hover(self, e):
        """
        Internal event handler managing hover color transitions dynamically.
        """
        if e.data == "true":
            self.bgcolor = self.hover_bg_color
            if self.variant == "outline":
                self.border = ft.Border.all(1, tokens.get_color("primary", self.dark))
        else:
            self.bgcolor = self.bg_color
            if self.variant == "outline":
                self.border = ft.Border.all(1, tokens.get_color("border", self.dark))
        self.update()

    def _handle_click(self, e):
        """
        Internal click callback forwarder.
        """
        if self.click_handler:
            self.click_handler(e)
            
    def set_disabled(self, disabled: bool):
        """
        Updates the button disabled state, opacity, and event handlers.

        Args:
            disabled (bool): Desired disabled state value.
        """
        self.is_disabled = disabled
        self.opacity = 0.6 if disabled else 1.0
        self.on_click = self._handle_click if not disabled else None
        self.on_hover = self._handle_hover if not disabled else None
        self.update()
