"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.
    """
    import re

    def words(text):
        return set(re.findall(r"[a-z0-9]+", str(text).lower()))

    search_terms = words(description)
    results = []

    for listing in load_listings():
        if max_price is not None and listing["price"] > max_price:
            continue
        if size and size.lower() not in listing["size"].lower():
            continue

        haystack = words(listing["title"]) | words(listing["description"]) | words(" ".join(listing["style_tags"]))
        score = len(search_terms & haystack)

        if score > 0:
            results.append((score, listing))

    results.sort(key=lambda pair: pair[0], reverse=True)
    return [listing for score, listing in results[:config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    items = wardrobe.get("items", [])

    if not items:
        prompt = (
            f"Someone is considering buying this thrifted item: {new_item['title']}. "
            f"It's a {new_item['category']}, colors: {', '.join(new_item['colors'])}, "
            f"style: {', '.join(new_item['style_tags'])}.\n\n"
            "They haven't told you what else they own. Suggest two general outfit "
            "ideas for how to style this piece. Keep it to 3-4 sentences."
        )
    else:
        owned = "\n".join(f"- {it['name']}" for it in items)
        prompt = (
            f"Someone is considering buying this thrifted item: {new_item['title']}. "
            f"It's a {new_item['category']}, colors: {', '.join(new_item['colors'])}, "
            f"style: {', '.join(new_item['style_tags'])}.\n\n"
            f"Here's what they already own:\n{owned}\n\n"
            "Suggest 1-2 outfits that pair the new item with things they already own. "
            "Name the specific pieces from their wardrobe. Keep it to 3-4 sentences."
        )

    return generate(prompt)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    if not outfit or not outfit.strip():
        return "Can't make a fit card — no outfit suggestion to work from."

    prompt = (
        f"Write a short, casual social media caption (2-4 sentences) for someone "
        f"posting about a thrifted find. The item: {new_item['title']}, "
        f"${new_item['price']} on {new_item['platform']}. "
        f"How they're styling it: {outfit}\n\n"
        "Write it like a real caption a person would post — not a product "
        "description. Mention the price and platform once each. Capture the vibe."
    )

    return generate(prompt)
