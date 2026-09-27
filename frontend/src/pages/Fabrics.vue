<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON } from '../api'
const items = ref([]); const windows = ref([]); const wid = ref(null); const panels = ref({})
onMounted(async () => {
  items.value = (await getJSON('/api/fabrics')).items
  windows.value = (await getJSON('/api/windows')).items.filter(x=>x.data_quality==='clean')
  if (windows.value.length) wid.value = windows.value[0].id
})
watch(wid, async () => {
  panels.value = {}
  if (!wid.value) return
  for (const f of items.value.filter(x=>x.data_quality==='clean')) {
    const r = await getJSON(`/api/estimate?window_id=${wid.value}&fabric_id=${f.id}`)
    panels.value[f.id] = r.panels
  }
})
</script>
<template><div class="page"><h1>面料</h1>
<label>按窗 <select v-model.number="wid"><option v-for="x in windows" :key="x.id" :value="x.id">{{ x.name }}</option></select></label>
<div v-for="f in items" :key="f.id" class="fab">{{ f.name }} 门幅{{ f.fabric_width }}m<span v-if="panels[f.id]"> 主帘{{ panels[f.id] }}幅</span></div>
</div></template>
