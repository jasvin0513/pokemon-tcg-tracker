"""
This script provides users with a popup that lets them filter their search for cards
"""

import sys, warnings
from PySide6 import QtCore, QtWidgets, QtGui
import search_api
import search_filters
            
# Create the selection page
class SearchSelection(QtWidgets.QTableWidget):
    def __init__(self, width, height):
        super().__init__()
        
        # Initialize home page size
        self.width = width
        self.height = height
        
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
        warnings.filterwarnings("ignore", category=UserWarning, module="qt.gui.imageio")
        sets = search_api.get_sets()
        set_filter = search_filters.SetFilter(sets)
        layout.addWidget(set_filter)
        filters.append(set_filter)
        warnings.resetwarnings()
        
        # Create a button that searches the API using each filter
        search_button = QtWidgets.QPushButton("Search", self)
        search_button.clicked.connect(lambda: self.search_cards(filters))
        layout.addWidget(search_button)

        
    def search_cards(self, filters):
        parameters = ''
        for filter in filters:
            if filter.get_content().strip():
                parameters += (f" {filter.type}:{filter.get_content()} ")
        
        search_api.search_cards(parameters)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    selection = SearchSelection(600, 300)
    selection.resize(selection.width, selection.height)
    selection.show()
    
    sys.exit(app.exec())