"""
This is the main search file that displays all cards captured by a search
"""
import sys
from PySide6 import QtCore, QtWidgets, QtGui
import search_selection

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
        for card in cards:
            # Create the card widget
            card_widget = QtWidgets.QPushButton()
            card_widget.setStyleSheet("background-color: white; border: 1px solid black;")
            card_widget.setFixedSize(245, 342)
            name = QtWidgets.QLabel(str(card))
            name.setFont(QtGui.QFont('Arial Font', 12))
            name.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
            
            # Make card clickable
            card_widget.clicked.connect(lambda: print("Card clicked"))
            
            # Add the card to the next available position
            card_layout.addWidget(card_widget, row, col)
            row += 1
            card_layout.addWidget(name, row, col)
            col += 1
            row -= 1
            
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
        
        # Create the filter button
        search_selection_button = QtWidgets.QPushButton('Filter')
        search_selection_button.clicked.connect(self.show_search_selection())
        
        # Create a vertical layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(60)
        self.layout.addWidget(title)
        
        # Add the table and filter to the layout
        self.layout.addWidget(search_selection_button)
        self.table = CardGrid(list(range(1,10)))
        self.layout.addWidget(self.table)
    
    def show_search_selection(self):
        # Create and show the SearchSelection widget
        selection_widget = search_selection.SearchSelection()
        selection_widget.show()
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    search = SearchPage(1150, 700)
    search.resize(search.width, search.height)
    search.show()
    
    sys.exit(app.exec())