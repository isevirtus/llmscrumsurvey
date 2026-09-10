# Data Documentation

This document describes every data file used and produced by the analysis scripts.

---

## Directory Layout

```
llmscrumsurvey/
├── data/
│   ├── merged_survey_data.xlsx            # Main input — unified survey dataset
│   ├── merged_survey_data-processing.xlsx # Intermediate processing workbook
│   └── codebooks/
│       ├── rq2_final_qualitative_codebook.xlsx         # RQ2 qualitative codebook
│       ├── rq3_positive_examples_coding_checker (1).xlsx  # RQ3 positive-example codebook
│       ├── rq4_codebook.xlsx                            # RQ4 risks/negative examples
│       ├── rq5_codebook.xlsx                            # RQ5 new-skills codebook
│       └── general_comments_supplementary_codebook.xlsx # General-comments codebook
└── reports/
    ├── figures/                           # Generated figures (PDF + PNG)
    ├── descriptive_statistics_report.md   # Full Markdown statistics report
    ├── descriptive_statistics_tables.xlsx # All tables in Excel format
    ├── figure_index.csv                   # Index of all generated figures
    └── *.csv                              # Per-section frequency tables
```

---

## Input Dataset — `data/merged_survey_data.xlsx`

Unified dataset combining all survey responses collected from Scrum practitioners.

| Column | Type | Description |
|---|---|---|
| `Carimbo de data/hora` | datetime | Timestamp of response submission |
| `source` | str | Origin survey: `'Survey 1 (respostas)'` or `'Survey 2 (Udemy)'` |
| *(survey questions)* | varies | 104 survey question columns (see below) |

### Filtering Pipeline

The analysis applies a sequential filtering pipeline to obtain the **final analytic sample (N=79)**:

| Stage | Label | N |
|---|---|---|
| 1 | All submissions | 159 |
| 2 | Consenting responses | 158 |
| 3 | Scrum-experienced respondents | 128 |
| 4 | Also worked in Scrum projects | 111 |
| 5 | LLM users (used AI in last 6 months for Scrum) | 81 |
| 6 | Final analytic sample (no contradictory responses) | **79** |

### Survey Question Categories

The survey covers the following thematic areas:

1. **Participant profile** — age, education, country, Scrum knowledge, certifications, experience
2. **Organization & project** — industry, size, team size, problem domain, application domain, product duration
3. **RQ1 — LLM usage** — AI tools used, frequency, interaction modes, knowledge level, formality, policy
4. **RQ2 — Scrum activity adoption** — adoption level and perceived helpfulness per Scrum activity (artifacts, events, roles)
5. **RQ3 — Benefits** — experienced benefits, helpfulness by accountability, efficiency, Likert-scale benefit statements
6. **RQ4 — Risks & challenges** — problems encountered, biggest risks, concerns about intensive use, negative examples
7. **RQ5 — Future perspectives** — human–AI relationship, role replacement, and required new skills
8. **General comments** — optional comments, suggestions, or examples not tied to a specific RQ construct

---

## Intermediate Workbook — `data/merged_survey_data-processing.xlsx`

Working spreadsheet used during data cleaning and column mapping. Kept for audit
purposes. Not used directly by the analysis scripts.

---

## Qualitative Codebooks — `data/codebooks/`

The codebooks preserve raw responses, normalization or translation decisions,
segment-level coding, and the available checker decisions. They are qualitative
audit artifacts and are not read by the descriptive-analysis scripts. Raw
open-response totals in `reports/04_rq2_open_response_counts.csv` through
`reports/08_general_comments_open_count.csv` are computed directly from
`data/merged_survey_data.xlsx` after applying the final-sample filter.

Because coding is segment-level, one usable raw response may yield multiple coded
segments. Segment counts describe the coded material; they are not prevalence
estimates for the full analytic sample.

### `rq2_final_qualitative_codebook.xlsx`

Current coding and checker workbook for the open-ended responses associated with
**RQ2**. It covers additional activities and example prompts for learning about
Scrum, Scrum artifacts, Scrum events, and other Agile management tasks. It also
contains the task-oriented coding scheme, segment classifications, and checker
decisions.

### `rq3_positive_examples_coding_checker (1).xlsx`

Coding and checker workbook for the positive-example item associated with **RQ3**
(benefits). It contains 23 raw responses, 19 responses marked usable, and 52 coded
segments. The workbook distinguishes direct Scrum-management support from
adjacent software-engineering support and out-of-scope examples.

### `rq4_codebook.xlsx`

Coding and checker workbook for the two open-ended **RQ4** items: the biggest
perceived risk and negative examples. It contains 34 biggest-risk answers and 16
negative-example answers, with source-row identifiers linking the records to the
merged survey data. Coding is organized around risks, mechanisms, and
consequences.

### `rq5_codebook.xlsx`

Coding workbook for the **RQ5** new-skills item. It contains 20 raw responses, 17
responses currently marked usable, and 25 coded segments. Checker-agreement and
final-usability fields are retained in the workbook and are under author
verification; final classifications should not be described as independently
checked until those fields have been completed.

### `general_comments_supplementary_codebook.xlsx`

Separate supplementary workbook for the optional general-comments item. It
contains 8 raw comments, 7 comments marked usable, and 7 coded segments. These
segments are retained as contextual or audit material and must not be combined
with RQ-specific qualitative counts.

### Coding and checking terminology

The documented workflow distinguishes initial extraction/coding from a subsequent
checker review. This is a checker-audit workflow, not independent double coding.
Accordingly, percent agreement may summarize recorded checker decisions, but it
should not be presented as Cohen's kappa or as an independent inter-rater
reliability estimate.

---

## Output Files — `reports/`

### Pre-generated CSV Tables (`reports/*.csv`)

Each script run produces a set of named CSV files. Files are prefixed by section:

| Prefix | Content |
|---|---|
| `00_` | Filtering pipeline summary |
| `01_profile_*` | Participant profile by cohort (N=158, N=128, N=111, N=79) |
| `02_org_project_*` | Organization and project characteristics by cohort |
| `03_rq1_*` | RQ1 — LLM usage patterns |
| `04_rq2_*` | RQ2 — Scrum activity adoption and helpfulness |
| `05_rq3_*` | RQ3 — Benefits and perceived value |
| `06_rq4_*` | RQ4 — Risks, problems, and concerns |
| `07_rq5_*` | RQ5 — Future perspectives |
| `08_general_*` | General open-ended comments |
| `99_consistency_*` | Internal consistency checks |

Files with suffix `_other_unmatched.csv` contain free-text responses that did not
match any predefined option, preserved for qualitative inspection.

### Markdown Report — `reports/descriptive_statistics_report.md`

Human-readable Markdown tables for all survey sections, generated by
`scripts/generate_descriptive_statistics.py`.

### Excel Tables — `reports/descriptive_statistics_tables.xlsx`

Alternative to the Markdown report, in multi-sheet Excel format for easy
inspection or integration with office software.

### Figures — `reports/figures/`

Publication-ready figures generated by `scripts/generate_descriptive_statistics.py`.
Both PDF (vector) and PNG (raster) versions are provided.

| File | Description |
|---|---|
| `figure_02_filtering_pipeline.*` | Funnel diagram of the filtering pipeline |
| `figure_03a_organization_industry.*` | Organization industry distribution |
| `figure_03b_organization_size.*` | Organization size distribution |
| `figure_04a_primary_role.*` | Primary Scrum role of participants |
| `figure_04b_application_domain.*` | Application domain distribution |
| `figure_04c_scrum_team_size.*` | Scrum team size distribution |
| `figure_04d_product_duration.*` | Product/project duration distribution |
| `figure_05a_frequency_of_use.*` | Frequency of LLM use |
| `appendix_table3_benefits_chart.*` | Benefits experienced (appendix figure) |
| `appendix_table4_problems_chart.*` | Problems encountered (appendix figure) |
| *(additional figures)* | Further RQ-specific plots |

---

## Reproducibility

To regenerate all outputs from scratch:

```bash
# Descriptive statistics + figures
uv run python scripts/generate_descriptive_statistics.py

# Table 2 (participant profile with certifications)
uv run python scripts/compute_table2_participant_profile.py
```

Both scripts accept `--input` and `--output-dir` flags to override the default
paths (`data/merged_survey_data.xlsx` and `reports/` respectively).
