"""
Typography Custom Components for Flet.

Implements token-aware typography text blocks including DisplayText, HeadingText,
SubheadingText, BodyText, CaptionText, and MonospaceText components.
"""

import flet as ft
from design_system.tokens.manager import tokens


class BaseText(ft.Text):
    """
    Base token-aware text class extending ft.Text.

    Automatically resolves typography design tokens such as font-size,
    font-weight, and color depending on the provided token names and theme context.
    """

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
        """
        Initializes a BaseText component.

        Args:
            value (str): Inner text content.
            size_token (str): Typography scale size key (e.g., 'sm', 'lg').
            weight_token (str): Typography scale weight key (e.g., 'semibold').
            color_token (str, optional): Semantic color token. Defaults to 'text-primary'.
            dark (bool, optional): Active theme mode state. Defaults to False.
            font_family_token (str, optional): Font family token ('body', 'heading').
                Defaults to 'body'.
            italic (bool, optional): Whether text renders italic. Defaults to False.
        """
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
    """Display-sized big text for banners or page heroes."""

    def __init__(self, value: str, color_token: str = "text-primary", dark: bool = False, **kwargs):
        """
        Initializes DisplayText component.

        Args:
            value (str): Text content.
            color_token (str, optional): Semantic color token. Defaults to 'text-primary'.
            dark (bool, optional): Theme mode state. Defaults to False.
        """
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
    """Heading text component supporting multiple logical level weights (H1, H2, H3)."""

    def __init__(self, value: str, level: int = 1, color_token: str = "text-primary", dark: bool = False, **kwargs):
        """
        Initializes HeadingText component.

        Args:
            value (str): Text content.
            level (int, optional): Heading hierarchical level (1 = H1, 2 = H2, 3 = H3).
                Defaults to 1.
            color_token (str, optional): Semantic color token. Defaults to 'text-primary'.
            dark (bool, optional): Theme mode state. Defaults to False.
        """
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
    """Medium-weight heading text, ideal for section or subtitle descriptors."""

    def __init__(self, value: str, color_token: str = "text-secondary", dark: bool = False, **kwargs):
        """
        Initializes SubheadingText component.

        Args:
            value (str): Text content.
            color_token (str, optional): Semantic color token. Defaults to 'text-secondary'.
            dark (bool, optional): Theme mode state. Defaults to False.
        """
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
    """Standard copy and paragraph text block."""

    def __init__(self, value: str, size: str = "md", color_token: str = "text-primary", dark: bool = False, **kwargs):
        """
        Initializes BodyText component.

        Args:
            value (str): Text content.
            size (str, optional): Typography scale size ('sm', 'md', 'lg'). Defaults to 'md'.
            color_token (str, optional): Semantic color token. Defaults to 'text-primary'.
            dark (bool, optional): Theme mode state. Defaults to False.
        """
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
    """Extra-small text block ideal for auxiliary data, footers, or sub-labels."""

    def __init__(self, value: str, color_token: str = "text-secondary", dark: bool = False, **kwargs):
        """
        Initializes CaptionText component.

        Args:
            value (str): Text content.
            color_token (str, optional): Semantic color token. Defaults to 'text-secondary'.
            dark (bool, optional): Theme mode state. Defaults to False.
        """
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
    """Code-aligned, monospace-family text block, perfect for syntax blocks."""

    def __init__(self, value: str, color_token: str = "text-secondary", dark: bool = False, **kwargs):
        """
        Initializes MonospaceText component.

        Args:
            value (str): Text content.
            color_token (str, optional): Semantic color token. Defaults to 'text-secondary'.
            dark (bool, optional): Theme mode state. Defaults to False.
        """
        super().__init__(
            value=value,
            size_token="sm",
            weight_token="normal",
            color_token=color_token,
            dark=dark,
            font_family_token="monospace",
            **kwargs
        )
