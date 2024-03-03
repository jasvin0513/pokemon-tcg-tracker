"""
This script provides users with a popup that lets them filter their search for cards
"""

import sys, os
from PySide6 import QtCore, QtWidgets, QtGui
import search_api
import search_filters

os.environ["QT_LOGGING_RULES"] = "qt.gui.imageio=false"

# Create the selection page
class SearchSelection(QtWidgets.QWidget):
    # Create a custom signal
    cards_emitted = QtCore.Signal(list)
    hideRequested = QtCore.Signal()
    
    def __init__(self, app, filter_cache = None):
        super().__init__()
        
        # Initialize home page size
        self.width = 600
        self.height = 300
        
        # Create a loading screen
        self.loading_screen = search_filters.LoadingScreen()
        self.loading_screen.show()
        
        # Align each search criteria vertically and add them to the list of filters
        filters = []
        layout = QtWidgets.QVBoxLayout(self)
        
        # If the cache is empty, create each filter. Otherwise use the cache
        if filter_cache == None:
            # Name filter
            name_filter = search_filters.NameFilter()
            # National number filter
            national_filter = search_filters.NationalNoFilter()
            # Set filter
            set_filter = search_filters.SetFilter()
        else:
            # Name filter
            name_filter = filter_cache.NameFilter
            # National number filter
            national_filter = filter_cache.NationalNoFilter
            # Set filter
            set_filter = filter_cache.SetFilter
            
        # Add filters to the layout and list of filters
        layout.addWidget(name_filter)
        filters.append(name_filter)
        layout.addWidget(national_filter)
        filters.append(national_filter)
        layout.addWidget(set_filter)
        filters.append(set_filter)
        
        # Once all filters are populated, hide the loading screen
        if self.loading_screen.isVisible():
            self.loading_screen.hide()
        
        self.cards = None
        # Create a button that searches the API using each filter
        search_button = QtWidgets.QPushButton("Search", self)
        search_button.clicked.connect(lambda: self.set_cards(self.search_cards(filters)))
        self.cards_emitted.connect(self.handle_cards_received)
        layout.addWidget(search_button)
        
        # Connect the aboutToQuit signal to a function that prints the cards before the application closes
        # app.aboutToQuit.connect(lambda: print(self.cards))
    
    # Sets the list of cards for the widget
    def set_cards(self, result):
        self.cards = result
        self.emit_cards_signal()
    
    # Sends a list of cards to other widgets as a signal
    def emit_cards_signal(self):
        print(f"Signal emitted with {len(self.cards)} cards")
        self.cards_emitted.emit(self.cards)
        self.hideRequested.emit()
        self.cards = None
        
    def handle_cards_received(self, cards):
        print(f"Received cards signal with {len(cards)} cards in SearchSelection")
    
    # Searches the card API and returns a list of cards
    def search_cards(self, filters):
        parameters = ''
        for filter in filters:
            if filter.get_content().strip():
                parameters += (f" {filter.type}:{filter.get_content()} ")
        
        print(f"Search parameters: {parameters}")
        return search_api.search_cards(parameters)

if __name__ == "__main__":
    filter_app = QtWidgets.QApplication([])

    selection = SearchSelection(filter_app)
    selection.resize(selection.width, selection.height)
    selection.show()

    sys.exit(filter_app.exec())