# Telescope — Design

> _Zoom into your graph._ A visual-analytics prototype for the first exploration of
> attributed knowledge graphs. Load a graph and get its main metrics computed,
> visualised, and interactively explorable. No notebook, no code.

Telescope was developed for the Course on Visual Analytics (VAST Challenge 2025 —
Design Challenge). Most of the work went into the **Guide view**. The **Graph view**
(node-link workspace) is under active development.

This folder holds the design that spans the whole project. Setup and code-level
documentation live in the README inside each folder (see the map at the end).

## Who it is for

Two audiences, one surface:

- **Data scientists** who approach a new graph and want a structured first pass:
  degree distribution, centralities, components, assortativity — without writing code.
  Each panel is a metric computed on the loaded data and made interactive.
- **Non-expert users** (the VAST Challenge target) who want to understand what those
  metrics mean. Every panel has a theory drawer that explains the metric and what a
  "normal" or "anomalous" reading looks like.

The data scientist reads the chart. The non-expert reads the explanation. Both drill
into the same focus modal.

## How panels stay in sync

Every panel reacts to global filters and selection through **three shared bitmaps**:
`activeNodeMask`, `activeEdgeMask`, and `selectedMask`. They are built once, in
`useFilteredModel` / `usePanelContext`.

The key rule is **mask-only semantics**: filters dim marks, they do not recompute
metrics. A power-law fit stays anchored to the full graph while the marks fade.
Per-panel **Lock** freezes a card on its current view.

The full cross-panel contract is in [contract.md](contract.md): what each store owns,
the two count-view exceptions, the upstream-write policy. Every panel obeys it.

## Built-in datasets

Six datasets are exposed via `GET /datasets/`:

- **karate** — Zachary's Karate Club (auto-promoted on `club`: Mr. Hi / Officer)
- **les_miserables** — co-appearance graph
- **florentine** — Florentine families
- **davis** — Davis Southern Women (bipartite, auto-promoted on `bipartite`)
- **email_eu_core** — Email Eu-Core (directed, real department node types)
- **movielens_small** — MovieLens Small (larger, weighted, temporal)

The NetworkX built-ins load as-is; no synthetic `Node Type` is added. Single-type
graphs with one discriminator attribute (Karate's `club`, Davis' `bipartite`) go
through **auto-promotion**: that attribute becomes the effective type everywhere —
colours, legends, chip group. The two larger built-ins carry real `Node Type` /
`Edge Type` set by their loaders.

## Knowledge Graphs

In order to use Telescope with a Knowledge Graph, we recommend you download a dataset from a recent VAST Challenge.
You may use the helpers in the [`data`](../data/README.md) directory to download any such dataset and to create two new datasets:

- `genre_influence.json` relationships between songs and albums from the [VAST 2025 MC1](https://vast-challenge.github.io/2025/MC1.html) dataset, organized by musical genre (directed).
- `asoiaf_interaction.json` undirected interaction graph of characters from JRR Martin's _A Song of Ice and Fire_ series, based from data from [https://github.com/mathbeveridge/asoiaf](https://github.com/mathbeveridge/asoiaf) by [Andrew Beveridge](https://github.com/mathbeveridge) released under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Scope and limitations

Design decisions, not oversights:

- **Read-only.** No graph editing. The tool is for exploration and screening, not
  authoring.
- **No persistence.** The registry is in-memory; a restart clears loaded graphs. This
  is acceptable for a prototype with no auth and no multi-user requirement.
- **Scale ceiling ~100K edges.** Frontend SoA + bitset and backend NetworKit handle
  MC1 and MovieLens comfortably. Far larger graphs would need a binary wire format and
  server-side masking — out of scope on purpose.
- **No layout breadth.** Not a Gephi replacement. Telescope covers the _exploratory_
  phase that comes before a full layout/community workflow: the moment when the
  analyst has not yet decided which metric matters.
- **Mask-only everywhere but two count views.** A documented choice (see
  [contract.md](contract.md)), not a limitation to apologise for.
- **Multigraph parallel edges in Ego Comparison.** `mergeLayers`
  (`panels/layeredGraph.js`) groups edges by `(source, target, type)`, so parallel
  edges collapse to one visual record that references the first `edge_id`. The
  single-ego view (`EgoNetworkPanel`) preserves every parallel edge.

## Notes on MC1

The reference dataset (`data/MC1_release/MC1_graph.json`) is a directed multigraph:
17,412 nodes and 37,857 edges, 16 weakly connected components, LCC covering >99%. It
has five node types (`Person`, `Song`, `RecordLabel`, `Album`, `MusicalGroup`) and
twelve edge types. Centralities are computed via NetworKit because pure NetworkX is
too slow at this scale.

## Where each piece is documented

| Topic                                           | Where                                                               |
| ----------------------------------------------- | ------------------------------------------------------------------- |
| Design rationale, datasets, scope (this page)   | [README.md](README.md)                                              |
| Cross-panel contract (bitmaps, mask-only, Lock) | [contract.md](contract.md)                                          |
| Backend architecture, endpoints, setup, tests   | [`api/README.md`](../api/README.md)                                 |
| Frontend architecture, design system, setup     | [`frontend/README.md`](../frontend/README.md)                       |
| Panel catalogue, spec format, authoring how-to  | [`frontend/src/panels/README.md`](../frontend/src/panels/README.md) |
| Data download and creation scripts              | [`data/README.md`](../data/README.md)                               |
| Meeting notes and wireframes (archive)          | [history/](history/)                                                |

## Team

Contributions to this folder, from the git history:

- **Salvo Rinzivillo** — meeting 1 notes (design discussion, blackboard).
- **Giulia Fabiani** ([@g-fabiani4](https://github.com/g-fabiani4-unipi)) — meeting 4
  notes and wireframes (home-view grid, shared state, filter history).
- **Francesco Secoli** ([@sclfnc](https://github.com/sclfnc)) — the design
  documentation: this page, the cross-panel contract, and the project report.
