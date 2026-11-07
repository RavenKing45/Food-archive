INDIA'S CULINARY MEMORY ARCHIVE — CONTENT AND CLASSIFICATION UPDATE

This package updates the regional content and record classification for all
72 food records, adds the Diu Hoka Fruit entry, and makes State / Union
Territory labels read from one shared data field.

FILES TO REPLACE
1. app.py
2. index.html
3. state_pages.json

NEW IMAGE
Copy assets/dishes/hoka-fruit.webp into your existing assets/dishes/ folder.
This image is the replacement photo previously installed under the old
bebinca-diu.webp slug.

INSTALLATION (PowerShell, from your project root)
1. Back up app.py, index.html and state_pages.json.
2. Extract this ZIP into the project root and allow the three files to be
   replaced and the assets/dishes folder to be merged.
3. The ZIP adds assets/dishes/hoka-fruit.webp.
4. After confirming the Diu page displays Hoka Fruit correctly, the old
   assets/dishes/bebinca-diu.webp file can be removed because the Diu data
   no longer references that slug:

   Remove-Item .\assets\dishes\bebinca-diu.webp -ErrorAction SilentlyContinue

5. Restart Streamlit.

No change to requirements.txt is needed. Existing images and page content for
the other 71 entries are retained. The old Diu Bebinca entry is replaced by
Hoka Fruit of Diu. Daman Jetty Roll remains unchanged.

WHAT CHANGED
- All 72 food records now include classification.recordType,
  classification.foodForm and classification.definition.
- The Hoka Fruit entry has foodCharacteristics and consumption fields; its
  page uses those instead of Ingredients and Preparation.
- Both homepage cards and chapter headings use administrativeType from
  state_pages.json. The previous duplicated hard-coded UT lists were removed.
- Goa remains a State. The eight current Union Territories are correctly
  identified separately.

AUDIT FILES
- region_type_audit.csv: each of the 36 regions and its administrative type.
- food_classification_audit.csv: all 72 food names and classifications.
- CLASSIFICATION_AND_REGION_AUDIT.txt: definitions and rationale.

The change is local only. It does not push or modify your GitHub repository.
