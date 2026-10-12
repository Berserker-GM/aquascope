// A name for a point that came without one: a pasted link (#p=24.35,89.8&tab=river) or a click on the
// map (#591). The nearest named water in OpenStreetMap within 5 km, else the nearest town, from Photon's
// reverse lookup; the rules are place-search-core.js's. A point found by name in the search keeps that
// name instead, and nothing is asked.

import { photonReverseUrl, pointLabel } from "./place-search-core.js?v=__BUILD__";

const cache = new Map();
const WATER_KM = 5;
const TOWN_KM = 10;

async function features(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();
  return data.features || [];
}

/** `{ name, detail, water }` for a point, or null (nothing named near, or Photon unreachable). */
export async function namePoint(lat, lon) {
  const key = `${lat},${lon}`;
  if (cache.has(key)) return cache.get(key);
  const ask = (async () => {
    try {
      const water = await features(photonReverseUrl(lat, lon, { water: true, radiusKm: WATER_KM }));
      const label = pointLabel(water, []);
      if (label) return label;
      return pointLabel([], await features(photonReverseUrl(lat, lon, { radiusKm: TOWN_KM })));
    } catch (err) {
      console.info("place name unavailable:", err.message);
      cache.delete(key);   // a later look may reach it
      return null;
    }
  })();
  cache.set(key, ask);
  return ask;
}
