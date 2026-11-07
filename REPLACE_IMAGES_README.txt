IMAGE REPLACEMENT PACKAGE — FOOD ARCHIVE

This package contains 15 replacement images only. It does not modify app.py, index.html, or state_pages.json.

WINDOWS POWERSHELL (run from your project root):
  Expand-Archive -LiteralPath ".\dish_image_replacements.zip" -DestinationPath "." -Force

The ZIP contains assets/dishes/<existing-filename>, so the corresponding old image files are overwritten.

MAC / LINUX (run from your project root):
  unzip -o dish_image_replacements.zip -d .

IMPORTANT — HOKA FRUIT TEMPORARY FILENAME:
  The Hoka fruit photo is currently named assets/dishes/bebinca-diu.webp because the Diu page still uses the existing Bebinca slug. This is intentional so the image can be replaced now without changing page content. When the content and classification are updated, rename the file and slug together to hoka-fruit.webp / hoka-fruit.

Before extracting, make a backup of your current assets/dishes folder.
