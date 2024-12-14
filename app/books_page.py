from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button

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
