from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from data_requests import server_url
from kivy.uix.video import Video


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
        self.current_sentence_index = 1
        self.title_label.text = title
        self.display_current_sentence()

    def display_current_sentence(self):
        # Get the current sentence and its GIFs
        if self.current_story:
            current_sentence = next(
                sentence
                for sentence in self.current_story
                if (sentence["nth_sentence"] == self.current_sentence_index)
            )
            sentence = current_sentence["sentence"]
            gifs = current_sentence["transcript"].split(",")

            # Update the sentence label
            self.sentence_label.text = sentence
            self.sentence_label.texture_update()

            # Remove existing GIFs
            for old_gif in self.gif_layout.children[:]:
                self.gif_layout.remove_widget(old_gif)

            # Add new GIFs
            for gif in gifs:
                gif_box = BoxLayout(
                    orientation="vertical", size_hint=(None, 1), width=200
                )

                # Add GIF image
                if gif.split(".")[-1] in ["mp4", "gif"]:
                    gif_image = Video(
                        source=(server_url + "static/sign_language_media/" + gif),
                        state="play",
                    )
                else:
                    gif_image = AsyncImage(
                        source=(server_url + "static/sign_language_media/" + gif),
                        size_hint=(1, 0.8),
                        size=(200, 80),  # Size of the GIF
                    )
                gif_box.add_widget(gif_image)

                # Add file name label
                gif_label = Label(
                    text=gif.split("/")[-1].split(".")[
                        0
                    ],  # Extract file name from path
                    size_hint=(1, 0.2),
                    font_size=18,
                    halign="center",
                    valign="middle",
                    color=(0, 0, 0, 1),
                )
                gif_label.bind(size=gif_label.setter("text_size"))
                gif_box.add_widget(gif_label)

                self.gif_layout.add_widget(gif_box)

            # Enable or disable navigation buttons based on current index
            self.left_button.disabled = self.current_sentence_index == 1
            self.right_button.disabled = self.current_sentence_index == len(
                self.current_story
            )

    def show_next_sentence(self, instance):
        if self.current_sentence_index < len(self.current_story):
            self.current_sentence_index += 1
            self.display_current_sentence()

    def show_previous_sentence(self, instance):
        if self.current_sentence_index > 1:
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
