# Does PEGI Really Protect Children?
**An Empirical Data Science & Parental Perception Study on Video Game Age Ratings, Content Descriptors, and Family Usage**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org/)
[![Data Version](https://img.shields.io/badge/Dataset-v1.0.0-success.svg)](DATA_DICTIONARY.md)

## Overview & Editorial Stance

This project investigates whether the **Pan European Game Information (PEGI)** classification system provides consistent, intelligible, and actionable guidance for parents. Rather than making causal claims about video game effects on child behavior, this study adopts a **data journalism and applied data science** approach to evaluate:

1. **Internal Consistency:** How well PEGI age ratings (`PEGI 3`, `7`, `12`, `16`, `18`) align with official content descriptors, detailed consumer advice texts, platforms, and monetisation mechanics (such as in-game purchases and loot boxes).
2. **Parental Comprehension & Adoption:** Whether parents understand what PEGI icons actually measure (content vs. game difficulty) and whether they use the system as a simple purchase filter or as an active supervision tool.

> **Core Thesis:** *PEGI is a useful framework, but its practical effectiveness depends less on the age badge itself than on the clarity of its descriptors, parental literacy, and real-world household usage.*

---

## Key Research Hypotheses

- **H1:** Games rated `PEGI 12`, `16`, and `18` exhibit statistically distinct content descriptor profiles.
- **H2:** Specific descriptors—particularly violence, fear/horror, bad language, and gambling/paid random items—strongly drive higher age tiers.
- **H3:** Rating distributions and disclosure nuances vary significantly across publishers, platforms, and monetisation models.
- **H4:** A substantial share of parents recognize the PEGI logo but misinterpret specific content icons or confuse age ratings with gameplay difficulty.
- **H5:** Parents rely on PEGI primarily at the point of purchase rather than as a conversational or parental-control framework.

---

## Repository Structure

```text
pegi-parental-guidance-study/
├── .gitignore                 # Excludes local data files, caches, and virtual environments
├── LICENSE                    # MIT License (code & documentation)
├── README.md                  # Project overview, methodology, and setup instructions
├── DATA_DICTIONARY.md         # Full 28-column schema documentation
├── requirements.txt           # Reproducible Python dependencies
├── data/                      # Local storage (ignored by Git; hosted externally)
│   ├── raw/                   # Raw PEGI search extracts (e.g., PEGI.txt)
│   ├── processed/             # Cleaned analytical CSV/Parquet datasets
│   └── survey/                # Anonymized parental survey responses
├── scripts/
│   ├── parse_pegi_txt.py      # Deterministic parser transforming raw PEGI cards to CSV
│   └── pegi_logger_v2.py      # Interactive CLI tool for manual PEGI record auditing
├── notebooks/
│   ├── 01_eda_pegi_ratings.ipynb
│   ├── 02_predictive_modeling.ipynb
│   └── 03_parent_survey_analysis.ipynb
└── outputs/
    └── figures/               # Publication-ready charts and SHAP visualisations
```

---

## Methodology & Pipeline

1. **Controlled Data Collection (`scripts/`):**
   - Game classifications, content descriptors, and detailed *Content Specific Issues* / *Other Issues* disclosures are audited directly from the official [PEGI Public Search](https://pegi.info/search-pegi).
   - Data is structured into a standardized 28-column schema documented in [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md).
2. **Exploratory Data Analysis (`01_eda_pegi_ratings.ipynb`):**
   - Distribution of age ratings, co-occurrence heatmaps of content descriptors, monetisation prevalence, and textual discrepancies between header icons and detailed consumer notes.
3. **Interpretable Predictive Modeling (`02_predictive_modeling.ipynb`):**
   - Comparison of **Ordinal Logistic Regression**, **Random Forest**, and **XGBoost / LightGBM** classifiers to predict PEGI age tiers from content and commercial features.
   - **SHAP (SHapley Additive exPlanations)** values are used to quantify feature contributions without inferring psychological causality.
4. **Parental Survey Analysis (`03_parent_survey_analysis.ipynb`):**
   - Anonymous, GDPR/ICO-compliant questionnaire targeting parents and legal guardians of children aged 6–14, cross-referenced with empirical dataset findings.

---

## Getting Started

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/grace-moussoni/pegi-parental-guidance-study.git
cd pegi-parental-guidance-study

python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Data Access & Parsing

To keep the Git history lightweight, raw and processed datasets are excluded via `.gitignore` and hosted externally (e.g., Kaggle Datasets). If you have the raw extract placed at `data/raw/PEGI.txt`, regenerate the structured dataset with:

```bash
python scripts/parse_pegi_txt.py
```

---

## Ethics, Privacy & Limitations

- **Zero Child Data:** No personally identifiable information (PII) from children or families is collected. Parental survey responses are strictly anonymous and aggregated.
- **No Causal Claims:** Feature importance in predictive models reflects classification criteria, not behavioral or psychological effects on players.
- **Content Discrepancy Nuance:** Secondary themes (e.g., brief substance references or suggestive outfits) may appear in PEGI's *Other issues* section without triggering a top-level icon.

---

## License & Attribution

- **Code & Notebooks:** Released under the [MIT License](LICENSE).
- **Classification Data:** Game rating descriptions originate from public PEGI consumer disclosures and are used strictly for non-commercial research and educational data journalism.