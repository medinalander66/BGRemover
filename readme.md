# High-Resolution Background Remover

A small Tkinter desktop application that removes image backgrounds with `rembg` and saves the result as a transparent PNG. The original image resolution is preserved.

## Requirements

- Windows
- Python 3.9 or newer
- Internet access for the first `rembg` model download

## Installation

Open PowerShell in this folder and run:

```powershell
py -m pip install Pillow rembg
```

If pip is not available, run:

```powershell
py -m ensurepip --upgrade
py -m pip install Pillow rembg
```

## Run the application

```powershell
py .\bg_remover.py
```

A window will open. Select an input image, choose an output location, and click **Remove Background**.

## Supported input formats

- JPG/JPEG
- PNG
- BMP
- TIFF

The output is always saved as a PNG file so transparency can be preserved.

## Troubleshooting

### `ModuleNotFoundError: No module named 'PIL'`

Install Pillow using the same Python launcher used to run the app:

```powershell
py -m pip install Pillow
```

### `ModuleNotFoundError: No module named 'rembg'`

Install rembg:

```powershell
py -m pip install rembg
```

Using `py -m pip` helps ensure the packages are installed for the same Python interpreter that runs the application.
