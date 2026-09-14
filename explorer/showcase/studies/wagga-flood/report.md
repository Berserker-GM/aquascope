# Design Flood for the Murrumbidgee at Wagga Wagga Levee Upgrade: Evidence Status Report

**Author:** AquaScope Studio  
**Date:** 2026-09-14  
**Description:** set the design discharge for the Wagga Wagga levee upgrade and state how reliable that number is  
**Data Sources:** BasinATLAS (HydroATLAS v1.0), ERA5 via Open-Meteo, bom, similar_basins  
**Version:** 1.0  

**Site:** 35.1000 S, 147.3700 E

**Answer.** Notice: the Critic's fix requests on findings, key_numbers, limitations, problem, site_data were not all resolved; read the report with the list of what this study does not establish.

Donor gauges 0 (not established). The regional flood-frequency chain intended to produce a 100-year discharge estimate for the Murrumbidgee at Wagga Wagga did not complete: similar_basins returned zero donor gauges (n_candidates = 0) against a target of 10, so regionalize_signatures and the GloFAS cross-check were both skipped. The only figures available are catchment descriptors from BasinATLAS (HydroATLAS v1.0) at hybas_id 5120597860 - upstream area 27,041.2 km2, mean elevation 715.0 m, precipitation 868.0 mm/yr, aridity index 0.74, degree of regulation 114.9%, and mean annual natural discharge 114.97 m3/s - none of which is a flood quantile. No 100-year design discharge, and no confidence band around one, can be reported from this run.

*Key numbers*

| Quantity | Value | Unit | Step |
| --- | --- | --- | --- |
| Upstream area | 27040.0 | km2 | s1 |
| Donor gauges | 0.0 |  | s2 |

## Summary

The brief called for a 100-year design discharge for a levee upgrade on the Murrumbidgee at Wagga Wagga, to be produced by regionalising flow signatures from 10 donor gauges selected for similarity to the site's BasinATLAS catchment attributes, cross-checked against GloFAS. The catchment characterisation (s1) succeeded and passed its gates. The donor search (s2) failed both its gates (min_donors, not_empty), returning zero candidate gauges from the gauged_pool source. Because the signature-transfer step (s3) and the GloFAS cross-check (s4) both depend on s2, neither ran. No 100-year discharge estimate, gauged or regionalised, and no uncertainty band exist in this output. The only quantitative material available is the BasinATLAS catchment description: upstream area 27,041.2 km2, mean elevation 715.0 m, precipitation 868.0 mm/yr, aridity index 0.74, degree of regulation 114.9%, and mean annual natural discharge 114.97 m3/s, none of which substitutes for a flood quantile.

## The decision

The design discharge cannot be set from this run: the evidence base is graded not_established. There is no numeric value, band, or method output to anchor a design flow; setting one now would mean asserting a number the study does not contain. The conditions producing this state are: no discharge gauge exists at or near Wagga Wagga on the Murrumbidgee; similar_basins failed its min_donors and not_empty gates, returning n_candidates = 0; regionalize_signatures and the GloFAS cross-check were consequently skipped; only physical catchment descriptors from BasinATLAS survive with confidence. What would change this: a successful similar_basins run yielding at least the planned 10 donor gauges with flow records (would allow regionalize_signatures to compute a q100 and could raise the grade to indicative); a working GloFAS discharge series for the grid cell (would allow a screening-level cross-check even without donors); discovery of any at-site or historical peak-flow record on the Murrumbidgee near Wagga Wagga (could raise the grade toward established); or a diagnosis of why the donor search returned zero, since neither its search radius nor similarity thresholds are reported here.

## Findings

Finding f1 (not_established): the donor-basin search for regional flood-frequency transfer returned zero candidate gauges (s2.n_candidates = 0), against a planned 10; this is the point of failure in the evidence chain. Finding f2 (screening): BasinATLA gives a mean annual natural discharge of 114.97 m3/s at the outlet (s1.attributes.discharge_m3s), but this is a long-term average flow, not a flood quantile, and cannot stand in for a 100-year design discharge. No finding reaches indicative or established grade in this run; the consistency checks confirm the donor count of 0 disagrees with the planned 10, and that both regionalize_signatures and the GloFAS cross-check collapsed in lock-step with the donor-search failure, leaving no independent lines of evidence to compare.

## Problem and decision

A levee upgrade on the Murrumbidgee at Wagga Wagga (lat -35.1, lon 147.37) requires a 100-year return-period design discharge in m3/s, together with a defensible statement of how much confidence can be placed in that figure. No discharge gauge exists at or near this reach within a defensible distance; the nearby BOM stations identified (e.g. bom:410001 M/BIDGEE R @ WAGGA) are water-quality only, and the groundwater stations (e.g. bom:GW030475.1.1 Wagga Wagga) do not measure streamflow. The intended approach was therefore regional flood-frequency transfer from gauged donor basins, cross-checked against GloFAS modelled discharge, rather than an at-site frequency fit.

## Site and data

Catchment attributes for the sub-basin (hybas_id 5120597860, pfaf_id 564270701000) draining to the site, from BasinATLAS (HydroATLAS v1.0), area-weighted upstream over 203 level-12 sub-basins: total area 27,983.8 km2, upstream area 27,041.2 km2, mean elevation 715.0 m, mean slope 6.7 degrees, precipitation 868.0 mm/yr, potential evapotranspiration 1,223.0 mm/yr, actual evapotranspiration 681.0 mm/yr, aridity index (P/PET) 0.74, mean annual temperature 12.3 C, runoff 140.95 mm/yr, mean annual natural discharge at the outlet 114.97 m3/s, degree of regulation by reservoirs 114.9%, reservoir volume upstream 4,164 million m3, and population 523,789 people. No discharge gauge exists at or near Wagga Wagga on the Murrumbidgee within a defensible distance; nearby BOM stations found are groundwater-level and water-quality records only, none providing discharge.

## Methodology

The plan was: (1) characterise the catchment via BasinATLAS descriptors to define the attribute space for donor selection; (2) identify the 10 gauged donor basins most similar to the site's catchment from the gauged_pool source; (3) transfer flow signatures, including annual maximum flow, from those donors, quoting leave-one-out skill and inter-donor spread as the uncertainty band; (4) cross-check the regionalised estimate against GloFAS modelled discharge for the site's grid cell; (5) report the 100-year design flow as the regionalised estimate with its band, flagged against GloFAS, stating that the absence of an at-site record widens the uncertainty beyond what a gauged analysis would give. Step 1 executed and passed its gates. Step 2 executed but failed its gates. Steps 3 and 4 were not run as a direct consequence.

## Results: step s1

describe_catchment (BasinATLAS, HydroATLAS v1.0) at lat -35.1, lon 147.37 returned sub-basin hybas_id 5120597860 (next_down 5120597910, main_bas 5120073410, sub_area 110.6 km2, up_area 27,041.2 km2), upstream of 203 level-12 sub-basins. Attributes: area 27,983.8 km2, upstream area 27,041.2 km2, elevation 715.0 m, slope 6.7 degrees, precipitation 868.0 mm/yr, PET 1,223.0 mm/yr, AET 681.0 mm/yr, aridity 0.74, temperature 12.3 C, snow cover 1.0%, runoff 140.95 mm/yr, natural discharge 114.97 m3/s, forest 40.0%, cropland 5.0%, pasture 25.0%, urban 1.0%, irrigated 0.0%, glacier 0.0%, wetland 1.0%, lake 0.3%, karst 9.0%, clay 26.0%, silt 17.0%, sand 57.0%, soil organic carbon 29.0 t/ha, soil water 61.0%, groundwater table 464.14 cm, population density 19.51 people/km2, population 523,789, degree of regulation 114.9%, human footprint 8.6, reservoir volume 4,164 million m3. Both gates (not_empty, max_area_km2 27,983.8 vs ceiling 27,984 km2) passed.

![The site, in longitude and latitude (no basemap); no catalogue station was listed with it.](figures/s1_site_map.png)
*The site, in longitude and latitude (no basemap); no catalogue station was listed with it.*

*Catchment attributes from BasinATLAS for the site at 35.10 S, 147.37 E.*

| attribute | label | value | unit | source | note |
| --- | --- | --- | --- | --- | --- |
| n_sub_basins |  | 203.0 |  |  |  |
| area_km2 |  | 27983.8 |  |  |  |
| outlet_hybas_id |  | 5120597860.0 |  |  |  |
| upstream_area_km2 |  | 27041.2 |  |  |  |
| elevation_m | mean elevation | 715.0 | m | basinatlas_upstream |  |
| slope_deg | mean slope | 6.7 | degrees | basinatlas_upstream |  |
| precipitation_mm_yr | annual precipitation (WorldClim) | 868.0 | mm/yr | basinatlas_upstream |  |
| pet_mm_yr | annual potential evapotranspiration | 1223.0 | mm/yr | basinatlas_upstream |  |
| aet_mm_yr | annual actual evapotranspiration | 681.0 | mm/yr | basinatlas_upstream |  |
| aridity_index | aridity index (P/PET) | 0.74 | P/PET | basinatlas_upstream |  |
| temperature_c | mean annual air temperature | 12.3 | °C | basinatlas_upstream |  |
| snow_cover_pct | annual snow cover extent | 1.0 | % | basinatlas_upstream |  |
| runoff_mm_yr | annual land-surface runoff | 140.95 | mm/yr | area_weighted_mean |  |
| discharge_m3s | mean annual natural discharge at the outlet | 114.97 | m3/s | basinatlas_upstream |  |
| forest_pct | forest cover | 40.0 | % | basinatlas_upstream |  |
| cropland_pct | cropland | 5.0 | % | basinatlas_upstream |  |
| pasture_pct | pasture | 25.0 | % | basinatlas_upstream |  |
| urban_pct | urban extent | 1.0 | % | basinatlas_upstream |  |
| irrigated_pct | irrigated area | 0.0 | % | basinatlas_upstream |  |
| glacier_pct | glacier extent | 0.0 | % | basinatlas_upstream |  |
| wetland_pct | wetlands (all classes) | 1.0 | % | basinatlas_upstream |  |
| lake_pct | lake area | 0.3 | % | basinatlas_upstream |  |
| karst_pct | karst extent | 9.0 | % | basinatlas_upstream |  |
| clay_pct | clay fraction in soil | 26.0 | % | basinatlas_upstream |  |
| silt_pct | silt fraction in soil | 17.0 | % | basinatlas_upstream |  |
| sand_pct | sand fraction in soil | 57.0 | % | basinatlas_upstream |  |
| soil_organic_carbon_t_ha | soil organic carbon | 29.0 | t/ha | basinatlas_upstream |  |
| soil_water_pct | annual soil water content | 61.0 | % | basinatlas_upstream |  |
| groundwater_table_cm | groundwater table depth | 464.14 | cm | area_weighted_mean |  |
| population_density | population density | 19.51 | people/km2 | basinatlas_upstream |  |
| population | population count | 523789.0 | people | basinatlas_upstream |  |
| degree_of_regulation_pct | degree of regulation by reservoirs | 114.9 | % | basinatlas_upstream |  |
| human_footprint_2009 | human footprint (2009) | 8.6 | index 0-50 | basinatlas_upstream |  |
| reservoir_volume_mcm | reservoir volume upstream | 4164.0 | million m3 | basinatlas_upstream |  |

## Results: step s2

similar_basins was run requesting k=10 donors from the gauged_pool source at lat -35.1, lon 147.37. It returned n_candidates = 0 and an empty stations list, method 'combined'. Both gates failed: min_donors ('no donor count at k', value 10) and not_empty ('nothing at stations'). No donor gauges were identified, so no similarity-based transfer basis exists.

## Results: step s3

regionalize_signatures did not run. Its dependency, s2, failed its gates and produced zero donor stations, so no leave-one-out skill score, no transferred annual-maximum signature, and no 100-year quantile or uncertainty band were computed.

## Results: step s4

The GloFAS cross-check (anywhere) did not run because it depends on s3, which was itself skipped. No GloFAS discharge series, return-level figure, or window parameter exists for this site in this run.

## Limitations and what this study does not establish

No 100-year discharge figure was produced by any step; the study establishes catchment physical descriptors only. Design-flood guidance under climate change remains unsettled in the broader literature; even had an estimate been produced, it would be stationary, with any climate scenario an overlay rather than a nonstationary fit. Rare quantiles are sensitive to distribution and estimator choice; had GEV and Log-Pearson III fits been available, a spread above 25% would be reported as disagreement, not averaged - this check was never reached. The catchment carries a degree of regulation of 114.9%, meaning any future annual-maxima transfer would describe the operated river, not a natural flood regime. GloFAS, had it run, is a modelled discharge product, not a gauge reading, and indicative only. No at-site or near-site discharge gauge exists on the Murrumbidgee at Wagga Wagga within a defensible distance; only groundwater and water-quality BOM stations were found nearby.

## What this study does not establish

- Step s2, gate min_donors: no donor count at 'k'
- Step s2, gate not_empty: nothing at 'stations'
- Step s3 (regionalize_signatures) did not run: depends on s2 (failed its gate), so it was not run
- Step s4 (anywhere) did not run: depends on s3 (skipped), so it was not run

## Caveats

- Design-flood guidance under climate change is immature (Wasko et al. 2024, HESS): the estimate here is stationary, and any climate scenario is an overlay on it, not a nonstationary fit.
- Rare quantiles move with the distribution and the estimator. Two fits (GEV by L-moments and Log-Pearson III) are quoted with their intervals and the spread between them; a spread above 25 percent is reported as disagreement, not averaged away.
- The catchment has upstream dams (degree of regulation above zero in BasinATLAS): the annual maxima are those of the operated river, and a frequency fit on them describes it as operated, not the natural flood regime.
- GloFAS discharge is a model output for a grid cell of about 5 km, not a gauge reading; return levels from it are indicative only.

## Recommendations

No design discharge value can be adopted from this study; the evidence does not carry a course of action beyond stating the gap. Before any number is fixed for the levee upgrade, obtain: (1) a diagnosis of why similar_basins returned zero candidates (search radius, similarity thresholds, pool filtering), so the gauged_pool source can actually be queried and re-run; (2) any short-record or historical peak-flow data for the Murrumbidgee at or near Wagga Wagga, including discontinued gauges, to test whether at_site_flood_frequency becomes possible; (3) a GloFAS reanalysis discharge series for the site's grid cell, which alone could support a screening-grade cross-check. If donors are recovered and regionalize_signatures completes, the resulting q100 with its leave-one-out skill and donor spread should be reported as indicative, flagged against GloFAS, and explicitly labelled as describing an operated (regulated) river given the 114.9% degree of regulation. Until then, the levee design should not be finalised on a numeric 100-year flow from this analysis.

## References

1. Oudin, L. et al. (2008). Spatial proximity, physical similarity, regression and ungaged catchments. Water Resour. Res. 44, W03413.
2. Harrigan, S. et al. (2020). GloFAS-ERA5 operational global river discharge reanalysis 1979-present. Earth Syst. Sci. Data 12, 2043-2060.
3. HydroATLAS v1.0 (BasinATLAS), CC BY 4.0. Linke, S., Lehner, B., Ouellet Dallaire, C., et al. (2019). Global hydro-environmental sub-basin and river reach characteristics at high spatial resolution. Scientific Data 6: 283. https://doi.org/10.1038/s41597-019-0300-6
4. England, J. F. et al. (2019). Guidelines for determining flood flow frequency, Bulletin 17C. USGS Techniques and Methods 4-B5.
5. Hosking, J. R. M. (1990). L-moments: analysis and estimation of distributions using linear combinations of order statistics. J. R. Stat. Soc. B 52, 105-124.
6. Wasko, C. et al. (2024). A systematic review of climate change science for flood and design guidance. Hydrol. Earth Syst. Sci. 28, 1251-1285. doi:10.5194/hess-28-1251-2024
7. Nonstationary flood frequency estimates are parameter-fragile: Stoch. Environ. Res. Risk Assess. (2024), doi:10.1007/s00477-024-02680-9
8. Multi-approach cross-checks in infrastructure flood practice: J. Hydrol. (2024), doi:10.1016/j.jhydrol.2024.130698
9. Wasko et al. 2024, HESS
10. BasinATLAS (HydroATLAS v1.0)
11. Rekin226 and contributors (2026). AquaScope: Open-source water data aggregation toolkit (version 0.16.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.21903143

## Appendix: reproducibility

Re-run the same steps with no model: `aquascope run study.yaml`. Resume the workspace: `aquascope studio --resume workspace.json`.

Model: claude-sonnet-5 via anthropic; ledger: consultant 1 call(s), 4173 tokens, methodologist 1 call(s), 13175 tokens, analyst 1 call(s), 3778 tokens, interpreter 1 call(s), 9039 tokens, author 1 call(s), 13671 tokens, critic 1 call(s), 10901 tokens. aquascope 0.16.0.

```yaml
# An AquaScope study (version 3): the plan behind an answer, its gates, and what happened.
#   aquascope run study.yaml
version: 3
title: "Estimate the 100-year return-period flood discharge (m3/s) f: -35.1, 147.37"
question: "Design flood for a levee upgrade on the Murrumbidgee at Wagga Wagga: the 100-year flow, and how far the evidence can be trusted."
created: "2026-09-14T17:06:59+00:00"
aquascope_version: "0.16.0"
author: "methodologist"
model: "claude-sonnet-5"
problem:
  kind: "flood_risk"
  site: {"lat": -35.1, "lon": 147.37}
  params: {"return_period": 100, "decision": "design flow"}
  text: "Design flood for a levee upgrade on the Murrumbidgee at Wagga Wagga: the 100-year flow, and how far the evidence can be trusted."
plan:
  author: "methodologist"
  playbook: "flood_risk"
  objective: "Estimate the 100-year return-period flood discharge (m3/s) for the Murrumbidgee at Wagga Wagga to support a levee upgrade design, and state the confidence that can be placed in that estimate."
  decision: "set the design discharge for the Wagga Wagga levee upgrade and state how reliable that number is"
  methodology: ["Characterise the catchment draining to the site using BasinATLAS descriptors (area, elevation, climate, dams) to define the attribute space for donor selection.", "Identify the 10 gauged donor basins whose catchments most resemble the site's in that attribute space.", "Transfer flow signatures (including annual maximum flow) from those 10 donors to the ungauged site, quoting the leave-one-out skill and the spread across donors as the uncertainty band.", "Cross-check the regionalised estimate against GloFAS modelled discharge for the grid cell containing the site, treating GloFAS as an independent but coarse-resolution check.", "Report the 100-year design flow as the regionalised estimate with its band, flagged against the GloFAS cross-check, and state plainly that no at-site record exists so the uncertainty is wider than a gauged analysis would give."]
  assumptions: ["no discharge gauge exists at or near Wagga Wagga on the Murrumbidgee within a defensible distance; nearby BOM stations are groundwater and water-quality only", "the 100-year flow will be derived from regional flood frequency (similar_basins, regionalize_signatures) using the 10 donor gauges drawn from the wider pool of 34,786 gauged catchments, cross-checked against GloFAS discharge", "catchment descriptors (area 27041 km2 upstream, 27983.8 km2 total, mean elevation 715 m, precipitation 868 mm/yr, aridity 0.74, 114.9 dams index) come from BasinATLAS (HydroATLAS v1.0) and are used to select similar donor basins", "because no at-site record exists, the resulting estimate carries wider uncertainty than a gauged analysis would, and this must be stated plainly in the report", "No discharge gauge exists at or near Wagga Wagga on the Murrumbidgee within a defensible distance (50 km); the nearby BOM stations found are groundwater-level and water-quality only, not discharge.", "The 100-year flow is derived from regional flood frequency (similar_basins, regionalize_signatures) using 10 donor gauges drawn from a pool of 34,786 gauged catchments, cross-checked against GloFAS discharge for the cell.", "Catchment descriptors (upstream area 27041.2 km2, total area 27983.8 km2, mean elevation 715 m, precipitation 868 mm/yr, aridity 0.74, dams index 114.9) come from BasinATLAS (HydroATLAS v1.0) and are used to select similar donor basins.", "Because no at-site record exists, the resulting estimate carries wider uncertainty than a gauged analysis would, and this is stated plainly in the report.", "The catchment has upstream dams (degree of regulation above zero), so any transferred annual-maximum signal describes the operated river, not a natural flood regime."]
  alternatives: [{"method": "at_site_flood_frequency", "why_not": "No discharge record exists within 50 km of Wagga Wagga, so the sufficiency table marks this method not_defensible."}, {"method": "trend_mann_kendall", "why_not": "Requires an at-site discharge series, which does not exist here; also marked not_defensible."}]
  limitations_expected: ["Design-flood guidance under climate change is immature (Wasko et al. 2024, HESS): the estimate here is stationary, and any climate scenario is an overlay on it, not a nonstationary fit.", "Rare quantiles move with the distribution and the estimator; where two fits are available they should be quoted with their intervals, and a spread above 25 percent reported as disagreement rather than averaged away.", "The catchment has upstream dams (degree of regulation above zero in BasinATLAS): any annual-maxima signal transferred from donors reflects the operated river, not the natural flood regime.", "GloFAS discharge is a model output for a grid cell of about 5 km, not a gauge reading; return levels from it are indicative only and are used as a cross-check, not the primary estimate."]
  citations: ["England, J. F. et al. (2019). Guidelines for determining flood flow frequency, Bulletin 17C. USGS Techniques and Methods 4-B5.", "Hosking, J. R. M. (1990). L-moments: analysis and estimation of distributions using linear combinations of order statistics. J. R. Stat. Soc. B 52, 105-124.", "Wasko, C. et al. (2024). A systematic review of climate change science for flood and design guidance. Hydrol. Earth Syst. Sci. 28, 1251-1285. doi:10.5194/hess-28-1251-2024", "Nonstationary flood frequency estimates are parameter-fragile: Stoch. Environ. Res. Risk Assess. (2024), doi:10.1007/s00477-024-02680-9", "Multi-approach cross-checks in infrastructure flood practice: J. Hydrol. (2024), doi:10.1016/j.jhydrol.2024.130698", "Oudin, L. et al. (2008). Spatial proximity, physical similarity, regression and ungaged catchments. Water Resour. Res. 44, W03413.", "Harrigan, S. et al. (2020). GloFAS-ERA5 operational global river discharge reanalysis 1979-present. Earth Syst. Sci. Data 12, 2043-2060.", "Wasko et al. 2024, HESS", "BasinATLAS (HydroATLAS v1.0)"]
  caveats: ["Design-flood guidance under climate change is immature (Wasko et al. 2024, HESS): the estimate here is stationary, and any climate scenario is an overlay on it, not a nonstationary fit.", "Rare quantiles move with the distribution and the estimator. Two fits (GEV by L-moments and Log-Pearson III) are quoted with their intervals and the spread between them; a spread above 25 percent is reported as disagreement, not averaged away.", "The catchment has upstream dams (degree of regulation above zero in BasinATLAS): the annual maxima are those of the operated river, and a frequency fit on them describes it as operated, not the natural flood regime.", "GloFAS discharge is a model output for a grid cell of about 5 km, not a gauge reading; return levels from it are indicative only."]
  rationale: "Estimate the 100-year return-period flood discharge (m3/s) for the Murrumbidgee at Wagga Wagga to support a levee upgrade design, and state the confidence that can be placed in that estimate."
  recon_notes: ["10 donor gauges from a pool of 34,786 gauged catchments.", "ERA5 temperature and forcing and GloFAS discharge are assumed reachable for any point on land (Open-Meteo); not checked here.", "CMIP6 change factors need model output you supply (aquascope.climate works on downloaded data); not counted.", "No gauge with a usable record within 50 km: at-site methods are not defensible; what remains is the regionalisation path (similar_basins, regionalize_signatures) and the GloFAS cross-check."]
steps:
  - tool: "describe_catchment"
    id: "s1"
    rationale: "Establishes the catchment attributes (area, elevation, precipitation, aridity, dams) that anchor the similarity search for donor basins."
    arguments:
      lat: -35.1
      lon: 147.37
      upstream: true
    expects:
      - {"check": "not_empty", "path": "sub_basin"}
      - {"check": "max_area_km2", "path": "sub_basin.up_area", "value": 27983.8}
    outputs: [{"kind": "figure", "id": "s1_site_map", "caption": "site map from describe_catchment"}, {"kind": "table", "id": "s1_catchment_attributes", "caption": "catchment attributes from describe_catchment (area 27041 km2 upstream, mean elevation 715 m, precip 868 mm/yr, aridity 0.74, dams index 114.9)"}]
  - tool: "similar_basins"
    id: "s2"
    rationale: "Selects the 10 donor gauges from the pool of 34,786 gauged catchments whose BasinATLAS attributes most resemble the Wagga Wagga catchment."
    method: "similar_basins"
    arguments:
      lat: -35.1
      lon: 147.37
      k: 10
      sources: ["gauged_pool"]
    expects:
      - {"check": "min_donors", "path": "k", "value": 10}
      - {"check": "not_empty", "path": "stations"}
    depends_on: ["s1"]
    outputs: [{"kind": "figure", "id": "s2_donors_map", "caption": "donors map from similar_basins"}, {"kind": "table", "id": "s2_donors", "caption": "10 donor gauges selected by catchment similarity"}]
  - tool: "regionalize_signatures"
    id: "s3"
    rationale: "Transfers flow signatures, including the annual maximum flow distribution needed for the 100-year quantile, from the 10 donors with a leave-one-out skill score and an uncertainty band."
    method: "regionalize_signatures"
    arguments:
      lat: -35.1
      lon: 147.37
      k: 10
    expects:
      - {"check": "not_empty", "path": "estimates"}
      - {"check": "not_empty", "path": "skill"}
    depends_on: ["s2"]
    outputs: [{"kind": "figure", "id": "s3_signatures_band", "caption": "regionalised flow signatures band, including annual maximum flow, from the 10 donors"}, {"kind": "table", "id": "s3_signatures", "caption": "signatures table from regionalize_signatures"}, {"kind": "table", "id": "s3_donors", "caption": "donor contributions from regionalize_signatures"}]
  - tool: "anywhere"
    id: "s4"
    rationale: "Provides GloFAS modelled discharge for the Wagga Wagga grid cell as an independent cross-check against the regionalised 100-year estimate."
    method: "glofas_cross_check"
    arguments:
      lat: -35.1
      lon: 147.37
      years: 20
    expects:
      - {"check": "not_empty", "path": "climate", "repaired_from": "glofas"}
    depends_on: ["s3"]
    outputs: [{"kind": "figure", "id": "s4_glofas_series", "caption": "GloFAS modelled discharge series for the Wagga Wagga cell"}, {"kind": "table", "id": "s4_glofas_summary", "caption": "GloFAS indicative return-level summary for the cell"}]
results:
  s1: {"ok": true, "gates": [{"check": "not_empty", "passed": true, "detail": "'sub_basin' is present"}, {"check": "max_area_km2", "passed": true, "detail": "catchment of 27,041 km2 against a ceiling of 27,984 km2"}], "summary": "latitude=-35.1, longitude=147.37, license=CC-BY-4.0, attribution=HydroATLAS v1.0 (BasinATLAS), CC BY 4.0. Linke, S., Lehner, B., Ouellet Dallaire, C., et al. (2019). Global hydro-environmental sub-bas", "fallback_used": false, "sha256": "1bf59bc4ec7fe83b"}
  s2: {"ok": true, "gates": [{"check": "min_donors", "passed": false, "detail": "no donor count at 'k'"}, {"check": "not_empty", "passed": false, "detail": "nothing at 'stations'"}], "summary": "method=combined", "fallback_used": false, "sha256": "782fe972228ff5bd", "failed_reason": "gate failed: min_donors (no donor count at 'k'); not_empty (nothing at 'stations')"}
```

## Cite this software

AquaScope Studio (2026). AquaScope: Open-source water data aggregation toolkit (version 0.16.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.21903143


---

*{'model': 'claude-sonnet-5', 'provider': 'anthropic', 'prose': 'model', 'tokens': {'consultant': {'calls': 1, 'prompt_tokens': 3208, 'completion_tokens': 965, 'cost_usd': 0.016066}, 'methodologist': {'calls': 1, 'prompt_tokens': 10327, 'completion_tokens': 2848, 'cost_usd': 0.049134}, 'analyst': {'calls': 1, 'prompt_tokens': 3501, 'completion_tokens': 277, 'cost_usd': 0.009772}, 'interpreter': {'calls': 1, 'prompt_tokens': 5332, 'completion_tokens': 3707, 'cost_usd': 0.047734}, 'author': {'calls': 2, 'prompt_tokens': 23028, 'completion_tokens': 14995, 'cost_usd': 0.196006}, 'critic': {'calls': 1, 'prompt_tokens': 7785, 'completion_tokens': 3116, 'cost_usd': 0.04673}}, 'total_tokens': 79089, 'total_usd': 0.365442, 'budget': None, 'dropped': 0, 'aquascope_version': '0.16.0', 'date': '2026-09-14 17:10 UTC', 'workspace': 'f8dce0b184e5', 'plan_author': 'methodologist', 'written_by': {'answer': 'model', 'summary': 'model', 'decision': 'model', 'findings': 'model', 'problem': 'model', 'site_data': 'model', 'methodology': 'model', 'results-s1': 'model', 'results-s2': 'model', 'results-s3': 'model', 'results-s4': 'model', 'limitations': 'model', 'recommendations': 'model', 'references': 'template', 'appendix': 'template'}}*
