import sys
from PySide6 import QtCore, QtWidgets, QtGui

# Create the home page

class HomePage(QtWidgets.QWidget):
    def __init__(self, width, height):
        super().__init__()
        
        # Initialize home page size
        self.width = width
        self.height = height
        
        # Print the title of the program
        self.title = QtWidgets.QLabel("Pokemon TCG Tracker", 
                                    alignment=QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.title.setFont(font)
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.title)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    home = HomePage(900, 600)
    home.resize(home.width, home.height)
    home.show()
    
    sys.exit(app.exec())