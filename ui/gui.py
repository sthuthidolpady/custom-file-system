import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QListWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox,
    QInputDialog, QLabel, QProgressBar
)
from backend.file_system import FileSystem


TOTAL_STORAGE = 1024 * 1024  # 1 MB (PRD requirement)


class FileSystemGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.fs = FileSystem()
        self.init_ui()
        self.refresh()

    def init_ui(self):
        self.setWindowTitle("File System Manager")
        self.setGeometry(200, 100, 900, 650)

        # Light theme
        self.setStyleSheet("""
            QWidget { background-color: #f4f6f8; font-size: 14px; }
            QListWidget { background-color: white; border: 1px solid #ccc; }
        """)

        self.list = QListWidget()

        # Buttons
        btn_create = QPushButton("Create")
        btn_read = QPushButton("Read")
        btn_write = QPushButton("Write")
        btn_delete = QPushButton("Delete")
        btn_rename = QPushButton("Rename")
        btn_props = QPushButton("Properties")

        btn_create.clicked.connect(self.create_file)
        btn_read.clicked.connect(self.read_file)
        btn_write.clicked.connect(self.write_file)
        btn_delete.clicked.connect(self.delete_file)
        btn_rename.clicked.connect(self.rename_file)
        btn_props.clicked.connect(self.show_props)

        # Button colors
        btn_create.setStyleSheet("background:#4CAF50;color:white;padding:8px;")
        btn_read.setStyleSheet("background:#2196F3;color:white;padding:8px;")
        btn_write.setStyleSheet("background:#FF9800;color:white;padding:8px;")
        btn_delete.setStyleSheet("background:#F44336;color:white;padding:8px;")
        btn_rename.setStyleSheet("background:#9C27B0;color:white;padding:8px;")
        btn_props.setStyleSheet("background:#009688;color:white;padding:8px;")

        right = QVBoxLayout()
        for b in [btn_create, btn_read, btn_write, btn_delete, btn_rename, btn_props]:
            right.addWidget(b)
        right.addStretch()

        # 🔹 Storage UI (PRD)
        self.storage_label = QLabel("Storage: 0 B / 1 MB")
        self.storage_bar = QProgressBar()
        self.storage_bar.setMaximum(100)

        # Layout
        main = QHBoxLayout()
        main.addWidget(self.list, 3)
        main.addLayout(right, 1)

        wrapper = QVBoxLayout()
        wrapper.addLayout(main)
        wrapper.addWidget(self.storage_label)
        wrapper.addWidget(self.storage_bar)

        self.setLayout(wrapper)

    def refresh(self):
        self.list.clear()
        self.list.addItems(self.fs.list_files())
        self.update_storage()

    def selected_file(self):
        item = self.list.currentItem()
        return item.text() if item else None

    # ---------- File Ops ----------
    def create_file(self):
        name, ok = QInputDialog.getText(self, "Create", "Filename:")
        if ok and name:
            self.fs.create_file(name)
            self.refresh()

    def read_file(self):
        name = self.selected_file()
        if name:
            QMessageBox.information(self, "Read", self.fs.read_file(name))

    def write_file(self):
        name = self.selected_file()
        if name:
            data, ok = QInputDialog.getMultiLineText(self, "Write", "Content:")
            if ok:
                self.fs.write_file(name, data)
                self.refresh()

    def delete_file(self):
        name = self.selected_file()
        if name:
            self.fs.delete_file(name)
            self.refresh()

    def rename_file(self):
        old = self.selected_file()
        if old:
            new, ok = QInputDialog.getText(self, "Rename", "New name:")
            if ok and new:
                self.fs.rename_file(old, new)
                self.refresh()

    def show_props(self):
        name = self.selected_file()
        if name:
            info = self.fs.file_info(name)
            msg = "\n".join(f"{k}: {v}" for k, v in info.items())
            QMessageBox.information(self, "Properties", msg)

    # ---------- Storage ----------
    def update_storage(self):
        used = 0
        for f in self.fs.list_files():
            used += self.fs.file_info(f)["Size (bytes)"]

        percent = int((used / TOTAL_STORAGE) * 100) if TOTAL_STORAGE else 0
        self.storage_bar.setValue(min(percent, 100))
        self.storage_label.setText(
            f"Storage: {used} B / 1 MB"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = FileSystemGUI()
    w.show()
    sys.exit(app.exec_())
