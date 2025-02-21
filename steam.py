import requests
from bs4 import BeautifulSoup

def scrape_steam(minimum_discount=80):
    url = "https://store.steampowered.com/search/?specials=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve the Steam page.")
        return []
    
    soup = BeautifulSoup(response.text, "lxml")
    # Each deal is within an <a> tag with class "search_result_row"
    game_elements = soup.find_all("a", class_="search_result_row")
    
    deals = []
    for game in game_elements:
        # Extract the game title
        title_elem = game.find("span", class_="title")
        title = title_elem.text.strip() if title_elem else "Unknown Title"

        # Extract the discount percentage from the discount_pct element
        discount_elem = game.find("div", class_="discount_pct")
        discount_text = discount_elem.text.strip() if discount_elem else ""
        discount_value = 0
        if discount_text.startswith("-"):
            try:
                discount_value = int(discount_text.strip("-%"))
            except ValueError:
                discount_value = 0
        
        # Extract the final price from the discount_final_price element
        final_price_elem = game.find("div", class_="discount_final_price")
        price_text = final_price_elem.text.strip() if final_price_elem else ""

        # Determine if the game is free (in case price_text is empty or mentions "Free")
        is_free = "Free" in price_text or not price_text

        # Filter: include free games or games with a discount of 80% or more
        if is_free or discount_value >= minimum_discount:
            deals.append({
                "title": title,
                "discount": discount_text,
                "price": price_text
            })
    
    return deals

if __name__ == "__main__":
    minimum_discount = int(input("Enter the minimum discount percentage (default is 80): ") or 80)
    steam_deals = scrape_steam(minimum_discount)
    print(f"### Steam Deals with Free/{minimum_discount}%+ Discounts:\n")
    for deal in steam_deals:
        print(f"Title: {deal['title']} | Discount: {deal['discount']} | Price: {deal['price']}")