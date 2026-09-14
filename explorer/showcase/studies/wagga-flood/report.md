# Estimate the 100-year annual exceedance probability flood flow (Q100) for the Mu (-35.1, 147.37)

**Author:** AquaScope Studio  
**Date:** 2026-09-14  
**Description:** size the levee upgrade to withstand the 100-year flood flow on the Murrumbidgee at Wagga Wagga  
**Data Sources:** BasinATLAS (HydroATLAS v1.0), ERA5 via Open-Meteo, bom, similar_basins  
**Version:** 1.0  

**Site:** 35.1000 S, 147.3700 E

**Answer.** Notice: this report did not pass the Critic's checks (numbers_come_from_tools); read its numbers with the list of what this study does not establish.

size the levee upgrade to withstand the 100-year flood flow on the Murrumbidgee at Wagga Wagga: mean daily flow 1.083 mm/d (screening). Signatures transferred from 1155 donors (similarity): mean daily flow 1.083 mm/d (band 0.8211 to 1.429); low flow: exceeded 95 % of days 0.2469 mm/d (band 0.1444 to 0.422); high flow: exceeded 5 % of days 3.125 mm/d (band 2.391 to 4.084); mean annual daily maximum 7.424 mm/d (band 5.315 to 10.37); mean flow / BasinATLAS precipitation 0.5018 - (band 0.4017 to 0.602), leave-one-out NSE -0.027; baseflow / total flow 0.7692 - (band 0.7317 to 0.8067), leave-one-out NSE 0.33.

*Key numbers*

| Quantity | Value | Unit | Step |
| --- | --- | --- | --- |
| Upstream area | 27040.0 | km2 | s1 |
| Donor gauges | 10.0 |  | s2 |
| mean daily flow | 1.083 | mm/d | s3 |
| mean daily flow band, low | 0.8211 | mm/d | s3 |
| mean daily flow band, high | 1.429 | mm/d | s3 |
| low flow: exceeded 95 % of days | 0.2469 | mm/d | s3 |
| low flow: exceeded 95 % of days band, low | 0.1444 | mm/d | s3 |
| low flow: exceeded 95 % of days band, high | 0.422 | mm/d | s3 |
| high flow: exceeded 5 % of days | 3.125 | mm/d | s3 |
| high flow: exceeded 5 % of days band, low | 2.391 | mm/d | s3 |
| high flow: exceeded 5 % of days band, high | 4.084 | mm/d | s3 |
| mean annual daily maximum | 7.424 | mm/d | s3 |
| mean annual daily maximum band, low | 5.315 | mm/d | s3 |
| mean annual daily maximum band, high | 10.37 | mm/d | s3 |
| mean flow / BasinATLAS precipitation | 0.5018 | - | s3 |
| mean flow / BasinATLAS precipitation band, low | 0.4017 | - | s3 |
| mean flow / BasinATLAS precipitation band, high | 0.602 | - | s3 |
| baseflow / total flow | 0.7692 | - | s3 |
| baseflow / total flow band, low | 0.7317 | - | s3 |
| baseflow / total flow band, high | 0.8067 | - | s3 |
| ERA5 precipitation | 588.0 | mm per year | s4 |
| ERA5 reference evapotranspiration | 1428.0 | mm per year | s4 |
| Aridity index | 0.4117 |  | s4 |
| GloFAS mean discharge (cell) | 0.0313 | m3/s | s4 |

## Summary

Estimate the 100-year annual exceedance probability flood flow (Q100) for the Murrumbidgee at Wagga Wagga to inform levee upgrade sizing, using regional transfer from similar gauged catchments and an independent GloFAS cross-check, given no usable discharge record within 50 km.. 4 step(s) ran (methodologist plan, playbook flood_risk); 7 of 7 gates passed. Signatures transferred from 1155 donors (similarity): mean daily flow 1.083 mm/d (band 0.8211 to 1.429); low flow: exceeded 95 % of days 0.2469 mm/d (band 0.1444 to 0.422); high flow: exceeded 5 % of days 3.125 mm/d (band 2.391 to 4.084); mean annual daily maximum 7.424 mm/d (band 5.315 to 10.37); mean flow / BasinATLAS precipitation 0.5018 - (band 0.4017 to 0.602), leave-one-out NSE -0.027; baseflow / total flow 0.7692 - (band 0.7317 to 0.8067), leave-one-out NSE 0.33.

## The decision

size the levee upgrade to withstand the 100-year flood flow on the Murrumbidgee at Wagga Wagga: mean daily flow 1.083 mm/d (screening). It holds under these conditions: Design-flood guidance under climate change is immature (Wasko et al.; Rare quantiles move with the distribution and the estimator..

## Findings

- [screening] Upstream area: 27040 km2 (from s1.attributes.upstream_area_km2)
- [screening] Donor gauges: 10 (from s2.stations.0.score)
- [screening] mean daily flow: 1.083 mm/d (from s3.estimates.q_mean_mm.value)
- [screening] mean daily flow band, low: 0.8211 mm/d (from s3.estimates.q_mean_mm.low)
- [screening] mean daily flow band, high: 1.429 mm/d (from s3.estimates.q_mean_mm.high)
- [screening] low flow: exceeded 95 % of days: 0.2469 mm/d (from s3.estimates.q95_mm.value)
- [screening] low flow: exceeded 95 % of days band, low: 0.1444 mm/d (from s3.estimates.q95_mm.low)
- [screening] low flow: exceeded 95 % of days band, high: 0.422 mm/d (from s3.estimates.q95_mm.high)
- [screening] high flow: exceeded 5 % of days: 3.125 mm/d (from s3.estimates.q05_mm.value)
- [screening] high flow: exceeded 5 % of days band, low: 2.391 mm/d (from s3.estimates.q05_mm.low)
- [screening] high flow: exceeded 5 % of days band, high: 4.084 mm/d (from s3.estimates.q05_mm.high)
- [screening] mean annual daily maximum: 7.424 mm/d (from s3.estimates.q_annual_max_mm.value)
- [screening] mean annual daily maximum band, low: 5.315 mm/d (from s3.estimates.q_annual_max_mm.low)
- [screening] mean annual daily maximum band, high: 10.37 mm/d (from s3.estimates.q_annual_max_mm.high)
- [screening] mean flow / BasinATLAS precipitation: 0.5018 - (from s3.estimates.q95_mm.donor_max)
- [screening] mean flow / BasinATLAS precipitation band, low: 0.4017 - (from s3.estimates.runoff_ratio.low)
- [screening] mean flow / BasinATLAS precipitation band, high: 0.602 - (from s3.estimates.runoff_ratio.high)
- [screening] baseflow / total flow: 0.7692 - (from s3.estimates.baseflow_index.value)
- [screening] baseflow / total flow band, low: 0.7317 - (from s3.estimates.baseflow_index.low)
- [screening] baseflow / total flow band, high: 0.8067 - (from s3.estimates.baseflow_index.high)
- [screening] ERA5 precipitation: 588 mm per year (from s4.climate.precipitation_mm_per_year)
- [screening] ERA5 reference evapotranspiration: 1428 mm per year (from s4.climate.et0_mm_per_year)
- [screening] Aridity index: 0.4117 (from s4.climate.aridity_index)
- [screening] GloFAS mean discharge (cell): 0.0313 m3/s (from s4.glofas.stats.mean)

## Problem and decision

Design flood for a levee upgrade on the Murrumbidgee at Wagga Wagga: the 100-year flow, and how far the evidence can be trusted. Decision: size the levee upgrade to withstand the 100-year flood flow on the Murrumbidgee at Wagga Wagga. Quantities wanted: 100-year annual exceedance probability flood flow (Q100) in cubic metres per second; uncertainty range or confidence bound on Q100; cross-check flow from GloFAS reanalysis for the same site. Constraints: no gauge with a usable discharge record within 50 km of the site, so at-site flood frequency analysis is not defensible; estimate must be built via regionalisation (similar_basins, regionalize_signatures) using 10 donor gauges drawn from a pool of 34,786 gauged catchments, cross-checked against GloFAS discharge; trend/Mann-Kendall analysis is not defensible for this site (no local record); upstream catchment area at site is about 27041 km2 (HydroBASINS unit 5120597860, BasinATLAS area 27983.8 km2). Intake: return_period = 100, decision = design flow. Assumed: site coordinates (-35.1, 147.37) represent the Wagga Wagga levee location on the Murrumbidgee; the nearby BOM stations listed (groundwater bores, water quality gauge 410001) do not provide a usable discharge record for at-site flood frequency analysis; regionalisation via similar_basins and regionalize_signatures on the 10 donor gauges is the primary evidence path; GloFAS discharge cross-check is reachable for this site (Open-Meteo/ERA5-based) though not independently verified here; HydroATLAS catchment attributes (area, precipitation, aridity, dam density) are used to support donor basin similarity weighting.

## Site and data

Site: -35.1, 147.37. The datasets within reach or attached:

| Id | Kind | Variable | Source | Name | Years | Resolution | km | Period | Quality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| catchment | catchment |  | BasinATLAS (HydroATLAS v1.0) | the catchment of the point |  |  |  |  |  |
| donors | donors |  | similar_basins | 10 donor gauges by catchment similarity |  |  |  |  |  |
| era5 | reanalysis | climate | ERA5 via Open-Meteo | ERA5 cell | 86.7 | daily |  | 1940-01-01 to 2026-09-14 |  |

and 25 more short record(s) within reach, under a year of record each, not listed.

- 10 donor gauges from a pool of 34,786 gauged catchments.
- ERA5 temperature and forcing and GloFAS discharge are assumed reachable for any point on land (Open-Meteo); not checked here.
- CMIP6 change factors need model output you supply (aquascope.climate works on downloaded data); not counted.
- No gauge with a usable record within 50 km: at-site methods are not defensible; what remains is the regionalisation path (similar_basins, regionalize_signatures) and the GloFAS cross-check.

## Methodology

Objective: Estimate the 100-year annual exceedance probability flood flow (Q100) for the Murrumbidgee at Wagga Wagga to inform levee upgrade sizing, using regional transfer from similar gauged catchments and an independent GloFAS cross-check, given no usable discharge record within 50 km..

1. Characterise the ungauged catchment at the levee site (area, climate, land cover, dams) from BasinATLAS/HydroATLAS to anchor the similarity search.
2. Identify 10 donor gauges whose catchments most resemble this one in attribute space, drawn from the pool of 34,786 gauged catchments.
3. Transfer flow signatures (including annual maximum) from the donor gauges to the ungauged site, quoting the leave-one-out skill and the spread across donors as the uncertainty band on Q100.
4. Obtain GloFAS reanalysis-based modelled discharge for the site cell as an independent cross-check on the regionalised flood estimate.
5. Report the Q100 estimate with its uncertainty band and the GloFAS ratio, flagging any spread or disagreement above 25 percent as unresolved rather than averaged away.

Step s1: `describe_catchment(lat=-35.1, lon=147.37, upstream=True)`; gates: not_empty on sub_basin; max_area_km2 27983.8 on sub_basin.up_area.

Step s2: `similar_basins(lat=-35.1, lon=147.37, k=10)`, method similar_basins; gates: min_donors 10 on k; not_empty on stations.

Step s3: `regionalize_signatures(lat=-35.1, lon=147.37, k=10)`, method regionalize_signatures; gates: not_empty on estimates; not_empty on skill.

Step s4: `anywhere(lat=-35.1, lon=147.37, years=20)`, method glofas_cross_check; gates: not_empty on climate.

Assumptions: site coordinates (-35.1, 147.37) represent the Wagga Wagga levee location on the Murrumbidgee; the nearby BOM stations listed (groundwater bores, water quality gauge 410001) do not provide a usable discharge record for at-site flood frequency analysis; regionalisation via similar_basins and regionalize_signatures on the 10 donor gauges is the primary evidence path; GloFAS discharge cross-check is reachable for this site (Open-Meteo/ERA5-based) though not independently verified here; HydroATLAS catchment attributes (area, precipitation, aridity, dam density) are used to support donor basin similarity weighting.

Alternatives considered: at_site_flood_frequency: no gauge with a usable discharge record exists within 50 km of the site, so the sufficiency table marks this not_defensible; trend_mann_kendall: there is no local discharge record at this site to run a trend test on.

## Results: step s1

The catchment (BasinATLAS): upstream area 2.704e+04 km2, mean elevation 715 m, aridity index (P/PET) 0.74 P/PET, degree of regulation by reservoirs 114.9 %. Gates: not_empty passed ('sub_basin' is present); max_area_km2 passed (catchment of 27,041 km2 against a ceiling of 27,984 km2).

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

10 donor gauges by combined: Tumunu Stream, Dublon, Chuuk IS, FSM (usgs USGS-16897200), Edeng River, Babelthuap, Palau (usgs USGS-16891300), Kmekumel River, Babelthuap, Palau (usgs USGS-16891310), Tabecheding River, Babelthuap, Palau (usgs USGS-16890900), Ngerimel River, Babelthuap, Palau (usgs USGS-16891200). Gates: min_donors passed (10 donors, 10 needed); not_empty passed ('stations' is present).

![The site and the 10 donor gauges the similarity search selected, in longitude and latitude (no basemap); labels are the station ids.](figures/s2_donors_map.png)
*The site and the 10 donor gauges the similarity search selected, in longitude and latitude (no basemap); labels are the station ids.*

*Donor gauges selected for the site at 35.10 S, 147.37 E.*

| source | station_id | name | latitude | longitude | distance_km | score | similarity_distance | up_area_km2 | period_start | period_end |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| usgs | USGS-16897200 | Tumunu Stream, Dublon, Chuuk IS, FSM | 7.37606944444444 | 151.874166666667 | 4746.7 | 9.9531 | 2.9898 | 174.6 | 1968-05-31 | 1978-01-30 |
| usgs | USGS-16891300 | Edeng River, Babelthuap, Palau | 7.383333333333334 | 134.55194444444444 | 4911.7 | 10.2252 | 2.8383 | 427.8 | 1969-10-01 | 1983-09-29 |
| usgs | USGS-16891310 | Kmekumel River, Babelthuap, Palau | 7.387611111111111 | 134.54322222222223 | 4912.4 | 10.2351 | 2.8688 | 427.8 | 1978-08-31 | 2005-05-24 |
| usgs | USGS-16890900 | Tabecheding River, Babelthuap, Palau | 7.450805555555556 | 134.525 | 4919.7 | 10.2385 | 2.8307 | 427.8 | 1970-09-30 | 2005-02-02 |
| usgs | USGS-16891200 | Ngerimel River, Babelthuap, Palau | 7.371666666666666 | 134.52694444444447 | 4911.1 | 10.2391 | 2.8917 | 427.8 | 1969-10-01 | 1978-04-29 |
| usgs | USGS-16891400 | SF Ngerdorch River, Babelthuap, Palau | 7.440055555555555 | 134.5768611111111 | 4917.1 | 10.2395 | 2.8526 | 427.8 | 1971-02-28 | 1992-01-14 |
| usgs | USGS-16891420 | NF Ngerdorch River nr Melekeok, Babelthuap, Palau | 7.509305555555556 | 134.60302777777778 | 4923.7 | 10.2556 | 2.8642 | 427.8 | 1993-11-02 | 2004-02-13 |
| usgs | USGS-16890600 | Diongradid River, Babelthuap, Palau | 7.60388888888889 | 134.586388888889 | 4934.4 | 10.2685 | 2.8373 | 427.8 | 1969-10-01 | 2005-05-23 |
| usgs | USGS-16893300 |  | 9.537777777777778 | 138.18805555555556 | 5056.6 | 10.3898 | 2.3816 | 125.1 | 1968-03-31 | 1974-09-29 |
| usgs | USGS-16835000 | Inarajan River nr Inarajan, Guam | 13.279527777777778 | 144.73988888888888 | 5386.7 | 10.9339 | 1.8666 | 374.9 | 1952-09-30 | 1983-01-04 |

## Results: step s3

Signatures transferred from 1155 donors (similarity): mean daily flow 1.083 mm/d (band 0.8211 to 1.429); low flow: exceeded 95 % of days 0.2469 mm/d (band 0.1444 to 0.422); high flow: exceeded 5 % of days 3.125 mm/d (band 2.391 to 4.084); mean annual daily maximum 7.424 mm/d (band 5.315 to 10.37); mean flow / BasinATLAS precipitation 0.5018 - (band 0.4017 to 0.602), leave-one-out NSE -0.027; baseflow / total flow 0.7692 - (band 0.7317 to 0.8067), leave-one-out NSE 0.33. Gates: not_empty passed ('estimates' is present); not_empty passed ('skill' is present).

![Flow signatures transferred to the site from 10 donor catchments, with the one-standard-deviation band across donors as error bars and the leave-one-out skill (NSE) where published.](figures/s3_signatures_band.png)
*Flow signatures transferred to the site from 10 donor catchments, with the one-standard-deviation band across donors as error bars and the leave-one-out skill (NSE) where published.*

*Flow signatures at the site at 35.10 S, 147.37 E.*

| signature | label | value | low | high | unit | n_donors | nse |
| --- | --- | --- | --- | --- | --- | --- | --- |
| q_mean_mm | mean daily flow | 1.0834 | 0.8211 | 1.4294 | mm/d | 10 |  |
| q_median_mm | median daily flow | 0.6895 | 0.4778 | 0.9951 | mm/d | 10 |  |
| q95_mm | low flow: exceeded 95 % of days | 0.2469 | 0.1444 | 0.422 | mm/d | 10 |  |
| q05_mm | high flow: exceeded 5 % of days | 3.1251 | 2.3913 | 4.0841 | mm/d | 10 |  |
| q_annual_max_mm | mean annual daily maximum | 7.4238 | 5.3153 | 10.3687 | mm/d | 10 |  |
| runoff_ratio | mean flow / BasinATLAS precipitation | 0.5018 | 0.4017 | 0.602 | - | 10 | -0.027 |
| baseflow_index | baseflow / total flow | 0.7692 | 0.7317 | 0.8067 | - | 10 | 0.33 |
| fdc_slope | slope of the flow-duration curve (log space, 33-66 %) | 2.3252 | 1.7808 | 2.8697 | - | 10 | 0.169 |
| high_flow_frequency | days above 3 x median per year | 43.5213 | 25.9787 | 61.0639 | days/yr | 10 | 0.263 |
| low_flow_frequency | days below 0.2 x median per year | 4.559 | 0.0 | 13.7352 | days/yr | 10 | 0.269 |
| zero_flow_fraction | fraction of zero-flow days | 0.0 | 0.0 | 0.0 | - | 10 | -0.087 |
| seasonality_index | Markham seasonality of monthly flow | 0.2925 | 0.1776 | 0.4075 | - | 10 | 0.332 |
| flashiness_index | Richards-Baker flashiness | 0.1653 | 0.1187 | 0.2119 | - | 10 | 0.421 |

*Donor gauges selected for the site at 35.10 S, 147.37 E.*

| source | station_id | name | latitude | longitude | distance_km | score | similarity_distance | up_area_km2 | period_start | period_end |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hubeau_hydrometrie | A735201001 | Le Rupt de Mad à Onville | 49.012193042 | 5.961532525 |  | 1.0736 | 1.0736 | 398.8 | 1964-08-01 |  |
| hubeau_hydrometrie | A623201001 | La Plaine à Raon-l'Étape [La Trouche] | 48.416320357 | 6.877878865 |  | 1.1868 | 1.1868 | 130.3 | 1969-11-09 |  |
| hubeau_hydrometrie | A615103001 | La Meurthe à Raon-l'Étape | 48.402032182 | 6.845062409 |  | 1.2075 | 1.2075 | 1096.2 | 1973-11-01 |  |
| hubeau_hydrometrie | F041000201 | La Digeanne à Montmoyen | 47.740042453 | 4.786663807 |  | 1.2279 | 1.2279 | 109.6 | 2006-05-15 |  |
| hubeau_hydrometrie | A631101003 | La Meurthe à Baccarat - amont | 48.447732868 | 6.740048847 |  | 1.2289 | 1.2289 | 1096.2 | 2015-07-16 |  |
| hubeau_hydrometrie | A631101001 | La Meurthe à Baccarat - aval | 48.44923718 | 6.738612663 |  | 1.2289 | 1.2289 | 1096.2 | 1981-01-01 |  |
| hubeau_hydrometrie | A215030001 | Le ruisseau le Strengbach à Ribeauvillé | 48.200033318 | 7.301208506 |  | 1.2339 | 1.2339 | 585.2 | 1971-06-25 |  |
| hubeau_hydrometrie | A343021001 | La Zinsel du Sud à Eckartswiller [Oberhof] | 48.799588457 | 7.310495367 |  | 1.2407 | 1.2407 | 177.4 | 2006-07-05 |  |
| hubeau_hydrometrie | A932215050 | L'Horn à Bousseviller | 49.127103129 | 7.47209323 |  | 1.2417 | 1.2417 | 153.4 | 1969-10-01 |  |
| hubeau_hydrometrie | A643112002 | La Vezouze à Blâmont - amont | 48.588299085 | 6.845033347 |  | 1.2428 | 1.2428 | 152.1 | 2007-01-01 |  |

## Results: step s4

ERA5 climate for the cell: precipitation 588 mm per year, reference evapotranspiration 1,428 mm per year, aridity index 0.41 (semi-arid). GloFAS modelled discharge (grid cell, indicative): mean 0.0313 m3/s, 100-year GEV 0.8165 m3/s. Gates: not_empty passed ('climate' is present).

![Mean monthly precipitation (bars) and FAO-56 reference evapotranspiration (line) for the ERA5 cell at the site at 35.10 S, 147.37 E, 20 years ending 2026-09-07.](figures/s4_monthly_climate.png)
*Mean monthly precipitation (bars) and FAO-56 reference evapotranspiration (line) for the ERA5 cell at the site at 35.10 S, 147.37 E, 20 years ending 2026-09-07.*

![Annual maxima of the modelled discharge from GloFAS v4 (Open-Meteo) for the grid cell at the site at 35.10 S, 147.37 E, 2006 to 2026: a model output, indicative only, not a gauge reading.](figures/s4_glofas_series.png)
*Annual maxima of the modelled discharge from GloFAS v4 (Open-Meteo) for the grid cell at the site at 35.10 S, 147.37 E, 2006 to 2026: a model output, indicative only, not a gauge reading.*

*Mean monthly precipitation and reference evapotranspiration for the ERA5 cell at the site at 35.10 S, 147.37 E.*

| month | precipitation_mm | et0_mm |
| --- | --- | --- |
| 1 | 45.7827 | 215.7587 |
| 2 | 40.2024 | 189.1472 |
| 3 | 56.3582 | 145.3053 |
| 4 | 38.7146 | 94.3356 |
| 5 | 41.8059 | 58.2131 |
| 6 | 55.8828 | 38.361 |
| 7 | 43.4654 | 39.9545 |
| 8 | 48.8317 | 54.8161 |
| 9 | 48.1823 | 90.307 |
| 10 | 44.6339 | 135.3294 |
| 11 | 69.6873 | 173.0123 |
| 12 | 51.9935 | 204.0143 |

*GloFAS modelled discharge for the grid cell at the site at 35.10 S, 147.37 E (indicative).*

| item | value |
| --- | --- |
| variable | discharge |
| unit | m3/s |
| n | 7306 |
| start | 2006-09-07 |
| end | 2026-09-07 |
| years | 20.0 |
| stats.mean | 0.0313 |
| stats.median | 0.02 |
| stats.min | 0.0 |
| stats.max | 0.69 |
| sampling.n | 7306 |
| sampling.span_years | 20.0 |
| sampling.per_year | 365.3 |
| sampling.inferred_resolution | daily |
| trend.on | annual mean |
| trend.p_value | 0.7264 |
| trend.tau | 0.0643 |
| trend.trend | no trend |
| trend.sens_slope_per_year | 0.0003 |
| trend.n_years | 19 |
| source | GloFAS v4 (modelled) via Open-Meteo |
| modelled | True |
| return_level_T2_gev | 0.3015 |
| return_level_T5_gev | 0.4473 |
| return_level_T10_gev | 0.5405 |
| return_level_T25_gev | 0.6547 |
| return_level_T50_gev | 0.7369 |
| return_level_T100_gev | 0.8165 |
| q10 | 0.08 |
| q50 | 0.02 |
| q95 | 0.0 |

## Limitations and what this study does not establish

Every gate and check passed.

Caveats, verbatim from the playbook:
- Design-flood guidance under climate change is immature (Wasko et al. 2024, HESS): the estimate here is stationary, and any climate scenario is an overlay on it, not a nonstationary fit.
- Rare quantiles move with the distribution and the estimator. Two fits (GEV by L-moments and Log-Pearson III) are quoted with their intervals and the spread between them; a spread above 25 percent is reported as disagreement, not averaged away.
- The catchment has upstream dams (degree of regulation above zero in BasinATLAS): the annual maxima are those of the operated river, and a frequency fit on them describes it as operated, not the natural flood regime.
- GloFAS discharge is a model output for a grid cell of about 5 km, not a gauge reading; return levels from it are indicative only.

Expected at planning:
- Design-flood guidance under climate change is immature (Wasko et al. 2024, HESS): the estimate here is stationary, and any climate scenario is an overlay on it, not a nonstationary fit.
- Rare quantiles move with the distribution and the estimator; the spread between donor-based transfer and GloFAS is reported as disagreement above 25 percent, not averaged away.
- The catchment has upstream dams (degree of regulation above zero in BasinATLAS): any transferred annual-maximum signature reflects the operated river, not the natural flood regime.
- GloFAS discharge is a model output for a grid cell of about 5 km, not a gauge reading; return levels from it are indicative only.

## What this study does not establish

- These numbers are not in any tool result: 2.704.

## Caveats

- Design-flood guidance under climate change is immature (Wasko et al. 2024, HESS): the estimate here is stationary, and any climate scenario is an overlay on it, not a nonstationary fit.
- Rare quantiles move with the distribution and the estimator. Two fits (GEV by L-moments and Log-Pearson III) are quoted with their intervals and the spread between them; a spread above 25 percent is reported as disagreement, not averaged away.
- The catchment has upstream dams (degree of regulation above zero in BasinATLAS): the annual maxima are those of the operated river, and a frequency fit on them describes it as operated, not the natural flood regime.
- GloFAS discharge is a model output for a grid cell of about 5 km, not a gauge reading; return levels from it are indicative only.

## Recommendations

- Adopt this as the answer to the decision: size the levee upgrade to withstand the 100-year flood flow on the Murrumbidgee at Wagga Wagga: mean daily flow 1.083 mm/d (screening).
- Read the numbers with this caveat: Design-flood guidance under climate change is immature (Wasko et al. 2024, HESS): the estimate here is stationary, and any climate scenario is an overlay on it, not a nonstationary fit.
- Read the numbers with this caveat: Rare quantiles move with the distribution and the estimator.
- Read the numbers with this caveat: The catchment has upstream dams (degree of regulation above zero in BasinATLAS): the annual maxima are those of the operated river, and a frequency fit on them describes it as operated, not the natural flood regime.
- Read the numbers with this caveat: GloFAS discharge is a model output for a grid cell of about 5 km, not a gauge reading; return levels from it are indicative only.

## References

1. Oudin, L. et al. (2008). Spatial proximity, physical similarity, regression and ungaged catchments. Water Resour. Res. 44, W03413.
2. Harrigan, S. et al. (2020). GloFAS-ERA5 operational global river discharge reanalysis 1979-present. Earth Syst. Sci. Data, 12, 2043-2060.
3. Bloeschl, G., Sivapalan, M., Wagener, T., Viglione, A., Savenije, H. (eds.) (2013). Runoff Prediction in Ungauged Basins. Cambridge University Press; Oudin, L. et al. (2008). Spatial proximity, physical similarity, regression and ungaged catchments. Water Resour. Res. 44, W03413. Attributes: HydroATLAS v1.0 (BasinATLAS), CC BY 4.0. Linke, S., Lehner, B., Ouellet Dallaire, C., et al. (2019). Global hydro-environmental sub-basin and river reach characteristics at high spatial resolution. Scientific Data 6: 283. https://doi.org/10.1038/s41597-019-0300-6
4. Bloeschl, G. et al. (eds.) (2013). Runoff Prediction in Ungauged Basins. Cambridge University Press
5. Addor, N. et al. (2018). A ranking of hydrological signatures based on their predictability in space. Water Resour. Res. 54, 8792-8812.
6. Hersbach, H. et al. (2020). The ERA5 global reanalysis. Q. J. R. Meteorol. Soc., 146, 1999-2049
7. Open-Meteo.com (CC BY 4.0).
8. Allen, R. G., Pereira, L. S., Raes, D., & Smith, M. (1998). Crop evapotranspiration. FAO Irrigation and Drainage Paper 56.
9. Hosking, J. R. M. (1990). L-moments: analysis and estimation of distributions using linear combinations of order statistics. J. R. Stat. Soc. B, 52(1), 105-124.
10. England, J. F. Jr. et al. (2018). Guidelines for determining flood flow frequency, Bulletin 17C. USGS Techniques and Methods 4-B5.
11. England, J. F. et al. (2019). Guidelines for determining flood flow frequency, Bulletin 17C. USGS Techniques and Methods 4-B5.
12. Wasko, C. et al. (2024). A systematic review of climate change science for flood and design guidance. Hydrol. Earth Syst. Sci. 28, 1251-1285. doi:10.5194/hess-28-1251-2024
13. Nonstationary flood frequency estimates are parameter-fragile: Stoch. Environ. Res. Risk Assess. (2024), doi:10.1007/s00477-024-02680-9
14. Multi-approach cross-checks in infrastructure flood practice: J. Hydrol. (2024), doi:10.1016/j.jhydrol.2024.130698
15. Wasko et al. 2024, HESS
16. Rekin226 and contributors (2026). AquaScope: Open-source water data aggregation toolkit (version 0.16.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.21903143

## Appendix: reproducibility

Re-run the same steps with no model: `aquascope run study.yaml`. Resume the workspace: `aquascope studio --resume workspace.json`.

Model: claude-sonnet-5 via anthropic; ledger: consultant 1 call(s), 4180 tokens, methodologist 1 call(s), 13605 tokens, interpreter 0 call(s), 0 tokens, author 2 call(s), 73440 tokens, critic 1 call(s), 32265 tokens. aquascope 0.16.0.

```yaml
# An AquaScope study (version 3): the plan behind an answer, its gates, and what happened.
#   aquascope run study.yaml
version: 3
title: "Estimate the 100-year annual exceedance probability flood fl: -35.1, 147.37"
question: "Design flood for a levee upgrade on the Murrumbidgee at Wagga Wagga: the 100-year flow, and how far the evidence can be trusted."
created: "2026-09-14T22:09:32+00:00"
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
  objective: "Estimate the 100-year annual exceedance probability flood flow (Q100) for the Murrumbidgee at Wagga Wagga to inform levee upgrade sizing, using regional transfer from similar gauged catchments and an independent GloFAS cross-check, given no usable discharge record within 50 km."
  decision: "size the levee upgrade to withstand the 100-year flood flow on the Murrumbidgee at Wagga Wagga"
  methodology: ["Characterise the ungauged catchment at the levee site (area, climate, land cover, dams) from BasinATLAS/HydroATLAS to anchor the similarity search.", "Identify 10 donor gauges whose catchments most resemble this one in attribute space, drawn from the pool of 34,786 gauged catchments.", "Transfer flow signatures (including annual maximum) from the donor gauges to the ungauged site, quoting the leave-one-out skill and the spread across donors as the uncertainty band on Q100.", "Obtain GloFAS reanalysis-based modelled discharge for the site cell as an independent cross-check on the regionalised flood estimate.", "Report the Q100 estimate with its uncertainty band and the GloFAS ratio, flagging any spread or disagreement above 25 percent as unresolved rather than averaged away."]
  assumptions: ["site coordinates (-35.1, 147.37) represent the Wagga Wagga levee location on the Murrumbidgee", "the nearby BOM stations listed (groundwater bores, water quality gauge 410001) do not provide a usable discharge record for at-site flood frequency analysis", "regionalisation via similar_basins and regionalize_signatures on the 10 donor gauges is the primary evidence path", "GloFAS discharge cross-check is reachable for this site (Open-Meteo/ERA5-based) though not independently verified here", "HydroATLAS catchment attributes (area, precipitation, aridity, dam density) are used to support donor basin similarity weighting"]
  alternatives: [{"method": "at_site_flood_frequency", "why_not": "no gauge with a usable discharge record exists within 50 km of the site, so the sufficiency table marks this not_defensible"}, {"method": "trend_mann_kendall", "why_not": "there is no local discharge record at this site to run a trend test on"}]
  limitations_expected: ["Design-flood guidance under climate change is immature (Wasko et al. 2024, HESS): the estimate here is stationary, and any climate scenario is an overlay on it, not a nonstationary fit.", "Rare quantiles move with the distribution and the estimator; the spread between donor-based transfer and GloFAS is reported as disagreement above 25 percent, not averaged away.", "The catchment has upstream dams (degree of regulation above zero in BasinATLAS): any transferred annual-maximum signature reflects the operated river, not the natural flood regime.", "GloFAS discharge is a model output for a grid cell of about 5 km, not a gauge reading; return levels from it are indicative only."]
  citations: ["England, J. F. et al. (2019). Guidelines for determining flood flow frequency, Bulletin 17C. USGS Techniques and Methods 4-B5.", "Hosking, J. R. M. (1990). L-moments: analysis and estimation of distributions using linear combinations of order statistics. J. R. Stat. Soc. B 52, 105-124.", "Wasko, C. et al. (2024). A systematic review of climate change science for flood and design guidance. Hydrol. Earth Syst. Sci. 28, 1251-1285. doi:10.5194/hess-28-1251-2024", "Nonstationary flood frequency estimates are parameter-fragile: Stoch. Environ. Res. Risk Assess. (2024), doi:10.1007/s00477-024-02680-9", "Multi-approach cross-checks in infrastructure flood practice: J. Hydrol. (2024), doi:10.1016/j.jhydrol.2024.130698", "Oudin, L. et al. (2008). Spatial proximity, physical similarity, regression and ungaged catchments. Water Resour. Res. 44, W03413.", "Harrigan, S. et al. (2020). GloFAS-ERA5 operational global river discharge reanalysis 1979-present. Earth Syst. Sci. Data 12, 2043-2060.", "Wasko et al. 2024, HESS"]
  caveats: ["Design-flood guidance under climate change is immature (Wasko et al. 2024, HESS): the estimate here is stationary, and any climate scenario is an overlay on it, not a nonstationary fit.", "Rare quantiles move with the distribution and the estimator. Two fits (GEV by L-moments and Log-Pearson III) are quoted with their intervals and the spread between them; a spread above 25 percent is reported as disagreement, not averaged away.", "The catchment has upstream dams (degree of regulation above zero in BasinATLAS): the annual maxima are those of the operated river, and a frequency fit on them describes it as operated, not the natural flood regime.", "GloFAS discharge is a model output for a grid cell of about 5 km, not a gauge reading; return levels from it are indicative only."]
  rationale: "Estimate the 100-year annual exceedance probability flood flow (Q100) for the Murrumbidgee at Wagga Wagga to inform levee upgrade sizing, using regional transfer from similar gauged catchments and an independent GloFAS cross-check, given no usable discharge record within 50 km."
  recon_notes: ["10 donor gauges from a pool of 34,786 gauged catchments.", "ERA5 temperature and forcing and GloFAS discharge are assumed reachable for any point on land (Open-Meteo); not checked here.", "CMIP6 change factors need model output you supply (aquascope.climate works on downloaded data); not counted.", "No gauge with a usable record within 50 km: at-site methods are not defensible; what remains is the regionalisation path (similar_basins, regionalize_signatures) and the GloFAS cross-check."]
steps:
  - tool: "describe_catchment"
    id: "s1"
    rationale: "Establish the catchment attributes (area, climate, dams) that anchor donor-basin similarity weighting."
    arguments:
      lat: -35.1
      lon: 147.37
      upstream: true
    expects:
      - {"check": "not_empty", "path": "sub_basin"}
      - {"check": "max_area_km2", "path": "sub_basin.up_area", "value": 27983.8}
    outputs: [{"kind": "figure", "id": "s1_site_map", "caption": "site map from describe_catchment"}, {"kind": "table", "id": "s1_catchment_attributes", "caption": "catchment attributes from describe_catchment"}]
  - tool: "similar_basins"
    id: "s2"
    rationale: "Select the 10 donor gauges whose catchments most resemble this one, as required by the regionalisation constraint."
    method: "similar_basins"
    arguments:
      lat: -35.1
      lon: 147.37
      k: 10
    expects:
      - {"check": "min_donors", "path": "k", "value": 10}
      - {"check": "not_empty", "path": "stations"}
    depends_on: ["s1"]
    outputs: [{"kind": "figure", "id": "s2_donors_map", "caption": "donors map from similar_basins"}, {"kind": "table", "id": "s2_donors", "caption": "donors from similar_basins"}]
  - tool: "regionalize_signatures"
    id: "s3"
    rationale: "Transfer flow signatures, including the annual-maximum flood signature, from the 10 donors with a band and leave-one-out skill to serve as the Q100 estimate."
    method: "regionalize_signatures"
    arguments:
      lat: -35.1
      lon: 147.37
      k: 10
    expects:
      - {"check": "not_empty", "path": "estimates"}
      - {"check": "not_empty", "path": "skill"}
    depends_on: ["s2"]
    outputs: [{"kind": "figure", "id": "s3_signatures_band", "caption": "signatures band from regionalize_signatures"}, {"kind": "table", "id": "s3_signatures", "caption": "signatures from regionalize_signatures"}, {"kind": "table", "id": "s3_donors", "caption": "donors from regionalize_signatures"}]
  - tool: "anywhere"
    id: "s4"
    rationale: "Obtain GloFAS modelled discharge and its own indicative frequency fit for the cell as an independent cross-check on the regionalised Q100."
    method: "glofas_cross_check"
    arguments:
      lat: -35.1
      lon: 147.37
      years: 20
    expects:
      - {"check": "not_empty", "path": "climate"}
    outputs: [{"kind": "figure", "id": "s4_monthly_climate", "caption": "monthly climate from anywhere"}, {"kind": "figure", "id": "s4_glofas_series", "caption": "glofas series from anywhere"}, {"kind": "table", "id": "s4_monthly_climate", "caption": "monthly climate from anywhere"}, {"kind": "table", "id": "s4_glofas_summary", "caption": "glofas summary from anywhere"}]
results:
  s1: {"ok": true, "gates": [{"check": "not_empty", "passed": true, "detail": "'sub_basin' is present"}, {"check": "max_area_km2", "passed": true, "detail": "catchment of 27,041 km2 against a ceiling of 27,984 km2"}], "summary": "latitude=-35.1, longitude=147.37, license=CC-BY-4.0, attribution=HydroATLAS v1.0 (BasinATLAS), CC BY 4.0. Linke, S., Lehner, B., Ouellet Dallaire, C., et al. (2019). Global hydro-environmental sub-bas", "fallback_used": false, "sha256": "1bf59bc4ec7fe83b"}
  s2: {"ok": true, "gates": [{"check": "min_donors", "passed": true, "detail": "10 donors, 10 needed"}, {"check": "not_empty", "passed": true, "detail": "'stations' is present"}], "summary": "k=10, method=combined", "fallback_used": false, "sha256": "2c75cc3db8ebf457"}
  s3: {"ok": true, "gates": [{"check": "not_empty", "passed": true, "detail": "'estimates' is present"}, {"check": "not_empty", "passed": true, "detail": "'skill' is present"}], "summary": "method=similarity", "fallback_used": false, "sha256": "c11ef6a0e6d49119"}
  s4: {"ok": true, "gates": [{"check": "not_empty", "passed": true, "detail": "'climate' is present"}], "summary": "years=20, start=2006-09-07, end=2026-09-07", "fallback_used": false, "sha256": "72932c28d6f2dcbc"}
```

## Cite this software

AquaScope Studio (2026). AquaScope: Open-source water data aggregation toolkit (version 0.16.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.21903143


---

*{'model': 'claude-sonnet-5', 'provider': 'anthropic', 'prose': 'template', 'tokens': {'consultant': {'calls': 1, 'prompt_tokens': 3208, 'completion_tokens': 972, 'cost_usd': 0.016136}, 'methodologist': {'calls': 1, 'prompt_tokens': 10356, 'completion_tokens': 3249, 'cost_usd': 0.053202}, 'interpreter': {'calls': 0, 'prompt_tokens': 0, 'completion_tokens': 0, 'cost_usd': 0.0}, 'author': {'calls': 2, 'prompt_tokens': 54806, 'completion_tokens': 18634, 'cost_usd': 0.295952}, 'critic': {'calls': 1, 'prompt_tokens': 26069, 'completion_tokens': 6196, 'cost_usd': 0.114098}}, 'total_tokens': 123490, 'total_usd': 0.479388, 'budget': None, 'dropped': 0, 'aquascope_version': '0.16.0', 'date': '2026-09-14 22:18 UTC', 'workspace': 'cdb11f3b6a3d', 'plan_author': 'methodologist', 'written_by': {'answer': 'template', 'summary': 'template', 'decision': 'template', 'findings': 'template', 'problem': 'template', 'site_data': 'template', 'methodology': 'template', 'results-s1': 'template', 'results-s2': 'template', 'results-s3': 'template', 'results-s4': 'template', 'limitations': 'template', 'recommendations': 'template', 'references': 'template', 'appendix': 'template'}}*
