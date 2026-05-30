"""
Unit tests for Flet Token-Driven Design System.

Verifies the state and loading of the TokenManager class, color resolution layer,
spacing scale limits, and custom UI components instantiation.
"""

import pytest
import flet as ft
from design_system.tokens.manager import TokenManager

def test_token_manager_loading():
    manager = TokenManager()
    assert manager is not None
    assert "colors" in manager.global_tokens
    assert "spacing" in manager.global_tokens
    assert "radius" in manager.global_tokens
    assert "typography" in manager.global_tokens

def test_color_resolution():
    manager = TokenManager()
    # Light mode primary resolution (primary -> blue-600 -> #0284C7)
    light_primary = manager.get_color("primary", dark=False)
    assert light_primary == "#0284C7"

    # Dark mode primary resolution (primary -> blue-100 -> #E0F2FE)
    dark_primary = manager.get_color("primary", dark=True)
    assert dark_primary == "#E0F2FE"

    # Direct primitive resolution
    blue_600 = manager.get_color_primitive("blue-600")
    assert blue_600 == "#0284C7"

def test_spacing_and_radius():
    manager = TokenManager()
    assert manager.get_spacing("sm") == 8
    assert manager.get_spacing("md") == 12
    assert manager.get_spacing("xxl") == 32
    assert manager.get_spacing("non_existent") == 0

    assert manager.get_radius("xs") == 4
    assert manager.get_radius("md") == 12
    assert manager.get_radius("full") == 9999

def test_typography():
    manager = TokenManager()
    assert manager.get_font_size("xs") == 12
    assert manager.get_font_size("xxxl") == 32
    
    font_weight_bold = manager.get_font_weight("bold")
    assert font_weight_bold == ft.FontWeight.BOLD

    font_weight_normal = manager.get_font_weight("normal")
    assert font_weight_normal == ft.FontWeight.NORMAL

def test_components_instantiation():
    from design_system.components.typography import DisplayText, HeadingText, BodyText
    from design_system.components.button import DesignButton
    from design_system.components.card import DesignCard
    from design_system.components.input import DesignTextField
    from design_system.components.toggle import DesignSwitch, DesignCheckbox
    from design_system.components.layout import DesignSection, DesignSpacer

    # Instantiations should succeed without TypeError
    assert DisplayText("Hello") is not None
    assert HeadingText("Title") is not None
    assert BodyText("Body") is not None
    assert DesignButton("Click Me", on_click=lambda e: None, icon=ft.Icons.CHECK_CIRCLE) is not None
    assert DesignCard(content=ft.Text("Card")) is not None
    assert DesignTextField(label="Input", hint_text="Enter text", prefix_icon=ft.Icons.LOCK_ROUNDED) is not None
    assert DesignSwitch("Switch") is not None
    assert DesignCheckbox("Checkbox") is not None
    assert DesignSection("Section") is not None
    assert DesignSpacer() is not None

def test_bot_import():
    from design_system.bot.client import bot
    assert bot is not None

def test_all_sidebar_navigation_views(monkeypatch):
    from unittest.mock import MagicMock
    mock_page = MagicMock()
    mock_page.update = lambda: None
    
    # Use monkeypatch to safely override Flet properties during this test only
    monkeypatch.setattr(ft.Control, "update", lambda self: None)
    monkeypatch.setattr(ft.Control, "page", property(lambda self: mock_page))
    
    from design_system.main import main
    
    added_controls = []
    def mock_add(*controls):
        added_controls.extend(controls)
    mock_page.add = mock_add
    
    # Call main
    main(mock_page)
    
    assert len(added_controls) == 1
    main_layout = added_controls[0]
    row_layout = main_layout.controls[1]
    sidebar_col = row_layout.controls[0]
    sidebar_menu = sidebar_col.content.controls[2]
    
    for nav_item in sidebar_menu.controls:
        # Call the on_click handler of each nav_item Container and ensure it executes without errors
        nav_item.on_click(None)

