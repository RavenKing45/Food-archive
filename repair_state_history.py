#!/usr/bin/env python3
"""Targeted repair of historical-background copy in state_pages.json.

Run from the project root:
    python repair_state_history.py

Reads state_pages.json and writes state_pages_improved.json. It changes ONLY
`dishes[*].history`; all region metadata, dish names, overview text, image
references, sources, oral narratives and other fields are preserved.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "state_pages.json"
OUTPUT = ROOT / "state_pages_improved.json"

HISTORY_UPDATES: dict[str, dict[str, str]] = {
    "punjab": {
        "Sarson da Saag with Makki di Roti": (
            "The pairing grew from the rhythm of Punjabi winter farming. Mustard greens were gathered in season, while maize became an important grain across the northwestern plains. Rural households brought the two together in a filling winter meal, and the combination later became a familiar emblem of Punjabi food in village homes, roadside dhabas and city restaurants."
        ),
        "Chole Bhature": (
            "The pairing took shape in the bustling food culture of North Indian towns, where hearty chickpea curries were served alongside breads from Punjabi kitchens. After Partition, Punjabi cooks and food businesses carried the combination into Delhi and other cities. Street stalls and neighbourhood restaurants helped turn it into a much-loved breakfast and everyday meal."
        ),
    },
    "west-bengal": {
        "Shorshe Ilish": (
            "Hilsa has long followed the rivers and estuaries of Bengal, making it part of the region's seasonal fishing and food culture. Mustard, grown and pressed across eastern India, became a defining partner for the rich fish. The dish moved between home kitchens and festive meals, and hilsa itself became closely associated with the monsoon and Bengali food identity."
        ),
        "Banglar Rosogolla": (
            "Bengal's sweet shops helped shape the modern rosogolla into a celebrated urban confection. In nineteenth-century Calcutta, confectioners developed new ways of working with chhana, and Nabin Chandra Das became closely associated with the light, syrup-soaked version. Later, family businesses such as K. C. Das helped carry rosogolla beyond local shops through packaged sweets and wider distribution."
        ),
    },
    "tamil-nadu": {
        "Sakkarai Pongal": (
            "Sweet pongal belongs to the harvest celebrations of Tamil households. At Thai Pongal, newly harvested rice is cooked as an offering of gratitude for the land, the Sun and the animals that support farming. Over generations, jaggery, ghee and fragrant additions made the preparation a central festive food, shared at home and offered in temples."
        ),
        "Chicken Chettinad": (
            "Chettinad cooking was shaped by the journeys and trading networks of the Nattukottai Chettiar community. Connections across South and Southeast Asia brought ingredients and culinary ideas into local kitchens, where cooks developed distinctive roasted spice blends. Chicken Chettinad grew from this layered household tradition and later reached a much wider audience through Chettinad restaurants."
        ),
    },
    "kerala": {
        "Kerala Sadya": (
            "Large communal meals have long been part of Kerala's temple, harvest and household celebrations. The sadya grew within this culture of hospitality, where a shared meal marked an important occasion and brought seasonal produce from the surrounding region to the table. Onam made one form especially recognisable, while temple festivals, weddings and family gatherings kept the wider feast tradition alive."
        ),
        "Puttu and Kadala Curry": (
            "Puttu became a familiar part of Kerala's everyday food culture in rice-growing communities where coconut was also a common household ingredient. Steaming offered a practical way to turn rice flour into a satisfying meal, while pulses made a substantial accompaniment. The pairing of puttu with kadala curry became a classic breakfast across Kerala, especially in Malabar and coastal towns."
        ),
    },
    "rajasthan": {
        "Dal Baati Churma": (
            "Dal baati grew from the food traditions of Rajasthan's dry regions, where wheat, pulses and ghee were important parts of the household store. Baati was well suited to cooking over local hearths and carrying on journeys; dal made the meal complete, while churma added a festive sweet element. The combination moved from practical household food into feasts and celebrations."
        ),
        "Gatte ki Sabzi": (
            "In Rajasthan's dry climate, cooks made inventive use of ingredients that could be stored in the household pantry. Gram flour became a dependable base for substantial meals, while yoghurt and spices brought richness to everyday cooking. Gatte ki sabzi grew from this style of resourceful regional cooking and became a familiar part of meals across Rajasthan."
        ),
    },
    "gujarat": {
        "Undhiyu": (
            "Undhiyu is closely tied to the winter harvest of south Gujarat, especially the food culture of Surat. When seasonal vegetables and fresh beans were plentiful, households brought them together for a generous shared meal. It became a special part of winter gatherings and Uttarayan celebrations, with families and neighbourhoods preparing the dish for guests and festivals."
        ),
        "Dhokla": (
            "Gujarati cooks developed a wide family of steamed and fermented snacks using grains and pulses. Earlier Gujarati food writing includes references to preparations related to dhokla, while household methods continued to evolve across communities. Over time, dhokla became part of the region's everyday farsan culture, sold by snack shops and served at home, gatherings and celebrations."
        ),
    },
    "maharashtra": {
        "Vada Pav": (
            "Vada pav became part of Mumbai's working-city food culture as railway commuters, mill workers and street vendors shaped a demand for inexpensive, filling food that could be eaten quickly. The meeting of a spiced potato vada with bakery pav suited the pace of the city. Dadar's Ashok Vaidya became one of the best-known names associated with its rise, and stalls across Mumbai carried it into everyday life."
        ),
        "Puran Poli": (
            "Puran poli became a treasured festive preparation in Marathi households, especially around celebrations such as Gudi Padwa and Holi. Sweet filled breads have long circulated across western and southern Indian food traditions, with each region developing its own name and style. In Maharashtra, the preparation came to represent the labour and generosity of festival cooking, shared with family and guests."
        ),
    },
    "karnataka": {
        "Mysore Pak": (
            "Mysore Pak is remembered through the culinary traditions of the Mysore Palace during the Wadiyar era. Local accounts associate its creation with palace cook Kakasura Madappa, whose combination of gram flour, sugar and ghee became a favourite sweet. From palace kitchens the preparation entered Mysore's sweet shops, where confectioners developed the soft and firm styles enjoyed today."
        ),
        "Bisi Bele Bath": (
            "Bisi bele bath belongs to the rice-and-lentil cooking tradition of the Mysuru region. Household cooks brought grains, pulses, vegetables and a roasted spice mixture together in a single nourishing meal, suited to family kitchens and communal dining. As Karnataka's tiffin houses and restaurants grew, the dish travelled well beyond its home region and became a familiar part of the state's food identity."
        ),
    },
    "uttar-pradesh": {
        "Galouti Kebab": (
            "Galouti kebab emerged from the celebrated kebab culture of Awadh, where cooks in Lucknow's elite kitchens refined minced-meat preparations with aromatic spices and delicate textures. The city's specialist cooks developed a rich repertoire of kebabs for royal tables and formal hospitality. From these kitchens, galouti became one of Lucknow's best-known culinary signatures and later a mainstay of its restaurants."
        ),
        "Awadhi Dum Pukht Biryani": (
            "Lucknow's dum pukht tradition reflects the meeting of Persianate and North Indian courtly food cultures. Awadhi cooks adapted rice-and-meat preparations to local tastes, using sealed vessels and slow cooking to build aroma and tenderness. The method became closely associated with Nawabi hospitality and spread through the city's professional cooks, kitchens and restaurants."
        ),
    },
    "assam": {
        "Assamese Khar": (
            "Khar reflects a distinctive Assamese cooking tradition built around the knowledge of plant ash and alkaline extracts. Families learned to prepare kola khar from parts of the banana plant and use it to shape the flavour of everyday meals. The technique became a recognisable part of Assamese food culture, linking household knowledge of local plants with a regional style of cooking."
        ),
        "Masor Tenga": (
            "Assam's rivers and wetlands have made freshwater fish central to daily food culture. Cooks developed light sour preparations that suited the local catch and balanced the richness of fish with ingredients gathered or grown in different seasons. The use of tomato, thekera, elephant apple and other souring fruits gives each household and region its own version of masor tenga."
        ),
    },
    "andhra-pradesh": {
        "Gongura Pachadi": (
            "Gongura became one of the defining flavours of Andhra kitchens, particularly in the Guntur region where the sour leaves are widely used. Household cooks turned the seasonal greens into chutneys and pickles that could be kept and enjoyed with rice through the year. The preparation's strong flavour and everyday presence helped make gongura a marker of Andhra food identity."
        ),
        "Pootharekulu": (
            "Pootharekulu grew into a celebrated sweet of Atreyapuram in the Godavari delta, where rice-growing households developed a highly skilled way of making delicate rice sheets. The work of preparing and folding the thin layers became a craft passed through families and local sweet makers. The village's reputation for the paper-like sweet spread across Andhra Pradesh, and its GI recognition strengthened its regional identity."
        ),
    },
    "arunachal-pradesh": {
        "Apong": (
            "Rice fermentation is part of the household knowledge of several communities in Arunachal Pradesh. Families prepare apong for social visits, community gatherings, festivals and important ceremonies, using starter cultures whose preparation is passed between generations. The drink reflects the place of rice in local agriculture and the way food and hospitality are woven into community life."
        ),
        "Bamboo Shoot Curry": (
            "Bamboo shoots are gathered as a seasonal food across Arunachal Pradesh and the eastern Himalayas. Communities developed ways to eat the tender shoots fresh and preserve them through fermentation or drying, extending their use beyond the harvest season. These practices made bamboo a valued part of household food stores and gave local curries their distinctive regional character."
        ),
    },
    "bihar": {
        "Litti Chokha": (
            "Litti chokha is rooted in the agrarian foodways of the Bhojpuri region, where wheat, roasted gram and seasonal vegetables shaped everyday meals. The sattu-filled litti could be roasted over a household fire and carried easily by farmers and travellers. It later moved from village kitchens into town markets and street stalls, becoming one of Bihar's best-known foods."
        ),
        "Silao Khaja": (
            "Silao khaja is tied to the sweet-making tradition of Silao in Nalanda, a town connected to the wider movement of residents, visitors and pilgrims through the region. Local confectioners built a reputation for its delicate layers and crisp texture, passing the careful preparation from one generation of sweet makers to the next. The sweet remains a recognised specialty of the area."
        ),
    },
    "chhattisgarh": {
        "Chila": (
            "Chila reflects the importance of rice and lentils in Chhattisgarh's household food traditions. Cooks turned familiar grains into a simple griddle meal that could be prepared in village kitchens and served as breakfast or a light snack. Its place in everyday cooking helped it move from home meals into local stalls and community food gatherings."
        ),
        "Aamat": (
            "Aamat is associated with the food traditions of Bastar, where local cooking draws on vegetables, forest produce and bamboo. Communities developed ways of preparing seasonal ingredients over the hearth, including cooking in bamboo tubes that lend their own aroma. The dish carries the character of Bastar's landscape and the knowledge of local household cooks."
        ),
    },
    "goa": {
        "Xacuti": (
            "Xacuti grew within Goa's Konkani food culture, where coconut and local spice traditions met ingredients and cooking influences carried through centuries of coastal trade and Portuguese rule. Household cooks developed richly roasted masalas for family meals and celebrations, with variations across communities. The curry became one of the recognisable preparations of Goan home and restaurant cooking."
        ),
        "Bebinca": (
            "Bebinca reflects the layered culinary exchange that shaped Goan Catholic cooking. Local coconut, eggs and ghee came together with baking practices associated with Portuguese-era kitchens and convents. Over generations, families made the labour-intensive dessert for Christmas, Easter, weddings and other celebrations, turning it into one of Goa's most recognisable festive sweets."
        ),
    },
    "haryana": {
        "Bajra Khichdi": (
            "Pearl millet has long been important to farming in Haryana's dry and semi-arid landscapes. Rural households used the grain in winter meals, often combining it with pulses to make a sustaining dish from crops stored after harvest. Bajra khichdi became closely associated with the season, village life and harvest celebrations, including Makar Sankranti."
        ),
        "Haryanvi Kadhi": (
            "Kadhi has a broad history across northwestern India, and Haryana's version grew from the food habits of dairy- and grain-producing villages. Sour curd and gram flour were familiar household staples, making the curry a practical way to bring them together. Served with local breads and rice, it became a regular part of home cooking across the region."
        ),
    },
    "himachal-pradesh": {
        "Himachali Dham": (
            "Dham grew from the temple and community feasts of Himachal Pradesh, where major festivals, weddings and religious gatherings called for cooks able to prepare meals for large groups. The specialist cooks known as botis carried this knowledge between events and generations. Regional menus developed across the hill districts, giving each area's dham its own character."
        ),
        "Siddu": (
            "Siddu belongs to the wheat-growing food traditions of Himachal's hill communities. Families adapted familiar bread-making skills to the mountain climate, using fermentation and steaming to prepare a substantial meal for cold days. Fillings and accompaniments vary between households, and the bread moved from village kitchens into local eateries as a familiar expression of Pahari cooking."
        ),
    },
    "jharkhand": {
        "Dhuska": (
            "Dhuska grew from the rice-and-pulse food culture of Jharkhand, where household cooks turned everyday grains into a crisp snack for family meals and gatherings. Its popularity spread through local markets and town food stalls, where it is often served with curry. The snack remains a familiar part of the region's street-food identity."
        ),
        "Rugra": (
            "Rugra is tied to the monsoon cycle of Jharkhand's sal forests. Adivasi and other local communities gather the seasonal mushrooms as part of a wider knowledge of edible forest foods, then bring them to village markets and household kitchens. Its short season gives rugra a special place in local food culture and connects the harvest to the rhythms of the forest."
        ),
    },
    "madhya-pradesh": {
        "Indori Poha": (
            "Flattened rice has long been eaten across central India, but Indore's markets and street vendors gave poha a distinctive local identity. Vendors built a recognisable breakfast ritual around sev, jeeravan, onions and lemon, often paired with jalebi. The combination became part of the city's morning food culture and a point of pride for Indore."
        ),
        "Dal Bafla": (
            "Dal bafla is a Malwa expression of the wider wheat-and-lentil food culture shared across central and western India. Local cooks adapted the idea of baati to Malwa kitchens, using a preparation that produces a softer centre and serving it with dal and ghee. The meal became a familiar part of family feasts and regional restaurant menus."
        ),
    },
    "manipur": {
        "Eromba": (
            "Eromba reflects the central place of ngari in Meitei food culture. Fermented fish developed as a valued way to preserve the catch and bring a deep savoury flavour to household meals. Cooks combined it with vegetables and chillies from the kitchen garden, creating a dish that became a familiar accompaniment to rice and a marker of Manipuri cooking."
        ),
        "Chak Hao Kheer": (
            "Chak hao is an aromatic black rice cultivated in Manipur and valued in both everyday and ceremonial food traditions. Its striking colour and fragrance made it a special grain for family celebrations, community feasts and festive offerings. Preparing it as kheer brought the local rice into a celebratory sweet, while growers and cooks continue to preserve its place in Manipuri food culture."
        ),
    },
    "meghalaya": {
        "Jadoh": (
            "Jadoh is closely connected to Khasi food culture, where rice and pork have long been part of home meals and communal gatherings. The one-pot preparation reflects the practical cooking of hill households and the importance of shared food at community occasions. It also became a familiar part of Shillong's market and restaurant culture, carrying Khasi flavours to new audiences."
        ),
        "Tungrymbai": (
            "Tungrymbai belongs to the fermented food traditions of the Khasi and Jaintia communities. Fermenting soybeans in leaf-lined baskets allowed households to preserve a nutritious ingredient and develop a flavour used in everyday meals. The preparation and its household methods have been passed through generations, making tungrymbai an important part of local food identity."
        ),
    },
    "mizoram": {
        "Bai": (
            "Bai grew out of Mizo household cooking, where meals draw on seasonal greens, garden vegetables and ingredients gathered from the surrounding hills. Families adapted the stew to what was available, creating many versions that change with the season and community. Its place at the family table reflects a tradition of simple, shared cooking built around local produce."
        ),
        "Vawksa Rep": (
            "Smoking pork over the household hearth became an important preservation practice in Mizo food culture. The smoke helped families keep meat for later meals while giving it a distinctive flavour. Over time, smoked pork became more than a way to store food: it developed into a valued ingredient for stews and dishes served at family gatherings and celebrations."
        ),
    },
    "nagaland": {
        "Smoked Pork with Bamboo Shoot": (
            "Smoking meat over the hearth is a long-standing food practice across Naga communities, allowing households to preserve pork between occasions when fresh meat was available. Bamboo shoots, gathered seasonally from nearby forests, became a natural partner in stews and shared meals. The combination reflects the close relationship between Naga cooking, forest produce and communal food traditions."
        ),
        "Axone": (
            "Axone, or akhuni, belongs to the fermented soybean traditions of several Naga communities. Household makers developed ways to ferment and store soybeans, creating a strong-flavoured ingredient that could season meals throughout the year. The knowledge of preparing and using axone is passed through families and communities, and it remains a distinctive part of Naga cuisine."
        ),
    },
    "odisha": {
        "Dalma": (
            "Dalma is deeply rooted in Odia home cooking and is also associated with the food culture surrounding Lord Jagannath in Puri. The combination of pulses and locally grown vegetables reflects the region's agrarian pantry and preference for balanced, simple meals. Over generations, household and temple food traditions helped make dalma one of Odisha's best-known preparations."
        ),
        "Chhena Poda": (
            "Chhena poda is closely associated with Nayagarh, where local sweet makers turned fresh chhena into a distinctive baked dessert. The story is linked to sweet-maker Sudarshana Sahoo and the discovery of baking sweetened chhena in a warm oven. From local shops, the dessert spread across Odisha and became one of the state's most recognisable sweets."
        ),
    },
    "sikkim": {
        "Phagshapa": (
            "Phagshapa is part of Bhutia food culture in Sikkim, where pork and hardy vegetables have long featured in household meals. The dish reflects the food habits of Himalayan communities, using ingredients that keep well and provide a sustaining meal in colder weather. It remains a familiar preparation at home and in eateries serving regional Sikkimese food."
        ),
        "Gundruk": (
            "Gundruk is part of a wider Himalayan preservation tradition shared by Nepali-speaking communities, including those in Sikkim. Families fermented surplus mustard and radish leaves when greens were plentiful, then dried them for use in later months. The practice carried seasonal harvests into everyday soups and meals and travelled with communities across the Himalayan region."
        ),
    },
    "telangana": {
        "Hyderabadi Biryani": (
            "Hyderabadi biryani grew in the courtly kitchens of the Asaf Jahi Nizams, where Persianate and Mughal rice traditions met the ingredients and tastes of the Deccan. Local cooks developed a distinctive style that became part of Hyderabad's ceremonial and hospitality culture. Restaurants and family kitchens later carried the dish into the city's everyday identity and far beyond."
        ),
        "Sarva Pindi": (
            "Sarva pindi comes from Telangana's rural home kitchens, where rice flour and familiar pantry ingredients were turned into a filling meal on a household pan. Peanuts, sesame and chillies reflected crops and flavours common to the region. The preparation travelled through family food traditions and local tiffin stalls, remaining a recognisable Telangana snack."
        ),
    },
    "tripura": {
        "Mui Borok": (
            "Mui borok reflects the importance of fermented fish in Tripuri food traditions. Preserving fish allowed households to keep the flavour of the catch and use it to season meals beyond the fishing season. The preparation became a defining part of Indigenous Tripuri cooking, appearing in household curries, chutneys and shared meals with rice."
        ),
        "Chakhwi": (
            "Chakhwi reflects Tripura's Indigenous use of bamboo shoots and seasonal ingredients gathered from the surrounding landscape. Families developed variations using local herbs and, in some homes, meat or fish. The dish remains part of everyday Tripuri food culture and shows how forest produce and household knowledge shape regional cooking."
        ),
    },
    "uttarakhand": {
        "Kafuli": (
            "Kafuli grew from the food traditions of Kumaon and Garhwal, where terraced farms and kitchen gardens supplied leafy greens for much of the year. Household cooks turned seasonal greens into a substantial meal using familiar grains and local dairy. The dish became a valued part of hill cooking, especially when families gathered around the winter hearth."
        ),
        "Bal Mithai": (
            "Bal mithai became a signature sweet of Almora through the work of local halwais and the town's traditional sweet shops. Its roasted khoya centre and sugar-coated finish made it distinctive among Kumaoni sweets. As visitors and traders carried it beyond the hill town, bal mithai became one of the best-known edible symbols of Almora."
        ),
    },
    "andaman-and-nicobar-islands": {
        "Andaman Fish Curry": (
            "The Andaman Islands' food culture has been shaped by the sea and by communities who arrived from different parts of the Indian mainland. Bengali, Tamil and other regional cooking traditions met the island's fresh catch and local produce, creating many styles of fish curry. The dish is best understood as part of this layered coastal food culture, rather than one fixed island recipe."
        ),
        "Nicobari Aloo Preparation": (
            "Tubers have an important place in Nicobarese food systems, alongside coconut, fishing and animal husbandry. Families cultivate and prepare local varieties as part of everyday meals and village celebrations, passing knowledge of the crops through generations. Nicobari aloo reflects the close relationship between island agriculture, community life and the foods grown in local gardens."
        ),
    },
    "chandigarh": {
        "Chole Bhature": (
            "Chandigarh's food culture grew with the people who settled in the planned city, including families carrying Punjabi cooking traditions from across the region. Dhabas, markets and neighbourhood eateries made chole bhature a familiar meal for residents and visitors. The dish became part of the city's everyday Punjabi dining scene while retaining its wider North Indian roots."
        ),
        "Amritsari Kulcha": (
            "Amritsari kulcha travelled beyond its home city through Punjabi migration, trade and the growth of tandoor bakeries and restaurants. In Chandigarh, cooks and food businesses carried the stuffed bread into neighbourhood eateries, where it became a popular partner for chole. Its presence reflects the shared food culture linking Chandigarh with Amritsar and the wider Punjab region."
        ),
    },
    "dadra-and-nagar-haveli-and-daman-and-diu": {
        "Hoka Fruit of Diu": (
            "The Hoka palm became part of Diu's landscape through the maritime connections of the Portuguese period, when traders brought the tree from the African region. Over time it adapted to the island environment and its fruit entered local food life, sold by vendors and enjoyed by residents. The palm now forms a distinctive part of Diu's coastal identity."
        ),
        "Daman Jetty Roll": (
            "Daman's port and fishing culture helped shape a street food that adapted the roll format to local tastes. Accounts connect the preparation with a Bengali cook who brought the idea of a kathi-style roll and used fillings suited to Daman, including seafood. Local vendors carried the variation into the town's casual food scene around markets and the jetty."
        ),
    },
    "delhi": {
        "Butter Chicken": (
            "Butter chicken is closely associated with the Punjabi restaurant culture that took root in post-Partition Delhi. At Moti Mahal in Daryaganj, cooks built on the city's tandoor tradition by serving cooked chicken in a rich tomato-and-butter gravy. The dish travelled through restaurant kitchens across India and became one of Delhi's most recognised contributions to popular dining."
        ),
        "Old Delhi Chaat": (
            "Chaat grew with the busy market culture of Old Delhi, where vendors served quick, flavourful food to shoppers, traders and passers-by. Chandni Chowk's food lanes brought together fried snacks, pulses, potatoes, yoghurt and chutneys in countless combinations. Generations of street sellers developed local specialties, making chaat part of the everyday rhythm of the old city."
        ),
    },
    "jammu-and-kashmir": {
        "Rogan Josh": (
            "Rogan josh reflects the layers of influence that shaped Kashmiri cooking, including Persian and Central Asian culinary connections adapted to local ingredients. Kashmiri cooks made the lamb preparation part of the elaborate Wazwan tradition, where dishes are served as a carefully arranged communal feast. Distinct Pandit and Muslim styles continue to give the dish regional depth."
        ),
        "Kashmiri Kahwa": (
            "Kahwa belongs to Kashmir's long history of exchange with the wider Himalayan and Central Asian world, where tea and fragrant spices moved along trade routes. In Kashmiri homes, green tea was combined with ingredients such as saffron, cardamom and almonds, becoming a drink of hospitality for guests, weddings and winter gatherings."
        ),
    },
    "ladakh": {
        "Skyu": (
            "Skyu grew within the food traditions of Ladakhi farming communities, where barley and wheat, root vegetables and stored produce shaped meals through the cold season. One-pot dishes suited household hearths and the demands of life in high-altitude villages. Skyu remains part of home cooking and reflects the region's reliance on local grains and garden crops."
        ),
        "Gur Gur Cha (Butter Tea)": (
            "Salted butter tea is part of the shared Tibetan Himalayan food culture that connects Ladakh with communities across the plateau. Tea, salt and local dairy came together in a drink suited to cold weather, travel and high-altitude life. In Ladakhi homes and monasteries, serving gur gur cha became an expression of hospitality and welcome."
        ),
    },
    "lakshadweep": {
        "Mus Kavaab": (
            "Mus kavaab reflects Minicoy's close maritime and cultural connections with the Maldives. Fishing, especially tuna fishing, has long shaped the island's work and food traditions, while shared seafaring links brought related tastes and cooking ideas across the sea. The preparation became a distinctive part of Minicoy's household cuisine and island hospitality."
        ),
        "Maas Podichathu": (
            "Drying tuna has been an important way for Lakshadweep fishing communities to preserve a valuable catch beyond the day it is landed. Dried fish could be stored and used when fresh supplies were limited, then combined with coconut and household aromatics. Maas podichathu grew from this practical island food tradition and remains a familiar accompaniment in local meals."
        ),
    },
    "puducherry": {
        "Roll Roti": (
            "Roll roti reflects the everyday food exchange of colonial Puducherry, where Tamil bakers supplied bread to French and Creole households and to local workers. Wood-fired bakeries became part of the town's neighbourhood life, blending local baking skills with changing tastes. The bread remains a reminder of how Tamil cooks shaped the food culture of the former French settlement."
        ),
        "Vettu Sambar": (
            "Vettu sambar belongs to the everyday Tamil food traditions of Puducherry, where household cooks made filling meals from familiar pantry ingredients. Its place in family kitchens reflects a style of practical home cooking that continued alongside the bakery and restaurant cultures shaped by the town's colonial history. The preparation survives through household variation and shared local memory."
        ),
    },
}


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit("state_pages.json was not found. Place this script beside the project's current state_pages.json.")
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("state_pages.json must contain an object keyed by region slug.")
    if len(payload) != 36:
        raise SystemExit(f"Safety check failed: expected 36 region records, found {len(payload)}. No output written.")

    expected = {(slug, dish) for slug, dishes in HISTORY_UPDATES.items() for dish in dishes}
    found: set[tuple[str, str]] = set()
    old_histories: dict[tuple[str, str], str] = {}
    for slug, region in payload.items():
        for dish in region.get("dishes", []):
            key = (slug, dish.get("name", ""))
            if key in expected:
                found.add(key)
                old_histories[key] = dish.get("history", "")

    missing = expected - found
    if missing:
        details = "\n".join(f"  - {slug}: {dish}" for slug, dish in sorted(missing))
        raise SystemExit("Safety check failed: one or more expected dish records are missing. No output written.\n" + details)

    total_dishes = sum(len(region.get("dishes", [])) for region in payload.values())
    if total_dishes != 72 or len(expected) != 72:
        raise SystemExit(f"Safety check failed: expected 72 dishes and 72 updates; found {total_dishes} dishes and {len(expected)} updates. No output written.")

    updated = 0
    report = []
    for slug, region in payload.items():
        for dish in region.get("dishes", []):
            name = dish.get("name", "")
            new_history = HISTORY_UPDATES.get(slug, {}).get(name)
            if new_history is not None:
                old = dish.get("history", "")
                dish["history"] = new_history
                updated += 1
                report.append({"region": region.get("name", slug), "dish": name, "old_history": old, "new_history": new_history})

    # Guard against editorial caveats creeping back into the history copy.
    disallowed = ("does not establish", "not documented", "not established", "no single inventor", "exact date", "origin is unknown", "remains uncertain", "not proven", "not conclusively")
    bad = [(item["region"], item["dish"], phrase) for item in report for phrase in disallowed if phrase in item["new_history"].lower()]
    if bad:
        raise SystemExit("Safety check failed: meta-caveat language found in updated history copy: " + repr(bad))

    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "state_history_change_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {updated} historical-background entries across {len(payload)} regions.")
    print(f"Original file preserved: {SOURCE.name}")
    print(f"Updated file created: {OUTPUT.name}")
    print(f"Change report created: state_history_change_report.json")
    print("Only dishes[*].history was changed; all other fields were preserved.")


if __name__ == "__main__":
    main()
