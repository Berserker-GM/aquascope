// The study on the map: one GeoJSON source and a few layers that show where
// the crew looked (the site, the gauge, the catchment, the ERA5 and GloFAS
// cells as boxes, the donor gauges), drawn as each step lands, one step
// picked out when its row is clicked, cleared on New study. The features are
// the engine's (aquascope.study_map); this module only draws them. The
// source and layers are named study-*, which map.js carries across a
// basemap change.

import { state } from "./core.js?v=__BUILD__";
import { fitBoundsTo, map } from "./map.js?v=__BUILD__";
import { boundsOf, featuresFromArtifact, featuresFromWorkspace } from "./study-map-data.js?v=__BUILD__";

const SRC = "study-map";
const EMPTY = { type: "FeatureCollection", features: [] };
const INK = "#c2185b";      // the study's colour: distinct from the gauge styles and the catchment blue
const DONOR = "#6a1b9a";
const HL = "#ff9800";

let current = EMPTY;
let focused = null;

const isArea = ["in", ["geometry-type"], ["literal", ["Polygon", "MultiPolygon"]]];
const isPoint = ["==", ["geometry-type"], "Point"];
const stepIs = (id) => ["==", ["get", "step_id"], id === null ? "" : id];

function ensureLayers() {
  if (!state.mapOk || !map) return false;
  try {
    if (!map.getSource(SRC)) map.addSource(SRC, { type: "geojson", data: EMPTY });
    if (!map.getLayer("study-fill")) {
      map.addLayer({ id: "study-fill", type: "fill", source: SRC, filter: isArea,
        paint: { "fill-color": INK, "fill-opacity": ["case", ["==", ["get", "role"], "catchment"], 0.12, 0.06] } });
      map.addLayer({ id: "study-line", type: "line", source: SRC, filter: isArea,
        paint: { "line-color": INK, "line-width": 1.4, "line-dasharray": [3, 2] } });
      map.addLayer({ id: "study-points", type: "circle", source: SRC, filter: isPoint,
        paint: {
          "circle-radius": ["match", ["get", "role"], "site", 5, "gauge", 7, "catchment", 6, 4.5],
          "circle-color": ["match", ["get", "role"], "donor", DONOR, "station", "#ffffff", "site", "#ffffff", INK],
          "circle-stroke-color": ["match", ["get", "role"], "donor", "#ffffff", INK],
          "circle-stroke-width": ["match", ["get", "role"], "site", 2.5, "station", 1.5, 1.2],
        } });
      map.addLayer({ id: "study-hl-line", type: "line", source: SRC, filter: ["all", isArea, stepIs(null)],
        paint: { "line-color": HL, "line-width": 3 } });
      map.addLayer({ id: "study-hl-points", type: "circle", source: SRC, filter: ["all", isPoint, stepIs(null)],
        paint: { "circle-radius": 10, "circle-color": "rgba(0,0,0,0)", "circle-stroke-color": HL, "circle-stroke-width": 3 } });
    }
    return true;
  } catch (err) {
    console.info("study map unavailable:", err && err.message);
    return false;
  }
}

function setHighlight(id) {
  if (!map.getLayer("study-hl-line")) return;
  map.setFilter("study-hl-line", ["all", isArea, stepIs(id)]);
  map.setFilter("study-hl-points", ["all", isPoint, stepIs(id)]);
}

// Draw a FeatureCollection as the study map (it replaces what was drawn: the engine sends the whole study).
export function showStudyFeatures(fc) {
  current = fc && Array.isArray(fc.features) ? fc : EMPTY;
  if (!ensureLayers()) return;
  map.getSource(SRC).setData(current);
  if (focused !== null && !current.features.some((f) => f.properties.step_id === focused)) focused = null;
  setHighlight(focused);
}

// The map of a workspace the page holds (a finished, resumed or recorded study); an empty one clears it.
export function showStudyMapFor(ws) {
  showStudyFeatures(featuresFromWorkspace(ws));
}

// A streamed artifact during a run: study_map.geojson is drawn; anything else is ignored. True when drawn.
export function studyMapArtifact(artifact) {
  const fc = featuresFromArtifact(artifact);
  if (!fc) return false;
  showStudyFeatures(fc);
  return true;
}

// Pick out one step's features and bring them into view; the same step again lets go.
export function focusStudyStep(stepId) {
  // a fallback's events name "s3.fallback"; its features ride on s3
  const id = stepId === undefined || stepId === null ? null : String(stepId).replace(/\.fallback$/, "");
  focused = focused === id ? null : id;
  if (!ensureLayers()) return;
  setHighlight(focused);
  if (focused === null) return;
  const b = boundsOf(current.features, focused);
  if (!b) return;
  if (b[0] === b[2] && b[1] === b[3]) {
    map.flyTo({ center: [b[0], b[1]], zoom: Math.max(map.getZoom(), 10), duration: 700 });
  } else {
    fitBoundsTo([[b[0], b[1]], [b[2], b[3]]]);
  }
}

export function clearStudyMap() {
  focused = null;
  showStudyFeatures(EMPTY);
}

export const studyMapFocused = () => focused;
