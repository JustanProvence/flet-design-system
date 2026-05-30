
import flet as ft
from design_system.tokens.manager import tokens
from design_system.components.typography import (
    HeadingText,
    BodyText,
)
from design_system.components.card import DesignCard
from design_system.components.layout import DesignSpacer


def main(page: ft.Page):
    # Base page settings
    page.title = "Responsive Flet App with Design System"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = tokens.get_color("background", dark=False)

    # State tracker
    state = {
        "dark_mode": False,
    }

    # Helper to resolve colors dynamically based on current mode
    def c(name: str) -> str:
        return tokens.get_color(name, state["dark_mode"])

    # Re-apply page background when theme changes
    def update_theme_background():
        page.bgcolor = c("background")
        page.update()

    def handle_theme_toggle(e):
        state["dark_mode"] = not state["dark_mode"]
        page.theme_mode = ft.ThemeMode.DARK if state["dark_mode"] else ft.ThemeMode.LIGHT

        # Toggle icon
        theme_btn.icon = ft.Icons.LIGHT_MODE_ROUNDED if state["dark_mode"] else ft.Icons.DARK_MODE_ROUNDED
        theme_btn.tooltip = "Switch to Light Mode" if state["dark_mode"] else "Switch to Dark Mode"
        theme_btn.icon_color = c("primary")
        theme_btn.update()

        # Update page and rebuild
        update_theme_background()

        # Also update dynamic colors on header and footer
        top_banner.bgcolor = c("surface")
        top_banner.border = ft.Border.only(bottom=ft.BorderSide(1, c("border")))
        top_banner_title.color = c("text-primary")
        top_banner_nav_home.color = c("text-primary")
        top_banner_nav_about.color = c("text-primary")
        top_banner_nav_services.color = c("text-primary")
        top_banner_nav_contact.color = c("text-primary")
        top_banner.update()

        footer_content.color = c("text-secondary")
        bottom_footer.bgcolor = c("surface")
        bottom_footer.border = ft.Border.only(top=ft.BorderSide(1, c("border")))
        bottom_footer.update()

        # Update sidebar and main content dynamic colors (text, card bg, etc.)
        # For simplicity in this example, we'll rely on component's dark param
        # being passed down or manually updating if needed.
        # A full refresh of the main_content_area would be ideal, but for now,
        # relying on individual components' 'dark' parameter is sufficient.
        main_content_container.content = build_main_content()  # Rebuild content to apply new theme
        main_content_container.update()

        sidebar_container.content = build_sidebar()
        sidebar_container.update()

    theme_btn = ft.IconButton(
        icon=ft.Icons.DARK_MODE_ROUNDED,
        icon_color=c("primary"),
        icon_size=20,
        tooltip="Switch to Dark Mode",
        on_click=handle_theme_toggle,
    )

    # Header Section
    top_banner_title = HeadingText("Responsive App", level=1, dark=state["dark_mode"])
    top_banner_nav_home = BodyText("Home", dark=state["dark_mode"])
    top_banner_nav_about = BodyText("About", dark=state["dark_mode"])
    top_banner_nav_services = BodyText("Services", dark=state["dark_mode"])
    top_banner_nav_contact = BodyText("Contact", dark=state["dark_mode"])

    top_banner = ft.Container(
        content=ft.ResponsiveRow(
            [
                ft.Column(
                    [top_banner_title],
                    col={"xs": 12, "md": 6},
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.TextButton(content=top_banner_nav_home, on_click=lambda e: print("Home clicked")),
                                ft.TextButton(content=top_banner_nav_about, on_click=lambda e: print("About clicked")),
                                ft.TextButton(content=top_banner_nav_services,
                                              on_click=lambda e: print("Services clicked")),
                                ft.TextButton(content=top_banner_nav_contact,
                                              on_click=lambda e: print("Contact clicked")),
                                theme_btn,
                            ],
                            spacing=tokens.get_spacing("sm"),
                            alignment=ft.MainAxisAlignment.END,
                        )
                    ],
                    col={"xs": 12, "md": 6},
                    alignment=ft.MainAxisAlignment.END,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=c("surface"),
        padding=ft.Padding.symmetric(horizontal=tokens.get_spacing("lg"), vertical=tokens.get_spacing("md")),
        border=ft.Border.only(bottom=ft.BorderSide(1, c("border"))),
    )

    # Sidebar Content Builder
    def build_sidebar():
        return ft.Container(
            content=ft.Column(
                [
                    HeadingText("Sidebar", level=2, dark=state["dark_mode"]),
                    BodyText(
                        "This is a sidebar. It will move to the bottom on smaller screens.",
                        size="sm",
                        dark=state["dark_mode"],
                    ),
                    DesignSpacer("sm"),
                    ft.Column(
                        [
                            BodyText("Item 1", dark=state["dark_mode"]),
                            BodyText("Item 2", dark=state["dark_mode"]),
                            BodyText("Item 3", dark=state["dark_mode"]),
                        ],
                        spacing=tokens.get_spacing("xs"),
                    ),
                ],
                spacing=tokens.get_spacing("md"),
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=tokens.get_spacing("lg"),
            bgcolor=c("surface"),
            border_radius=tokens.get_radius("md"),
            border=ft.Border.all(1, c("border")),
            expand=True,
        )

    sidebar_container = ft.Container(
        content=build_sidebar(),
        col={"xs": 12, "md": 4},  # Full width on small, 1/3 on medium/large
        padding=tokens.get_spacing("md"),
    )

    # Main Content Builder
    def build_main_content():
        return ft.Container(
            content=ft.Column(
                [
                    HeadingText("Main Content Area", level=2, dark=state["dark_mode"]),
                    BodyText(
                        "This is the primary content section of our responsive application.",
                        dark=state["dark_mode"],
                    ),
                    DesignSpacer("md"),
                    ft.ResponsiveRow(
                        [
                            ft.Container(
                                content=DesignCard(
                                    content=ft.Column(
                                        [
                                            HeadingText("Feature One", level=3, dark=state["dark_mode"]),
                                            BodyText(
                                                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                                                size="sm",
                                                dark=state["dark_mode"],
                                            ),
                                        ],
                                        spacing=tokens.get_spacing("xs"),
                                    ),
                                    dark=state["dark_mode"],
                                    variant="surface",
                                    interactive=True,
                                ),
                                col={"xs": 12, "sm": 6, "md": 4},
                                padding=tokens.get_spacing("xs"),
                            ),
                            ft.Container(
                                content=DesignCard(
                                    content=ft.Column(
                                        [
                                            HeadingText("Feature Two", level=3, dark=state["dark_mode"]),
                                            BodyText(
                                                "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                                                size="sm",
                                                dark=state["dark_mode"],
                                            ),
                                        ],
                                        spacing=tokens.get_spacing("xs"),
                                    ),
                                    dark=state["dark_mode"],
                                    variant="surface",
                                    interactive=True,
                                ),
                                col={"xs": 12, "sm": 6, "md": 4},
                                padding=tokens.get_spacing("xs"),
                            ),
                            ft.Container(
                                content=DesignCard(
                                    content=ft.Column(
                                        [
                                            HeadingText("Feature Three", level=3, dark=state["dark_mode"]),
                                            BodyText(
                                                "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
                                                size="sm",
                                                dark=state["dark_mode"],
                                            ),
                                        ],
                                        spacing=tokens.get_spacing("xs"),
                                    ),
                                    dark=state["dark_mode"],
                                    variant="surface",
                                    interactive=True,
                                ),
                                col={"xs": 12, "sm": 6, "md": 4},
                                padding=tokens.get_spacing("xs"),
                            ),
                        ],
                        run_spacing={"xs": tokens.get_spacing("sm")},  # Spacing between cards in a row
                        # column_spacing=tokens.get_spacing("sm"), # Spacing between columns in a row
                    ),
                    DesignSpacer("md"),
                    BodyText("More content here to demonstrate layout.", dark=state["dark_mode"]),
                ],
                spacing=tokens.get_spacing("md"),
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=tokens.get_spacing("lg"),
            expand=True,
        )

    main_content_container = ft.Container(
        content=build_main_content(),
        col={"xs": 12, "md": 8},  # Full width on small, 2/3 on medium/large
    )

    # Main Content Area (Sidebar + Main Content)
    main_layout_row = ft.ResponsiveRow(
        [
            sidebar_container,
            main_content_container,
        ],
        spacing=tokens.get_spacing("md"),  # Spacing between sidebar and main content
        run_spacing=tokens.get_spacing("md"),  # Spacing when sidebar wraps below main content
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    # Footer Section
    footer_content = BodyText("© 2023 Responsive Example App", dark=state["dark_mode"])
    bottom_footer = ft.Container(
        content=ft.Row(
            [
                footer_content,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=c("surface"),
        padding=ft.Padding.symmetric(horizontal=tokens.get_spacing("lg"), vertical=tokens.get_spacing("md")),
        border=ft.Border.only(top=ft.BorderSide(1, c("border"))),
    )

    # Core main layout skeleton
    app_layout = ft.Column(
        [
            top_banner,
            ft.Container(
                content=ft.Column([main_layout_row], scroll=ft.ScrollMode.ADAPTIVE),
                padding=ft.Padding.symmetric(horizontal=tokens.get_spacing("lg")),
                expand=True,
                alignment=ft.Alignment.TOP_LEFT,
            ),
            bottom_footer,
        ],
        spacing=0,
        expand=True,
    )

    page.add(app_layout)


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8551)
