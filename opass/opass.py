#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# ORGANIC PASSWORD GENERATOR

import argparse
import sys
from datetime import datetime
import hashlib
import io

# Fix encoding for Windows terminals
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# --- EVENT DATA & SYMBOLS ---
SYMBOLS = {
    "holidays": "!",
    "seasons": "#",
    "culture": "$",
    "history": "%",
    "personal": "&",
    "tech": "@"
}

def calculate_easter(year):
    """Computes the date of Easter for a given year (Gauss algorithm)."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return f"{day:02d}{month:02d}"

EVENTS_DATA = {
    "holidays": {
        "Christmas": lambda y: "2512",
        "New Year's Day": lambda y: "0101",
        "Easter": calculate_easter,
        "Valentine's Day": lambda y: "1402",
        "Halloween": lambda y: "3110",
        "Independence Day (USA)": lambda y: "0407",
        "New Year's Eve": lambda y: "3112",
        "Labor Day (May)": lambda y: "0105",
        "Epiphany": lambda y: "0601"
    },
    "seasons": {
        "Summer Solstice": lambda y: "2106",
        "Winter Solstice": lambda y: "2112",
        "Spring Equinox": lambda y: "2003",
        "Autumn Equinox": lambda y: "2309"
    },
    "culture": {
        "Pi Day": lambda y: "1403",
        "Star Wars Day": lambda y: "0405",
        "World Book Day": lambda y: "2304",
        "Earth Day": lambda y: "2204",
        "World Music Day": lambda y: "2106",
        "Programmer's Day": lambda y: "1309",
        "Talk Like a Pirate Day": lambda y: "1909",
        "Fibonacci Day": lambda y: "2311",
        "Palindrome Day": lambda y: "1002"
    },
    "history": {
        "Moon Landing (Apollo 11)": lambda y: "2007",
        "Fall of Berlin Wall": lambda y: "0911",
        "First Internet Message": lambda y: "2910",
        "Bitcoin Genesis Block": lambda y: "0301",
        "First Flight (Wright)": lambda y: "1712",
        "Gutenberg Bible": lambda y: "2302",
        "Declaration Independence": lambda y: "0407",
        "World Wide Web": lambda y: "1208"
    },
    "personal": {
        "Custom Date 1": lambda y: "0101",
        "Custom Date 2": lambda y: "1501",
        "Custom Date 3": lambda y: "0802",
        "Custom Date 4": lambda y: "2503",
        "Custom Date 5": lambda y: "1506"
    },
    "tech": {
        "Unix Epoch": lambda y: "0101",
        "Y2K": lambda y: "0101",
        "iPhone Release": lambda y: "2906",
        "Windows 95": lambda y: "2408",
        "Linux Birthday": lambda y: "2508",
        "Python Release": lambda y: "2002",
        "Git Initial Release": lambda y: "0704"
    }
}

# --- REFACTORED TRANSFORMATION FUNCTIONS ---

def _transform_reverse(keyword):
    return keyword[::-1]

def _transform_caps(keyword):
    return keyword.upper()

def _transform_leet(keyword):
    # Apply leet only after capitalizing the first letter of the original word
    transformed = keyword.capitalize()
    leet_map = str.maketrans("aeioAEIO", "@310@310")
    return transformed.translate(leet_map)

def _transform_alnum(keyword):
    result = []
    for char in keyword.lower():
        if 'a' <= char <= 'z':
            result.append(str(ord(char) - ord('a') + 1))
        elif '0' <= char <= '9':
            result.append(char)
    return "".join(result)

def _transform_alternate(keyword):
    result = []
    for i, char in enumerate(keyword):
        if i % 2 == 0:
            result.append(char.upper())
        else:
            result.append(char.lower())
    return "".join(result)

def _transform_vowelcaps(keyword):
    vowels = "aeiouAEIOU"
    result = []
    for char in keyword:
        if char in vowels:
            result.append(char.upper())
        else:
            result.append(char.lower())
    return "".join(result)

TRANSFORMATION_FUNCS = {
    "reverse": _transform_reverse,
    "caps": _transform_caps,
    "leet": _transform_leet,
    "alnum": _transform_alnum,
    "alternate": _transform_alternate,
    "vowelcaps": _transform_vowelcaps
}

def apply_transformations(keyword, styles):
    """Applies a sequence of transformations to the keyword."""
    if not keyword:
        return ""
    
    temp_keyword = keyword
    for style in styles:
        if style in TRANSFORMATION_FUNCS:
            # Special handling for leet to always capitalize the *original* word's first letter
            if style == 'leet':
                temp_keyword = TRANSFORMATION_FUNCS[style](keyword)
            else:
                 temp_keyword = TRANSFORMATION_FUNCS[style](temp_keyword)
    return temp_keyword


def generate_password(category, event_name, keyword, year, structure, transformations):
    """Generates the password based on user inputs."""
    transformed_keyword = apply_transformations(keyword, transformations)
    symbol = SYMBOLS[category]
    event_date = EVENTS_DATA[category][event_name](year)
    
    components = {'k': transformed_keyword, 's': symbol, 'd': event_date}
    password_parts = [components[part] for part in structure.split('_')]
    
    return {
        "password": "".join(password_parts),
        "transformed_keyword": transformed_keyword,
        "symbol": symbol,
        "date": event_date
    }

# --- HELP FUNCTIONS ---

def list_events():
    """Display all available events organized by category."""
    print("\n" + "="*70)
    print("📋 AVAILABLE EVENTS BY CATEGORY")
    print("="*70)
    
    for category, events in EVENTS_DATA.items():
        symbol = SYMBOLS[category]
        print(f"\n🔹 {category.upper()} [{symbol}]:")
        for event_name in events.keys():
            print(f"   • {event_name}")
    
    print("\n" + "="*70 + "\n")

def print_examples():
    """Display usage examples."""
    print("\n" + "="*70)
    print("📚 USAGE EXAMPLES")
    print("="*70)
    print("\n1. Basic password with default leet transformation:")
    print("   python opass.py holidays Christmas secret")
    print("\n2. Use multiple transformations (applied in order):")
    print("   python opass.py culture 'Pi Day' myword -t reverse -t caps")
    print("\n3. Custom year and structure:")
    print("   python opass.py history 'Moon Landing (Apollo 11)' apollo -y 1969 -s d_s_k")
    print("\n4. Chain transformations:")
    print("   python opass.py tech 'iPhone Release' apple -t leet -t reverse")
    print("\n5. Alphanumeric conversion:")
    print("   python opass.py personal 'Custom Date 1' birthday -t alnum")
    print("\n6. Alternating case transformation:")
    print("   python opass.py seasons 'Spring Equinox' flower -t alternate -s k_d_s")
    print("\n7. Vowel capitalization:")
    print("   python opass.py tech 'Python Release' coding -t vowelcaps")
    print("\n8. Complex transformation chain:")
    print("   python opass.py history 'Bitcoin Genesis Block' satoshi -t caps -t reverse -s s_d_k")
    print("\n9. List all available events:")
    print("   python opass.py --list")
    print("\n10. Show this help:")
    print("   python opass.py --examples")
    print("\n" + "="*70 + "\n")

# --- COMMAND-LINE INTERFACE ---

def main():
    parser = argparse.ArgumentParser(
        description="""
🌿 ORGANIC PASSWORD GENERATOR
==============================

Generate memorable, secure passwords using meaningful events and personal keywords.
Combine different transformations to create unique password patterns.

Categories & Symbols:
  holidays (!)  - Holiday dates
  seasons (#)   - Seasonal events
  culture ($)   - Cultural milestones
  history (%)   - Historical events
  personal (&)  - Personal dates
  tech (@)      - Technology milestones

Transformations:
  leet      - Converts vowels to numbers (a→@, e→3, i→1, o→0)
  reverse   - Reverses the keyword
  caps      - Converts to uppercase
  alnum     - Converts letters to numbers (a=1, b=2, etc.)
  alternate - Alternates uppercase/lowercase (aBaBaB)
  vowelcaps - Capitalizes only vowels

Structure Options:
  k_s_d - Keyword-Symbol-Date (default)
  d_s_k - Date-Symbol-Keyword
  s_k_d - Symbol-Keyword-Date
  k_d_s - Keyword-Date-Symbol
  d_k_s - Date-Keyword-Symbol
  s_d_k - Symbol-Date-Keyword
        """,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Use --list to see all available events, or --examples for usage examples."
    )
    
    parser.add_argument("category", nargs='?', help="Event category (holidays, seasons, culture, history, personal, tech)", 
                       choices=list(EVENTS_DATA.keys()))
    parser.add_argument("event", nargs='?', help="The specific event name")
    parser.add_argument("keyword", nargs='?', help="Your personal keyword")
    parser.add_argument("-y", "--year", type=int, default=datetime.now().year, 
                       help="Reference year (default: current year)")
    parser.add_argument("-s", "--structure", default="k_s_d", 
                       choices=["k_s_d", "d_s_k", "s_k_d", "k_d_s", "d_k_s", "s_d_k"], 
                       help="Password structure (default: k_s_d)")
    parser.add_argument("-t", "--transformation", action='append', 
                       choices=["leet", "reverse", "caps", "alnum", "alternate", "vowelcaps"],
                       help="Add transformations (can be used multiple times). Applied in order.\n"
                            "Default: leet if none specified")
    parser.add_argument("--list", action='store_true', help="List all available events")
    parser.add_argument("--examples", action='store_true', help="Show usage examples")

    args = parser.parse_args()

    # Handle special flags
    if args.list:
        list_events()
        sys.exit(0)
    
    if args.examples:
        print_examples()
        sys.exit(0)
    
    # Validate required arguments
    if not args.category or not args.event or not args.keyword:
        parser.print_help()
        print("\n❌ Error: category, event, and keyword are required when generating a password.")
        print("   Use --list to see available events or --examples for usage examples.\n")
        sys.exit(1)

    # If no transformation is specified, default to 'leet'
    if not args.transformation:
        args.transformation = ['leet']
    
    if args.event not in EVENTS_DATA[args.category]:
        print(f"\n❌ Error: Invalid event '{args.event}' for category '{args.category}'.")
        print(f"   Use --list to see all available events.\n")
        sys.exit(1)

    # Generate password and related details
    result = generate_password(
        args.category, args.event, args.keyword, args.year, args.structure, args.transformation
    )
    password = result["password"]
    
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    hex_dig = hash_object.hexdigest()
    
    transformation_map = {
        "leet": "leet speak", 
        "reverse": "reversal", 
        "caps": "uppercase", 
        "alnum": "alphanumeric conversion",
        "alternate": "alternating case",
        "vowelcaps": "vowel capitalization"
    }
    structure_map = {
        "k_s_d": "Word-Symbol-Date", 
        "d_s_k": "Date-Symbol-Word", 
        "s_k_d": "Symbol-Word-Date",
        "k_d_s": "Word-Date-Symbol",
        "d_k_s": "Date-Word-Symbol",
        "s_d_k": "Symbol-Date-Word"
    }
    
    # Create a descriptive string for the transformation chain
    trans_chain_desc = " then ".join([transformation_map.get(t, t) for t in args.transformation])

    print("\n" + "="*50)
    print("🌿 Your Organic Password (clear text):")
    print(f"   {password}")
    
    print("\n🧠 How to Remember This:")
    print(f"   1. The event '{args.event}' for year {args.year}, which corresponds to the date '{result['date']}'.")
    print(f"   2. Your keyword '{args.keyword}', transformed with '{trans_chain_desc}' becomes '{result['transformed_keyword']}'.")
    print(f"   3. The symbol '{result['symbol']}' associated with the category '{args.category}'.")
    print(f"   4. All combined using the structure '{structure_map.get(args.structure)}'.")
    
    print("\n🔒 Hashed Password (SHA-256):")
    print(f"   {hex_dig}")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()