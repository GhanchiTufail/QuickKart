from enum import Enum

class CategoryEnum(str, Enum):
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing & Apparel"
    BOOKS = "Books & Literature"
    HOME = "Home & Kitchen"
    BEAUTY = "Beauty & Personal Care"
    SPORTS = "Sports & Outdoors"
    TOYS = "Toys & Games"
    HEALTH = "Health & Wellness"
    GROCERIES = "Groceries"
    OFFICE = "Office Supplies"
    BABY = "Baby & Kids"
    SHOES = "Shoes & Footwear"
    JEWELRY = "Jewelry & Watches"
    TOOLS = "Tools & Hardware"
    MOVIES = "Movies & Music"

class ELECTRONICS(str, Enum):
    LAPTOPS_COMPUTERS = "Laptops & Computers"
    SMARTPHONES_ACCESSORIES = "Smartphones & Accessories"
    TABLETS_E_READERS = "Tablets & E-Readers"
    TV_HOME_THEATER = "TVs & Home Theater"
    HEADPHONES_SPEAKERS = "Headphones & Speakers"
    CAMERAS_PHOTOGRAPHY = "Cameras & Photography"
    WEARABLE_TECHNOLOGY = "Wearable Technology"
    PRINTERS_SCANNERS = "Printers & Scanners"
    COMPUTER_COMPONENTS = "Computer Components"
    GAMING_CONSOLES = "Gaming Consoles"
    SMART_HOME_DEVICES = "Smart Home Devices"

class CLOTHING(str, Enum):
    MENS_CLOTHING = "Men's Clothing"
    WOMENS_CLOTHING = "Women's Clothing"
    KIDS_CLOTHING = "Kids' Clothing"
    ACTIVEWEAR = "Activewear"
    SLEEPWEAR_LOUNGEWEAR = "Sleepwear & Loungewear"
    SWIMWEAR = "Swimwear"
    FORMAL_WEAR = "Formal Wear"
    WINTER_COATS_JACKETS = "Winter Coats & Jackets"
    BELTS_ACCESSORIES = "Belts & Accessories"
    HATS_CAPS = "Hats & Caps"

class BOOKS(str, Enum):
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    CHILDRENS_BOOKS = "Children's Books"
    TEXTBOOKS = "Textbooks"
    COOKBOOKS = "Cookbooks"
    SCIENCE_FICTION_FANTASY = "Science Fiction & Fantasy"
    MYSTERY_THRILLER = "Mystery & Thriller"
    ROMANCE = "Romance"
    BIOGRAPHIES = "Biographies"
    AUDIOBOOKS = "Audiobooks"
    EBOOKS = "eBooks"
    ACADEMIC_JOURNALS = "Academic Journals"

class HOME(str, Enum):
    FURNITURE = "Furniture"
    KITCHEN_APPLIANCES = "Kitchen Appliances"
    COOKWARE_BAKEWARE = "Cookware & Bakeware"
    BEDDING_BATH = "Bedding & Bath"
    HOME_DECOR = "Home Decor"
    LIGHTING = "Lighting"
    STORAGE_ORGANIZATION = "Storage & Organization"
    GARDENING_OUTDOOR = "Gardening & Outdoor"
    HOME_IMPROVEMENT = "Home Improvement"
    CLEANING_SUPPLIES = "Cleaning Supplies"

class MOVIES(str, Enum):
    DVDS_BLU_RAYS = "DVDs & Blu-rays"
    STREAMING_DEVICES = "Streaming Devices"
    MOVIE_MERCHANDISE = "Movie Merchandise"
    MUSIC_CDS = "Music CDs"
    VINYL_RECORDS = "Vinyl Records"
    CONCERT_VIDEOS = "Concert Videos"
    DOCUMENTARIES = "Documentaries"
    MOVIE_GENRES = "Movie Genres"
    MUSICAL_INSTRUMENTS = "Musical Instruments"
    KARAOKE_MACHINES = "Karaoke Machines"

class SPORTS(str, Enum):
    TEAM_SPORTS = "Team Sports"
    FITNESS_EQUIPMENT = "Fitness Equipment"
    OUTDOOR_RECREATION = "Outdoor Recreation"
    CYCLING = "Cycling"
    YOGA_PILATES = "Yoga & Pilates"
    WATER_SPORTS = "Water Sports"
    WINTER_SPORTS = "Winter Sports"
    CAMPING_HIKING = "Camping & Hiking"
    FISHING_HUNTING = "Fishing & Hunting"
    ATHLETIC_CLOTHING = "Athletic Clothing"

class TOYS(str, Enum):
    TODDLER_TOYS = "Toddler Toys"
    EDUCATIONAL_TOYS = "Educational Toys"
    ACTION_FIGURES = "Action Figures"
    DOLLS_ACCESSORIES = "Dolls & Accessories"
    BOARD_GAMES = "Board Games"
    PUZZLES = "Puzzles"
    BUILDING_SETS = "Building Sets"
    OUTDOOR_TOYS = "Outdoor Toys"
    VIDEO_GAMES = "Video Games"
    STEM_TOYS = "STEM Toys"

class HEALTH(str, Enum):
    VITAMINS_SUPPLEMENTS = "Vitamins & Supplements"
    MEDICAL_SUPPLIES = "Medical Supplies"
    FITNESS_TRACKERS = "Fitness Trackers"
    PAIN_RELIEF = "Pain Relief"
    SEXUAL_WELLNESS = "Sexual Wellness"
    VISION_CARE = "Vision Care"
    FIRST_AID = "First Aid"
    DIET_NUTRITION = "Diet & Nutrition"
    ESSENTIAL_OILS = "Essential Oils"
    MENTAL_HEALTH = "Mental Health"

class GROCERIES(str, Enum):
    PANTRY_STAPLES = "Pantry Staples"
    DAIRY_EGGS = "Dairy & Eggs"
    FRESH_PRODUCE = "Fresh Produce"
    BEVERAGES = "Beverages"
    SNACKS = "Snacks"
    FROZEN_FOODS = "Frozen Foods"
    BAKERY = "Bakery"
    MEAT_SEAFOOD = "Meat & Seafood"
    INTERNATIONAL_CUISINE = "International Cuisine"
    ORGANIC_NATURAL = "Organic & Natural"

class OFFICE(str, Enum):
    STATIONERY = "Stationery"
    OFFICE_FURNITURE = "Office Furniture"
    PRINTER_INK = "Printer & Ink"
    FILING_STORAGE = "Filing & Storage"
    SHIPPING_SUPPLIES = "Shipping Supplies"
    PRESENTATION_BOARDS = "Presentation Boards"
    WRITING_INSTRUMENTS = "Writing Instruments"
    CALENDARS_PLANNERS = "Calendars & Planners"
    BREAKROOM_SUPPLIES = "Breakroom Supplies"
    OFFICE_TECHNOLOGY = "Office Technology"

class BABY(str, Enum):
    BABY_GEAR = "Baby Gear"
    BABY_CLOTHING = "Baby Clothing"
    DIAPERING = "Diapering"
    FEEDING = "Feeding"
    NURSERY_FURNITURE = "Nursery Furniture"
    BABY_SAFETY = "Baby Safety"
    TOYS_ACTIVITIES = "Toys & Activities"
    MATERNITY_CARE = "Maternity Care"
    KIDS_FURNITURE = "Kids' Furniture"
    SCHOOL_SUPPLIES = "School Supplies"

class SHOES(str, Enum):
    MENS_SHOES = "Men's Shoes"
    WOMENS_SHOES = "Women's Shoes"
    KIDS_SHOES = "Kids' Shoes"
    ATHLETIC_SHOES = "Athletic Shoes"
    BOOTS = "Boots"
    SANDALS = "Sandals"
    FORMAL_SHOES = "Formal Shoes"
    SLIPPERS = "Slippers"
    SHOE_CARE = "Shoe Care"
    SPECIALTY_FOOTWEAR = "Specialty Footwear"
class JEWELRY(str, Enum):
    NECKLACES = "Necklaces"
    EARRINGS = "Earrings"
    BRACELETS = "Bracelets"
    RINGS = "Rings"
    WATCHES = "Watches"
    FINE_JEWELRY = "Fine Jewelry"
    FASHION_JEWELRY = "Fashion Jewelry"
    BODY_JEWELRY = "Body Jewelry"
    JEWELRY_BOXES = "Jewelry Boxes"
    WEDDING_ENGAGEMENT = "Wedding & Engagement"

class TOOLS(str, Enum):
    HAND_TOOLS = "Hand Tools"
    POWER_TOOLS = "Power Tools"
    TOOL_STORAGE = "Tool Storage"
    BUILDING_SUPPLIES = "Building Supplies"
    ELECTRICAL = "Electrical"
    PLUMBING = "Plumbing"
    PAINTING_SUPPLIES = "Painting Supplies"
    GARDENING_TOOLS = "Gardening Tools"
    SAFETY_EQUIPMENT = "Safety Equipment"
    HARDWARE = "Hardware"

class BEAUTY(str, Enum):
    SKINCARE = "Skincare"
    MAKEUP = "Makeup"
    HAIR_CARE = "Hair Care"
    FRAGRANCES = "Fragrances"
    BATH_BODY = "Bath & Body"
    ORAL_CARE = "Oral Care"
    NAIL_CARE = "Nail Care"
    MEN_GROOMING = "Men's Grooming"
    BEAUTY_TOOLS = "Beauty Tools"
    SPA_WELLNESS = "Spa & Wellness"

CATEGORY_MAPPING = {
    CategoryEnum.ELECTRONICS: ELECTRONICS,
    CategoryEnum.CLOTHING: CLOTHING,
    CategoryEnum.BOOKS: BOOKS,
    CategoryEnum.HOME: HOME,
    CategoryEnum.BEAUTY: BEAUTY,
    CategoryEnum.SPORTS: SPORTS,
    CategoryEnum.TOYS: TOYS,
    CategoryEnum.HEALTH: HEALTH,
    CategoryEnum.GROCERIES: GROCERIES,
    CategoryEnum.OFFICE: OFFICE,
    CategoryEnum.BABY: BABY,
    CategoryEnum.SHOES: SHOES,
    CategoryEnum.JEWELRY: JEWELRY,
    CategoryEnum.TOOLS: TOOLS,
    CategoryEnum.MOVIES: MOVIES
}