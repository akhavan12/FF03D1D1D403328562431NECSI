#!/usr/bin/env python3
'''
Auto-generated script to import missing content from webarchives.
Generated from broken link analysis.

This script will import 85 webarchive files to fix broken links.
'''

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CLI_SCRIPT = BASE_DIR / "necsifactory" / "cli.py"

# Matched webarchives to import (sorted by confidence)
WEBARCHIVES_TO_IMPORT = [
    ("search", "Search — New England Complex Systems Institute.webarchive", 1.00),
    ("respiratory-health-for-better-covid-19-outcomes-1", "Respiratory Health for Better COVID-19 Outcomes — New England Complex Systems Institute.webarchive", 0.96),
    ("the-moran-model-as-a-dynamical-process-on-networks-and-its-implications-for-neutral-speciation", "The Moran model as a dynamical process on networks and its implications for neutral speciation — New.webarchive", 0.96),
    ("spontaneous-pattern-formation-and-genetic-invasion-in-locally-mating-and-competing-populations", "Spontaneous pattern formation and genetic invasion in locally mating and competing populations — New.webarchive", 0.96),
    ("respiratory-health-for-better-covid-19-outcomes-v3", "Respiratory Health for Better COVID-19 Outcomes — New England Complex Systems Institute.webarchive", 0.94),
    ("dynamics-of-cellular-level-function-and-regulation-derived-from-murine-expression-array-data", "Dynamics of Cellular Level Function and Regulation Derived From Murine Expression Array Data — New E.webarchive", 0.94),
    ("outbreak-guidelines-for-high-risk-institutions", "Outbreak Guidelines for High-Risk Institutions, V2 — New England Complex Systems Institute.webarchive", 0.94),
    ("what-causes-airway-instability-and-ventilation-defects-during-bronchoconstriction-in-asthma", "What Causes Airway Instability And Ventilation Defects During Bronchoconstriction In Asthma? — New E.webarchive", 0.94),
    ("the-effect-of-travel-restrictions-on-the-domestic-spread-of-the-wuhan-coronavirus-2019-ncov", "The Effect of Travel Restrictions on the Domestic Spread of the Wuhan Coronavirus 2019-nCov — New En.webarchive", 0.93),
    ("theory-and-associated-phenomenology-for-intrinsic-mortality-arising-from-natural-selection", "Theory and Associated Phenomenology for Intrinsic Mortality Arising from Natural Selection — New Eng.webarchive", 0.92),
    ("spontaneous-pattern-formation-and-diversity-in-spatially-structured-evolutionary-ecology", "Spontaneous pattern formation and diversity in spatially structured evolutionary ecology — New Engla.webarchive", 0.90),
    ("robustness-of-spontaneous-pattern-formation-in-spatially-distributed-genetic-populations", "Robustness of spontaneous pattern formation in spatially distributed genetic populations — New Engla.webarchive", 0.90),
    ("identifying-seasonal-mobility-profiles-from-anonymized-and-aggregated-mobile-phone-data", "Identifying Seasonal Mobility Profiles From Anonymized and Aggregated Mobile Phone Data — New Englan.webarchive", 0.89),
    ("coronavirus-guidelines-for-cleaning-and-disinfecting-to-prevent-covid-19-transmission", "Coronavirus Guidelines for Cleaning and Disinfecting to Prevent COVID-19 Transmission — New England .webarchive", 0.88),
    ("food-briefing-2", "Food Briefing — New England Complex Systems Institute.webarchive", 0.87),
    ("food-briefing-4", "Food Briefing — New England Complex Systems Institute.webarchive", 0.87),
    ("lockdown-to-contain-covid-19-is-a-window-of-opportunity-to-prevent-the-second-wave", "Lockdown to contain COVID-19 is a window of opportunity to prevent the second wave — New England Com.webarchive", 0.84),
    ("robustness-against-extinction-by-stochastic-sex-determination-in-small-populations", "Robustness against extinction by stochastic sex determination in small populations — New England Com.webarchive", 0.84),
    ("what-is-being-done-and-what-can-be-done-to-stop-the-wuhan-corona-virus-pandemic", "What is Being Done, and What Can be Done, to Stop the Wuhan Corona Virus Pandemic? — New England Com.webarchive", 0.83),
    ("individual-community-and-government-early-outbreak-response-guidelines-version-3", "Individual, Community and Government Early Outbreak Response Guidelines Version 3 — New England Comp.webarchive", 0.82),
    ("comparison-of-the-roughness-scaling-of-the-surface-topography-of-earth-and-venus", "Comparison of the Roughness Scaling of the Surface Topography of Earth and Venus — New England Compl.webarchive", 0.82),
    ("complexity-rising-from-human-beings-to-human-civilization-a-complexity-profile", "Complexity Rising: From Human Beings to Human Civilization, a Complexity Profile — New England Compl.webarchive", 0.81),
    ("zika-and-other-potential-causes-of-microcephaly-in-brazil-status-march-8-2016", "Zika and Other Potential Causes of Microcephaly in Brazil: Status March 8, 2016 — New England Comple.webarchive", 0.80),
    ("the-ifr-of-the-diamond-princess-has-been-misreported-best-current-value-is-2", "The IFR of the Diamond Princess has been Misreported, Best Current Value is 2.0% — New England Compl.webarchive", 0.80),
    ("the-food-crises-and-political-instability-in-north-africa-and-the-middle-east", "The Food Crises and Political Instability in North Africa and the Middle East — New England Complex .webarchive", 0.79),
    ("modeling-complex-systems-a-case-study-of-compartmental-models-in-epidemiology", "Modeling complex systems: A case study of compartmental models in epidemiology — New England Complex.webarchive", 0.79),
    ("roadmap-to-eliminating-covid-19-in-5-6-weeks-through-the-zero-covid-strategy", "Roadmap to Eliminating COVID-19 in 5-6 Weeks Through the Zero Covid Strategy — New England Complex S.webarchive", 0.78),
    ("use-of-thermodynamics-and-statistical-mechanics-in-describing-the-real-world", "Use of Thermodynamics and Statistical Mechanics in Describing the Real World — New England Complex S.webarchive", 0.78),
    ("dynamics-and-genealogy-of-strains-in-spatially-extended-host-pathogen-models", "Dynamics and genealogy of strains in spatially extended host pathogen models — New England Complex S.webarchive", 0.78),
    ("a-complex-systems-perspective-on-how-agents-can-support-collaborative-design", "A complex systems perspective on how agents can support collaborative design — New England Complex S.webarchive", 0.78),
    ("a-possible-link-between-pyriproxyfen-and-microcephaly-preliminary-version", "A Possible Link Between Pyriproxyfen and Microcephaly (Preliminary Version) — New England Complex Sy.webarchive", 0.76),
    ("substructure-in-complex-systems-and-partially-subdivided-neural-networks-i", "Substructure in Complex Systems and Partially Subdivided Neural Networks I — New England Complex Sys.webarchive", 0.76),
    ("changes-in-the-teaching-and-learning-process-in-a-complex-education-system", "Changes in the Teaching and Learning Process in a Complex Education System — New England Complex Sys.webarchive", 0.76),
    ("research-dynamics-of-complex-systems", "Dynamics of Complex Systems — New England Complex Systems Institute.webarchive", 0.75),
    ("engage-1", "Engage — New England Complex Systems Institute.webarchive", 0.75),
    ("a-linked-shared-space-model-for-covid-19-transmission-and-its-prevention", "A Linked Shared Space Model for COVID-19 Transmission and its Prevention — New England Complex Syste.webarchive", 0.73),
    ("theory-predicts-uneven-distribution-of-genetic-diversity-within-species", "Theory predicts uneven distribution of genetic diversity within species — New England Complex System.webarchive", 0.72),
    ("a-regulatory-system-for-the-financial-sector-of-complex-systems-science", "A Regulatory System for the Financial Sector of Complex Systems Science — New England Complex System.webarchive", 0.72),
    ("distributed-construction-by-mobile-robots-with-enhanced-building-blocks", "Distributed construction by mobile robots with enhanced building blocks — New England Complex System.webarchive", 0.72),
    ("review-of-ferguson-et-al-impact-of-non-pharmaceutical-interventions", "Review of Ferguson et al “Impact of non-pharmaceutical interventions...” Version 2 — New England Com.webarchive", 0.72),
    ("determining-the-rate-and-week-of-infection-of-zika-caused-microcephaly", "Determining the Rate and Week of Infection of Zika Caused Microcephaly — New England Complex Systems.webarchive", 0.71),
    ("anticipating-economic-market-crises-using-measures-of-collective-panic", "Anticipating economic market crises using measures of collective panic — New England Complex Systems.webarchive", 0.71),
    ("multiscale-information-theory-and-the-marginal-utility-of-information", "Multiscale Information Theory and the Marginal Utility of Information — New England Complex Systems .webarchive", 0.71),
    ("sensitivity-of-ballistic-deposition-to-pseudorandom-number-generators", "Sensitivity of ballistic deposition to pseudorandom number generators — New England Complex Systems .webarchive", 0.71),
    ("new-method-uses-physics-to-identify-valuable-biodiversity-communities", "New Method Uses Physics to Identify Valuable Biodiversity Communities — New England Complex Systems .webarchive", 0.71),
    ("what-complex-systems-research-can-teach-us-about-collaborative-design", "What complex systems research can teach us about collaborative design — New England Complex Systems .webarchive", 0.71),
    ("research-evolution-of-lifespans", "Evolution of Lifespans — New England Complex Systems Institute.webarchive", 0.71),
    ("the-evolution-of-reproductive-restraint-through-social-communication", "The Evolution of Reproductive Restraint Through Social Communication — New England Complex Systems I.webarchive", 0.69),
    ("estimating-the-total-genetic-diversity-of-a-spatial-field-population", "Estimating The Total Genetic Diversity of a Spatial Field Population — New England Complex Systems I.webarchive", 0.69),
    ("special-guidelines-for-medical-workers-during-the-covid-19-pandemic", "Special guidelines for medical workers during the Covid-19 Pandemic — New England Complex Systems In.webarchive", 0.68),
    ("stopping-hospital-acquired-infections-using-complex-systems-science", "Stopping Hospital Acquired Infections Using Complex Systems Science — New England Complex Systems In.webarchive", 0.68),
    ("opportunities-in-delivery-of-preventive-services-in-retail-settings", "Opportunities in Delivery of Preventive Services in Retail Settings — New England Complex Systems In.webarchive", 0.68),
    ("news-articles-about-global-patterns-of-speciation-and-diversity", "Global Patterns of Speciation and Diversity — New England Complex Systems Institute.webarchive", 0.68),
    ("where-do-pre-symptomatic-and-asymptomatic-cases-come-from-in-china", "Where do pre-symptomatic and asymptomatic cases come from in China? — New England Complex Systems In.webarchive", 0.68),
    ("systemic-risk-of-pandemic-via-novel-pathogens-coronavirus-a-note", "Systemic Risk of Pandemic via Novel Pathogens – Coronavirus: A Note — New England Complex Systems In.webarchive", 0.67),
    ("a-complex-systems-science-approach-to-healthcare-costs-and-quality", "A Complex Systems Science Approach to Healthcare Costs and Quality — New England Complex Systems Ins.webarchive", 0.67),
    ("a-mathematical-theory-of-strong-emergence-using-multiscale-variety", "A Mathematical Theory of Strong Emergence using Multiscale Variety — New England Complex Systems Ins.webarchive", 0.67),
    ("complex-systems-perspectives-on-education-and-the-education-system", "Complex Systems Perspectives on Education and the Education System — New England Complex Systems Ins.webarchive", 0.67),
    ("coronavirus-guide-for-supermarkets-grocery-stores-and-pharmacies", "Coronavirus Guide for Supermarkets, Grocery Stores, and Pharmacies — New England Complex Systems Ins.webarchive", 0.67),
    ("research-making-things-work", "Making Things Work — New England Complex Systems Institute.webarchive", 0.67),
    ("why-public-health-officials-underestimate-the-risk-of-ebola-in-us", "Why Public Health Officials Underestimate the Risk of Ebola in US — New England Complex Systems Inst.webarchive", 0.66),
    ("is-zika-the-cause-of-microcephaly-status-report-november-4-2016", "Is Zika the cause of Microcephaly? Status Report November 4, 2016 — New England Complex Systems Inst.webarchive", 0.66),
    ("interplay-between-turing-pattern-formation-and-domain-coarsening", "Interplay between Turing pattern formation and domain coarsening — New England Complex Systems Insti.webarchive", 0.65),
    ("freight-time-and-cost-optimization-in-complex-logistics-networks", "Freight Time and Cost Optimization in Complex Logistics Networks — New England Complex Systems Insti.webarchive", 0.65),
    ("response-to-review-by-trevor-charles-re-precautionary-principle", "Response to review by Trevor Charles re: Precautionary Principle — New England Complex Systems Insti.webarchive", 0.65),
    ("scientific-guide-for-complex-systems-and-occupy-wall-street", "Complex Systems and Occupy Wall Street — New England Complex Systems Institute.webarchive", 0.64),
    ("negative-representation-and-instability-in-democratic-elections", "Negative Representation and Instability in Democratic Elections — New England Complex Systems Instit.webarchive", 0.64),
    ("was-india-saved-by-staying-below-the-critical-travel-threshold", "Was India saved by staying below the critical travel threshold? — New England Complex Systems Instit.webarchive", 0.64),
    ("comment-on-forecasting-covid-19-impact-on-hospital-bed-days", "Comment on “Forecasting COVID-19 impact on hospital bed-days..." — New England Complex Systems Insti.webarchive", 0.63),
    ("covid-19-employee-safety-and-screening-questions-for-employers", "COVID-19 Employee Safety and Screening Questions for Employers — New England Complex Systems Institu.webarchive", 0.63),
    ("framing-a-complexity-theory-solution-to-the-middle-east-crises", "Framing a Complexity Theory Solution to the Middle East Crises — New England Complex Systems Institu.webarchive", 0.63),
    ("multiscale-analysis-of-the-healthcare-and-public-health-system", "Multiscale analysis of the healthcare and public health system — New England Complex Systems Institu.webarchive", 0.63),
    ("brief-discussion-of-the-mathematics-of-kin-and-group-selection", "Brief Discussion of the Mathematics of Kin and Group Selection — New England Complex Systems Institu.webarchive", 0.63),
    ("spectral-analysis-and-the-dynamic-response-of-complex-networks", "Spectral analysis and the dynamic response of complex networks — New England Complex Systems Institu.webarchive", 0.63),
    ("is-zika-the-cause-of-microcephaly-status-report-june-22-2016", "Is Zika the cause of Microcephaly? Status Report June 22, 2016 — New England Complex Systems Institu.webarchive", 0.62),
    ("is-zika-the-cause-of-microcephaly-status-report-june-27-2016", "Is Zika the cause of Microcephaly? Status Report June 27, 2016 — New England Complex Systems Institu.webarchive", 0.62),
    ("networks-of-economic-market-interdependence-and-systemic-risk", "Networks of Economic Market Interdependence and Systemic Risk — New England Complex Systems Institut.webarchive", 0.62),
    ("analytically-solvable-model-of-probabilistic-network-dynamics", "Analytically Solvable Model Of Probabilistic Network Dynamics — New England Complex Systems Institut.webarchive", 0.62),
    ("in-memoriam-thomas-c-schelling", "Thomas C. Schelling — New England Complex Systems Institute.webarchive", 0.60),
    ("market-instability-and-the-uptick-rule", "Market Instability — New England Complex Systems Institute.webarchive", 0.47),
    ("three-food-crisis-videos", "Food Crisis — New England Complex Systems Institute.webarchive", 0.46),
    ("what-india-needs-to-do-to-eliminate-covid", "What India needs to do to eliminate Covid— A case for a sub-national Zero Covid Strategy — New Engla.webarchive", 0.42),
    ("darwins-books", "Books — New England Complex Systems Institute.webarchive", 0.38),
    ("how-does-evolution-occur", "Evolution — New England Complex Systems Institute.webarchive", 0.38),
    ("iccs-2018", "HumanCurrent at ICCS 2018 — New England Complex Systems Institute.webarchive", 0.36),
]

def import_webarchive(slug: str, filename: str, confidence: float):
    '''Import a single webarchive file.'''
    print(f"🔄 Importing: {slug} (confidence: {confidence:.2f})")
    
    try:
        # Run the CLI command to import the webarchive
        result = subprocess.run([
            sys.executable, str(CLI_SCRIPT), "ingest", 
            "--webarchive", str(BASE_DIR / "incoming" / filename),
            "--build"
        ], capture_output=True, text=True, cwd=BASE_DIR)
        
        if result.returncode == 0:
            print(f"✅ Successfully imported: {slug}")
            return True
        else:
            print(f"❌ Failed to import {slug}: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error importing {slug}: {e}")
        return False

def main():
    '''Import all matched webarchives.'''
    print(f"🚀 Starting import of {len(WEBARCHIVES_TO_IMPORT)} webarchive files...")
    print("=" * 80)
    
    success_count = 0
    for slug, filename, confidence in WEBARCHIVES_TO_IMPORT:
        if import_webarchive(slug, filename, confidence):
            success_count += 1
        print()
    
    print("=" * 80)
    print(f"📊 Import Summary:")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {len(WEBARCHIVES_TO_IMPORT) - success_count}")
    print(f"   📈 Success Rate: {success_count/len(WEBARCHIVES_TO_IMPORT)*100:.1f}%")
    
    if success_count > 0:
        print(f"\n🎉 Imported {success_count} webarchive files!")
        print("   Run the link checker again to see the improvement:")
        print("   python scripts/check_internal_links.py --save-report")

if __name__ == "__main__":
    main()
