"""
Multi-County Payment Standards for Illinois Housing Authorities
Supports Cook, DuPage, Will (Joliet), and Lake Counties
"""

# =============================================================================
# COUNTY REGISTRY
# =============================================================================

COUNTIES = {
    "cook": {
        "name": "Cook County",
        "authority": "Housing Authority of Cook County (HACC)",
        "effective_date": "January 1, 2026",
        "url_slug": "Cook-County",
        "type": "range",  # Uses A-Z range letter system
        "payment_standards_url": "https://thehacc.org/app/uploads/2025/11/Payment-Standard-Eff-1-2026.pdf",
        "explainer": """
## How Cook County Payment Standards Work

The Housing Authority of Cook County (HACC) uses a **tiered payment standard system**
based on geographic zones. Each ZIP code is assigned a **Range Letter (A-Z)**, and each
range has specific payment amounts by bedroom size.

**Key Points:**
- **26 payment tiers** from Range A (lowest) to Range Z (highest)
- Payment standards vary significantly by neighborhood
- Higher-cost areas like Barrington (Range Z) have standards nearly double lower-cost areas
- The "lesser of" rule applies: if you rent a unit larger than your voucher size,
  payment is capped at your voucher's bedroom standard

**Example:** A 1-bedroom voucher holder in ZIP 60610 (Range Z) has a payment standard
of $2,245/month, while the same voucher in ZIP 60406 (Range A) is $1,145/month.
""",
    },
    "dupage": {
        "name": "DuPage County",
        "authority": "DuPage Housing Authority (DHA)",
        "effective_date": "January 1, 2025",
        "url_slug": "DuPage-County",
        "type": "direct",  # Direct ZIP to amounts
        "payment_standards_url": "https://www.dupagehousing.org/dupage-payment-standards",
        "explainer": """
## How DuPage County Payment Standards Work

The DuPage Housing Authority (DHA) sets payment standards **directly by ZIP code**.
Each ZIP code has specific maximum amounts for each bedroom size.

**Key Points:**
- Payment standards are set at the ZIP code level
- Standards are based on HUD Small Area Fair Market Rents (SAFMRs)
- DHA also covers Kendall County under a separate program
- Utility allowances are subtracted from the payment standard

**Example:** In Naperville (60540), the 2-bedroom payment standard is $2,250/month,
while in Addison (60101) it's $1,580/month.
""",
    },
    "will": {
        "name": "Will County",
        "authority": "Housing Authority of Joliet (HAJ)",
        "effective_date": "October 1, 2025",
        "url_slug": "Will-County",
        "type": "direct",
        "payment_standards_url": "https://www.hajoliet.org/sites/default/files/file-attachements/2026_haj_payment_standards.10-2025.pdf",
        "explainer": """
## How Will County Payment Standards Work

The Housing Authority of Joliet (HAJ) administers vouchers for all of Will County.
Payment standards are set **by ZIP code** based on local market rents.

**Key Points:**
- Covers all of Will County including Joliet, Bolingbrook, Romeoville, Plainfield
- Standards updated annually based on HUD Fair Market Rents
- Some ZIP codes cross into other counties - verify property location

**Example:** In Bolingbrook (60440), the 2-bedroom standard is $2,266/month,
while in Joliet (60435) it's $1,793/month.
""",
    },
    "lake": {
        "name": "Lake County",
        "authority": "Lake County Housing Authority (LCHA)",
        "effective_date": "January 1, 2026",
        "url_slug": "Lake-County",
        "type": "direct",
        "payment_standards_url": "https://www.lakecountyha.org/plugins/show_image.php?id=1662",
        "explainer": """
## How Lake County Payment Standards Work

The Lake County Housing Authority covers most of Lake County. Note that **Waukegan
and North Chicago** have separate housing authorities with their own standards.

**Key Points:**
- Based on HUD Small Area Fair Market Rents (SAFMRs)
- Wide variation between areas (Highland Park vs North Chicago)
- Some ZIP codes cross county lines - verify property is in Lake County
- Waukegan Housing Authority handles Waukegan separately

**Example:** In Highland Park (60035), the 2-bedroom standard is $2,490/month,
while in North Chicago (60064) it's $1,440/month.
""",
    },
}


# =============================================================================
# COOK COUNTY DATA (Range-based system)
# =============================================================================

COOK_RANGE_AMOUNTS = {
    "A": {"studio": 1040, "1br": 1145, "2br": 1310, "3br": 1660, "4br": 1960},
    "B": {"studio": 1095, "1br": 1200, "2br": 1360, "3br": 1730, "4br": 2050},
    "C": {"studio": 1130, "1br": 1220, "2br": 1400, "3br": 1760, "4br": 2090},
    "D": {"studio": 1150, "1br": 1240, "2br": 1420, "3br": 1795, "4br": 2135},
    "E": {"studio": 1180, "1br": 1270, "2br": 1460, "3br": 1830, "4br": 2200},
    "F": {"studio": 1210, "1br": 1300, "2br": 1495, "3br": 1895, "4br": 2255},
    "G": {"studio": 1250, "1br": 1350, "2br": 1530, "3br": 1960, "4br": 2340},
    "H": {"studio": 1275, "1br": 1380, "2br": 1575, "3br": 2000, "4br": 2375},
    "I": {"studio": 1300, "1br": 1400, "2br": 1600, "3br": 2050, "4br": 2440},
    "J": {"studio": 1325, "1br": 1435, "2br": 1640, "3br": 2095, "4br": 2475},
    "K": {"studio": 1350, "1br": 1460, "2br": 1670, "3br": 2120, "4br": 2505},
    "L": {"studio": 1370, "1br": 1480, "2br": 1690, "3br": 2140, "4br": 2530},
    "M": {"studio": 1405, "1br": 1500, "2br": 1725, "3br": 2195, "4br": 2590},
    "N": {"studio": 1450, "1br": 1555, "2br": 1780, "3br": 2270, "4br": 2685},
    "O": {"studio": 1485, "1br": 1590, "2br": 1820, "3br": 2305, "4br": 2740},
    "P": {"studio": 1525, "1br": 1640, "2br": 1870, "3br": 2375, "4br": 2830},
    "Q": {"studio": 1585, "1br": 1680, "2br": 1930, "3br": 2430, "4br": 2930},
    "R": {"studio": 1620, "1br": 1720, "2br": 1975, "3br": 2505, "4br": 3025},
    "S": {"studio": 1670, "1br": 1775, "2br": 2040, "3br": 2600, "4br": 3090},
    "T": {"studio": 1715, "1br": 1840, "2br": 2090, "3br": 2660, "4br": 3185},
    "U": {"studio": 1760, "1br": 1880, "2br": 2140, "3br": 2735, "4br": 3250},
    "V": {"studio": 1800, "1br": 1935, "2br": 2195, "3br": 2800, "4br": 3330},
    "W": {"studio": 1870, "1br": 2000, "2br": 2280, "3br": 2900, "4br": 3400},
    "X": {"studio": 1950, "1br": 2100, "2br": 2350, "3br": 2990, "4br": 3540},
    "Y": {"studio": 2000, "1br": 2180, "2br": 2440, "3br": 3170, "4br": 3650},
    "Z": {"studio": 2035, "1br": 2245, "2br": 2570, "3br": 3200, "4br": 3800},
}

COOK_ZIP_TO_RANGE = {
    "60803": "C", "60501": "A", "60004": "T", "60005": "O", "60006": "L",
    "60010": "Z", "60011": "M", "60103": "W", "60133": "P", "60455": "B",
    "60458": "H", "60459": "I", "60499": "L", "60638": "F", "60104": "F",
    "60163": "C", "60402": "H", "60406": "A", "60153": "E", "60155": "D",
    "60513": "F", "60089": "X", "60633": "D", "60527": "U", "60409": "D",
    "60643": "H", "60827": "C", "60411": "C", "60412": "L", "60415": "D",
    "60478": "T", "60525": "J", "60418": "I", "60445": "E", "60141": "A",
    "60067": "S", "60169": "Q", "60192": "Z", "60195": "S", "60456": "K",
    "60422": "Z", "60430": "K", "60453": "H", "60454": "L", "60457": "C",
    "60461": "Z", "60477": "M", "60487": "K", "60438": "F", "60439": "J",
    "60462": "N", "60467": "V", "60074": "N", "60078": "L", "60463": "U",
    "60428": "R", "60465": "G", "60464": "Y", "60068": "Q", "60426": "C",
    "60161": "L", "60164": "B", "60471": "I", "60165": "F", "60655": "I",
    "60546": "H", "60472": "G", "60056": "O", "60714": "I", "60656": "M",
    "60706": "G", "60062": "W", "60065": "L", "60093": "Y", "60452": "G",
    "60107": "X", "60476": "F", "60466": "N", "60484": "N", "60154": "T",
    "60558": "Z", "60469": "I", "60070": "J", "60480": "M", "60305": "N",
    "60171": "G", "60482": "E", "60015": "Z", "60016": "N", "60017": "L",
    "60018": "E", "60007": "P", "60009": "L", "60707": "I", "60201": "X",
    "60202": "T", "60203": "Y", "60204": "L", "60805": "J", "60130": "I",
    "60712": "Z", "60131": "B", "60022": "Y", "60025": "R", "60026": "X",
    "60425": "U", "60029": "U", "60429": "P", "60162": "N", "60008": "Q",
    "60043": "Z", "60053": "Z", "60076": "P", "60077": "N", "60090": "P",
    "60091": "Z", "60120": "G", "60126": "V", "60159": "L", "60160": "F",
    "60168": "L", "60172": "S", "60173": "W", "60176": "G", "60193": "U",
    "60194": "V", "60301": "N", "60302": "N", "60304": "N", "60419": "Q",
    "60423": "O", "60443": "Q", "60473": "V", "60475": "A", "60521": "Z",
    "60526": "K", "60534": "D",
    # Chicago ZIP codes
    "60601": "J", "60602": "J", "60603": "J", "60604": "J", "60605": "J",
    "60606": "J", "60607": "J", "60608": "H", "60609": "F", "60610": "Z",
    "60611": "Z", "60612": "L", "60613": "H", "60614": "Z", "60615": "D",
    "60616": "G", "60617": "B", "60618": "L", "60619": "C", "60620": "D",
    "60621": "B", "60622": "N", "60623": "F", "60624": "D", "60625": "L",
    "60626": "K", "60628": "C", "60629": "F", "60630": "K", "60631": "M",
    "60632": "F", "60634": "L", "60636": "D", "60637": "E", "60639": "H",
    "60640": "M", "60641": "L", "60642": "N", "60644": "E", "60645": "M",
    "60646": "L", "60647": "M", "60649": "C", "60651": "F", "60652": "G",
    "60653": "D", "60654": "N", "60657": "Q", "60659": "K", "60660": "L",
    "60661": "L",
}

COOK_TOWN_TO_ZIPS = {
    "Alsip": ["60803"],
    "Arlington Heights": ["60004", "60005", "60006"],
    "Barrington": ["60010", "60011"],
    "Barrington Hills": ["60010"],
    "Bartlett": ["60103"],
    "Bedford Park": ["60455", "60458", "60459"],
    "Bellwood": ["60104"],
    "Berkeley": ["60163"],
    "Berwyn": ["60402"],
    "Blue Island": ["60406"],
    "Bridgeview": ["60455"],
    "Broadview": ["60153", "60155"],
    "Brookfield": ["60513"],
    "Buffalo Grove": ["60089"],
    "Burbank": ["60459"],
    "Burnham": ["60633"],
    "Burr Ridge": ["60527"],
    "Calumet City": ["60409"],
    "Calumet Park": ["60643", "60827"],
    "Chicago": ["60601", "60602", "60603", "60604", "60605", "60606", "60607",
                "60608", "60609", "60610", "60611", "60612", "60613", "60614",
                "60615", "60616", "60617", "60618", "60619", "60620", "60621",
                "60622", "60623", "60624", "60625", "60626", "60628", "60629",
                "60630", "60631", "60632", "60633", "60634", "60636", "60637",
                "60638", "60639", "60640", "60641", "60642", "60643", "60644",
                "60645", "60646", "60647", "60649", "60651", "60652", "60653",
                "60654", "60655", "60656", "60657", "60659", "60660", "60661"],
    "Chicago Heights": ["60411", "60412"],
    "Chicago Ridge": ["60415"],
    "Country Club Hills": ["60478"],
    "Countryside": ["60525"],
    "Crestwood": ["60418", "60445"],
    "Deer Park": ["60010"],
    "Deerfield": ["60015"],
    "Des Plaines": ["60016", "60017", "60018"],
    "Dixmoor": ["60406", "60426"],
    "Dolton": ["60419", "60429"],
    "East Hazel Crest": ["60429"],
    "Elk Grove Village": ["60007"],
    "Elmwood Park": ["60707"],
    "Evanston": ["60201", "60202", "60203", "60204"],
    "Evergreen Park": ["60805"],
    "Flossmoor": ["60422"],
    "Forest Park": ["60130"],
    "Forest View": ["60155"],
    "Franklin Park": ["60131"],
    "Glencoe": ["60022"],
    "Glenview": ["60025", "60026"],
    "Glenwood": ["60425"],
    "Golf": ["60029"],
    "Hanover Park": ["60133"],
    "Harvey": ["60426"],
    "Harwood Heights": ["60706"],
    "Hazel Crest": ["60429"],
    "Hickory Hills": ["60457"],
    "Hillside": ["60162"],
    "Hines": ["60141"],
    "Hodgkins": ["60525"],
    "Hoffman Estates": ["60169", "60192", "60195"],
    "Hometown": ["60456"],
    "Homewood": ["60430"],
    "Indian Head Park": ["60525"],
    "Inverness": ["60010", "60067"],
    "Justice": ["60458"],
    "Kenilworth": ["60043"],
    "La Grange": ["60525"],
    "La Grange Highlands": ["60525"],
    "La Grange Park": ["60526"],
    "Lansing": ["60438"],
    "Lemont": ["60439"],
    "Lincolnwood": ["60712"],
    "Lynwood": ["60411"],
    "Lyons": ["60534"],
    "Markham": ["60428"],
    "Matteson": ["60443"],
    "Maywood": ["60153"],
    "McCook": ["60525"],
    "Melrose Park": ["60160", "60164", "60165"],
    "Merrionette Park": ["60655"],
    "Midlothian": ["60445"],
    "Morton Grove": ["60053"],
    "Mount Prospect": ["60056"],
    "Niles": ["60714"],
    "Norridge": ["60706"],
    "North Riverside": ["60546"],
    "Northbrook": ["60062", "60065"],
    "Northfield": ["60093"],
    "Northlake": ["60164"],
    "Oak Forest": ["60452"],
    "Oak Lawn": ["60453", "60454", "60455", "60456", "60457", "60458", "60459"],
    "Oak Park": ["60301", "60302", "60304", "60305"],
    "Olympia Fields": ["60461"],
    "Orland Hills": ["60477", "60487"],
    "Orland Park": ["60462", "60467"],
    "Palatine": ["60067", "60074", "60078"],
    "Palos Heights": ["60463"],
    "Palos Hills": ["60465"],
    "Palos Park": ["60464"],
    "Park Forest": ["60466"],
    "Park Ridge": ["60068"],
    "Phoenix": ["60426"],
    "Posen": ["60469"],
    "Prospect Heights": ["60070"],
    "Richton Park": ["60471"],
    "River Forest": ["60305"],
    "River Grove": ["60171"],
    "Riverdale": ["60827"],
    "Riverside": ["60546"],
    "Robbins": ["60472"],
    "Rolling Meadows": ["60008"],
    "Rosemont": ["60018"],
    "Sauk Village": ["60411"],
    "Schaumburg": ["60159", "60168", "60173", "60193", "60194", "60195"],
    "Schiller Park": ["60176"],
    "Skokie": ["60076", "60077"],
    "South Barrington": ["60010"],
    "South Chicago Heights": ["60411"],
    "South Holland": ["60473"],
    "Steger": ["60475"],
    "Stickney": ["60402"],
    "Stone Park": ["60165"],
    "Streamwood": ["60107"],
    "Summit": ["60501"],
    "Thornton": ["60476"],
    "Tinley Park": ["60477", "60478", "60487"],
    "University Park": ["60466", "60484"],
    "Westchester": ["60154"],
    "Western Springs": ["60558"],
    "Wheeling": ["60090"],
    "Willow Springs": ["60480"],
    "Wilmette": ["60091"],
    "Winnetka": ["60093"],
    "Worth": ["60482"],
}


# =============================================================================
# DUPAGE COUNTY DATA (Direct ZIP to amounts)
# =============================================================================

DUPAGE_ZIP_AMOUNTS = {
    # Format: "ZIP": {"studio": X, "1br": X, "2br": X, "3br": X, "4br": X}
    "60101": {"studio": 1310, "1br": 1400, "2br": 1580, "3br": 2030, "4br": 2380},  # Addison
    "60103": {"studio": 1560, "1br": 1670, "2br": 1880, "3br": 2410, "4br": 2840},  # Bartlett
    "60106": {"studio": 1410, "1br": 1510, "2br": 1700, "3br": 2190, "4br": 2570},  # Bensenville
    "60108": {"studio": 1560, "1br": 1670, "2br": 1880, "3br": 2410, "4br": 2840},  # Bloomingdale
    "60116": {"studio": 1760, "1br": 1890, "2br": 2130, "3br": 2740, "4br": 3210},  # Carol Stream
    "60117": {"studio": 1560, "1br": 1670, "2br": 1880, "3br": 2410, "4br": 2840},  # Bloomingdale
    "60126": {"studio": 1910, "1br": 2050, "2br": 2310, "3br": 2970, "4br": 3490},  # Elmhurst
    "60137": {"studio": 1340, "1br": 1430, "2br": 1620, "3br": 2080, "4br": 2440},  # Glen Ellyn
    "60138": {"studio": 1340, "1br": 1430, "2br": 1620, "3br": 2080, "4br": 2440},  # Glen Ellyn
    "60139": {"studio": 1560, "1br": 1670, "2br": 1880, "3br": 2410, "4br": 2840},  # Glendale Heights
    "60143": {"studio": 1610, "1br": 1720, "2br": 1940, "3br": 2490, "4br": 2930},  # Itasca
    "60148": {"studio": 1780, "1br": 1900, "2br": 2150, "3br": 2760, "4br": 3240},  # Lombard
    "60157": {"studio": 1780, "1br": 1900, "2br": 2150, "3br": 2760, "4br": 3240},  # Lombard (Medinah)
    "60181": {"studio": 1910, "1br": 2050, "2br": 2310, "3br": 2970, "4br": 3490},  # Villa Park
    "60185": {"studio": 1660, "1br": 1780, "2br": 2010, "3br": 2580, "4br": 3030},  # West Chicago
    "60187": {"studio": 1760, "1br": 1890, "2br": 2130, "3br": 2740, "4br": 3210},  # Wheaton
    "60188": {"studio": 1560, "1br": 1670, "2br": 1880, "3br": 2410, "4br": 2840},  # Carol Stream
    "60189": {"studio": 1760, "1br": 1890, "2br": 2130, "3br": 2740, "4br": 3210},  # Wheaton
    "60190": {"studio": 1760, "1br": 1890, "2br": 2130, "3br": 2740, "4br": 3210},  # Winfield
    "60191": {"studio": 1610, "1br": 1720, "2br": 1940, "3br": 2490, "4br": 2930},  # Wood Dale
    "60199": {"studio": 1760, "1br": 1890, "2br": 2130, "3br": 2740, "4br": 3210},  # Carol Stream
    "60502": {"studio": 1980, "1br": 2120, "2br": 2390, "3br": 3070, "4br": 3610},  # Aurora
    "60504": {"studio": 2145, "1br": 2310, "2br": 2640, "3br": 3366, "4br": 3971},  # Aurora
    "60514": {"studio": 1860, "1br": 1990, "2br": 2250, "3br": 2890, "4br": 3390},  # Clarendon Hills
    "60515": {"studio": 1710, "1br": 1830, "2br": 2070, "3br": 2660, "4br": 3120},  # Downers Grove
    "60516": {"studio": 1710, "1br": 1830, "2br": 2070, "3br": 2660, "4br": 3120},  # Downers Grove
    "60517": {"studio": 1710, "1br": 1830, "2br": 2070, "3br": 2660, "4br": 3120},  # Woodridge
    "60519": {"studio": 1710, "1br": 1830, "2br": 2070, "3br": 2660, "4br": 3120},  # Eola
    "60521": {"studio": 2060, "1br": 2210, "2br": 2490, "3br": 3200, "4br": 3760},  # Hinsdale
    "60523": {"studio": 2270, "1br": 2430, "2br": 2740, "3br": 3520, "4br": 4130},  # Oak Brook
    "60527": {"studio": 1960, "1br": 2100, "2br": 2370, "3br": 3040, "4br": 3570},  # Willowbrook
    "60532": {"studio": 1760, "1br": 1890, "2br": 2130, "3br": 2740, "4br": 3210},  # Lisle
    "60540": {"studio": 1860, "1br": 1990, "2br": 2250, "3br": 2890, "4br": 3390},  # Naperville
    "60555": {"studio": 1760, "1br": 1890, "2br": 2130, "3br": 2740, "4br": 3210},  # Warrenville
    "60559": {"studio": 1760, "1br": 1890, "2br": 2130, "3br": 2740, "4br": 3210},  # Westmont
    "60561": {"studio": 1710, "1br": 1830, "2br": 2070, "3br": 2660, "4br": 3120},  # Darien
    "60563": {"studio": 2000, "1br": 2130, "2br": 2410, "3br": 3100, "4br": 3640},  # Naperville
    "60565": {"studio": 1860, "1br": 1990, "2br": 2250, "3br": 2890, "4br": 3390},  # Naperville
}

DUPAGE_TOWN_TO_ZIPS = {
    "Addison": ["60101"],
    "Aurora": ["60502", "60504"],
    "Bartlett": ["60103"],
    "Bensenville": ["60106"],
    "Bloomingdale": ["60108", "60117"],
    "Carol Stream": ["60116", "60188", "60199"],
    "Clarendon Hills": ["60514"],
    "Darien": ["60561"],
    "Downers Grove": ["60515", "60516"],
    "Elmhurst": ["60126"],
    "Glen Ellyn": ["60137", "60138"],
    "Glendale Heights": ["60139"],
    "Hinsdale": ["60521"],
    "Itasca": ["60143"],
    "Lisle": ["60532"],
    "Lombard": ["60148", "60157"],
    "Naperville": ["60540", "60563", "60565"],
    "Oak Brook": ["60523"],
    "Villa Park": ["60181"],
    "Warrenville": ["60555"],
    "West Chicago": ["60185"],
    "Westmont": ["60559"],
    "Wheaton": ["60187", "60189"],
    "Willowbrook": ["60527"],
    "Winfield": ["60190"],
    "Wood Dale": ["60191"],
    "Woodridge": ["60517"],
}


# =============================================================================
# WILL COUNTY DATA (Direct ZIP to amounts)
# =============================================================================

WILL_ZIP_AMOUNTS = {
    # Housing Authority of Joliet - Effective October 1, 2025
    # Source: https://www.hajoliet.org/sites/default/files/file-attachements/2026_haj_payment_standards.10-2025.pdf
    "60153": {"studio": 1386, "1br": 1485, "2br": 1672, "3br": 2156, "4br": 2486},  # Maywood
    "60401": {"studio": 1287, "1br": 1375, "2br": 1551, "3br": 2002, "4br": 2310},  # Beecher
    "60403": {"studio": 1540, "1br": 1650, "2br": 1859, "3br": 2398, "4br": 2772},  # Crest Hill
    "60404": {"studio": 2189, "1br": 2332, "2br": 2629, "3br": 3388, "4br": 3916},  # Shorewood
    "60407": {"studio": 1320, "1br": 1430, "2br": 1749, "3br": 2332, "4br": 2629},  # Godley
    "60408": {"studio": 1375, "1br": 1474, "2br": 1661, "3br": 2134, "4br": 2475},  # Braidwood
    "60410": {"studio": 1837, "1br": 1969, "2br": 2310, "3br": 3025, "4br": 3465},  # Channahon
    "60416": {"studio": 1089, "1br": 1177, "2br": 1540, "3br": 2090, "4br": 2321},  # Coal City
    "60417": {"studio": 1430, "1br": 1529, "2br": 1727, "3br": 2222, "4br": 2574},  # Crete
    "60421": {"studio": 1265, "1br": 1342, "2br": 1518, "3br": 1958, "4br": 2266},  # Elwood
    "60423": {"studio": 1683, "1br": 1793, "2br": 2024, "3br": 2607, "4br": 3014},  # Frankfort
    "60431": {"studio": 1650, "1br": 1771, "2br": 2068, "3br": 2706, "4br": 3047},  # Joliet
    "60432": {"studio": 1430, "1br": 1518, "2br": 1716, "3br": 2211, "4br": 2552},  # Joliet
    "60433": {"studio": 1452, "1br": 1551, "2br": 1749, "3br": 2255, "4br": 2607},  # Joliet
    "60434": {"studio": 1606, "1br": 1716, "2br": 1936, "3br": 2497, "4br": 2882},  # Joliet
    "60435": {"studio": 1485, "1br": 1595, "2br": 1793, "3br": 2310, "4br": 2673},  # Joliet
    "60436": {"studio": 1518, "1br": 1617, "2br": 1826, "3br": 2354, "4br": 2717},  # Joliet
    "60439": {"studio": 1419, "1br": 1518, "2br": 1705, "3br": 2200, "4br": 2541},  # Lemont
    "60440": {"studio": 1881, "1br": 2013, "2br": 2266, "3br": 2915, "4br": 3377},  # Bolingbrook
    "60441": {"studio": 1716, "1br": 1837, "2br": 2068, "3br": 2662, "4br": 3080},  # Lockport
    "60442": {"studio": 1265, "1br": 1353, "2br": 1529, "3br": 1969, "4br": 2277},  # Manhattan
    "60446": {"studio": 2112, "1br": 2255, "2br": 2541, "3br": 3267, "4br": 3784},  # Romeoville
    "60447": {"studio": 1430, "1br": 1551, "2br": 1969, "3br": 2662, "4br": 2948},  # Minooka
    "60448": {"studio": 1694, "1br": 1804, "2br": 2035, "3br": 2618, "4br": 3036},  # Mokena
    "60449": {"studio": 1375, "1br": 1463, "2br": 1650, "3br": 2123, "4br": 2453},  # Monee
    "60451": {"studio": 1485, "1br": 1595, "2br": 1793, "3br": 2310, "4br": 2673},  # New Lenox
    "60466": {"studio": 1650, "1br": 1771, "2br": 1991, "3br": 2563, "4br": 2970},  # Park Forest
    "60467": {"studio": 2134, "1br": 2277, "2br": 2563, "3br": 3300, "4br": 3817},  # Orland Park
    "60468": {"studio": 1210, "1br": 1287, "2br": 1463, "3br": 1881, "4br": 2167},  # Peotone
    "60471": {"studio": 1518, "1br": 1617, "2br": 1826, "3br": 2354, "4br": 2717},  # Richton Park
    "60475": {"studio": 1166, "1br": 1243, "2br": 1397, "3br": 1804, "4br": 2079},  # Steger
    "60481": {"studio": 1177, "1br": 1254, "2br": 1419, "3br": 1826, "4br": 2112},  # Wilmington
    "60484": {"studio": 1683, "1br": 1793, "2br": 2024, "3br": 2607, "4br": 3014},  # University Park
    "60487": {"studio": 1606, "1br": 1716, "2br": 1936, "3br": 2497, "4br": 2882},  # Tinley Park
    "60490": {"studio": 2442, "1br": 2607, "2br": 2937, "3br": 3784, "4br": 4378},  # Bolingbrook
    "60491": {"studio": 1892, "1br": 2024, "2br": 2277, "3br": 2937, "4br": 3388},  # Homer Glen
    "60503": {"studio": 2167, "1br": 2343, "2br": 2750, "3br": 3619, "4br": 4048},  # Aurora
    "60517": {"studio": 1716, "1br": 1837, "2br": 2068, "3br": 2662, "4br": 3080},  # Woodridge
    "60544": {"studio": 2123, "1br": 2266, "2br": 2563, "3br": 3300, "4br": 3806},  # Plainfield
    "60564": {"studio": 2442, "1br": 2607, "2br": 2937, "3br": 3784, "4br": 4378},  # Naperville
    "60565": {"studio": 2079, "1br": 2211, "2br": 2497, "3br": 3212, "4br": 3718},  # Naperville
    "60567": {"studio": 1793, "1br": 1914, "2br": 2156, "3br": 2783, "4br": 3212},  # Naperville
    "60585": {"studio": 2387, "1br": 2563, "2br": 2937, "3br": 3817, "4br": 4345},  # Plainfield
    "60586": {"studio": 2321, "1br": 2497, "2br": 2860, "3br": 3718, "4br": 4235},  # Plainfield
}

WILL_TOWN_TO_ZIPS = {
    "Aurora": ["60503"],
    "Beecher": ["60401"],
    "Bolingbrook": ["60440", "60490"],
    "Braidwood": ["60408"],
    "Channahon": ["60410"],
    "Coal City": ["60416"],
    "Crest Hill": ["60403"],
    "Crete": ["60417"],
    "Elwood": ["60421"],
    "Frankfort": ["60423"],
    "Godley": ["60407"],
    "Homer Glen": ["60491"],
    "Joliet": ["60431", "60432", "60433", "60434", "60435", "60436"],
    "Lemont": ["60439"],
    "Lockport": ["60441"],
    "Manhattan": ["60442"],
    "Maywood": ["60153"],
    "Minooka": ["60447"],
    "Mokena": ["60448"],
    "Monee": ["60449"],
    "Naperville": ["60564", "60565", "60567"],
    "New Lenox": ["60451"],
    "Orland Park": ["60467"],
    "Park Forest": ["60466"],
    "Peotone": ["60468"],
    "Plainfield": ["60544", "60585", "60586"],
    "Richton Park": ["60471"],
    "Romeoville": ["60446"],
    "Shorewood": ["60404"],
    "Steger": ["60475"],
    "Tinley Park": ["60487"],
    "University Park": ["60484"],
    "Wilmington": ["60481"],
    "Woodridge": ["60517"],
}


# =============================================================================
# LAKE COUNTY DATA (Direct ZIP to amounts)
# =============================================================================

LAKE_ZIP_AMOUNTS = {
    # Lake County Housing Authority - Effective January 1, 2026
    # Source: https://www.lakecountyha.org/plugins/show_image.php?id=1662
    "60002": {"studio": 1250, "1br": 1340, "2br": 1510, "3br": 1940, "4br": 2280},  # Antioch
    "60010": {"studio": 2190, "1br": 2340, "2br": 2670, "3br": 3440, "4br": 3980},  # Barrington
    "60011": {"studio": 1470, "1br": 1570, "2br": 1770, "3br": 2500, "4br": 2800},  # Barrington
    "60013": {"studio": 1450, "1br": 1550, "2br": 1750, "3br": 2250, "4br": 2619},  # Cary
    "60015": {"studio": 2190, "1br": 2340, "2br": 2640, "3br": 3390, "4br": 3980},  # Deerfield
    "60020": {"studio": 1370, "1br": 1470, "2br": 1660, "3br": 2130, "4br": 2500},  # Fox Lake
    "60021": {"studio": 2000, "1br": 2135, "2br": 2405, "3br": 3100, "4br": 3590},  # Fox River Grove
    "60030": {"studio": 1630, "1br": 1740, "2br": 1970, "3br": 2700, "4br": 3020},  # Grayslake
    "60031": {"studio": 1690, "1br": 1800, "2br": 2030, "3br": 2610, "4br": 3020},  # Gurnee
    "60035": {"studio": 2070, "1br": 2220, "2br": 2530, "3br": 3220, "4br": 3810},  # Highland Park
    "60040": {"studio": 1860, "1br": 2000, "2br": 2240, "3br": 2880, "4br": 3340},  # Highwood
    "60041": {"studio": 1190, "1br": 1280, "2br": 1450, "3br": 1870, "4br": 2165},  # Ingleside
    "60042": {"studio": 1685, "1br": 1800, "2br": 2025, "3br": 2610, "4br": 3045},  # Island Lake
    "60044": {"studio": 1600, "1br": 1750, "2br": 1900, "3br": 2450, "4br": 2900},  # Lake Bluff
    "60045": {"studio": 2220, "1br": 2370, "2br": 2670, "3br": 3440, "4br": 3980},  # Lake Forest
    "60046": {"studio": 1690, "1br": 1810, "2br": 2040, "3br": 2630, "4br": 2750},  # Lake Villa
    "60047": {"studio": 1970, "1br": 2110, "2br": 2390, "3br": 3060, "4br": 3600},  # Lake Zurich/Long Grove
    "60048": {"studio": 1710, "1br": 1830, "2br": 2070, "3br": 2660, "4br": 3120},  # Libertyville
    "60050": {"studio": 1425, "1br": 1525, "2br": 1750, "3br": 2225, "4br": 2600},  # McHenry
    "60051": {"studio": 1775, "1br": 1905, "2br": 2170, "3br": 2765, "4br": 3270},  # McHenry
    "60060": {"studio": 1660, "1br": 1770, "2br": 2000, "3br": 2600, "4br": 3020},  # Mundelein
    "60061": {"studio": 1900, "1br": 2050, "2br": 2310, "3br": 2975, "4br": 3480},  # Vernon Hills
    "60064": {"studio": 1190, "1br": 1400, "2br": 1715, "3br": 2015, "4br": 2400},  # North Chicago
    "60069": {"studio": 2000, "1br": 2135, "2br": 2405, "3br": 3100, "4br": 3585},  # Lincolnshire
    "60073": {"studio": 1590, "1br": 1700, "2br": 1920, "3br": 2500, "4br": 2900},  # Round Lake
    "60074": {"studio": 1425, "1br": 1525, "2br": 1715, "3br": 2205, "4br": 2550},  # Palatine
    "60081": {"studio": 1375, "1br": 1474, "2br": 1661, "3br": 2134, "4br": 2475},  # Spring Grove
    "60083": {"studio": 1730, "1br": 1845, "2br": 2100, "3br": 2685, "4br": 3160},  # Wadsworth
    "60084": {"studio": 1370, "1br": 1470, "2br": 1660, "3br": 2200, "4br": 2500},  # Wauconda
    "60085": {"studio": 1280, "1br": 1370, "2br": 1540, "3br": 1980, "4br": 2290},  # Waukegan
    "60087": {"studio": 1350, "1br": 1450, "2br": 1630, "3br": 2300, "4br": 2500},  # Waukegan
    "60089": {"studio": 1990, "1br": 2140, "2br": 2440, "3br": 3110, "4br": 3680},  # Buffalo Grove
    "60096": {"studio": 1250, "1br": 1340, "2br": 1510, "3br": 1940, "4br": 2260},  # Winthrop Harbor
    "60099": {"studio": 1280, "1br": 1380, "2br": 1570, "3br": 2000, "4br": 2370},  # Zion
}

LAKE_TOWN_TO_ZIPS = {
    "Antioch": ["60002"],
    "Barrington": ["60010", "60011"],
    "Buffalo Grove": ["60089"],
    "Cary": ["60013"],
    "Deerfield": ["60015"],
    "Fox Lake": ["60020"],
    "Fox River Grove": ["60021"],
    "Grayslake": ["60030"],
    "Gurnee": ["60031"],
    "Highland Park": ["60035"],
    "Highwood": ["60040"],
    "Ingleside": ["60041"],
    "Island Lake": ["60042"],
    "Lake Bluff": ["60044"],
    "Lake Forest": ["60045"],
    "Lake Villa": ["60046"],
    "Lake Zurich": ["60047"],
    "Libertyville": ["60048"],
    "Lincolnshire": ["60069"],
    "Long Grove": ["60047"],
    "McHenry": ["60050", "60051"],
    "Mundelein": ["60060"],
    "North Chicago": ["60064"],
    "Palatine": ["60074"],
    "Round Lake": ["60073"],
    "Spring Grove": ["60081"],
    "Vernon Hills": ["60061"],
    "Wadsworth": ["60083"],
    "Wauconda": ["60084"],
    "Waukegan": ["60085", "60087"],
    "Winthrop Harbor": ["60096"],
    "Zion": ["60099"],
}


# =============================================================================
# LOOKUP FUNCTIONS
# =============================================================================

def get_county_info(county_key: str) -> dict | None:
    """Get county metadata by key (cook, dupage, will, lake)."""
    return COUNTIES.get(county_key.lower())


def get_all_counties() -> list[dict]:
    """Return a list of all counties with payment standards."""
    return [{"key": key, **info} for key, info in COUNTIES.items()]


def get_zips_for_town(town: str) -> list[str]:
    """Get ZIP codes for a town name. Returns empty list if not found."""
    return TOWN_TO_ZIPS.get(town, [])


def get_payment_standard(county_key: str, zip_code: str, bedrooms: int) -> int | None:
    """
    Get the payment standard for a given county, ZIP code, and bedroom count.

    Args:
        county_key: County identifier (cook, dupage, will, lake)
        zip_code: 5-digit ZIP code as string
        bedrooms: Number of bedrooms (0 for studio, 1-4 for 1BR-4BR)

    Returns:
        Payment standard amount in dollars, or None if not found
    """
    county_key = county_key.lower()
    zip_code = str(zip_code).strip()
    bedroom_key = "studio" if bedrooms == 0 else f"{bedrooms}br"

    if county_key == "cook":
        if zip_code not in COOK_ZIP_TO_RANGE:
            return None
        range_letter = COOK_ZIP_TO_RANGE[zip_code]
        if range_letter not in COOK_RANGE_AMOUNTS:
            return None
        return COOK_RANGE_AMOUNTS[range_letter].get(bedroom_key)

    elif county_key == "dupage":
        if zip_code not in DUPAGE_ZIP_AMOUNTS:
            return None
        return DUPAGE_ZIP_AMOUNTS[zip_code].get(bedroom_key)

    elif county_key == "will":
        if zip_code not in WILL_ZIP_AMOUNTS:
            return None
        return WILL_ZIP_AMOUNTS[zip_code].get(bedroom_key)

    elif county_key == "lake":
        if zip_code not in LAKE_ZIP_AMOUNTS:
            return None
        return LAKE_ZIP_AMOUNTS[zip_code].get(bedroom_key)

    return None


def get_all_zip_codes(county_key: str) -> list[str]:
    """Return a sorted list of all ZIP codes for a county."""
    county_key = county_key.lower()

    if county_key == "cook":
        return sorted(COOK_ZIP_TO_RANGE.keys())
    elif county_key == "dupage":
        return sorted(DUPAGE_ZIP_AMOUNTS.keys())
    elif county_key == "will":
        return sorted(WILL_ZIP_AMOUNTS.keys())
    elif county_key == "lake":
        return sorted(LAKE_ZIP_AMOUNTS.keys())

    return []


def is_valid_zip(county_key: str, zip_code: str) -> bool:
    """Check if a ZIP code is valid for a county."""
    return str(zip_code).strip() in get_all_zip_codes(county_key)


def get_all_towns(county_key: str) -> list[str]:
    """Return a sorted list of all town names for a county."""
    county_key = county_key.lower()

    if county_key == "cook":
        return sorted(COOK_TOWN_TO_ZIPS.keys())
    elif county_key == "dupage":
        return sorted(DUPAGE_TOWN_TO_ZIPS.keys())
    elif county_key == "will":
        return sorted(WILL_TOWN_TO_ZIPS.keys())
    elif county_key == "lake":
        return sorted(LAKE_TOWN_TO_ZIPS.keys())

    return []


def get_zips_for_town(county_key: str, town: str) -> list[str]:
    """Get ZIP codes for a town in a county."""
    county_key = county_key.lower()

    if county_key == "cook":
        return COOK_TOWN_TO_ZIPS.get(town, [])
    elif county_key == "dupage":
        return DUPAGE_TOWN_TO_ZIPS.get(town, [])
    elif county_key == "will":
        return WILL_TOWN_TO_ZIPS.get(town, [])
    elif county_key == "lake":
        return LAKE_TOWN_TO_ZIPS.get(town, [])

    return []


def resolve_location(county_key: str, location: str) -> list[str]:
    """
    Convert a location (town name or ZIP code) to a list of ZIP codes.

    Args:
        county_key: County identifier
        location: Either a town name or a ZIP code

    Returns:
        List of ZIP codes
    """
    county_key = county_key.lower()
    location = location.strip()

    # Check if it's a ZIP code (5 digits)
    if len(location) == 5 and location.isdigit():
        if is_valid_zip(county_key, location):
            return [location]
        return []

    # Get the appropriate town mapping
    if county_key == "cook":
        town_map = COOK_TOWN_TO_ZIPS
    elif county_key == "dupage":
        town_map = DUPAGE_TOWN_TO_ZIPS
    elif county_key == "will":
        town_map = WILL_TOWN_TO_ZIPS
    elif county_key == "lake":
        town_map = LAKE_TOWN_TO_ZIPS
    else:
        return []

    # Try to match as town name (case-insensitive)
    for town, zips in town_map.items():
        if town.lower() == location.lower():
            return zips

    return []
