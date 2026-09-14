# Potomac River at Little Falls: Reliability of an 8 m3/s Run-of-River Municipal Abstraction in a Dry Year

**Author:** AquaScope Studio  
**Date:** 2026-09-14  
**Description:** whether the Potomac at Little Falls can reliably deliver an 8 m3/s municipal abstraction, run of river with no storage, during a dry year  
**Data Sources:** BasinATLAS (HydroATLAS v1.0), ERA5 via Open-Meteo, similar_basins, usgs  
**Version:** 1.0  

**Site:** 38.9500 N, 77.1300 W

**Answer.** Notice: the Critic's fix requests on limitations, site_data were not all resolved; read the report with the list of what this study does not establish.

Whether the Potomac at Little Falls can reliably deliver an 8 m3/s municipal abstraction, run of river with no storage, during a dry year: 7Q10 18.79 m3/s (established). The 10-year low-flow statistic (7Q10) is 18.79 m3/s, well below the 80 m3/s the river must carry to keep a Q95 reserve of 35.7 m3/s in the channel while capping the abstraction at 10% of flow (USGS-01646500, Little Falls Pump Station gauge, 1930-03-01 to 2026-09-13, 96.5 years; low_flow_context and supply_reliability tools). Under that screening rule the 8 m3/s demand is met on 76.6% of days and delivers 89.6% of the wanted annual volume, but only 3.125% of years pass with no shortfall day at all (worst year 1930, 203 days short), so the supply_reliability screen returns a verdict of 'unreliable'.

*Key numbers*

| Quantity | Value | Unit | Step |
| --- | --- | --- | --- |
| Upstream area | 30090.0 | km2 | s1 |
| Record length | 96.5 | years | s2 |
| Mean of the record | 321.0 | m3/s | s2 |
| 100-year return level, GEV (L-moments) | 11300.0 | m3/s | s2 |
| 100-year return level, Log-Pearson III | 10790.0 | m3/s | s2 |
| 100-year LP3 90 % interval, low | 8995.0 | m3/s | s2 |
| 100-year LP3 90 % interval, high | 12950.0 | m3/s | s2 |
| Q95 (exceeded 95 % of days) | 35.7 | m3/s | s2 |
| Q50 (median flow) | 186.0 | m3/s | s2 |
| Q10 | 716.0 | m3/s | s2 |
| Mann-Kendall p-value (annual mean) | 0.8222 |  | s2 |
| Sen's slope | 0.0592 | m3/s per year | s2 |
| 2-year return level, GEV (L-moments) | 2858.0 | m3/s | s2 |
| 2-year return level, Log-Pearson III | 2876.0 | m3/s | s2 |
| 5-year return level, GEV (L-moments) | 4433.0 | m3/s | s2 |
| 5-year return level, Log-Pearson III | 4540.0 | m3/s | s2 |
| 10-year return level, GEV (L-moments) | 5706.0 | m3/s | s2 |
| 10-year return level, Log-Pearson III | 5820.0 | m3/s | s2 |
| 25-year return level, GEV (L-moments) | 7634.0 | m3/s | s2 |
| 25-year return level, Log-Pearson III | 7643.0 | m3/s | s2 |
| 50-year return level, GEV (L-moments) | 9338.0 | m3/s | s2 |
| 50-year return level, Log-Pearson III | 9153.0 | m3/s | s2 |
| Q95 | 35.7 | m3/s | s3 |
| Q50 | 185.0 | m3/s | s3 |
| 7Q10 | 18.79 | m3/s | s3 |
| Baseflow index | 0.6898 |  | s3 |
| Days the demand is met | 76.6 | % | s4 |
| Years without a shortfall | 3.125 | % | s4 |
| Volume delivered | 89.61 | % | s4 |
| Flow the river must carry | 80.0 | m3/s | s4 |
| Demand | 8.0 | m3/s | s4 |
| Verdict | unreliable |  | s4 |
| Days short in the worst year (1930) | 203 | days | s4 |

## Summary

The city asked whether the Potomac at Little Falls can reliably supply an 8 m3/s run-of-river municipal abstraction with no storage in a dry year. The study used the 96.5-year USGS-01646500 daily discharge record (1930-03-01 to 2026-09-13), computed the flow-duration curve, low-flow statistics (Q95, 7Q10, baseflow index) and a screening reliability rule keeping Q95 in the river and capping withdrawal at 10% of flow. The 7Q10 is 18.79 m3/s and Q95 is 35.7 m3/s, both far short of the 80 m3/s the river would need to carry to deliver 8 m3/s under the rule. The screen finds the demand met on 76.6% of days and 89.6% of volume, but only 3.125% of years free of any shortfall day, giving an overall verdict of 'unreliable'. No trend was found in the annual mean flow (Mann-Kendall p=0.82), so the historical record is taken as representative of dry-year risk, not worsening or improving over time.

## The decision

Decide with the supply_reliability screen's annual no-shortfall reliability (3.125% of years, USGS-01646500, 96.5 years) rather than the more favourable daily or volumetric figures, since the client's question is about reliable delivery through a dry year, not average performance. No numeric band was set for the verdict; the tool returns a categorical 'unreliable' given the stated conditions: an assumed Q95 environmental reserve of 35.7 m3/s, a 10% abstraction-share cap, and no storage. These are playbook defaults, not a verified regulatory minimum-flow standard, and the record embeds only 2.6% degree of regulation (HydroATLAS), so upstream reservoir operations that could support droughts in practice are not reflected. The verdict would change with: a different regulatory instream-flow requirement in place of Q95; a looser or stricter abstraction share than 10%; data on scheduled upstream low-flow augmentation releases (297 million m3 of upstream storage noted); or a seasonal rather than constant 8 m3/s demand profile.

## Findings

One graded finding was produced: the observed record maximum of 12100 m3/s (1936) sits close to but above both the GEV (11301 m3/s) and Log-Pearson III (10794 m3/s) 100-year return levels, with an empirical return period near 97 years (established); this bears on flood risk, not on the dry-year abstraction question. Consistency checks show the Q95 figure (35.7 m3/s) agrees exactly between the flow-duration and low-flow-context steps, and the two flood-frequency fits agree within 5% at the 100-year level (11301 vs 10794 m3/s), both unremarkable.

## Problem and decision

The client wants to know whether the Potomac River at Little Falls can reliably supply 8 m3/s to the city's water works, taken run of river with no storage to buffer shortfalls, during a dry year. The brief frames this as a supply-reliability screening question, requiring flow-duration percentiles (Q95, Q90, Q75), a low-flow frequency statistic (7Q10), the exceedance probability of flow falling below the 8 m3/s threshold, and the fraction of daily flow the abstraction would represent.

## Site and data

The abstraction point at 38.95N, 77.13W drains an upstream area of 30090.7 km2 (HydroATLAS BasinATLAS v1.0, area-weighted over 229 level-12 sub-basins). Mean annual natural discharge at the outlet is estimated at 357.14 m3/s, with annual precipitation 1004 mm/yr, potential evapotranspiration 1095 mm/yr, and an aridity index of 0.92. The catchment is 75% forest, 22% cropland, 5% urban, with 43% karst extent. Degree of regulation by reservoirs is 2.6%, with 297 million m3 of upstream reservoir volume; these two known dams are treated as already embedded in the observed gauge record, not separately modelled.

## Methodology

The plan characterised the catchment context, then fetched and summarised the daily discharge record at USGS-01646500 (0.2 km from the site, 96.5 years), computing the flow-duration curve and a Mann-Kendall trend test. It then computed low-flow context statistics (Q95, Q50, Q10, baseflow index, 7Q10) via a Lyne-Hollick baseflow filter and Weibull-plotting-position low-flow frequency analysis. Finally it ran a supply-reliability screening rule (Vogel and Fennessey 1994; Smakhtin and Eriyagama 2008; Acreman and Dunbar 2004) that keeps Q95 in the river and caps the abstraction at 10% of daily flow, computing the days, years and volume fraction on which the 8 m3/s demand is met.

## Results: step s1

describe_catchment (HydroATLAS BasinATLAS v1.0) for 38.95N, 77.13W reports an upstream area of 30090.7 km2 across 229 level-12 sub-basins, mean elevation 390 m, mean slope 6.5 degrees, annual precipitation 1004 mm/yr, PET 1095 mm/yr, AET 809 mm/yr, aridity index 0.92, mean annual temperature 10.6 C, 5% snow cover, runoff 408.51 mm/yr, mean annual natural discharge 357.14 m3/s, forest 75%, cropland 22%, pasture 7%, urban 5%, wetlands 5%, karst 43%, degree of regulation 2.6%, and upstream reservoir volume 297 million m3. No gates were specified for this step; it ran without failure.

![The site, in longitude and latitude (no basemap); no catalogue station was listed with it.](figures/s1_site_map.png)
*The site, in longitude and latitude (no basemap); no catalogue station was listed with it.*

*Catchment attributes from BasinATLAS for the site at 38.95 N, 77.13 W.*

| attribute | label | value | unit | source | note |
| --- | --- | --- | --- | --- | --- |
| n_sub_basins |  | 229.0 |  |  |  |
| area_km2 |  | 30090.3 |  |  |  |
| outlet_hybas_id |  | 7120567540.0 |  |  |  |
| upstream_area_km2 |  | 30090.7 |  |  |  |
| elevation_m | mean elevation | 390.0 | m | basinatlas_upstream |  |
| slope_deg | mean slope | 6.5 | degrees | basinatlas_upstream |  |
| precipitation_mm_yr | annual precipitation (WorldClim) | 1004.0 | mm/yr | basinatlas_upstream |  |
| pet_mm_yr | annual potential evapotranspiration | 1095.0 | mm/yr | basinatlas_upstream |  |
| aet_mm_yr | annual actual evapotranspiration | 809.0 | mm/yr | basinatlas_upstream |  |
| aridity_index | aridity index (P/PET) | 0.92 | P/PET | basinatlas_upstream |  |
| temperature_c | mean annual air temperature | 10.6 | °C | basinatlas_upstream |  |
| snow_cover_pct | annual snow cover extent | 5.0 | % | basinatlas_upstream |  |
| runoff_mm_yr | annual land-surface runoff | 408.51 | mm/yr | area_weighted_mean |  |
| discharge_m3s | mean annual natural discharge at the outlet | 357.14 | m3/s | basinatlas_upstream |  |
| forest_pct | forest cover | 75.0 | % | basinatlas_upstream |  |
| cropland_pct | cropland | 22.0 | % | basinatlas_upstream |  |
| pasture_pct | pasture | 7.0 | % | basinatlas_upstream |  |
| urban_pct | urban extent | 5.0 | % | basinatlas_upstream |  |
| irrigated_pct | irrigated area | 0.0 | % | basinatlas_upstream |  |
| glacier_pct | glacier extent | 0.0 | % | basinatlas_upstream |  |
| wetland_pct | wetlands (all classes) | 5.0 | % | basinatlas_upstream |  |
| lake_pct | lake area | 0.1 | % | basinatlas_upstream |  |
| karst_pct | karst extent | 43.0 | % | basinatlas_upstream |  |
| clay_pct | clay fraction in soil | 20.0 | % | basinatlas_upstream |  |
| silt_pct | silt fraction in soil | 40.0 | % | basinatlas_upstream |  |
| sand_pct | sand fraction in soil | 40.0 | % | basinatlas_upstream |  |
| soil_organic_carbon_t_ha | soil organic carbon | 42.0 | t/ha | basinatlas_upstream |  |
| soil_water_pct | annual soil water content | 79.0 | % | basinatlas_upstream |  |
| groundwater_table_cm | groundwater table depth | 325.26 | cm | area_weighted_mean |  |
| population_density | population density | 87.47 | people/km2 | basinatlas_upstream |  |
| population | population count | 2609208.98 | people | basinatlas_upstream |  |
| degree_of_regulation_pct | degree of regulation by reservoirs | 2.6 | % | basinatlas_upstream |  |
| human_footprint_2009 | human footprint (2009) | 13.1 | index 0-50 | basinatlas_upstream |  |
| reservoir_volume_mcm | reservoir volume upstream | 297.0 | million m3 | basinatlas_upstream |  |

## Results: step s2

analyze_station on USGS-01646500 (1930-03-01 to 2026-09-13, 96.5 years, n=35261 daily values) passed all three gates (min_years, not_empty trend, unit_present m3/s). Mean flow is 321.00 m3/s, median 185.0 m3/s, min 3.43 m3/s, max 12100.0 m3/s. The flow-duration curve gives Q95=35.7 m3/s, Q50=186.0 m3/s, Q10=716.0 m3/s. Mann-Kendall trend on annual means: p=0.8222, tau=0.0158, Sen's slope 0.0592 m3/s/yr, 'no trend'. Flood-frequency fits (GEV by L-moments and Log-Pearson III) give 100-year return levels of 11301.0 m3/s and 10793.8 m3/s respectively (90% LP3 interval 8995.3-12951.8 m3/s); the record maximum of 12100.0 m3/s (1936) has an empirical return period of 97 years.

![Flow-duration curve of discharge at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500) from the ranked daily flows, with Q95, Q50 and Q10 marked (log scale).](figures/s2_fdc.png)
*Flow-duration curve of discharge at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500) from the ranked daily flows, with Q95, Q50 and Q10 marked (log scale).*

*The record (17631 rows) is in the workbook (`workbook.xlsx`, sheet `s2_series`) and the notebook, not printed here.*

*Summary of the record at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500).*

| item | value |
| --- | --- |
| source | usgs |
| station_id | USGS-01646500 |
| variable | discharge |
| unit | m3/s |
| n | 35261 |
| start | 1930-03-01 |
| end | 2026-09-13 |
| years | 96.5 |
| stats.mean | 321.0023 |
| stats.median | 185.0 |
| stats.min | 3.43 |
| stats.max | 12100.0 |

*Annual maxima at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500).*

| year | value |
| --- | --- |
| 1930 | 977.0 |
| 1931 | 1020.0 |
| 1932 | 4620.0 |
| 1933 | 3430.0 |
| 1934 | 3400.0 |
| 1935 | 1890.0 |
| 1936 | 12100.0 |
| 1937 | 8800.0 |
| 1938 | 1150.0 |
| 1939 | 3480.0 |
| 1940 | 2810.0 |
| 1941 | 2000.0 |
| 1942 | 11500.0 |
| 1943 | 3340.0 |
| 1944 | 2080.0 |
| 1945 | 3700.0 |
| 1946 | 1670.0 |
| 1947 | 1160.0 |
| 1948 | 2590.0 |
| 1949 | 3310.0 |
| 1950 | 3570.0 |
| 1951 | 2940.0 |
| 1952 | 4130.0 |
| 1953 | 2680.0 |
| 1954 | 3090.0 |
| 1955 | 5860.0 |
| 1956 | 1850.0 |
| 1957 | 1950.0 |
| 1958 | 2300.0 |
| 1959 | 1350.0 |
| 1960 | 3280.0 |
| 1961 | 3100.0 |
| 1962 | 3230.0 |
| 1963 | 3090.0 |
| 1964 | 2600.0 |
| 1965 | 2620.0 |
| 1966 | 2190.0 |
| 1967 | 3940.0 |
| 1968 | 2140.0 |
| 1969 | 824.0 |
| 1970 | 2430.0 |
| 1971 | 2530.0 |
| 1972 | 9460.0 |
| 1973 | 3000.0 |
| 1974 | 1370.0 |
| 1975 | 5270.0 |
| 1976 | 5490.0 |
| 1977 | 2470.0 |
| 1978 | 4000.0 |
| 1979 | 5690.0 |

*Return levels at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500) by return period, with the confidence band.*

| T | GEV | LP3 | lower | upper |
| --- | --- | --- | --- | --- |
| 2.0 | 2857.9761 | 2876.14 | 2629.4617 | 3145.9598 |
| 5.0 | 4432.8959 | 4539.9358 | 4090.0806 | 5039.2691 |
| 10.0 | 5705.5232 | 5820.3517 | 5148.8632 | 6579.4124 |
| 25.0 | 7633.5141 | 7643.4463 | 6597.3099 | 8855.4689 |
| 50.0 | 9337.52 | 9152.7562 | 7759.7691 | 10795.8039 |
| 100.0 | 11301.1726 | 10793.7752 | 8995.3302 | 12951.7851 |

*Flow-duration percentiles at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500).*

| exceedance_pct | value |
| --- | --- |
| 10.0 | 716.0 |
| 50.0 | 186.0 |
| 95.0 | 35.7 |

*Mann-Kendall trend test and Sen slope at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500).*

| item | value |
| --- | --- |
| on | annual mean |
| p_value | 0.8222 |
| tau | 0.0158 |
| trend | no trend |
| sens_slope_per_year | 0.0592 |
| n_years | 96 |

## Results: step s3

low_flow_context on USGS-01646500 (same record, 96.5 years) passed both gates (min_years, not_empty low_flow). It gives Q05=1050.0 m3/s, Q10=716.0 m3/s, Q25=379.0 m3/s, Q50=185.0 m3/s, Q75=83.8 m3/s, Q90=48.4 m3/s, Q95=35.7 m3/s, a baseflow index of 0.6898 (Lyne-Hollick filter), and a 7Q10 of 18.79 m3/s (Weibull plotting position).

![Flow-duration curve of discharge at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500) from the 7 percentiles the tool reported, with Q95, Q50 and Q10 marked (log scale).](figures/s3_fdc.png)
*Flow-duration curve of discharge at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500) from the 7 percentiles the tool reported, with Q95, Q50 and Q10 marked (log scale).*

*Low-flow statistics at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500).*

| item | value |
| --- | --- |
| source | usgs |
| station_id | USGS-01646500 |
| variable | discharge |
| unit | m3/s |
| start | 1930-03-01 |
| end | 2026-09-13 |
| years | 96.5 |
| fetch_note | USGS daily values (NWIS); full record requested (from 1930-03-01, the catalog's first date for this station). |
| stats.mean | 321.0023413970108 |
| stats.min | 3.43 |
| stats.max | 12100.0 |
| n_days | 35261 |
| bfi | 0.6897934817779634 |
| low_flow.7q10 | 18.788571428571426 |
| low_flow.text | minimum 7-day mean flow with a 10-year return period (Weibull) |
| recent.end | 2026-09-13 |
| recent.last_30d_mean | 78.30666666666666 |
| recent.last_30d_exceedance_pct | 77.26666855732964 |
| recent.last_90d_mean | 79.68666666666667 |
| recent.last_90d_exceedance_pct | 76.69946966903944 |
| station_name | POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA |
| name | POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA |
| fdc.q05 | 1050.0 |
| fdc.q10 | 716.0 |
| fdc.q25 | 379.0 |
| fdc.q50 | 185.0 |
| fdc.q75 | 83.8 |
| fdc.q90 | 48.4 |
| fdc.q95 | 35.7 |
| stats.mean | 321.0023413970108 |
| stats.min | 3.43 |
| stats.max | 12100.0 |
| low_flow.7q10 | 18.788571428571426 |
| low_flow.text | minimum 7-day mean flow with a 10-year return period (Weibull) |
| recent.end | 2026-09-13 |
| recent.last_30d_mean | 78.30666666666666 |
| recent.last_30d_exceedance_pct | 77.26666855732964 |
| recent.last_90d_mean | 79.68666666666667 |
| recent.last_90d_exceedance_pct | 76.69946966903944 |

## Results: step s4

supply_reliability on USGS-01646500, demand 8.0 m3/s, share 0.10, reserve Q95, passed all four gates (min_years, not_empty reliability, not_empty fdc, unit_present). The reserve is set at 35.7 m3/s, requiring the river to carry 80.0 m3/s to deliver the full demand. Reliability results: daily reserve-only reliability 91.87%, days demand met 76.6% (from key_numbers), volumetric reliability 89.61%, annual (no-shortfall) reliability 3.125%, average 84.83 days short per year, worst year 1930 with 203 days short out of 96 years of record. The verdict returned is 'unreliable'.

![The flow-duration curve at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500) with the flow the demand needs (red), the reserve left in the river (orange) and Q95 (dashed); the demand is met on 77% of days.](figures/s4_reliability_curve.png)
*The flow-duration curve at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500) with the flow the demand needs (red), the reserve left in the river (orange) and Q95 (dashed); the demand is met on 77% of days.*

*Supply reliability at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500).*

| item | value |
| --- | --- |
| demand_m3s | 8.0 |
| demand_given_as | m3/s |
| share | 0.1 |
| unit | m3/s |
| mode | gauged |
| source | usgs |
| station_id | USGS-01646500 |
| variable | discharge |
| start | 1930-03-01 |
| end | 2026-09-13 |
| years | 96.5 |
| fetch_note | USGS daily values (NWIS); full record requested (from 1930-03-01, the catalog's first date for this station). |
| n_days | 35261 |
| bfi | 0.6897934817779634 |
| low_flow.7q10 | 18.788571428571426 |
| low_flow.text | minimum 7-day mean flow with a 10-year return period (Weibull) |
| recent.end | 2026-09-13 |
| recent.last_30d_mean | 78.30666666666666 |
| recent.last_30d_exceedance_pct | 77.26666855732964 |
| recent.last_90d_mean | 79.68666666666667 |
| recent.last_90d_exceedance_pct | 76.69946966903944 |
| reserve_m3s | 35.7 |
| reserve_rule | Q95 kept in the river |
| required_flow_m3s | 80.0 |
| reliability.daily | 0.7660304585803012 |
| reliability.daily_reserve_only | 0.9187203993080174 |
| reliability.annual | 0.03125 |
| reliability.volumetric | 0.896103237287655 |
| reliability.days_short_per_year | 84.83333333333333 |
| reliability.worst_year.year | 1930 |
| reliability.worst_year.days_short | 203 |
| reliability.n_days | 35261 |
| reliability.n_years | 96 |
| verdict | unreliable |
| text | On 77% of days the river can give 8 m3/s while keeping 35.7 m3/s in the channel and taking no more than 10% of the flow (the river must carry 80 m3/s). |
| station_name | POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA |
| name | POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA |
| reliability.daily | 0.7660304585803012 |
| reliability.daily_reserve_only | 0.9187203993080174 |
| reliability.annual | 0.03125 |
| reliability.volumetric | 0.896103237287655 |
| reliability.days_short_per_year | 84.83333333333333 |
| reliability.worst_year.year | 1930 |
| reliability.worst_year.days_short | 203 |
| reliability.n_days | 35261 |
| reliability.n_years | 96 |
| fdc.q05 | 1050.0 |
| fdc.q10 | 716.0 |
| fdc.q25 | 379.0 |
| fdc.q50 | 185.0 |

*Flow-duration percentiles at POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA (usgs USGS-01646500).*

| exceedance_pct | value |
| --- | --- |
| 5.0 | 1050.0 |
| 10.0 | 716.0 |
| 25.0 | 379.0 |
| 50.0 | 185.0 |
| 75.0 | 83.8 |
| 90.0 | 48.4 |
| 95.0 | 35.7 |

## Limitations and what this study does not establish

This is a screening rule in the flow-duration-curve environmental-flow tradition (Vogel and Fennessey 1994; Smakhtin and Eriyagama 2008; Acreman and Dunbar 2004), keeping Q95 in the river and capping abstraction at 10% of flow; it is not a licence or regulatory flow-standard assessment. The reliability figures describe the 96.5 years on record at USGS-01646500; a changing climate, new upstream abstraction, or a drier decade than any recorded would move them, though no trend is claimed or shown to cause any change (Mann-Kendall p=0.82). Return flows, other upstream abstractions besides the two dams already embedded in the record (2.6% degree of regulation), and any future storage or drought-release operations are not represented. Demand is treated as a constant 8 m3/s year-round; no seasonal profile was supplied. Water quality constraints on the abstraction are out of scope.

## Caveats

- A screening rule, not a licence assessment: Q95 kept in the river and at most the stated share of the flow taken are assumptions in the tradition of flow-duration-curve environmental-flow practice (Smakhtin and Eriyagama 2008; Acreman and Dunbar 2004); the regulator's flow standard, return flows, upstream abstractions and storage are not in the number.
- Reliability read off the record describes the years on record; a changing climate, new upstream abstraction or a drier decade than any recorded moves it.

## Recommendations

The results do not support adopting an unmitigated 8 m3/s run-of-river abstraction as reliable: only 3.125% of years on the USGS-01646500 record pass without a shortfall day, and the river must sustain 80 m3/s under the stated Q95-reserve, 10%-share screening rule against a 7Q10 of only 18.79 m3/s. Before any course of action is chosen, obtain the applicable regulatory or interstate-compact minimum in-stream flow requirement (rather than relying on the assumed Q95 reserve), records of scheduled upstream low-flow augmentation releases (297 million m3 of upstream storage noted in HydroATLAS but not reflected in the gauge record), and a seasonal or monthly municipal demand profile. These could materially change the required-flow threshold or the reliability figures; absent them, the current screening indicates that run-of-river supply without storage or augmentation should not be relied upon to meet 8 m3/s through a dry year.

## References

1. Vogel, R. M., & Fennessey, N. M. (1994). Flow-duration curves I: new interpretation and confidence intervals. J. Water Resour. Plann. Manage., 120(4), 485-504.
2. Smakhtin, V., & Eriyagama, N. (2008). Developing a software package for global desktop assessment of environmental flows. Environ. Model. Softw. 23, 1396-1406
3. HydroATLAS v1.0 (BasinATLAS), CC BY 4.0. Linke, S., Lehner, B., Ouellet Dallaire, C., et al. (2019). Global hydro-environmental sub-basin and river reach characteristics at high spatial resolution. Scientific Data 6: 283. https://doi.org/10.1038/s41597-019-0300-6
4. Hosking, J. R. M. (1990). L-moments: analysis and estimation of distributions using linear combinations of order statistics. J. R. Stat. Soc. B, 52(1), 105-124.
5. England, J. F. Jr. et al. (2018). Guidelines for determining flood flow frequency, Bulletin 17C. USGS Techniques and Methods 4-B5.
6. Mann, H. B. (1945). Nonparametric tests against trend. Econometrica, 13, 245-259
7. Sen, P. K. (1968). J. Am. Stat. Assoc., 63, 1379-1389.
8. Lyne, V., & Hollick, M. (1979). Stochastic time-variable rainfall-runoff modelling. Inst. Eng. Aust. Natl. Conf. Publ. 79/10, 89-93.
9. Smakhtin, V. U. (2001). Low flow hydrology: a review. J. Hydrol. 240, 147-186.
10. Acreman, M., & Dunbar, M. J. (2004). Defining environmental river flow requirements: a review. Hydrol. Earth Syst. Sci. 8, 861-876.
11. Smakhtin, V., & Eriyagama, N. (2008). Developing a software package for global desktop assessment of environmental flows. Environ. Model. Softw. 23, 1396-1406. doi:10.1016/j.envsoft.2008.04.002
12. Oudin, L. et al. (2008). Spatial proximity, physical similarity, regression and ungaged catchments. Water Resour. Res. 44, W03413.
13. National-scale validation of donor regionalisation: Hydrol. Earth Syst. Sci. 28 (2024), doi:10.5194/hess-28-3367-2024
14. Rekin226 and contributors (2026). AquaScope: Open-source water data aggregation toolkit (version 0.16.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.21903143

## Appendix: reproducibility

Re-run the same steps with no model: `aquascope run study.yaml`. Resume the workspace: `aquascope studio --resume workspace.json`.

Model: claude-sonnet-5 via anthropic; ledger: consultant 1 call(s), 4350 tokens, methodologist 1 call(s), 17544 tokens, interpreter 1 call(s), 22541 tokens, author 1 call(s), 23043 tokens, critic 1 call(s), 23123 tokens. aquascope 0.16.0.

```yaml
# An AquaScope study (version 3): the plan behind an answer, its gates, and what happened.
#   aquascope run study.yaml
version: 3
title: "Determine whether the Potomac River at Little Falls can reli: 38.95, -77.13"
question: "Can the Potomac at Little Falls reliably supply 8 m3/s to the city's water works, run of river, in a dry year?"
created: "2026-09-14T15:56:23+00:00"
aquascope_version: "0.16.0"
author: "methodologist"
model: "claude-sonnet-5"
problem:
  kind: "supply_reliability"
  site: {"lat": 38.95, "lon": -77.13}
  params: {"demand_m3s": 8.0, "use": "municipal", "share": 0.1, "storage": false, "demand_ml_day": null}
  text: "Can the Potomac at Little Falls reliably supply 8 m3/s to the city's water works, run of river, in a dry year?"
plan:
  author: "methodologist"
  playbook: "supply_reliability"
  objective: "Determine whether the Potomac River at Little Falls can reliably deliver a run-of-river municipal abstraction of 8 m3/s during a dry year, with no storage to buffer shortfalls."
  decision: "whether the Potomac at Little Falls can reliably supply an 8 m3/s municipal abstraction, run of river with no storage, in a dry year"
  methodology: ["Characterise the catchment at the site to confirm the scale and regulation context of the flow being screened.", "Fetch and summarise the daily discharge record at the representative gauge, computing the flow-duration curve and checking for trend.", "Compute low-flow context statistics (Q95, Q50, Q10, baseflow index, 7Q10) to describe how the river behaves in dry spells.", "Run the supply-reliability screening rule, keeping Q95 in the river and capping the abstraction at the specified share of daily flow, to get the days, years and volume fraction on which the 8 m3/s demand is met."]
  assumptions: ["daily resolution assumed for the discharge record as the catalog does not state it", "USGS-01646500 (Little Falls Pump Station gauge) taken as the representative record given its 0.2 km distance and 96.5 years of data", "run of river phrasing in the problem is taken to mean no storage is available, matching the playbook default", "share of flow left at the playbook default of 10 percent since the client did not specify a stricter or looser screening rule", "Daily resolution assumed for the discharge record as the catalog does not state it.", "USGS-01646500 (Little Falls Pump Station gauge) taken as the representative record given its 0.2 km distance and 96.5 years of data.", "Run of river phrasing in the problem is taken to mean no storage is available, matching the playbook default.", "Share of flow left at the playbook default of 10 percent since the client did not specify a stricter or looser screening rule.", "The two dams noted upstream (catchment dams=2.6) are treated as already embedded in the observed record and not separately modeled."]
  alternatives: [{"method": "similar_basins", "why_not": "meant for an ungauged point; a gauge with 96.5 years of record sits 0.2 km from the site, so donor regionalization is unnecessary and only marginal per the sufficiency table."}, {"method": "gr4j_calibration", "why_not": "the catchment area of 30,091 km2 is above the 10,000 km2 ceiling for a lumped rainfall-runoff model, so this method is not_defensible."}, {"method": "recharge_wtf", "why_not": "no groundwater level record exists at this site, so water-table fluctuation recharge is not_defensible."}]
  limitations_expected: ["The reliability figure describes the years on record; a changing climate, new upstream abstraction, or a drier decade than any recorded would move it.", "This is a screening rule in the flow-duration-curve environmental-flow tradition (keeping Q95 in the river, capping abstraction at 10 percent of flow), not a licence or regulatory flow-standard assessment.", "Return flows, other upstream abstractions besides the two known dams, and any future storage are not represented in the number.", "Water quality constraints on the abstraction are out of scope for this quantity-only reliability question."]
  citations: ["Vogel, R. M. and Fennessey, N. M. (1994). Flow-duration curves I: new interpretation and confidence intervals. J. Water Resour. Plann. Manage. 120, 485-504.", "Smakhtin, V., & Eriyagama, N. (2008). Developing a software package for global desktop assessment of environmental flows. Environ. Model. Softw. 23, 1396-1406. doi:10.1016/j.envsoft.2008.04.002", "Acreman, M., & Dunbar, M. J. (2004). Defining environmental river flow requirements: a review. Hydrol. Earth Syst. Sci. 8, 861-876.", "Smakhtin, V. U. (2001). Low flow hydrology: a review. J. Hydrol. 240, 147-186.", "Lyne, V., & Hollick, M. (1979). Stochastic time-variable rainfall-runoff modelling. Inst. Eng. Aust. Natl. Conf. Publ. 79/10, 89-93.", "Oudin, L. et al. (2008). Spatial proximity, physical similarity, regression and ungaged catchments. Water Resour. Res. 44, W03413.", "National-scale validation of donor regionalisation: Hydrol. Earth Syst. Sci. 28 (2024), doi:10.5194/hess-28-3367-2024", "Smakhtin and Eriyagama 2008", "Acreman and Dunbar 2004"]
  caveats: ["A screening rule, not a licence assessment: Q95 kept in the river and at most the stated share of the flow taken are assumptions in the tradition of flow-duration-curve environmental-flow practice (Smakhtin and Eriyagama 2008; Acreman and Dunbar 2004); the regulator's flow standard, return flows, upstream abstractions and storage are not in the number.", "Reliability read off the record describes the years on record; a changing climate, new upstream abstraction or a drier decade than any recorded moves it."]
  rationale: "Determine whether the Potomac River at Little Falls can reliably deliver a run-of-river municipal abstraction of 8 m3/s during a dry year, with no storage to buffer shortfalls."
  recon_notes: ["Record resolution is not in the catalog; daily is assumed for every variable.", "10 donor gauges from a pool of 34,786 gauged catchments.", "ERA5 temperature and forcing and GloFAS discharge are assumed reachable for any point on land (Open-Meteo); not checked here.", "CMIP6 change factors need model output you supply (aquascope.climate works on downloaded data); not counted."]
steps:
  - tool: "describe_catchment"
    id: "s1"
    rationale: "Catchment size, degree of regulation by dams and drainage area frame whether the low flows at the gauge are natural and whether the screening applies at this scale."
    arguments:
      lat: 38.95
      lon: -77.13
      upstream: true
    outputs: [{"kind": "figure", "id": "s1_site_map", "caption": "site map from describe_catchment"}, {"kind": "table", "id": "s1_catchment_attributes", "caption": "catchment attributes from describe_catchment"}]
  - tool: "analyze_station"
    id: "s2"
    rationale: "The record summary, trend and flow-duration percentiles at the gauge 0.2 km from the site anchor the whole screening on an observed, unregionalized record."
    method: "flow_duration"
    arguments:
      source: "usgs"
      station_id: "USGS-01646500"
      variable: "discharge"
    expects:
      - {"check": "min_years", "value": 10, "path": "years"}
      - {"check": "not_empty", "path": "trend", "repaired_from": "fdc"}
      - {"check": "unit_present", "path": "unit"}
    outputs: [{"kind": "figure", "id": "s2_series", "caption": "series from analyze_station"}, {"kind": "figure", "id": "s2_fdc", "caption": "fdc from analyze_station"}, {"kind": "figure", "id": "s2_trend", "caption": "trend from analyze_station"}, {"kind": "table", "id": "s2_summary", "caption": "summary from analyze_station"}, {"kind": "table", "id": "s2_fdc_percentiles", "caption": "fdc percentiles from analyze_station"}, {"kind": "table", "id": "s2_trend", "caption": "trend from analyze_station"}]
  - tool: "low_flow_context"
    id: "s3"
    rationale: "Q95, Q50, Q10, the baseflow index and the 7Q10 statistic say directly how low the river gets in a dry year and how much baseflow sustains it."
    method: "low_flow_frequency"
    arguments:
      source: "usgs"
      station_id: "USGS-01646500"
    expects:
      - {"check": "min_years", "value": 10, "path": "years"}
      - {"check": "not_empty", "path": "low_flow"}
    depends_on: ["s2"]
    outputs: [{"kind": "table", "id": "s3_low_flow_stats", "caption": "Q95, Q50, Q10, baseflow index and 7Q10 from low_flow_context"}]
  - tool: "supply_reliability"
    id: "s4"
    rationale: "The screening rule on the full daily record gives the fraction of days, years and volume the 8 m3/s abstraction can be taken while Q95 stays in the river and no more than 10 percent of flow is withdrawn."
    method: "supply_reliability"
    arguments:
      source: "usgs"
      station_id: "USGS-01646500"
      demand_m3s: 8.0
      share: 0.1
      reserve: "q95"
    expects:
      - {"check": "min_years", "value": 10, "path": "years"}
      - {"check": "not_empty", "path": "reliability"}
      - {"check": "not_empty", "path": "fdc"}
      - {"check": "unit_present", "path": "unit"}
    depends_on: ["s2", "s3"]
    outputs: [{"kind": "figure", "id": "s4_reliability_curve", "caption": "reliability curve from supply_reliability"}, {"kind": "table", "id": "s4_reliability", "caption": "reliability statistics (exceedance probability, days/years/volume met) from supply_reliability"}, {"kind": "table", "id": "s4_fdc_percentiles", "caption": "fdc percentiles from supply_reliability"}]
results:
  s1: {"ok": true, "gates": [], "summary": "latitude=38.95, longitude=-77.13, license=CC-BY-4.0, attribution=HydroATLAS v1.0 (BasinATLAS), CC BY 4.0. Linke, S., Lehner, B., Ouellet Dallaire, C., et al. (2019). Global hydro-environmental sub-bas", "fallback_used": false, "sha256": "c2dfc5b37399373f"}
  s2: {"ok": true, "gates": [{"check": "min_years", "passed": true, "detail": "96.5 years of record, 10 needed"}, {"check": "not_empty", "passed": true, "detail": "'trend' is present"}, {"check": "unit_present", "passed": true, "detail": "unit m3/s"}], "summary": "source=usgs, station_id=USGS-01646500, variable=discharge, unit=m3/s, years=96.5, start=1930-03-01, end=2026-09-13", "fallback_used": false, "sha256": "5c811c84c26f373c"}
  s3: {"ok": true, "gates": [{"check": "min_years", "passed": true, "detail": "96.5 years of record, 10 needed"}, {"check": "not_empty", "passed": true, "detail": "'low_flow' is present"}], "summary": "source=usgs, station_id=USGS-01646500, variable=discharge, unit=m3/s, years=96.5, start=1930-03-01, end=2026-09-13", "fallback_used": false, "sha256": "23a238b4de85b94f"}
  s4: {"ok": true, "gates": [{"check": "min_years", "passed": true, "detail": "96.5 years of record, 10 needed"}, {"check": "not_empty", "passed": true, "detail": "'reliability' is present"}, {"check": "not_empty", "passed": true, "detail": "'fdc' is present"}, {"check": "unit_present", "passed": true, "detail": "unit m3/s"}], "summary": "source=usgs, station_id=USGS-01646500, variable=discharge, unit=m3/s, years=96.5, start=1930-03-01, end=2026-09-13", "fallback_used": false, "sha256": "2e92094a349777c4"}
```

## Cite this software

AquaScope Studio (2026). AquaScope: Open-source water data aggregation toolkit (version 0.16.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.21903143


---

*{'model': 'claude-sonnet-5', 'provider': 'anthropic', 'prose': 'model', 'tokens': {'consultant': {'calls': 1, 'prompt_tokens': 3440, 'completion_tokens': 910, 'cost_usd': 0.01598}, 'methodologist': {'calls': 1, 'prompt_tokens': 12167, 'completion_tokens': 5377, 'cost_usd': 0.078104}, 'interpreter': {'calls': 1, 'prompt_tokens': 12769, 'completion_tokens': 9772, 'cost_usd': 0.123258}, 'author': {'calls': 2, 'prompt_tokens': 34148, 'completion_tokens': 11634, 'cost_usd': 0.184636}, 'critic': {'calls': 1, 'prompt_tokens': 13337, 'completion_tokens': 9786, 'cost_usd': 0.124534}}, 'total_tokens': 113340, 'total_usd': 0.526512, 'budget': None, 'dropped': 2, 'aquascope_version': '0.16.0', 'date': '2026-09-14 16:01 UTC', 'workspace': 'dc453229134f', 'plan_author': 'methodologist', 'written_by': {'answer': 'model', 'summary': 'model', 'decision': 'model', 'findings': 'model', 'problem': 'model', 'site_data': 'model', 'methodology': 'model', 'results-s1': 'model', 'results-s2': 'model', 'results-s3': 'model', 'results-s4': 'model', 'limitations': 'model', 'recommendations': 'model', 'references': 'template', 'appendix': 'template'}}*
