# Supplementary Material: "Large Language Models in Scrum Management: Findings from an International Survey of Practitioners"

## Overview

This repository contains the supplementary material for the research paper
**"Large Language Models in Scrum Management: Findings from an International
Survey of Practitioners"** submitted to the **Journal of Systems and Software**.

The study investigates how Agile practitioners currently use Large Language Models
(AI chat assistants such as ChatGPT, Claude, and Gemini) to support **Scrum
management activities** — spanning Scrum artifacts, events, and roles. Through an
international online survey of 159 practitioners from **37 countries**, the research
characterises usage patterns, perceived benefits, risks, and expectations for the
future role of LLMs in Scrum practice.

---

## Research Questions

1. **RQ1** — What is the current level of knowledge and usage of LLMs among
   Scrum professionals?
2. **RQ2** — In which Scrum practices (artifacts, events, and roles) are LLMs
   being adopted, and how helpful are they perceived to be?
3. **RQ3** — What benefits do Scrum teams perceive from using LLMs?
4. **RQ4** — What risks and challenges are associated with LLM use in Scrum
   contexts?
5. **RQ5** — What are professionals' expectations for the future role of LLMs
   in Scrum management activities?

---

## Methodology

### Survey Design

- **Survey type**: Online questionnaire (Google Forms) combining closed- and
  open-ended items
- **Target population**: Scrum Masters, Product Owners, Developers, and other
  Agile practitioners
- **Distribution channels**: Professional social networks (LinkedIn Agile/Scrum
  groups), mailing lists of software engineering associations, direct invitations,
  and snowball sampling
- **Total submissions**: 159 responses from **37 countries**
- **Data analysis**: Descriptive statistics for closed-ended items; thematic coding
  for open-ended responses
- **Approximate completion time**: ~12 minutes

### Filtering Pipeline

| Stage                                                     | Cohort   | N      |
| --------------------------------------------------------- | -------- | ------ |
| All submissions                                           | —        | 159    |
| Consenting responses                                      | —        | 158    |
| Scrum-experienced respondents                             | —        | 128    |
| Worked in at least one Scrum project                      | —        | 111    |
| LLM users (AI chat assistants for Scrum in last 6 months) | —        | 81     |
| **Final analytic sample** (no contradictory responses)    | **N=79** | **79** |

---

## Repository Structure

```
llmscrumsurvey/
├── README.md                    # This file
├── DATA_README.md               # Detailed data documentation
├── CITATION.cff                 # Citation metadata
├── LICENSE                      # MIT License
├── pyproject.toml               # Python project & dependency declaration (uv)
├── uv.lock                      # Locked dependency versions
├── .python-version              # Python version pin (3.12)
├── .gitignore
├── data/
│   ├── merged_survey_data.xlsx              # Main input — unified survey dataset (N=159)
│   ├── merged_survey_data-processing.xlsx   # Intermediate processing workbook
│   └── codebooks/
│       ├── rq2_final_qualitative_codebook.xlsx              # RQ2 qualitative codebook
│       └── rq3_positive_examples_coding_checker (1).xlsx    # RQ3 coding checker
├── scripts/
│   ├── generate_descriptive_statistics.py   # Descriptive statistics + figures (main script)
│   └── compute_table2_participant_profile.py # Table 2 — participant profile with certifications
└── reports/
    ├── figures/                             # Publication-ready figures (PDF + PNG)
    ├── descriptive_statistics_report.md     # Full Markdown statistics report
    ├── descriptive_statistics_tables.xlsx   # All tables in Excel format
    ├── figure_index.csv                     # Index of generated figures
    └── *.csv                                # Per-section frequency tables (pre-generated)
```

---

## Setup & Reproduction

### Prerequisites

- Python ≥ 3.12
- [uv](https://github.com/astral-sh/uv) package manager

### 1. Clone the repository

```bash
git clone https://github.com/isevirtus/llmscrumsurvey
cd llmscrumsurvey
```

### 2. Install dependencies

```bash
uv sync
```

> All dependencies (`pandas`, `openpyxl`, `matplotlib`, `seaborn`) are declared
> in `pyproject.toml` and pinned in `uv.lock`.

### 3. Generate descriptive statistics and figures

```bash
uv run python scripts/generate_descriptive_statistics.py
```

This reads `data/merged_survey_data.xlsx` and writes all outputs to `reports/`:

- `reports/descriptive_statistics_report.md` — Markdown tables
- `reports/descriptive_statistics_tables.xlsx` — Excel tables
- `reports/figures/` — publication-ready figures (PDF + PNG)
- `reports/*.csv` — per-section frequency tables

Override input or output paths with CLI flags:

```bash
uv run python scripts/generate_descriptive_statistics.py \
    --input data/merged_survey_data.xlsx \
    --output-dir reports
```

### 4. Compute Table 2 (participant profile with certifications)

```bash
uv run python scripts/compute_table2_participant_profile.py
```

This reads `data/merged_survey_data.xlsx` and writes Table 2 outputs to `reports/`:

- `reports/table2_participant_profile_N79.csv`
- `reports/table2_participant_profile_N79.tex` (LaTeX-ready)
- `reports/table2_participant_profile_N79_all_countries.csv`
- `reports/table2_certification_summary_N79.csv`
- `reports/table2_scrum_certification_free_text_audit_N79.csv`
- `reports/table2_agile_certification_free_text_audit_N79.csv`

Override paths:

```bash
uv run python scripts/compute_table2_participant_profile.py \
    --input data/merged_survey_data.xlsx \
    --output-dir reports
```

---

## Pre-generated Outputs

The `reports/` directory already contains **pre-generated outputs** from the
final analysis run. These allow reviewers to inspect all results without
re-running the scripts.

See [DATA_README.md](DATA_README.md) for a complete file-by-file description.

---

## Key Findings

### RQ1 — Knowledge and Usage of LLMs

LLM use in Scrum is already routine rather than exploratory:

- **48%** of respondents use LLM chat assistants **daily or almost daily**
- **78%** self-assess as having intermediate or advanced proficiency
- **ChatGPT** dominates adoption (85.7%), followed by **Gemini** (60%) and
  **Copilot** (57%)
- Adoption is largely **bottom-up**: formal organizational governance covers only
  roughly half of respondents; 55.6% use LLMs informally

### RQ2 — LLM Adoption Across Scrum Practices

Current use concentrates on **text-intensive and analytical tasks**:

- Highest adoption: Writing Product Backlog Items (PBIs), Non-functional
  Requirements, and Acceptance Criteria; event summarization; issue summaries
- Lowest adoption (resistance): strategic activities such as defining Product/Sprint
  Goals, estimating effort, and defining the Definition of Done

### RQ3 — Perceived Benefits

Top benefits reported by the final analytic sample (N=79):

| Benefit                                      | Count | %     |
| -------------------------------------------- | ----- | ----- |
| Increased productivity                       | 61    | 77.2% |
| Reduced time for repetitive tasks            | 60    | 76.5% |
| Improved quality of artifacts                | —     | ~74%  |
| Better communication with stakeholders       | 44    | 55.9% |
| Improved knowledge sharing and documentation | 36    | 45.6% |

Developers report the highest perceived benefit; Product Owners show the greatest
variability.

### RQ4 — Risks and Challenges

Top problems encountered (N=79):

| Problem                                       | Count | %     |
| --------------------------------------------- | ----- | ----- |
| Solutions almost right, but not quite         | 53    | 67.6% |
| Hallucinations (fabricated/incorrect answers) | 41    | 51.5% |
| Privacy/confidentiality concerns              | 37    | 47.1% |
| Difficulty validating AI-generated content    | 35    | 44.1% |
| High variability in output quality            | 34    | 42.6% |

Qualitative themes: misleading outputs in management reports, over-reliance and
declining critical engagement, and social signals of uncritical AI use.

### RQ5 — Future Perspectives

- **Majority** favour **human-led** or balanced human-AI collaboration models;
  full role replacement by AI is widely rejected
- **New skills** most anticipated: prompt engineering, critical AI evaluation,
  multidisciplinary reasoning, and oversight of AI-generated artefacts
- Formalization of LLM governance and context-aware tooling are seen as
  key enablers for responsible adoption

---

## Contributing

This is a research repository. Contributions are welcome:

1. **Issues** — bug reports or questions about the data/code.
2. **Discussions** — research-related questions.
3. **Pull Requests** — improvements to analysis scripts.

---

## Citation

If you use this data or code in your work, please cite:

```bibtex
@article{albuquerque2026llmscrum,
  title   = {Large Language Models in Scrum Management: Findings from an International Survey of Practitioners},
  author  = {Danyllo Albuquerque and Mirko Perkusich and Matheus Paixão and
             Allysson Allex Araújo and Marcos Kalinowski and Rohit Gheyi and
             Danilo Santos and Angelo Perkusich},
  journal = {Journal of Systems and Software},
  year    = {2026},
  doi     = {PLACEHOLDER_DOI},
  url     = {https://github.com/isevirtus/llmscrumsurvey},
  note    = {Supplementary material available at GitHub repository}
}
```

See [CITATION.cff](CITATION.cff) for full citation metadata.

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## Authors

| Author                    | Affiliation                               | ORCID                                                        |
| ------------------------- | ----------------------------------------- | ------------------------------------------------------------ |
| **Danyllo Albuquerque**   | VIRTUS / UFCG, Campina Grande, PB, Brazil | [0000-0001-5515-7812](https://orcid.org/0000-0001-5515-7812) |
| **Mirko Perkusich**       | VIRTUS / UFCG, Campina Grande, PB, Brazil | [0000-0002-9433-4962](https://orcid.org/0000-0002-9433-4962) |
| **Matheus Paixão**        | UECE, Fortaleza, CE, Brazil               | —                                                            |
| **Allysson Allex Araújo** | UFCA, Juazeiro do Norte, CE, Brazil       | —                                                            |
| **Marcos Kalinowski**     | PUC-Rio, Rio de Janeiro, RJ, Brazil       | —                                                            |
| **Rohit Gheyi**           | VIRTUS / UFCG, Campina Grande, PB, Brazil | —                                                            |
| **Danilo Santos**         | VIRTUS / UFCG, Campina Grande, PB, Brazil | —                                                            |
| **Angelo Perkusich**      | VIRTUS / UFCG, Campina Grande, PB, Brazil | [0000-0002-7377-1258](https://orcid.org/0000-0002-7377-1258) |
