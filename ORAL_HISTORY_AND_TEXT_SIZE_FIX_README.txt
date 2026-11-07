ORAL HISTORY DISPLAY + DISH TEXT SIZE FIX

FILES
- app.py: replacement Streamlit app with two targeted fixes.

CHANGES
1. The Oral narrative panel is displayed only when that dish has a non-empty, attributed oralNarrative record.
2. Dishes without a documented oral account no longer show a placeholder or an empty panel.
3. When no oral narrative exists, the historical photograph/document panel uses the available row width instead of leaving an empty second column.
4. The descriptive text beside the main food photograph (About this food and Historical background) is enlarged from 12px to 14px, with a slightly more open line height.

SCOPE
- No dish content or existing source URLs were changed.
- All 72 food records and the Hoka Fruit classification remain in state_pages.json unchanged.
- No image, index.html, navigation, ingredients, preparation steps, or other component needs replacement.

INSTALLATION
1. Back up the current app.py.
2. Extract this ZIP into the project root, replacing app.py.
3. Keep your existing state_pages.json, index.html and assets folders.
4. Restart Streamlit.
