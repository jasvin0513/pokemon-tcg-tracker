import sys
from PySide6 import QtCore, QtWidgets

# Create the sidebar class

class SideBar(QtWidgets.QFrame):
    def __init__(self, width, height):
        super().__init__()
        
        # Initialize sidebar size
        self.width = width
        self.height = height
        
        # Create buttons
        buttonWidth = 50
        buttonHeight = 50
        
        # Button for the collections page
        self.collection = QtWidgets.QPushButton("Collection")
        self.collection.setFixedSize(buttonWidth, buttonHeight)
        
        # Button for the search page
        self.search = QtWidgets.QPushButton("Search")
        self.search.setFixedSize(buttonWidth, buttonHeight)
        
        # Button for the analytics page
        self.analytics = QtWidgets.QPushButton("Analytics")
        self.analytics.setFixedSize(buttonWidth, buttonHeight)
        
        # Style buttons vertically in the sidebar
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.collection)
        self.layout.addWidget(self.search)
        self.layout.addWidget(self.analytics)
        
        # Center the buttons horizontally and add padding
        self.layout.setAlignment(QtCore.Qt.AlignHCenter)
        self.layout.setSpacing(50)
        
        # Add a border when attached to other pages
        self.setStyleSheet("QFrame { border-right: 10px solid white; }")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    sidebar = SideBar(100,600)
    sidebar.resize(sidebar.width, sidebar.height)
    sidebar.show()
    
    sys.exit(app.exec())