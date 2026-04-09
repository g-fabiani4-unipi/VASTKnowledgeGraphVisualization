<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <article class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
    <p class="text-xs font-semibold uppercase tracking-wider text-slate-500">{{ subtitle }}</p>
    <h3 class="mt-1 text-base font-semibold text-slate-900">{{ title }}</h3>
    <div class="mt-4 rounded-lg border border-dashed border-slate-300 bg-slate-50 p-4 text-sm text-slate-600">
      <slot />
    </div>
  </article>
</template>

