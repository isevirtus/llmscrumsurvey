#!/usr/bin/env python3
"""
Generate deterministic descriptive statistics for the manuscript:
"Large Language Models in Scrum Management: Findings from an International Survey of Practitioners".

This script is intended to replace manual/LLM-based counting. It applies the
agreed filtering pipeline and exports audit-ready CSV and Markdown reports.

Default input:
    data/merged_survey_data.xlsx

Default outputs:
    reports/descriptive_statistics_report.md
    reports/descriptive_statistics_tables.xlsx
    reports/*.csv

Run (from project root):
    uv run python scripts/generate_descriptive_statistics.py
    uv run python scripts/generate_descriptive_statistics.py --input data/merged_survey_data.xlsx --output-dir reports

Dependencies:
    pip install pandas openpyxl
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

import pandas as pd

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

DEFAULT_INPUT = Path("data/merged_survey_data.xlsx")
DEFAULT_OUTPUT_DIR = Path("reports")

RESPONSE_ORDER_ADOPTION = [
    "Currently Mostly AI Chat Assistant",
    "Currently Partially AI Chat Assistant",
    "Plan to Mostly Use AI Chat Assistant",
    "Plan to Partially Use AI Chat Assistant",
    "Don't Plan to Use AI Chat Assistant for This Task",
]

RESPONSE_ORDER_HELPFULNESS = [
    "Very Helpful",
    "Helpful",
    "Neutral",
    "Slightly Helpful",
    "Not Helpful",
    "Not applicable",
]

# Some older/generated scripts used a different scale. Keep aliases to be safe.
HELPFULNESS_ALIASES = {
    "not at all helpful": "Not Helpful",
    "not helpful": "Not Helpful",
    "slightly helpful": "Slightly Helpful",
    "moderately helpful": "Helpful",
    "helpful": "Helpful",
    "very helpful": "Very Helpful",
    "extremely helpful": "Very Helpful",
    "not applicable": "Not applicable",
    "n/a": "Not applicable",
    "na": "Not applicable",
}

AGREEMENT_ORDER = [
    "Strongly disagree",
    "Disagree",
    "Neutral",
    "Agree",
    "Strongly agree",
]
AGREEMENT_ALIASES = {
    "strongly disagree": "Strongly disagree",
    "disagree": "Disagree",
    "neutral": "Neutral",
    "agree": "Agree",
    "strongly agree": "Strongly agree",
}

YES_NO_MAYBE_ORDER = ["Yes", "Maybe", "No"]
YES_NO_MAYBE_ALIASES = {"yes": "Yes", "maybe": "Maybe", "no": "No"}

AI_TOOLS = [
    "ChatGPT (OpenAI)",
    "Gemini (Google)",
    "Claude (Anthropic)",
    "Copilot Chat (Microsoft)",
    "DeepSeek Chat",
    "Perplexity AI",
    "Mistral Le Chat",
    "A proprietary or internal AI Chat Assistant developed or customized by your organization",
]

INTERACTION_MODES = [
    "Text (typing or copy-pasting prompts)",
    "Voice (speaking or dictation)",
    "Images or screenshots (e.g., sharing a burndown chart)",
    "Files or documents (e.g., uploading PDFs, code files)",
    "Technical implementation tasks (e.g., writing/explaining/debugging code; generating tests, scripts, and config files; CI/CD & Infrastructure-as-Code; crafting queries/API calls; refactoring/performance/security hardening) (excludes inline autocomplete tools)",
]

BENEFITS = [
    "Increased productivity",
    "Improved quality of artifacts",
    "Reduced time for repetitive tasks",
    "Support in decision-making",
    "Better communication with stakeholders",
    "Faster onboarding of new team members",
    "Improved knowledge sharing and documentation",
    "Enhanced creativity in problem-solving",
    "Better stakeholder alignment through clearer outputs",
    "Increased stakeholder trust in project outputs",
]

BENEFIT_SHORT_LABELS = {
    "Increased productivity": "Increased productivity",
    "Improved quality of artifacts": "Improved quality of artifacts",
    "Reduced time for repetitive tasks": "Reduced time for repetitive tasks",
    "Support in decision-making": "Support in decision-making",
    "Better communication with stakeholders": "Better communication with stakeholders",
    "Faster onboarding of new team members": "Faster onboarding of new team members",
    "Improved knowledge sharing and documentation": "Improved knowledge sharing and documentation",
    "Enhanced creativity in problem-solving": "Enhanced creativity in problem-solving",
    "Better stakeholder alignment through clearer outputs": "Better stakeholder alignment through clearer outputs",
    "Increased stakeholder trust in project outputs": "Increased stakeholder trust in project outputs",
}

PROBLEMS = [
    "Solutions that are almost right, but not quite",
    "Difficulty in validating AI Chat Assistant-generated content",
    "High variability in output quality",
    "Difficulty adapting to project/team context",
    "Lack of integration with existing tools",
    "Over-dependence of the team on AI Chat Assistants",
    "Resistance from team members to adopt AI Chat Assistants",
    "I've become less confident in my own problem-solving",
    "Privacy/confidentiality concerns",
    "Legal/ethical uncertainties about AI use",
    "Hallucinations (confident, but fabricated or incorrect answers)",
]

PROBLEM_SHORT_LABELS = {
    "Solutions that are almost right, but not quite": "Solutions almost right, but not quite",
    "Difficulty in validating AI Chat Assistant-generated content": "Difficulty validating AI-generated content",
    "High variability in output quality": "High variability in output quality",
    "Difficulty adapting to project/team context": "Difficulty adapting to project/team context",
    "Lack of integration with existing tools": "Lack of integration with existing tools",
    "Over-dependence of the team on AI Chat Assistants": "Over-dependence of the team on AI",
    "Resistance from team members to adopt AI Chat Assistants": "Resistance from team members",
    "I've become less confident in my own problem-solving": "Less confidence in own problem-solving",
    "Privacy/confidentiality concerns": "Privacy/confidentiality concerns",
    "Legal/ethical uncertainties about AI use": "Legal/ethical uncertainties",
    "Hallucinations (confident, but fabricated or incorrect answers)": "Hallucinations",
}

ROLE_REPLACEMENT = [
    "No role replacement",
    "Yes, Product Owner",
    "Yes, Scrum Master",
    "Yes, Developers",
]

# -----------------------------------------------------------------------------
# Generic helpers
# -----------------------------------------------------------------------------


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def normalize_key(value: object) -> str:
    return normalize_text(value).lower()


def pct(count: int, denominator: int) -> float:
    return round((count / denominator) * 100, 1) if denominator else 0.0


def starts_with_yes(value: object) -> bool:
    return normalize_key(value).startswith("yes")


def safe_sheet_name(name: str) -> str:
    cleaned = re.sub(r"[\\/*?:\[\]]", "_", name)[:31]
    return cleaned or "Sheet"


def extract_bracket_label(column_name: str) -> str:
    match = re.search(r"\[(.*?)\]", column_name, flags=re.S)
    if match:
        return normalize_text(match.group(1))
    return normalize_text(column_name)


def compact_label(text: str, max_len: int = 90) -> str:
    text = normalize_text(text)
    return text if len(text) <= max_len else text[: max_len - 1] + "…"


def find_column(
    df: pd.DataFrame,
    required_fragments: Iterable[str],
    forbidden_fragments: Iterable[str] = (),
) -> str:
    required = [fragment.lower() for fragment in required_fragments]
    forbidden = [fragment.lower() for fragment in forbidden_fragments]
    matches = []
    for col in df.columns:
        simplified = re.sub(r"\s+", " ", str(col)).lower()
        if all(fragment in simplified for fragment in required) and not any(
            fragment in simplified for fragment in forbidden
        ):
            matches.append(col)
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one column for required={list(required_fragments)} forbidden={list(forbidden_fragments)}, "
            f"found {len(matches)}: {matches}"
        )
    return matches[0]


def find_columns(
    df: pd.DataFrame,
    required_fragments: Iterable[str],
    forbidden_fragments: Iterable[str] = (),
) -> List[str]:
    required = [fragment.lower() for fragment in required_fragments]
    forbidden = [fragment.lower() for fragment in forbidden_fragments]
    matches = []
    for col in df.columns:
        simplified = re.sub(r"\s+", " ", str(col)).lower()
        if all(fragment in simplified for fragment in required) and not any(
            fragment in simplified for fragment in forbidden
        ):
            matches.append(col)
    return matches


def categorical_table(
    series: pd.Series,
    denominator: int | None = None,
    order: Sequence[str] | None = None,
    aliases: Mapping[str, str] | None = None,
    include_missing: bool = False,
) -> pd.DataFrame:
    values: List[str] = []
    aliases = aliases or {}
    for value in series:
        label = normalize_text(value)
        if not label:
            if include_missing:
                values.append("Missing/No answer")
            continue
        values.append(aliases.get(label.lower(), label))

    denominator = len(series) if denominator is None else denominator
    counts = Counter(values)
    rows = []

    if order:
        seen = set()
        for label in order:
            seen.add(label)
            rows.append(
                {
                    "response": label,
                    "count": counts.get(label, 0),
                    "percent": pct(counts.get(label, 0), denominator),
                    "denominator": denominator,
                }
            )
        for label, count in counts.most_common():
            if label not in seen:
                rows.append(
                    {
                        "response": label,
                        "count": count,
                        "percent": pct(count, denominator),
                        "denominator": denominator,
                    }
                )
    else:
        for label, count in counts.most_common():
            rows.append(
                {
                    "response": label,
                    "count": count,
                    "percent": pct(count, denominator),
                    "denominator": denominator,
                }
            )

    return pd.DataFrame(rows, columns=["response", "count", "percent", "denominator"])


def parse_multiselect_by_options(
    value: object, options: Sequence[str]
) -> Tuple[set[str], str]:
    """
    Parse multi-select cells using canonical option substring matching, not comma splitting.
    This avoids errors when options themselves contain commas.
    """
    raw = normalize_text(value)
    if not raw:
        return set(), ""

    selected: set[str] = set()
    residual = raw
    for option in sorted(options, key=len, reverse=True):
        pattern = re.escape(option)
        if re.search(pattern, raw, flags=re.IGNORECASE):
            selected.add(option)
            residual = re.sub(pattern, "", residual, flags=re.IGNORECASE)

    # Clean separators and punctuation left after removing canonical options.
    residual = re.sub(r"\s*,\s*", ", ", residual)
    residual = re.sub(r"^(,\s*)+|(,\s*)+$", "", residual).strip()
    residual = re.sub(r"(,\s*){2,}", ", ", residual).strip()
    return selected, residual


def multiselect_table(
    series: pd.Series,
    options: Sequence[str],
    denominator: int,
    short_labels: Mapping[str, str] | None = None,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    short_labels = short_labels or {option: option for option in options}
    counter: Counter[str] = Counter()
    residual_counter: Counter[str] = Counter()
    rows_with_any_selection = 0

    for value in series:
        selected, residual = parse_multiselect_by_options(value, options)
        if selected or residual:
            rows_with_any_selection += 1
        counter.update(selected)
        if residual:
            residual_counter[residual] += 1

    rows = []
    for option in options:
        count = counter[option]
        rows.append(
            {
                "label": short_labels.get(option, option),
                "original_label": option,
                "count": count,
                "percent": pct(count, denominator),
                "denominator": denominator,
            }
        )
    table = (
        pd.DataFrame(rows)
        .sort_values(["count", "label"], ascending=[False, True])
        .reset_index(drop=True)
    )

    residual = pd.DataFrame(
        [
            {"other_or_unmatched_response": response, "count": count}
            for response, count in residual_counter.most_common()
        ]
    )
    return table, residual


def matrix_table(
    df: pd.DataFrame, columns: Sequence[str], denominator: int, category: str
) -> pd.DataFrame:
    rows = []
    for col in columns:
        label = extract_bracket_label(col)
        counts = Counter(normalize_text(v) for v in df[col] if normalize_text(v))
        current_mostly = counts.get("Currently Mostly AI Chat Assistant", 0)
        current_partially = counts.get("Currently Partially AI Chat Assistant", 0)
        plan_mostly = counts.get("Plan to Mostly Use AI Chat Assistant", 0)
        plan_partially = counts.get("Plan to Partially Use AI Chat Assistant", 0)
        dont_plan = counts.get("Don't Plan to Use AI Chat Assistant for This Task", 0)
        current_total = current_mostly + current_partially
        plan_total = plan_mostly + plan_partially
        rows.append(
            {
                "category": category,
                "activity": label,
                "currently_mostly_count": current_mostly,
                "currently_partially_count": current_partially,
                "current_total_count": current_total,
                "current_total_percent": pct(current_total, denominator),
                "plan_mostly_count": plan_mostly,
                "plan_partially_count": plan_partially,
                "plan_total_count": plan_total,
                "plan_total_percent": pct(plan_total, denominator),
                "dont_plan_count": dont_plan,
                "dont_plan_percent": pct(dont_plan, denominator),
                "denominator": denominator,
            }
        )
    return pd.DataFrame(rows)


def open_response_count(
    series: pd.Series, denominator: int, question: str
) -> Dict[str, object]:
    nonempty = series.apply(lambda x: bool(normalize_text(x))).sum()
    return {
        "question": question,
        "non_empty_count": int(nonempty),
        "percent": pct(int(nonempty), denominator),
        "denominator": denominator,
    }


def write_csv(
    output_dir: Path, name: str, table: pd.DataFrame, registry: Dict[str, pd.DataFrame]
) -> None:
    path = output_dir / f"{name}.csv"
    table.to_csv(path, index=False, encoding="utf-8")
    registry[name] = table


# -----------------------------------------------------------------------------
# Main analysis
# -----------------------------------------------------------------------------


def build_statistics(
    input_path: Path, output_dir: Path
) -> Tuple[Dict[str, pd.DataFrame], str]:
    df = pd.read_excel(input_path, engine="openpyxl")
    output_dir.mkdir(parents=True, exist_ok=True)
    tables: Dict[str, pd.DataFrame] = {}

    # Columns used in filtering
    consent_col = find_column(df, ["agree to participate"])
    scrum_exp_col = find_column(df, ["experience", "scrum projects"])
    worked_scrum_col = find_column(df, ["have you worked", "scrum initiative"])
    llm_use_col = find_column(
        df, ["last 6 months", "ai chat assistant", "scrum management"]
    )
    formality_col = find_column(
        df, ["how formally", "use ai chat assistants", "scrum management"]
    )

    total_submissions = len(df)
    consenting = df[df[consent_col].apply(starts_with_yes)].copy()
    non_consent = df[~df[consent_col].apply(starts_with_yes)].copy()
    scrum_experienced = consenting[
        consenting[scrum_exp_col].apply(lambda x: normalize_key(x) != "no experience")
    ].copy()
    no_scrum_experience = consenting[
        consenting[scrum_exp_col].apply(lambda x: normalize_key(x) == "no experience")
    ].copy()
    worked_scrum = scrum_experienced[
        scrum_experienced[worked_scrum_col].apply(starts_with_yes)
    ].copy()
    did_not_work_scrum = scrum_experienced[
        ~scrum_experienced[worked_scrum_col].apply(starts_with_yes)
    ].copy()
    llm_users_precheck = scrum_experienced[
        scrum_experienced[llm_use_col].apply(starts_with_yes)
    ].copy()
    llm_nonusers = scrum_experienced[
        ~scrum_experienced[llm_use_col].apply(starts_with_yes)
    ].copy()
    final_sample = llm_users_precheck[
        ~llm_users_precheck[formality_col].apply(
            lambda x: normalize_key(x).startswith(
                "i don't use llm in scrum-based activities"
            )
        )
    ].copy()
    consistency_excluded = llm_users_precheck[
        llm_users_precheck[formality_col].apply(
            lambda x: normalize_key(x).startswith(
                "i don't use llm in scrum-based activities"
            )
        )
    ].copy()

    N_consenting = len(consenting)
    N_scrum = len(scrum_experienced)
    N_worked = len(worked_scrum)
    N_precheck = len(llm_users_precheck)
    N_final = len(final_sample)

    pipeline = pd.DataFrame(
        [
            {
                "step": "Survey submissions",
                "n_remaining": total_submissions,
                "n_removed_at_step": "",
                "basis": "All rows in spreadsheet",
            },
            {
                "step": "Consenting responses",
                "n_remaining": len(consenting),
                "n_removed_at_step": len(non_consent),
                "basis": "Agreed to participate",
            },
            {
                "step": "Responses with Scrum experience",
                "n_remaining": len(scrum_experienced),
                "n_removed_at_step": len(no_scrum_experience),
                "basis": "Scrum experience answer is not 'No experience'",
            },
            {
                "step": "Reported having worked in a Scrum initiative/project",
                "n_remaining": len(worked_scrum),
                "n_removed_at_step": len(did_not_work_scrum),
                "basis": "Answered yes to having worked in a Scrum initiative/project",
            },
            {
                "step": "Reported LLM use for Scrum in last 6 months",
                "n_remaining": len(llm_users_precheck),
                "n_removed_at_step": len(llm_nonusers),
                "basis": "Answered yes to LLM use for Scrum management work",
            },
            {
                "step": "Final analytic sample",
                "n_remaining": len(final_sample),
                "n_removed_at_step": len(consistency_excluded),
                "basis": "Excluded contradictory formality answers: 'I don't use LLM in Scrum-based activities'",
            },
        ]
    )
    write_csv(output_dir, "00_filtering_pipeline", pipeline, tables)

    # Demographics/background - export for multiple scopes so manuscript can choose defensible denominator.
    profile_cols = {
        "country": find_column(df, ["country", "currently work"]),
        "age_group": find_column(df, ["age group"]),
        "academic_education": find_column(df, ["academic education"]),
        "scrum_knowledge": find_column(df, ["knowledge level", "scrum"]),
        "scrum_experience_years": scrum_exp_col,
    }
    scopes = {
        "consenting_N158": consenting,
        "scrum_experienced_N128": scrum_experienced,
        "worked_scrum_N111": worked_scrum,
        "final_analytic_N79": final_sample,
    }
    for scope_name, scope_df in scopes.items():
        for short_name, col in profile_cols.items():
            table = categorical_table(
                scope_df[col], denominator=len(scope_df), include_missing=False
            )
            table.insert(0, "scope", scope_name)
            table.insert(1, "variable", short_name)
            write_csv(
                output_dir, f"01_profile_{scope_name}_{short_name}", table, tables
            )

    # Organization and project profile.
    org_project_cols = {
        "organization_industry": find_column(df, ["organization", "main industry"]),
        "organization_size": find_column(df, ["size of the organization"]),
        "worked_scrum_initiative": worked_scrum_col,
        "primary_role": find_column(df, ["primary role", "scrum team"]),
        "application_domain": find_column(df, ["main application domain"]),
        "problem_domain": find_column(df, ["main problem domain"]),
        "scrum_team_size": find_column(df, ["how many members", "scrum team"]),
        "product_duration": find_column(df, ["how long", "product"]),
    }
    for scope_name, scope_df in {
        "scrum_experienced_N128": scrum_experienced,
        "worked_scrum_N111": worked_scrum,
        "final_analytic_N79": final_sample,
    }.items():
        for short_name, col in org_project_cols.items():
            table = categorical_table(
                scope_df[col], denominator=len(scope_df), include_missing=False
            )
            table.insert(0, "scope", scope_name)
            table.insert(1, "variable", short_name)
            write_csv(
                output_dir, f"02_org_project_{scope_name}_{short_name}", table, tables
            )

    # RQ1: LLM knowledge and usage.
    rq1_cols = {
        "llm_use_last_6_months": llm_use_col,
        "frequency": find_column(df, ["how often", "ai chat assistants"]),
        "llm_knowledge": find_column(df, ["knowledge level", "ai chat assistants"]),
        "formal_policy": find_column(df, ["formal policy", "ai chat assistants"]),
        "formality_of_use": formality_col,
        "time_per_day": find_column(df, ["time per day", "scrum management"]),
    }
    # RQ1 main stats over final sample, plus non-user screening over Scrum-experienced respondents.
    for short_name, col in rq1_cols.items():
        scope_df = (
            scrum_experienced if short_name == "llm_use_last_6_months" else final_sample
        )
        table = categorical_table(
            scope_df[col], denominator=len(scope_df), include_missing=False
        )
        table.insert(
            0,
            "scope",
            "scrum_experienced_N128"
            if short_name == "llm_use_last_6_months"
            else "final_analytic_N79",
        )
        table.insert(1, "variable", short_name)
        write_csv(output_dir, f"03_rq1_{short_name}", table, tables)

    ai_tools_col = find_column(df, ["which ai chat assistants"])
    tools_table, tools_other = multiselect_table(
        final_sample[ai_tools_col], AI_TOOLS, N_final
    )
    write_csv(output_dir, "03_rq1_ai_tools", tools_table, tables)
    write_csv(output_dir, "03_rq1_ai_tools_other_unmatched", tools_other, tables)

    interaction_col = find_column(df, ["usually interact", "ai chat assistants"])
    interaction_table, interaction_other = multiselect_table(
        final_sample[interaction_col], INTERACTION_MODES, N_final
    )
    write_csv(output_dir, "03_rq1_interaction_modes", interaction_table, tables)
    write_csv(
        output_dir,
        "03_rq1_interaction_modes_other_unmatched",
        interaction_other,
        tables,
    )

    # Model text responses: exact frequencies can be noisy but still useful for auditing.
    models_col = find_column(df, ["which model", "assistant uses"])
    model_table = categorical_table(
        final_sample[models_col], denominator=N_final, include_missing=False
    )
    write_csv(output_dir, "03_rq1_model_free_text_frequencies", model_table, tables)

    # RQ2 matrices.
    learning_cols = find_columns(df, ["learn, explore", "related to scrum", "["])
    artifact_cols = find_columns(df, ["scrum artifacts", "["])
    event_cols = find_columns(df, ["scrum events", "["])
    management_cols = find_columns(df, ["other agile management tasks", "["])

    # Remove accidental columns outside the matrices if any.
    learning_cols = [c for c in learning_cols if c in df.columns and c.index(c) >= 0]
    artifact_cols = [
        c
        for c in artifact_cols
        if "In WHAT WAYS do you use" in c and "SCRUM ARTIFACTS" in c
    ]
    event_cols = [
        c for c in event_cols if "In WHAT WAYS do you use" in c and "SCRUM EVENTS" in c
    ]
    management_cols = [
        c
        for c in management_cols
        if "In WHAT WAYS do you use" in c and "OTHER AGILE MANAGEMENT TASKS" in c
    ]

    rq2_matrix = pd.concat(
        [
            matrix_table(
                final_sample,
                learning_cols,
                N_final,
                "Exploring and learning Scrum practices",
            ),
            matrix_table(final_sample, artifact_cols, N_final, "Scrum artifacts"),
            matrix_table(final_sample, event_cols, N_final, "Scrum events"),
            matrix_table(
                final_sample, management_cols, N_final, "Other agile management tasks"
            ),
        ],
        ignore_index=True,
    )
    write_csv(output_dir, "04_rq2_adoption_matrix_all_activities", rq2_matrix, tables)
    write_csv(
        output_dir,
        "04_rq2_top_current_use",
        rq2_matrix.sort_values(
            ["current_total_count", "activity"], ascending=[False, True]
        ).head(25),
        tables,
    )
    write_csv(
        output_dir,
        "04_rq2_top_planned_use",
        rq2_matrix.sort_values(
            ["plan_total_count", "activity"], ascending=[False, True]
        ).head(25),
        tables,
    )
    write_csv(
        output_dir,
        "04_rq2_top_dont_plan",
        rq2_matrix.sort_values(
            ["dont_plan_count", "activity"], ascending=[False, True]
        ).head(25),
        tables,
    )

    # Other/open counts for RQ2.
    open_questions = []
    for fragments, label in [
        (["other task", "learning", "scrum"], "RQ2 other learning/exploring task"),
        (
            ["example prompts", "scrum artifacts"],
            "RQ2 example prompts for Scrum artifacts",
        ),
        (["other task", "scrum artifacts"], "RQ2 other artifact task"),
        (["example prompts", "scrum events"], "RQ2 example prompts for Scrum events"),
        (["other task", "scrum events"], "RQ2 other event task"),
        (
            ["example prompts", "other agile management"],
            "RQ2 example prompts for other management tasks",
        ),
        (["other task", "other agile management"], "RQ2 other management task"),
    ]:
        cols = find_columns(df, fragments)
        if cols:
            open_questions.append(
                open_response_count(final_sample[cols[0]], N_final, label)
            )
    open_counts = pd.DataFrame(open_questions)
    write_csv(output_dir, "04_rq2_open_response_counts", open_counts, tables)

    # RQ3: Helpfulness, benefits, agreement.
    helpfulness_cols = find_columns(df, ["helpful", "scrum accountabilities"])
    helpful_rows = []
    for col in helpfulness_cols:
        role = extract_bracket_label(col)
        table = categorical_table(
            final_sample[col],
            denominator=N_final,
            order=RESPONSE_ORDER_HELPFULNESS,
            aliases=HELPFULNESS_ALIASES,
        )
        for _, row in table.iterrows():
            helpful_rows.append({"role": role, **row.to_dict()})
    helpfulness_table = pd.DataFrame(helpful_rows)
    write_csv(
        output_dir,
        "05_rq3_helpfulness_by_scrum_accountability",
        helpfulness_table,
        tables,
    )

    benefits_col = find_column(df, ["what benefits", "scrum management tasks"])
    benefit_table, benefit_other = multiselect_table(
        final_sample[benefits_col], BENEFITS, N_final, BENEFIT_SHORT_LABELS
    )
    write_csv(output_dir, "05_rq3_benefits_experienced", benefit_table, tables)
    write_csv(output_dir, "05_rq3_benefits_other_unmatched", benefit_other, tables)

    efficiency_col = find_column(df, ["help you perform", "more efficiently"])
    efficiency_table = categorical_table(
        final_sample[efficiency_col], denominator=N_final, include_missing=False
    )
    write_csv(output_dir, "05_rq3_efficiency_general_item", efficiency_table, tables)

    benefit_agreement_cols = find_columns(df, ["benefits of ai chat assistants", "["])
    benefit_agreement_rows = []
    for col in benefit_agreement_cols:
        statement = extract_bracket_label(col)
        table = categorical_table(
            final_sample[col],
            denominator=N_final,
            order=AGREEMENT_ORDER,
            aliases=AGREEMENT_ALIASES,
        )
        for _, row in table.iterrows():
            benefit_agreement_rows.append({"statement": statement, **row.to_dict()})
    benefit_agreement = pd.DataFrame(benefit_agreement_rows)
    write_csv(output_dir, "05_rq3_benefit_agreement_items", benefit_agreement, tables)

    positive_col = find_column(df, ["positive example"])
    write_csv(
        output_dir,
        "05_rq3_positive_example_count",
        pd.DataFrame(
            [
                open_response_count(
                    final_sample[positive_col],
                    N_final,
                    "Positive examples of using AI Chat Assistants",
                )
            ]
        ),
        tables,
    )

    # RQ4: problems and downside/risk perceptions.
    problems_col = find_column(df, ["problems or frustations", "encountered"])
    problem_table, problem_other = multiselect_table(
        final_sample[problems_col], PROBLEMS, N_final, PROBLEM_SHORT_LABELS
    )
    write_csv(output_dir, "06_rq4_problems_encountered", problem_table, tables)
    write_csv(output_dir, "06_rq4_problems_other_unmatched", problem_other, tables)

    biggest_risk_col = find_column(df, ["biggest risk"])
    write_csv(
        output_dir,
        "06_rq4_biggest_risk_open_count",
        pd.DataFrame(
            [
                open_response_count(
                    final_sample[biggest_risk_col],
                    N_final,
                    "Biggest risk open-ended responses",
                )
            ]
        ),
        tables,
    )

    intensive_cols = find_columns(df, ["intensive use", "could cause", "["])
    intensive_rows = []
    for col in intensive_cols:
        risk = extract_bracket_label(col)
        table = categorical_table(
            final_sample[col],
            denominator=N_final,
            order=AGREEMENT_ORDER,
            aliases=AGREEMENT_ALIASES,
        )
        for _, row in table.iterrows():
            intensive_rows.append({"risk": risk, **row.to_dict()})
    intensive_table = pd.DataFrame(intensive_rows)
    write_csv(output_dir, "06_rq4_intensive_use_could_cause", intensive_table, tables)

    negative_col = find_column(df, ["negative example"])
    write_csv(
        output_dir,
        "06_rq4_negative_example_count",
        pd.DataFrame(
            [
                open_response_count(
                    final_sample[negative_col],
                    N_final,
                    "Negative examples of using AI Chat Assistants",
                )
            ]
        ),
        tables,
    )

    rarely_col = find_column(df, ["rarely help improve", "efficiency"])
    rarely_table = categorical_table(
        final_sample[rarely_col], denominator=N_final, include_missing=False
    )
    write_csv(output_dir, "06_rq4_rarely_help_efficiency_item", rarely_table, tables)

    # RQ5: future perspectives.
    future_rel_col = find_column(
        df, ["relationship between humans and ai", "scrum management"]
    )
    future_rel = categorical_table(
        final_sample[future_rel_col], denominator=N_final, include_missing=False
    )
    write_csv(output_dir, "07_rq5_future_human_ai_relationship", future_rel, tables)

    replacement_col = find_column(df, ["replace", "scrum accountabilities"])
    replacement_table, replacement_other = multiselect_table(
        final_sample[replacement_col], ROLE_REPLACEMENT, N_final
    )
    write_csv(output_dir, "07_rq5_role_replacement", replacement_table, tables)
    write_csv(
        output_dir, "07_rq5_role_replacement_other_unmatched", replacement_other, tables
    )

    skills_col = find_column(df, ["new skills", "collaborate with ai"])
    write_csv(
        output_dir,
        "07_rq5_new_skills_open_count",
        pd.DataFrame(
            [
                open_response_count(
                    final_sample[skills_col], N_final, "New skills open-ended responses"
                )
            ]
        ),
        tables,
    )

    comments_col = find_column(df, ["further comments", "suggestions"])
    write_csv(
        output_dir,
        "08_general_comments_open_count",
        pd.DataFrame(
            [
                open_response_count(
                    final_sample[comments_col],
                    N_final,
                    "Further comments, suggestions, or examples",
                )
            ]
        ),
        tables,
    )

    # Optional consistency checks.
    checks = pd.DataFrame(
        [
            {
                "check": "N_final_expected_79",
                "value": N_final,
                "status": "OK" if N_final == 79 else "CHECK",
            },
            {
                "check": "N_precheck_expected_81",
                "value": N_precheck,
                "status": "OK" if N_precheck == 81 else "CHECK",
            },
            {
                "check": "N_scrum_expected_128",
                "value": N_scrum,
                "status": "OK" if N_scrum == 128 else "CHECK",
            },
            {
                "check": "N_consenting_expected_158",
                "value": N_consenting,
                "status": "OK" if N_consenting == 158 else "CHECK",
            },
            {
                "check": "N_worked_scrum_expected_111",
                "value": N_worked,
                "status": "OK" if N_worked == 111 else "CHECK",
            },
        ]
    )
    write_csv(output_dir, "99_consistency_checks", checks, tables)

    report = build_markdown_report(tables, input_path, output_dir)
    (output_dir / "descriptive_statistics_report.md").write_text(
        report, encoding="utf-8"
    )

    # Excel workbook with all tables in separate sheets for easier inspection.
    excel_path = output_dir / "descriptive_statistics_tables.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        for name, table in tables.items():
            table.to_excel(writer, index=False, sheet_name=safe_sheet_name(name))

    return tables, report


# -----------------------------------------------------------------------------
# Markdown report
# -----------------------------------------------------------------------------


def md_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    if df.empty:
        return "_No rows._"
    display_df = df.head(max_rows).copy()
    lines = []
    lines.append("| " + " | ".join(str(c) for c in display_df.columns) + " |")
    lines.append("| " + " | ".join("---" for _ in display_df.columns) + " |")
    for _, row in display_df.iterrows():
        values = [str(row[c]).replace("|", "\\|") for c in display_df.columns]
        lines.append("| " + " | ".join(values) + " |")
    if len(df) > max_rows:
        lines.append(f"\n_Showing {max_rows} of {len(df)} rows._")
    return "\n".join(lines)


def build_markdown_report(
    tables: Mapping[str, pd.DataFrame], input_path: Path, output_dir: Path
) -> str:
    lines: List[str] = []
    lines.append("# Deterministic descriptive statistics report")
    lines.append("")
    lines.append(f"Input file: `{input_path.name}`")
    lines.append(f"Output directory: `{output_dir}`")
    lines.append("")
    lines.append("## Filtering pipeline")
    lines.append(md_table(tables["00_filtering_pipeline"], max_rows=10))
    lines.append("")
    lines.append("## Consistency checks")
    lines.append(md_table(tables["99_consistency_checks"], max_rows=10))
    lines.append("")

    def add_section(title: str, table_name: str, max_rows: int = 20) -> None:
        if table_name in tables:
            lines.append(f"## {title}")
            lines.append(md_table(tables[table_name], max_rows=max_rows))
            lines.append("")

    add_section("RQ1 — Frequency of LLM use for Scrum management", "03_rq1_frequency")
    add_section("RQ1 — LLM knowledge", "03_rq1_llm_knowledge")
    add_section("RQ1 — Formal policy", "03_rq1_formal_policy")
    add_section("RQ1 — Formality of use", "03_rq1_formality_of_use")
    add_section("RQ1 — Time per day", "03_rq1_time_per_day")
    add_section("RQ1 — AI tools", "03_rq1_ai_tools")
    add_section("RQ1 — Interaction modes", "03_rq1_interaction_modes")
    add_section(
        "RQ2 — Top current-use activities", "04_rq2_top_current_use", max_rows=15
    )
    add_section(
        "RQ2 — Top planned-use activities", "04_rq2_top_planned_use", max_rows=15
    )
    add_section("RQ2 — Top don't-plan activities", "04_rq2_top_dont_plan", max_rows=15)
    add_section(
        "RQ3 — Helpfulness by Scrum accountability",
        "05_rq3_helpfulness_by_scrum_accountability",
        max_rows=20,
    )
    add_section("RQ3 — Benefits experienced", "05_rq3_benefits_experienced")
    add_section(
        "RQ3 — Benefit agreement items", "05_rq3_benefit_agreement_items", max_rows=30
    )
    add_section("RQ4 — Problems encountered", "06_rq4_problems_encountered")
    add_section(
        "RQ4 — Intensive use could cause",
        "06_rq4_intensive_use_could_cause",
        max_rows=20,
    )
    add_section(
        "RQ5 — Future human-AI relationship", "07_rq5_future_human_ai_relationship"
    )
    add_section(
        "RQ5 — Potential replacement of Scrum accountabilities",
        "07_rq5_role_replacement",
    )
    lines.append("## Generated CSV tables")
    for name in sorted(tables):
        lines.append(f"- `{name}.csv`")
    lines.append("")
    lines.append("## Notes")
    lines.append(
        "- Multi-select questions are parsed using canonical option matching, not comma splitting."
    )
    lines.append("- Percentages use the denominator shown in each table.")
    lines.append(
        "- The main LLM-in-Scrum analyses use the final analytic sample (N = 79)."
    )
    lines.append(
        "- Broader profile tables are exported separately for transparency, but should not be mixed with N = 79 results unless explicitly explained."
    )
    return "\n".join(lines)


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate deterministic descriptive statistics for the LLM-in-Scrum survey."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Path to merged_survey_data.xlsx",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for generated reports/tables",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables, _ = build_statistics(args.input, args.output_dir)
    checks = tables["99_consistency_checks"]
    print("Done.")
    print(checks.to_string(index=False))
    print(f"Report: {args.output_dir / 'descriptive_statistics_report.md'}")
    print(f"Workbook: {args.output_dir / 'descriptive_statistics_tables.xlsx'}")


if __name__ == "__main__":
    main()
