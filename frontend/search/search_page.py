"""
This is the main search file that displays all cards captured by a search
"""
import sys
from functools import partial
from PySide6 import QtCore, QtWidgets, QtGui
import search_selection, search_filters, requests

# Create the search table
class CardGrid(QtWidgets.QWidget):
    def __init__(self, cards):
        super().__init__()
        
        # Set the layout for the widget
        main_layout = QtWidgets.QVBoxLayout(self)
        
        # Set the layout for the card grid
        card_grid = QtWidgets.QWidget()
        card_layout = QtWidgets.QGridLayout(card_grid)
        row = 0
        col = 0
        
        # Iterate through each card object and display them as a widget
        if cards:
            for card in cards:
                # Get the card's image
                response = requests.get(card.image_url)
                pixmap_icon = QtGui.QPixmap()
                pixmap_icon.loadFromData(response.content)
                
                # Create the card widget
                card_widget = QtWidgets.QPushButton()
                card_widget.setIcon(pixmap_icon)
                card_widget.setIconSize(QtCore.QSize(245, 342)) 
                
                name = QtWidgets.QLabel(str(card))
                name.setFont(QtGui.QFont('Arial Font', 12))
                name.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
                
                # Make card clickable
                card_widget.clicked.connect(partial(self.show_card_details, card, pixmap_icon))
                
                # Add the card to the next available position
                card_layout.addWidget(card_widget, row, col)
                row += 1
                card_layout.addWidget(name, row, col)
                col += 1
                row -= 1
                
                # Start a new row after every 3 cards
                if col == 3:
                    row += 2
                    col = 0

        # Create a scrollable grid
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(card_grid)
        scroll_area.setMaximumHeight(500)
        main_layout.addWidget(scroll_area)
        
    def show_card_details(self, card, icon):
        card_details_popup = CardDetails(card, icon)
        card_details_popup.exec()
            
# Create the card details page when a card button is clicked
class CardDetails(QtWidgets.QDialog):
    def __init__(self, card, icon):
        super().__init__()
        
        # Displays the card's icon
        card_image = QtWidgets.QLabel(self)
        card_image.setPixmap(icon)
        
        # Displays the card's information
        card_information = QtWidgets.QLabel(str(card))
        
        # Input widget for the number of copies to be added to the collection
        quantity_input = QtWidgets.QLineEdit(self)
        
        # Button to add cards to the collection
        confirm_button = QtWidgets.QPushButton("Add to Collection")
        confirm_button.clicked.connect(lambda: self.add_cards(quantity_input.text()))
        
        # Display all components vertically
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(card_image)
        layout.addWidget(card_information)
        layout.addWidget(quantity_input)
        layout.addWidget(confirm_button)
    
    def add_cards(self, quantity):
        try:
            if int(quantity) > 0:
                print(f"{quantity} added to collection")
                self.accept()
            else:
                print("Invalid quantity")
        except:
            print("Invalid quantity")

# Create the search page
class SearchPage(QtWidgets.QWidget):
    def __init__(self, width, height):
        super().__init__()
        
        # Initialize home page size
        self.width = width
        self.height = height
        
        # Create the page title
        title = QtWidgets.QLabel("Card Search", 
                                    alignment=QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(18)
        title.setFont(font)
        
        # Create the filter button and a cache for the filters
        self.filter_cache = None
        self.cards = None
        search_selection_button = QtWidgets.QPushButton('Filter')
        search_selection_button.clicked.connect(self.toggle_search_selection)
        
        # Create a vertical layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(60)
        self.layout.addWidget(title)
        
        # Add the table and filter to the layout
        self.layout.addWidget(search_selection_button)
        self.table = CardGrid(self.cards)
        self.layout.addWidget(self.table)
    
    # Control the SearchSelection widget
    def toggle_search_selection(self):
        # Check if the SearchSelection widget is already visible
        if hasattr(self, 'selection_widget') and self.selection_widget.isVisible():
            self.selection_widget.hide()
        else:
            # Initialize the filter cache if needed
            if self.filter_cache == None:
                self.loading_screen = search_filters.LoadingScreen()
                self.loading_screen.show()
                self.filter_cache = search_filters.FilterCache()
                
                # Once all filters are populated, hide the loading screen
                if self.loading_screen.isVisible():
                    self.loading_screen.hide()
                
            # Create and show the SearchSelection widget
            self.selection_widget = search_selection.SearchSelection(self, self.filter_cache)
            self.selection_widget.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.selection_widget.show()
            
            # Connect the hideRequested signal to hide_search_selection method
            self.selection_widget.hideRequested.connect(self.hide_search_selection)
            # Connect the cardsReceived signal to handle_cards_received method
            self.selection_widget.cards_emitted.connect(self.handle_cards_received)
    
    # Hide the SearchSelection widget if it is visible
    def hide_search_selection(self):
        if hasattr(self, 'selection_widget'):
            self.selection_widget.hide()
    
    # Check to see if the cards were selected by the filter
    def handle_cards_received(self, cards):
        print(f"Received cards signal with {len(cards)} cards in SearchPage")
        self.cards = cards
        self.layout.removeWidget(self.table)
        self.table = CardGrid(self.cards)
        self.layout.addWidget(self.table)
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    search = SearchPage(1150, 700)
    search.resize(search.width, search.height)
    search.show()
    
    sys.exit(app.exec())