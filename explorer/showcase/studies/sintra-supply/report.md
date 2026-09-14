# Estimate whether an ungauged stream in the Sintra hills can sustain a 4 ML/day ( (38.8, -9.38)

**Author:** AquaScope Studio  
**Date:** 2026-09-14  
**Description:** whether the ungauged Sintra hills stream can supply a village with a 4 ML/day run-of-river abstraction, and how reliable that supply would be  
**Data Sources:** BasinATLAS (HydroATLAS v1.0), ERA5 via Open-Meteo, similar_basins  
**Version:** 1.0  

**Site:** 38.8000 N, 9.3800 W

**Answer.** Notice: the Critic's fix requests on decision, methodology, recommendations, results-s4 were not all resolved; read the report with the list of what this study does not establish.

whether the ungauged Sintra hills stream can supply a village with a 4 ML/day run-of-river abstraction, and how reliable that supply would be: mean daily flow 0.1316 mm/d (screening). Signatures transferred from 1155 donors (similarity): mean daily flow 0.1316 mm/d (band 0.0162 to 1.068); low flow: exceeded 95 % of days 0.0242 mm/d (band 0.0027 to 0.2187); high flow: exceeded 5 % of days 0.3869 mm/d (band 0.0429 to 3.486); mean annual daily maximum 0.8084 mm/d (band 0.0708 to 9.236); mean flow / BasinATLAS precipitation 0.2498 - (band 0.0222 to 0.4773), leave-one-out NSE -0.027; baseflow / total flow 0.7386 - (band 0.5823 to 0.8949), leave-one-out NSE 0.33.

*Key numbers*

| Quantity | Value | Unit | Step |
| --- | --- | --- | --- |
| Upstream area | 478.7 | km2 | s1 |
| Donor gauges | 10 |  | s2 |
| mean daily flow | 0.1316 | mm/d | s3 |
| mean daily flow band, low | 0.0162 | mm/d | s3 |
| mean daily flow band, high | 1.068 | mm/d | s3 |
| low flow: exceeded 95 % of days | 0.0242 | mm/d | s3 |
| low flow: exceeded 95 % of days band, low | 0.0027 | mm/d | s3 |
| low flow: exceeded 95 % of days band, high | 0.2187 | mm/d | s3 |
| high flow: exceeded 5 % of days | 0.3869 | mm/d | s3 |
| high flow: exceeded 5 % of days band, low | 0.0429 | mm/d | s3 |
| high flow: exceeded 5 % of days band, high | 3.486 | mm/d | s3 |
| mean annual daily maximum | 0.8084 | mm/d | s3 |
| mean annual daily maximum band, low | 0.0708 | mm/d | s3 |
| mean annual daily maximum band, high | 9.236 | mm/d | s3 |
| mean flow / BasinATLAS precipitation | 0.2498 | - | s3 |
| mean flow / BasinATLAS precipitation band, low | 0.0222 | - | s3 |
| mean flow / BasinATLAS precipitation band, high | 0.4773 | - | s3 |
| baseflow / total flow | 0.7386 | - | s3 |
| baseflow / total flow band, low | 0.5823 | - | s3 |
| baseflow / total flow band, high | 0.8949 | - | s3 |
| Days the demand is met | 83.17 | % | s4 |
| Flow the river must carry | 0.463 | m3/s | s4 |
| Demand | 0.0463 | m3/s | s4 |
| Verdict | seasonal shortfalls |  | s4 |
| Donor gauges | 5 |  | s4.fallback |

## Summary

Estimate whether an ungauged stream in the Sintra hills can sustain a 4 ML/day (0.0463 m3/s) run-of-river abstraction for a village, and how reliably, using regionalisation since no gauge exists within 50 km of the site.. 4 step(s) ran (methodologist plan, playbook supply_reliability); 8 of 10 gates passed. Signatures transferred from 1155 donors (similarity): mean daily flow 0.1316 mm/d (band 0.0162 to 1.068); low flow: exceeded 95 % of days 0.0242 mm/d (band 0.0027 to 0.2187); high flow: exceeded 5 % of days 0.3869 mm/d (band 0.0429 to 3.486); mean annual daily maximum 0.8084 mm/d (band 0.0708 to 9.236); mean flow / BasinATLAS precipitation 0.2498 - (band 0.0222 to 0.4773), leave-one-out NSE -0.027; baseflow / total flow 0.7386 - (band 0.5823 to 0.8949), leave-one-out NSE 0.33. 2 point(s) are listed under what this study does not establish.

## The decision

whether the ungauged Sintra hills stream can supply a village with a 4 ML/day run-of-river abstraction, and how reliable that supply would be: mean daily flow 0.1316 mm/d (screening). It holds under these conditions: step s4 did not pass not_empty: nothing at 'fdc'; step s4.fallback did not pass min_donors: no donor count at 'k'; A screening rule, not a licence assessment: Q95 kept in the river and at most the stated share of the flow taken are assumptions in the tradition of flow-duration-curve environmental-flow practice (Smakhtin and Eriyagama 2008; Acreman and Dunbar 2004); the regulator's flow standard, return flows, upstream abstractions and storage are not in the number.; Reliability read off the record describes the years on record; a changing climate, new upstream abstraction or a drier decade than any recorded moves it.. What would change it: supply_reliability (s4) establishing its result: gate failed: not_empty (nothing at 'fdc'); the fallback similar_basins did not pass its own gates.

## Findings

- [screening] Upstream area: 478.7 km2 (from s1.attributes.area_km2)
- [screening] Donor gauges: 10 (from s2.k)
- [screening] mean daily flow: 0.1316 mm/d (from s3.estimates.q_mean_mm.value)
- [screening] mean daily flow band, low: 0.0162 mm/d (from s3.estimates.q_mean_mm.low)
- [screening] mean daily flow band, high: 1.068 mm/d (from s3.estimates.q_mean_mm.high)
- [screening] low flow: exceeded 95 % of days: 0.0242 mm/d (from s3.estimates.q95_mm.value)
- [screening] low flow: exceeded 95 % of days band, low: 0.0027 mm/d (from s3.estimates.q95_mm.low)
- [screening] low flow: exceeded 95 % of days band, high: 0.2187 mm/d (from s3.estimates.q95_mm.high)
- [screening] high flow: exceeded 5 % of days: 0.3869 mm/d (from s3.estimates.q05_mm.value)
- [screening] high flow: exceeded 5 % of days band, low: 0.0429 mm/d (from s3.estimates.q05_mm.low)
- [screening] high flow: exceeded 5 % of days band, high: 3.486 mm/d (from s3.estimates.q05_mm.high)
- [screening] mean annual daily maximum: 0.8084 mm/d (from s3.estimates.q_annual_max_mm.value)
- [screening] mean annual daily maximum band, low: 0.0708 mm/d (from s3.estimates.q_annual_max_mm.low)
- [screening] mean annual daily maximum band, high: 9.236 mm/d (from s3.estimates.q_annual_max_mm.high)
- [screening] mean flow / BasinATLAS precipitation: 0.2498 - (from s3.estimates.runoff_ratio.value)
- [screening] mean flow / BasinATLAS precipitation band, low: 0.0222 - (from s3.estimates.runoff_ratio.low)
- [screening] mean flow / BasinATLAS precipitation band, high: 0.4773 - (from s3.estimates.runoff_ratio.high)
- [screening] baseflow / total flow: 0.7386 - (from s3.estimates.baseflow_index.value)
- [screening] baseflow / total flow band, low: 0.5823 - (from s3.estimates.baseflow_index.low)
- [screening] baseflow / total flow band, high: 0.8949 - (from s3.estimates.baseflow_index.high)
- [not established] Flow the river must carry: 0.463 m3/s (from s4.required_flow_m3s)
- [not established] Demand: 0.0463 m3/s (from s4.demand_m3s)

## Problem and decision

A stream in the Sintra hills near Lisbon with no gauge: can it supply a village with 4 ML/day run of river, and how reliably? Decision: whether the ungauged Sintra hills stream can supply a village with a 4 ML/day run-of-river abstraction, and how reliable that supply would be. Quantities wanted: estimated flow duration curve (Q05, Q50, Q95) at the site; mean annual flow; abstraction as a fraction of daily flow; percent of time the 4 ML/day demand can be met without storage. Constraints: no run-of-river storage assumed (village take is direct from the stream); no gauge within 50 km of the site (nearest is hubeau_hydrometrie/S516001001 at 823 km, unusable for at-site methods); abstraction screened against a maximum share of daily flow; estimate must come from regionalisation (similar basins, regionalised signatures) rather than at-site record. Intake: demand_m3s = 0.0463, demand_ml_day = 4.0, use = municipal, share = 0.1, storage = False. Assumed: catchment delineation from BasinATLAS (HydroATLAS v1.0), HYBAS id 2120018870, upstream area 478.7 km2, taken as the contributing area at the site; flow regime estimated via regionalize_signatures and similar_basins using the 10 donor gauges identified in the catalog, since no discharge record exists at this site or within 50 km; GloFAS reanalysis discharge at this point used as an independent cross-check on the regionalised estimate; share of flow (10 percent of daily flow) used as the default screening threshold for a safe abstraction, per the playbook default; no storage or regulation at the offtake, consistent with the client's description of run-of-river supply; 1 ML/day equals 0.01157 m3/s, so 4 ML/day equals about 0.0463 m3/s.

## Site and data

Site: 38.8, -9.38. The datasets within reach or attached:

| Id | Kind | Variable | Source | Name | Years | Resolution | km | Period | Quality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| catchment | catchment |  | BasinATLAS (HydroATLAS v1.0) | the catchment of the point |  |  |  |  |  |
| donors | donors |  | similar_basins | 10 donor gauges by catchment similarity |  |  |  |  |  |
| era5 | reanalysis | climate | ERA5 via Open-Meteo | ERA5 cell | 86.7 | daily |  | 1940-01-01 to 2026-09-14 |  |

- No catalog gauge within 50 km; the nearest is La Nivelle à Ciboure (hubeau_hydrometrie/S516001001) at 823 km.
- 10 donor gauges from a pool of 34,786 gauged catchments.
- ERA5 temperature and forcing and GloFAS discharge are assumed reachable for any point on land (Open-Meteo); not checked here.
- CMIP6 change factors need model output you supply (aquascope.climate works on downloaded data); not counted.
- No gauge with a usable record within 50 km: at-site methods are not defensible; what remains is the regionalisation path (similar_basins, regionalize_signatures) and the GloFAS cross-check.

## Methodology

Objective: Estimate whether an ungauged stream in the Sintra hills can sustain a 4 ML/day (0.0463 m3/s) run-of-river abstraction for a village, and how reliably, using regionalisation since no gauge exists within 50 km of the site..

1. Delineate the contributing catchment at the site from BasinATLAS to fix the upstream area needed to convert regionalised flow signatures from mm/d to m3/s.
2. Identify donor gauges whose catchments most resemble the site's attributes, since no at-site discharge record exists within 50 km.
3. Transfer flow signatures (mean, median, Q95, Q05) from the donor set to the site, quantifying the transfer with a band and leave-one-out skill.
4. Screen the 4 ML/day demand against the transferred flow-duration points and the 10 percent share-of-flow rule, keeping Q95 as reserve, to read off the percent of time the demand can be met without storage.
5. Report the abstraction as a fraction of daily flow and the resulting reliability as a band bounded by the donor transfer's own uncertainty.

Step s1: `describe_catchment(lat=38.8, lon=-9.38, upstream=True)`; gates: not_empty on sub_basin; max_area_km2 478.7 on sub_basin.up_area.

Step s2: `similar_basins(lat=38.8, lon=-9.38, k=10)`, method similar_basins; gates: min_donors 3 on k; not_empty on stations.

Step s3: `regionalize_signatures(lat=38.8, lon=-9.38, k=10, method='similarity')`, method regionalize_signatures; gates: not_empty on estimates; not_empty on skill.

Step s4: `supply_reliability(lat=38.8, lon=-9.38, demand_m3s=0.0463, demand_ml_day=4.0, share=0.1, reserve='q95')`, method regionalize_signatures; gates: not_empty on reliability; not_empty on fdc.

Assumptions: catchment delineation from BasinATLAS (HydroATLAS v1.0), HYBAS id 2120018870, upstream area 478.7 km2, taken as the contributing area at the site; flow regime estimated via regionalize_signatures and similar_basins using the 10 donor gauges identified in the catalog, since no discharge record exists at this site or within 50 km; GloFAS reanalysis discharge at this point used as an independent cross-check on the regionalised estimate; share of flow (10 percent of daily flow) used as the default screening threshold for a safe abstraction, per the playbook default; no storage or regulation at the offtake, consistent with the client's description of run-of-river supply; 1 ML/day equals 0.01157 m3/s, so 4 ML/day equals about 0.0463 m3/s; Catchment delineation from BasinATLAS (HydroATLAS v1.0), HYBAS id 2120018870, upstream area 478.7 km2, taken as the contributing area at the site.; No gauge within 50 km (nearest hubeau_hydrometrie/S516001001 at 823 km) rules out at-site methods; the regionalisation path (similar_basins, regionalize_signatures) is the only defensible route.; 10 percent of daily flow is used as the default screening share, per the playbook default, with Q95 kept in the river as environmental reserve.; No storage or regulation at the offtake, consistent with the client's description of run-of-river supply.; 1 ML/day equals 0.01157 m3/s, so 4 ML/day equals about 0.0463 m3/s..

Alternatives considered: flow_duration (at-site, via analyze_station): no discharge record at this site or within 50 km; sufficiency table marks flow_duration not_defensible here; gr4j_calibration: no discharge record at this site to calibrate against; not_defensible; baseflow_separation: no discharge record at this site; not_defensible; low_flow_frequency (at-site): no discharge record at this site; not_defensible.

## Results: step s1

The catchment (BasinATLAS): upstream area 478.7 km2, mean elevation 44 m, aridity index (P/PET) 0.8 P/PET, degree of regulation by reservoirs 0 %. Gates: not_empty passed ('sub_basin' is present); max_area_km2 passed (catchment of 479 km2 against a ceiling of 479 km2).

![The site, in longitude and latitude (no basemap); no catalogue station was listed with it.](figures/s1_site_map.png)
*The site, in longitude and latitude (no basemap); no catalogue station was listed with it.*

*Catchment attributes from BasinATLAS for the site at 38.80 N, 9.38 W.*

| attribute | label | value | unit | source | note |
| --- | --- | --- | --- | --- | --- |
| n_sub_basins |  | 1.0 |  |  |  |
| area_km2 |  | 478.5 |  |  |  |
| outlet_hybas_id |  | 2120018870.0 |  |  |  |
| upstream_area_km2 |  | 478.7 |  |  |  |
| elevation_m | mean elevation | 44.0 | m | basinatlas_upstream |  |
| slope_deg | mean slope | 4.0 | degrees | basinatlas_upstream |  |
| precipitation_mm_yr | annual precipitation (WorldClim) | 751.0 | mm/yr | basinatlas_upstream |  |
| pet_mm_yr | annual potential evapotranspiration | 939.0 | mm/yr | basinatlas_upstream |  |
| aet_mm_yr | annual actual evapotranspiration | 575.0 | mm/yr | basinatlas_upstream |  |
| aridity_index | aridity index (P/PET) | 0.8 | P/PET | basinatlas_upstream |  |
| temperature_c | mean annual air temperature | 15.9 | °C | basinatlas_upstream |  |
| snow_cover_pct | annual snow cover extent | 1.0 | % | basinatlas_upstream |  |
| runoff_mm_yr | annual land-surface runoff | 252.0 | mm/yr | sub_basin |  |
| discharge_m3s | mean annual natural discharge at the outlet | 3.83 | m3/s | basinatlas_upstream |  |
| forest_pct | forest cover | 39.0 | % | basinatlas_upstream |  |
| cropland_pct | cropland | 18.0 | % | basinatlas_upstream |  |
| pasture_pct | pasture | 3.0 | % | basinatlas_upstream |  |
| urban_pct | urban extent | 48.0 | % | basinatlas_upstream |  |
| irrigated_pct | irrigated area | 0.0 | % | basinatlas_upstream |  |
| glacier_pct | glacier extent | 0.0 | % | basinatlas_upstream |  |
| wetland_pct | wetlands (all classes) | 1.0 | % | basinatlas_upstream |  |
| lake_pct | lake area | 0.0 | % | basinatlas_upstream |  |
| karst_pct | karst extent | 30.0 | % | basinatlas_upstream |  |
| clay_pct | clay fraction in soil | 20.0 | % | basinatlas_upstream |  |
| silt_pct | silt fraction in soil | 32.0 | % | basinatlas_upstream |  |
| sand_pct | sand fraction in soil | 48.0 | % | basinatlas_upstream |  |
| soil_organic_carbon_t_ha | soil organic carbon | 35.0 | t/ha | basinatlas_upstream |  |
| soil_water_pct | annual soil water content | 67.0 | % | basinatlas_upstream |  |
| groundwater_table_cm | groundwater table depth | 246.0 | cm | sub_basin |  |
| population_density | population density | 2460.12 | people/km2 | basinatlas_upstream |  |
| population | population count | 1368709.96 | people | basinatlas_upstream |  |
| degree_of_regulation_pct | degree of regulation by reservoirs | 0.0 | % | basinatlas_upstream |  |
| human_footprint_2009 | human footprint (2009) | 38.7 | index 0-50 | basinatlas_upstream |  |
| reservoir_volume_mcm | reservoir volume upstream | 0.0 | million m3 | basinatlas_upstream |  |

## Results: step s2

10 donor gauges by combined: Le Gave d'Oloron [Le Gave d'Ossau] à Oloron-Sainte-Marie - Quartier Sestiaa (hubeau_hydrometrie Q614292002), Le Luy du Béarn à Saint-Médard (hubeau_hydrometrie Q335401001), Le Luy à Saint-Pandelon (hubeau_hydrometrie Q346401001), La Nivelle à Ciboure (hubeau_hydrometrie S516001001), La Nive à Villefranque (hubeau_hydrometrie Q933251001). Gates: min_donors passed (10 donors, 3 needed); not_empty passed ('stations' is present).

![The site and the 10 donor gauges the similarity search selected, in longitude and latitude (no basemap); labels are the station ids.](figures/s2_donors_map.png)
*The site and the 10 donor gauges the similarity search selected, in longitude and latitude (no basemap); labels are the station ids.*

*Donor gauges selected for the site at 38.80 N, 9.38 W.*

| source | station_id | name | latitude | longitude | distance_km | score | similarity_distance | up_area_km2 | period_start | period_end |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hubeau_hydrometrie | Q614292002 | Le Gave d'Oloron [Le Gave d'Ossau] à Oloron-Sainte-Marie - Quartier Sestiaa | 43.191760961 | -0.604709963 | 882.9 | 1.8255 | 0.463 | 1184.1 | 2011-11-17 |  |
| hubeau_hydrometrie | Q335401001 | Le Luy du Béarn à Saint-Médard | 43.529796146 | -0.619116123 | 901.7 | 1.8854 | 0.5504 | 319.8 | 1969-08-27 |  |
| hubeau_hydrometrie | Q346401001 | Le Luy à Saint-Pandelon | 43.676839536 | -1.04192191 | 882.5 | 1.8945 | 0.6884 | 1213.1 | 1967-01-01 |  |
| hubeau_hydrometrie | S516001001 | La Nivelle à Ciboure | 43.384770372 | -1.66398305 | 822.8 | 1.9088 | 0.9671 | 239.8 | 2000-05-22 |  |
| hubeau_hydrometrie | Q933251001 | La Nive à Villefranque | 43.432791065 | -1.456860164 | 839.5 | 1.9133 | 0.9172 | 998.7 | 2008-06-26 |  |
| hubeau_hydrometrie | Q935001001 | L'Adour à Anglet [Convergent] | 43.527353493 | -1.514822499 | 841.8 | 1.9136 | 0.9093 | 16831.2 | 1999-06-16 |  |
| hubeau_hydrometrie | Q935002001 | L'Adour à Bayonne [Lesseps] - Lesseps | 43.497579072 | -1.479417197 | 842.2 | 1.914 | 0.909 | 16831.2 | 1998-11-04 |  |
| hubeau_hydrometrie | Q935251001 | La Nive à Bayonne [Pont Blanc] - Pont-Blanc | 43.477828356 | -1.472382671 | 841.4 | 1.9172 | 0.9187 | 998.7 | 2006-08-12 |  |
| hubeau_hydrometrie | Q022501101 | L'Echez à Tarbes | 43.23728759 | 0.048674918 | 931.4 | 1.9195 | 0.4628 | 134.4 | 1992-05-15 |  |
| hubeau_hydrometrie | Q022501001 | La Gespe à Tarbes [Route de Lourdes] | 43.216477891 | 0.05499409 | 930.8 | 1.92 | 0.4705 | 134.4 | 1986-06-15 |  |

## Results: step s3

Signatures transferred from 1155 donors (similarity): mean daily flow 0.1316 mm/d (band 0.0162 to 1.068); low flow: exceeded 95 % of days 0.0242 mm/d (band 0.0027 to 0.2187); high flow: exceeded 5 % of days 0.3869 mm/d (band 0.0429 to 3.486); mean annual daily maximum 0.8084 mm/d (band 0.0708 to 9.236); mean flow / BasinATLAS precipitation 0.2498 - (band 0.0222 to 0.4773), leave-one-out NSE -0.027; baseflow / total flow 0.7386 - (band 0.5823 to 0.8949), leave-one-out NSE 0.33. Gates: not_empty passed ('estimates' is present); not_empty passed ('skill' is present).

![Flow signatures transferred to the site from 10 donor catchments, with the one-standard-deviation band across donors as error bars and the leave-one-out skill (NSE) where published.](figures/s3_signatures_band.png)
*Flow signatures transferred to the site from 10 donor catchments, with the one-standard-deviation band across donors as error bars and the leave-one-out skill (NSE) where published.*

*Flow signatures at the site at 38.80 N, 9.38 W.*

| signature | label | value | low | high | unit | n_donors | nse |
| --- | --- | --- | --- | --- | --- | --- | --- |
| q_mean_mm | mean daily flow | 0.1316 | 0.0162 | 1.0683 | mm/d | 10 |  |
| q_median_mm | median daily flow | 0.0791 | 0.0103 | 0.6072 | mm/d | 10 |  |
| q95_mm | low flow: exceeded 95 % of days | 0.0242 | 0.0027 | 0.2187 | mm/d | 10 |  |
| q05_mm | high flow: exceeded 5 % of days | 0.3869 | 0.0429 | 3.4863 | mm/d | 10 |  |
| q_annual_max_mm | mean annual daily maximum | 0.8084 | 0.0708 | 9.2355 | mm/d | 10 |  |
| runoff_ratio | mean flow / BasinATLAS precipitation | 0.2498 | 0.0222 | 0.4773 | - | 10 | -0.027 |
| baseflow_index | baseflow / total flow | 0.7386 | 0.5823 | 0.8949 | - | 10 | 0.33 |
| fdc_slope | slope of the flow-duration curve (log space, 33-66 %) | 2.3492 | 1.2893 | 3.4092 | - | 10 | 0.169 |
| high_flow_frequency | days above 3 x median per year | 45.7318 | 17.2689 | 74.1946 | days/yr | 10 | 0.263 |
| low_flow_frequency | days below 0.2 x median per year | 14.5541 | 0.0 | 33.7549 | days/yr | 10 | 0.269 |
| zero_flow_fraction | fraction of zero-flow days | 0.0032 | 0.0 | 0.0095 | - | 10 | -0.087 |
| seasonality_index | Markham seasonality of monthly flow | 0.3113 | 0.1647 | 0.4578 | - | 10 | 0.332 |
| flashiness_index | Richards-Baker flashiness | 0.2502 | 0.0445 | 0.4559 | - | 10 | 0.421 |

*Donor gauges selected for the site at 38.80 N, 9.38 W.*

| source | station_id | name | latitude | longitude | distance_km | score | similarity_distance | up_area_km2 | period_start | period_end |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| uk_ea | 2134c5d5-e2bb-4c03-bde5-f39a082e2b95 | Connolly'S Mill Combined | 51.419659 | -0.18127 |  | 0.6131 | 0.6131 | 187.7 | 1962-10-01 |  |
| uk_ea | 024f218d-9a70-43b7-8ea2-7d038eeb2cff | Esher | 51.382361 | -0.376781 |  | 0.6241 | 0.6241 | 479.2 | 1984-12-18 |  |
| uk_ea | 7569bff4-df95-4bac-aec1-cc051cb0e77f | Leatherhead | 51.294985 | -0.336089 |  | 0.6265 | 0.6265 | 479.2 | 1986-11-12 |  |
| uk_ea | 649eb398-029b-4ebc-bb4d-e36ee07c234e | Bromley | 51.394815 | 0.016923 |  | 0.6309 | 0.6309 | 173.2 | 2006-12-28 |  |
| uk_ea | 3ab02013-e0a1-4215-96f2-22f078b21f21 | Hawley | 51.424331 | 0.2312 |  | 0.6395 | 0.6395 | 251.8 | 1963-12-01 |  |
| uk_ea | 5d03a6ea-4229-4687-a492-2ba63b35a4ed | Poynings | 50.893423 | -0.204661 |  | 0.6531 | 0.6531 | 391.3 | 1999-05-21 |  |
| uk_ea | 0ee042cb-d2b3-497b-9305-2ac0a8960696 | Denham Lodge Main | 51.567599 | -0.49112 |  | 0.6651 | 0.6651 | 898.2 | 1986-11-01 |  |
| uk_ea | 3769621b-8599-4bcf-b5f9-1017619dbed2 | Staines Ash | 51.440376 | -0.512035 |  | 0.6736 | 0.6736 | 973.6 | 1995-06-29 |  |
| uk_ea | 77d381c3-f098-4b67-b0d5-0e08a548fe0e | Greenford | 51.527366 | -0.344873 |  | 0.6749 | 0.6749 | 169.6 | 1988-11-30 |  |
| uk_ea | 64118c69-e564-40c3-9fec-0e6047e955b9 | Loughton | 51.640481 | 0.081584 |  | 0.6771 | 0.6771 | 352.0 | 1971-12-01 |  |

## Results: step s4

No gauge: from 1155 donor catchments (similarity) over an upstream area of 478.7 km2, the flow exceeded 95 % of the time is about 0.3297 m3/s (band 0.03269 to 3.327 m3/s), the median 1.201 m3/s. A demand of 0.0463 m3/s with Q95 kept in the river and at most 10 % of the flow taken needs 0.463 m3/s in the river, exceeded about 83.2 % of the time (band 30.1 to 94.1 %); verdict: seasonal shortfalls. Gates: not_empty passed ('reliability' is present); not_empty FAILED (nothing at 'fdc'). The fallback similar_basins ran and did not pass its gates. 5 donor gauges by similarity: Le Las [Le Las] au Revest-les-Eaux - Mesure du débit réservé - Barrage de Dardennes (hubeau_hydrometrie Y452000102), Le Lez à Montpellier - Trinquat (hubeau_hydrometrie Y321002101), Le Lez à Lattes [3ème écluse] (hubeau_hydrometrie Y321002001), La Mosson à Saint-Jean-de-Védas (hubeau_hydrometrie Y314001001), Le Lez [source] à Saint-Clément-de-Rivière (hubeau_hydrometrie Y320001001).

![The site and the 5 donor gauges the similarity search selected, in longitude and latitude (no basemap); labels are the station ids.](figures/s4.fallback_donors_map.png)
*The site and the 5 donor gauges the similarity search selected, in longitude and latitude (no basemap); labels are the station ids.*

*Supply reliability at the site at 38.80 N, 9.38 W.*

| item | value |
| --- | --- |
| demand_m3s | 0.0463 |
| demand_given_as | m3/s |
| share | 0.1 |
| unit | m3/s |
| mode | regional |
| latitude | 38.8 |
| longitude | -9.38 |
| area_km2 | 478.7 |
| signatures_m3s.q95.value | 0.32966030092592585 |
| signatures_m3s.q95.low | 0.03268900462962963 |
| signatures_m3s.q95.high | 3.327075810185185 |
| signatures_m3s.q95.n_donors | 5 |
| signatures_m3s.q50.value | 1.2006283564814815 |
| signatures_m3s.q50.low | 0.21109340277777777 |
| signatures_m3s.q50.high | 6.836434375 |
| signatures_m3s.q50.n_donors | 5 |
| signatures_m3s.q05.value | 5.6529815972222215 |
| signatures_m3s.q05.low | 1.2416281249999999 |
| signatures_m3s.q05.high | 25.74176006944444 |
| signatures_m3s.q05.n_donors | 5 |
| signatures_m3s.q_mean.value | 1.913137847222222 |
| signatures_m3s.q_mean.low | 0.3800789351851851 |
| signatures_m3s.q_mean.high | 9.62829699074074 |
| signatures_m3s.q_mean.n_donors | 5 |
| n_donors | 1155 |
| regionalisation_method | similarity |
| reserve_rule | Q95 kept in the river |
| reserve_m3s | 0.32966030092592585 |
| required_flow_m3s | 0.46299999999999997 |
| reliability.daily | 0.8317450688475874 |
| reliability.low | 0.30052698976370745 |
| reliability.high | 0.9413644542402462 |
| reliability.basis | exceedance of the required flow read off the transferred Q95, median and Q05 (log-linear); at most 0.95 and at least 0.05 can be read from three points |
| verdict | seasonal shortfalls |
| text | From 1155 donor catchments the flow exceeded 95 % of the time is about 0.32966 m3/s (band 0.03268900462962963 to 3.327075810185185); the 0.0463 m3/s demand needs the river to carry 0.46299999999999997 m3/s, exceeded about 83% of the time. |
| reliability.daily | 0.8317450688475874 |
| reliability.low | 0.30052698976370745 |
| reliability.high | 0.9413644542402462 |
| reliability.basis | exceedance of the required flow read off the transferred Q95, median and Q05 (log-linear); at most 0.95 and at least 0.05 can be read from three points |
| signatures_m3s.q95.value | 0.32966030092592585 |
| signatures_m3s.q95.low | 0.03268900462962963 |
| signatures_m3s.q95.high | 3.327075810185185 |
| signatures_m3s.q95.n_donors | 5 |
| signatures_m3s.q50.value | 1.2006283564814815 |
| signatures_m3s.q50.low | 0.21109340277777777 |
| signatures_m3s.q50.high | 6.836434375 |
| signatures_m3s.q50.n_donors | 5 |
| signatures_m3s.q05.value | 5.6529815972222215 |
| signatures_m3s.q05.low | 1.2416281249999999 |
| signatures_m3s.q05.high | 25.74176006944444 |

*Donor gauges selected for the site at 38.80 N, 9.38 W.*

| source | station_id | name | latitude | longitude | distance_km | score | similarity_distance | up_area_km2 | period_start | period_end |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hubeau_hydrometrie | Y452000102 | Le Las [Le Las] au Revest-les-Eaux - Mesure du débit réservé - Barrage de Dardennes | 43.173831793 | 5.930455437 |  | 0.2379 | 0.2379 | 405.8 | 2021-06-24 |  |
| hubeau_hydrometrie | Y321002101 | Le Lez à Montpellier - Trinquat | 43.592487899 | 3.904095942 |  | 0.2663 | 0.2663 | 196.8 | 2022-05-18 |  |
| hubeau_hydrometrie | Y321002001 | Le Lez à Lattes [3ème écluse] | 43.562967873 | 3.895080838 |  | 0.2663 | 0.2663 | 196.8 | 2008-02-02 |  |
| hubeau_hydrometrie | Y314001001 | La Mosson à Saint-Jean-de-Védas | 43.552503815 | 3.821010639 |  | 0.2729 | 0.2729 | 367.4 | 1980-09-30 |  |
| hubeau_hydrometrie | Y320001001 | Le Lez [source] à Saint-Clément-de-Rivière | 43.716477128 | 3.847281832 |  | 0.3108 | 0.3108 | 196.8 | 1986-02-01 |  |

## Limitations and what this study does not establish

- Step s4, gate not_empty: nothing at 'fdc'
- Step s4.fallback, gate min_donors: no donor count at 'k'

Caveats, verbatim from the playbook:
- A screening rule, not a licence assessment: Q95 kept in the river and at most the stated share of the flow taken are assumptions in the tradition of flow-duration-curve environmental-flow practice (Smakhtin and Eriyagama 2008; Acreman and Dunbar 2004); the regulator's flow standard, return flows, upstream abstractions and storage are not in the number.
- Reliability read off the record describes the years on record; a changing climate, new upstream abstraction or a drier decade than any recorded moves it.
- Every transferred flow is quoted with its band across donors and the leave-one-out skill; three flow-duration points give the reliability to within that band and not beyond it, and a bare regionalised reliability is not an estimate.

Expected at planning:
- A screening rule, not a licence assessment: Q95 kept in the river and at most the stated share of flow taken follow flow-duration-curve environmental-flow practice, not a regulator's formal standard.
- Reliability is quoted with its cross-donor band and leave-one-out skill; three transferred flow-duration points give the reliability to within that band and not beyond it.
- The estimate describes the regionalised long-term regime; a changing climate, new upstream abstraction, or a drier decade than any donor's record would move the answer.
- No return flows, upstream abstractions, dams or storage are represented at this ungauged site beyond the zero-dams catchment attribute.

## What this study does not establish

- Step s4, gate not_empty: nothing at 'fdc'
- Step s4.fallback, gate min_donors: no donor count at 'k'

## Caveats

- A screening rule, not a licence assessment: Q95 kept in the river and at most the stated share of the flow taken are assumptions in the tradition of flow-duration-curve environmental-flow practice (Smakhtin and Eriyagama 2008; Acreman and Dunbar 2004); the regulator's flow standard, return flows, upstream abstractions and storage are not in the number.
- Reliability read off the record describes the years on record; a changing climate, new upstream abstraction or a drier decade than any recorded moves it.
- Every transferred flow is quoted with its band across donors and the leave-one-out skill; three flow-duration points give the reliability to within that band and not beyond it, and a bare regionalised reliability is not an estimate.

## Recommendations

- Adopt this as the answer to the decision: whether the ungauged Sintra hills stream can supply a village with a 4 ML/day run-of-river abstraction, and how reliable that supply would be: mean daily flow 0.1316 mm/d (screening).
- To firm it up: supply_reliability (s4) establishing its result: gate failed: not_empty (nothing at 'fdc'); the fallback similar_basins did not pass its own gates.
- Before relying on step s4, settle the failed gate not_empty: nothing at 'fdc'. A longer record or another source would.
- Before relying on step s4.fallback, settle the failed gate min_donors: no donor count at 'k'. A longer record or another source would.
- A fallback ran after a failed gate; its numbers are indicative, not a substitute for the step that failed.

## References

1. Oudin, L. et al. (2008). Spatial proximity, physical similarity, regression and ungaged catchments. Water Resour. Res. 44, W03413.
2. Bloeschl, G., Sivapalan, M., Wagener, T., Viglione, A., Savenije, H. (eds.) (2013). Runoff Prediction in Ungauged Basins. Cambridge University Press; Oudin, L. et al. (2008). Spatial proximity, physical similarity, regression and ungaged catchments. Water Resour. Res. 44, W03413. Attributes: HydroATLAS v1.0 (BasinATLAS), CC BY 4.0. Linke, S., Lehner, B., Ouellet Dallaire, C., et al. (2019). Global hydro-environmental sub-basin and river reach characteristics at high spatial resolution. Scientific Data 6: 283. https://doi.org/10.1038/s41597-019-0300-6
3. Bloeschl, G. et al. (eds.) (2013). Runoff Prediction in Ungauged Basins. Cambridge University Press
4. Addor, N. et al. (2018). A ranking of hydrological signatures based on their predictability in space. Water Resour. Res. 54, 8792-8812.
5. Vogel, R. M. and Fennessey, N. M. (1994). Flow-duration curves I: new interpretation and confidence intervals. J. Water Resour. Plann. Manage. 120, 485-504.
6. Smakhtin, V., & Eriyagama, N. (2008). Developing a software package for global desktop assessment of environmental flows. Environ. Model. Softw. 23, 1396-1406
7. Acreman, M., & Dunbar, M. J. (2004). Defining environmental river flow requirements: a review. Hydrol. Earth Syst. Sci. 8, 861-876.
8. Smakhtin, V., & Eriyagama, N. (2008). Developing a software package for global desktop assessment of environmental flows. Environ. Model. Softw. 23, 1396-1406. doi:10.1016/j.envsoft.2008.04.002
9. Smakhtin, V. U. (2001). Low flow hydrology: a review. J. Hydrol. 240, 147-186.
10. Lyne, V., & Hollick, M. (1979). Stochastic time-variable rainfall-runoff modelling. Inst. Eng. Aust. Natl. Conf. Publ. 79/10, 89-93.
11. National-scale validation of donor regionalisation: Hydrol. Earth Syst. Sci. 28 (2024), doi:10.5194/hess-28-3367-2024
12. Rekin226 and contributors (2026). AquaScope: Open-source water data aggregation toolkit (version 0.16.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.21903143

## Appendix: reproducibility

Re-run the same steps with no model: `aquascope run study.yaml`. Resume the workspace: `aquascope studio --resume workspace.json`.

Model: claude-sonnet-5 via anthropic; ledger: consultant 1 call(s), 4248 tokens, methodologist 2 call(s), 21198 tokens, analyst 1 call(s), 4465 tokens, interpreter 0 call(s), 0 tokens, author 1 call(s), 37847 tokens, critic 1 call(s), 36147 tokens. aquascope 0.16.0.

```yaml
# An AquaScope study (version 3): the plan behind an answer, its gates, and what happened.
#   aquascope run study.yaml
version: 3
title: "Estimate whether an ungauged stream in the Sintra hills can : 38.8, -9.38"
question: "A stream in the Sintra hills near Lisbon with no gauge: can it supply a village with 4 ML/day run of river, and how reliably?"
created: "2026-09-14T16:54:24+00:00"
aquascope_version: "0.16.0"
author: "methodologist"
model: "claude-sonnet-5"
problem:
  kind: "supply_reliability"
  site: {"lat": 38.8, "lon": -9.38}
  params: {"demand_m3s": 0.0463, "demand_ml_day": 4.0, "use": "municipal", "share": 0.1, "storage": false}
  text: "A stream in the Sintra hills near Lisbon with no gauge: can it supply a village with 4 ML/day run of river, and how reliably?"
plan:
  author: "methodologist"
  playbook: "supply_reliability"
  objective: "Estimate whether an ungauged stream in the Sintra hills can sustain a 4 ML/day (0.0463 m3/s) run-of-river abstraction for a village, and how reliably, using regionalisation since no gauge exists within 50 km of the site."
  decision: "whether the ungauged Sintra hills stream can supply the village's 4 ML/day run-of-river demand, and how reliably, expressed as a band across donor-transferred flow duration points rather than a single number"
  methodology: ["Delineate the contributing catchment at the site from BasinATLAS to fix the upstream area needed to convert regionalised flow signatures from mm/d to m3/s.", "Identify donor gauges whose catchments most resemble the site's attributes, since no at-site discharge record exists within 50 km.", "Transfer flow signatures (mean, median, Q95, Q05) from the donor set to the site, quantifying the transfer with a band and leave-one-out skill.", "Screen the 4 ML/day demand against the transferred flow-duration points and the 10 percent share-of-flow rule, keeping Q95 as reserve, to read off the percent of time the demand can be met without storage.", "Report the abstraction as a fraction of daily flow and the resulting reliability as a band bounded by the donor transfer's own uncertainty."]
  assumptions: ["catchment delineation from BasinATLAS (HydroATLAS v1.0), HYBAS id 2120018870, upstream area 478.7 km2, taken as the contributing area at the site", "flow regime estimated via regionalize_signatures and similar_basins using the 10 donor gauges identified in the catalog, since no discharge record exists at this site or within 50 km", "GloFAS reanalysis discharge at this point used as an independent cross-check on the regionalised estimate", "share of flow (10 percent of daily flow) used as the default screening threshold for a safe abstraction, per the playbook default", "no storage or regulation at the offtake, consistent with the client's description of run-of-river supply", "1 ML/day equals 0.01157 m3/s, so 4 ML/day equals about 0.0463 m3/s", "Catchment delineation from BasinATLAS (HydroATLAS v1.0), HYBAS id 2120018870, upstream area 478.7 km2, taken as the contributing area at the site.", "No gauge within 50 km (nearest hubeau_hydrometrie/S516001001 at 823 km) rules out at-site methods; the regionalisation path (similar_basins, regionalize_signatures) is the only defensible route.", "10 percent of daily flow is used as the default screening share, per the playbook default, with Q95 kept in the river as environmental reserve.", "No storage or regulation at the offtake, consistent with the client's description of run-of-river supply.", "1 ML/day equals 0.01157 m3/s, so 4 ML/day equals about 0.0463 m3/s."]
  alternatives: [{"method": "flow_duration (at-site, via analyze_station)", "why_not": "no discharge record at this site or within 50 km; sufficiency table marks flow_duration not_defensible here"}, {"method": "gr4j_calibration", "why_not": "no discharge record at this site to calibrate against; not_defensible"}, {"method": "baseflow_separation", "why_not": "no discharge record at this site; not_defensible"}, {"method": "low_flow_frequency (at-site)", "why_not": "no discharge record at this site; not_defensible"}]
  limitations_expected: ["A screening rule, not a licence assessment: Q95 kept in the river and at most the stated share of flow taken follow flow-duration-curve environmental-flow practice, not a regulator's formal standard.", "Reliability is quoted with its cross-donor band and leave-one-out skill; three transferred flow-duration points give the reliability to within that band and not beyond it.", "The estimate describes the regionalised long-term regime; a changing climate, new upstream abstraction, or a drier decade than any donor's record would move the answer.", "No return flows, upstream abstractions, dams or storage are represented at this ungauged site beyond the zero-dams catchment attribute."]
  citations: ["Vogel, R. M. and Fennessey, N. M. (1994). Flow-duration curves I: new interpretation and confidence intervals. J. Water Resour. Plann. Manage. 120, 485-504.", "Smakhtin, V., & Eriyagama, N. (2008). Developing a software package for global desktop assessment of environmental flows. Environ. Model. Softw. 23, 1396-1406. doi:10.1016/j.envsoft.2008.04.002", "Acreman, M., & Dunbar, M. J. (2004). Defining environmental river flow requirements: a review. Hydrol. Earth Syst. Sci. 8, 861-876.", "Smakhtin, V. U. (2001). Low flow hydrology: a review. J. Hydrol. 240, 147-186.", "Lyne, V., & Hollick, M. (1979). Stochastic time-variable rainfall-runoff modelling. Inst. Eng. Aust. Natl. Conf. Publ. 79/10, 89-93.", "Oudin, L. et al. (2008). Spatial proximity, physical similarity, regression and ungaged catchments. Water Resour. Res. 44, W03413.", "National-scale validation of donor regionalisation: Hydrol. Earth Syst. Sci. 28 (2024), doi:10.5194/hess-28-3367-2024", "Smakhtin and Eriyagama 2008", "Acreman and Dunbar 2004"]
  caveats: ["A screening rule, not a licence assessment: Q95 kept in the river and at most the stated share of the flow taken are assumptions in the tradition of flow-duration-curve environmental-flow practice (Smakhtin and Eriyagama 2008; Acreman and Dunbar 2004); the regulator's flow standard, return flows, upstream abstractions and storage are not in the number.", "Reliability read off the record describes the years on record; a changing climate, new upstream abstraction or a drier decade than any recorded moves it.", "Every transferred flow is quoted with its band across donors and the leave-one-out skill; three flow-duration points give the reliability to within that band and not beyond it, and a bare regionalised reliability is not an estimate."]
  rationale: "Estimate whether an ungauged stream in the Sintra hills can sustain a 4 ML/day (0.0463 m3/s) run-of-river abstraction for a village, and how reliably, using regionalisation since no gauge exists within 50 km of the site."
  recon_notes: ["No catalog gauge within 50 km; the nearest is La Nivelle \u00e0 Ciboure (hubeau_hydrometrie/S516001001) at 823 km.", "10 donor gauges from a pool of 34,786 gauged catchments.", "ERA5 temperature and forcing and GloFAS discharge are assumed reachable for any point on land (Open-Meteo); not checked here.", "CMIP6 change factors need model output you supply (aquascope.climate works on downloaded data); not counted.", "No gauge with a usable record within 50 km: at-site methods are not defensible; what remains is the regionalisation path (similar_basins, regionalize_signatures) and the GloFAS cross-check."]
  replans: [{"step": "s4", "reason": "gate failed: not_empty (nothing at 'fdc')", "fallback": {"tool": "similar_basins", "arguments": {"lat": 38.8, "lon": -9.38, "k": 5, "method": "similarity"}, "rationale": "The failed supply_reliability step had no fdc since there is no gauge record at this ungauged Sintra hills point, so a regional cross-check against donor gauges is the defensible fallback per the playbook.", "expects": [{"check": "min_donors", "path": "k"}, {"check": "not_empty", "path": "stations"}]}}]
steps:
  - tool: "describe_catchment"
    id: "s1"
    rationale: "Establishes the catchment and upstream area needed to convert regionalised signatures from mm/d to m3/s."
    arguments:
      lat: 38.8
      lon: -9.38
      upstream: true
    expects:
      - {"check": "not_empty", "path": "sub_basin"}
      - {"check": "max_area_km2", "path": "sub_basin.up_area", "value": 478.7}
    outputs: [{"kind": "figure", "id": "s1_site_map", "caption": "site map from describe_catchment"}, {"kind": "table", "id": "s1_catchment_attributes", "caption": "catchment attributes from describe_catchment"}]
  - tool: "similar_basins"
    id: "s2"
    rationale: "Selects donor gauges whose catchments most resemble this one in BasinATLAS attribute space, the basis for the regionalised transfer."
    method: "similar_basins"
    arguments:
      lat: 38.8
      lon: -9.38
      k: 10
    expects:
      - {"check": "min_donors", "path": "k", "value": 3}
      - {"check": "not_empty", "path": "stations"}
    depends_on: ["s1"]
    outputs: [{"kind": "figure", "id": "s2_donors_map", "caption": "donors map from similar_basins"}, {"kind": "table", "id": "s2_donors", "caption": "donors from similar_basins"}]
  - tool: "regionalize_signatures"
    id: "s3"
    rationale: "Transfers mean, median, Q95 and Q05 flow (mm/d, converted via upstream area to m3/s) from the donor set with a band and leave-one-out skill, giving the mean annual flow and flow-duration percentiles the brief asks for."
    method: "regionalize_signatures"
    arguments:
      lat: 38.8
      lon: -9.38
      k: 10
      method: "similarity"
    expects:
      - {"check": "not_empty", "path": "estimates"}
      - {"check": "not_empty", "path": "skill"}
    depends_on: ["s2"]
    outputs: [{"kind": "table", "id": "s3_signatures", "caption": "regionalised flow signatures (mean, Q95, Q50, Q05) from regionalize_signatures"}]
  - tool: "supply_reliability"
    id: "s4"
    rationale: "Screens the 4 ML/day demand against the regionalised flow-duration points and the 10 percent share-of-flow rule, keeping Q95 in the river, to give the percent of time the demand is met and the abstraction's share of daily flow."
    method: "regionalize_signatures"
    arguments:
      lat: 38.8
      lon: -9.38
      demand_m3s: 0.0463
      demand_ml_day: 4.0
      share: 0.1
      reserve: "q95"
    expects:
      - {"check": "not_empty", "path": "reliability"}
      - {"check": "not_empty", "path": "fdc"}
    fallback: {"step": {"tool": "similar_basins", "arguments": {"lat": 38.8, "lon": -9.38, "k": 5, "method": "similarity"}, "rationale": "The failed supply_reliability step had no fdc since there is no gauge record at this ungauged Sintra hills point, so a regional cross-check against donor gauges is the defensible fallback per the playbook.", "expects": [{"check": "min_donors", "path": "k"}, {"check": "not_empty", "path": "stations"}]}}
    depends_on: ["s2", "s3"]
    outputs: [{"kind": "figure", "id": "s4_reliability_curve", "caption": "reliability curve from supply_reliability"}, {"kind": "table", "id": "s4_reliability", "caption": "reliability (percent of time demand met) from supply_reliability"}, {"kind": "table", "id": "s4_fdc_percentiles", "caption": "fdc percentiles (Q05, Q50, Q95) from supply_reliability"}]
results:
  s1: {"ok": true, "gates": [{"check": "not_empty", "passed": true, "detail": "'sub_basin' is present"}, {"check": "max_area_km2", "passed": true, "detail": "catchment of 479 km2 against a ceiling of 479 km2"}], "summary": "latitude=38.8, longitude=-9.38, license=CC-BY-4.0, attribution=HydroATLAS v1.0 (BasinATLAS), CC BY 4.0. Linke, S., Lehner, B., Ouellet Dallaire, C., et al. (2019). Global hydro-environmental sub-basin", "fallback_used": false, "sha256": "9dbb0a626977d684"}
  s2: {"ok": true, "gates": [{"check": "min_donors", "passed": true, "detail": "10 donors, 3 needed"}, {"check": "not_empty", "passed": true, "detail": "'stations' is present"}], "summary": "k=10, method=combined", "fallback_used": false, "sha256": "5b2b0361728e5387"}
  s3: {"ok": true, "gates": [{"check": "not_empty", "passed": true, "detail": "'estimates' is present"}, {"check": "not_empty", "passed": true, "detail": "'skill' is present"}], "summary": "method=similarity", "fallback_used": false, "sha256": "844a31370580337d"}
  s4: {"ok": true, "gates": [{"check": "not_empty", "passed": true, "detail": "'reliability' is present"}, {"check": "not_empty", "passed": false, "detail": "nothing at 'fdc'"}], "summary": "unit=m3/s, n_donors=1155", "fallback_used": true, "sha256": "0c4a572cbe2a06c1", "failed_reason": "gate failed: not_empty (nothing at 'fdc'); the fallback similar_basins did not pass its own gates", "fallback": {"tool": "similar_basins", "arguments": {"lat": 38.8, "lon": -9.38, "k": 5, "method": "similarity"}, "ok": true, "gates": [{"check": "min_donors", "passed": false, "detail": "no donor count at 'k'"}, {"check": "not_empty", "passed": true, "detail": "'stations' is present"}], "summary": "k=5, method=similarity"}}
```

## Cite this software

AquaScope Studio (2026). AquaScope: Open-source water data aggregation toolkit (version 0.16.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.21903143


---

*{'model': 'claude-sonnet-5', 'provider': 'anthropic', 'prose': 'template', 'tokens': {'consultant': {'calls': 1, 'prompt_tokens': 3031, 'completion_tokens': 1217, 'cost_usd': 0.018232}, 'methodologist': {'calls': 2, 'prompt_tokens': 15130, 'completion_tokens': 6068, 'cost_usd': 0.09094}, 'analyst': {'calls': 1, 'prompt_tokens': 4216, 'completion_tokens': 249, 'cost_usd': 0.010922}, 'interpreter': {'calls': 0, 'prompt_tokens': 0, 'completion_tokens': 0, 'cost_usd': 0.0}, 'author': {'calls': 1, 'prompt_tokens': 28754, 'completion_tokens': 9093, 'cost_usd': 0.148438}, 'critic': {'calls': 1, 'prompt_tokens': 24235, 'completion_tokens': 11912, 'cost_usd': 0.16759}}, 'total_tokens': 103905, 'total_usd': 0.436122, 'budget': None, 'dropped': 0, 'aquascope_version': '0.16.0', 'date': '2026-09-14 17:03 UTC', 'workspace': '37875e261a1d', 'plan_author': 'methodologist', 'written_by': {'answer': 'template', 'summary': 'template', 'decision': 'template', 'findings': 'template', 'problem': 'template', 'site_data': 'template', 'methodology': 'template', 'results-s1': 'template', 'results-s2': 'template', 'results-s3': 'template', 'results-s4': 'template', 'limitations': 'template', 'recommendations': 'template', 'references': 'template', 'appendix': 'template'}}*
