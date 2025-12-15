import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QFileDialog, QComboBox, QMessageBox
)

API_KEY = "paat-gffXox3xS6LvMNCSCCmXFKv6WLH"


# ---- REAL VERIFIED PICSART EFFECT LIST ----
EFFECT_LIST = [
    "1972", "apr1", "apr2", "apr3",
    "blur", "gblur", "lensblur", "motionblur", "smartblur", "pixelize",
    "brl1", "brnz1", "brnz2", "brnz3", "brnz4",
    "cyber1", "cyber2", "dodger", "fattal2",
    "food1", "food2",
    "light1", "light2", "light3", "light4", "light5",
    "light6", "light7", "light8", "light9", "light10",
    "light11", "light12", "light13", "light14", "light15",
    "light16", "light17", "light18", "light19", "light20",
    "mnch1", "mnch2", "mnch3",
    "nature1", "nature2",
    "noise", "ntrl1", "ntrl2",
    "popart", "saturation",
    "sft1", "sft2", "sft3", "sft4",
    "shadow1", "shadow2",
    "sketch1", "sketch2", "sketch3",
    "spc1", "tl1", "tl2",
    "urban1", "urban2",
    "water1", "water2",
]


# ---- APPLY EFFECT FUNCTION ----
def apply_effect(image_path, effect_name):
    url = "https://api.picsart.io/tools/1.0/effects"

    headers = {
        "X-Picsart-API-Key": API_KEY,
        "accept": "application/json"
    }

    data = {
        "effect_name": effect_name,
        "format": "PNG"
    }

    files = {
        "image": open(image_path, "rb")
    }

    # First request: triggers the Picsart effect
    response = requests.post(url, headers=headers, data=data, files=files)

    if response.status_code != 200:
        print("ERROR:", response.text)
        return None

    # Extract JSON
    json_data = response.json()

    # Extract the REAL processed image URL
    if "data" not in json_data or "url" not in json_data["data"]:
        print("API returned no URL:", json_data)
        return None

    image_url = json_data["data"]["url"]

    # Second request: download the actual edited image bytes
    img_data = requests.get(image_url)

    if img_data.status_code == 200:
        with open("output.png", "wb") as f:
            f.write(img_data.content)
        return "output.png"

    print("Failed to download final image:", img_data.text)
    return None


# ---- GUI ----
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Picsart Filter Selection")
        self.resize(400, 260)

        self.image_path = None

        self.label = QLabel("Select an image and choose a filter")
        self.effect_box = QComboBox()
        self.effect_box.addItems(EFFECT_LIST)

        self.pick_btn = QPushButton("Pick Image")
        self.pick_btn.clicked.connect(self.pick_image)

        self.apply_btn = QPushButton("Apply Filter")
        self.apply_btn.clicked.connect(self.apply_filter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.effect_box)
        layout.addWidget(self.pick_btn)
        layout.addWidget(self.apply_btn)
        self.setLayout(layout)

    def pick_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Choose Image", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.image_path = file_path
            self.label.setText(f"Selected: {file_path}")

    def apply_filter(self):
        if not self.image_path:
            QMessageBox.warning(self, "Error", "Pick an image first.")
            return

        effect = self.effect_box.currentText()
        success = apply_effect(self.image_path, effect)

        if success:
            QMessageBox.information(
                self, "Success",
                "Filter applied! Saved as output.png"
            )
        else:
            QMessageBox.critical(
                self, "Failure",
                "Could not apply your selected filter"
            )


app = QApplication([])
window = MyWindow()
window.show()
sys.exit(app.exec())