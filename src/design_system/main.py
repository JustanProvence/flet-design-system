"""
Main entry point and documentation application for the Flet Design System.

Defines and launches a highly interactive Flet web application that acts as a
reusable component sandbox, design token visualizer, and documentation hub.
"""

import flet as ft
from design_system.tokens.manager import tokens
from design_system.components.typography import (
    DisplayText,
    HeadingText,
    SubheadingText,
    BodyText,
    CaptionText,
    MonospaceText,
)
from design_system.components.button import DesignButton
from design_system.components.card import DesignCard
from design_system.components.input import DesignTextField
from design_system.components.toggle import DesignSwitch, DesignCheckbox
from design_system.components.layout import DesignSection, DesignSpacer

def main(page: ft.Page):
    # Base page settings
    page.title = "Flet Token-Driven Design System"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = tokens.get_color("background", dark=False)
    
    # State tracker
    state = {
        "active_tab": "welcome",  # welcome, tokens, buttons, cards, inputs, toggles, layouts
        "dark_mode": False,
        # Interactive States
        "btn_disabled": False,
        "btn_click_count": 0,
        "input_value": "",
        "input_error": None,
        "chk_value": False,
        "sw_value": False,
    }

    # Helper to resolve colors dynamically based on current mode
    def c(name: str) -> str:
        return tokens.get_color(name, state["dark_mode"])

    # Re-apply page background when theme changes
    def update_theme_background():
        page.bgcolor = c("background")
        page.update()

    # Shared Component: Code Block with a copy button
    class CodeBlock(ft.Container):
        def __init__(self, code: str):
            self.code_text = code
            super().__init__(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(
                                value=self.code_text,
                                size=13,
                                font_family=tokens.get_font_family("monospace"),
                                color=tokens.get_color_primitive("slate-300"),
                            ),
                            expand=True,
                            padding=12,
                        ),
                        ft.IconButton(
                            icon=ft.icons.COPY_ROUNDED,
                            icon_color=tokens.get_color_primitive("slate-300"),
                            icon_size=16,
                            tooltip="Copy Snippet",
                            on_click=self._copy_code,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=tokens.get_color_primitive("slate-900"),
                border_radius=tokens.get_radius("sm"),
                border=ft.border.all(1, tokens.get_color_primitive("slate-800")),
                margin=ft.margin.only(top=8),
            )

        def _copy_code(self, e):
            page.set_clipboard(self.code_text)
            page.show_snack_bar(
                ft.SnackBar(
                    ft.Text("Snippet copied to clipboard!"),
                    action="OK",
                    duration=1500,
                )
            )

    # Views Builder Functions
    def build_welcome_view():
        return ft.Column(
            [
                DisplayText("Flet Design System", color_token="primary", dark=state["dark_mode"]),
                BodyText(
                    "A professional, production-ready, token-driven design system library built using Flet and Python.",
                    size="lg",
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),
                DesignCard(
                    content=ft.Column(
                        [
                            HeadingText("Key Design System Features", level=2, dark=state["dark_mode"]),
                            DesignSpacer("sm"),
                            ft.Row(
                                [
                                    ft.Icon(ft.icons.TOKEN_ROUNDED, color=c("primary"), size=20),
                                    BodyText("Three-layer design token architecture (Primitive → Semantic → Component)", dark=state["dark_mode"]),
                                ],
                                spacing=8,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(ft.icons.PALETTE_ROUNDED, color=c("primary"), size=20),
                                    BodyText("Native light/dark mode mapping powered by central tokens.json config", dark=state["dark_mode"]),
                                ],
                                spacing=8,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(ft.icons.WIDGETS_ROUNDED, color=c("primary"), size=20),
                                    BodyText("Complete reusable custom UI component library (Buttons, Cards, Inputs, Toggles, etc.)", dark=state["dark_mode"]),
                                ],
                                spacing=8,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(ft.icons.TERMINAL_ROUNDED, color=c("primary"), size=20),
                                    BodyText("Robust project environment setup using Poetry and python-flet", dark=state["dark_mode"]),
                                ],
                                spacing=8,
                            ),
                        ],
                        spacing=8,
                    ),
                    dark=state["dark_mode"],
                ),
                DesignSpacer("lg"),
                HeadingText("Getting Started", level=2, dark=state["dark_mode"]),
                BodyText(
                    "This library defines and uses Design Tokens to maintain strict visual alignment across platforms. All components respond instantly to color palette or sizing adjustments in tokens.json.",
                    dark=state["dark_mode"],
                ),
                DesignSpacer("sm"),
                CodeBlock(
                    "from design_system.tokens.manager import tokens\n"
                    "from design_system.components.button import DesignButton\n\n"
                    "# Accessing token values directly\n"
                    "primary_color = tokens.get_color('primary', dark=False)\n"
                    "button_radius = tokens.get_radius('md')\n\n"
                    "# Using components\n"
                    "button = DesignButton('Click Me', on_click=lambda e: print('Clicked'))"
                ),
            ],
            spacing=16,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def build_tokens_view():
        # Colors visualization
        color_chips = []
        for name, val in tokens.global_tokens["colors"].items():
            color_chips.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                bgcolor=val,
                                height=50,
                                border_radius=tokens.get_radius("xs"),
                                border=ft.border.all(1, c("border")),
                            ),
                            ft.Text(name, size=11, weight="bold", color=c("text-primary")),
                            ft.Text(val, size=10, color=c("text-secondary")),
                        ],
                        spacing=4,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    width=90,
                    bgcolor=c("surface"),
                    padding=8,
                    border_radius=tokens.get_radius("sm"),
                    border=ft.border.all(1, c("border")),
                )
            )

        # Spacing visualization
        spacing_bars = []
        for name, val in tokens.global_tokens["spacing"].items():
            spacing_bars.append(
                ft.Row(
                    [
                        ft.Text(f"{name} ({val}px)", width=100, size=12, weight="semibold", color=c("text-primary")),
                        ft.Container(
                            bgcolor=c("primary"),
                            width=max(val, 2),
                            height=12,
                            border_radius=tokens.get_radius("xs"),
                        ),
                    ],
                    spacing=12,
                )
            )

        # Radius visualization
        radius_boxes = []
        for name, val in tokens.global_tokens["radius"].items():
            radius_boxes.append(
                ft.Container(
                    content=ft.Text(name, size=11, color=tokens.get_color_primitive("white") if state["dark_mode"] else tokens.get_color_primitive("black")),
                    bgcolor=c("primary-container"),
                    width=60,
                    height=60,
                    alignment=ft.alignment.center,
                    border_radius=val,
                    border=ft.border.all(1, c("primary")),
                )
            )

        # Typography scale list
        typo_list = []
        for name, val in tokens.global_tokens["typography"]["font-size"].items():
            typo_list.append(
                ft.Row(
                    [
                        ft.Text(f"{name} ({val}px)", width=110, size=12, weight="bold", color=c("text-primary")),
                        ft.Text("The quick brown fox jumps over the lazy dog", size=val, color=c("text-primary")),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        return ft.Column(
            [
                HeadingText("Design System Tokens", level=1, dark=state["dark_mode"]),
                BodyText(
                    "Our central design tokens configured inside tokens.json. Changing these values automatically scales the entire UI.",
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),
                
                DesignSection(
                    title="1. Brand Colors (Primitives)",
                    subtitle="Central color palette values utilized inside both light and dark themes",
                    controls=[ft.Row(color_chips, wrap=True, spacing=12)],
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),
                
                DesignSection(
                    title="2. Spacing Scale",
                    subtitle="Standardized layout gap values to maintain strict horizontal and vertical alignment",
                    controls=spacing_bars,
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),
                
                DesignSection(
                    title="3. Border Radius Scale",
                    subtitle="Standardized rounding rules across panels, cards, and button states",
                    controls=[ft.Row(radius_boxes, spacing=16)],
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),
                
                DesignSection(
                    title="4. Typography Scale",
                    subtitle="Scalable display, heading, and body typography rules mapped directly from tokens",
                    controls=typo_list,
                    dark=state["dark_mode"],
                ),
            ],
            spacing=16,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def build_buttons_view():
        def on_btn_click(e):
            state["btn_click_count"] += 1
            btn_counter_text.value = f"Click count: {state['btn_click_count']}"
            btn_counter_text.update()

        def toggle_btn_disabled(e):
            state["btn_disabled"] = e.control.value
            primary_btn.set_disabled(state["btn_disabled"])
            secondary_btn.set_disabled(state["btn_disabled"])
            outline_btn.set_disabled(state["btn_disabled"])
            success_btn.set_disabled(state["btn_disabled"])
            danger_btn.set_disabled(state["btn_disabled"])

        # Creating reference instances
        primary_btn = DesignButton("Primary Button", on_click=on_btn_click, variant="primary", dark=state["dark_mode"], disabled=state["btn_disabled"])
        secondary_btn = DesignButton("Secondary Button", on_click=on_btn_click, variant="secondary", dark=state["dark_mode"], disabled=state["btn_disabled"])
        outline_btn = DesignButton("Outline Button", on_click=on_btn_click, variant="outline", dark=state["dark_mode"], disabled=state["btn_disabled"])
        text_btn = DesignButton("Text Button", on_click=on_btn_click, variant="text", dark=state["dark_mode"], disabled=state["btn_disabled"])
        success_btn = DesignButton("Success Button", on_click=on_btn_click, variant="success", dark=state["dark_mode"], disabled=state["btn_disabled"], icon=ft.icons.CHECK_CIRCLE)
        warning_btn = DesignButton("Warning Button", on_click=on_btn_click, variant="warning", dark=state["dark_mode"], disabled=state["btn_disabled"], icon=ft.icons.WARNING_ROUNDED)
        danger_btn = DesignButton("Danger Button", on_click=on_btn_click, variant="danger", dark=state["dark_mode"], disabled=state["btn_disabled"], icon=ft.icons.DELETE_ROUNDED)

        btn_counter_text = ft.Text(f"Click count: {state['btn_click_count']}", weight="bold", color=c("text-primary"))

        return ft.Column(
            [
                HeadingText("Button Component", level=1, dark=state["dark_mode"]),
                BodyText(
                    "Custom styled buttons leveraging theme tokens. Supports multiple context variants, custom icons, disabled states, and fluid hover styling.",
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),
                
                # Interactive Controller Container
                DesignCard(
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.SETTINGS, color=c("primary")),
                            ft.Text("Button Controls:", weight="bold", color=c("text-primary")),
                            DesignCheckbox("Disable Buttons", value=state["btn_disabled"], dark=state["dark_mode"], on_change=toggle_btn_disabled),
                            DesignSpacer("md", horizontal=True),
                            btn_counter_text,
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    dark=state["dark_mode"],
                    variant="variant",
                ),
                DesignSpacer("sm"),

                # Showcase Grid
                DesignSection(
                    title="Live Showcase",
                    subtitle="Interactive grid showing each supported visual variant of DesignButton",
                    controls=[
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text("Primary", size=12, color=c("text-secondary")),
                                        primary_btn,
                                    ]
                                ),
                                ft.Column(
                                    [
                                        ft.Text("Secondary", size=12, color=c("text-secondary")),
                                        secondary_btn,
                                    ]
                                ),
                                ft.Column(
                                    [
                                        ft.Text("Outline", size=12, color=c("text-secondary")),
                                        outline_btn,
                                    ]
                                ),
                                ft.Column(
                                    [
                                        ft.Text("Text Style", size=12, color=c("text-secondary")),
                                        text_btn,
                                    ]
                                ),
                            ],
                            spacing=16,
                            wrap=True,
                        ),
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text("Success Context (with Icon)", size=12, color=c("text-secondary")),
                                        success_btn,
                                    ]
                                ),
                                ft.Column(
                                    [
                                        ft.Text("Warning Context", size=12, color=c("text-secondary")),
                                        warning_btn,
                                    ]
                                ),
                                ft.Column(
                                    [
                                        ft.Text("Danger Context", size=12, color=c("text-secondary")),
                                        danger_btn,
                                    ]
                                ),
                            ],
                            spacing=16,
                            wrap=True,
                        ),
                    ],
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),

                # Code Section
                DesignSection(
                    title="How to use",
                    subtitle="Code snippet representing button implementation",
                    controls=[
                        CodeBlock(
                            "from design_system.components.button import DesignButton\n"
                            "import flet as ft\n\n"
                            "# Create a standard Primary Button\n"
                            "btn1 = DesignButton(\n"
                            "    text='Primary Button',\n"
                            "    on_click=click_handler,\n"
                            "    variant='primary',\n"
                            "    dark=is_dark_mode\n"
                            ")\n\n"
                            "# Create a Success Button with an icon\n"
                            "btn2 = DesignButton(\n"
                            "    text='Save Changes',\n"
                            "    on_click=save_handler,\n"
                            "    variant='success',\n"
                            "    icon=ft.icons.CHECK_CIRCLE,\n"
                            "    dark=is_dark_mode\n"
                            ")"
                        )
                    ],
                    dark=state["dark_mode"],
                ),
            ],
            spacing=16,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def build_cards_view():
        return ft.Column(
            [
                HeadingText("Card Component", level=1, dark=state["dark_mode"]),
                BodyText(
                    "Standard panels to compartmentalize complex page structures. Supports surface (elevated), variant (filled), outline, and interactive hover shadow modes.",
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),

                DesignSection(
                    title="Static Card Variants",
                    subtitle="Standard panel options utilizing colors and rounding tokens",
                    controls=[
                        ft.Row(
                            [
                                DesignCard(
                                    content=ft.Column(
                                        [
                                            HeadingText("Surface Card", level=3, dark=state["dark_mode"]),
                                            BodyText("Elevated box using white or grey-800 backdrop with subtle drop-shadows", size="sm", dark=state["dark_mode"]),
                                        ],
                                        spacing=8,
                                    ),
                                    width=240,
                                    dark=state["dark_mode"],
                                    variant="surface",
                                ),
                                DesignCard(
                                    content=ft.Column(
                                        [
                                            HeadingText("Variant Card", level=3, dark=state["dark_mode"]),
                                            BodyText("Flat panel filled with variant color background, useful for nested layouts", size="sm", dark=state["dark_mode"]),
                                        ],
                                        spacing=8,
                                    ),
                                    width=240,
                                    dark=state["dark_mode"],
                                    variant="variant",
                                ),
                                DesignCard(
                                    content=ft.Column(
                                        [
                                            HeadingText("Outline Card", level=3, dark=state["dark_mode"]),
                                            BodyText("Framed transparent box, elegant inside clear grid interfaces", size="sm", dark=state["dark_mode"]),
                                        ],
                                        spacing=8,
                                    ),
                                    width=240,
                                    dark=state["dark_mode"],
                                    variant="outline",
                                ),
                            ],
                            spacing=16,
                            wrap=True,
                        )
                    ],
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),

                DesignSection(
                    title="Interactive Hover Cards",
                    subtitle="Cards configured to respond visually with lift-on-hover and background-shifting animations",
                    controls=[
                        ft.Row(
                            [
                                DesignCard(
                                    content=ft.Column(
                                        [
                                            ft.Row([ft.Icon(ft.icons.LAUNCH, color=c("primary")), HeadingText("Click Me", level=3, dark=state["dark_mode"])]),
                                            BodyText("Hover over this container to see state transformation and active elevation curves.", size="sm", dark=state["dark_mode"]),
                                        ],
                                        spacing=8,
                                    ),
                                    width=360,
                                    dark=state["dark_mode"],
                                    interactive=True,
                                    on_click=lambda e: page.show_snack_bar(ft.SnackBar(ft.Text("Card clicked!"))),
                                )
                            ],
                            spacing=16,
                        )
                    ],
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),

                DesignSection(
                    title="How to use",
                    subtitle="Implement clean, modular layouts easily",
                    controls=[
                        CodeBlock(
                            "from design_system.components.card import DesignCard\n"
                            "import flet as ft\n\n"
                            "# Normal elevated content container\n"
                            "card = DesignCard(\n"
                            "    content=ft.Text('Content Here'),\n"
                            "    variant='surface',\n"
                            "    dark=is_dark_mode\n"
                            ")\n\n"
                            "# Interactive hover-to-shadow card\n"
                            "clickable_card = DesignCard(\n"
                            "    content=ft.Text('Hover and Click Me!'),\n"
                            "    variant='outline',\n"
                            "    interactive=True,\n"
                            "    on_click=card_clicked,\n"
                            "    dark=is_dark_mode\n"
                            ")"
                        )
                    ],
                    dark=state["dark_mode"],
                ),
            ],
            spacing=16,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def build_inputs_view():
        def handle_text_change(e):
            state["input_value"] = e.control.value
            live_label.value = f"Current Value: '{state['input_value']}'"
            live_label.update()

        def toggle_error(e):
            if e.control.value:
                state["input_error"] = "This is a custom design error message!"
            else:
                state["input_error"] = None
            standard_input.error_text = state["input_error"]
            standard_input.update()

        live_label = ft.Text("Current Value: ''", color=c("text-primary"), weight="bold")
        standard_input = DesignTextField(
            label="Interactive Input",
            hint_text="Type something here...",
            prefix_icon=ft.icons.EDIT_NOTE,
            suffix_icon=ft.icons.KEYBOARD,
            dark=state["dark_mode"],
            on_change=handle_text_change,
        )

        return ft.Column(
            [
                HeadingText("TextField Component", level=1, dark=state["dark_mode"]),
                BodyText(
                    "Standard input forms built with token-driven states (focus, hover, text styles). Offers password masking, helper guidelines, error displays, and custom icons.",
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),

                DesignCard(
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.BUG_REPORT, color=c("primary")),
                            ft.Text("Simulate Input States:", weight="bold", color=c("text-primary")),
                            DesignCheckbox("Trigger Field Error", value=bool(state["input_error"]), dark=state["dark_mode"], on_change=toggle_error),
                            DesignSpacer("md", horizontal=True),
                            live_label,
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    dark=state["dark_mode"],
                    variant="variant",
                ),
                DesignSpacer("sm"),

                DesignSection(
                    title="Live Input Showcases",
                    subtitle="Interactive text boxes styled cleanly to maintain consistent focus states",
                    controls=[
                        ft.Column(
                            [
                                ft.Text("Standard Input Box", size=12, color=c("text-secondary")),
                                standard_input,
                                DesignSpacer("xs"),
                                ft.Text("Password and Masking Field", size=12, color=c("text-secondary")),
                                DesignTextField(
                                    label="Security Key",
                                    hint_text="Enter credentials...",
                                    is_password=True,
                                    can_reveal_password=True,
                                    prefix_icon=ft.icons.LOCK_ROUNDED,
                                    dark=state["dark_mode"],
                                ),
                            ],
                            spacing=12,
                        )
                    ],
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),

                DesignSection(
                    title="How to use",
                    subtitle="Write elegant inputs inside standard form panels",
                    controls=[
                        CodeBlock(
                            "from design_system.components.input import DesignTextField\n"
                            "import flet as ft\n\n"
                            "# Normal text entry field\n"
                            "field1 = DesignTextField(\n"
                            "    label='Full Name',\n"
                            "    hint_text='Enter your first and last name',\n"
                            "    prefix_icon=ft.icons.PERSON_ROUNDED,\n"
                            "    dark=is_dark_mode\n"
                            ")\n\n"
                            "# Masked password field with a reveal eye button\n"
                            "field2 = DesignTextField(\n"
                            "    label='Secret Word',\n"
                            "    is_password=True,\n"
                            "    can_reveal_password=True,\n"
                            "    prefix_icon=ft.icons.LOCK,\n"
                            "    dark=is_dark_mode\n"
                            ")"
                        )
                    ],
                    dark=state["dark_mode"],
                ),
            ],
            spacing=16,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def build_toggles_view():
        def switch_changed(e):
            state["sw_value"] = e.control.value
            switch_status.value = f"Switch state: {state['sw_value']}"
            switch_status.update()

        def checkbox_changed(e):
            state["chk_value"] = e.control.value
            checkbox_status.value = f"Checkbox state: {state['chk_value']}"
            checkbox_status.update()

        switch_status = ft.Text("Switch state: False", color=c("text-primary"), size=13)
        checkbox_status = ft.Text("Checkbox state: False", color=c("text-primary"), size=13)

        return ft.Column(
            [
                HeadingText("Toggles & Selection Controls", level=1, dark=state["dark_mode"]),
                BodyText(
                    "Binary selection toggles (Switches and Checkboxes). Built to cleanly mirror global color values on toggled states.",
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),

                DesignSection(
                    title="Interactive Selection Components",
                    subtitle="Toggles that update their values and styles seamlessly on tap",
                    controls=[
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text("Custom Switch Component", size=12, color=c("text-secondary")),
                                        DesignSwitch("Enable Notification Audio", value=state["sw_value"], dark=state["dark_mode"], on_change=switch_changed),
                                        switch_status,
                                    ],
                                    spacing=8,
                                    horizontal_alignment=ft.CrossAxisAlignment.START,
                                ),
                                DesignSpacer("lg", horizontal=True),
                                ft.Column(
                                    [
                                        ft.Text("Custom Checkbox Component", size=12, color=c("text-secondary")),
                                        DesignCheckbox("Accept System Agreement", value=state["chk_value"], dark=state["dark_mode"], on_change=checkbox_changed),
                                        checkbox_status,
                                    ],
                                    spacing=8,
                                    horizontal_alignment=ft.CrossAxisAlignment.START,
                                ),
                            ],
                            spacing=32,
                            wrap=True,
                        )
                    ],
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),

                DesignSection(
                    title="How to use",
                    subtitle="Easily represent forms or app settings",
                    controls=[
                        CodeBlock(
                            "from design_system.components.toggle import DesignSwitch, DesignCheckbox\n\n"
                            "# Setup toggle switch\n"
                            "sw = DesignSwitch(\n"
                            "    label='Mute System Audio',\n"
                            "    value=False,\n"
                            "    dark=is_dark_mode,\n"
                            "    on_change=audio_handler\n"
                            ")\n\n"
                            "# Setup toggle checkbox\n"
                            "chk = DesignCheckbox(\n"
                            "    label='Subscribe to Newsletter',\n"
                            "    value=True,\n"
                            "    dark=is_dark_mode,\n"
                            "    on_change=news_handler\n"
                            ")"
                        )
                    ],
                    dark=state["dark_mode"],
                ),
            ],
            spacing=16,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def build_layouts_view():
        return ft.Column(
            [
                HeadingText("Layout & Spacer Utilities", level=1, dark=state["dark_mode"]),
                BodyText(
                    "Structural blocks enabling neat section organization, spacing padding, and consistent page flow without raw pixel coding.",
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),

                DesignSection(
                    title="DesignSection Layout Utility",
                    subtitle="Provides a titled divider block for neat and standardized content grouping",
                    controls=[
                        ft.Column(
                            [
                                BodyText("Using DesignSection directly ensures headers and boundaries are perfectly placed.", dark=state["dark_mode"]),
                            ]
                        )
                    ],
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),

                DesignSection(
                    title="DesignSpacer Layout Utility",
                    subtitle="Injects standard spaces. Let's see some spacers visualized",
                    controls=[
                        ft.Column(
                            [
                                ft.Text("Below is a 12px ('md') spacer separating two colored blocks:", size=11, color=c("text-secondary")),
                                ft.Container(bgcolor=c("primary-container"), height=25, alignment=ft.alignment.center, content=ft.Text("Block A", color=c("primary"))),
                                DesignSpacer("md"),
                                ft.Container(bgcolor=c("primary-container"), height=25, alignment=ft.alignment.center, content=ft.Text("Block B", color=c("primary"))),
                                
                                DesignSpacer("lg"),
                                ft.Text("Below is a 32px ('xxl') spacer separating two colored blocks:", size=11, color=c("text-secondary")),
                                ft.Container(bgcolor=c("primary-container"), height=25, alignment=ft.alignment.center, content=ft.Text("Block C", color=c("primary"))),
                                DesignSpacer("xxl"),
                                ft.Container(bgcolor=c("primary-container"), height=25, alignment=ft.alignment.center, content=ft.Text("Block D", color=c("primary"))),
                            ]
                        )
                    ],
                    dark=state["dark_mode"],
                ),
                DesignSpacer("md"),

                DesignSection(
                    title="How to use",
                    subtitle="Never hardcode gaps or standard headers again",
                    controls=[
                        CodeBlock(
                            "from design_system.components.layout import DesignSection, DesignSpacer\n"
                            "import flet as ft\n\n"
                            "# Create a neatly header-separated group of inputs\n"
                            "section = DesignSection(\n"
                            "    title='Profile Information',\n"
                            "    subtitle='Configure your public user profile details',\n"
                            "    controls=[\n"
                            "        field_first_name,\n"
                            "        DesignSpacer('sm'), # standard gap\n"
                            "        field_last_name,\n"
                            "    ],\n"
                            "    dark=is_dark_mode\n"
                            ")"
                        )
                    ],
                    dark=state["dark_mode"],
                ),
            ],
            spacing=16,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    # Core Navigation router
    content_area = ft.Container(
        expand=True,
        padding=tokens.get_spacing("xl"),
        content=build_welcome_view(),
    )

    def navigate_to(tab_name: str):
        state["active_tab"] = tab_name
        
        # Highlight sidebar list item
        for item in sidebar_menu.controls:
            is_active = item.data == tab_name
            item.bgcolor = c("primary-container") if is_active else "transparent"
            item.content.controls[0].color = c("primary") if is_active else c("text-secondary")
            item.content.controls[1].color = c("primary") if is_active else c("text-primary")
            item.content.controls[1].weight = ft.FontWeight.W_600 if is_active else ft.FontWeight.NORMAL
            item.update()

        # Load active view
        if tab_name == "welcome":
            content_area.content = build_welcome_view()
        elif tab_name == "tokens":
            content_area.content = build_tokens_view()
        elif tab_name == "buttons":
            content_area.content = build_buttons_view()
        elif tab_name == "cards":
            content_area.content = build_cards_view()
        elif tab_name == "inputs":
            content_area.content = build_inputs_view()
        elif tab_name == "toggles":
            content_area.content = build_toggles_view()
        elif tab_name == "layouts":
            content_area.content = build_layouts_view()
            
        content_area.update()

    # Rebuild navigation sidebar and layout on theme change
    def rebuild_nav_and_views():
        navigate_to(state["active_tab"])
        # Update top banner colors
        top_banner.bgcolor = c("surface")
        top_banner.border = ft.border.only(bottom=ft.border.BorderSide(1, c("border")))
        top_banner.content.controls[0].controls[1].color = c("text-primary")
        top_banner.content.controls[1].icon_color = c("primary")
        top_banner.update()
        
        # Update sidebar container colors
        sidebar_col.bgcolor = c("surface")
        sidebar_col.border = ft.border.only(right=ft.border.BorderSide(1, c("border")))
        sidebar_col.update()

    def handle_theme_toggle(e):
        state["dark_mode"] = not state["dark_mode"]
        page.theme_mode = ft.ThemeMode.DARK if state["dark_mode"] else ft.ThemeMode.LIGHT
        
        # Toggle icon
        theme_btn.icon = ft.icons.LIGHT_MODE_ROUNDED if state["dark_mode"] else ft.icons.DARK_MODE_ROUNDED
        theme_btn.tooltip = "Switch to Light Mode" if state["dark_mode"] else "Switch to Dark Mode"
        theme_btn.update()
        
        # Update page and rebuild
        update_theme_background()
        rebuild_nav_and_views()

    # Layout Elements Builders
    def make_nav_item(icon: ft.IconData, label: str, data_key: str):
        is_active = (state["active_tab"] == data_key)
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, color=c("primary") if is_active else c("text-secondary"), size=18),
                    ft.Text(label, color=c("primary") if is_active else c("text-primary"), size=13, weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.NORMAL),
                ],
                spacing=12,
            ),
            padding=ft.padding.symmetric(horizontal=12, vertical=10),
            border_radius=tokens.get_radius("sm"),
            bgcolor=c("primary-container") if is_active else "transparent",
            data=data_key,
            on_click=lambda e: navigate_to(data_key),
            on_hover=lambda e: handle_nav_hover(e),
            animate=ft.animation.Animation(150, ft.AnimationCurve.EASE_OUT_QUAD),
        )

    def handle_nav_hover(e):
        if e.control.data == state["active_tab"]:
            return
        if e.data == "true":
            e.control.bgcolor = c("surface-variant")
        else:
            e.control.bgcolor = "transparent"
        e.control.update()

    theme_btn = ft.IconButton(
        icon=ft.icons.DARK_MODE_ROUNDED,
        icon_color=tokens.get_color("primary", dark=False),
        icon_size=20,
        tooltip="Switch to Dark Mode",
        on_click=handle_theme_toggle,
    )

    top_banner = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Icon(ft.icons.DESIGN_SERVICES, color="#0284C7", size=24),
                        ft.Text(
                            "CLAUDE-FLET DESIGN SYSTEM",
                            size=16,
                            weight="bold",
                            color=tokens.get_color("text-primary", dark=False),
                            font_family=tokens.get_font_family("heading"),
                        ),
                        ft.Container(
                            content=ft.Text("v0.1.0", size=10, weight="bold", color="#0284C7"),
                            bgcolor="#E0F2FE",
                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                            border_radius=12,
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                theme_btn,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=tokens.get_color("surface", dark=False),
        padding=ft.padding.symmetric(horizontal=24, vertical=12),
        border=ft.border.only(bottom=ft.border.BorderSide(1, tokens.get_color("border", dark=False))),
    )

    sidebar_menu = ft.Column(
        [
            make_nav_item(ft.icons.INFO_ROUNDED, "Introduction", "welcome"),
            make_nav_item(ft.icons.TOKEN, "Design Tokens", "tokens"),
            make_nav_item(ft.icons.SMART_BUTTON_ROUNDED, "Buttons", "buttons"),
            make_nav_item(ft.icons.CREDIT_CARD_ROUNDED, "Cards", "cards"),
            make_nav_item(ft.icons.INPUT_ROUNDED, "TextFields", "inputs"),
            make_nav_item(ft.icons.TOGGLE_ON_ROUNDED, "Toggles", "toggles"),
            make_nav_item(ft.icons.GRID_VIEW_ROUNDED, "Layout & Spacers", "layouts"),
        ],
        spacing=8,
    )

    sidebar_col = ft.Container(
        content=ft.Column(
            [
                ft.Text("DOCUMENTATION", size=11, weight="bold", color=c("text-secondary")),
                DesignSpacer("xs"),
                sidebar_menu,
            ],
            spacing=8,
        ),
        width=250,
        bgcolor=tokens.get_color("surface", dark=False),
        padding=ft.padding.symmetric(horizontal=16, vertical=24),
        border=ft.border.only(right=ft.border.BorderSide(1, tokens.get_color("border", dark=False))),
    )

    # Core main layout skeleton
    main_layout = ft.Column(
        [
            top_banner,
            ft.Row(
                [
                    sidebar_col,
                    content_area,
                ],
                expand=True,
                spacing=0,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
        ],
        spacing=0,
        expand=True,
    )

    page.add(main_layout)

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550)
