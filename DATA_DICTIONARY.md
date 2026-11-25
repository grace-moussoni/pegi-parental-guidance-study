# Data Dictionary — PEGI Video Game Classifications Dataset

This document describes the schema, data types, and encoding rules for `pegi_games_dataset_v2.csv` (`v1.0.0`). Each record corresponds to a video game or downloadable content (DLC) entry verified via the official PEGI public search database.

## Overview

- **File Format:** UTF-8 with BOM (`utf-8-sig`), comma-separated, all fields quoted (`QUOTE_ALL`).
- **Granularity:** One row per game/DLC title entry.
- **Total Columns:** 28

---

## Schema Reference

### 1. Identifiers & Traceability

| Column Name | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `game_id` | `string` | Unique sequential project identifier (`GAME_XXXX`). | `GAME_0001` |
| `title` | `string` | Official title of the game or DLC as listed on PEGI. | `Little Nightmares III - The Shores` |
| `pegi_id` | `string` | URL-friendly slug derived from the game title. | `little-nightmares-iii-the-shores` |
| `pegi_url` | `string` | Reference search URL on the official PEGI portal for auditability. | `https://pegi.info/search-pegi?q=Backrooms+Level+X` |

### 2. Age Rating Classification

| Column Name | Data Type | Description | Allowed Values / Example |
| :--- | :--- | :--- | :--- |
| `pegi_rating_code` | `integer` | Numeric PEGI minimum age classification (ordinal target variable). | `3`, `7`, `12`, `16`, `18` |
| `pegi_rating_label` | `string` | Human-readable PEGI age label. | `PEGI 3`, `PEGI 7`, `PEGI 12`, `PEGI 16`, `PEGI 18` |

### 3. Content Descriptors (Binary Indicators)

Each descriptor column is binary-encoded (`1` = descriptor present on the PEGI header/classification; `0` = descriptor absent).

| Column Name | Data Type | Description | Allowed Values |
| :--- | :--- | :--- | :--- |
| `descriptor_violence` | `integer` | Game contains depictions of violence (mild, moderate, strong, or extreme). | `0`, `1` |
| `descriptor_bad_language` | `integer` | Game contains mild swearing or strong profanity. | `0`, `1` |
| `descriptor_fear` | `integer` | Game contains scenes or imagery likely to frighten young children or induce horror/dread. | `0`, `1` |
| `descriptor_sex` | `integer` | Game depicts nudity, sexual behaviour, or sexual references. | `0`, `1` |
| `descriptor_drugs` | `integer` | Game refers to or depicts the use of illegal drugs, alcohol, or tobacco. | `0`, `1` |
| `descriptor_discrimination` | `integer` | Game contains depictions of, or material that may encourage, discrimination. | `0`, `1` |
| `descriptor_gambling` | `integer` | Game encourages or teaches gambling, or includes paid random items (loot boxes). | `0`, `1` |

### 4. Qualitative & Consumer Information Texts (NLP Fields)

| Column Name | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `consumer_advice` | `string` | Official PEGI *Advice for consumers* summary explaining the age rating. | `This game has received a PEGI 12 because it features moderate horror scenes...` |
| `game_summary` | `string` | Official PEGI *Brief outline of the game* describing core gameplay and premise. | `First-person survival horror game in which players are immersed...` |
| `specific_concerns` | `string` | Detailed breakdown under *Content specific issues* justifying the rating. | `This game contains moderate horror sequences and disturbing images...` |
| `other_notes` | `string` | Additional disclosures under *Other issues* (e.g., secondary themes, mild substance references, store links). | `All violence in the game is implied...` |

### 5. Game Metadata & Commercial Mechanics

| Column Name | Data Type | Description | Allowed Values / Example |
| :--- | :--- | :--- | :--- |
| `platforms` | `string` | Supported hardware platforms separated by ` ; `. | `PlayStation 5 ; Nintendo Switch 2` |
| `genres` | `string` | Primary game genre(s) separated by ` ; ` (`Unknown` if not explicitly listed on the PEGI card). | `Action ; RPG` or `Unknown` |
| `publisher` | `string` | Name of the publishing entity listed on PEGI. | `Bandai Namco Entertainment Europe` |
| `developer` | `string` | Name of the development studio (`Unknown` if omitted on the PEGI card). | `Unknown` |
| `release_date` | `string` | Earliest listed European release or pre-release date in ISO 8601 format (`YYYY-MM-DD`). | `2026-09-30` |
| `monetisation` | `string` | Disclosed monetisation mechanics separated by ` ; `. | `In-game purchases`, `Loot boxes / Paid random items`, `None / Unknown` |
| `online_play` | `string` | Indicator of online multiplayer or co-op functionality inferred from the PEGI description. | `Yes`, `No`, `Unknown` |

### 6. Provenance & Versioning Metadata

| Column Name | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `date_verified` | `string` | Date the record was extracted or manually audited (`YYYY-MM-DD`). | `2026-11-24` |
| `verified_by` | `string` | Identifier of the data collector or automated parser script. | `AUTO_PARSER` |
| `data_source` | `string` | Origin of the classification record. | `PEGI Official Search` |
| `dataset_version` | `string` | Semantic version tag of the dataset release. | `v1.0.0` |

---

## Notes on Data Quality & Limitations

- **Header Descriptors vs. Detailed Notes:** Secondary themes (such as brief references to alcohol, suicide, or suggestive outfits) may appear in `other_notes` without triggering a top-level `descriptor_*` icon, in accordance with PEGI rating thresholds.
- **Missing Metadata (`genres`, `developer`):** PEGI search cards do not consistently expose structured genre or developer fields; these default to `Unknown` unless enriched from external game databases.