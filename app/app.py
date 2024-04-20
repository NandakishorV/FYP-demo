from PyQt5.QtWidgets import QApplication
from ui import GraphUI

def main():
    app = QApplication([])
    window = GraphUI()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
