
    // ── Template Data Injected by app.py ───────────────────────────
    const STORY_IMAGES = {"chole-bhature": "../../assets/stories/chole-bhature.jpg", "dal-bati": "../../assets/stories/dal-bati.jpg", "daulat-ki-chat": "../../assets/stories/daulat-ki-chat.jpg", "masala-dosa": "../../assets/stories/masala-dosa.jpg", "rasogulla": "../../assets/stories/rasogulla.jpg", "vada-pav": "../../assets/stories/vada-pav.jpg", "vada-pav-mumbai-commuter-food": "../../assets/stories/vada-pav.jpg", "rasgulla-two-regional-traditions": "../../assets/stories/rasogulla.jpg", "dal-baati-food-for-the-road": "../../assets/stories/dal-bati.jpg", "masala-dosa-udupi-network": "../../assets/stories/masala-dosa.jpg", "chole-bhature-post-partition-delhi": "../../assets/stories/chole-bhature.jpg", "daulat-ki-chaat-delhi-winter": "../../assets/stories/daulat-ki-chat.jpg"};
    const STATE_IMAGES = {"andaman-and-nicobar-islands": "../../assets/states/andaman-and-nicobar-islands.jpg", "andhra-pradesh": "../../assets/states/andhra-pradesh.jpg", "arunachal-pradesh": "../../assets/states/arunachal-pradesh.jpg", "assam": "../../assets/states/assam.jpg", "bihar": "../../assets/states/bihar.jpg", "chandigarh": "../../assets/states/chandigarh.jpg", "chhattisgarh": "../../assets/states/chhattisgarh.jpg", "dadra-and-nagar-haveli-and-daman-and-diu": "../../assets/states/dadra-and-nagar-haveli-and-daman-and-diu.jpg", "delhi": "../../assets/states/delhi.jpg", "goa": "../../assets/states/goa.jpg", "gujarat": "../../assets/states/gujarat.jpg", "haryana": "../../assets/states/haryana.jpg", "himachal-pradesh": "../../assets/states/himachal-pradesh.jpg", "jammu-and-kashmir": "../../assets/states/jammu-and-kashmir.jpg", "jharkhand": "../../assets/states/jharkhand.jpg", "karnataka": "../../assets/states/karnataka.jpg", "kerala": "../../assets/states/kerala.jpg", "ladakh": "../../assets/states/ladakh.jpg", "lakshadweep": "../../assets/states/lakshadweep.jpg", "madhya-pradesh": "../../assets/states/madhya-pradesh.jpg", "maharashtra": "../../assets/states/maharashtra.jpg", "manipur": "../../assets/states/manipur.jpg", "meghalaya": "../../assets/states/meghalaya.jpg", "mizoram": "../../assets/states/mizoram.jpg", "nagaland": "../../assets/states/nagaland.jpg", "odisha": "../../assets/states/odisha.jpg", "puducherry": "../../assets/states/puducherry.jpg", "punjab": "../../assets/states/punjab.jpg", "rajasthan": "../../assets/states/rajasthan.jpg", "sikkim": "../../assets/states/sikkim.jpg", "tamil-nadu": "../../assets/states/tamil-nadu.jpg", "telangana": "../../assets/states/telangana.jpg", "tripura": "../../assets/states/tripura.jpg", "uttar-pradesh": "../../assets/states/uttar-pradesh.jpg", "uttarakhand": "../../assets/states/uttarakhand.jpg", "west-bengal": "../../assets/states/west-bengal.jpg"};
    const REGION_TYPES = {"punjab": "State", "west-bengal": "State", "tamil-nadu": "State", "kerala": "State", "rajasthan": "State", "gujarat": "State", "maharashtra": "State", "karnataka": "State", "uttar-pradesh": "State", "assam": "State", "andhra-pradesh": "State", "arunachal-pradesh": "State", "bihar": "State", "chhattisgarh": "State", "goa": "State", "haryana": "State", "himachal-pradesh": "State", "jharkhand": "State", "madhya-pradesh": "State", "manipur": "State", "meghalaya": "State", "mizoram": "State", "nagaland": "State", "odisha": "State", "sikkim": "State", "telangana": "State", "tripura": "State", "uttarakhand": "State", "andaman-and-nicobar-islands": "Union Territory", "chandigarh": "Union Territory", "dadra-and-nagar-haveli-and-daman-and-diu": "Union Territory", "delhi": "Union Territory", "jammu-and-kashmir": "Union Territory", "ladakh": "Union Territory", "lakshadweep": "Union Territory", "puducherry": "Union Territory"};

    // ── Researched Food Stories Curatorial Dataset ──────────────────
    const stories = [
      {
        slug: "vada-pav-mumbai-commuter-food",
        folio: "FOLIO · 01",
        title: "Vada Pav: The Food of a City That Never Stops",
        description: "How Mumbai's working rhythms shaped one of its most recognisable foods.",
        region: "Mumbai · Maharashtra",
        provenance: "Western India",
        archivalClass: "Urban Commuter Foodways",
        pullQuote: "Food had to be more than delicious. It had to be affordable, filling, and easy to carry.",
        contextualPlates: [
          { stateSlug: "maharashtra", title: "Plate II: Maharashtra Foodways", desc: "The western railway junctions and industrial corridors that shaped the commuter culinary sphere." }
        ],
        paragraphs: [
          "Mumbai's streets move at a relentless pace. Every day, thousands of people pass through railway stations, rush between workplaces and squeeze meals into the few minutes they can spare. In a city like this, food had to be more than delicious. It had to be affordable, filling and easy to carry.",
          "Vada pav answered that need. A spiced potato fritter, tucked inside a bread roll and served with chutneys, brought together familiar Maharashtrian flavours and the convenience of bakery bread. Its rise is often associated with Ashok Vaidya's stall near Dadar railway station in the 1960s, although the precise origins remain disputed.",
          "What followed was bigger than one vendor or one recipe. Vada pav became part of the everyday life of Mumbai — a reminder that some of a city's most recognisable foods emerge not from royal kitchens, but from the demands of ordinary working people."
        ],
        editorialNote: "Ashok Vaidya is widely credited in popular accounts, but the precise year and first vendor are not firmly established. The story describes the conditions behind the snack's rise rather than claiming a single inventor.",
        sources: [
          { title: "Meet Mumbai's Iconic Veggie Burger", publisher: "KPBS Public Media", date: "4 November 2016", url: "https://www.kpbs.org/news/2016/11/04/meet-mumbais-iconic-veggie-burger" },
          { title: "Handcart to TasteAtlas: The story behind Dadar's famous Ashok Vada Pav", publisher: "The Indian Express", date: "27 June 2026", url: "https://indianexpress.com/article/cities/mumbai/ashok-vada-pav-dadar-kirti-college-tasteatlas-ranking-history-10759907/" }
        ]
      },
      {
        slug: "rasgulla-two-regional-traditions",
        folio: "FOLIO · 02",
        title: "Rasgulla: Two Regions, Two Culinary Memories",
        description: "Temple tradition and confectionery innovation behind two regional identities.",
        region: "Odisha · West Bengal",
        provenance: "Eastern India",
        archivalClass: "Confectionery & Ritual Traditions",
        pullQuote: "These are not simply two claims competing for ownership of one dessert. They represent different ways in which a food becomes meaningful.",
        contextualPlates: [
          { stateSlug: "odisha", title: "Plate II-A: Puri & Jagannath Temple Kitchens", desc: "The Niladri Bije ritual tradition where rasagola is offered to Goddess Lakshmi." },
          { stateSlug: "west-bengal", title: "Plate II-B: North Kolkata Sweetshops", desc: "The 19th-century chhana confectionery innovation developed in urban Bengal." }
        ],
        paragraphs: [
          "Ask where the rasgulla comes from, and you may find yourself in the middle of a much older cultural conversation. In Odisha, Rasagola is associated with the Jagannath Temple's Niladri Bije tradition. Its place in the ritual gives the sweet a significance beyond the kitchen: it becomes part of religious practice and regional memory.",
          "Travel to nineteenth-century Kolkata, however, and another chapter emerges. Here, the modern chhana-based rosogolla became associated with confectioner Nabin Chandra Das and the city's growing sweet-shop culture.",
          "These are not simply two claims competing for ownership of one dessert. They represent different ways in which a food becomes meaningful: through temple tradition in one place, and confectionery innovation and urban culture in another. Today, Banglar Rasogolla and Odisha Rasagola have separate Geographical Indication registrations. The archive preserves this story not to declare a winner, but to show how a humble sweet can carry the identity of two regions."
        ],
        editorialNote: "Do not present a 12th-century Puri origin or an exact 1868 invention date as settled fact. GI registration records distinct regional products; it does not decide historical priority.",
        sources: [
          { title: "Registration Details of Geographical Indications in India", publisher: "Geographical Indications Registry, Government of India", date: "Register updated through 15 May 2025", url: "https://www.ipindia.gov.in/writereaddata/Portal/Images/pdf/Total_Registered_GI_details_of_GI_Application_in_India_15_05_2025.pdf" },
          { title: "My City, My Heritage: My Kolkata — section 'Nabin Chandra Das & Sweet Shops of Kolkata'", publisher: "Sahapedia / InterGlobe Foundation", date: "First edition 2022", url: "https://www.sahapedia.org/sites/default/files/pdf/my-city-my-heritage/MCMH_Kolkata.pdf" },
          { title: "Who deserves credit for the rasgulla? Bengalis, Odiyas...or the Portuguese?", publisher: "Scroll.in", date: "4 August 2015", url: "https://scroll.in/article/745871/who-deserves-credit-for-the-rasgulla-bengalis-odiyas-or-the-portuguese" }
        ]
      },
      {
        slug: "dal-baati-food-for-the-road",
        folio: "FOLIO · 03",
        title: "Dal Baati: Food Designed for the Desert",
        description: "How climate, travel and storage shaped a lasting Rajasthani meal.",
        region: "Rajasthan",
        provenance: "North-Western India",
        archivalClass: "Arid Landscapes & Military Mobility",
        pullQuote: "In western Rajasthan, preparing a meal has historically meant working with what the landscape allows.",
        contextualPlates: [
          { stateSlug: "rajasthan", title: "Plate II: The Arid Thar Landscape", desc: "Desert caravans and warrior mobility where water scarcity governed culinary preservation." }
        ],
        paragraphs: [
          "In western Rajasthan, preparing a meal has historically meant working with what the landscape allows. Water can be scarce, journeys can be long, and food that spoils quickly is not always practical.",
          "Baati reflects this relationship between food and environment. Made from wheat dough and traditionally baked or roasted over heat, the hard bread could be carried and kept for days. Its practicality also made it useful during military campaigns, a connection examined in a 2023 article in the Indian Journal of History of Science.",
          "Over time, baati became part of the familiar combination with dal and churma. What is now recognised as one of Rajasthan's signature meals carries a much more practical history: making food that could survive travel and suit the conditions of the region. Its story is not about a single inventor. It is about how geography and necessity can shape an entire food tradition."
        ],
        editorialNote: "The 2023 academic article discusses baati's suitability and use in military settings. It does not establish every popular Bappa Rawal or churma-origin legend.",
        sources: [
          { title: "Food, water and intoxicants in the battlefield practices of Rajasthan", publisher: "Indian Journal of History of Science, 58 (2023), pp. 57–63", date: "Published 6 February 2023", url: "https://doi.org/10.1007/s43539-023-00072-6" }
        ]
      },
      {
        slug: "masala-dosa-udupi-network",
        folio: "FOLIO · 04",
        title: "Masala Dosa: How Udupi Took Its Food Across India",
        description: "The cooks and restaurant networks that carried Udupi food into new cities.",
        region: "Udupi · Karnataka",
        provenance: "Southern India",
        archivalClass: "Commercial Tiffin Networks",
        pullQuote: "Culinary traditions do not spread by recipes alone. They travel through migration, businesses, and the people who carry their skills into new places.",
        contextualPlates: [
          { stateSlug: "karnataka", title: "Plate II-A: Coastal Kanara & Temple Kitchens", desc: "The Brahmin kitchen traditions of Udupi mathas." },
          { stateSlug: "tamil-nadu", title: "Plate II-B: The Madras Restaurant Expansion", desc: "The mid-century vegetarian tiffin diner movement across urban Tamil Nadu." }
        ],
        paragraphs: [
          "A dish can travel much farther than the people who first made it. Masala dosa is a good example. Its roots are closely associated with Udupi's culinary traditions, where the crisp rice-and-lentil dosa is paired with a spiced potato filling. But its wider popularity was shaped by something beyond the recipe: the movement of cooks and restaurant owners.",
          "During the early twentieth century, Udupi cooks and restaurateurs began establishing themselves in cities beyond coastal Karnataka. Madras was among the important destinations. Restaurant ventures associated with figures such as K. Krishna Rao helped introduce Udupi-style food to new urban audiences.",
          "As these restaurants spread, so did the dishes they served. Masala dosa moved from a regional food tradition into the everyday eating habits of people across India. Its history shows that culinary traditions do not spread by recipes alone. They travel through migration, businesses and the people who carry their skills into new places."
        ],
        editorialNote: "K. Krishna Rao is associated with the popularisation of masala dosa in Madras, but a single, conclusively documented inventor or first date has not been established.",
        sources: [
          { title: "Quantity Food Production — B.Sc. Hospitality Studies and Catering Services", publisher: "Yashwantrao Chavan Maharashtra Open University", date: "First published June 2018", url: "https://ycmou.ac.in/media/publication/ycmou_book/RVV_YB_128.pdf" },
          { title: "Madras Day special: How masala dosa became Chennai's signature dish", publisher: "The Federal", date: "23 August 2021", url: "https://thefederal.com/features/madras-day-special-masala-dosa-and-chennai-are-made-for-each-other" }
        ]
      },
      {
        slug: "chole-bhature-post-partition-delhi",
        folio: "FOLIO · 05",
        title: "Chole Bhature: A Food Tradition Carried Across a Border",
        description: "How Partition-era migration helped shape Delhi's everyday food culture.",
        region: "Punjab · Delhi",
        provenance: "Northern India",
        archivalClass: "Post-Partition Urban Migration",
        pullQuote: "Behind that familiar plate lies a story of displacement, rebuilding, and the way food can help people preserve a sense of home in a new place.",
        contextualPlates: [
          { stateSlug: "punjab", title: "Plate II-A: The Grain & Legume Plains of Punjab", desc: "The robust bread and spiced chickpea traditions of undivided Punjab." },
          { stateSlug: "delhi", title: "Plate II-B: Post-Partition Resettlement Quarters", desc: "Refugee-established dhabas across Karol Bagh, Kingsway Camp, and Lajpat Nagar." }
        ],
        paragraphs: [
          "In 1947, Partition forced millions of people to leave their homes and rebuild their lives elsewhere. Among the things they carried with them were habits that could not simply be left behind — the language they spoke, the customs they followed and the food they knew.",
          "Punjabi migrants became an important part of Delhi's changing food culture. Refugee-run dhabas and small eateries introduced familiar Punjabi preparations into neighbourhoods that were themselves being reshaped by migration.",
          "Chole bhature became part of this changing landscape. The combination of spiced chickpeas and deep-fried bread was not invented by Partition, but its popularity in Delhi grew within the wider movement of Punjabi people, food businesses and culinary traditions into the capital. Today, it is an everyday favourite across the city. Yet behind that familiar plate lies a story of displacement, rebuilding and the way food can help people preserve a sense of home in a new place."
        ],
        editorialNote: "The evidence supports Partition-era Punjabi influence on Delhi's food culture; it does not establish that chole bhature itself originated in Delhi or after 1947.",
        sources: [
          { title: "How Punjabi refugees transformed Delhi's food culture after the Partition", publisher: "The Patriot", date: "15 August 2025", url: "https://thepatriot.in/cover-story/how-punjabi-refugees-transformed-delhis-food-culture-after-the-partition-74377" },
          { title: "Foods of India — Talk About Delhi", publisher: "Delhi Tourism, Government of NCT of Delhi", date: "Undated cultural feature", url: "https://delhitourism.gov.in/talk_delhi/foods.html" }
        ]
      },
      {
        slug: "daulat-ki-chaat-delhi-winter",
        folio: "FOLIO · 06",
        title: "Daulat Ki Chaat: A Sweet That Belongs to Winter",
        description: "A seasonal Old Delhi delicacy shaped by cold weather and delicate technique.",
        region: "Old Delhi",
        provenance: "Northern India",
        archivalClass: "Seasonal Ephemeral Delicacies",
        pullQuote: "Food culture is not always built around permanent availability. Sometimes, a dish becomes special precisely because it belongs to a particular season.",
        contextualPlates: [
          { stateSlug: "delhi", title: "Plate II: Dawn in Shahjahanabad", desc: "The winter morning streetscapes of Dariba Kalan and Chandni Chowk where the foam is sold." }
        ],
        paragraphs: [
          "In Old Delhi, some foods are not available throughout the year. Daulat ki chaat belongs to the colder months, when vendors prepare its delicate milk-and-cream foam and sell it in the early hours of the day.",
          "Unlike sweets that depend on heavy syrups or elaborate decoration, its appeal lies in its texture. The airy mixture is carefully prepared and handled before it loses its structure, then finished with ingredients such as saffron, nuts and silver leaf.",
          "Stories about overnight dew and moonlight have become part of its identity. While these explanations are better understood as popular tradition than established cooking requirements, they reflect the close association between the dessert and Delhi's winter mornings. Related preparations are found elsewhere in North India under names such as malaiyo and nimish. Its exact origins remain uncertain, but its seasonal character is unmistakable. Daulat ki chaat reminds us that food culture is not always built around permanent availability. Sometimes, a dish becomes special precisely because it belongs to a particular season."
        ],
        editorialNote: "Dew is a popular explanation, not an established technical requirement. Avoid claims of a 500-year or Mughal-court origin.",
        sources: [
          { title: "The beloved 'snack of wealth' made on Delhi's streets", publisher: "BBC Travel", date: "18 July 2022", url: "https://www.bbc.com/travel/article/20220717-the-beloved-snack-of-wealth-made-on-delhis-streets" },
          { title: "Long before Daulat ki Chaat became an Instagram favourite, it was an unembellished country dish", publisher: "Scroll.in", date: "17 February 2022", url: "https://scroll.in/magazine/1017455/long-before-daulat-ki-chaat-became-an-instagram-favourite-it-was-an-unembellished-country-dish" }
        ]
      }
    ];

    // ── Regional Catalogue Data ────────────────────────────────────
    const featuredStates = [
      "Rajasthan", "Kerala", "Punjab", "Assam", "West Bengal",
      "Tamil Nadu", "Gujarat", "Maharashtra"
    ];
    const allStates = [
      "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana",
      "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
      "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
      "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands",
      "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Jammu and Kashmir", "Ladakh",
      "Lakshadweep", "Puducherry"
    ];

    function escapeHtml(value) {
      return String(value == null ? "" : value).replace(/[&<>"']/g, ch => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[ch]);
    }

    // ── Render Food Story Folio Cards ──────────────────────────────
    function storyCard(story, index) {
      const image = STORY_IMAGES[story.slug] || "";
      return `<button class="story-archive-card" type="button" data-story-index="${index}" aria-label="Open curated monograph: ${escapeHtml(story.title)}">
        <div class="folio-ribbon">
          <span class="folio-num">${escapeHtml(story.folio)}</span>
          <span class="folio-region">${escapeHtml(story.region)}</span>
        </div>
        <div class="story-visual" aria-hidden="true">
          ${image ? `<img class="story-card-photo" src="${image}" alt="${escapeHtml(story.title)}" loading="lazy" decoding="async">` : ""}
        </div>
        <div class="story-copy">
          <h3>${escapeHtml(story.title)}</h3>
          <p>${escapeHtml(story.description)}</p>
          <div class="story-footer-action">
            <span>Read Curated Monograph</span>
            <span aria-hidden="true">→</span>
          </div>
        </div>
      </button>`;
    }

    const storyGrid = document.getElementById("story-grid");
    // The collection is set as two rows of three monographs, so no row reads as
    // one long undifferentiated strip of identical cards.
    const STORY_ROW_SIZE = 3;
    let storyRowsMarkup = "";
    for (let i = 0; i < stories.length; i += STORY_ROW_SIZE) {
      const row = stories.slice(i, i + STORY_ROW_SIZE)
        .map((s, j) => storyCard(s, i + j))
        .join("");
      storyRowsMarkup += `<div class="story-row">${row}</div>`;
    }
    storyGrid.innerHTML = storyRowsMarkup;

    // ── Story Reader Implementation (Task 2) ───────────────────────
    let currentStoryIndex = 0;
    const storyPage        = document.getElementById("story-page-root");
    const progressBar      = document.getElementById("story-progress-bar");
    const storyPageRegion  = document.getElementById("story-page-region");
    const storyFolioPill   = document.getElementById("story-folio-pill");
    const storyFolioStamp  = document.getElementById("story-folio-stamp");
    const storyPageTitle   = document.getElementById("story-page-title");
    const storyPageSubtitle = document.getElementById("story-page-subtitle");
    const storyImageWrap   = document.getElementById("story-page-image-wrap");
    const storyImage       = document.getElementById("story-page-image");
    const storyPullquote   = document.getElementById("story-pullquote-text");
    const storyPullcite    = document.getElementById("story-pullquote-cite");
    const storyPart1       = document.getElementById("story-part-1");
    const storyPart2       = document.getElementById("story-part-2");
    const storyPart3       = document.getElementById("story-part-3");
    const storyContextGrid = document.getElementById("story-context-grid");
    const storyContextCaption = document.getElementById("story-context-caption-text");
    const storyNoteBody    = document.getElementById("story-page-note-body");
    const storySourcesList = document.getElementById("story-page-source-list");
    const storyStripProvenance = document.getElementById("story-strip-provenance");
    const storyStripClass      = document.getElementById("story-strip-class");
    const archiveMain      = document.querySelector("main");
    const archiveFooter    = document.querySelector(".site-footer");

    function updateReadingProgress() {
      if (storyPage.hidden) return;
      const scrollY = window.scrollY || document.documentElement.scrollTop;
      const totalH = document.documentElement.scrollHeight - window.innerHeight;
      const percent = totalH > 0 ? Math.min(100, Math.max(0, (scrollY / totalH) * 100)) : 0;
      progressBar.style.width = percent + "%";
    }
    window.addEventListener("scroll", updateReadingProgress, { passive: true });

    function openFoodStory(index) {
      const story = stories[index];
      if (!story) return;
      currentStoryIndex = index;

      // Meta Ribbon
      storyFolioPill.textContent = story.folio;
      storyFolioStamp.textContent = story.folio;
      storyPageRegion.textContent = story.region;
      storyPageTitle.textContent = story.title;
      storyPageSubtitle.textContent = story.description;
      if (storyStripProvenance) storyStripProvenance.textContent = story.provenance || "Pan-Indian Heritage";
      if (storyStripClass) storyStripClass.textContent = story.archivalClass || "Regional Foodways";

      // Primary Hero Plate
      const mainImg = STORY_IMAGES[story.slug] || "";
      if (mainImg) {
        storyImage.src = mainImg;
        storyImage.alt = story.title + " — archival food photograph";
        storyImageWrap.hidden = false;
      } else {
        storyImage.removeAttribute("src");
        storyImageWrap.hidden = true;
      }

      // Prose distribution
      const p = story.paragraphs || [];
      storyPart1.innerHTML = p[0] ? `<p>${escapeHtml(p[0])}</p>` : "";
      storyPart2.innerHTML = p[1] ? `<p>${escapeHtml(p[1])}</p>` : "";
      storyPart3.innerHTML = p[2] ? `<p>${escapeHtml(p[2])}</p>` : "";

      // Pull Quote
      storyPullquote.textContent = story.pullQuote || (p[0] || "");
      storyPullcite.textContent = story.region + " Archive Monograph";

      // Secondary Contextual Archival Plates (Task 2)
      if (story.contextualPlates && story.contextualPlates.length > 0) {
        storyContextGrid.className = "story-context-plate-grid" + (story.contextualPlates.length > 1 ? " dual-plate" : "");
        storyContextGrid.innerHTML = story.contextualPlates.map(plate => {
          const stateImg = STATE_IMAGES[plate.stateSlug] || "";
          return `<div class="context-plate-cell">
            ${stateImg ? `<img src="${stateImg}" alt="${escapeHtml(plate.title)}" loading="lazy">` : ""}
          </div>`;
        }).join("");
        storyContextCaption.innerHTML = story.contextualPlates.map(pl => `<div class="context-plate-desc-line"><strong>${escapeHtml(pl.title)}:</strong> ${escapeHtml(pl.desc)}</div>`).join("");
        document.getElementById("story-context-plate-wrap").hidden = false;
      } else {
        document.getElementById("story-context-plate-wrap").hidden = true;
      }

      // Curatorial Memorandum Note
      storyNoteBody.textContent = story.editorialNote || "";

      // Source Bibliography
      storySourcesList.innerHTML = (story.sources || []).map(s => `<li>
        <a href="${escapeHtml(s.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(s.title)}</a>
        <span class="story-source-meta">${escapeHtml(s.publisher || "")}${s.date ? " · " + escapeHtml(s.date) : ""}</span>
      </li>`).join("");

      // Update Prev / Next Buttons
      document.getElementById("story-reader-prev").style.visibility = index > 0 ? "visible" : "hidden";
      document.getElementById("story-reader-next").style.visibility = index < stories.length - 1 ? "visible" : "hidden";

      // Switch view
      archiveMain.hidden = true;
      if (archiveFooter) archiveFooter.hidden = true;
      storyPage.hidden = false;
      document.body.classList.add("story-page-open");
      window.scrollTo({ top: 0, behavior: "auto" });
      updateReadingProgress();
      try {
        history.pushState({ foodStory: story.slug }, "", "#story/" + encodeURIComponent(story.slug));
      } catch (e) {
        // srcdoc iframe safe fallback
      }
    }

    function closeFoodStory(updateHistory = true) {
      if (storyPage.hidden) return;
      storyPage.hidden = true;
      archiveMain.hidden = false;
      if (archiveFooter) archiveFooter.hidden = false;
      document.body.classList.remove("story-page-open");
      progressBar.style.width = "0%";
      try {
        if (updateHistory && location.hash.startsWith("#story/")) {
          history.pushState({}, "", location.pathname + location.search);
        }
      } catch (e) {}
      const stSec = document.getElementById("stories");
      if (stSec) window.scrollTo({ top: stSec.offsetTop, behavior: "auto" });
    }

    storyGrid.addEventListener("click", e => {
      const card = e.target.closest("[data-story-index]");
      if (card) openFoodStory(Number(card.dataset.storyIndex));
    });

    document.getElementById("story-back").addEventListener("click", () => closeFoodStory());
    document.getElementById("story-reader-back-link").addEventListener("click", () => closeFoodStory());

    document.getElementById("story-reader-prev").addEventListener("click", () => {
      if (currentStoryIndex > 0) openFoodStory(currentStoryIndex - 1);
    });
    document.getElementById("story-reader-next").addEventListener("click", () => {
      if (currentStoryIndex < stories.length - 1) openFoodStory(currentStoryIndex + 1);
    });

    window.addEventListener("popstate", () => {
      if (storyPage && !location.hash.startsWith("#story/")) closeFoodStory(false);
    });

    document.addEventListener("keydown", e => {
      if (e.key === "Escape" && !storyPage.hidden) closeFoodStory();
    });

    // ── Render Regional Atlas (Explore by Region) ──────────────────
    const stateGrid   = document.getElementById("state-grid");
    const searchInput = document.getElementById("state-search");
    const seeMoreBtn  = document.getElementById("see-more");
    const emptyMsg    = document.getElementById("states-empty");
    const countStatus = document.getElementById("state-count-status");
    let expanded = false;

    function renderStates(query = "") {
      const q = query.trim().toLocaleLowerCase();
      const matches = allStates.filter(name => name.toLocaleLowerCase().includes(q));
      const visible  = q ? matches : (expanded ? allStates : featuredStates);

      stateGrid.innerHTML = visible.map((name) => {
        const slug = name.toLowerCase().replace(/&/g, "and").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
        const image = STATE_IMAGES[slug];
        const regionType = REGION_TYPES[slug] || "State";
        const visualStyle = image
          ? `background-image: linear-gradient(180deg, rgba(21,6,5,0.05), rgba(18,5,4,0.72)), url('${image}')`
          : "";
        return `<article class="state-card" data-slug="${slug}" aria-label="${escapeHtml(name)} ${escapeHtml(regionType)} archive">
          <div class="state-visual" style="${visualStyle}" aria-hidden="true">
            ${image ? "" : `<span class="state-placeholder-mark" aria-hidden="true">✧</span>`}
          </div>
          <div class="state-copy">
            <span class="state-badge">${escapeHtml(regionType)}</span>
            <strong>${escapeHtml(name)}</strong>
          </div>
        </article>`;
      }).join("");

      emptyMsg.classList.toggle("visible", q.length > 0 && matches.length === 0);
      seeMoreBtn.style.display = q ? "none" : (allStates.length > featuredStates.length ? "inline-flex" : "none");
      seeMoreBtn.textContent = expanded ? "Show Fewer Regions ↑" : "See All 36 Regions →";

      if (q) {
        countStatus.textContent = matches.length === 1 ? "1 matching regional archive found" : `${matches.length} matching regional archives found`;
      } else {
        countStatus.textContent = expanded ? "Displaying all 36 regional archives" : `Displaying 8 featured regional archives (${allStates.length} total)`;
      }
    }

    searchInput.addEventListener("input", () => renderStates(searchInput.value));
    seeMoreBtn.addEventListener("click", () => {
      expanded = !expanded;
      renderStates(searchInput.value);
    });
    renderStates();

    // ── Hero Entrance — dealt once on load (Emil: one purposeful moment) ──
    requestAnimationFrame(() => document.documentElement.classList.add("m-enter"));

    // ── Direct URL Hash Deep-linking for Story Monograph ───────────
    function checkInitialHash() {
      let hash = window.location.hash;
      try {
        if ((!hash || hash === "#top" || hash === "#stories") && window.parent && window.parent !== window && window.parent.location && window.parent.location.hash) {
          hash = window.parent.location.hash;
        }
      } catch (e) {}

      if (hash && hash.startsWith("#story/")) {
        const slug = decodeURIComponent(hash.replace("#story/", ""));
        const idx = stories.findIndex(s => s.slug === slug);
        if (idx >= 0) openFoodStory(idx);
      }
    }
    checkInitialHash();
    window.addEventListener("DOMContentLoaded", checkInitialHash);
    window.addEventListener("load", checkInitialHash);
    setTimeout(checkInitialHash, 250);
    setTimeout(checkInitialHash, 600);

    // ── Smooth Scroll Navigation ───────────────────────────────────
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    document.querySelectorAll('.main-nav a[href^="#"], .hero-actions a[href^="#"]').forEach(link => {
      link.addEventListener("click", e => {
        const target = document.querySelector(link.getAttribute("href"));
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: prefersReducedMotion ? "auto" : "smooth", block: "start" });
      });
    });

    // ── Mobile Navigation Drawer ───────────────────────────────────
    const navToggle = document.getElementById("nav-toggle");
    const mainNav   = document.getElementById("main-nav");
    if (navToggle && mainNav) {
      navToggle.addEventListener("click", () => {
        const open = mainNav.classList.toggle("open");
        navToggle.setAttribute("aria-expanded", open ? "true" : "false");
      });
      document.addEventListener("click", e => {
        if (!navToggle.contains(e.target) && !mainNav.contains(e.target)) {
          mainNav.classList.remove("open");
          navToggle.setAttribute("aria-expanded", "false");
        }
      });
    }
  