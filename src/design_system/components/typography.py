import flet as ft
from design_system.tokens.manager import tokens

class BaseText(ft.Text):
    def __init__(
        self,
        value: str,
        size_token: str,
        weight_token: str,
        color_token: str = "text-primary",
        dark: bool = False,
        font_family_token: str = "body",
        italic: bool = False,
        **kwargs
    ):
        super().__init__(
            value=value,
            size=tokens.get_font_size(size_token),
            weight=tokens.get_font_weight(weight_token),
            color=tokens.get_color(color_token, dark),
            font_family=tokens.get_font_family(font_family_token),
            italic=italic,
            **kwargs
        )

class DisplayText(BaseText):
    def __init__(self, value: str, color_token: str = "text-primary", dark: bool = False, **kwargs):
        super().__init__(
            value=value,
            size_token="display",
            weight_token="bold",
            color_token=color_token,
            dark=dark,
            font_family_token="heading",
            **kwargs
        )

class HeadingText(BaseText):
    def __init__(self, value: str, level: int = 1, color_token: str = "text-primary", dark: bool = False, **kwargs):
        size_token = "xxl" if level == 1 else ("xl" if level == 2 else "lg")
        weight_token = "bold" if level == 1 else ("semibold" if level == 2 else "medium")
        super().__init__(
            value=value,
            size_token=size_token,
            weight_token=weight_token,
            color_token=color_token,
            dark=dark,
            font_family_token="heading",
            **kwargs
        )

class SubheadingText(BaseText):
    def __init__(self, value: str, color_token: str = "text-secondary", dark: bool = False, **kwargs):
        super().__init__(
            value=value,
            size_token="md",
            weight_token="medium",
            color_token=color_token,
            dark=dark,
            font_family_token="heading",
            **kwargs
        )

class BodyText(BaseText):
    def __init__(self, value: str, size: str = "md", color_token: str = "text-primary", dark: bool = False, **kwargs):
        # size can be "sm", "md", "lg"
        super().__init__(
            value=value,
            size_token=size,
            weight_token="normal",
            color_token=color_token,
            dark=dark,
            font_family_token="body",
            **kwargs
        )

class CaptionText(BaseText):
    def __init__(self, value: str, color_token: str = "text-secondary", dark: bool = False, **kwargs):
        super().__init__(
            value=value,
            size_token="xs",
            weight_token="normal",
            color_token=color_token,
            dark=dark,
            font_family_token="body",
            **kwargs
        )

class MonospaceText(BaseText):
    def __init__(self, value: str, color_token: str = "text-secondary", dark: bool = False, **kwargs):
        super().__init__(
            value=value,
            size_token="sm",
            weight_token="normal",
            color_token=color_token,
            dark=dark,
            font_family_token="monospace",
            **kwargs
        )
