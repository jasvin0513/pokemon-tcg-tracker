"""
This script provides users with a popup that lets them filter their search for cards
"""

import sys, os
from PySide6 import QtCore, QtWidgets, QtGui
import search_api
import search_filters

os.environ["QT_LOGGING_RULES"] = "qt.gui.imageio=false"

# Create a loading screen while the filters load
class LoadingScreen(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Loading filters...")
        self.setFixedSize(300, 1)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
    
# Create the selection page
class SearchSelection(QtWidgets.QTableWidget):
    def __init__(self, width, height):
        super().__init__()
        
        # Initialize home page size
        self.width = width
        self.height = height
        
        # Create a loading screen
        self.loading_screen = LoadingScreen()
        self.loading_screen.show()
        
        # Align each search criteria vertically and add them to the list of filters
        filters = []
        layout = QtWidgets.QVBoxLayout(self)
        
        # Create a filter for Pokemon names
        name_filter = search_filters.NameFilter()
        layout.addWidget(name_filter)
        filters.append(name_filter)
        
        #Create a filter for the national Pokedex numbers
        national_filter = search_filters.NationalNoFilter()
        layout.addWidget(national_filter)
        filters.append(national_filter)

        # Create a filter for sets
        sets = search_api.get_sets()
        set_filter = search_filters.SetFilter(sets)
        layout.addWidget(set_filter)
        filters.append(set_filter)
        
        # Once all filters are populated, hide the loading screen
        if self.loading_screen.isVisible():
            self.loading_screen.hide()
        
        self.cards = None
        # Create a button that searches the API using each filter
        search_button = QtWidgets.QPushButton("Search", self)
        search_button.clicked.connect(lambda: self.set_cards(self.search_cards(filters)))
        search_button.clicked.connect(self.close)
        layout.addWidget(search_button)
        
        # Connect the aboutToQuit signal to a function that returns the cards before the application closes
        app.aboutToQuit.connect(lambda: print(self.cards))
    
    def set_cards(self, result):
        self.cards = result
    
    def search_cards(self, filters):
        parameters = ''
        for filter in filters:
            if filter.get_content().strip():
                parameters += (f" {filter.type}:{filter.get_content()} ")
        
        return search_api.search_cards(parameters)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    selection = SearchSelection(600, 300)
    selection.resize(selection.width, selection.height)
    selection.show()
    
    sys.exit(app.exec())