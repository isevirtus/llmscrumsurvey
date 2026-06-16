# Deterministic descriptive statistics report

Input file: `merged_survey_data.xlsx`
Output directory: `/mnt/data/reports_full_v5`

## Filtering pipeline
| step | n_remaining | n_removed_at_step | basis |
| --- | --- | --- | --- |
| Survey submissions | 159 |  | All rows in spreadsheet |
| Consenting responses | 158 | 1 | Agreed to participate |
| Responses with Scrum experience | 128 | 30 | Scrum experience answer is not 'No experience' |
| Reported having worked in a Scrum initiative/project | 111 | 17 | Answered yes to having worked in a Scrum initiative/project |
| Reported LLM use for Scrum in last 6 months | 81 | 47 | Answered yes to LLM use for Scrum management work |
| Final analytic sample | 79 | 2 | Excluded contradictory formality answers: 'I don't use LLM in Scrum-based activities' |

## Consistency checks
| check | value | status |
| --- | --- | --- |
| N_final_expected_79 | 79 | OK |
| N_precheck_expected_81 | 81 | OK |
| N_scrum_expected_128 | 128 | OK |
| N_consenting_expected_158 | 158 | OK |
| N_worked_scrum_expected_111 | 111 | OK |

## RQ1 — Frequency of LLM use for Scrum management
| scope | variable | response | count | percent | denominator |
| --- | --- | --- | --- | --- | --- |
| final_analytic_N79 | frequency | Daily or almost daily | 38 | 48.1 | 79 |
| final_analytic_N79 | frequency | Weekly | 19 | 24.1 | 79 |
| final_analytic_N79 | frequency | Occasionally (less than once a month) | 12 | 15.2 | 79 |
| final_analytic_N79 | frequency | Monthly | 9 | 11.4 | 79 |
| final_analytic_N79 | frequency | Never | 1 | 1.3 | 79 |

## RQ1 — LLM knowledge
| scope | variable | response | count | percent | denominator |
| --- | --- | --- | --- | --- | --- |
| final_analytic_N79 | llm_knowledge | Qualified – Good conceptual knowledge and practical experience with AI Chat Assistants in professional tasks. | 43 | 54.4 | 79 |
| final_analytic_N79 | llm_knowledge | Proficient – In-depth conceptual understanding and extensive practical experience with AI Chat Assistants, often integrated into workflows. | 18 | 22.8 | 79 |
| final_analytic_N79 | llm_knowledge | Beginner – Knowledge of the main applications of AI Chat Assistants, occasional use in practice. | 15 | 19.0 | 79 |
| final_analytic_N79 | llm_knowledge | Specialist – Advanced conceptual knowledge and deep practical expertise, capable of guiding others in the professional use of AI Chat Assistants. | 2 | 2.5 | 79 |
| final_analytic_N79 | llm_knowledge | Novice – Minimum or conceptual knowledge without relevant practical experience. | 1 | 1.3 | 79 |

## RQ1 — Formal policy
| scope | variable | response | count | percent | denominator |
| --- | --- | --- | --- | --- | --- |
| final_analytic_N79 | formal_policy | YES, there is a formal and documented policy. | 34 | 43.0 | 79 |
| final_analytic_N79 | formal_policy | NO, there is no policy or guideline. | 19 | 24.1 | 79 |
| final_analytic_N79 | formal_policy | YES, but the policy is informal or not widely documented. | 11 | 13.9 | 79 |
| final_analytic_N79 | formal_policy | NO, but discussions about creating one are in progress. | 11 | 13.9 | 79 |
| final_analytic_N79 | formal_policy | I don’t know / Not sure. | 4 | 5.1 | 79 |

## RQ1 — Formality of use
| scope | variable | response | count | percent | denominator |
| --- | --- | --- | --- | --- | --- |
| final_analytic_N79 | formality_of_use | INFORMALLY (without a prescribed process for carrying out the activity). | 45 | 57.0 | 79 |
| final_analytic_N79 | formality_of_use | FORMALLY (with a prescribed process for carrying out the activity). | 34 | 43.0 | 79 |

## RQ1 — Time per day
| scope | variable | response | count | percent | denominator |
| --- | --- | --- | --- | --- | --- |
| final_analytic_N79 | time_per_day | 1–2 hours | 40 | 50.6 | 79 |
| final_analytic_N79 | time_per_day | < 1 hour | 34 | 43.0 | 79 |
| final_analytic_N79 | time_per_day | 3–4 hours | 5 | 6.3 | 79 |

## RQ1 — AI tools
| label | original_label | count | percent | denominator |
| --- | --- | --- | --- | --- |
| ChatGPT (OpenAI) | ChatGPT (OpenAI) | 68 | 86.1 | 79 |
| Gemini (Google) | Gemini (Google) | 48 | 60.8 | 79 |
| Copilot Chat (Microsoft) | Copilot Chat (Microsoft) | 47 | 59.5 | 79 |
| Claude (Anthropic) | Claude (Anthropic) | 20 | 25.3 | 79 |
| DeepSeek Chat | DeepSeek Chat | 16 | 20.3 | 79 |
| A proprietary or internal AI Chat Assistant developed or customized by your organization | A proprietary or internal AI Chat Assistant developed or customized by your organization | 11 | 13.9 | 79 |
| Perplexity AI | Perplexity AI | 8 | 10.1 | 79 |
| Mistral Le Chat | Mistral Le Chat | 3 | 3.8 | 79 |

## RQ1 — Interaction modes
| label | original_label | count | percent | denominator |
| --- | --- | --- | --- | --- |
| Text (typing or copy-pasting prompts) | Text (typing or copy-pasting prompts) | 79 | 100.0 | 79 |
| Files or documents (e.g., uploading PDFs, code files) | Files or documents (e.g., uploading PDFs, code files) | 59 | 74.7 | 79 |
| Images or screenshots (e.g., sharing a burndown chart) | Images or screenshots (e.g., sharing a burndown chart) | 46 | 58.2 | 79 |
| Technical implementation tasks (e.g., writing/explaining/debugging code; generating tests, scripts, and config files; CI/CD & Infrastructure-as-Code; crafting queries/API calls; refactoring/performance/security hardening) (excludes inline autocomplete tools) | Technical implementation tasks (e.g., writing/explaining/debugging code; generating tests, scripts, and config files; CI/CD & Infrastructure-as-Code; crafting queries/API calls; refactoring/performance/security hardening) (excludes inline autocomplete tools) | 40 | 50.6 | 79 |
| Voice (speaking or dictation) | Voice (speaking or dictation) | 16 | 20.3 | 79 |

## RQ2 — Top current-use activities
| category | activity | currently_mostly_count | currently_partially_count | current_total_count | current_total_percent | plan_mostly_count | plan_partially_count | plan_total_count | plan_total_percent | dont_plan_count | dont_plan_percent | denominator |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Scrum artifacts | Improve the description of a Product Backlog item | 22 | 27 | 49 | 62.0 | 12 | 15 | 27 | 34.2 | 3 | 3.8 | 79 |
| Scrum events | Summarize what happened during an Event (e.g., Sprint Review, Sprint Planning, Sprint Retrospective) given notes, audio recordings, or video recordings | 21 | 26 | 47 | 59.5 | 12 | 12 | 24 | 30.4 | 8 | 10.1 | 79 |
| Exploring and learning Scrum practices | Explore practices and techniques (e.g., estimation methods, refinement approaches, facilitation patterns.) | 13 | 33 | 46 | 58.2 | 8 | 17 | 25 | 31.6 | 8 | 10.1 | 79 |
| Exploring and learning Scrum practices | Get practical resources and examples (e.g., recommended tools, sample templates, or checklists to implement practices.) | 18 | 27 | 45 | 57.0 | 10 | 18 | 28 | 35.4 | 6 | 7.6 | 79 |
| Exploring and learning Scrum practices | Clarify Scrum concepts and roles (e.g., understanding Sprint events, accountabilities, or artifacts.) | 21 | 23 | 44 | 55.7 | 6 | 16 | 22 | 27.8 | 13 | 16.5 | 79 |
| Scrum artifacts | Define candidate non-functional requirements | 16 | 28 | 44 | 55.7 | 8 | 15 | 23 | 29.1 | 12 | 15.2 | 79 |
| Scrum events | Summarize Sprint Review stakeholder feedback and follow-up actions | 18 | 26 | 44 | 55.7 | 11 | 14 | 25 | 31.6 | 10 | 12.7 | 79 |
| Scrum artifacts | Improve the acceptance criteria of a Product Backlog item | 22 | 21 | 43 | 54.4 | 12 | 18 | 30 | 38.0 | 6 | 7.6 | 79 |
| Scrum events | Design the event agenda (i.e., the sequence of activities and minutes per activity) and timeboxes for Sprint events (e.g., Sprint Review, Sprint Planning, Sprint Retrospective) | 15 | 26 | 41 | 51.9 | 6 | 18 | 24 | 30.4 | 14 | 17.7 | 79 |
| Scrum artifacts | Define the acceptance criteria for a Product Backlog item | 22 | 18 | 40 | 50.6 | 13 | 16 | 29 | 36.7 | 10 | 12.7 | 79 |
| Scrum artifacts | Evaluate the quality of a Product Backlog item description | 14 | 26 | 40 | 50.6 | 17 | 14 | 31 | 39.2 | 8 | 10.1 | 79 |
| Other agile management tasks | Summarize key risks for stakeholders | 15 | 25 | 40 | 50.6 | 8 | 18 | 26 | 32.9 | 13 | 16.5 | 79 |
| Other agile management tasks | Identify possible mitigation strategies for risk items | 12 | 27 | 39 | 49.4 | 7 | 18 | 25 | 31.6 | 15 | 19.0 | 79 |
| Scrum artifacts | Improve the Definition of Done criteria | 17 | 22 | 39 | 49.4 | 12 | 16 | 28 | 35.4 | 12 | 15.2 | 79 |
| Other agile management tasks | Improve the product vision | 14 | 25 | 39 | 49.4 | 8 | 16 | 24 | 30.4 | 16 | 20.3 | 79 |

_Showing 15 of 25 rows._

## RQ2 — Top planned-use activities
| category | activity | currently_mostly_count | currently_partially_count | current_total_count | current_total_percent | plan_mostly_count | plan_partially_count | plan_total_count | plan_total_percent | dont_plan_count | dont_plan_percent | denominator |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Other agile management tasks | Evaluate the quality of a product roadmap | 10 | 15 | 25 | 31.6 | 10 | 27 | 37 | 46.8 | 17 | 21.5 | 79 |
| Scrum artifacts | Identify dependencies within a Product Backlog | 14 | 16 | 30 | 38.0 | 14 | 22 | 36 | 45.6 | 13 | 16.5 | 79 |
| Scrum events | Identify recurring themes or impediments from event notes | 13 | 14 | 27 | 34.2 | 7 | 28 | 35 | 44.3 | 17 | 21.5 | 79 |
| Other agile management tasks | Improve the product roadmap | 11 | 22 | 33 | 41.8 | 13 | 21 | 34 | 43.0 | 12 | 15.2 | 79 |
| Scrum artifacts | Define how to split Product Backlog items to fit a Sprint | 12 | 18 | 30 | 38.0 | 13 | 20 | 33 | 41.8 | 16 | 20.3 | 79 |
| Scrum artifacts | Define the Definition of Done criteria | 13 | 16 | 29 | 36.7 | 12 | 21 | 33 | 41.8 | 17 | 21.5 | 79 |
| Scrum artifacts | Define the next Product Goal | 11 | 15 | 26 | 32.9 | 10 | 23 | 33 | 41.8 | 20 | 25.3 | 79 |
| Scrum artifacts | Define the technical tasks for a Product Backlog item (i.e., decompose the Product Backlog item into smaller work items) | 17 | 17 | 34 | 43.0 | 15 | 18 | 33 | 41.8 | 12 | 15.2 | 79 |
| Scrum artifacts | Improve the Product Goal (according to the team’s criteria or commonly accepted best practices) | 14 | 16 | 30 | 38.0 | 15 | 18 | 33 | 41.8 | 16 | 20.3 | 79 |
| Exploring and learning Scrum practices | Simulate conversations to coach or mentor team members – e.g., helping a developer or Product Owner adopt Scrum values, improve backlog management, or grow in their role. | 8 | 22 | 30 | 38.0 | 11 | 22 | 33 | 41.8 | 16 | 20.3 | 79 |
| Scrum events | Capture/Identify action items and owners of Events (e.g., Sprint Review, Sprint Planning, Sprint Retrospective) | 15 | 20 | 35 | 44.3 | 12 | 20 | 32 | 40.5 | 12 | 15.2 | 79 |
| Scrum artifacts | Estimate the value (e.g., ROI, desirability, cost of delay) of a Product Backlog item | 12 | 18 | 30 | 38.0 | 11 | 21 | 32 | 40.5 | 17 | 21.5 | 79 |
| Other agile management tasks | Summarize impediment data (e.g., count, status, owner, resolution progress) into a concise report. | 9 | 21 | 30 | 38.0 | 9 | 23 | 32 | 40.5 | 17 | 21.5 | 79 |
| Other agile management tasks | Define corrective actions (e.g., limit WIP, improve QA, breakdown items, start a spike) given metrics analysis (e.g., velocity, burndown) | 12 | 17 | 29 | 36.7 | 10 | 21 | 31 | 39.2 | 19 | 24.1 | 79 |
| Scrum artifacts | Evaluate the quality of a Product Backlog item description | 14 | 26 | 40 | 50.6 | 17 | 14 | 31 | 39.2 | 8 | 10.1 | 79 |

_Showing 15 of 25 rows._

## RQ2 — Top don't-plan activities
| category | activity | currently_mostly_count | currently_partially_count | current_total_count | current_total_percent | plan_mostly_count | plan_partially_count | plan_total_count | plan_total_percent | dont_plan_count | dont_plan_percent | denominator |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Other agile management tasks | Define the team working agreement | 11 | 17 | 28 | 35.4 | 5 | 20 | 25 | 31.6 | 26 | 32.9 | 79 |
| Scrum artifacts | Define the Sprint Goal of a target Sprint | 13 | 16 | 29 | 36.7 | 12 | 15 | 27 | 34.2 | 23 | 29.1 | 79 |
| Scrum artifacts | Evaluate the quality of a Product Goal (according to the team’s criteria or commonly accepted best practices) | 12 | 15 | 27 | 34.2 | 15 | 15 | 30 | 38.0 | 22 | 27.8 | 79 |
| Other agile management tasks | Interpret burndown, burnup, or CFD charts | 11 | 19 | 30 | 38.0 | 6 | 21 | 27 | 34.2 | 22 | 27.8 | 79 |
| Scrum artifacts | Define the next Product Goal | 11 | 15 | 26 | 32.9 | 10 | 23 | 33 | 41.8 | 20 | 25.3 | 79 |
| Other agile management tasks | Describe the product vision | 13 | 18 | 31 | 39.2 | 6 | 22 | 28 | 35.4 | 20 | 25.3 | 79 |
| Scrum artifacts | Estimate technical task effort/size | 12 | 18 | 30 | 38.0 | 13 | 16 | 29 | 36.7 | 20 | 25.3 | 79 |
| Scrum artifacts | Evaluate the quality of a Sprint Goal (according to the team’s criteria or commonly accepted best practices) | 15 | 14 | 29 | 36.7 | 11 | 19 | 30 | 38.0 | 20 | 25.3 | 79 |
| Other agile management tasks | Define corrective actions (e.g., limit WIP, improve QA, breakdown items, start a spike) given metrics analysis (e.g., velocity, burndown) | 12 | 17 | 29 | 36.7 | 10 | 21 | 31 | 39.2 | 19 | 24.1 | 79 |
| Other agile management tasks | Define possible impediment mitigation options | 11 | 22 | 33 | 41.8 | 4 | 24 | 28 | 35.4 | 18 | 22.8 | 79 |
| Scrum artifacts | Estimate effort/size (e.g., story point, ideal hours, t-shirt sizing) of a Product Backlog item | 9 | 22 | 31 | 39.2 | 13 | 17 | 30 | 38.0 | 18 | 22.8 | 79 |
| Scrum artifacts | Improve the Sprint Goal (according to the team’s criteria or commonly accepted best practices) | 16 | 16 | 32 | 40.5 | 14 | 15 | 29 | 36.7 | 18 | 22.8 | 79 |
| Scrum artifacts | Define the Definition of Done criteria | 13 | 16 | 29 | 36.7 | 12 | 21 | 33 | 41.8 | 17 | 21.5 | 79 |
| Scrum artifacts | Estimate the value (e.g., ROI, desirability, cost of delay) of a Product Backlog item | 12 | 18 | 30 | 38.0 | 11 | 21 | 32 | 40.5 | 17 | 21.5 | 79 |
| Other agile management tasks | Evaluate the quality of a product roadmap | 10 | 15 | 25 | 31.6 | 10 | 27 | 37 | 46.8 | 17 | 21.5 | 79 |

_Showing 15 of 25 rows._

## RQ3 — Helpfulness by Scrum accountability
| role | response | count | percent | denominator |
| --- | --- | --- | --- | --- |
| Product Owner | Not Helpful | 0 | 0.0 | 79 |
| Product Owner | Slightly Helpful | 4 | 5.1 | 79 |
| Product Owner | Neutral | 8 | 10.1 | 79 |
| Product Owner | Helpful | 31 | 39.2 | 79 |
| Product Owner | Very Helpful | 22 | 27.8 | 79 |
| Product Owner | Not applicable | 14 | 17.7 | 79 |
| Scrum Master | Not Helpful | 0 | 0.0 | 79 |
| Scrum Master | Slightly Helpful | 0 | 0.0 | 79 |
| Scrum Master | Neutral | 9 | 11.4 | 79 |
| Scrum Master | Helpful | 30 | 38.0 | 79 |
| Scrum Master | Very Helpful | 29 | 36.7 | 79 |
| Scrum Master | Not applicable | 11 | 13.9 | 79 |
| Developer | Not Helpful | 0 | 0.0 | 79 |
| Developer | Slightly Helpful | 1 | 1.3 | 79 |
| Developer | Neutral | 6 | 7.6 | 79 |
| Developer | Helpful | 26 | 32.9 | 79 |
| Developer | Very Helpful | 37 | 46.8 | 79 |
| Developer | Not applicable | 9 | 11.4 | 79 |

## RQ3 — Benefits experienced
| label | original_label | count | percent | denominator |
| --- | --- | --- | --- | --- |
| Increased productivity | Increased productivity | 61 | 77.2 | 79 |
| Reduced time for repetitive tasks | Reduced time for repetitive tasks | 60 | 75.9 | 79 |
| Improved quality of artifacts | Improved quality of artifacts | 59 | 74.7 | 79 |
| Support in decision-making | Support in decision-making | 46 | 58.2 | 79 |
| Better communication with stakeholders | Better communication with stakeholders | 41 | 51.9 | 79 |
| Improved knowledge sharing and documentation | Improved knowledge sharing and documentation | 39 | 49.4 | 79 |
| Enhanced creativity in problem-solving | Enhanced creativity in problem-solving | 37 | 46.8 | 79 |
| Better stakeholder alignment through clearer outputs | Better stakeholder alignment through clearer outputs | 28 | 35.4 | 79 |
| Faster onboarding of new team members | Faster onboarding of new team members | 26 | 32.9 | 79 |
| Increased stakeholder trust in project outputs | Increased stakeholder trust in project outputs | 15 | 19.0 | 79 |

## RQ3 — Benefit agreement items
| statement | response | count | percent | denominator |
| --- | --- | --- | --- | --- |
| LLMs help reduce cognitive load in repetitive management tasks. | Strongly disagree | 0 | 0.0 | 79 |
| LLMs help reduce cognitive load in repetitive management tasks. | Disagree | 0 | 0.0 | 79 |
| LLMs help reduce cognitive load in repetitive management tasks. | Neutral | 6 | 7.6 | 79 |
| LLMs help reduce cognitive load in repetitive management tasks. | Agree | 38 | 48.1 | 79 |
| LLMs help reduce cognitive load in repetitive management tasks. | Strongly agree | 35 | 44.3 | 79 |
| LLMs improve collaboration between Agile roles (PO, SM, Dev, QA). | Strongly disagree | 0 | 0.0 | 79 |
| LLMs improve collaboration between Agile roles (PO, SM, Dev, QA). | Disagree | 2 | 2.5 | 79 |
| LLMs improve collaboration between Agile roles (PO, SM, Dev, QA). | Neutral | 29 | 36.7 | 79 |
| LLMs improve collaboration between Agile roles (PO, SM, Dev, QA). | Agree | 28 | 35.4 | 79 |
| LLMs improve collaboration between Agile roles (PO, SM, Dev, QA). | Strongly agree | 20 | 25.3 | 79 |
| LLMs accelerate the preparation of Scrum events (planning, review, retrospective). | Strongly disagree | 0 | 0.0 | 79 |
| LLMs accelerate the preparation of Scrum events (planning, review, retrospective). | Disagree | 1 | 1.3 | 79 |
| LLMs accelerate the preparation of Scrum events (planning, review, retrospective). | Neutral | 12 | 15.2 | 79 |
| LLMs accelerate the preparation of Scrum events (planning, review, retrospective). | Agree | 40 | 50.6 | 79 |
| LLMs accelerate the preparation of Scrum events (planning, review, retrospective). | Strongly agree | 26 | 32.9 | 79 |
| LLMs improve the quality of decision-making in my projects. | Strongly disagree | 0 | 0.0 | 79 |
| LLMs improve the quality of decision-making in my projects. | Disagree | 2 | 2.5 | 79 |
| LLMs improve the quality of decision-making in my projects. | Neutral | 19 | 24.1 | 79 |
| LLMs improve the quality of decision-making in my projects. | Agree | 40 | 50.6 | 79 |
| LLMs improve the quality of decision-making in my projects. | Strongly agree | 18 | 22.8 | 79 |
| LLMs increase transparency and traceability in Agile processes. | Strongly disagree | 0 | 0.0 | 79 |
| LLMs increase transparency and traceability in Agile processes. | Disagree | 4 | 5.1 | 79 |
| LLMs increase transparency and traceability in Agile processes. | Neutral | 27 | 34.2 | 79 |
| LLMs increase transparency and traceability in Agile processes. | Agree | 29 | 36.7 | 79 |
| LLMs increase transparency and traceability in Agile processes. | Strongly agree | 19 | 24.1 | 79 |

## RQ4 — Problems encountered
| label | original_label | count | percent | denominator |
| --- | --- | --- | --- | --- |
| Solutions almost right, but not quite | Solutions that are almost right, but not quite | 52 | 65.8 | 79 |
| Hallucinations | Hallucinations (confident, but fabricated or incorrect answers) | 43 | 54.4 | 79 |
| Privacy/confidentiality concerns | Privacy/confidentiality concerns | 40 | 50.6 | 79 |
| Difficulty validating AI-generated content | Difficulty in validating AI Chat Assistant-generated content | 37 | 46.8 | 79 |
| High variability in output quality | High variability in output quality | 33 | 41.8 | 79 |
| Legal/ethical uncertainties | Legal/ethical uncertainties about AI use | 27 | 34.2 | 79 |
| Difficulty adapting to project/team context | Difficulty adapting to project/team context | 26 | 32.9 | 79 |
| Lack of integration with existing tools | Lack of integration with existing tools | 26 | 32.9 | 79 |
| Less confidence in own problem-solving | I've become less confident in my own problem-solving | 22 | 27.8 | 79 |
| Over-dependence of the team on AI | Over-dependence of the team on AI Chat Assistants | 20 | 25.3 | 79 |
| Resistance from team members | Resistance from team members to adopt AI Chat Assistants | 18 | 22.8 | 79 |

## RQ4 — Intensive use could cause
| risk | response | count | percent | denominator |
| --- | --- | --- | --- | --- |
| Reduced understanding of processes (less deep understanding of processes) | Strongly disagree | 2 | 2.5 | 79 |
| Reduced understanding of processes (less deep understanding of processes) | Disagree | 9 | 11.4 | 79 |
| Reduced understanding of processes (less deep understanding of processes) | Neutral | 17 | 21.5 | 79 |
| Reduced understanding of processes (less deep understanding of processes) | Agree | 29 | 36.7 | 79 |
| Reduced understanding of processes (less deep understanding of processes) | Strongly agree | 22 | 27.8 | 79 |
| Reduced accountability (difficulty in assigning responsibility) | Strongly disagree | 3 | 3.8 | 79 |
| Reduced accountability (difficulty in assigning responsibility) | Disagree | 11 | 13.9 | 79 |
| Reduced accountability (difficulty in assigning responsibility) | Neutral | 25 | 31.6 | 79 |
| Reduced accountability (difficulty in assigning responsibility) | Agree | 23 | 29.1 | 79 |
| Reduced accountability (difficulty in assigning responsibility) | Strongly agree | 17 | 21.5 | 79 |
| Reduced trust (distrust in AI outputs or human–AI collaboration) | Strongly disagree | 3 | 3.8 | 79 |
| Reduced trust (distrust in AI outputs or human–AI collaboration) | Disagree | 8 | 10.1 | 79 |
| Reduced trust (distrust in AI outputs or human–AI collaboration) | Neutral | 23 | 29.1 | 79 |
| Reduced trust (distrust in AI outputs or human–AI collaboration) | Agree | 32 | 40.5 | 79 |
| Reduced trust (distrust in AI outputs or human–AI collaboration) | Strongly agree | 13 | 16.5 | 79 |
| Reduced motivation (reduced engagement of team members when delegating to AI) | Strongly disagree | 3 | 3.8 | 79 |
| Reduced motivation (reduced engagement of team members when delegating to AI) | Disagree | 13 | 16.5 | 79 |
| Reduced motivation (reduced engagement of team members when delegating to AI) | Neutral | 22 | 27.8 | 79 |
| Reduced motivation (reduced engagement of team members when delegating to AI) | Agree | 29 | 36.7 | 79 |
| Reduced motivation (reduced engagement of team members when delegating to AI) | Strongly agree | 12 | 15.2 | 79 |

## RQ5 — Future human-AI relationship
| response | count | percent | denominator |
| --- | --- | --- | --- |
| Human-led, with AI as assistants | 39 | 49.4 | 79 |
| Balanced human–AI collaboration | 25 | 31.6 | 79 |
| AI-led, with humans supervising | 11 | 13.9 | 79 |
| Fully AI automated | 2 | 2.5 | 79 |
| It will be a mix. The more the human master its knowledge the more he will lead. | 1 | 1.3 | 79 |

## RQ5 — Potential replacement of Scrum accountabilities
| label | original_label | count | percent | denominator |
| --- | --- | --- | --- | --- |
| No role replacement | No role replacement | 52 | 65.8 | 79 |
| Yes, Product Owner | Yes, Product Owner | 17 | 21.5 | 79 |
| Yes, Scrum Master | Yes, Scrum Master | 17 | 21.5 | 79 |
| Yes, Developers | Yes, Developers | 16 | 20.3 | 79 |

## Generated CSV tables
- `00_filtering_pipeline.csv`
- `01_profile_consenting_N158_academic_education.csv`
- `01_profile_consenting_N158_age_group.csv`
- `01_profile_consenting_N158_country.csv`
- `01_profile_consenting_N158_scrum_experience_years.csv`
- `01_profile_consenting_N158_scrum_knowledge.csv`
- `01_profile_final_analytic_N79_academic_education.csv`
- `01_profile_final_analytic_N79_age_group.csv`
- `01_profile_final_analytic_N79_country.csv`
- `01_profile_final_analytic_N79_scrum_experience_years.csv`
- `01_profile_final_analytic_N79_scrum_knowledge.csv`
- `01_profile_scrum_experienced_N128_academic_education.csv`
- `01_profile_scrum_experienced_N128_age_group.csv`
- `01_profile_scrum_experienced_N128_country.csv`
- `01_profile_scrum_experienced_N128_scrum_experience_years.csv`
- `01_profile_scrum_experienced_N128_scrum_knowledge.csv`
- `01_profile_worked_scrum_N111_academic_education.csv`
- `01_profile_worked_scrum_N111_age_group.csv`
- `01_profile_worked_scrum_N111_country.csv`
- `01_profile_worked_scrum_N111_scrum_experience_years.csv`
- `01_profile_worked_scrum_N111_scrum_knowledge.csv`
- `02_org_project_final_analytic_N79_application_domain.csv`
- `02_org_project_final_analytic_N79_organization_industry.csv`
- `02_org_project_final_analytic_N79_organization_size.csv`
- `02_org_project_final_analytic_N79_primary_role.csv`
- `02_org_project_final_analytic_N79_problem_domain.csv`
- `02_org_project_final_analytic_N79_product_duration.csv`
- `02_org_project_final_analytic_N79_scrum_team_size.csv`
- `02_org_project_final_analytic_N79_worked_scrum_initiative.csv`
- `02_org_project_scrum_experienced_N128_application_domain.csv`
- `02_org_project_scrum_experienced_N128_organization_industry.csv`
- `02_org_project_scrum_experienced_N128_organization_size.csv`
- `02_org_project_scrum_experienced_N128_primary_role.csv`
- `02_org_project_scrum_experienced_N128_problem_domain.csv`
- `02_org_project_scrum_experienced_N128_product_duration.csv`
- `02_org_project_scrum_experienced_N128_scrum_team_size.csv`
- `02_org_project_scrum_experienced_N128_worked_scrum_initiative.csv`
- `02_org_project_worked_scrum_N111_application_domain.csv`
- `02_org_project_worked_scrum_N111_organization_industry.csv`
- `02_org_project_worked_scrum_N111_organization_size.csv`
- `02_org_project_worked_scrum_N111_primary_role.csv`
- `02_org_project_worked_scrum_N111_problem_domain.csv`
- `02_org_project_worked_scrum_N111_product_duration.csv`
- `02_org_project_worked_scrum_N111_scrum_team_size.csv`
- `02_org_project_worked_scrum_N111_worked_scrum_initiative.csv`
- `03_rq1_ai_tools.csv`
- `03_rq1_ai_tools_other_unmatched.csv`
- `03_rq1_formal_policy.csv`
- `03_rq1_formality_of_use.csv`
- `03_rq1_frequency.csv`
- `03_rq1_interaction_modes.csv`
- `03_rq1_interaction_modes_other_unmatched.csv`
- `03_rq1_llm_knowledge.csv`
- `03_rq1_llm_use_last_6_months.csv`
- `03_rq1_model_free_text_frequencies.csv`
- `03_rq1_time_per_day.csv`
- `04_rq2_adoption_matrix_all_activities.csv`
- `04_rq2_open_response_counts.csv`
- `04_rq2_top_current_use.csv`
- `04_rq2_top_dont_plan.csv`
- `04_rq2_top_planned_use.csv`
- `05_rq3_benefit_agreement_items.csv`
- `05_rq3_benefits_experienced.csv`
- `05_rq3_benefits_other_unmatched.csv`
- `05_rq3_efficiency_general_item.csv`
- `05_rq3_helpfulness_by_scrum_accountability.csv`
- `05_rq3_positive_example_count.csv`
- `06_rq4_biggest_risk_open_count.csv`
- `06_rq4_intensive_use_could_cause.csv`
- `06_rq4_negative_example_count.csv`
- `06_rq4_problems_encountered.csv`
- `06_rq4_problems_other_unmatched.csv`
- `06_rq4_rarely_help_efficiency_item.csv`
- `07_rq5_future_human_ai_relationship.csv`
- `07_rq5_new_skills_open_count.csv`
- `07_rq5_role_replacement.csv`
- `07_rq5_role_replacement_other_unmatched.csv`
- `08_general_comments_open_count.csv`
- `99_consistency_checks.csv`

## Figure outputs
- See `figures/` for manuscript-ready PDF/PNG files.
- See `figure_index.csv` for the generated figure list.

## Notes
- Multi-select questions are parsed using canonical option matching, not comma splitting.
- Percentages use the denominator shown in each table.
- The main LLM-in-Scrum analyses use the final analytic sample (N = 79).
- Broader profile tables are exported separately for transparency, but should not be mixed with N = 79 results unless explicitly explained.
- The RQ2 radial/circular visuals were intentionally replaced by bar-based visuals for readability and to address reviewer concerns.