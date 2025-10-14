#!/usr/bin/env python3
'''
Auto-generated script to download missing content from necsi.edu as webarchives.

This script contains 324 URLs to download.
Priority is based on number of broken link references.

Usage:
1. Install Safari or use a web browser that can save as .webarchive
2. Open each URL and save as .webarchive in Factory/incoming/
3. Or use this script as a reference for manual downloading

Priority order (most referenced first):
'''

import webbrowser
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
INCOMING_DIR = BASE_DIR / "incoming"

# URLs to download (sorted by priority)
URLS_TO_DOWNLOAD = [
    ("from-big-data-to-important-information", "https://necsi.edu/research/from-big-data-to-important-information", 7),  # Priority 1
    ("theory-and-associated-phenomenology-for-intrinsic-mortality-arising-from-natural-selection", "https://necsi.edu/research/theory-and-associated-phenomenology-for-intrinsic-mortality-arising-from-natural-selection", 6),  # Priority 2
    ("complex-engineered-systems", "https://necsi.edu/research/complex-engineered-systems", 6),  # Priority 3
    ("steering-the-economy-toward-growth", "https://necsi.edu/research/steering-the-economy-toward-growth", 5),  # Priority 4
    ("accelerating-economic-growth-and-opportunity", "https://necsi.edu/research/accelerating-economic-growth-and-opportunity", 5),  # Priority 5
    ("what-should-tax-policy-be-for-economic-growth", "https://necsi.edu/research/what-should-tax-policy-be-for-economic-growth", 5),  # Priority 6
    ("complexity-rising-from-human-beings-to-human-civilization-a-complexity-profile", "https://necsi.edu/research/complexity-rising-from-human-beings-to-human-civilization-a-complexity-profile", 5),  # Priority 7
    ("use-of-thermodynamics-and-statistical-mechanics-in-describing-the-real-world", "https://necsi.edu/research/use-of-thermodynamics-and-statistical-mechanics-in-describing-the-real-world", 4),  # Priority 8
    ("emergence-of-simplicity-and-complexity", "https://necsi.edu/research/emergence-of-simplicity-and-complexity", 4),  # Priority 9
    ("relational-properties-in-objective-science", "https://necsi.edu/research/relational-properties-in-objective-science", 4),  # Priority 10
    ("yaneer-bar-yam", "https://necsi.edu/yaneer-bar-yam", 4),  # Priority 11
    ("conflict-in-yemen-from-ethnic-fighting-to-food-riots", "https://necsi.edu/research/conflict-in-yemen-from-ethnic-fighting-to-food-riots", 4),  # Priority 12
    ("global-pattern-formation-and-ethniccultural-violence", "https://necsi.edu/research/global-pattern-formation-and-ethniccultural-violence", 4),  # Priority 13
    ("an-exploration-of-social-identity-the-geography-and-politics-of-news-sharing-communities-in-twitter", "https://necsi.edu/research/an-exploration-of-social-identity-the-geography-and-politics-of-news-sharing-communities-in-twitter", 4),  # Priority 14
    ("the-limits-of-phenomenology", "https://necsi.edu/research/the-limits-of-phenomenology", 4),  # Priority 15
    ("the-food-crises-and-political-instability-in-north-africa-and-the-middle-east", "https://necsi.edu/research/the-food-crises-and-political-instability-in-north-africa-and-the-middle-east", 4),  # Priority 16
    ("corporate-competition-a-selforganized-network", "https://necsi.edu/research/corporate-competition-a-selforganized-network", 4),  # Priority 17
    ("ethical-values-a-multiscale-scientific-perspective", "https://necsi.edu/research/ethical-values-a-multiscale-scientific-perspective", 3),  # Priority 18
    ("educating-teams", "https://necsi.edu/research/educating-teams", 3),  # Priority 19
    ("hiring-teams", "https://necsi.edu/research/hiring-teams", 3),  # Priority 20
    ("why-teams", "https://necsi.edu/research/why-teams", 3),  # Priority 21
    ("functional-and-social-team-dynamics-in-industrial-settings", "https://necsi.edu/research/functional-and-social-team-dynamics-in-industrial-settings", 3),  # Priority 22
    ("step-by-step-to-stability-and-peace-in-syria", "https://necsi.edu/research/step-by-step-to-stability-and-peace-in-syria", 3),  # Priority 23
    ("swissification-syrias-best-hope-for-peace", "https://necsi.edu/research/swissification-syrias-best-hope-for-peace", 3),  # Priority 24
    ("an-exploration-of-social-identity-the-structure-of-the-bbc-newssharing-community-on-twitter", "https://necsi.edu/research/an-exploration-of-social-identity-the-structure-of-the-bbc-newssharing-community-on-twitter", 3),  # Priority 25
    ("sentiment-in-new-york-city", "https://necsi.edu/research/sentiment-in-new-york-city", 3),  # Priority 26
    ("aging-is-a-disease-is-there-a-cure", "https://necsi.edu/research/aging-is-a-disease-is-there-a-cure", 3),  # Priority 27
    ("business-dynamics", "https://necsi.edu/research/business-dynamics", 3),  # Priority 28
    ("how-community-response-stopped-ebola", "https://necsi.edu/research/how-community-response-stopped-ebola", 3),  # Priority 29
    ("longrange-interaction-and-evolutionary-stability-in-a-predatorprey-system", "https://necsi.edu/research/longrange-interaction-and-evolutionary-stability-in-a-predatorprey-system", 3),  # Priority 30
    ("stopping-hospital-acquired-infections-using-complex-systems-science", "https://necsi.edu/research/stopping-hospital-acquired-infections-using-complex-systems-science", 3),  # Priority 31
    ("effective-ebola-response", "https://necsi.edu/research/effective-ebola-response", 3),  # Priority 32
    ("draft-new-ebola-response-strategy", "https://necsi.edu/research/draft-new-ebola-response-strategy", 3),  # Priority 33
    ("is-the-response-in-liberia-succeeding", "https://necsi.edu/research/is-the-response-in-liberia-succeeding", 3),  # Priority 34
    ("networks-of-economic-market-interdependence-and-systemic-risk", "https://necsi.edu/research/networks-of-economic-market-interdependence-and-systemic-risk", 3),  # Priority 35
    ("multiscale-variety-in-complex-systems", "https://necsi.edu/research/multiscale-variety-in-complex-systems", 3),  # Priority 36
    ("about-engineering-complex-systems", "https://necsi.edu/research/about-engineering-complex-systems", 3),  # Priority 37
    ("large-scale-engineering-and-evolutionary-change", "https://necsi.edu/research/large-scale-engineering-and-evolutionary-change", 3),  # Priority 38
    ("the-evolution-of-reproductive-restraint-through-social-communication", "https://necsi.edu/research/the-evolution-of-reproductive-restraint-through-social-communication", 3),  # Priority 39
    ("south-african-riots", "https://necsi.edu/research/south-african-riots", 3),  # Priority 40
    ("the-food-crises-a-quantitative-model-of-food-prices-including-speculators-and-ethanol-conversion", "https://necsi.edu/research/the-food-crises-a-quantitative-model-of-food-prices-including-speculators-and-ethanol-conversion", 3),  # Priority 41
    ("food-for-fuel-the-price-of-ethanol", "https://necsi.edu/research/food-for-fuel-the-price-of-ethanol", 3),  # Priority 42
    ("update-february-2012-the-food-crises", "https://necsi.edu/research/update-february-2012-the-food-crises", 3),  # Priority 43
    ("logic-and-generalization", "https://necsi.edu/research/logic-and-generalization", 2),  # Priority 44
    ("safe-zones-in-syria", "https://necsi.edu/research/safe-zones-in-syria", 2),  # Priority 45
    ("peace-for-syria", "https://necsi.edu/research/peace-for-syria", 2),  # Priority 46
    ("a-possible-link-between-pyriproxyfen-and-microcephaly", "https://necsi.edu/research/a-possible-link-between-pyriproxyfen-and-microcephaly", 2),  # Priority 47
    ("draft-zika-virus-community-response", "https://necsi.edu/research/draft-zika-virus-community-response", 2),  # Priority 48
    ("zika-and-other-potential-causes-of-microcephaly-in-brazil-status-march-8-2016", "https://necsi.edu/research/zika-and-other-potential-causes-of-microcephaly-in-brazil-status-march-8-2016", 2),  # Priority 49
    ("transition-to-extinction", "https://necsi.edu/research/transition-to-extinction", 2),  # Priority 50
    ("anticipating-economic-market-crises-using-measures-of-collective-panic", "https://necsi.edu/research/anticipating-economic-market-crises-using-measures-of-collective-panic", 2),  # Priority 51
    ("the-european-debt-crisis", "https://necsi.edu/research/the-european-debt-crisis", 2),  # Priority 52
    ("regulation-of-short-selling", "https://necsi.edu/research/regulation-of-short-selling", 2),  # Priority 53
    ("what-is-evolution", "https://necsi.edu/research/what-is-evolution", 2),  # Priority 54
    ("evidence-for-evolution", "https://necsi.edu/research/evidence-for-evolution", 2),  # Priority 55
    ("co-evolution", "https://necsi.edu/research/co-evolution", 2),  # Priority 56
    ("breeding", "https://necsi.edu/research/breeding", 2),  # Priority 57
    ("charles-darwin", "https://necsi.edu/research/charles-darwin", 2),  # Priority 58
    ("lamarck-vs-darwin", "https://necsi.edu/research/lamarck-vs-darwin", 2),  # Priority 59
    ("activities", "https://necsi.edu/research/activities", 2),  # Priority 60
    ("sources-and-acknowledgments", "https://necsi.edu/research/sources-and-acknowledgments", 2),  # Priority 61
    ("environmental-complexity-information-for-humanenvironment-wellbeing", "https://necsi.edu/research/environmental-complexity-information-for-humanenvironment-wellbeing", 2),  # Priority 62
    ("winter-school", "https://necsi.edu/winter-school", 2),  # Priority 63
    ("conditions-for-neutral-speciation-via-isolation-by-distance", "https://necsi.edu/research/conditions-for-neutral-speciation-via-isolation-by-distance", 2),  # Priority 64
    ("evolution-and-stability-of-ring-species", "https://necsi.edu/research/evolution-and-stability-of-ring-species", 2),  # Priority 65
    ("the-role-of-sex-separation-in-neutral-speciation", "https://necsi.edu/research/the-role-of-sex-separation-in-neutral-speciation", 2),  # Priority 66
    ("global-patterns-of-speciation-and-diversity", "https://necsi.edu/research/global-patterns-of-speciation-and-diversity", 2),  # Priority 67
    ("multiscale-representation-phase-i", "https://necsi.edu/research/multiscale-representation-phase-i", 2),  # Priority 68
    ("dynamics-of-cellular-level-function-and-regulation-derived-from-murine-expression-array-data-1", "https://necsi.edu/research/dynamics-of-cellular-level-function-and-regulation-derived-from-murine-expression-array-data-1", 2),  # Priority 69
    ("interplay-between-turing-pattern-formation-and-domain-coarsening", "https://necsi.edu/research/interplay-between-turing-pattern-formation-and-domain-coarsening", 2),  # Priority 70
    ("the-symbolic-species", "https://necsi.edu/research/the-symbolic-species", 2),  # Priority 71
    ("sixyear-report-on-the-arab-spring", "https://necsi.edu/research/sixyear-report-on-the-arab-spring", 2),  # Priority 72
    ("complexity-and-the-limits-of-revolution", "https://necsi.edu/research/complexity-and-the-limits-of-revolution", 2),  # Priority 73
    ("the-math-that-explains-the-world-the-arab-spring", "https://necsi.edu/research/the-math-that-explains-the-world-the-arab-spring", 2),  # Priority 74
    ("food-briefing", "https://necsi.edu/research/food-briefing", 2),  # Priority 75
    ("rfs-global-security", "https://necsi.edu/research/rfs-global-security", 2),  # Priority 76
    ("from-centrality-to-temporary-fame", "https://necsi.edu/research/from-centrality-to-temporary-fame", 2),  # Priority 77
    ("information-flow-structure-in-largescale-product-development-organizational-networks", "https://necsi.edu/research/information-flow-structure-in-largescale-product-development-organizational-networks", 2),  # Priority 78
    ("topology-of-largescale-engineering-problemsolving-networks", "https://necsi.edu/research/topology-of-largescale-engineering-problemsolving-networks", 2),  # Priority 79
    ("update-july-2012-the-food-crises", "https://necsi.edu/research/update-july-2012-the-food-crises", 2),  # Priority 80
    ("mexico-corn-imports", "https://necsi.edu/research/mexico-corn-imports", 2),  # Priority 81
    ("the-future-of-democracy", "https://necsi.edu/research/the-future-of-democracy", 2),  # Priority 82
    ("the-dynamics-of-collaborative-design", "https://necsi.edu/research/the-dynamics-of-collaborative-design", 2),  # Priority 83
    ("hiroki-tasaka", "https://necsi.edu/hiroki-tasaka", 1),  # Priority 84
    ("logic-and-the-dynamics-of-subjective-truth", "https://necsi.edu/research/logic-and-the-dynamics-of-subjective-truth", 1),  # Priority 85
    ("how-can-we-stop-ethnic-violence", "https://necsi.edu/research/how-can-we-stop-ethnic-violence", 1),  # Priority 86
    ("zika-virus-disease-and-transmission", "https://necsi.edu/research/zika-virus-disease-and-transmission", 1),  # Priority 87
    ("community-zika-prevention-guide", "https://necsi.edu/research/community-zika-prevention-guide", 1),  # Priority 88
    ("gua-de-prevencin-comunitaria-del-zika", "https://necsi.edu/research/gua-de-prevencin-comunitaria-del-zika", 1),  # Priority 89
    ("guia-de-preveno-comunitria-do-zika", "https://necsi.edu/research/guia-de-preveno-comunitria-do-zika", 1),  # Priority 90
    ("zika-annotated-bibliography", "https://necsi.edu/research/zika-annotated-bibliography", 1),  # Priority 91
    ("a-possible-link-between-pyriproxyfen-and-microcephaly-preliminary-version", "https://necsi.edu/research/a-possible-link-between-pyriproxyfen-and-microcephaly-preliminary-version", 1),  # Priority 92
    ("is-zika-the-cause-of-microcephaly-status-report-june-22-2016", "https://necsi.edu/research/is-zika-the-cause-of-microcephaly-status-report-june-22-2016", 1),  # Priority 93
    ("is-zika-the-cause-of-microcephaly-status-report-june-27-2016", "https://necsi.edu/research/is-zika-the-cause-of-microcephaly-status-report-june-27-2016", 1),  # Priority 94
    ("determining-the-rate-and-week-of-infection-of-zika-caused-microcephaly", "https://necsi.edu/research/determining-the-rate-and-week-of-infection-of-zika-caused-microcephaly", 1),  # Priority 95
    ("is-zika-the-cause-of-microcephaly-status-report-november-4-2016", "https://necsi.edu/research/is-zika-the-cause-of-microcephaly-status-report-november-4-2016", 1),  # Priority 96
    ("the-precautionary-principle", "https://necsi.edu/research/the-precautionary-principle", 1),  # Priority 97
    ("climate-models-and-precautionary-measures", "https://necsi.edu/research/climate-models-and-precautionary-measures", 1),  # Priority 98
    ("response-to-review-by-trevor-charles-re-precautionary-principle", "https://necsi.edu/research/response-to-review-by-trevor-charles-re-precautionary-principle", 1),  # Priority 99
    ("complex-systems-and-occupy-wall-street", "https://necsi.edu/research/complex-systems-and-occupy-wall-street", 1),  # Priority 100
    ("scientific-guide-for-complex-systems-and-occupy-wall-street", "https://necsi.edu/research/scientific-guide-for-complex-systems-and-occupy-wall-street", 1),  # Priority 101
    ("dynamic-medicine", "https://necsi.edu/research/dynamic-medicine", 1),  # Priority 102
    ("complex-systems-science-and-obesity", "https://necsi.edu/research/complex-systems-science-and-obesity", 1),  # Priority 103
    ("a-complex-systems-science-approach-to-healthcare-costs-and-quality", "https://necsi.edu/research/a-complex-systems-science-approach-to-healthcare-costs-and-quality", 1),  # Priority 104
    ("opportunities-in-delivery-of-preventive-services-in-retail-settings", "https://necsi.edu/research/opportunities-in-delivery-of-preventive-services-in-retail-settings", 1),  # Priority 105
    ("what-causes-airway-instability-and-ventilation-defects-during-bronchoconstriction-in-asthma", "https://necsi.edu/research/what-causes-airway-instability-and-ventilation-defects-during-bronchoconstriction-in-asthma", 1),  # Priority 106
    ("patient-safety-in-complex-medical-settings", "https://necsi.edu/research/patient-safety-in-complex-medical-settings", 1),  # Priority 107
    ("improving-the-effectiveness-of-health-care-and-public-health", "https://necsi.edu/research/improving-the-effectiveness-of-health-care-and-public-health", 1),  # Priority 108
    ("science-meets-eastern-medicine", "https://necsi.edu/research/science-meets-eastern-medicine", 1),  # Priority 109
    ("system-care-multiscale-analysis-of-medical-errors", "https://necsi.edu/research/system-care-multiscale-analysis-of-medical-errors", 1),  # Priority 110
    ("necsi-prescription-form", "https://necsi.edu/research/necsi-prescription-form", 1),  # Priority 111
    ("crisis-in-medical-care", "https://necsi.edu/research/crisis-in-medical-care", 1),  # Priority 112
    ("the-rationale-for-systemlevel-strategies-of-infection-control", "https://necsi.edu/research/the-rationale-for-systemlevel-strategies-of-infection-control", 1),  # Priority 113
    ("executive-summary-multiscale-analysis-of-care-facility-infection-control-and-policy-interventions", "https://necsi.edu/research/executive-summary-multiscale-analysis-of-care-facility-infection-control-and-policy-interventions", 1),  # Priority 114
    ("multiscale-analysis-of-the-healthcare-and-public-health-system", "https://necsi.edu/research/multiscale-analysis-of-the-healthcare-and-public-health-system", 1),  # Priority 115
    ("understanding-the-healthcare-medical-system-crisis", "https://necsi.edu/research/understanding-the-healthcare-medical-system-crisis", 1),  # Priority 116
    ("the-emergency-department-as-a-complex-system", "https://necsi.edu/research/the-emergency-department-as-a-complex-system", 1),  # Priority 117
    ("design-of-an-emergency-department-process", "https://necsi.edu/research/design-of-an-emergency-department-process", 1),  # Priority 118
    ("why-public-health-officials-underestimate-the-risk-of-ebola-in-us", "https://necsi.edu/research/why-public-health-officials-underestimate-the-risk-of-ebola-in-us", 1),  # Priority 119
    ("ebola-concerns-grow-as-winter-holidays-loom", "https://necsi.edu/research/ebola-concerns-grow-as-winter-holidays-loom", 1),  # Priority 120
    ("stopping-ebola-globally-and-in-west-africa", "https://necsi.edu/research/stopping-ebola-globally-and-in-west-africa", 1),  # Priority 121
    ("response-to-cdc-director-frieden", "https://necsi.edu/research/response-to-cdc-director-frieden", 1),  # Priority 122
    ("the-threat-of-ebola-in-the-west", "https://necsi.edu/research/the-threat-of-ebola-in-the-west", 1),  # Priority 123
    ("scientists-find-a-solution-to-stopping-outbreaks", "https://necsi.edu/research/scientists-find-a-solution-to-stopping-outbreaks", 1),  # Priority 124
    ("general-features-of-complex-systems", "https://necsi.edu/research/general-features-of-complex-systems", 1),  # Priority 125
    ("complex-systems-perspectives-on-education-and-the-education-system", "https://necsi.edu/research/complex-systems-perspectives-on-education-and-the-education-system", 1),  # Priority 126
    ("changes-in-the-teaching-and-learning-process-in-a-complex-education-system", "https://necsi.edu/research/changes-in-the-teaching-and-learning-process-in-a-complex-education-system", 1),  # Priority 127
    ("planning-documents-for-a-national-initiative-on-complex-systems-in-k16-education", "https://necsi.edu/research/planning-documents-for-a-national-initiative-on-complex-systems-in-k16-education", 1),  # Priority 128
    ("exercising-in-the-space-of-possibilities", "https://necsi.edu/research/exercising-in-the-space-of-possibilities", 1),  # Priority 129
    ("multiscale-information-theory-and-the-marginal-utility-of-information", "https://necsi.edu/research/multiscale-information-theory-and-the-marginal-utility-of-information", 1),  # Priority 130
    ("an-informationtheoretic-formalism-for-multiscale-structure-in-complex-systems", "https://necsi.edu/research/an-informationtheoretic-formalism-for-multiscale-structure-in-complex-systems", 1),  # Priority 131
    ("computationally-tractable-pairwise-complexity-profile", "https://necsi.edu/research/computationally-tractable-pairwise-complexity-profile", 1),  # Priority 132
    ("information-flow-through-a-chaotic-channel", "https://necsi.edu/research/information-flow-through-a-chaotic-channel", 1),  # Priority 133
    ("a-mathematical-theory-of-strong-emergence-using-multiscale-variety", "https://necsi.edu/research/a-mathematical-theory-of-strong-emergence-using-multiscale-variety", 1),  # Priority 134
    ("a-selfstabilizing-robust-region-finder-applied-to-color-and-optical-flow-pictures", "https://necsi.edu/research/a-selfstabilizing-robust-region-finder-applied-to-color-and-optical-flow-pictures", 1),  # Priority 135
    ("sensitivity-of-ballistic-deposition-to-pseudorandom-number-generators", "https://necsi.edu/research/sensitivity-of-ballistic-deposition-to-pseudorandom-number-generators", 1),  # Priority 136
    ("comparison-of-the-roughness-scaling-of-the-surface-topography-of-earth-and-venus", "https://necsi.edu/research/comparison-of-the-roughness-scaling-of-the-surface-topography-of-earth-and-venus", 1),  # Priority 137
    ("multiscale-complexity-of-correlated-gaussians", "https://necsi.edu/research/multiscale-complexity-of-correlated-gaussians", 1),  # Priority 138
    ("multiscale-complexityentropy", "https://necsi.edu/research/multiscale-complexityentropy", 1),  # Priority 139
    ("multiscale-analysis-of-information-correlations-in-an-infiniterange-ferromagnetic-ising-system", "https://necsi.edu/research/multiscale-analysis-of-information-correlations-in-an-infiniterange-ferromagnetic-ising-system", 1),  # Priority 140
    ("sum-rule-for-multiscale-representations-of-kinematic-system", "https://necsi.edu/research/sum-rule-for-multiscale-representations-of-kinematic-system", 1),  # Priority 141
    ("cell-fates-as-highdimensional-attractor-states-of-a-complex-gene-regulatory-network", "https://necsi.edu/research/cell-fates-as-highdimensional-attractor-states-of-a-complex-gene-regulatory-network", 1),  # Priority 142
    ("dynamics-and-genealogy-of-strains-in-spatially-extended-host-pathogen-models", "https://necsi.edu/research/dynamics-and-genealogy-of-strains-in-spatially-extended-host-pathogen-models", 1),  # Priority 143
    ("the-gene-centered-view-of-evolution-and-symmetry-breaking", "https://necsi.edu/research/the-gene-centered-view-of-evolution-and-symmetry-breaking", 1),  # Priority 144
    ("conflict-and-complexity", "https://necsi.edu/research/conflict-and-complexity", 1),  # Priority 145
    ("economics-of-food-prices-and-crises", "https://necsi.edu/research/economics-of-food-prices-and-crises", 1),  # Priority 146
    ("unifying-themes-in-complex-systems-ix", "https://necsi.edu/research/unifying-themes-in-complex-systems-ix", 1),  # Priority 147
    ("unifying-themes-in-complex-systems-viii", "https://necsi.edu/research/unifying-themes-in-complex-systems-viii", 1),  # Priority 148
    ("unifying-themes-in-complex-systems-vii", "https://necsi.edu/research/unifying-themes-in-complex-systems-vii", 1),  # Priority 149
    ("unifying-themes-in-complex-systems-vi", "https://necsi.edu/research/unifying-themes-in-complex-systems-vi", 1),  # Priority 150
    ("unifying-themes-in-complex-systems-v", "https://necsi.edu/research/unifying-themes-in-complex-systems-v", 1),  # Priority 151
    ("unifying-themes-in-complex-systems-iv", "https://necsi.edu/research/unifying-themes-in-complex-systems-iv", 1),  # Priority 152
    ("unifying-themes-in-complex-systems-iiib", "https://necsi.edu/research/unifying-themes-in-complex-systems-iiib", 1),  # Priority 153
    ("unifying-themes-in-complex-systems-iiia", "https://necsi.edu/research/unifying-themes-in-complex-systems-iiia", 1),  # Priority 154
    ("unifying-themes-in-complex-systems-ii", "https://necsi.edu/research/unifying-themes-in-complex-systems-ii", 1),  # Priority 155
    ("unifying-themes-in-complex-systems-i", "https://necsi.edu/research/unifying-themes-in-complex-systems-i", 1),  # Priority 156
    ("virtual-worlds", "https://necsi.edu/research/virtual-worlds", 1),  # Priority 157
    ("introduction-to-the-modeling-and-analysis-of-complex-systems", "https://necsi.edu/research/introduction-to-the-modeling-and-analysis-of-complex-systems", 1),  # Priority 158
    ("how-wars-will-be-fought-in-the-21st-century", "https://necsi.edu/research/how-wars-will-be-fought-in-the-21st-century", 1),  # Priority 159
    ("will-threats-against-north-korea-achieve-us-objectives", "https://necsi.edu/research/will-threats-against-north-korea-achieve-us-objectives", 1),  # Priority 160
    ("special-operations-forces-a-global-immune-system", "https://necsi.edu/research/special-operations-forces-a-global-immune-system", 1),  # Priority 161
    ("military-strategy-in-a-complex-world", "https://necsi.edu/research/military-strategy-in-a-complex-world", 1),  # Priority 162
    ("global-civilization-and-counterterrorism", "https://necsi.edu/research/global-civilization-and-counterterrorism", 1),  # Priority 163
    ("principles-of-security-human-cyber-and-biological", "https://necsi.edu/research/principles-of-security-human-cyber-and-biological", 1),  # Priority 164
    ("complexity-of-military-conflict", "https://necsi.edu/research/complexity-of-military-conflict", 1),  # Priority 165
    ("the-collapse-of-civilization", "https://necsi.edu/research/the-collapse-of-civilization", 1),  # Priority 166
    ("science-of-winning-soccer", "https://necsi.edu/research/science-of-winning-soccer", 1),  # Priority 167
    ("complex-systems-and-sports", "https://necsi.edu/research/complex-systems-and-sports", 1),  # Priority 168
    ("applications-of-complex-systems-sports-and-complexity", "https://necsi.edu/research/applications-of-complex-systems-sports-and-complexity", 1),  # Priority 169
    ("brief-discussion-of-the-mathematics-of-kin-and-group-selection", "https://necsi.edu/research/brief-discussion-of-the-mathematics-of-kin-and-group-selection", 1),  # Priority 170
    ("multilevel-and-kin-selection-in-a-connected-world", "https://necsi.edu/research/multilevel-and-kin-selection-in-a-connected-world", 1),  # Priority 171
    ("evolution-in-spatial-predatorprey-models-and-the-prudent-predator", "https://necsi.edu/research/evolution-in-spatial-predatorprey-models-and-the-prudent-predator", 1),  # Priority 172
    ("the-moran-model-as-a-dynamical-process-on-networks-and-its-implications-for-neutral-speciation", "https://necsi.edu/research/the-moran-model-as-a-dynamical-process-on-networks-and-its-implications-for-neutral-speciation", 1),  # Priority 173
    ("robustness-against-extinction-by-stochastic-sex-determination-in-small-populations", "https://necsi.edu/research/robustness-against-extinction-by-stochastic-sex-determination-in-small-populations", 1),  # Priority 174
    ("stability-and-instability-of-polymorphic-populations", "https://necsi.edu/research/stability-and-instability-of-polymorphic-populations", 1),  # Priority 175
    ("beyond-the-mean-field-in-hostpathogen-spatial-ecology", "https://necsi.edu/research/beyond-the-mean-field-in-hostpathogen-spatial-ecology", 1),  # Priority 176
    ("invasion-and-extinction-in-the-mean-field-approximation-for-a-spatial-hostpathogen-model", "https://necsi.edu/research/invasion-and-extinction-in-the-mean-field-approximation-for-a-spatial-hostpathogen-model", 1),  # Priority 177
    ("mean-field-approximation-to-a-spatial-hostpathogen-model", "https://necsi.edu/research/mean-field-approximation-to-a-spatial-hostpathogen-model", 1),  # Priority 178
    ("somatic-evolution-in-the-immune-system", "https://necsi.edu/research/somatic-evolution-in-the-immune-system", 1),  # Priority 179
    ("selfreplicating-worms-that-increase-structural-complexity-through-gene-transmission", "https://necsi.edu/research/selfreplicating-worms-that-increase-structural-complexity-through-gene-transmission", 1),  # Priority 180
    ("a-new-structurally-dissolvable-selfreproducing-loop-evolving-in-a-simple-cellular-automata-space", "https://necsi.edu/research/a-new-structurally-dissolvable-selfreproducing-loop-evolving-in-a-simple-cellular-automata-space", 1),  # Priority 181
    ("spontaneous-evolution-of-selfreproducing-loops-on-cellular-automata", "https://necsi.edu/research/spontaneous-evolution-of-selfreproducing-loops-on-cellular-automata", 1),  # Priority 182
    ("new-method-uses-physics-to-identify-valuable-biodiversity-communities", "https://necsi.edu/research/new-method-uses-physics-to-identify-valuable-biodiversity-communities", 1),  # Priority 183
    ("theory-predicts-uneven-distribution-of-genetic-diversity-within-species", "https://necsi.edu/research/theory-predicts-uneven-distribution-of-genetic-diversity-within-species", 1),  # Priority 184
    ("estimating-the-total-genetic-diversity-of-a-spatial-field-population", "https://necsi.edu/research/estimating-the-total-genetic-diversity-of-a-spatial-field-population", 1),  # Priority 185
    ("spontaneous-pattern-formation-and-diversity-in-spatially-structured-evolutionary-ecology", "https://necsi.edu/research/spontaneous-pattern-formation-and-diversity-in-spatially-structured-evolutionary-ecology", 1),  # Priority 186
    ("spontaneous-pattern-formation-and-genetic-diversity-in-habitats-with-irregular-geographical-features", "https://necsi.edu/research/spontaneous-pattern-formation-and-genetic-diversity-in-habitats-with-irregular-geographical-features", 1),  # Priority 187
    ("spontaneous-pattern-formation-and-genetic-invasion-in-locally-mating-and-competing-populations", "https://necsi.edu/research/spontaneous-pattern-formation-and-genetic-invasion-in-locally-mating-and-competing-populations", 1),  # Priority 188
    ("the-role-of-spontaneous-pattern-formation-in-the-creation-and-maintenance-of-biological-diversity", "https://necsi.edu/research/the-role-of-spontaneous-pattern-formation-in-the-creation-and-maintenance-of-biological-diversity", 1),  # Priority 189
    ("robustness-of-spontaneous-pattern-formation-in-spatially-distributed-genetic-populations", "https://necsi.edu/research/robustness-of-spontaneous-pattern-formation-in-spatially-distributed-genetic-populations", 1),  # Priority 190
    ("dynamical-response-of-networks-under-external-perturbations", "https://necsi.edu/research/dynamical-response-of-networks-under-external-perturbations", 1),  # Priority 191
    ("analytically-solvable-model-of-probabilistic-network-dynamics", "https://necsi.edu/research/analytically-solvable-model-of-probabilistic-network-dynamics", 1),  # Priority 192
    ("spectral-analysis-and-the-dynamic-response-of-complex-networks", "https://necsi.edu/research/spectral-analysis-and-the-dynamic-response-of-complex-networks", 1),  # Priority 193
    ("response-of-complex-networks-to-stimuli", "https://necsi.edu/research/response-of-complex-networks-to-stimuli", 1),  # Priority 194
    ("optimization-of-robustness-and-connectivity-in-complex-networks", "https://necsi.edu/research/optimization-of-robustness-and-connectivity-in-complex-networks", 1),  # Priority 195
    ("dynamics-of-cellular-level-function-and-regulation-derived-from-murine-expression-array-data", "https://necsi.edu/research/dynamics-of-cellular-level-function-and-regulation-derived-from-murine-expression-array-data", 1),  # Priority 196
    ("substructure-in-complex-systems-and-partially-subdivided-neural-networks-i", "https://necsi.edu/research/substructure-in-complex-systems-and-partially-subdivided-neural-networks-i", 1),  # Priority 197
    ("sleep-as-temporary-brain-dissociation", "https://necsi.edu/research/sleep-as-temporary-brain-dissociation", 1),  # Priority 198
    ("identifying-seasonal-mobility-profiles-from-anonymized-and-aggregated-mobile-phone-data", "https://necsi.edu/research/identifying-seasonal-mobility-profiles-from-anonymized-and-aggregated-mobile-phone-data", 1),  # Priority 199
    ("analysis-of-infectiousrecovery-epidemic-models-for-membership-dynamics-of-online-social-networks", "https://necsi.edu/research/analysis-of-infectiousrecovery-epidemic-models-for-membership-dynamics-of-online-social-networks", 1),  # Priority 200
    ("dynamic-model-of-timedependent-complex-networks", "https://necsi.edu/research/dynamic-model-of-timedependent-complex-networks", 1),  # Priority 201
    ("preferential-detachment-in-broadcast-signaling-networks", "https://necsi.edu/research/preferential-detachment-in-broadcast-signaling-networks", 1),  # Priority 202
    ("the-statistical-mechanics-of-complex-product-development", "https://necsi.edu/research/the-statistical-mechanics-of-complex-product-development", 1),  # Priority 203
    ("unusual-percolation-in-simple-smallworld-networks", "https://necsi.edu/research/unusual-percolation-in-simple-smallworld-networks", 1),  # Priority 204
    ("11-separation-of-scales", "https://necsi.edu/research/11-separation-of-scales", 1),  # Priority 205
    ("12-revolution-in-physics", "https://necsi.edu/research/12-revolution-in-physics", 1),  # Priority 206
    ("13-representations-and-information-as-a-function-of-scale", "https://necsi.edu/research/13-representations-and-information-as-a-function-of-scale", 1),  # Priority 207
    ("14-universality", "https://necsi.edu/research/14-universality", 1),  # Priority 208
    ("food-briefing-4", "https://necsi.edu/research/food-briefing-4", 1),  # Priority 209
    ("a-proposal-to-help-distressed-homeowners", "https://necsi.edu/research/a-proposal-to-help-distressed-homeowners", 1),  # Priority 210
    ("market-instability", "https://necsi.edu/research/market-instability", 1),  # Priority 211
    ("the-500-aapl-close", "https://necsi.edu/research/the-500-aapl-close", 1),  # Priority 212
    ("evidence-of-market-manipulation-in-the-financial-crisis", "https://necsi.edu/research/evidence-of-market-manipulation-in-the-financial-crisis", 1),  # Priority 213
    ("market-failure", "https://necsi.edu/research/market-failure", 1),  # Priority 214
    ("a-regulatory-system-for-the-financial-sector-of-complex-systems-science", "https://necsi.edu/research/a-regulatory-system-for-the-financial-sector-of-complex-systems-science", 1),  # Priority 215
    ("the-computer-as-a-road-map-to-unknowable-territory", "https://necsi.edu/research/the-computer-as-a-road-map-to-unknowable-territory", 1),  # Priority 216
    ("press-release-on-the-uptick-rule", "https://necsi.edu/research/press-release-on-the-uptick-rule", 1),  # Priority 217
    ("technical-report-on-sec-uptick-rule-proposals", "https://necsi.edu/research/technical-report-on-sec-uptick-rule-proposals", 1),  # Priority 218
    ("technical-report-on-the-sec-uptick-repeal-pilot", "https://necsi.edu/research/technical-report-on-the-sec-uptick-repeal-pilot", 1),  # Priority 219
    ("flash-crash", "https://necsi.edu/research/flash-crash", 1),  # Priority 220
    ("gradually-then-suddenly", "https://necsi.edu/research/gradually-then-suddenly", 1),  # Priority 221
    ("best-way-to-combat-coronavirus-is-to-agree-on-norms-to-create-safe-spaces-for-families-groups", "https://necsi.edu/research/best-way-to-combat-coronavirus-is-to-agree-on-norms-to-create-safe-spaces-for-families-groups", 1),  # Priority 222
    ("dont-be-too-quick-to-dismiss-travel-restrictions", "https://necsi.edu/research/dont-be-too-quick-to-dismiss-travel-restrictions", 1),  # Priority 223
    ("2019-ncov-outbreak-updates", "https://necsi.edu/research/2019-ncov-outbreak-updates", 1),  # Priority 224
    ("systemic-risk-of-pandemic-via-novel-pathogens-coronavirus-a-note", "https://necsi.edu/research/systemic-risk-of-pandemic-via-novel-pathogens-coronavirus-a-note", 1),  # Priority 225
    ("pandemic-math", "https://necsi.edu/research/pandemic-math", 1),  # Priority 226
    ("massive-testing-can-stop-the-coronavirus-outbreak", "https://necsi.edu/research/massive-testing-can-stop-the-coronavirus-outbreak", 1),  # Priority 227
    ("first-thoughts-on-superspreader-events", "https://necsi.edu/research/first-thoughts-on-superspreader-events", 1),  # Priority 228
    ("review-of-ferguson-et-al-impact-of-nonpharmaceutical-interventions-version-2", "https://necsi.edu/research/review-of-ferguson-et-al-impact-of-nonpharmaceutical-interventions-version-2", 1),  # Priority 229
    ("a-linked-shared-space-model-for-covid-19-transmission-and-its-prevention", "https://necsi.edu/research/a-linked-shared-space-model-for-covid-19-transmission-and-its-prevention", 1),  # Priority 230
    ("why-a-5-week-lockdown-can-stop-covid-19", "https://necsi.edu/research/why-a-5-week-lockdown-can-stop-covid-19", 1),  # Priority 231
    ("covid-19-how-to-win", "https://necsi.edu/research/covid-19-how-to-win", 1),  # Priority 232
    ("breaking-the-testing-logjam-ct-scan-diagnosis", "https://necsi.edu/research/breaking-the-testing-logjam-ct-scan-diagnosis", 1),  # Priority 233
    ("testing-treatments-for-covid-19", "https://necsi.edu/research/testing-treatments-for-covid-19", 1),  # Priority 234
    ("lockdown-to-contain-covid-19-is-a-window-of-opportunity-to-prevent-the-second-wave", "https://necsi.edu/research/lockdown-to-contain-covid-19-is-a-window-of-opportunity-to-prevent-the-second-wave", 1),  # Priority 235
    ("a-brief-cautionary-note-on-opening-schools", "https://necsi.edu/research/a-brief-cautionary-note-on-opening-schools", 1),  # Priority 236
    ("getting-to-zero-stopping-covid-in-ireland", "https://necsi.edu/research/getting-to-zero-stopping-covid-in-ireland", 1),  # Priority 237
    ("strategizing-covid19-lockdowns-using-mobility-patterns", "https://necsi.edu/research/strategizing-covid19-lockdowns-using-mobility-patterns", 1),  # Priority 238
    ("covidzero-how-to-end-the-pandemic-in-5-weeks", "https://necsi.edu/research/covidzero-how-to-end-the-pandemic-in-5-weeks", 1),  # Priority 239
    ("recommended-covidzero-speech-for-president-joe-biden", "https://necsi.edu/research/recommended-covidzero-speech-for-president-joe-biden", 1),  # Priority 240
    ("essential-coronavirus-guidelines", "https://necsi.edu/research/essential-coronavirus-guidelines", 1),  # Priority 241
    ("individual-community-and-government-early-outbreak-response-guidelines-version-3", "https://necsi.edu/research/individual-community-and-government-early-outbreak-response-guidelines-version-3", 1),  # Priority 242
    ("color-zone-pandemic-response-version-2", "https://necsi.edu/research/color-zone-pandemic-response-version-2", 1),  # Priority 243
    ("guidelines-for-coronavirus-in-business-settings", "https://necsi.edu/research/guidelines-for-coronavirus-in-business-settings", 1),  # Priority 244
    ("a-family-guide-with-thoughts-on-safe-spaces", "https://necsi.edu/research/a-family-guide-with-thoughts-on-safe-spaces", 1),  # Priority 245
    ("outbreak-guidelines-for-high-risk-institutions-v2", "https://necsi.edu/research/outbreak-guidelines-for-high-risk-institutions-v2", 1),  # Priority 246
    ("covid-19-recommendations-for-policy-makers", "https://necsi.edu/research/covid-19-recommendations-for-policy-makers", 1),  # Priority 247
    ("guidelines-for-self-isolation", "https://necsi.edu/research/guidelines-for-self-isolation", 1),  # Priority 248
    ("respiratory-health-for-better-covid-19-outcomes", "https://necsi.edu/research/respiratory-health-for-better-covid-19-outcomes", 1),  # Priority 249
    ("coronavirus-guide-for-supermarkets-grocery-stores-and-pharmacies", "https://necsi.edu/research/coronavirus-guide-for-supermarkets-grocery-stores-and-pharmacies", 1),  # Priority 250
    ("covid-19-employee-safety-and-screening-questions-for-employers", "https://necsi.edu/research/covid-19-employee-safety-and-screening-questions-for-employers", 1),  # Priority 251
    ("community-action-and-support-for-covid-19", "https://necsi.edu/research/community-action-and-support-for-covid-19", 1),  # Priority 252
    ("sewing-masks", "https://necsi.edu/research/sewing-masks", 1),  # Priority 253
    ("everyday-life-and-covid19", "https://necsi.edu/research/everyday-life-and-covid19", 1),  # Priority 254
    ("special-guidelines-for-medical-workers-during-the-covid-19-pandemic", "https://necsi.edu/research/special-guidelines-for-medical-workers-during-the-covid-19-pandemic", 1),  # Priority 255
    ("coronavirus-guidelines-for-cleaning-and-disinfecting-to-prevent-covid-19-transmission", "https://necsi.edu/research/coronavirus-guidelines-for-cleaning-and-disinfecting-to-prevent-covid-19-transmission", 1),  # Priority 256
    ("opening-up", "https://necsi.edu/research/opening-up", 1),  # Priority 257
    ("travel-restrictions-for-limiting-community-disease-spread", "https://necsi.edu/research/travel-restrictions-for-limiting-community-disease-spread", 1),  # Priority 258
    ("psychology-and-strategy-for-getting-to-zero", "https://necsi.edu/research/psychology-and-strategy-for-getting-to-zero", 1),  # Priority 259
    ("travel-between-zones", "https://necsi.edu/research/travel-between-zones", 1),  # Priority 260
    ("unsuccessful-versus-successful-covid-strategies", "https://necsi.edu/research/unsuccessful-versus-successful-covid-strategies", 1),  # Priority 261
    ("asia-pacific-zero-covid-coalition-concept-paper", "https://necsi.edu/research/asia-pacific-zero-covid-coalition-concept-paper", 1),  # Priority 262
    ("roadmap-to-eliminating-covid-19-in-5-6-weeks-through-the-zero-covid-strategy", "https://necsi.edu/research/roadmap-to-eliminating-covid-19-in-5-6-weeks-through-the-zero-covid-strategy", 1),  # Priority 263
    ("what-india-needs-to-do-to-eliminate-covid", "https://necsi.edu/research/what-india-needs-to-do-to-eliminate-covid", 1),  # Priority 264
    ("modeling-complex-systems-a-case-study-of-compartmental-models-in-epidemiology", "https://necsi.edu/research/modeling-complex-systems-a-case-study-of-compartmental-models-in-epidemiology", 1),  # Priority 265
    ("the-effect-of-travel-restrictions-on-the-domestic-spread-of-the-wuhan-coronavirus-2019-ncov", "https://necsi.edu/research/the-effect-of-travel-restrictions-on-the-domestic-spread-of-the-wuhan-coronavirus-2019-ncov", 1),  # Priority 266
    ("the-impact-of-travel-and-timing-in-eliminating-covid-19", "https://necsi.edu/research/the-impact-of-travel-and-timing-in-eliminating-covid-19", 1),  # Priority 267
    ("toward-a-disease-model-of-the-coronavirus", "https://necsi.edu/research/toward-a-disease-model-of-the-coronavirus", 1),  # Priority 268
    ("combining-pcr-and-ct-testing-for-covid", "https://necsi.edu/research/combining-pcr-and-ct-testing-for-covid", 1),  # Priority 269
    ("ct-testing-for-covid-benefits-exceed-risks", "https://necsi.edu/research/ct-testing-for-covid-benefits-exceed-risks", 1),  # Priority 270
    ("what-models-can-and-cannot-tell-us-about-covid-19", "https://necsi.edu/research/what-models-can-and-cannot-tell-us-about-covid-19", 1),  # Priority 271
    ("case-studies-of-covid19-travel-restrictions", "https://necsi.edu/research/case-studies-of-covid19-travel-restrictions", 1),  # Priority 272
    ("the-ifr-of-the-diamond-princess-has-been-misreported-best-current-value-is-2", "https://necsi.edu/research/the-ifr-of-the-diamond-princess-has-been-misreported-best-current-value-is-2", 1),  # Priority 273
    ("minimizing-economic-costs-for-covid-19", "https://necsi.edu/research/minimizing-economic-costs-for-covid-19", 1),  # Priority 274
    ("lowest-cost-virus-suppression", "https://necsi.edu/research/lowest-cost-virus-suppression", 1),  # Priority 275
    ("unmasking-the-mask-studies", "https://necsi.edu/research/unmasking-the-mask-studies", 1),  # Priority 276
    ("was-india-saved-by-staying-below-the-critical-travel-threshold", "https://necsi.edu/research/was-india-saved-by-staying-below-the-critical-travel-threshold", 1),  # Priority 277
    ("comment-on-forecasting-covid-19-impact-on-hospital-bed-days", "https://necsi.edu/research/comment-on-forecasting-covid-19-impact-on-hospital-bed-days", 1),  # Priority 278
    ("where-do-pre-symptomatic-and-asymptomatic-cases-come-from-in-china", "https://necsi.edu/research/where-do-pre-symptomatic-and-asymptomatic-cases-come-from-in-china", 1),  # Priority 279
    ("could-air-filtration-reduce-covid19-severity-and-spread", "https://necsi.edu/research/could-air-filtration-reduce-covid19-severity-and-spread", 1),  # Priority 280
    ("the-potential-for-screening-and-tracking-of-covid19-using-particle-counters", "https://necsi.edu/research/the-potential-for-screening-and-tracking-of-covid19-using-particle-counters", 1),  # Priority 281
    ("what-is-being-done-and-what-can-be-done-to-stop-the-wuhan-corona-virus-pandemic", "https://necsi.edu/research/what-is-being-done-and-what-can-be-done-to-stop-the-wuhan-corona-virus-pandemic", 1),  # Priority 282
    ("community-action-for-the-wuhan-coronavirus-pandemic", "https://necsi.edu/research/community-action-for-the-wuhan-coronavirus-pandemic", 1),  # Priority 283
    ("engage-1", "https://necsi.edu/engage", 1),  # Priority 284
    ("thomas-schelling-wins-nobel-prize-for-economics", "https://necsi.edu/research/thomas-schelling-wins-nobel-prize-for-economics", 1),  # Priority 285
    ("humancurrent-at-iccs-2018", "https://necsi.edu/research/humancurrent-at-iccs-2018", 1),  # Priority 286
    ("alfredo-j-morales", "https://necsi.edu/research/alfredo-j-morales", 1),  # Priority 287
    ("twitter-rising", "https://necsi.edu/research/twitter-rising", 1),  # Priority 288
    ("search", "https://necsi.edu/search", 1),  # Priority 289
    ("negative-representation-and-instability-in-democratic-elections", "https://necsi.edu/research/negative-representation-and-instability-in-democratic-elections", 1),  # Priority 290
    ("the-structure-and-dynamics-of-complex-product-design", "https://necsi.edu/research/the-structure-and-dynamics-of-complex-product-design", 1),  # Priority 291
    ("a-complex-systems-perspective-on-how-agents-can-support-collaborative-design", "https://necsi.edu/research/a-complex-systems-perspective-on-how-agents-can-support-collaborative-design", 1),  # Priority 292
    ("when-systems-engineering-fails", "https://necsi.edu/research/when-systems-engineering-fails", 1),  # Priority 293
    ("a-complex-systems-perspective-on-computersupported-collaborative-design-technology", "https://necsi.edu/research/a-complex-systems-perspective-on-computersupported-collaborative-design-technology", 1),  # Priority 294
    ("what-complex-systems-research-can-teach-us-about-collaborative-design", "https://necsi.edu/research/what-complex-systems-research-can-teach-us-about-collaborative-design", 1),  # Priority 295
    ("complex-systems-engineering-principles", "https://necsi.edu/research/complex-systems-engineering-principles", 1),  # Priority 296
    ("complex-systems-and-evolutionary-engineering", "https://necsi.edu/research/complex-systems-and-evolutionary-engineering", 1),  # Priority 297
    ("freight-time-and-cost-optimization-in-complex-logistics-networks", "https://necsi.edu/research/freight-time-and-cost-optimization-in-complex-logistics-networks", 1),  # Priority 298
    ("complex-engineered-systems-a-new-paradigm", "https://necsi.edu/research/complex-engineered-systems-a-new-paradigm", 1),  # Priority 299
    ("distributed-construction-by-mobile-robots-with-enhanced-building-blocks", "https://necsi.edu/research/distributed-construction-by-mobile-robots-with-enhanced-building-blocks", 1),  # Priority 300
    ("building-patterned-structures-with-robot-swarms", "https://necsi.edu/research/building-patterned-structures-with-robot-swarms", 1),  # Priority 301
    ("construction-by-robot-swarms-using-extended-stigmergy", "https://necsi.edu/research/construction-by-robot-swarms-using-extended-stigmergy", 1),  # Priority 302
    ("when-representative-democracy-isnt", "https://necsi.edu/research/when-representative-democracy-isnt", 1),  # Priority 303
    ("corporations-and-regulators", "https://necsi.edu/research/corporations-and-regulators", 1),  # Priority 304
    ("military-intervention-in-egypt", "https://necsi.edu/research/military-intervention-in-egypt", 1),  # Priority 305
    ("contagion-and-cascades-through-the-middle-east", "https://necsi.edu/research/contagion-and-cascades-through-the-middle-east", 1),  # Priority 306
    ("framing-a-complexity-theory-solution-to-the-middle-east-crises", "https://necsi.edu/research/framing-a-complexity-theory-solution-to-the-middle-east-crises", 1),  # Priority 307
    ("necsi-analyzes-unrest-in-the-middle-east", "https://necsi.edu/research/necsi-analyzes-unrest-in-the-middle-east", 1),  # Priority 308
    ("biofuels-panel", "https://necsi.edu/research/biofuels-panel", 1),  # Priority 309
    ("rfs-congress", "https://necsi.edu/research/rfs-congress", 1),  # Priority 310
    ("myths-and-facts-about-the-renewable-fuel-standard", "https://necsi.edu/research/myths-and-facts-about-the-renewable-fuel-standard", 1),  # Priority 311
    ("modeling-policy-and-agricultural-decisions-in-afghanistan", "https://necsi.edu/research/modeling-policy-and-agricultural-decisions-in-afghanistan", 1),  # Priority 312
    ("social-fragmentation-at-multiple-scales", "https://necsi.edu/research/social-fragmentation-at-multiple-scales", 1),  # Priority 313
    ("us-social-fragmentation", "https://necsi.edu/research/us-social-fragmentation", 1),  # Priority 314
    ("vulnerability-analysis-of-high-dimensional-complex-systems", "https://necsi.edu/research/vulnerability-analysis-of-high-dimensional-complex-systems", 1),  # Priority 315
    ("developing-a-mobile-produce-distribution-system-for-lowincome-urban-residents-in-food-deserts", "https://necsi.edu/research/developing-a-mobile-produce-distribution-system-for-lowincome-urban-residents-in-food-deserts", 1),  # Priority 316
    ("dynamic-urban-food-environments", "https://necsi.edu/research/dynamic-urban-food-environments", 1),  # Priority 317
    ("agentbased-modeling-of-policies-to-improve-urban-food-access-for-lowincome-populations", "https://necsi.edu/research/agentbased-modeling-of-policies-to-improve-urban-food-access-for-lowincome-populations", 1),  # Priority 318
    ("will-the-new-ring-vaccination-stop-the-spread-of-ebola", "https://necsi.edu/research/will-the-new-ring-vaccination-stop-the-spread-of-ebola", 1),  # Priority 319
    ("research-making-things-work", "https://necsi.edu/research/making-things-work", 0),  # Priority 320
    ("research-dynamics-of-complex-systems", "https://necsi.edu/research/dynamics-of-complex-systems", 0),  # Priority 321
    ("https:-necsi.edu-certificate-programs", "https://necsi.edu/research/https:-necsi.edu-certificate-programs", 0),  # Priority 322
    ("research-evolution-of-lifespans", "https://necsi.edu/research/evolution-of-lifespans", 0),  # Priority 323
    ("radio-0fuaa7oj0gfhz9dkapxxibq6utt8qm", "https://necsi.edu/research/radio-0fuaa7oj0gfhz9dkapxxibq6utt8qm", 0),  # Priority 324
]

def open_urls_in_browser():
    '''Open all URLs in the default browser for manual downloading.'''
    print(f"🌐 Opening {len(URLS_TO_DOWNLOAD)} URLs in browser...")
    print("📋 Instructions:")
    print("   1. For each URL that opens:")
    print("   2. Save the page as .webarchive")
    print("   3. Save to Factory/incoming/ directory")
    print("   4. Use filename format: 'Page Title — New England Complex Systems Institute.webarchive'")
    print("   5. Press Enter to continue to next URL")
    print()
    
    for i, (slug, url, ref_count) in enumerate(URLS_TO_DOWNLOAD, 1):
        print(f"📄 {i}/{len(URLS_TO_DOWNLOAD)}: {slug}")
        print(f"   URL: {url}")
        print(f"   References: {ref_count} broken links")
        print(f"   Opening in browser...")
        
        webbrowser.open(url)
        
        # Wait for user input
        input("   Press Enter when you've saved this page as .webarchive...")
        print()

def print_url_list():
    '''Print all URLs for manual copying.'''
    print("📋 ALL URLs TO DOWNLOAD:")
    print("=" * 80)
    
    for i, (slug, url, ref_count) in enumerate(URLS_TO_DOWNLOAD, 1):
        print(f"{i:3d}. {slug}")
        print(f"     {url}")
        print(f"     References: {ref_count}")
        print()

def main():
    '''Main function.'''
    print("🚀 NECSI Missing Content Download Helper")
    print("=" * 80)
    print(f"📊 Total URLs to download: {len(URLS_TO_DOWNLOAD)}")
    print()
    
    choice = input("Choose option:\n1. Open URLs in browser (one by one)\n2. Print all URLs\n3. Exit\nChoice (1-3): ")
    
    if choice == "1":
        open_urls_in_browser()
    elif choice == "2":
        print_url_list()
    else:
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
