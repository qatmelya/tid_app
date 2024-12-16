from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from data_requests import get_books, get_book_content_by_id, server_url

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

books = get_books()


class BooksPage(BoxLayout):
    page_name = "books"
    readable_name = "Kitaplar"
    icon_path = "static/book.png"

    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.screen_manager = screen_manager

        # Search bar at the top
        search_layout = BoxLayout(
            size_hint=(1, 0.1), spacing=10, padding=[10, 10, 10, 10]
        )
        self.search_input = TextInput(
            hint_text="Search for a book...",
            size_hint=(0.8, 1),
            multiline=False,
        )
        self.search_input.bind(text=self.filter_books)
        search_layout.add_widget(self.search_input)

        self.clear_search_button = Button(text="Clear", size_hint=(0.2, 1))
        self.clear_search_button.bind(on_press=self.clear_search)
        search_layout.add_widget(self.clear_search_button)

        self.add_widget(search_layout)

        # Scrollable layout for books
        self.scroll_view = ScrollView(size_hint=(1, 0.9))
        self.books_layout = GridLayout(
            cols=2, size_hint_y=None, spacing=10, padding=[10, 10, 10, 10]
        )
        self.books_layout.bind(minimum_height=self.books_layout.setter("height"))
        self.scroll_view.add_widget(self.books_layout)
        self.add_widget(self.scroll_view)

        self.displayed_books = books[:]  # Start with the full list of books
        self.load_books()

    def load_books(self):
        # Clear the current book widgets
        self.books_layout.clear_widgets()

        # Add filtered books to the grid layout
        for book in self.displayed_books:
            book_layout = BoxLayout(
                orientation="vertical", size_hint=(1, 1), size_hint_min_y=500
            )

            # Add book cover image
            cover = AsyncImage(
                source=(server_url + book["cover_path"]), size_hint=(1, 0.8)
            )
            book_layout.add_widget(cover)

            # Add book name as a button
            btn = Button(text=book["title"], size_hint=(1, 0.2))
            btn.bind(on_press=lambda instance, book=book: self.open_book(book))
            book_layout.add_widget(btn)

            self.books_layout.add_widget(book_layout)

    def filter_books(self, instance, text):
        # Filter books based on search input
        search_query = text.lower()
        self.displayed_books = [
            book for book in books if search_query in book["title"].lower()
        ]
        self.load_books()

    def clear_search(self, instance):
        # Clear the search input and reset the displayed books
        self.search_input.text = ""
        self.displayed_books = books[:]
        self.load_books()

    def open_book(self, book):
        book_content_screen = self.screen_manager.get_screen("book_content")
        book_content_page = book_content_screen.children[0]
        book_content_page.update_content(
            get_book_content_by_id(book["book_id"]), book["title"]
        )
        self.screen_manager.current = "book_content"
