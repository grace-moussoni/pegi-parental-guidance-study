import re
import csv
import pandas as pd
from datetime import datetime

INPUT_TXT = "data/raw/PEGI.txt"
OUTPUT_CSV = "data/processed/pegi_games_dataset_v2.csv"

COLUMNS = [
    "game_id", "title", "pegi_id", "pegi_url", "pegi_rating_code", "pegi_rating_label",
    "descriptor_violence", "descriptor_bad_language", "descriptor_fear", "descriptor_sex",
    "descriptor_drugs", "descriptor_discrimination", "descriptor_gambling",
    "consumer_advice", "game_summary", "specific_concerns", "other_notes",
    "platforms", "genres", "publisher", "developer", "release_date",
    "monetisation", "online_play", "date_verified", "verified_by",
    "data_source", "dataset_version"
]

def slugify(text):
    return re.sub(r'[^a-zA-Z0-9]+', '-', text.lower()).strip('-')

def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return date_str.strip()

def parse_pegi_txt(input_path=INPUT_TXT, output_path=OUTPUT_CSV):
    with open(input_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Remove page markers [PAGE1 : ... ];
    clean_text = re.sub(r'\[PAGE\d+\s*:\s*', '', raw_text)
    clean_text = re.sub(r'\];\s*', '\n', clean_text)
    clean_text = re.sub(r'\]\s*$', '', clean_text)

    blocks = [b.strip() for b in re.split(r'(?=^age rating \d+)', clean_text.strip(), flags=re.MULTILINE) if b.strip()]
    rows = []

    for idx, block in enumerate(blocks, start=1):
        lines = [l.strip() for l in block.splitlines()]
        m_rating = re.match(r'^age rating (\d+)', lines[0])
        rating_code = int(m_rating.group(1)) if m_rating else None
        rating_label = f"PEGI {rating_code}" if rating_code else ""

        title = lines[1] if len(lines) > 1 else ""
        publisher = lines[2] if len(lines) > 2 else ""

        rel_idx = next((i for i, l in enumerate(lines) if l.startswith(("Release Dates & Platforms:", "Pre-release dates:"))), None)
        raw_tags = [l for l in lines[3:rel_idx] if l] if (rel_idx and rel_idx > 3) else []
        tags_lower = " | ".join(raw_tags).lower()

        desc_violence = 1 if "violence" in tags_lower else 0
        desc_bad_lang = 1 if ("swearing" in tags_lower or "language" in tags_lower) else 0
        desc_fear = 1 if ("horror" in tags_lower or "fear" in tags_lower) else 0
        desc_sex = 1 if "sex" in tags_lower else 0
        desc_drugs = 1 if "drugs" in tags_lower else 0
        desc_discrim = 1 if "discrimination" in tags_lower else 0
        desc_gambling = 1 if ("gambling" in tags_lower or "paid random items" in tags_lower) else 0

        monetisation_list = []
        if "in-game purchases" in tags_lower:
            monetisation_list.append("In-game purchases")
        if "paid random items" in tags_lower:
            monetisation_list.append("Loot boxes / Paid random items")
        monetisation = " ; ".join(monetisation_list) if monetisation_list else "None / Unknown"

        section_headers = [
            "Advice for consumers",
            "Brief outline of the game",
            "Content specific issues",
            "Other issues"
        ]
        sec_indices = {l: i for i, l in enumerate(lines) if l in section_headers}
        first_sec = min(sec_indices.values()) if sec_indices else len(lines)
        plat_lines = [l for l in lines[rel_idx + 1:first_sec] if l] if rel_idx is not None else []

        platforms, dates = [], []
        for pl in plat_lines:
            if " - " in pl:
                p_name, p_date = pl.rsplit(" - ", 1)
                platforms.append(p_name.strip())
                dates.append(parse_date(p_date))
            else:
                platforms.append(pl.strip())

        def get_section_text(header):
            if header not in sec_indices:
                return ""
            start = sec_indices[header] + 1
            next_starts = [v for v in sec_indices.values() if v > sec_indices[header]]
            end = min(next_starts) if next_starts else len(lines)
            return " ".join([l for l in lines[start:end] if l]).strip()

        consumer_advice = get_section_text("Advice for consumers")
        game_summary = get_section_text("Brief outline of the game")
        specific_concerns = get_section_text("Content specific issues")
        other_notes = get_section_text("Other issues")

        full_text_lower = f"{game_summary} {specific_concerns} {other_notes}".lower()
        if any(k in full_text_lower for k in ["online multiplayer", "online co-op", "mmorpg", "mmoprg"]):
            online_play = "Yes"
        elif "single-player" in full_text_lower and "multiplayer" not in full_text_lower:
            online_play = "No"
        else:
            online_play = "Unknown"

        rows.append({
            "game_id": f"GAME_{idx:04d}",
            "title": title,
            "pegi_id": slugify(title),
            "pegi_url": f"https://pegi.info/search-pegi?q={title.replace(' ', '+')}",
            "pegi_rating_code": rating_code,
            "pegi_rating_label": rating_label,
            "descriptor_violence": desc_violence,
            "descriptor_bad_language": desc_bad_lang,
            "descriptor_fear": desc_fear,
            "descriptor_sex": desc_sex,
            "descriptor_drugs": desc_drugs,
            "descriptor_discrimination": desc_discrim,
            "descriptor_gambling": desc_gambling,
            "consumer_advice": consumer_advice,
            "game_summary": game_summary,
            "specific_concerns": specific_concerns,
            "other_notes": other_notes,
            "platforms": " ; ".join(dict.fromkeys(platforms)),
            "genres": "Unknown",
            "publisher": publisher,
            "developer": "Unknown",
            "release_date": sorted(dates)[0] if dates else "",
            "monetisation": monetisation,
            "online_play": online_play,
            "date_verified": datetime.today().strftime("%Y-%m-%d"),
            "verified_by": "AUTO_PARSER",
            "data_source": "PEGI Official Search",
            "dataset_version": "v1.0.0"
        })

    df = pd.DataFrame(rows, columns=COLUMNS)
    df.to_csv(output_path, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_ALL)
    print(f"Successfully parsed {len(df)} games into {output_path}")

if __name__ == "__main__":
    parse_pegi_txt()