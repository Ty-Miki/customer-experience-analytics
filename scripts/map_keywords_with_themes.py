def map_keywords_to_themes(keywords: list, theme_map: dict) -> list:
    themes = set()
    for kw in keywords:
        for key, theme in theme_map.items():
            if key in kw:
                themes.add(theme)
    return list(themes) if themes else ["Other"]
