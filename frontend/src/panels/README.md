# panels/ — Interactive D3 Panels

Self-contained Vue components rendered inside `GuidePanel` (Guide view). Each panel:

- Fetches its own data via a dedicated composable (`useDegreeFit`, `useComponents`,
  `useCentrality`, `useEgoSubgraph`, …) — or reads the `useSchema` payload when
  metadata-only.
- Renders via `useD3Chart` (ResizeObserver + RAF) for static charts, or `useForceGraph`
  for force-directed (`EgoNetworkPanel`, `EgoComparisonPanel`).
- Exposes controls via `Teleport` into the collapsible drawer inside `GuidePanel`.
- Teleports an interactive theory block into the `PanelFocus` modal drawer
  (`#theoryTarget`).

The full cross-panel contract (bitmaps, mask-only, Lock, selection caps) is in
[`docs/contract.md`](../../../docs/contract.md). Every panel obeys it.

## Catalogue

| Panel                 | ID                                | Component                                         | Status        |
| --------------------- | --------------------------------- | ------------------------------------------------- | ------------- |
| Degree Distribution   | `degree`                          | `DegreeDistribution.vue`                          | ✓ implemented |
| Connected Components  | `connectivity`                    | `ConnectedComponents.vue`                         | ✓ implemented |
| PageRank              | `cent_pagerank`                   | `CentralityPanel.vue` (`measure: 'pagerank'`)     | ✓ implemented |
| Eigenvector           | `cent_eigenvector`                | `CentralityPanel.vue` (`measure: 'eigenvector'`)  | ✓ implemented |
| Betweenness           | `cent_betweenness`                | `CentralityPanel.vue` (`measure: 'betweenness'`)  | ✓ implemented |
| Closeness             | `cent_closeness`                  | `CentralityPanel.vue` (`measure: 'closeness'`)    | ✓ implemented |
| Centrality Comparison | `cent_compare`                    | `CentralityComparison.vue`                        | ✓ implemented |
| Ego Network           | `ego`                             | `EgoNetworkPanel.vue`                             | ✓ implemented |
| Ego Comparison        | `ego_compare`                     | `EgoComparisonPanel.vue`                          | ✓ implemented |
| Type Mixing Matrix    | `type_mixing`                     | `TypeMixingMatrix.vue`                            | ✓ implemented |
| Edge Flow             | `edge_flow`                       | `EdgeFlow.vue`                                    | ✓ implemented |
| Activity Timeline     | `timeline_node` / `timeline_edge` | `ActivityTimeline.vue` (`mode: 'node' \| 'edge'`) | ✓ implemented |

`AttributeFilters.vue` (`mode: 'node' | 'edge'`) is the sidebar filter editor — **not**
in the panel registry; `GuideSidebar` mounts it directly when
`sidebars.mode === 'filters'`. Stub entries (~20) live in `ALL_SPECS` as a roadmap
reference and are left out of the UI export
(`PANEL_SPECS = ALL_SPECS.filter(p => p.status !== 'stub')`). Moving a panel
`stub → planned → implemented` is a one-field change.

## File structure

```
panels/
├── index.js                    # ALL_SPECS + PANEL_SPECS (filtered export) + SECTIONS
├── usePanel.js                 # initializes per-panel `controls` from controlsSchema.default
├── useD3Chart.js               # ResizeObserver + RAF wrapper for static D3 charts
├── shared.js                   # D3 utilities (scales, axes, colors, stats, formatters, tooltips)
├── layeredGraph.js             # pure helpers (fromEgoPayload, mergeLayers, filterIntersection) for ego panels
├── *.vue                       # one component per panel (see the catalogue above)
├── NotImplementedStub.vue      # placeholder for planned panels
└── controls/
    ├── ControlSection.vue      # drawer-section wrapper (title + optional actions slot)
    ├── ControlToggleGroup.vue  # pill segmented control — mutually exclusive options
    ├── ControlSwitch.vue       # on/off slider with inline label
    ├── ControlBoolean.vue      # eye/eye-off toggle, supports disabled prop
    └── SliderControl.vue       # `@vueform/slider` wrapped in `ControlSection`
```

## Panel spec format (`index.js`)

```js
{
  id: 'degree',
  label: 'Degree Distribution',
  section: '2. Descriptive Metrics',
  conditional: false,         // true = only shown when schema conditions are met
  defaultActive: true,
  status: 'implemented',      // 'implemented' | 'planned' | 'stub'
  component: DegreeDistribution,
  componentProps: { mode: 'node' },   // optional, for parametric panels
  available: (schema) => true,        // optional predicate — hide when data is absent
  controlsSchema: { ... },            // declarative spec — usePanel reads only `default` per field
}
// Theory text is not a spec field: each component Teleports an interactive block into
// PanelFocus's #theoryTarget drawer (it receives controls + live data).
```

## How a panel binds to shared state

- **`filters.*`** → `useFilteredModel` builds `activeNodeMask` / `activeEdgeMask`
  (Uint32-packed bitsets). Panels read them via `usePanelContext` and **dim** marks —
  mask-only: filters never recompute metrics. The two count-view exceptions
  (`type_mixing` / `edge_flow`) recompute aggregate counts under the edge mask. No panel
  reads `filters.*` raw to skip a mask; the only allowed raw read shows the state of a
  widget the panel itself edits (`ConnectedComponents` → `wccFilter` for its Top-N
  button state).
- **`selection.ids` / `selection.edgeIds`** → `selectedMask` / `selectedEdgeMask` +
  predicates `isSelected(id)` / `isEdgeSelected(edgeId)`. Per-node marks write via
  `add`/`toggle`; aggregate broadcasts use `replaceCapped(ids, SELECTION_CAPS[id])` so
  the store tracks overflow for the "+N more" caption. `EgoComparisonPanel` caps on read
  (`ids.slice(0, MAX_LAYERS)`).
- **Isolation (Lock)** freezes a panel on a deep-cloned snapshot of filters + selection
  - all masks; `usePanelContext` resolves to the snapshot while frozen.

## Authoring a new panel

Minimal skeleton (see existing panels for measure-specific variations):

```vue
<script setup>
import { ref, toRef, watch, nextTick } from "vue";
import { useFooData } from "@/composables/useFoo.js";
import { usePanel } from "./usePanel.js";
import { useD3Chart } from "./useD3Chart.js";
import ControlSection from "./controls/ControlSection.vue";

const props = defineProps({
  panelSpec: { type: Object, required: true },
  schema: { type: Object, default: null },
  graphId: { type: String, default: null },
  widened: { type: Boolean, default: false },
  controlsTarget: { type: String, default: null },
});
defineEmits(["request-widen", "request-shrink"]);

const { data, loading, error } = useFooData(toRef(props, "graphId"));
const { controls, updateControl } = usePanel(props, props.panelSpec.id, data);

const containerRef = ref(null);
function render() {
  /* d3 logic — reads data.value, controls.value, props.schema */
}

watch([data, controls], () => nextTick(render), { deep: true });
useD3Chart(containerRef, render);
</script>

<template>
  <Teleport v-if="controlsTarget" :to="`#${controlsTarget}`">
    <div class="grid grid-cols-2 auto-rows-min gap-1.5">
      <ControlSection title="View"><!-- controls --></ControlSection>
    </div>
  </Teleport>
  <div
    ref="containerRef"
    class="chart-elev w-full"
    style="aspect-ratio: 4/3; position: relative;"
  />
</template>
```

## Controls drawer pattern

Controls are teleported into `GuidePanel`'s collapsible drawer (toggled by
`SlidersHorizontal` in the panel header). The target div `id` is passed as
`controlsTarget` — it is `null` until the drawer is mounted and ready (`drawerReady`).
Always guard the Teleport with `v-if="controlsTarget"`.

Layout inside the drawer: `grid grid-cols-2 auto-rows-min gap-1.5`.
`ControlSection :col-span="2"` for full-width groups. `ControlToggleGroup` for
mutually-exclusive pills, `ControlSwitch` for additive booleans, `ControlBoolean` for
eye/eye-off, `SliderControl` for range sliders. `controlsSchema` in the registry is read
only for the `default` field by `usePanel.js`; keep entries minimal
(`{ default: <value> }`).

## Shared utilities (`shared.js`)

- **Constants:** `COLOR_SCHEME` (semantic + sky accents), `SLATE` (neutral grey scale),
  `MARGINS_DEFAULT`, `LAYER_PALETTE` (4-hue ordinal for ego layers), `FORMATTERS`
  (number / integer / percent / siPrefix / exponential).
- **Stats:** `pearson(xs, ys)`, `spearman(xs, ys)`, `summaryStats(seq)`
  (mean/median/IQR/whisker bounds).
- **D3 helpers:** `drawAxes`, `drawGrid`, `drawLine`,
  `drawTypeLegend(svg, totalW, types, typeColor)`,`resizeAndRenderFactory(containerRef, renderFunc)`.
- **Tooltips:** `makeTooltip(container)`, `showTip`, `hideTip`, `attachVLineTooltip`.
  Theory links: `theoryLinkClass(on)`.
- **Formatters:** `formatAttrSummary(attr)`, `formatCoverage(coverage)`.
- **Conversion utilities**: `radiansToDegrees`.

Node-type colours come from `@/composables/useNodeTypeColors.js`, not from `shared.js` —
share that mapping across panels rather than instantiating a local `d3.scaleOrdinal`.
Use `seededUnit(id)` for deterministic jitter, never `Math.random()` in a render.

## Team

Contributions to this folder, from the git history:

- **Francesco Secoli** ([@sclfnc](https://github.com/sclfnc)) — all twelve Guide-view
  panels, the registry and spec format, the controls drawer system, `useD3Chart`,
  `shared.js`, and `layeredGraph.js`.
- **Giulia Fabiani** ([@g-fabiani4](https://github.com/g-fabiani4-unipi)) — Graph-view
  panel specs in the registry with per-view panel filtering; shared fallback color
  constant, adaptation of `drawAxes` to dynamic plots, radians to degrees conversion, `resizeAndRenderFactory` in `shared.js`.
