from kivy.uix.gridlayout import GridLayout
from books_page import BooksPage
from kivy.uix.button import Button
from kivy.uix.image import Image


class _DummyPage:
    def __init__(self, readable_name, icon_path):
        self.page_name = None
        self.readable_name = readable_name
        self.icon_path = icon_path


class MainPage(GridLayout):
    page_name = "main"
    readable_name = "Ana Sayfa"

    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.row_force_default = True
        self.row_default_height = 100
        self.spacing = (10, 10)
        self.padding = (40, 20)
        self.cols = 1
        self.screen_manager = screen_manager
        pages = [
            BooksPage,
            _DummyPage(
                readable_name="Çeviri (Yakında...)", icon_path="static/translation.png"
            ),
        ]
        for page in pages:
            btn_layout = GridLayout(spacing=(10, 10))
            btn_layout.cols = 2
            page_btn = Button(text=page.readable_name, color=(0, 0, 0, 1))
            btn_icon = Image(source=page.icon_path, size_hint=(0.3, 1))
            btn_layout.add_widget(btn_icon)
            btn_layout.add_widget(page_btn)
            self.add_widget(btn_layout)

            if page.page_name is not None:
                page_btn.bind(
                    on_press=lambda instance, page_name=page.page_name: self.open_page(
                        page_name
                    )
                )

    def open_page(self, page_name):
        self.screen_manager.current = page_name
