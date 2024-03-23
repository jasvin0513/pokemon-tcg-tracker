import sys
from PySide6 import QtWidgets
from home import HomePage
from sidebar import SideBar
from search.search_page import SearchPage

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        # Create instances of each page
        self.page_width = 1150
        self.page_height = 700
        
        # Home Page
        self.home = HomePage(self.page_width, self.page_height)
        
        # Search Page
        self.search = SearchPage(self.page_width, self.page_height)
        
        # Create stacked widget to switch between pages
        self.stackedWidget = QtWidgets.QStackedWidget()
        self.stackedWidget.addWidget(self.home)
        self.stackedWidget.addWidget(self.search)
        
        # Create an instance of the sidebar
        self.sidebar_width = 100
        self.sidebar = SideBar(self.sidebar_width, self.page_height, self.stackedWidget)
        
        
        # Arrange the sidebar and stacked widget horizontally
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.sidebar)
        self.layout.addWidget(self.stackedWidget)
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    main = MainWindow()
    main.resize(main.page_width + main.sidebar_width, main.page_height)
    main.show()
    
    sys.exit(app.exec())