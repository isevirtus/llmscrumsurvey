#!/usr/bin/env python3
"""
Compute Table 2 (participant profile) for the final analytic sample (N=79)
from merged_survey_data.xlsx, including certification statistics.

Filtering logic:
159 survey submissions -> 158 consenting responses -> 128 Scrum-experienced
respondents -> 81 initially screened LLM-for-Scrum users -> 79 final analytic
responses after excluding contradictory LLM-use responses.

Outputs:
  - table2_participant_profile_N79.csv
  - table2_participant_profile_N79.tex
  - table2_participant_profile_N79_all_countries.csv
  - table2_certification_summary_N79.csv
  - table2_scrum_certification_free_text_audit_N79.csv
  - table2_agile_certification_free_text_audit_N79.csv

Run (from project root):
  uv run python scripts/compute_table2_participant_profile.py \
      --input data/merged_survey_data.xlsx \
      --output-dir reports
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd

# -----------------------------------------------------------------------------
# Generic helpers
# -----------------------------------------------------------------------------


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def normalize_key(value: object) -> str:
    return normalize_text(value).lower()


def starts_with_yes(value: object) -> bool:
    return normalize_key(value).startswith("yes")


def pct(count: int, denominator: int) -> float:
    return round(100 * count / denominator, 1) if denominator else 0.0


def find_column(
    df: pd.DataFrame,
    required_fragments: Iterable[str],
    forbidden_fragments: Iterable[str] = (),
) -> str:
    required = [f.lower() for f in required_fragments]
    forbidden = [f.lower() for f in forbidden_fragments]
    matches = []

    for col in df.columns:
        simplified = re.sub(r"\s+", " ", str(col)).lower()
        if all(f in simplified for f in required) and not any(
            f in simplified for f in forbidden
        ):
            matches.append(col)

    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one column for required={list(required_fragments)} "
            f"forbidden={list(forbidden_fragments)}, found {len(matches)}: {matches}"
        )

    return matches[0]


def categorical_counts(
    series: pd.Series,
    denominator: int,
    order: Sequence[str] | None = None,
) -> pd.DataFrame:
    clean = series.map(normalize_text)
    counts = clean[clean != ""].value_counts()

    if order:
        rows = []
        used = set()

        for label in order:
            count = int(counts.get(label, 0))
            rows.append(
                {
                    "response": label,
                    "count": count,
                    "percent": pct(count, denominator),
                }
            )
            used.add(label)

        for label, count in counts.items():
            if label not in used:
                rows.append(
                    {
                        "response": label,
                        "count": int(count),
                        "percent": pct(int(count), denominator),
                    }
                )

        return pd.DataFrame(rows)

    return pd.DataFrame(
        [
            {
                "response": label,
                "count": int(count),
                "percent": pct(int(count), denominator),
            }
            for label, count in counts.items()
        ]
    )


def latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "<": r"\textless{}",
        ">": r"\textgreater{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


# -----------------------------------------------------------------------------
# Short labels for profile variables
# -----------------------------------------------------------------------------


def short_scrum_knowledge(label: str) -> str:
    if label.startswith("Novice"):
        return "Novice"
    if label.startswith("Beginner"):
        return "Beginner"
    if label.startswith("Qualified"):
        return "Qualified"
    if label.startswith("Proficient"):
        return "Proficient"
    if label.startswith("Specialist"):
        return "Specialist"
    return label


def short_education(label: str) -> str:
    return {
        "Professional/Regular high school": "Professional / high school",
        "Master's degree (Professional or academic)": "Master's degree",
        "Doctorate degree (Professional or academic)": "Doctorate degree",
    }.get(label, label)


def short_experience(label: str) -> str:
    return {
        "Less than 3 years": "< 3 years",
        "Between 3 and 5 years": "3--5 years",
        "Between 6 and 10 years": "6--10 years",
        "Between 11 and 15 years": "11--15 years",
        "Between 16 and 20 years": "16--20 years",
        "More than 20 years": "> 20 years",
    }.get(label, label)


# -----------------------------------------------------------------------------
# Filtering
# -----------------------------------------------------------------------------


def build_final_sample(df: pd.DataFrame) -> pd.DataFrame:
    consent_col = find_column(df, ["agree to participate"])
    scrum_exp_col = find_column(df, ["experience", "scrum projects"])
    llm_use_col = find_column(
        df,
        ["last 6 months", "ai chat assistant", "scrum management"],
    )
    formality_col = find_column(
        df,
        ["how formally", "use ai chat assistants", "scrum management"],
    )

    consenting = df[df[consent_col].apply(starts_with_yes)].copy()

    scrum_experienced = consenting[
        consenting[scrum_exp_col].apply(lambda x: normalize_key(x) != "no experience")
    ].copy()

    llm_users_precheck = scrum_experienced[
        scrum_experienced[llm_use_col].apply(starts_with_yes)
    ].copy()

    final_sample = llm_users_precheck[
        ~llm_users_precheck[formality_col].apply(
            lambda x: normalize_key(x).startswith(
                "i don't use llm in scrum-based activities"
            )
        )
    ].copy()

    return final_sample


# -----------------------------------------------------------------------------
# Certification parsing
# -----------------------------------------------------------------------------


SCRUM_CERT_OPTIONS = [
    ("Scrum Master --- Foundational", "Scrum Master — Foundational (e.g., PSM I, CSM)"),
    (
        "Scrum Master --- Intermediate",
        "Scrum Master — Intermediate (e.g., PSM II, A-CSM)",
    ),
    ("Scrum Master --- Advanced", "Scrum Master — Advanced (e.g., PSM III, CSP-SM)"),
    (
        "Product Owner --- Foundational",
        "Product Owner — Foundational (e.g., PSPO I, CSPO)",
    ),
    (
        "Product Owner --- Intermediate",
        "Product Owner — Intermediate (e.g., PSPO II, A-CSPO)",
    ),
    ("Product Owner --- Advanced", "Product Owner — Advanced (e.g., PSPO III, CSP-PO)"),
    ("Developer certification", "Developer (e.g., PSD, CSD, A-CSD, CSP-D)"),
]

AGILE_CERT_OPTIONS = [
    ("PMI-ACP", "PMI-ACP"),
    ("Scaled frameworks", "Scaled frameworks (e.g., SAFe, CASP, SPS)"),
    ("Kanban", "Kanban (e.g., PSK, APK)"),
    (
        "Agile facilitation/coaching/leadership",
        "Agile Facilitation/Coaching/Leadership (e.g., PAL, PAL-EBM, PSF, CAL, CAF)",
    ),
]

NO_CERT_PATTERNS = [
    r"^no$",
    r"^none$",
    r"^nenhuma$",
    r"^nenhuma certificação$",
    r"^não$",
    r"^nao$",
    r"^not yet$",
    r"not yet certified",
    r"no certification",
    r"no certifications",
    r"do not have",
    r"don't have",
    r"dont have",
    r"do not hold",
    r"don't hold",
    r"did not have",
    r"did not held",
    r"don'?t any certifications",
    r"dont any certifications",
    r"i learned on job",
    r"studying",
    r"in progress",
]


def is_no_cert_free_text(text: str) -> bool:
    key = normalize_key(text)

    if not key:
        return True

    return any(re.search(pattern, key) for pattern in NO_CERT_PATTERNS)


def parse_certification_cell(
    value: object,
    options: Sequence[tuple[str, str]],
) -> tuple[set[str], str, bool]:
    """
    Parse a multi-select certification cell using canonical option matching.

    Returns:
      selected_short_labels: canonical options detected in the cell.
      residual: remaining text after removing canonical options and separators.
      no_cert_like: True if residual is empty or clearly means no certification.

    This intentionally avoids comma splitting because canonical options contain
    commas inside examples, e.g., "PSM I, CSM".
    """
    raw = normalize_text(value)

    if not raw:
        return set(), "", True

    selected: set[str] = set()
    residual = raw

    for short_label, canonical in sorted(
        options, key=lambda x: len(x[1]), reverse=True
    ):
        pattern = re.escape(canonical)

        if re.search(pattern, raw, flags=re.IGNORECASE):
            selected.add(short_label)
            residual = re.sub(pattern, "", residual, flags=re.IGNORECASE)

    residual = re.sub(r"\s*,\s*", ", ", residual)
    residual = re.sub(r"^(,\s*)+|(,\s*)+$", "", residual).strip()
    residual = re.sub(r"(,\s*){2,}", ", ", residual).strip()

    no_cert_like = is_no_cert_free_text(residual)

    return selected, residual, no_cert_like


def certification_table(
    series: pd.Series,
    denominator: int,
    options: Sequence[tuple[str, str]],
    category_type: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Build certification table rows and a residual audit table.

    category_type: "scrum" or "agile". Used to name output labels.
    """
    option_counts: Counter[str] = Counter()
    residual_counts: Counter[str] = Counter()
    no_cert_count = 0
    at_least_one_count = 0

    for value in series:
        selected, residual, no_cert_like = parse_certification_cell(value, options)

        if selected:
            at_least_one_count += 1
            option_counts.update(selected)

            if residual and not no_cert_like:
                residual_counts[residual] += 1
        else:
            if no_cert_like:
                no_cert_count += 1
            else:
                at_least_one_count += 1
                residual_counts[residual] += 1

    rows = []

    for short_label, _canonical in options:
        count = int(option_counts[short_label])
        rows.append(
            {
                "response": short_label,
                "count": count,
                "percent": pct(count, denominator),
            }
        )

    other_label = (
        "Other Scrum-role certification/free-text response"
        if category_type == "scrum"
        else "Other Agile/related certification/free-text response"
    )
    no_cert_label = (
        "No Scrum-role certification reported"
        if category_type == "scrum"
        else "No Agile/related certification reported"
    )

    other_count = int(sum(residual_counts.values()))

    rows.append(
        {
            "response": other_label,
            "count": other_count,
            "percent": pct(other_count, denominator),
        }
    )
    rows.append(
        {
            "response": no_cert_label,
            "count": no_cert_count,
            "percent": pct(no_cert_count, denominator),
        }
    )

    table = pd.DataFrame(rows)

    residual = pd.DataFrame(
        [
            {
                "free_text_or_unmatched_response": response,
                "count": count,
            }
            for response, count in residual_counts.most_common()
        ]
    )

    table.attrs["at_least_one_count"] = at_least_one_count
    table.attrs["no_cert_count"] = no_cert_count
    table.attrs["other_count"] = other_count

    return table, residual


# -----------------------------------------------------------------------------
# LaTeX rendering
# -----------------------------------------------------------------------------


def render_latex_table(groups: list[tuple[str, pd.DataFrame]], n: int) -> str:
    latex_lines = []

    latex_lines.append(r"\begin{table}[!h]")
    latex_lines.append(r"\centering")
    latex_lines.append(
        rf"\caption{{Participant profile of the final analytic sample (N = {n}).}}"
    )
    latex_lines.append(r"\label{tab:demographics}")
    latex_lines.append(r"\small")
    latex_lines.append("")
    latex_lines.append(r"\begin{minipage}{0.98\linewidth}")
    latex_lines.append(r"\centering")
    latex_lines.append("")
    latex_lines.append(r"\scalebox{0.68}{")
    latex_lines.append(r"\begin{tabular}{p{4.0cm} p{6.2cm} r r}")
    latex_lines.append(r"\hline")
    latex_lines.append(
        r"\textbf{Category} & \textbf{Response} & \textbf{Count} & \textbf{Percent} \\"
    )
    latex_lines.append(r"\hline")

    for category, table in groups:
        rows = list(table.to_dict("records"))

        latex_lines.append(
            rf"\multirow{{{len(rows)}}}{{*}}{{\textbf{{{latex_escape(category)}}}}}"
        )

        for row in rows:
            response = str(row["response"])
            count = int(row["count"])
            percent = float(row["percent"])

            latex_lines.append(
                rf" & {latex_escape(response)} & {count} & {percent:.1f}\% \\"
            )

        latex_lines.append(r"\hline")
        latex_lines.append("")

    latex_lines.append(r"\end{tabular}")
    latex_lines.append(r"}")
    latex_lines.append("")
    latex_lines.append(r"\par\vspace{1mm}")
    latex_lines.append("")
    latex_lines.append(r"\parbox{0.96\linewidth}{")
    latex_lines.append(r"\scriptsize")
    latex_lines.append(
        r"\textit{Note.} Certification items were multiple-choice; therefore, percentages within certification categories do not sum to 100\%."
    )
    latex_lines.append(r"}")
    latex_lines.append("")
    latex_lines.append(r"\end{minipage}")
    latex_lines.append(r"\end{table}")

    return "\n".join(latex_lines)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/merged_survey_data.xlsx"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports"),
    )
    parser.add_argument(
        "--country-min-count",
        type=int,
        default=2,
        help="Countries with counts below this threshold are grouped as Others.",
    )
    args = parser.parse_args()

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(args.input, engine="openpyxl")
    final_sample = build_final_sample(df)

    n = len(final_sample)

    if n != 79:
        raise RuntimeError(
            f"Expected final analytic sample N=79, got N={n}. "
            "Check filtering logic or input file."
        )

    country_col = find_column(df, ["country", "currently work"])
    education_col = find_column(df, ["academic education"])
    scrum_knowledge_col = find_column(df, ["knowledge level", "scrum"])
    scrum_exp_col = find_column(df, ["experience", "scrum projects"])
    scrum_cert_col = find_column(df, ["scrum-role certifications"])
    agile_cert_col = find_column(df, ["agile or related certifications"])

    # Countries: show countries with count >= threshold; group the rest.
    country_all = categorical_counts(final_sample[country_col], n)
    country_all.to_csv(
        output_dir / "table2_participant_profile_N79_all_countries.csv",
        index=False,
    )

    country_major = country_all[country_all["count"] >= args.country_min_count].copy()
    country_minor = country_all[country_all["count"] < args.country_min_count].copy()

    if not country_minor.empty:
        country_major = pd.concat(
            [
                country_major,
                pd.DataFrame(
                    [
                        {
                            "response": f"Others ({country_minor['response'].nunique()} countries)",
                            "count": int(country_minor["count"].sum()),
                            "percent": pct(int(country_minor["count"].sum()), n),
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )

    education_order = [
        "Professional/Regular high school",
        "Undergraduate (not completed)",
        "Undergraduate (completed)",
        "MBA",
        "Master's degree (Professional or academic)",
        "Doctorate degree (Professional or academic)",
    ]

    knowledge_order = [
        'Novice - Minimum or "conceptual" knowledge without relevant practical experience.',
        "Beginner - Knowledge of the main practical aspects.",
        "Qualified - Good conceptual knowledge and practical experience.",
        "Proficient - In-depth advanced conceptual understanding and high practical knowledge.",
        "Specialist - In-depth conceptual knowledge and deep practical understanding.",
    ]

    experience_order = [
        "Less than 3 years",
        "Between 3 and 5 years",
        "Between 6 and 10 years",
        "Between 11 and 15 years",
        "Between 16 and 20 years",
        "More than 20 years",
    ]

    education = categorical_counts(final_sample[education_col], n, education_order)
    education["response"] = education["response"].map(short_education)

    knowledge = categorical_counts(
        final_sample[scrum_knowledge_col], n, knowledge_order
    )
    knowledge["response"] = knowledge["response"].map(short_scrum_knowledge)

    experience = categorical_counts(final_sample[scrum_exp_col], n, experience_order)
    experience = experience[experience["count"] > 0].copy()
    experience["response"] = experience["response"].map(short_experience)

    scrum_certs, scrum_residual = certification_table(
        final_sample[scrum_cert_col],
        n,
        SCRUM_CERT_OPTIONS,
        "scrum",
    )

    agile_certs, agile_residual = certification_table(
        final_sample[agile_cert_col],
        n,
        AGILE_CERT_OPTIONS,
        "agile",
    )

    # Save residual audits to inspect free-text/unmatched responses.
    scrum_residual.to_csv(
        output_dir / "table2_scrum_certification_free_text_audit_N79.csv",
        index=False,
    )
    agile_residual.to_csv(
        output_dir / "table2_agile_certification_free_text_audit_N79.csv",
        index=False,
    )

    cert_summary = pd.DataFrame(
        [
            {
                "certification_type": "Scrum-role certifications",
                "metric": "At least one Scrum-role certification/free-text credential",
                "count": int(scrum_certs.attrs["at_least_one_count"]),
                "percent": pct(int(scrum_certs.attrs["at_least_one_count"]), n),
                "denominator": n,
            },
            {
                "certification_type": "Scrum-role certifications",
                "metric": "No Scrum-role certification reported",
                "count": int(scrum_certs.attrs["no_cert_count"]),
                "percent": pct(int(scrum_certs.attrs["no_cert_count"]), n),
                "denominator": n,
            },
            {
                "certification_type": "Agile/related certifications",
                "metric": "At least one Agile/related certification/free-text credential",
                "count": int(agile_certs.attrs["at_least_one_count"]),
                "percent": pct(int(agile_certs.attrs["at_least_one_count"]), n),
                "denominator": n,
            },
            {
                "certification_type": "Agile/related certifications",
                "metric": "No Agile/related certification reported",
                "count": int(agile_certs.attrs["no_cert_count"]),
                "percent": pct(int(agile_certs.attrs["no_cert_count"]), n),
                "denominator": n,
            },
        ]
    )

    cert_summary.to_csv(
        output_dir / "table2_certification_summary_N79.csv",
        index=False,
    )

    groups = [
        ("Country of work", country_major),
        ("Education background", education),
        ("Scrum knowledge", knowledge),
        ("Scrum experience", experience),
        ("Scrum certifications", scrum_certs),
        ("Agile certifications", agile_certs),
    ]

    flat_rows = []

    for category, table in groups:
        for _, row in table.iterrows():
            flat_rows.append(
                {
                    "category": category,
                    "response": str(row["response"]),
                    "count": int(row["count"]),
                    "percent": float(row["percent"]),
                    "denominator": n,
                }
            )

    flat = pd.DataFrame(flat_rows)

    flat.to_csv(
        output_dir / "table2_participant_profile_N79.csv",
        index=False,
    )

    tex = render_latex_table(groups, n)

    (output_dir / "table2_participant_profile_N79.tex").write_text(
        tex,
        encoding="utf-8",
    )

    print(f"Final analytic sample: N={n}")
    print(f"Saved: {output_dir / 'table2_participant_profile_N79.csv'}")
    print(f"Saved: {output_dir / 'table2_participant_profile_N79_all_countries.csv'}")
    print(f"Saved: {output_dir / 'table2_participant_profile_N79.tex'}")
    print(f"Saved: {output_dir / 'table2_certification_summary_N79.csv'}")
    print(f"Saved: {output_dir / 'table2_scrum_certification_free_text_audit_N79.csv'}")
    print(f"Saved: {output_dir / 'table2_agile_certification_free_text_audit_N79.csv'}")


if __name__ == "__main__":
    main()
