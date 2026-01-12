"""
HACC Payment Standards for Cook County, IL
Effective January 1, 2026

Data extracted from: Housing Authority of Cook County Payment Standards PDF
"""

# Payment amounts by Range letter (A-Z) and bedroom count
# Format: Range -> {bedrooms: amount}
RANGE_AMOUNTS = {
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

# ZIP code to Range letter mapping
# Extracted from HACC Payment Standards PDF (Pages 1-2)
ZIP_TO_RANGE = {
    # Page 1 - City/ZIP/Range mappings
    "60803": "C",  # Alsip
    "60501": "A",  # Argo
    "60004": "T",  # Arlington Heights
    "60005": "O",  # Arlington Heights
    "60006": "L",  # Arlington Heights
    "60010": "Z",  # Barrington
    "60011": "M",  # Barrington
    "60010": "Z",  # Barrington Hills
    "60103": "W",  # Bartlett
    "60133": "P",  # Bartlett (East Hazel Crest)
    "60455": "B",  # Bedford Park
    "60458": "H",  # Bedford Park (Elk Grove Village)
    "60459": "I",  # Bedford Park (Elmwood Park)
    "60499": "L",  # Bedford Park (Evanston)
    "60501": "A",  # Bedford Park (Evanston)
    "60638": "F",  # Bedford Park (Evanston)
    "60104": "F",  # Bellwood
    "60163": "C",  # Berkeley (Evergreen Park)
    "60402": "H",  # Berwyn
    "60406": "A",  # Blue Island
    "60455": "B",  # Bridgeview
    "60153": "E",  # Broadview
    "60155": "D",  # Broadview (Forest View)
    "60513": "F",  # Brookfield
    "60089": "X",  # Buffalo Grove
    "60459": "I",  # Burbank
    "60633": "D",  # Burnham (Glenview)
    "60527": "U",  # Burr Ridge
    "60409": "D",  # Calumet City (Golf)
    "60643": "H",  # Calumet Park
    "60827": "C",  # Calumet Park (Harvey)
    "60411": "C",  # Chicago Heights (Harvey)
    "60412": "L",  # Chicago Heights
    "60415": "D",  # Chicago Ridge
    "60478": "T",  # Country Club Hills
    "60525": "J",  # Countryside (Hickory Hills)
    "60418": "I",  # Crestwood
    "60445": "E",  # Crestwood (Hillside)

    # Page 1 continued
    "60010": "Z",  # Deer Park
    "60501": "A",  # Deer Park
    "60004": "T",  # Deerfield
    "60015": "Z",  # Des Plaines
    "60016": "N",  # Des Plaines
    "60017": "L",  # Des Plaines
    "60018": "E",  # Des Plaines
    "60406": "A",  # Dixmoor
    "60426": "C",  # Dixmoor (Hometown)
    "60419": "Q",  # Dolton (Homewood)
    "60429": "P",  # Dolton (Homewood)
    "60007": "P",  # Indian Head Park (Elk Grove Village)
    "60009": "L",  # Inverness
    "60707": "I",  # Inverness
    "60201": "X",  # Evanston (Justice)
    "60202": "T",  # Evanston (Kenilworth)
    "60203": "Y",  # Evanston (La Grange)
    "60204": "L",  # Evanston (LaGrange)
    "60805": "J",  # LaGrange Highlands
    "60422": "Z",  # La Grange Park (Flossmoor)
    "60411": "C",  # Lansing
    "60130": "I",  # Lemont
    "60402": "H",  # Lincolnwood
    "60638": "F",  # Lincolnwood
    "60712": "Z",  # Lincolnwood (Palatine)
    "60411": "C",  # Lynwood (Palatine)
    "60131": "B",  # Lynwood (Franklin Park)
    "60022": "Y",  # Lyons (Glencoe)
    "60025": "R",  # Markham
    "60026": "X",  # Markham (Glenview)
    "60425": "U",  # Matteson
    "60029": "U",  # McCook
    "60133": "P",  # Melrose Park
    "60426": "C",  # Melrose Park (Harvey)
    "60428": "R",  # Melrose Park
    "60656": "M",  # Melrose Park
    "60706": "G",  # Melrose Park
    "60429": "P",  # Merrionette Park (Hazel Crest)
    "60457": "C",  # Merrionette Park
    "60162": "N",  # Midlothian
    "60163": "C",  # Morton Grove

    # Page 1 continued - right columns
    "60141": "A",  # Hines
    "60525": "J",  # Hodgkins
    "60010": "Z",  # Hoffman Estates
    "60067": "S",  # Hoffman Estates (Norridge)
    "60169": "Q",  # Hoffman Estates (North Riverside)
    "60192": "Z",  # Hoffman Estates (Northbrook)
    "60195": "S",  # Hoffman Estates (Northbrook)
    "60456": "K",  # Hometown (Northfield)
    "60422": "Z",  # Homewood (Northlake)
    "60430": "K",  # Homewood (Oak Forest)
    "60525": "J",  # Oak Lawn
    "60453": "H",  # Oak Lawn
    "60454": "L",  # Oak Lawn (Schiller Park)
    "60455": "B",  # Oak Lawn (Skokie)
    "60456": "K",  # Oak Lawn (Skokie)
    "60457": "C",  # Oak Lawn (South Barrington)
    "60458": "H",  # Oak Lawn (South Chgo Hts)
    "60459": "I",  # Oak Lawn (South Holland)
    "60461": "Z",  # Olympia Fields
    "60477": "M",  # Orland Hills
    "60487": "K",  # Orland Hills (Stickney)
    "60438": "F",  # Orland Hills (Lansing)
    "60439": "J",  # Orland Park
    "60462": "N",  # Orland Park
    "60467": "V",  # Orland Park (Streamwood)
    "60067": "S",  # Palatine
    "60074": "N",  # Palatine
    "60078": "L",  # Palatine (Tinley Park)
    "60463": "U",  # Palos Heights (Tinley Park)
    "60428": "R",  # Palos Hills
    "60465": "G",  # Palos Hills (Tinley Park)
    "60464": "Y",  # Palos Park
    "60068": "Q",  # Park Ridge
    "60426": "C",  # Phoenix (Westchester)
    "60161": "L",  # Posen
    "60163": "C",  # Prospect Heights
    "60164": "B",  # Richton Park
    "60471": "I",  # Richton Park
    "60165": "F",  # River Forest (Melrose Park)
    "60655": "I",  # River Grove (Merrionette Park)
    "60803": "C",  # Riverdale (Merrionette Park)
    "60827": "C",  # Riverdale
    "60546": "H",  # Riverside
    "60472": "G",  # Robbins

    # Page 1 - far right columns
    "60056": "O",  # Mount Prospect
    "60714": "I",  # Niles
    "60656": "M",  # Norridge
    "60706": "G",  # Norridge
    "60546": "H",  # North Riverside
    "60062": "W",  # Northbrook
    "60065": "L",  # Northbrook
    "60093": "Y",  # Northfield
    "60164": "B",  # Northlake
    "60452": "G",  # Oak Forest
    "60453": "H",  # Schiller Park
    "60454": "L",  # Schiller Park
    "60455": "B",  # Skokie
    "60456": "K",  # Skokie
    "60457": "C",  # South Barrington
    "60458": "H",  # South Chgo Hts
    "60459": "I",  # South Holland
    "60461": "Z",  # Steger
    "60402": "H",  # Stickney
    "60487": "K",  # Stickney
    "60638": "F",  # Stickney
    "60165": "F",  # Stone Park
    "60107": "X",  # Streamwood
    "60501": "A",  # Summit
    "60476": "F",  # Thornton
    "60477": "M",  # Tinley Park
    "60478": "T",  # Tinley Park
    "60487": "K",  # Tinley Park
    "60466": "N",  # University Park
    "60484": "N",  # University Park
    "60154": "T",  # Westchester
    "60558": "Z",  # Western Springs
    "60469": "I",  # Posen
    "60070": "J",  # Prospect Heights (Wheeling)
    "60471": "I",  # Richton Park
    "60480": "M",  # Willow Springs
    "60305": "N",  # River Forest (Wilmette)
    "60171": "G",  # River Grove
    "60827": "C",  # Riverdale
    "60093": "Y",  # Winnetka
    "60482": "E",  # Worth

    # Page 2 - Additional ZIP to Range mappings
    "60004": "T",
    "60005": "O",
    "60006": "L",
    "60007": "P",
    "60008": "Q",
    "60009": "L",
    "60010": "Z",
    "60011": "M",
    "60015": "Z",
    "60016": "N",
    "60017": "L",
    "60018": "E",
    "60022": "Y",
    "60025": "R",
    "60026": "X",
    "60029": "U",
    "60043": "Z",
    "60053": "Z",
    "60056": "O",
    "60062": "W",
    "60065": "L",
    "60067": "S",
    "60068": "Q",
    "60070": "J",
    "60074": "N",
    "60076": "P",
    "60077": "N",
    "60078": "L",
    "60089": "X",
    "60090": "P",
    "60091": "Z",
    "60093": "Y",
    "60103": "W",
    "60104": "F",
    "60107": "X",
    "60120": "G",
    "60126": "V",
    "60130": "I",
    "60131": "B",
    "60133": "P",
    "60141": "A",
    "60153": "E",
    "60154": "T",
    "60155": "D",
    "60159": "L",
    "60160": "F",
    "60161": "L",
    "60162": "N",
    "60163": "C",
    "60164": "B",
    "60165": "F",
    "60168": "L",
    "60169": "Q",
    "60171": "G",
    "60172": "S",
    "60173": "W",
    "60176": "G",
    "60192": "Z",
    "60193": "U",
    "60194": "V",
    "60195": "S",
    "60201": "X",
    "60202": "T",
    "60203": "Y",
    "60204": "L",
    "60301": "N", # Added for Oak Park area
    "60302": "N",
    "60304": "N",
    "60305": "N",
    "60402": "H",
    "60406": "A",
    "60409": "D",
    "60411": "C",
    "60412": "L",
    "60415": "D",
    "60418": "I",
    "60419": "Q",
    "60422": "Z",
    "60423": "O",
    "60425": "U",
    "60426": "C",
    "60428": "R",
    "60429": "P",
    "60430": "K",
    "60438": "F",
    "60439": "J",
    "60443": "Q",
    "60445": "E",
    "60452": "G",
    "60453": "H",
    "60454": "L",
    "60455": "B",
    "60456": "K",
    "60457": "C",
    "60458": "H",
    "60459": "I",
    "60461": "Z",
    "60462": "N",
    "60463": "U",
    "60464": "Y",
    "60465": "G",
    "60466": "N",
    "60467": "V",
    "60469": "I",
    "60471": "I",
    "60472": "G",
    "60473": "V",
    "60475": "A",
    "60476": "F",
    "60477": "M",
    "60478": "T",
    "60480": "M",
    "60482": "E",
    "60484": "N",
    "60487": "K",
    "60501": "A",
    "60513": "F",
    "60521": "Z",
    "60525": "J",
    "60526": "K",
    "60527": "U",
    "60534": "D",
    "60546": "H",
    "60558": "Z",
    "60601": "J", # Chicago downtown
    "60602": "J",
    "60603": "J",
    "60604": "J",
    "60605": "J",
    "60606": "J",
    "60607": "J",
    "60608": "H",
    "60609": "F",
    "60610": "Z",
    "60611": "Z",
    "60612": "L",
    "60613": "H",
    "60614": "Z",
    "60615": "D",
    "60616": "G",
    "60617": "B",
    "60618": "L",
    "60619": "C",
    "60620": "D",
    "60621": "B",
    "60622": "N",
    "60623": "F",
    "60624": "D",
    "60625": "L",
    "60626": "K",
    "60628": "C",
    "60629": "F",
    "60630": "K",
    "60631": "M",
    "60632": "F",
    "60633": "D",
    "60634": "L",
    "60636": "D",
    "60637": "E",
    "60638": "F",
    "60639": "H",
    "60640": "M",
    "60641": "L",
    "60642": "N",
    "60643": "H",
    "60644": "E",
    "60645": "M",
    "60646": "L",
    "60647": "M",
    "60649": "C",
    "60651": "F",
    "60652": "G",
    "60653": "D",
    "60654": "N",
    "60655": "I",
    "60656": "M",
    "60657": "Q",
    "60659": "K",
    "60660": "L",
    "60661": "L",
    "60706": "G",
    "60707": "I",
    "60712": "Z",
    "60714": "I",
    "60803": "C",
    "60805": "J",
    "60827": "C",
}


def get_payment_standard(zip_code: str, bedrooms: int) -> int | None:
    """
    Get the HACC payment standard for a given ZIP code and bedroom count.

    Args:
        zip_code: 5-digit ZIP code as string
        bedrooms: Number of bedrooms (0 for studio, 1-4 for 1BR-4BR)

    Returns:
        Payment standard amount in dollars, or None if ZIP not found
    """
    zip_code = str(zip_code).strip()

    if zip_code not in ZIP_TO_RANGE:
        return None

    range_letter = ZIP_TO_RANGE[zip_code]

    if range_letter not in RANGE_AMOUNTS:
        return None

    bedroom_key = "studio" if bedrooms == 0 else f"{bedrooms}br"

    if bedroom_key not in RANGE_AMOUNTS[range_letter]:
        return None

    return RANGE_AMOUNTS[range_letter][bedroom_key]


def get_all_zip_codes() -> list[str]:
    """Return a sorted list of all ZIP codes with payment standards."""
    return sorted(ZIP_TO_RANGE.keys())


def is_valid_zip(zip_code: str) -> bool:
    """Check if a ZIP code is in the HACC payment standards."""
    return str(zip_code).strip() in ZIP_TO_RANGE
