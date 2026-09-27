<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([]); const windows = ref([]); const wid = ref(null)
async function load(){
  items.value = (await getJSON('/api/fabrics' + (wid.value ? `?window_id=${wid.value}` : ''))).items
}
onMounted(async () => {
  windows.value = (await getJSON('/api/windows')).items.filter(x=>x.data_quality==='clean')
  if (windows.value.length) wid.value = windows.value[0].id
  await load()
})
</script>
<template><div class="page"><h1>面料</h1>
<label>按窗户看主帘幅数 <select v-model.number="wid" @change="load"><option v-for="x in windows" :key="x.id" :value="x.id">{{ x.name }}</option></select></label>
<div v-for="f in items" :key="f.id" class="fab">{{ f.name }} 门幅{{ f.fabric_width }}m<template v-if="wid"> 主帘 {{ f.main_panels == null ? '—' : f.main_panels + ' 幅' }}</template></div>
</div></template>
