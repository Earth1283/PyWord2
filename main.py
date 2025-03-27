import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog,
    QMessageBox, QToolBar, QAction, QFontDialog,
    QColorDialog, QLabel, QWidget, QVBoxLayout
)
from PyQt5.QtGui import QIcon, QFont, QColor, QTextCursor
from PyQt5.QtCore import Qt, QTimer

class WordEditor(QMainWindow):
    """
    A basic word processor application built using PyQt5.
    """
    def __init__(self):
        super().__init__()

        # Initialize the user interface
        self.initUI()

    def initUI(self):
        """
        Sets up the main window, text editor, toolbar, and menu.
        """
        # Set window title and icon
        self.setWindowTitle("PyQt5 Word Editor")
        self.setWindowIcon(QIcon.fromTheme("edit-document", QIcon("edit.png")))

        # Create the text edit widget
        self.textEdit = QTextEdit(self)
        self.setCentralWidget(self.textEdit)

        # Create the toolbar
        self.toolbar = QToolBar("Main Toolbar", self)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # Create actions for the toolbar and menu
        self.createActions()
        # Add actions to the toolbar
        self.addActionsToToolbar()
        # Create the menu bar
        self.createMenu()

        # Set the initial font
        self.default_font = QFont("Arial", 12)
        self.textEdit.setFont(self.default_font)

        # Set the initial window size
        self.setGeometry(300, 300, 800, 600)

        # Create the status bar
        self.statusBar().showMessage("Ready")  # Initial status message

        # Create word count label in the status bar
        self.wordCountLabel = QLabel("Words: 0", self)
        self.statusBar().addPermanentWidget(self.wordCountLabel)  # Add to the right side

        # Connect textEdit's textChanged signal to updateWordCount
        self.textEdit.textChanged.connect(self.updateWordCount)

        # Use a timer to delay the word count update.  This improves performance.
        self.wordCountTimer = QTimer()
        self.wordCountTimer.timeout.connect(self.updateWordCount)
        self.wordCountTimer.setSingleShot(True)  # Single shot timer

        # Show the main window
        self.show()

    def createActions(self):
        """
        Creates the actions for opening, saving, and exiting files,
        as well as for font and color customization.  Modified to include emojis.
        """
        # File menu actions
        self.openAction = QAction(QIcon.fromTheme("document-open", QIcon("open.png")), "Open 📂", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.setStatusTip("Open a file")
        self.openAction.triggered.connect(self.openFile)

        self.saveAction = QAction(QIcon.fromTheme("document-save", QIcon("save.png")), "Save 💾", self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.setStatusTip("Save the file")
        self.saveAction.triggered.connect(self.saveFile)

        self.saveAsAction = QAction("Save As... 📝", self)  # Added emoji
        self.saveAsAction.setShortcut("Ctrl+Shift+S")
        self.saveAsAction.setStatusTip("Save the file with a new name")
        self.saveAsAction.triggered.connect(self.saveAsFile)

        self.exitAction = QAction(QIcon.fromTheme("application-exit", QIcon("exit.png")), "Exit 🚪", self)
        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.setStatusTip("Exit the application")
        self.exitAction.triggered.connect(self.close)

        # Edit menu actions
        self.fontAction = QAction(QIcon.fromTheme("preferences-desktop-font", QIcon("font.png")), "Font ✒️", self)
        self.fontAction.setStatusTip("Change font")
        self.fontAction.triggered.connect(self.setFont)

        self.colorAction = QAction(QIcon.fromTheme("preferences-desktop-color", QIcon("color.png")), "Color 🎨", self)
        self.colorAction.setStatusTip("Change text color")
        self.colorAction.triggered.connect(self.setColor)

        self.aboutAction = QAction("About ℹ️", self) # added emoji
        self.aboutAction.setStatusTip("Show About Box")
        self.aboutAction.triggered.connect(self.showAbout)

    def addActionsToToolbar(self):
        """Adds the defined actions to the toolbar."""
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.fontAction)
        self.toolbar.addAction(self.colorAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.exitAction)

    def createMenu(self):
        """
        Creates the menu bar and adds the file and edit menus.
        """
        self.menuBar = self.menuBar()
        fileMenu = self.menuBar.addMenu("&File")
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

        editMenu = self.menuBar.addMenu("&Edit")
        editMenu.addAction(self.fontAction)
        editMenu.addAction(self.colorAction)

        helpMenu = self.menuBar.addMenu("&Help")
        helpMenu.addAction(self.aboutAction)
        self.statusBar()

    def openFile(self):
        """
        Opens a file and loads its content into the text edit widget.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    text = file.read()
                    self.textEdit.setText(text)
                    self.statusBar().showMessage(f"Opened file: {file_name}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {e}")
                self.statusBar().showMessage(f"Error opening file: {e}", 3000)

    def saveFile(self):
        """
        Saves the content of the text edit widget to the current file.
        If no file is currently open, it calls saveAsFile().
        """
        if hasattr(self, 'current_file'):
            try:
                with open(self.current_file, 'w') as file:
                    file.write(self.textEdit.toPlainText())
                self.statusBar().showMessage(f"Saved to {self.current_file}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {e}")
                self.statusBar().showMessage(f"Error saving file: {e}", 3000)
        else:
            self.saveAsFile()

    def saveAsFile(self):
        """
        Saves the content of the text edit widget to a new file.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save As", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write(self.textEdit.toPlainText())
                self.current_file = file_name
                self.statusBar().showMessage(f"Saved as {file_name}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {e}")
                self.statusBar().showMessage(f"Error saving file: {e}", 3000)

    def setFont(self):
        """
        Opens a font dialog and sets the selected font for the text edit widget.
        """
        font, ok = QFontDialog.getFont(self.default_font, self)
        if ok:
            self.textEdit.setFont(font)
            self.default_font = font

    def setColor(self):
        """
        Opens a color dialog and sets the selected text color for the text edit widget.
        """
        color = QColorDialog.getColor(Qt.black, self)
        if color.isValid():
            self.textEdit.setTextColor(color)

    def showAbout(self):
        """Displays a simple About dialog box."""
        QMessageBox.about(self, "About PyQt5 Word Editor",
                            "This is a basic word processor application created with PyQt5.")

    def updateWordCount(self):
        """
        Updates the word count in the status bar.  This function is called
        whenever the text in the textEdit widget changes.
        """
        # Use a timer to delay the actual word count calculation
        # This improves performance, especially with large documents.
        self.wordCountTimer.start(200)  # 200 ms delay

        # Get the text from the text edit widget
        text = self.textEdit.toPlainText()
        # Split the text into words, handling multiple spaces and newlines
        words = text.split()
        word_count = len(words)
        self.wordCountLabel.setText(f"Words: {word_count}")
        # update the status bar
        self.statusBar().showMessage(f"Word Count: {word_count}", 3000)

if __name__ == '__main__':
    # Create the application instance
    app = QApplication(sys.argv)
    # Create and show the main window
    word_editor = WordEditor()
    # Start the event loop
    sys.exit(app.exec_())
