# The Explorer in real browsers (#591)

**Question.** Do the Explorer's main journeys work in the browsers people use, not only in
the headless Chrome the pull requests are checked in?

**Answer so far: in Chrome on a Mac, 10 of 13 journeys pass.** Two had problems, one of
them fixed here; one could not be checked. Safari, Firefox, iPhone and Android are not
checked yet.

Checked by the maintainer on 2026-10-12, Chrome on macOS with a GPU, on the live site
<https://rekin226-aquascope-explorer.static.hf.space/>.

## Chrome on a Mac

| Journey | Link (after the site's address) | Result |
|---|---|---|
| The globe opens | (none) | pass |
| Rivers flow | `#v=5/50/10` | pass |
| Click a gauge | `#s=usgs/USGS-01646500` | pass |
| Click a river | `#p=24.35,89.8&tab=river` | problem, below |
| Trace to the sea | `#p=24.35,89.8&tab=river`, then Trace to the sea | pass |
| Floods ahead and flood depth | (none) | pass |
| The time bar (play, peak to map, swipe, GIF) | (none) | pass |
| Ask the map | (none) | pass |
| Explain this view and Scout | (none) | pass |
| Drop a HEC-RAS result | (none) | not checked, below |
| Groundwater and a MODFLOW model | (none) | problem, fixed here |
| The bulletin | (none) | pass |
| Phone layout | (none) | pass, in a narrow Chrome window on the Mac, not on a phone |

### Click a river: the instructions confused

The link opens a point beside the Jamuna in Bangladesh. The checklist asked the tester to
look for "the snap line" saying the click snapped to the main channel, 86 years of
simulated flow and the return-period table. The maintainer could not tell what to look for,
and asked whether "Jamuna in Bangladesh" can be found with the Explorer's search instead of
a link. The river search and the wording of this journey are handled in a separate change
under #591; this page will say what it found.

### Groundwater and a MODFLOW model: asked for a georeference first (fixed)

After dropping `freyberg.hds` and `freyberg.dis` (FloPy's `freyberg_multilayer_transient`
example), the page asked for the lower-left x and y in the CRS's units, the rotation and a
CRS before it showed anything. The checklist had not said to drop `freyberg.nam`, which
carries the georeference (`xul`, `yul`, `rotation`, `proj4_str`). But a model without a
georeference must still be viewable. Fixed:

- A `.nam` with FloPy's georeference comment is read when it is dropped or picked with the
  other files. Checked with the Freyberg `.nam`: the model lands near Austin, Texas, UTM
  zone 14N, rotated 15 degrees, with dates from 2 January 2015, without a question.
- When the files do not say where the model is, nothing blocks. The first choice, one
  click, is **Place it at the centre of the map (approximate)**: north up, at its true size
  in its own length unit (metres when the files name none). The legend row and the cell
  card say "approximate placement". The exact form (origin, rotation, CRS) is the second
  choice, and stays reachable from the legend row.
- **Tools**, **Open model results** now offers **MODFLOW: the Freyberg model**: the three
  files, 10.8 MB, fetched by the page from FloPy's GitHub repository (pinned to one commit,
  public domain), checked against their SHA-256 and read like a drop.

### Drop a HEC-RAS result: not checked

The tester could not get the sample file. The HydroShare resource lists dozens of plans
with near-identical names, and a browser page cannot fetch the one #592 used: HydroShare
redirects to a signed Google Cloud Storage address that sends no
`Access-Control-Allow-Origin`. **Tools**, **Open model results** now offers **HEC-RAS 2D:
compound flooding in Portsmouth, Virginia**, read from the Archive's byte-for-byte copy
(`samples/hec-ras/`, CC BY 4.0, Zanko Zandsalimi, GNN4CF, HydroShare). Until the copy is
published by `mirror-samples.yml`, the button says so. This journey is to be checked again.

### Found in headless Chrome, not in the real one

In headless Chrome on the SwiftShader software renderer, the live page's main thread stayed
busy for more than 90 seconds after load (a script evaluation and a screenshot both timed
out). Chrome with a GPU was fine. Slow laptops and phones without a capable GPU may freeze
the same way; this is tracked under #591.

## What remains

- Safari on a Mac.
- Firefox.
- Safari on an iPhone.
- Chrome on Android.
- In Chrome on a Mac: the HEC-RAS journey once the sample is published, and the river
  journey with its new wording.

## How to run the checklist

1. Note the browser, its version and the device.
2. For each journey above, open the Explorer at the link (the site's address followed by
   the link part), do what it asks, and mark it **pass**, **problem** (with a short note of
   what looked wrong) or **skip**.
3. The two model journeys need no download: **Tools**, **Open model results**, then a
   sample. To test a drop instead, drop all of a model's files together (for MODFLOW the
   `.hds`, its `.dis` and its `.nam`).
4. On a phone, also use the map with one thumb for a minute: the legend should be a small
   chip until opened, cards should open as a bottom sheet, and nothing should cover more
   than about a quarter of the screen.
5. Add the results to this page: one table per browser, as above.
