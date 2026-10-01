# FitFindr notes

## Listing fields
id, title, description, category, style_tags, size, condition,
price, colors, brand, platform

## Things to handle
- price is a float, and max_price is a simple <= check
- size is inconsistent: "W30 L30", "S/M", "XL (oversized)", "M", "W28", "L"
- brand can be null
- style_tags and colors are lists; title and description are free text

## Wardrobe shape
- {"items": [...]}; an empty wardrobe is {"items": []}
- item notes can be null

## Empty-search test query
python app.py ask 'designer ballgown size XXS under $5'