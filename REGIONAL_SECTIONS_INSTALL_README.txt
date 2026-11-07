REGIONAL GEOGRAPHY + FOOD CULTURE UPDATE

Files in this package:
- app.py: renders the two regional information sections as compact category-led editorial panels.
- state_pages.json: structured content and section-specific source links for all 36 regions.
- region_sections_content_audit.csv: category and source-link audit for all regions.

What changed:
1. Replaced the old one-paragraph "geography" and "culinaryLandscape" fields with:
   - regionalGeography.items: Land & water; Soil & crops; Climate & seasons; Food connection.
   - foodCulture.items: Staple foods; Popular food types; Regional preferences; Traditional ingredients; Cooking & eating practices.
2. Each section has its own clickable source list.
3. Category labels, short paragraphs and source links use the existing vintage serif typography, maroon/brown palette and subtle dividers.
4. Regional content is written separately for each of the 36 regions. The wording avoids treating one community's food habits as universal.
5. State/Union Territory administrativeType fields are unchanged. The 28 States and 8 Union Territories remain correctly identified.
6. All 72 dish records, dish classifications, images/slugs, ingredients, preparation steps, history, oral narratives and dish references were preserved unchanged.
7. Hoka Fruit remains classified as a Traditional edible fruit; this update did not alter its record.
8. index.html is not included because it was not modified.

Installation:
1. Back up app.py and state_pages.json.
2. Extract this ZIP in the project root (the folder containing app.py and index.html), allowing app.py and state_pages.json to be replaced.
3. Keep index.html, assets/, requirements.txt and every other project file unchanged.
4. Restart Streamlit.

Validation:
- JSON parses successfully.
- 36 regional entries retained (28 States and 8 Union Territories).
- Every region has 4 Regional Geography items and 5 Food Culture & Preferences items.
- Every section has supporting source links (150 section-specific links across the archive).
- 72 dish arrays compared against the previous archive package: no dish records changed.
- app.py Python syntax compiled successfully.
- Embedded JavaScript passed node --check.

Editorial note:
These summaries are concise regional overviews, not claims that every household or community eats the same way. Where a region contains distinct ecological zones or communities, the wording notes variation. The source links are provided for further reading and verification; state-level sources do not necessarily establish identical conditions in every district.
