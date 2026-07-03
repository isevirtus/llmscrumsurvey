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

LLM use in Scrum is already routine rather than purely exploratory:

- **48.1%** of respondents use LLM chat assistants **daily or almost daily**
- **79.7%** self-assess as having qualified, proficient, or specialist-level LLM knowledge
- **ChatGPT** dominates adoption (86.1%), followed by **Gemini** (60.8%) and
  **Copilot Chat** (59.5%)
- Adoption is largely **bottom-up**: 57.0% reported informal use, while 43.0%
  reported formally established use
- Formal AI organizational policies were reported by 43.0% of respondents, while
  24.1% reported no organizational policy

### RQ2 — LLM Adoption Across Scrum Practices

Current use concentrates on **text-intensive, analytical, and synthesis-oriented tasks**:

- Highest current-use activities included improving Product Backlog item descriptions
  (62.0%), summarizing Scrum events (59.5%), exploring Scrum practices and
  techniques (58.2%), getting practical resources and examples (57.0%), clarifying
  Scrum concepts and roles (55.7%), defining non-functional requirements (55.7%),
  and summarizing Sprint Review feedback (55.7%)
- At the category level, exploring and learning Scrum practices showed the highest
  overall current adoption (81.0%), followed by artifact-related tasks (75.9%),
  event-related tasks (72.2%), and additional management activities (68.4%)
- Lower adoption or greater resistance appeared in some strategic or highly
  context-dependent activities, such as defining Product/Sprint Goals, effort
  estimation, Definition of Done, team agreements, and coaching or mentoring
  simulations

### RQ3 — Perceived Benefits

Top benefits reported by the final analytic sample (N = 79):

| Benefit                                      | Count | %     |
| -------------------------------------------- | ----- | ----- |
| Increased productivity                       | 61    | 77.2% |
| Reduced time for repetitive tasks            | 60    | 75.9% |
| Improved quality of artifacts                | 59    | 74.7% |
| Support in decision-making                   | 46    | 58.2% |
| Better communication with stakeholders       | 41    | 51.9% |
| Improved knowledge sharing and documentation | 39    | 49.4% |

Developers most frequently associated LLM use with reduced repetitive work and
improved artifact quality. Scrum Masters reported benefits related to productivity,
reduced repetitive work, artifact quality, and decision support. Product Owners
emphasized reduced repetitive work, productivity, communication with stakeholders,
and creativity in problem-solving.

### RQ4 — Risks and Challenges

Top problems encountered (N = 79):

| Problem                                       | Count | %     |
| --------------------------------------------- | ----- | ----- |
| Solutions almost right, but not quite         | 52    | 65.8% |
| Hallucinations                                | 43    | 54.4% |
| Privacy/confidentiality concerns              | 40    | 50.6% |
| Difficulty validating AI-generated content    | 37    | 46.8% |
| High variability in output quality            | 33    | 41.8% |

Qualitative themes included misleading or inaccurate outputs, privacy and security
concerns, validation effort, over-reliance, reduced critical engagement, and
inappropriate use of generated content.

### RQ5 — Future Perspectives

- **Human-led** work with AI as assistants was the most frequently selected future
  collaboration model (49.4%), followed by **balanced human-AI collaboration**
  (31.6%); together, these two categories accounted for 81.0% of respondents
- Full role replacement by AI was widely rejected: 65.8% selected no role
  replacement in the multiple-selection item about whether AI could fully or
  partially replace Scrum roles
- Among role-replacement options, Product Owner (21.5%), Scrum Master (21.5%),
  and Developers (20.3%) were selected at similar levels
- **New skills** most anticipated included prompt engineering, critical AI
  evaluation, multidisciplinary reasoning, process understanding, AI tool literacy,
  data/LLM understanding, and oversight of AI-generated artifacts
- Formalization of LLM governance and context-aware tooling are seen as key
  enablers for responsible adoption
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
