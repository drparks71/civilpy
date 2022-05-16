from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.utils import platform
import fitz  # PyMuPDF

if platform == "android":
    from android.permissions import request_permissions, Permission

import os
from time import time


class PDFViewerApp(App):
    def build(self):
        # Layout for the App
        self.layout = BoxLayout(orientation="vertical")

        # PDF File Parameters
        self.pdf_file = "C:\\Users\\dane\\PycharmProjects\\civilpy\\res\\ODOT_sample_plans.pdf"
        self.doc = fitz.open(self.pdf_file)

        # Initialize Display Attributes
        self.page_number = 0
        self.total_pages = len(self.doc)

        # Create Image Widget to Display PDF
        self.image_widget = PDFImageWidget(self)
        self.layout.add_widget(self.image_widget)

        # Create Page Label to display Current Page
        self.page_label = Label(
            text=f"Page 1 of {self.total_pages}", size_hint_y=0.1, halign="center"
        )
        self.layout.add_widget(self.page_label)

        # Display the first page
        self.display_page(self.page_number)

        return self.layout

    def display_page(self, page_number):
        """Render and display the given PDF page."""
        # Ensure the page number is within bounds
        if page_number < 0 or page_number >= self.total_pages:
            return

        # Update Page Label
        self.page_label.text = f"Page {page_number + 1} of {self.total_pages}"

        # Load the Page
        page = self.doc[page_number]
        pix = page.get_pixmap()

        # Convert Pixmap to Kivy Texture
        texture = Texture.create(size=(pix.width, pix.height))
        texture.blit_buffer(pix.samples, bufferfmt="ubyte", colorfmt="rgb")
        texture.flip_vertical()

        # Set the Image Widget Texture
        self.image_widget.texture = texture

    def go_to_next_page(self):
        """Navigate to the next page."""
        if self.page_number < self.total_pages - 1:
            self.page_number += 1
            self.display_page(self.page_number)

    def go_to_previous_page(self):
        """Navigate to the previous page."""
        if self.page_number > 0:
            self.page_number -= 1
            self.display_page(self.page_number)

    def long_press(self, touch_pos):
        """Handle long press gesture to add annotation."""
        print(f"Long press detected at {touch_pos}. Add your camera logic here.")


class PDFImageWidget(Image):
    """Custom Image widget to handle swipe and long-press gestures."""

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app  # Reference to the main App
        self.start_x = None  # To store the starting X position of the touch
        self.start_y = None  # To store the starting Y position of the touch
        self.touch_start_time = None  # To store the timestamp of the touch
        self.long_touch_event = None  # Handle for canceling long press

    def on_touch_down(self, touch):
        """Capture the starting point of the touch and schedule long press."""
        self.start_x = touch.x
        self.start_y = touch.y
        self.touch_start_time = time()

        # Schedule the long press callback (0.5 seconds threshold)
        self.long_touch_event = Clock.schedule_once(
            lambda dt: self.app.long_press(touch.pos), 0.5
        )
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        """Cancel long press and handle swipe."""
        # Cancel the long press detection if touch is released
        if self.long_touch_event:
            self.long_touch_event.cancel()
        self.long_touch_event = None

        # Calculate the time difference and distance for swipe vs long press
        touch_duration = time() - self.touch_start_time
        delta_x = touch.x - self.start_x
        delta_y = touch.y - self.start_y

        # Determine if it's a swipe (horizontal swipe with small vertical deviation)
        if abs(delta_x) > 50:  # Swipe threshold
            if delta_x > 0:
                self.app.go_to_previous_page()  # Swipe right
            else:
                self.app.go_to_next_page()  # Swipe left
        else:
            # If no significant movement, assume it's a tap or other gesture
            print("No swipe detected.")
        return super().on_touch_up(touch)


if __name__ == "__main__":
    PDFViewerApp().run()
