<script setup>
import DashboardCard from '../components/DashboardCard.vue'

const cards = [
  {
    title: 'Node-link diagram',
    subtitle: 'Graph Visualization',
    content: 'Placeholder for a node-link diagram visualization of the knowledge graph.',
  },
  {
    title: 'Sankey Diagram',
    subtitle: 'Graph Visualization',
    content: 'Placeholder for a Sankey diagram visualization of the knowledge graph focused on types.',
  },
  {
    title: 'Connected components',
    subtitle: 'View for community discovery/connected componetns',
    content: 'High-level overview of the connected components in the knowledge graph, showing the number of nodes and edges in each component.',
  },
  {
    title: 'Ego Network',
    subtitle: 'Neighborhood exploration from a node',
    content: 'Placeholder for an ego network visualization that allows users to explore the neighborhood of a specific node in the knowledge graph.',
  },
  {
    title: 'Spatial/Geographic view (?)',
    subtitle: 'Geographical projection of data',
    content: 'Placeholder for a spatial or geographic view that projects the knowledge graph data onto a map, showing the geographical distribution of entities and relationships.',
  },
  {
    title: 'Temporal view (?)',
    subtitle: 'Temporal projection of data',
    content: 'Placeholder for a temporal view that shows the evolution of the knowledge graph over time, allowing users to see how entities and relationships have changed or developed.',
  }


]
</script>

<template>
  <section class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
    <DashboardCard
      v-for="card in cards"
      :key="card.title"
      :title="card.title"
      :subtitle="card.subtitle"
    >
      {{ card.content }}
    </DashboardCard>
  </section>
</template>
