# Potomac River at Little Falls: Five-Year Drinking-Water Screen and Water Quality Index

**Author:** AquaScope Studio  
**Date:** 2026-09-14  
**Description:** screen recent Potomac River water quality at Little Falls against drinking-water guidelines to flag which parameters exceed and quantify an overall index  
**Data Sources:** BasinATLAS (HydroATLAS v1.0), ERA5 via Open-Meteo, similar_basins, usgs  
**Version:** 1.0  

**Site:** 38.9500 N, 77.1300 W

**Answer.** The CCME Water Quality Index for the Potomac River near Little Falls (USGS-01646500, 2021-09-14 to 2026-09-13) scores 100 of 100 (Excellent), grade: indicative. The score rests on a single guideline parameter, dissolved oxygen (0 of 1788 samples below the WHO 2022 minimum of 5.0 mg/L), short of CCME's recommended minimum of four guideline parameters. The FAO 29 irrigation water quality index computed alongside shows no restriction on use (class none, USSL class C2), based on mean electrical conductivity of 0.3351 dS/m alone, since sodium, calcium, magnesium, chloride, bicarbonate, boron, nitrate and pH were never sampled.

*Key numbers*

| Quantity | Value | Unit | Step |
| --- | --- | --- | --- |
| Samples | 5366.0 |  | s1 |
| WHO guideline alerts | 0.0 |  | s2 |
| CCME WQI | 100.0 | of 100 | s3 |

## Summary

Five years of sampled water-quality data (5366 samples, 2021-09-14 to 2026-09-13) at USGS-01646500, Potomac River near Wash DC, Little Falls Pump Sta, were screened against WHO (2022) drinking-water guidelines. Only three parameters were sampled: conductivity, dissolved oxygen and temperature; of these, only dissolved oxygen carries a WHO drinking threshold in this screen. No exceedances were found (0 of 1788 samples). The resulting CCME WQI is 100 of 100 (Excellent), but built from one guideline parameter rather than CCME's recommended four. The NSF WQI could not be computed (only 1 of 9 sub-indices available). An FAO 29 irrigation index computed alongside shows no restriction on use, but only conductivity among its 14 usual inputs was sampled.

## The decision

Decide with the CCME WQI of 100 (index, 0 to 100), grade indicative, band 95-100 (Excellent). This holds only under the condition that dissolved oxygen is the sole sampled parameter with a WHO drinking-water guideline; conductivity and temperature were sampled but carry no guideline in this screen, so they are neither cleared nor flagged. The score would firm up to established, or could change outright, if pH, nitrate, fecal coliform or metals were added and met (or failed) CCME's four-parameter design minimum; a single such addition failing its guideline would immediately lower the score and category.

## Findings

Finding f1 (grade: indicative): the CCME WQI scores 100 of 100, Excellent, for USGS-01646500 over 2021-09-14 to 2026-09-13, but uses only dissolved oxygen (n=1788) as its guideline parameter, short of CCME's recommended minimum of four (meets_minimum_design: false). Finding f2 (grade: screening): the FAO 29 irrigation water quality index shows restriction class none, but this rests on electrical conductivity alone (mean 0.3351 dS/m) since sodium, calcium, magnesium, chloride, bicarbonate, boron, nitrate and pH were never sampled at this station. The WHO screen (0 of 1788 dissolved-oxygen samples exceeding) and the CCME score agree, but mechanically, since both derive from the same series; the NSF WQI could not run (1 of 9 parameters present) and so neither corroborates nor contradicts the CCME result.

## Problem and decision

The client asked to screen the last five years of sampled water-quality parameters at the Potomac River near Little Falls against WHO drinking-water guidelines, flag which parameters exceed, and compute an overall water quality index, with an irrigation index for comparison. No health pass/fail verdict was requested.

## Site and data

The site at latitude 38.95, longitude -77.13 is served by USGS-01646500, POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA, the only water-quality station within 0.2 km, with a 96.5-year water-quality record (catalog start 1930-03-01). The five-year pull covers 2021-09-14 to 2026-09-13. Only three parameters were sampled at this station over that period: conductivity (n=1778, uS/cm @25C), dissolved oxygen (n=1788, mg/l), and temperature (n=1800, deg C), for 5366 total samples.

## Methodology

Step s1 pulled the last five years of sampled parameters at USGS-01646500 for drinking use. Step s2 screened each recognised parameter against the WHO (2022) drinking-water guideline for exceedance frequency. Step s3 computed the CCME WQI 1.0 (and attempted the NSF WQI) against the same guideline set. Step s4 computed the FAO 29 irrigation water quality index (mean statistic) on the same record for comparison. Daily sampling resolution was assumed; health_verdict was left false per the brief.

## Results: step s1

USGS-01646500 yielded 5366 samples across three parameters over 2021-09-14 to 2026-09-13: Conductivity (n=1778, uS/cm @25C, min 152.0, median 330.0, max 728.0), Dissolved Oxygen (n=1788, mg/l, min 6.1, median 10.1, max 15.8), and Temperature (n=1800, deg C, min -0.1, median 16.6, max 33.1).

![Distribution of the sampled values per parameter at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500) (5366 samples, 2021 to 2026): box is the interquartile range, the line the median, points beyond 1.5 IQR shown singly.](figures/s1_samples_by_parameter.png)
*Distribution of the sampled values per parameter at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500) (5366 samples, 2021 to 2026): box is the interquartile range, the line the median, points beyond 1.5 IQR shown singly.*

*The samples (5366 rows) is in the workbook (`workbook.xlsx`, sheet `s1_samples`) and the notebook, not printed here.*

*Samples per parameter at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500).*

| parameter | n | unit | start | end | min | median | max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Conductivity | 1778 | uS/cm @25C | 2021-09-14 | 2026-09-13 | 152.0 | 330.0 | 728.0 |
| DO | 1788 | mg/l | 2021-09-14 | 2026-09-13 | 6.1 | 10.1 | 15.8 |
| Temperature | 1800 | deg C | 2021-09-14 | 2026-09-13 | -0.1 | 16.6 | 33.1 |

## Results: step s2

The WHO (2022) drinking-water screen recognised one parameter, dissolved oxygen, against the rule 'at least 5.0 mg/L'. Of 1788 samples, 0 (0.0%) exceeded, status OK. No alerts (0) or warnings (0) were raised. Conductivity and temperature were sampled but had no applicable WHO threshold in this screen.

![Share of samples outside the WHO drinking-water guideline per parameter; red is an alert (over 10 %), orange a warning (any exceedance), green within the guideline.](figures/s2_who_exceedances.png)
*Share of samples outside the WHO drinking-water guideline per parameter; red is an alert (over 10 %), orange a warning (any exceedance), green within the guideline.*

*WHO drinking-water guideline screen per parameter.*

| parameter | rule | n | n_exceed | pct | status |
| --- | --- | --- | --- | --- | --- |
| dissolved_oxygen | at least 5.0 mg/L | 1788 | 0 | 0.0 | OK |

## Results: step s3

The CCME WQI 1.0 (drinking guideline set) scored 100.0 of 100, category Excellent, with F1 = 0.0, F2 = 0.0, F3 = 0.0, over 1 variable (dissolved oxygen) and 1788 tests; meets_minimum_design is false (CCME recommends at least 4 parameters). The NSF WQI could not be scored (score: null): only 1 of 9 sub-indices was available, dissolved_oxygen_saturation (Q = 96.4, value 103.7314%, n = 1788); 8 parameters (fecal coliform, pH, BOD, temperature change, phosphate, nitrate, turbidity, total solids) were missing.

![CCME WQI of 100 (Excellent) over 1788 samples against the drinking guidelines; the CCME factors are the scope, frequency and amplitude of the exceedances.](figures/s3_wqi_bars.png)
*CCME WQI of 100 (Excellent) over 1788 samples against the drinking guidelines; the CCME factors are the scope, frequency and amplitude of the exceedances.*

*Water quality index and its components.*

| item | value |
| --- | --- |
| use | drinking |
| variant | auto |
| guideline_set | drinking |
| ccme.index | ccme_wqi |
| ccme.guideline_set | drinking |
| ccme.score | 100.0 |
| ccme.category | Excellent |
| ccme.f1 | 0.0 |
| ccme.f2 | 0.0 |
| ccme.f3 | 0.0 |
| ccme.nse | 0.0 |
| ccme.n_variables | 1 |
| ccme.n_tests | 1788 |
| ccme.n_failed_variables | 0 |
| ccme.n_failed_tests | 0 |
| ccme.meets_minimum_design | False |
| ccme.period.start | 2021-09-14 |
| ccme.period.end | 2026-09-13 |
| ccme.period.years | 5.0 |
| ccme.sample_counts.dissolved_oxygen | 1788 |
| ccme.input.n_in | 5366 |
| ccme.input.n_used | 5366 |
| ccme.notes | Only 1 parameter(s) with a guideline were sampled; CCME recommends at least 4.; The index covers the sampled parameters that have a guideline in this set and nothing else. |
| ccme.citation | CCME (2001). Canadian water quality guidelines for the protection of aquatic life: CCME Water Quality Index 1.0, User's Manual. Canadian Council of Ministers of the Environment, Winnipeg. |
| nsf.index | nsf_wqi |
| nsf.complete | False |
| nsf.n_parameters | 1 |
| nsf.missing | fecal_coliform; ph; bod; temperature_change; phosphate; nitrate; turbidity; total_solids |
| nsf.weights_renormalised | True |
| nsf.period.start | 2021-09-14 |
| nsf.period.end | 2026-09-13 |
| nsf.period.years | 5.0 |
| nsf.sample_counts.conductivity | 1778 |
| nsf.sample_counts.dissolved_oxygen | 1788 |
| nsf.sample_counts.temperature | 1800 |
| nsf.input.n_in | 5366 |
| nsf.input.n_used | 5366 |
| nsf.notes | Temperature change needs a reference temperature; the parameter is left out.; Only 1 of the nine NSF parameters are present (fewer than 5); no score is reported.; The NSF sub-index curves used here are digitised approximations of the published curves. |
| nsf.citation | Brown, R. M., McClelland, N. I., Deininger, R. A. and Tozer, R. G. (1970). A water quality index: do we dare? Water and Sewage Works 117, 339-343. Sub-index curves are digitised approximations of the published rating curves. |
| index | ccme_wqi |
| score | 100.0 |
| category | Excellent |
| period.start | 2021-09-14 |
| period.end | 2026-09-13 |
| period.years | 5.0 |
| sample_counts.dissolved_oxygen | 1788 |
| n_samples | 1788 |
| unit | index, 0 to 100 |
| ccme.index | ccme_wqi |
| ccme.guideline_set | drinking |

## Results: step s4

The FAO 29 irrigation water quality index, computed with the mean statistic over the same period, returned restriction 'none' and USSL class C2, driven solely by salinity/EC of 0.3351 dS/m (mean conductivity 335.0641 uS/cm, mean DO 10.5555 mg/L, mean temperature 16.1873 deg C). Eleven inputs -- sodium, calcium, magnesium, bicarbonate, chloride, boron, nitrate, pH, TDS, potassium, carbonate -- were missing, so SAR, sodium percentage and RSC could not be computed.

*Irrigation water quality after FAO 29.*

| item | value |
| --- | --- |
| index | iwqi |
| restriction | none |
| class | none |
| values.conductivity | 335.0641 |
| values.dissolved_oxygen | 10.5555 |
| values.temperature | 16.1873 |
| units.conductivity | uS/cm |
| units.dissolved_oxygen | mg/L |
| units.temperature | deg C |
| statistic | mean |
| missing | sodium; calcium; magnesium; bicarbonate; chloride; boron; nitrate; ph; tds; potassium; carbonate |
| n_samples | 5366 |
| period.start | 2021-09-14 |
| period.end | 2026-09-13 |
| period.years | 5.0 |
| sample_counts.conductivity | 1778 |
| sample_counts.dissolved_oxygen | 1788 |
| sample_counts.temperature | 1800 |
| input.n_in | 5366 |
| input.n_used | 5366 |
| citation | Ayers, R. S. and Westcot, D. W. (1985). Water quality for agriculture. FAO Irrigation and Drainage Paper 29, Rev. 1. FAO, Rome; Richards, L. A. (ed.) (1954). Diagnosis and improvement of saline and alkali soils. USDA Handbook 60; Wilcox, L. V. (1955). Classification and use of irrigation waters. USDA Circular 969; Eaton, F. M. (1950). Significance of carbonates in irrigation waters. Soil Science 69, 123-134. |
| unit | meq/L |
| components.salinity_ec.value | 0.3351 |
| components.salinity_ec.unit | dS/m |
| components.salinity_ec.restriction | none |
| components.salinity_ec.thresholds.none_below | 0.7 |
| components.salinity_ec.thresholds.severe_above | 3.0 |
| components.salinity_ec.basis | FAO 29 Table 1, ECw |
| components.salinity_tds.unit | mg/L |
| components.salinity_tds.thresholds.none_below | 450.0 |
| components.salinity_tds.thresholds.severe_above | 2000.0 |
| components.salinity_tds.basis | FAO 29 Table 1, TDS |
| components.infiltration.unit | SAR with EC |
| components.infiltration.thresholds.note | SAR bands 0-3, 3-6, 6-12, 12-20, 20-40 read against EC (dS/m) |
| components.infiltration.basis | FAO 29 Table 1, infiltration |
| components.sodium_toxicity.unit | SAR |
| components.sodium_toxicity.thresholds.none_below | 3.0 |
| components.sodium_toxicity.thresholds.severe_above | 9.0 |
| components.sodium_toxicity.basis | FAO 29 Table 1, sodium (surface irrigation) |
| components.chloride_toxicity.unit | meq/L |
| components.chloride_toxicity.thresholds.none_below | 4.0 |
| components.chloride_toxicity.thresholds.severe_above | 10.0 |
| components.chloride_toxicity.basis | FAO 29 Table 1, chloride (surface irrigation) |
| components.boron_toxicity.unit | mg/L |
| components.boron_toxicity.thresholds.none_below | 0.7 |
| components.boron_toxicity.thresholds.severe_above | 3.0 |
| components.boron_toxicity.basis | FAO 29 Table 1, boron |
| components.nitrate_nitrogen.unit | mg/L as N |
| components.nitrate_nitrogen.thresholds.none_below | 5.0 |
| components.nitrate_nitrogen.thresholds.severe_above | 30.0 |

## Limitations and what this study does not establish

Both indices cover only the parameters that were actually sampled at USGS-01646500; a parameter never sampled (pH, nitrate, fecal coliform, metals, boron, TDS, ions) is unknown, not cleared. The CCME WQI is built from a single guideline parameter, short of CCME's recommended four, so meets_minimum_design is false and the Excellent category should be read cautiously. The NSF WQI could not be scored at all (1 of 9 sub-indices). The IWQI reflects only electrical conductivity; its 'none' restriction class does not account for sodium hazard, ion toxicity or bicarbonate effects. USGS daily values here are continuous-monitor means; nutrients, metals and bacteria typically come from discrete Water Quality Portal sampling not present in this pull. No cause is stated for any trend in the record.

## Caveats

- The index covers the parameters that were sampled and nothing else; a parameter that was not sampled is not cleared, it is unknown, and a Good or Excellent score is a statement about the sampled parameters, not a verdict that the water is safe for the use.
- The NSF sub-index curves used here are digitised approximations of the published rating curves (Brown et al. 1970), and the weights are renormalised when some of the nine parameters are missing.
- Guideline values are the WHO (2022) drinking-water guidelines (4th edition with addenda), as the WHO screen carries them.
- USGS daily water-quality values are a continuous monitor's daily means for temperature, specific conductance, dissolved oxygen and pH; nutrients, metals and bacteria come from discrete sampling (the Water Quality Portal) and are not in a USGS daily record.

## Recommendations

Adopt the CCME WQI of 100 (Excellent) as an indicative, not established, screen of drinking-water suitability for USGS-01646500 over 2021-09-14 to 2026-09-13, conditioned on it covering dissolved oxygen alone. Treat the FAO 29 irrigation class of 'none' the same way, as conditioned on conductivity alone. To firm up the drinking-water verdict, obtain at least three more WHO-guideline parameters (pH, nitrate, fecal/E. coli coliform, or a metal such as lead or arsenic) so CCME reaches its four-parameter design minimum. To firm up the irrigation comparison, obtain major ion chemistry (sodium, calcium, magnesium, chloride, bicarbonate, boron, nitrate-N, pH) so SAR, sodium percentage and RSC can be computed. Do not treat the current Excellent/none results as a safety clearance for parameters not sampled.

## References

1. CCME (2001). Canadian water quality guidelines for the protection of aquatic life: CCME Water Quality Index 1.0, User's Manual. Canadian Council of Ministers of the Environment, Winnipeg.
2. Brown, R. M., McClelland, N. I., Deininger, R. A. and Tozer, R. G. (1970). A water quality index: do we dare? Water and Sewage Works 117, 339-343.
3. WHO (2022) drinking-water guidelines, 4th edition with addenda
4. Ayers, R. S. and Westcot, D. W. (1985). Water quality for agriculture. FAO Irrigation and Drainage Paper 29, Rev. 1. FAO, Rome.
5. Richards, L. A. (ed.) (1954). Diagnosis and improvement of saline and alkali soils. USDA Handbook 60
6. Wilcox, L. V. (1955). Classification and use of irrigation waters. USDA Circular 969.
7. Eaton, F. M. (1950). Soil Science 69, 123-134.
8. World Health Organization (2022). Guidelines for drinking-water quality, 4th edition, incorporating the first and second addenda. WHO, Geneva.
9. WQI with PCA as the descriptive pair in current applications: Sustainability 16 (2024), doi:10.3390/su16135644; Water 16 (2024), doi:10.3390/w16111570.
10. Irrigation suitability indices (SAR, RSC, sodium percentage) in current applications: Water 16 (2024), doi:10.3390/w16020264.
11. CCME Water Quality Index 1.0
12. FAO Irrigation and Drainage Paper 29
13. Rekin226 and contributors (2026). AquaScope: Open-source water data aggregation toolkit (version 0.16.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.21903143

## Appendix: reproducibility

Re-run the same steps with no model: `aquascope run study.yaml`. Resume the workspace: `aquascope studio --resume workspace.json`.

Model: claude-sonnet-5 via anthropic; ledger: consultant 1 call(s), 4225 tokens, methodologist 1 call(s), 12751 tokens, interpreter 1 call(s), 12294 tokens. aquascope 0.16.0.

```yaml
# An AquaScope study (version 3): the plan behind an answer, its gates, and what happened.
#   aquascope run study.yaml
version: 3
title: "Screen the last five years of sampled water-quality paramete: 38.95, -77.13"
question: "Screen the last five years of water-quality samples of the Potomac at Little Falls against the drinking-water guidelines: which parameters exceed, and what is the index?"
created: "2026-09-14T17:13:23+00:00"
aquascope_version: "0.16.0"
author: "methodologist"
model: "claude-sonnet-5"
problem:
  kind: "water_quality"
  site: {"lat": 38.95, "lon": -77.13}
  params: {"use": "drinking", "years": 5, "health_verdict": false}
  text: "Screen the last five years of water-quality samples of the Potomac at Little Falls against the drinking-water guidelines: which parameters exceed, and what is the index?"
plan:
  author: "methodologist"
  playbook: "water_quality"
  objective: "Screen the last five years of sampled water-quality parameters at the Potomac River near Little Falls against drinking-water guidelines, flag which parameters exceed, and compute an overall water quality index, with an irrigation index computed alongside for comparison."
  decision: "screen recent Potomac River water quality at Little Falls against drinking-water guidelines to flag which parameters exceed and quantify an overall index"
  methodology: ["Pull the sampled water-quality parameters for the last 5 years at USGS-01646500 (Potomac River near Wash DC, Little Falls Pump Sta), the only water-quality station at 0.2 km from the site.", "Screen each sampled parameter against the WHO (2022) drinking-water guideline to flag exceedances and their frequency.", "Compute the CCME WQI 1.0 against the same WHO drinking-water guidelines to give a single 0-100 index and category over the sampled parameters.", "Compute the FAO 29 irrigation water quality index (IWQI) on the same sampled record to give the client the requested irrigation-use comparison figure.", "Report the exceedance list, the WQI score and category, and the IWQI alongside, noting that both indices cover only the parameters actually sampled."]
  assumptions: ["USGS-01646500 is the intended water-quality station given its 0.2 km proximity and 96.5-year water_quality record", "daily sampling resolution assumed since the catalog does not specify one", "health_verdict left at default false since the client asked for exceedances and an index, not a pass/fail health statement", "USGS-01646500 is the intended water-quality station given its 0.2 km proximity and 96.5-year water_quality record.", "Daily sampling resolution is assumed since the catalog does not specify one.", "health_verdict is left at default false: the client asked for exceedances and an index, not a pass/fail health statement.", "The IWQI is computed for comparison only; the decision use is drinking, not irrigation."]
  alternatives: [{"method": "NSF WQI", "why_not": "Not listed as a separate catalogue method; the wqi tool adds it automatically when enough of its nine parameters are present, so it is not planned as a distinct step."}]
  limitations_expected: ["The index covers only the parameters that were sampled; a parameter not sampled is unknown, not cleared.", "USGS daily water-quality values are continuous-monitor daily means (temperature, specific conductance, dissolved oxygen, pH); nutrients, metals and bacteria come from discrete Water Quality Portal sampling and may be sparse.", "A Good or Excellent WQI score is a statement about the sampled parameters, not a verdict that the water is safe to drink.", "The IWQI reflects irrigation suitability criteria (SAR, sodium percentage, RSC) and is not a drinking-water judgment."]
  citations: ["CCME (2001). Canadian water quality guidelines for the protection of aquatic life: CCME Water Quality Index 1.0, User's Manual. Canadian Council of Ministers of the Environment, Winnipeg.", "Brown, R. M., McClelland, N. I., Deininger, R. A. and Tozer, R. G. (1970). A water quality index: do we dare? Water and Sewage Works 117, 339-343.", "World Health Organization (2022). Guidelines for drinking-water quality, 4th edition, incorporating the first and second addenda. WHO, Geneva.", "Ayers, R. S. and Westcot, D. W. (1985). Water quality for agriculture. FAO Irrigation and Drainage Paper 29, Rev. 1. FAO, Rome.", "Richards, L. A. (ed.) (1954). Diagnosis and improvement of saline and alkali soils. USDA Handbook 60; Wilcox, L. V. (1955). Classification and use of irrigation waters. USDA Circular 969.", "WQI with PCA as the descriptive pair in current applications: Sustainability 16 (2024), doi:10.3390/su16135644; Water 16 (2024), doi:10.3390/w16111570.", "Irrigation suitability indices (SAR, RSC, sodium percentage) in current applications: Water 16 (2024), doi:10.3390/w16020264.", "WHO (2022) drinking-water guidelines, 4th edition with addenda", "CCME Water Quality Index 1.0", "FAO Irrigation and Drainage Paper 29", "Brown et al. 1970 (NSF WQI rating curves)"]
  caveats: ["The index covers the parameters that were sampled and nothing else; a parameter that was not sampled is not cleared, it is unknown, and a Good or Excellent score is a statement about the sampled parameters, not a verdict that the water is safe for the use.", "The NSF sub-index curves used here are digitised approximations of the published rating curves (Brown et al. 1970), and the weights are renormalised when some of the nine parameters are missing.", "Guideline values are the WHO (2022) drinking-water guidelines (4th edition with addenda), as the WHO screen carries them.", "USGS daily water-quality values are a continuous monitor's daily means for temperature, specific conductance, dissolved oxygen and pH; nutrients, metals and bacteria come from discrete sampling (the Water Quality Portal) and are not in a USGS daily record."]
  rationale: "Screen the last five years of sampled water-quality parameters at the Potomac River near Little Falls against drinking-water guidelines, flag which parameters exceed, and compute an overall water quality index, with an irrigation index computed alongside for comparison."
  recon_notes: ["Record resolution is not in the catalog; daily is assumed for every variable.", "10 donor gauges from a pool of 34,786 gauged catchments.", "ERA5 temperature and forcing and GloFAS discharge are assumed reachable for any point on land (Open-Meteo); not checked here.", "CMIP6 change factors need model output you supply (aquascope.climate works on downloaded data); not counted."]
steps:
  - tool: "water_quality_samples"
    id: "s1"
    rationale: "Fetch the last 5 years of sampled parameters at the nearest and only water-quality station, Little Falls Pump Sta, as tidy rows with per-parameter counts and units."
    arguments:
      source: "usgs"
      station_id: "USGS-01646500"
      years: 5
      use: "drinking"
    expects:
      - {"check": "not_empty", "path": "samples"}
      - {"check": "unit_present", "path": "unit"}
    outputs: [{"kind": "table", "id": "s1_samples", "caption": "sampled water-quality parameters, last 5 years, USGS-01646500"}, {"kind": "table", "id": "s1_sample_counts", "caption": "sample counts per parameter, USGS-01646500"}]
  - tool: "who_screen"
    id: "s2"
    rationale: "Flag which sampled parameters exceed the WHO (2022) drinking-water guideline and how often."
    arguments:
      from_step: "s1"
    depends_on: ["s1"]
    outputs: [{"kind": "figure", "id": "s2_who_exceedances", "caption": "share of samples exceeding WHO guideline, by parameter"}, {"kind": "table", "id": "s2_who_screen", "caption": "WHO guideline screen results"}]
  - tool: "wqi"
    id: "s3"
    rationale: "Compute the CCME WQI 1.0 against WHO (2022) drinking-water guidelines to give a single index and category over the sampled record."
    method: "water_quality_index"
    arguments:
      from_step: "s1"
      use: "drinking"
    expects:
      - {"check": "not_empty", "path": "ccme.score"}
      - {"check": "min_samples", "path": "ccme.sample_counts", "value": 4}
    fallback: {"step": {"tool": "who_screen", "arguments": {"from_step": "s1"}, "rationale": "If the WQI cannot be scored for insufficient sampled parameters, fall back to the exceedance screen alone.", "expects": []}}
    depends_on: ["s1"]
    outputs: [{"kind": "figure", "id": "s3_wqi_bars", "caption": "WQI sub-index bars by parameter"}, {"kind": "table", "id": "s3_wqi", "caption": "CCME WQI 1.0 score and category"}]
  - tool: "iwqi"
    id: "s4"
    rationale: "Compute the FAO 29 irrigation water quality index on the same sampled record to give the requested irrigation-use comparison alongside the drinking-water screen."
    method: "iwqi"
    arguments:
      from_step: "s1"
      statistic: "mean"
    depends_on: ["s1"]
    outputs: [{"kind": "table", "id": "s4_iwqi", "caption": "IWQI (FAO 29): SAR, sodium percentage, RSC and restriction class"}]
results:
  s1: {"ok": true, "gates": [{"check": "not_empty", "passed": true, "detail": "'samples' is present"}, {"check": "unit_present", "passed": true, "detail": "unit mg/l"}], "summary": "source=usgs, station_id=USGS-01646500, unit=mg/l, years=5.0, start=2021-09-14, end=2026-09-13", "fallback_used": false, "sha256": "212f4c106d1831c6"}
  s2: {"ok": true, "gates": [], "summary": "n_alerts=0, n_warnings=0", "fallback_used": false, "sha256": "4d9e192249f9fd1b"}
  s3: {"ok": true, "gates": [{"check": "not_empty", "passed": true, "detail": "'ccme.score' is present"}, {"check": "min_samples", "passed": true, "detail": "1 parameter(s) with at least 4 samples each"}], "summary": "unit=index, 0 to 100", "fallback_used": false, "sha256": "df6be9458bb65adc"}
  s4: {"ok": true, "gates": [], "summary": "unit=meq/L", "fallback_used": false, "sha256": "3ae4a3fb1f2c0122"}
```

## Cite this software

AquaScope Studio (2026). AquaScope: Open-source water data aggregation toolkit (version 0.16.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.21903143


---

*{'model': 'claude-sonnet-5', 'provider': 'anthropic', 'prose': 'model', 'tokens': {'consultant': {'calls': 1, 'prompt_tokens': 3209, 'completion_tokens': 1016, 'cost_usd': 0.016578}, 'methodologist': {'calls': 1, 'prompt_tokens': 10409, 'completion_tokens': 2342, 'cost_usd': 0.044238}, 'interpreter': {'calls': 1, 'prompt_tokens': 6658, 'completion_tokens': 5636, 'cost_usd': 0.069676}, 'author': {'calls': 1, 'prompt_tokens': 10586, 'completion_tokens': 4348, 'cost_usd': 0.064652}}, 'total_tokens': 44204, 'total_usd': 0.195144, 'budget': None, 'dropped': 0, 'aquascope_version': '0.16.0', 'date': '2026-09-14 17:15 UTC', 'workspace': '061c19d8556d', 'plan_author': 'methodologist', 'written_by': {'answer': 'model', 'summary': 'model', 'decision': 'model', 'findings': 'model', 'problem': 'model', 'site_data': 'model', 'methodology': 'model', 'results-s1': 'model', 'results-s2': 'model', 'results-s3': 'model', 'results-s4': 'model', 'limitations': 'model', 'recommendations': 'model', 'references': 'template', 'appendix': 'template'}}*
