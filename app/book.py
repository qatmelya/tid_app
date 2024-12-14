from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

# Example data structure for the story
story = [
    {
        "sentence": "The boy is running asdadaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbb.",
        "gifs": [
            "static/book1.jpg",
            "static/book2.jpg",
            "static/book1.jpg",
            "static/book2.jpg",
            "static/book1.jpg",
            "static/book2.jpg",
            "static/book1.jpg",
            "static/book2.jpg",
            "static/book2.jpg",
        ],
    },
    {
        "sentence": "The girl is reading a book.",
        "gifs": ["read1.gif", "read2.gif", "read3.gif"],
    },
    {"sentence": "The dog is barking.", "gifs": ["bark1.gif", "bark2.gif"]},
]

# Sample data for books
books = [
    {"name": "Book 1", "cover": "static/book1.jpg", "content": story},
    {"name": "Book 2", "cover": "static/book2.jpg", "content": story},
    {"name": "Book 3", "cover": "static/book3.png", "content": story},
]


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


class BooksPage(GridLayout):
    page_name = "books"
    readable_name = "Kitaplar"
    icon_path = "static/book.png"

    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.screen_manager = screen_manager

        for book in books:
            # Create a layout to combine the image and text
            book_layout = BoxLayout(orientation="vertical", size_hint=(0.2, 0.2))

            # Add book cover image
            cover = Image(source=book["cover"], size_hint=(1, 0.8))
            book_layout.add_widget(cover)

            # Add book name as a button
            btn = Button(text=book["name"], size_hint=(1, 0.2), color=(0, 0, 0, 1))
            btn.bind(on_press=lambda instance, book=book: self.open_book(book))
            book_layout.add_widget(btn)
            self.add_widget(book_layout)

    def open_book(self, book):
        book_content_screen = self.screen_manager.get_screen("book_content")
        # Access the BookContentPage widget from the screen's children
        book_content_page = book_content_screen.children[0]
        book_content_page.update_content(book["content"], book["name"])
        self.screen_manager.current = "book_content"


class BookContentPage(BoxLayout):
    page_name = "book_content"
    readable_name = "Kitap İçeriği"

    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.screen_manager = screen_manager
        self.padding = [10, 10, 10, 10]  # Add padding around the layout
        self.current_sentence_index = 0  # Track the current sentence index
        self.current_story = []  # Placeholder for the story content

        # Title label
        self.title_label = Label(
            size_hint=(1, 0.1),  # Reserve 10% of the height for the title
            font_size=24,
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1),
        )
        self.title_label.bind(size=self.title_label.setter("text_size"))
        self.add_widget(self.title_label)

        # Horizontal ScrollView for GIFs
        self.gif_scroll = ScrollView(
            size_hint=(1, 0.4),  # Allocate 40% of the remaining space
            do_scroll_x=True,
            do_scroll_y=False,
        )
        self.gif_layout = BoxLayout(orientation="horizontal", size_hint=(None, 1))
        self.gif_layout.bind(minimum_width=self.gif_layout.setter("width"))
        self.gif_scroll.add_widget(self.gif_layout)
        self.add_widget(self.gif_scroll)

        # Scrollable Label for the sentence
        self.sentence_scroll_view = ScrollView(size_hint=(1, 0.4))
        self.sentence_label = Label(
            text="",
            size_hint=(1, None),
            font_size=24,
            halign="center",
            valign="middle",
            padding=(20, 10),
            color=(0, 0, 0, 1),
        )
        self.sentence_label.bind(size=self.sentence_label.setter("text_size"))
        self.sentence_scroll_view.add_widget(self.sentence_label)
        self.add_widget(self.sentence_scroll_view)

        # Navigation buttons at the bottom
        nav_buttons_layout = BoxLayout(size_hint=(1, 0.1))

        self.left_button = Button(
            text="Previous", size_hint=(0.3, 1), font_size=18, color=(0, 0, 0, 1)
        )
        self.left_button.bind(on_press=self.show_previous_sentence)
        nav_buttons_layout.add_widget(self.left_button)

        self.back_button = Button(
            text="Back", size_hint=(0.4, 1), font_size=18, color=(0, 0, 0, 1)
        )
        self.back_button.bind(on_press=self.go_back)
        nav_buttons_layout.add_widget(self.back_button)

        self.right_button = Button(
            text="Next", size_hint=(0.3, 1), font_size=18, color=(0, 0, 0, 1)
        )
        self.right_button.bind(on_press=self.show_next_sentence)
        nav_buttons_layout.add_widget(self.right_button)

        self.add_widget(nav_buttons_layout)

        # Bind the ScrollView's width to dynamically adjust the Label's text wrapping
        self.gif_scroll.bind(width=self.update_text_size)

    def update_content(self, story, title):
        self.current_story = story
        self.current_sentence_index = 0
        self.title_label.text = title
        self.display_current_sentence()

    def display_current_sentence(self):
        # Get the current sentence and its GIFs
        if self.current_story:
            current_sentence = self.current_story[self.current_sentence_index]
            sentence = current_sentence["sentence"]
            gifs = current_sentence["gifs"]

            # Update the sentence label
            self.sentence_label.text = sentence
            self.sentence_label.texture_update()

            # Remove existing GIFs
            for old_gif in self.gif_layout.children[:]:
                self.gif_layout.remove_widget(old_gif)

            # Add new GIFs
            for gif in gifs:
                gif_image = Image(
                    source=gif,
                    size_hint=(None, 1),
                    size=(200, 200),
                )
                self.gif_layout.add_widget(gif_image)

            # Enable or disable navigation buttons based on current index
            self.left_button.disabled = self.current_sentence_index == 0
            self.right_button.disabled = (
                self.current_sentence_index == len(self.current_story) - 1
            )

    def show_next_sentence(self, instance):
        if self.current_sentence_index < len(self.current_story) - 1:
            self.current_sentence_index += 1
            self.display_current_sentence()

    def show_previous_sentence(self, instance):
        if self.current_sentence_index > 0:
            self.current_sentence_index -= 1
            self.display_current_sentence()

    def update_text_size(self, instance, value):
        # Ensure text wrapping adjusts with width changes
        self.sentence_label.text_size = (
            self.sentence_scroll_view.width - 20,
            None,
        )

    def go_back(self, instance):
        self.screen_manager.current = "books"


class BookApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        self.title = "TiD Çocuk Kitapları"
        screen_manager = ScreenManager()

        main_page = MainPage(screen_manager)
        main_screen = Screen(name=MainPage.page_name)
        main_screen.add_widget(main_page)
        screen_manager.add_widget(main_screen)

        books_page = BooksPage(screen_manager)
        books_screen = Screen(name=BooksPage.page_name)
        books_screen.add_widget(books_page)
        screen_manager.add_widget(books_screen)

        book_content_page = BookContentPage(screen_manager)
        book_content_screen = Screen(name=BookContentPage.page_name)
        book_content_screen.add_widget(book_content_page)
        screen_manager.add_widget(book_content_screen)

        return screen_manager


if __name__ == "__main__":
    BookApp().run()
