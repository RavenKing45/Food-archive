INDIA'S CULINARY MEMORY ARCHIVE — FOOD STORIES UPDATE

WHAT THIS UPDATE DOES
- Replaces the five generic Food Stories topics with eight researched stories.
- Makes each story card open a readable story panel.
- Adds a short historical narrative, an editorial caution where needed, and source links.
- Keeps the existing story-card design, colours, image placeholders, carousel motion, and STORY_IMAGES mechanism.
- Leaves all existing story images unchanged. No new images are included.
- Does not change app.py, state_pages.json, requirements.txt, the region grid, navigation, or food-record pages.

STORIES INCLUDED
1. Vada Pav: A Commuter's Food
2. Rasgulla: Two Regional Traditions
3. Pav Bhaji and the Mill City
4. Dal Baati: Food for the Road
5. Masala Dosa and Udupi's Reach
6. Chole Bhature after Partition
7. Galouti Kebab: A Soft Legend
8. Daulat Ki Chaat: Delhi's Winter Sweet

HELD BACK FOR FURTHER RESEARCH
- Dhokla: the proposed early textual references have not been checked against original manuscripts, editions, and passages.
- Nihari: the proposed Mughal, royal-kitchen, labourer, and soldier origin accounts lack sufficiently strong historical sources in the current research.
- Karachi Halwa: the migration context is plausible, but the sweet's origin and the cited confectionery-business histories remain insufficiently established.
- Benami Kheer: no reliable historical cookbook, manuscript, or court record was located for the garlic-based kheer or its claimed royal origin.

INSTALLATION — EASIEST METHOD
1. Back up your current index.html.
2. Copy index_food_stories_updated.html from this package into your project root.
3. Rename it to index.html, replacing the existing homepage.
4. Keep your existing assets/stories folder exactly as it is.
5. Restart Streamlit / redeploy the existing app.

OPTIONAL REBUILD METHOD
If you later want to reapply the story data to a fresh copy of the original homepage:
1. Put apply_food_stories.py and food_stories.json beside your current index.html.
2. Run: python apply_food_stories.py
3. The script creates index_food_stories_updated.html and does not overwrite the original.

CONTENT NOTES
- Dates and origin stories are qualified where evidence is uncertain.
- GI registrations are described as recognition of distinct regional products, not proof of historical priority.
- The 160-spice claim is kept specific to the Tunday Kebab tradition, not all Galouti kebabs.
- The Bappa Rawal/battlefield baati, toothless-Nawab, dew, and other oral-origin stories are labelled as tradition or uncertainty rather than established fact.
- The story images remain exactly as they currently appear; placeholder visuals are not presented as historical evidence.

PACKAGE FILES
- index_food_stories_updated.html: ready-to-use replacement homepage.
- food_stories.json: editable story content and source metadata.
- apply_food_stories.py: optional standard-library installer to regenerate the replacement from a fresh current index.html.
- FOOD_STORIES_SOURCE_AUDIT.csv: included/held story list, word counts, source counts, and editorial cautions.

VALIDATION
- 8 included stories and 4 held stories.
- JSON structure validated.
- Generated JavaScript syntax checked with Node.js.
- Existing navigation, region search/grid, and story-image injection markers preserved.
