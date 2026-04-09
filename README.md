# Photo Sorter

A lightweight Python application to organize photos by pressing number keys. Browse through images and sort them into numbered folders with an intuitive GUI.

## Features

- **Simple GUI** - Display photos one at a time in a clean interface
- **Quick Sorting** - Press 0-9 to move photos into corresponding numbered folders
- **Navigation** - Use arrow keys (↑↓) to browse through remaining photos
- **Live Count** - See how many photos are left to sort
- **Folder List** - See all remaining photos in a sidebar listbox
- **Auto-Create Folders** - Destination folders (0-9) are created automatically

## Requirements

- Python 3.8+
- Pillow (PIL)
- tkinter (usually included with Python)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/photo-sorter.git
   cd photo-sorter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Option 1: Run with Python
```bash
python photo_sorter.py
```

### Option 2: Use the compiled EXE (Windows)
First, build the executable:
```bash
build_exe_en.bat
```

Then run:
```
dist\PhotoSorter.exe
```

## Controls

- **0-9** - Move current photo to the corresponding folder
- **↑↓** - Navigate through the photo list
- **ESC** - Exit the application

## How It Works

1. Start the application
2. Select a folder containing photos
3. The app displays the first photo
4. Press a number (0-9) to move the photo to that numbered folder
5. The next photo automatically loads
6. Use arrow keys to browse through remaining photos
7. Continue until all photos are sorted

## Project Structure

```
photo-sorter/
├── photo_sorter.py      # Main application
├── build_exe_en.bat     # Build script for Windows EXE
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── LICENSE             # MIT License
```

## Building EXE

To create a standalone executable on Windows:
```bash
build_exe_en.bat
```

This will create `dist\PhotoSorter.exe` which doesn't require Python to be installed.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Created for efficient photo organization workflows.
