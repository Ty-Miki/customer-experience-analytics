from collections import defaultdict

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def map_keywords_to_themes(keywords: list, theme_map: dict) -> list:
    themes = set()
    for kw in keywords:
        for key, theme in theme_map.items():
            if key in kw:
                themes.add(theme)
    logging.info(f"Mapped keywords to themes using the given theme_map")
    return list(themes) if themes else ["Other"]

def get_examples_by_theme(df, theme_col: str ='themes', text_col: str ='cleaned_review', max_examples=3):
    theme_examples = defaultdict(list)
    for _, row in df.iterrows():
        for theme in row[theme_col]:
            if len(theme_examples[theme]) < max_examples:
                theme_examples[theme].append(row[text_col])
    return theme_examples
