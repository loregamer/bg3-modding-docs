import sys
import subprocess
import os # Needed for path checking
import keyring # For storing Divine.exe path securely
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLineEdit, QTextEdit, QComboBox, QLabel,
    QMessageBox, QTreeView
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem # Corrected import
from PyQt6.QtCore import QProcess

class PackageListerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LSLib Package Lister")
        self.setGeometry(100, 100, 600, 400)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # --- Divine.exe Path Selection ---
        divine_path_layout = QHBoxLayout()
        self.divine_path_edit = QLineEdit()
        self.divine_path_edit.setReadOnly(True) # Display only
        self.divine_path_edit.setPlaceholderText("Path to Divine.exe")
        change_divine_button = QPushButton("Change...")
        change_divine_button.clicked.connect(self.prompt_for_divine_path) # Connect button
        divine_path_layout.addWidget(QLabel("Divine.exe Path:"))
        divine_path_layout.addWidget(self.divine_path_edit)
        divine_path_layout.addWidget(change_divine_button)
        main_layout.addLayout(divine_path_layout)
        # --- End Divine.exe Path Selection ---

        # File selection
        file_layout = QHBoxLayout()
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("Select a package file (.pak, .lsv)")
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(QLabel("Package File:"))
        file_layout.addWidget(self.file_path_edit)
        file_layout.addWidget(browse_button)
        main_layout.addLayout(file_layout)

        # Game selection
        game_layout = QHBoxLayout()
        self.game_combo = QComboBox()
        self.game_combo.addItems(["bg3", "dos2de", "dos2", "dosee", "dos"]) # Add more if needed
        game_layout.addWidget(QLabel("Game:"))
        game_layout.addWidget(self.game_combo)
        game_layout.addStretch()
        main_layout.addLayout(game_layout)

        # List button
        list_button = QPushButton("List Package Contents")
        list_button.clicked.connect(self.list_contents)
        main_layout.addWidget(list_button)

        # Output area
        self.output_view = QTreeView() # Renamed from output_text
        # self.output_view.setReadOnly(True) # Removed: QTreeView has no setReadOnly
        self.output_model = QStandardItemModel() # Create the model
        self.output_view.setModel(self.output_model) # Set the model for the view
        self.output_view.setHeaderHidden(True) # Hide default header
        main_layout.addWidget(QLabel("Contents:"))
        main_layout.addWidget(self.output_view)

        # Process for running Divine
        self.process = QProcess(self)

        self.process = QProcess(self)

        # --- Divine.exe Path Handling ---
        self.keyring_service_name = "LSLibDivineGUI"
        self.keyring_username = "DivineExePath"
        self.divine_path = self.get_divine_path()

        # Removed automatic prompting: if not self.divine_path:
        #    self.prompt_for_divine_path()

        # Update the display field if path is found or set
        if self.divine_path:
            self.divine_path_edit.setText(self.divine_path)
        else:
            self.divine_path_edit.setPlaceholderText("Divine.exe path not set. Click 'Change...'")
        # --- End Divine.exe Path Handling ---

        # Connect QProcess signals
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)

    def get_divine_path(self):
        """Attempts to retrieve the Divine.exe path from keyring."""
        try:
            path = keyring.get_password(self.keyring_service_name, self.keyring_username)
            if path and os.path.exists(path):
                print(f"Found Divine.exe path in keyring: {path}") # Debug
                return path
            else:
                print("Divine.exe path not found in keyring or path is invalid.") # Debug
        except Exception as e:
            print(f"Error reading from keyring: {e}") # Debug
        return None

    def prompt_for_divine_path(self):
        """Prompts the user to select Divine.exe and saves it to keyring."""
        QMessageBox.information(self, "Divine.exe Not Found",
                                "Please locate the Divine.exe executable.")
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Divine.exe",
            "", # Start directory
            "Executable Files (Divine.exe)"
        )
        if file_name and os.path.exists(file_name):
            try:
                keyring.set_password(self.keyring_service_name, self.keyring_username, file_name)
                self.divine_path = file_name
                self.divine_path_edit.setText(file_name) # Update the display field
                print(f"Saved Divine.exe path to keyring: {file_name}") # Debug
                QMessageBox.information(self, "Path Saved",
                                        f"Divine.exe path saved successfully: {file_name}")
            except Exception as e:
                print(f"Error saving to keyring: {e}") # Debug
                QMessageBox.critical(self, "Error",
                                     f"Could not save Divine.exe path to keyring.\nError: {e}")
                # Optionally, proceed without saving or ask again
                self.divine_path = file_name # Use the path for this session even if saving failed
                self.divine_path_edit.setText(file_name) # Update display field even if save failed
        else:
            # Don't show critical error if user simply cancelled the dialog
            # Only show if the file_name was invalid OR the initial check failed
            if file_name: # User selected something, but it wasn't valid
                 QMessageBox.warning(self, "Warning", "Invalid file selected for Divine.exe.")
            # If self.divine_path is STILL None after this, it means the initial load failed AND the user cancelled/failed selection
            if not self.divine_path:
                 QMessageBox.critical(self, "Error", "Divine.exe path not set. The application might not function correctly.")
            # Ensure display is cleared if path becomes invalid/unset
            if not self.divine_path:
                self.divine_path_edit.clear()


    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Package File",
            "", # Start directory
            "Package Files (*.pak *.lsv);;All Files (*)"
        )
        if file_name:
            self.file_path_edit.setText(file_name)

    def list_contents(self):
        package_path = self.file_path_edit.text()
        selected_game = self.game_combo.currentText()

        # --- Check Divine Path --- (Added Check)
        if not self.divine_path or not os.path.exists(self.divine_path):
            QMessageBox.warning(self, "Divine Path Missing",
                              "The path to Divine.exe is not set or is invalid.\nPlease use the 'Change...' button to set it.")
            return
        # --- End Check ---

        if not package_path or not os.path.exists(package_path):
            QMessageBox.warning(self, "Warning", "Please select a valid package file.")
            return

        # Removed redundant check for divine_path existence here
        # if not os.path.exists(self.divine_path):
        #     QMessageBox.critical(self, "Error", f"Divine.exe not found at: {self.divine_path}\nPlease ensure it's in the correct location.")
        #     return

        # Ensure model is cleared before listing new contents
        self.output_model.clear()
        # self.output_text.append(f"Listing contents of {package_path} for game {selected_game}...\n") # Will use model

        # Prepare arguments for QProcess
        arguments = [
            "--action", "list-package",
            "--game", selected_game,
            "--source", package_path
        ]

        print(f"Executing: {self.divine_path} with arguments: {arguments}") # Debug print
        # Start the process directly, letting QProcess handle executable/args
        self.process.start(self.divine_path, arguments)


    def add_path_to_model(self, path):
        """Adds a single file path to the QStandardItemModel, creating parent items as needed."""
        parts = path.strip().replace("\\", "/").split('/') # Normalize separators and split
        parent_item = self.output_model.invisibleRootItem()

        for i, part in enumerate(parts):
            if not part: # Skip empty parts (e.g., from leading/trailing slashes)
                continue

            found = False
            for row in range(parent_item.rowCount()):
                child = parent_item.child(row)
                if child and child.text() == part:
                    parent_item = child
                    found = True
                    break

            if not found:
                new_item = QStandardItem(part)
                # Optional: Set icons for folders/files if desired
                # You might need more logic to determine if it's a file or directory based on position
                # if i < len(parts) - 1:
                    # new_item.setIcon(QIcon.fromTheme("folder")) # Example
                # else:
                    # new_item.setIcon(QIcon.fromTheme("text-x-generic")) # Example

                parent_item.appendRow(new_item)
                parent_item = new_item # Descend into the newly created item


    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        text = bytes(data).decode('utf-8', errors='ignore')
        # Parse the output and add to the model
        lines = text.splitlines()
        for line in lines:
            if line.strip(): # Ignore empty lines
                self.add_path_to_model(line)
        # self.output_text.append(text) # Will populate model

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        text = bytes(data).decode('utf-8', errors='ignore')
        # self.output_text.append(f"ERROR: {text}") # Handle errors differently? Maybe status bar or popup

    def process_finished(self, exitCode, exitStatus):
        status_str = "finished successfully" if exitStatus == QProcess.ExitStatus.NormalExit and exitCode == 0 else "failed/crashed"
        # self.output_text.append(f"\nProcess {status_str} with exit code {exitCode}.") # Status update, maybe status bar



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PackageListerApp()
    window.show()
    sys.exit(app.exec())
