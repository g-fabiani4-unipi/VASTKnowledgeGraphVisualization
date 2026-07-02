# Telescope — Zoom into your graph

A visual-analytics dashboard for the first exploration of attributed knowledge graphs.
Load a graph and get its main metrics — degree distribution, centralities, components,
type mixing, timelines — computed, visualised, and interactively explorable. No notebook,
no code.

Developed by students of the **Course on Visual Analytics** (University of Pisa) for the
**VAST Challenge 2025 – Design Challenge**. The challenge asks for a visual-analytics
design that helps non-expert users explore knowledge graphs: discover new relationships,
identify anomalies, and infer missing information.

> Challenge page: <https://vast-challenge.github.io/2025/DC.html>

## Quick start

```bash
./dev.sh            # backend (:8000) + frontend (:5173); Ctrl+C stops both
./dev.sh --dev      # also install test deps and run the API suite first
./dev.sh --log      # stream full pip/npm output
```

The script creates `api/venv`, installs Python and Node dependencies on first run, then
starts uvicorn and Vite. It needs a Linux shell with `bash`, `python3`, and Node
(`^20.19.0 || >=22.12.0`). To start backend or frontend by hand, see the README in each
folder.

## Repository layout

| Path                     | What's inside                                                                       |
| ------------------------ | ----------------------------------------------------------------------------------- |
| [`frontend/`](frontend/) | Vue 3 + D3 single-page app: the dashboard, its panels, stores, and composables.     |
| [`api/`](api/)           | FastAPI backend: graph loading, indices, and per-panel analysis endpoints.          |
| [`docs/`](docs/)         | Design documentation: what Telescope is, the cross-panel contract, meeting history. |
| [`data/`](data/)         | Dataset download and creations helpers. The datasets themselves are not committed.  |

## Documentation

| Topic                                     | Where                                                            |
| ----------------------------------------- | ---------------------------------------------------------------- |
| Design rationale, audiences, scope        | [`docs/README.md`](docs/README.md)                               |
| Cross-panel interaction contract          | [`docs/contract.md`](docs/contract.md)                           |
| Backend architecture, endpoints, setup    | [`api/README.md`](api/README.md)                                 |
| Frontend architecture, conventions, setup | [`frontend/README.md`](frontend/README.md)                       |
| Panel catalogue and authoring guide       | [`frontend/src/panels/README.md`](frontend/src/panels/README.md) |
| Meeting notes and early wireframes        | [`docs/history/`](docs/history/)                                 |

## Stack

| Area     | Tech                                                                                |
| -------- | ----------------------------------------------------------------------------------- |
| Frontend | Vue 3 · Vite · Pinia · Vue Router · Tailwind CSS v4 · D3 · Lucide · @vueform/slider |
| Backend  | FastAPI · NetworkX · NetworKit (centralities) · powerlaw (distribution fits)        |

## Team

Developed collaboratively by students of the Course on Visual Analytics. Specific
contributions, from the git history:

- **Salvo Rinzivillo** — project scaffolding (Vue 3 + Vite setup, Tailwind integration,
  first layout components), the original upstream API and its test suite, the initial
  README, meeting 1 notes, and the data download script.
- **Giulia Fabiani** ([@g-fabiani4](https://github.com/g-fabiani4-unipi)) — dashboard
  rework into nested router views (Graph/Guide), responsive layout, accessibility pass,
  Graph-view panels and per-view panel filtering, dataset-view loading skeletons,
  meeting 4 notes and wireframes.
- **Francesco Secoli** ([@sclfnc](https://github.com/sclfnc)) — the Telescope reference
  implementation: the modular FastAPI backend (indices, analysis endpoints, centrality
  pipeline), the D3 panels, the filter/selection bitmap model and cross-panel contract,
  the design system, and the design documentation.

## References

- VAST Challenge 2025 – Design Challenge: <https://vast-challenge.github.io/2025/DC.html>
- IEEE VIS / VAST community resources on visual analytics, graph visualization, and knowledge graphs
