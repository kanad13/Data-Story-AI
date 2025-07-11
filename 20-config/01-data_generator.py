import pandas as pd
import numpy as np
import random
import os
import duckdb
from datetime import datetime, timedelta


"""
Generates synthetic e-commerce sales data and loads it into DuckDB.

This script creates a Pandas DataFrame of synthetic sales data, including
product information, customer details, order dates, and more. It then
loads this data into both an in-memory and a persistent DuckDB database
for demonstration and analysis purposes.
"""


def create_data_definitions():
    """
    Defines and returns data structures for categories, products, prices, etc.

    This function sets up dictionaries and lists that define the categories,
    subcategories, product names, price ranges, payment methods, shipping states,
    and order statuses used for generating the synthetic sales data.

    Returns:
        tuple: A tuple containing dictionaries and lists for data definitions:
               (categories, product_names, price_ranges, payment_methods,
                shipping_states, order_statuses)
    """
    # 1. Define Categories and Subcategories
    categories = {
        "Electronics & Gadgets": ["Smartphones", "Laptops", "Headphones", "Smartwatches"],
        "Clothing & Apparel": ["Men's Clothing", "Women's Clothing", "Shoes", "Accessories"],
        "Home & Furniture": ["Furniture", "Home Decor", "Kitchen & Dining", "Bedding & Bath"],
        "Books & Media": ["Books", "E-books", "Movies", "Music"],
        "Beauty & Personal Care": ["Makeup", "Skincare", "Haircare", "Fragrances"],
        "Sports & Outdoors": ["Fitness Equipment", "Sports Apparel", "Camping & Hiking", "Cycling"],
        "Fashion Accessories": ["Jewelry", "Watches", "Bags & Luggage", "Sunglasses"],
        "Toys & Games": ["Educational Toys", "Action Figures", "Board Games", "Puzzles"]
    }

    # 2. Define Product Names (Realistic Names)
    product_names = {
        "Smartphones": [
            "Samsung Galaxy S24 Ultra",
            "Apple iPhone 15 Pro Max",
            "Google Pixel 8 Pro",
            "OnePlus 12",
            "Xiaomi 14 Pro",
            "Samsung Galaxy A54",
            "Apple iPhone 14",
            "Motorola Moto G Power (2024)",
            "Nothing Phone (2a)",
            "Google Pixel 7a"
        ],
        "Laptops": [
            "Apple MacBook Pro 16-inch (M3 Max)",
            "Dell XPS 15",
            "HP Spectre x360 14",
            "Lenovo ThinkPad X1 Carbon Gen 12",
            "Microsoft Surface Laptop Studio 2",
            "ASUS ROG Zephyrus G14",
            "Acer Swift 5",
            "LG Gram Style",
            "Razer Blade 15 Advanced Model",
            "Framework Laptop 16"
        ],
        "Headphones": [
            "Sony WH-1000XM5",
            "Apple AirPods Max",
            "Bose QuietComfort 45",
            "Sennheiser HD 800 S",
            "Jabra Elite 8 Active",
            "Beats Studio Pro",
            "Technics EAH-AZ80",
            "Anker Soundcore Life Q30",
            "Skullcandy Hesh ANC",
            "Audio-Technica ATH-M50xBT2"
        ],
        "Smartwatches": [
            "Apple Watch Series 9",
            "Samsung Galaxy Watch 6 Classic",
            "Google Pixel Watch 2",
            "Fitbit Versa 4",
            "Garmin Fenix 7",
            "Amazfit GTS 4 Mini",
            "Huawei Watch GT 4",
            "Withings ScanWatch Nova",
            "TicWatch Pro 5",
            "Polar Vantage V3"
        ],
        "Men's Clothing": [
            "Levi's 501 Original Fit Jeans",
            "Nike Dri-FIT T-Shirt",
            "Adidas Tiro 24 Training Pants",
            "Polo Ralph Lauren Classic Fit Oxford Shirt",
            "Tommy Hilfiger Lightweight Jacket",
            "Calvin Klein Boxer Briefs",
            "Uniqlo Ultra Light Down Vest",
            "Dockers Signature Khaki Pants",
            "J.Crew Slim-Fit Chino",
            "The North Face Apex Bionic Jacket"
        ],
        "Women's Clothing": [
            "Lululemon Align High-Rise Leggings",
            "Zara Flowy Printed Dress",
            "H&M Rib-knit Top",
            "Madewell Perfect Vintage Jeans",
            "Free People Ottoman Slouchy Tunic",
            "Anthropologie Somerset Maxi Dress",
            "Old Navy High-Waisted Leggings",
            "ASOS DESIGN Curve Wrap Mini Dress",
            "Banana Republic Factory Sloan Skinny Pant",
            "Everlane ReNew Teddy Liner"
        ],
        "Shoes": [
            "Nike Air Force 1 '07",
            "Adidas Ultraboost 22",
            "New Balance 990v5",
            "Converse Chuck Taylor All Star",
            "Vans Old Skool",
            "Dr. Martens 1460 Boots",
            "Timberland 6-Inch Premium Waterproof Boots",
            "Birkenstock Arizona Sandals",
            "Crocs Classic Clogs",
            "UGG Classic Mini II Boots"
        ],
        "Accessories": [
            "Ray-Ban Wayfarer Sunglasses",
            "Fjällräven Kånken Backpack",
            "Herschel Supply Co. Little America Backpack",
            "Anker PowerCore 10000 Portable Charger",
            "Apple USB-C to Lightning Cable",
            "Samsung 25W USB-C Charger",
            "Belkin Surge Protector Power Strip",
            "PopSockets PopGrip",
            "Tile Mate Bluetooth Tracker",
            "Hydro Flask Water Bottle"
        ],
        "Jewelry": [
            "Tiffany & Co. Diamond Pendant Necklace",
            "Cartier LOVE Bracelet",
            "Pandora Charm Bracelet",
            "Swarovski Crystal Stud Earrings",
            "Rolex Submariner Watch",
            "Omega Seamaster Planet Ocean Watch",
            "Michael Kors Gold-Tone Hoop Earrings",
            "Kate Spade New York Pendant Necklace",
            "Alex and Ani Bangle Bracelet",
            "David Yurman Cable Classics Bracelet"
        ],
        "Sunglasses": [
            "Ray-Ban Aviator Classic",
            "Oakley Holbrook Sunglasses",
            "Persol PO3092SM Sunglasses",
            "Maui Jim Polarized Sunglasses",
            "Warby Parker Haskell Sunglasses",
            "Gucci Oversized Square Sunglasses",
            "Prada Catwalk Sunglasses",
            "Tom Ford FT0009 Sunglasses",
            "Chanel Butterfly Sunglasses",
            "Dior SoReal Sunglasses"
        ],
        "Board Games": [
            "Catan",
            "Ticket to Ride",
            "Pandemic",
            "Codenames",
            "7 Wonders",
            "Gloomhaven",
            "Azul",
            "Spirit Island",
            "Wingspan",
            "Terraforming Mars"
        ],
         "Puzzles": [
            "Ravensburger 1000pc - Neuschwanstein Castle",
            "Buffalo Games - Charles Wysocki - Americana Collection - Apple Pickin' Time - 1000 Piece Jigsaw Puzzle",
            "Springbok - Coca-Cola Diner - 1000 Piece Jigsaw Puzzle",
            "White Mountain Puzzles - Candy Wrappers - 1000 Piece Jigsaw Puzzle",
            "Ceaco - Thomas Kinkade - Disney Dreams Collection - Mickey and Minnie Sweetheart Campfire - 750 Piece Jigsaw Puzzle",
            "Melissa & Doug - Solar System Floor Puzzle (48 pcs)",
            "Mudpuppy - Glow-in-the-Dark Constellations Puzzle (100 pcs)",
            "Magical Unicorns 500 Piece Round Jigsaw Puzzle",
            "National Geographic - World Map Puzzle (1000 pcs)",
            "MasterPieces - NFL Playing Field - StadiumView 3D Puzzle (128 pcs)"
        ],
        "Furniture": [
            "IKEA Hemnes Bed Frame",
            "West Elm Andes Sofa",
            "Ashley Furniture Signature Design - Larkinhurst Sofa",
            "CB2 Peek Acrylic Coffee Table",
            "Article Sven Charme Tan Sofa",
            "Wayfair Basics Task Chair",
            "AmazonBasics Classic Puresoft Padded Office Chair",
            "Nathan James Amalia Console Table",
            "Target Threshold Windham 5 Drawer Dresser",
            "Pottery Barn Teen Beanbag Chair"
        ],
        "Home Decor": [
            "Yankee Candle Large Jar Candle - Vanilla Bean",
            "Diptyque Baies Candle",
            "Nest Fragrances Reed Diffuser - Bamboo",
            "Umbra Prisma Wall Decor",
            "Kate and Laurel Sylvie Framed Canvas Wall Art",
            "Rifle Paper Co. Tapestry - Garden Party",
            "Hearth & Hand with Magnolia Throw Blanket",
            "Brooklinen Linen Throw Pillow Cover",
            "CB2 Brass Wall Mirror",
            "West Elm Ceramic Vase"
        ],
        "Kitchen & Dining": [
            "Instant Pot Duo 7-in-1 Multi-Cooker",
            "Ninja Foodi 8-in-1 Digital Air Fryer",
            "KitchenAid Stand Mixer",
            "Cuisinart Food Processor",
            "Le Creuset Dutch Oven",
            "All-Clad Stainless Steel Cookware Set",
            "Pyrex Glass Mixing Bowl Set",
            "Corelle Livingware 16-Piece Dinnerware Set",
            "Oneida Countess 45-Piece Flatware Set",
            "Libbey Classic Tumbler Glasses, Set of 12"
        ],
        "Bedding & Bath": [
            "Brooklinen Luxe Core Sheet Set",
            "Parachute Percale Sheet Set",
            "Casper Original Pillow",
            "Purple Harmony Pillow",
            "Linenspa Down Alternative Comforter",
            "Buffy Breeze Comforter",
            "Turkish Cotton Bath Towel Set",
            "Amazon Basics Microfiber Bath Towels",
            "Simple Shower Curtain",
            "Bath & Body Works Shower Gel - Japanese Cherry Blossom"
        ],
        "Books": [
            "The Housemaid by Freida McFadden",
            "It Ends With Us by Colleen Hoover",
            "Atomic Habits by James Clear",
            "The Seven Husbands of Evelyn Hugo by Taylor Jenkins Reid",
            "Where the Crawdads Sing by Delia Owens",
            "To Kill a Mockingbird by Harper Lee",
            "Pride and Prejudice by Jane Austen",
            "1984 by George Orwell",
            "The Great Gatsby by F. Scott Fitzgerald",
            "The Lord of the Rings by J.R.R. Tolkien"
        ],
        "E-books": [
            "Kindle Edition: Project Hail Mary by Andy Weir",
            "Kindle Edition: The Midnight Library by Matt Haig",
            "Kindle Edition: Dune by Frank Herbert",
            "Kindle Edition: Sapiens: A Brief History of Humankind by Yuval Noah Harari",
            "Kindle Edition: Educated by Tara Westover",
            "Kobo eBook: The Lincoln Highway by Amor Towles",
            "Kobo eBook: Cloud Cuckoo Land by Anthony Doerr",
            "Kobo eBook: Braiding Sweetgrass by Robin Wall Kimmerer",
            "Google Play Books: The Overstory by Richard Powers",
            "Google Play Books: Gilead by Marilynne Robinson"
        ],
        "Movies": [
            "Oppenheimer (Blu-ray)",
            "Barbie (DVD)",
            "Spider-Man: Across the Spider-Verse (4K UHD)",
            "The Super Mario Bros. Movie (Blu-ray)",
            "Avatar: The Way of Water (DVD)",
            "Top Gun: Maverick (Blu-ray)",
            "Everything Everywhere All at Once (DVD)",
            "Dune (4K UHD)",
            "No Time To Die (Blu-ray)",
            "Parasite (DVD)"
        ],
        "Music": [
            "Taylor Swift - 1989 (Taylor's Version) (CD)",
            "Olivia Rodrigo - GUTS (Vinyl)",
            "Drake - Certified Lover Boy (CD)",
            "Adele - 30 (Vinyl)",
            "Harry Styles - Harry's House (CD)",
            "Billie Eilish - Happier Than Ever (Vinyl)",
            "The Weeknd - After Hours (CD)",
            "Dua Lipa - Future Nostalgia (Vinyl)",
            "Kendrick Lamar - To Pimp a Butterfly (CD)",
            "Fleetwood Mac - Rumours (Vinyl)"
        ],
        "Makeup": [
            "Maybelline Fit Me Foundation",
            "L'Oréal Paris Voluminous Mascara",
            "NYX Professional Makeup Butter Gloss",
            "Revlon ColorStay Lipstick",
            "e.l.f. Cosmetics 16HR Camo Concealer",
            "Fenty Beauty Pro Filt'r Foundation",
            "MAC Cosmetics Ruby Woo Lipstick",
            "NARS Orgasm Blush",
            "Urban Decay Naked Eyeshadow Palette",
            "Anastasia Beverly Hills Brow Wiz"
        ],
        "Skincare": [
            "CeraVe Hydrating Facial Cleanser",
            "La Roche-Posay Toleriane Double Repair Face Moisturizer",
            "Neutrogena Hydro Boost Water Gel",
            "The Ordinary Hyaluronic Acid 2% + B5",
            "Paula's Choice 2% BHA Liquid Exfoliant",
            "Cetaphil Daily Facial Moisturizer SPF 15",
            "Sun Bum Original SPF 30 Sunscreen",
            "Differin Adapalene Gel 0.1% Acne Treatment",
            "Kiehl's Midnight Recovery Concentrate",
            "Clinique Moisture Surge 100H Auto-Replenishing Hydrator"
        ],
        "Haircare": [
            "Pantene Pro-V Daily Moisture Renewal Shampoo",
            "Dove Daily Moisture Conditioner",
            "OGX Argan Oil of Morocco Shampoo",
            "SheaMoisture Coconut & Hibiscus Curl & Shine Shampoo",
            "Tresemmé Keratin Smooth Heat Protect Spray",
            "Garnier Fructis Sleek & Shine Anti-Frizz Serum",
            "Living Proof Perfect hair Day Dry Shampoo",
            "Moroccanoil Treatment Original",
            "Redken All Soft Mega Mask",
            "Olaplex No. 3 Hair Perfector"
        ],
        "Fragrances": [
            "Chanel No. 5 Eau de Parfum",
            "Dior Sauvage Eau de Toilette",
            "Yves Saint Laurent Black Opium Eau de Parfum",
            "Tom Ford Black Orchid Eau de Parfum",
            "Giorgio Armani Acqua di Gio Eau de Toilette",
            "Lancôme La Vie Est Belle Eau de Parfum",
            "Gucci Bloom Eau de Parfum",
            "Versace Eros Eau de Toilette",
            "Creed Aventus Eau de Parfum",
            "Jo Malone London Lime Basil & Mandarin Cologne"
        ],
        "Fitness Equipment": [
            "Peloton Bike+",
            "NordicTrack Commercial 1750 Treadmill",
            "Bowflex SelectTech 552 Adjustable Dumbbells",
            "TRX PRO4 Suspension Trainer System",
            "Yoga Direct Deluxe Yoga Mat",
            "BalanceFrom GoYoga All-Purpose Exercise Yoga Mat",
            "Resistance Bands Set - Letsfit",
            "Fitbit Charge 5 Fitness Tracker",
            "Apple Fitness+ Subscription",
            "Nike Training Club Premium Subscription"
        ],
        "Sports Apparel": [
            "Nike Pro Dri-FIT Training Tights",
            "Adidas Own The Run Running Shorts",
            "Under Armour HeatGear Compression Shirt",
            "Lululemon ABC Jogger",
            "Athleta Salutation Stash Pocket II Tight",
            "Nike Metcon 8 Training Shoes",
            "Adidas Ultraboost Running Shoes",
            "New Balance Fresh Foam 880 Running Shoes",
            "Saucony Kinvara 14 Running Shoes",
            "ASICS GEL-Kayano 29 Running Shoes"
        ],
        "Camping & Hiking": [
            "Coleman Sundome 4-Person Tent",
            "REI Co-op Half Dome 2+ Tent",
            "Kelty Cosmic 20 Sleeping Bag",
            "Therm-a-Rest NeoAir XLite Sleeping Pad",
            "Osprey Atmos AG 65 Backpack",
            "Deuter Aircontact Lite 65+10 Backpack",
            "Black Diamond Trail Ergo Cork Trekking Poles",
            "MSR PocketRocket 2 Stove",
            "CamelBak Eddy+ Water Bottle",
            "LifeStraw Personal Water Filter"
        ],
        "Cycling": [
            "Specialized Sirrus X 4.0 Hybrid Bike",
            "Trek Domane AL 5 Road Bike",
            "Cannondale Topstone 4 Gravel Bike",
            "Giant Talon 2 Mountain Bike",
            "Schwinn High Timber Mountain Bike",
            "Garmin Edge 530 Cycling Computer",
            "Wahoo ELEMNT Bolt V2 GPS Bike Computer",
            "Shimano 105 R7000 Groupset",
            "SRAM Rival eTap AXS Groupset",
            "Continental Grand Prix 5000 Tires"
        ],
        "Fashion Accessories": [
            "Michael Kors Jet Set Travel Large Crossbody Bag",
            "Coach Outlet Signature Jacquard Crossbody",
            "Kate Spade New York Cameron Street Hilli Crossbody",
            "Fossil Buckner Backpack",
            "Samsonite Omni PC Hardside Luggage",
            "Herschel Trade Carry-On Luggage",
            "Daniel Wellington Classic Sheffield Watch",
            "MVMT Voyager Watch",
            "Fjallraven Greenland Beanie",
            "Carhartt Knit Cuffed Beanie"
        ],
        "Toys & Games": [
            "LEGO Classic Creative Brick Box",
            "Play-Doh Fun Factory",
            "Barbie Dreamhouse",
            "Hot Wheels Track Builder Unlimited Rapid Ramp Builder Box",
            "Monopoly Classic Board Game",
            "Scrabble Deluxe Edition Board Game",
            "Nintendo Switch OLED Model",
            "PlayStation 5 Console",
            "Xbox Series X Console",
            "Melissa & Doug Wooden Puzzles Set"
        ]
    }

    # 3. Define Price Ranges (Example - adjust as needed) - Adjusted ranges to be more in line with realistic product prices
    price_ranges = {
        "Smartphones": (150, 1800),  # Wider range to include budget to premium
        "Laptops": (250, 3500),  # Wider range to include budget to high-end
        "Headphones": (15, 600),  # Wider range
        "Smartwatches": (40, 900),  # Wider range
        "Men's Clothing": (10, 300),  # Wider range
        "Women's Clothing": (10, 400),  # Wider range
        "Shoes": (25, 400),  # Wider range
        "Accessories": (5, 250),  # Wider range
        "Furniture": (40, 3000),  # Wider range
        "Home Decor": (8, 600),  # Wider range
        "Kitchen & Dining": (8, 400),  # Wider range
        "Bedding & Bath": (15, 500),  # Wider range
        "Books": (4, 60),  # Wider range
        "E-books": (1, 40),  # Wider range
        "Movies": (8, 40),  # Wider range
        "Music": (4, 30),  # Wider range
        "Makeup": (8, 200),  # Wider range
        "Skincare": (10, 250),  # Wider range
        "Haircare": (6, 100),  # Wider range
        "Fragrances": (20, 400),  # Wider range
        "Fitness Equipment": (40, 2500),  # Wider range
        "Sports Apparel": (10, 200),  # Wider range
        "Camping & Hiking": (15, 600),  # Wider range
        "Cycling": (40, 3000),  # Wider range
        "Jewelry": (25, 5000),  # Wider range - Higher for Jewelry
        "Watches": (40, 10000),  # Wider, especially for watches
        "Bags & Luggage": (15, 500),  # Wider range
        "Sunglasses": (15, 300),  # Wider range
        "Educational Toys": (8, 120),  # Wider range
        "Action Figures": (6, 60),  # Wider range
        "Board Games": (10, 100),  # Wider range
        "Puzzles": (4, 50)   # Wider range
    }

    # 4. Define Lists for other categorical columns
    payment_methods = ["Credit Card", "PayPal", "Debit Card", "Online Banking"]
    shipping_states = ["California", "Texas", "New York", "Florida", "Illinois", "Pennsylvania"]
    order_statuses = ["Placed", "Processing", "Shipped", "Delivered", "Cancelled", "Returned"]

    return (categories, product_names, price_ranges, payment_methods,
            shipping_states, order_statuses)


def generate_single_order(order_id, customer_id, date_range, product_names,
                          price_ranges, payment_methods, shipping_states,
                          order_statuses, categories):
    """
    Generates data for a single synthetic e-commerce order.

    Args:
        order_id (int): Unique identifier for the order.
        customer_id (int): Identifier for the customer placing the order.
        date_range (pd.DatetimeIndex): Range of dates for order dates.
        product_names (dict): Dictionary of product names by subcategory.
        price_ranges (dict): Dictionary of price ranges by subcategory.
        payment_methods (list): List of possible payment methods.
        shipping_states (list): List of possible shipping states.
        order_statuses (list): List of possible order statuses.
        categories (dict): Dictionary of categories and subcategories.

    Returns:
        dict: A dictionary containing the data for a single order.
    """
    order_date = random.choice(date_range)

    # Corrected: Choose a subcategory directly from the keys of product_names
    chosen_subcategory_group = random.choice(list(product_names.keys()))

    # Determine category based on subcategory_group
    chosen_category = "Unknown Category"  # Default
    for cat, subcats in categories.items():
        if chosen_subcategory_group in subcats:
            chosen_category = cat
            break  # Found the category, no need to continue checking

    # Randomly choose a product name from the chosen subcategory group
    chosen_product_name = random.choice(product_names[chosen_subcategory_group])
    # Get price range for the subcategory group
    min_price, max_price = price_ranges.get(chosen_subcategory_group, (10, 100))  # Default price range if not found
    product_price = round(random.uniform(min_price, max_price), 2)  # Random price within range, rounded to 2 decimals
    quantity = random.randint(1, 5)  # Random quantity, up to 5 items

    payment_method = random.choice(payment_methods)
    shipping_state = random.choice(shipping_states)
    order_status = random.choice(order_statuses)

    order_data = {
        'order_id': order_id,
        'customer_id': customer_id,
        'order_date': order_date,
        'product_name': chosen_product_name,
        'product_category': chosen_category,
        'product_subcategory': chosen_subcategory_group,
        'quantity_ordered': quantity,
        'product_price': product_price,
        'payment_method': payment_method,
        'shipping_state': shipping_state,
        'order_status': order_status
    }
    return order_data


def create_sales_dataframe(order_data_list):
    """
    Creates a Pandas DataFrame from a list of order data dictionaries.

    Args:
        order_data_list (list): A list of dictionaries, where each dictionary
                                represents an order's data.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the sales data.
    """
    df_sales = pd.DataFrame(order_data_list)
    return df_sales


def load_data_to_duckdb(df_sales, persistent_db_path):
    """
    Loads the sales DataFrame into both in-memory and persistent DuckDB databases.

    Verifies that the data is loaded correctly by comparing row counts.

    Args:
        df_sales (pd.DataFrame): The sales data DataFrame to load.
        persistent_db_path (str): Path to the persistent DuckDB database file.
    """
    # Persistent database connection
    con_persistent = duckdb.connect(database=persistent_db_path, read_only=False)
    con_persistent.register('sales_df', df_sales)
    con_persistent.execute("CREATE OR REPLACE TABLE sales_table AS SELECT * FROM sales_df")

    # In-memory database connection (for primary work)
    con_memory = duckdb.connect(database=':memory:', read_only=False)
    con_memory.register('sales_df', df_sales)
    con_memory.execute("CREATE OR REPLACE TABLE sales_table AS SELECT * FROM sales_df")

    # Verify data in both databases
    duckdb_row_count_persistent = con_persistent.execute("SELECT COUNT(*) FROM sales_table").fetchone()[0]
    duckdb_row_count_memory = con_memory.execute("SELECT COUNT(*) FROM sales_table").fetchone()[0]
    pandas_row_count = len(df_sales)

    if duckdb_row_count_persistent == pandas_row_count and duckdb_row_count_memory == pandas_row_count:
        print(f"Successfully loaded {duckdb_row_count_persistent} rows into persistent DuckDB table 'sales_table' at {persistent_db_path}.")
        print(f"Successfully loaded {duckdb_row_count_memory} rows into in-memory DuckDB table 'sales_table'.")
    else:
        print(f"Warning: Row counts don't match across databases. Persistent: {duckdb_row_count_persistent}, In-Memory: {duckdb_row_count_memory}, Pandas: {pandas_row_count}")

    con_persistent.close()  # Close the persistent connection. The file will remain.
    # con_memory.close() # Keep the in-memory connection open for further queries

    print("Data loaded into both persistent and in-memory DuckDB instances.")


def run_example_queries(df_sales):
    """
    Executes and prints results of example DuckDB queries on sales data.

    Args:
        df_sales (pd.DataFrame): The sales data DataFrame to query.
    """
    con = duckdb.connect(database=':memory:', read_only=False)  # Reconnect if needed
    con.register('sales_df', df_sales)
    con.execute("CREATE TABLE sales_table AS SELECT * FROM sales_df")

    # Example queries
    avg_price = con.execute("SELECT AVG(product_price) FROM sales_table").fetchone()[0]
    print(f"\nAverage product price: {avg_price}")

    top_categories = con.execute(
        "SELECT product_category, SUM(quantity_ordered) AS total_quantity "
        "FROM sales_table GROUP BY product_category ORDER BY total_quantity DESC LIMIT 5"
    ).fetchall()
    print("\nTop 5 product categories by quantity ordered:")
    for category, quantity in top_categories:
        print(f"- {category}: {quantity}")

    con.close()


def main():
    """
    Main function to generate synthetic sales data, load it to DuckDB, and run queries.
    """
    # Get data definitions
    (categories, product_names, price_ranges, payment_methods,
     shipping_states, order_statuses) = create_data_definitions()

    # 5. Define Date Range for Orders (e.g., last year)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    date_range = pd.date_range(start_date, end_date, freq='D')  # Daily frequency

    # 6. Number of Orders to Generate
    num_orders = 10000  # Example - you can adjust this

    # 7. Initialize List to store order data
    order_data_list = []

    # 8. Data Generation Loop
    for i in range(num_orders):
        order_id = i + 1  # Simple order ID
        customer_id = random.randint(1, 500)  # Example: 500 unique customers (adjust as needed)
        order_data = generate_single_order(
            order_id, customer_id, date_range, product_names,
            price_ranges, payment_methods, shipping_states,
            order_statuses, categories
        )
        order_data_list.append(order_data)

    # 9. Create Pandas DataFrame
    df_sales = create_sales_dataframe(order_data_list)

    # 10. Save to CSV
    df_sales.to_csv("synthetic_ecommerce_sales_data.csv", index=False)
    print("Synthetic dataset generated and saved to synthetic_ecommerce_sales_data.csv")

    # 11. Load DataFrame into DuckDB (In-Memory and Persistent File)
    # Get the parent directory and create the database in 30-database/
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    database_dir = os.path.join(parent_dir, "30-database")

    # Create the database directory if it doesn't exist
    os.makedirs(database_dir, exist_ok=True)

    persistent_db_path = os.path.join(database_dir, "my_ecommerce_db.duckdb")
    load_data_to_duckdb(df_sales, persistent_db_path)

    # 12. (Optional) Run Example DuckDB queries
    run_example_queries(df_sales)


if __name__ == "__main__":
    main()
