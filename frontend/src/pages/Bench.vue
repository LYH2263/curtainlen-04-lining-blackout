<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const windows = ref([]); const fabrics = ref([]); const wid = ref(1); const fid = ref(1); const out = ref(null)
const liningOn = ref(false); const hemTop = ref(0.1); const hemBottom = ref(0.1); const err = ref('')
onMounted(async () => {
  windows.value = (await getJSON('/api/windows')).items.filter(x=>x.data_quality==='clean')
  fabrics.value = (await getJSON('/api/fabrics')).items.filter(x=>x.data_quality==='clean')
  if (windows.value.length) wid.value = windows.value[0].id
  if (fabrics.value.length) fid.value = fabrics.value[0].id
  const s = await getJSON('/api/settings')
  if (s.lining_hem_top !== undefined) hemTop.value = Number(s.lining_hem_top)
  if (s.lining_hem_bottom !== undefined) hemBottom.value = Number(s.lining_hem_bottom)
})
async function go(save){
  err.value = ''; out.value = null
  const q = `window_id=${wid.value}&fabric_id=${fid.value}&lining_enabled=${liningOn.value}&lining_hem_top=${hemTop.value}&lining_hem_bottom=${hemBottom.value}`
  try {
    out.value = save
      ? await postJSON('/api/estimate',{window_id:wid.value,fabric_id:fid.value,save:true,lining_enabled:liningOn.value,lining_hem_top:hemTop.value,lining_hem_bottom:hemBottom.value})
      : await getJSON(`/api/estimate?${q}`)
  } catch(e){ err.value = String(e.message || e) }
}
</script>
<template><div class="page"><h1>算料</h1>
<select v-model.number="wid"><option v-for="x in windows" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<select v-model.number="fid"><option v-for="x in fabrics" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<label><input type="checkbox" v-model="liningOn" /> 遮光里衬</label>
<template v-if="liningOn">
  <label>里衬上折边 <input type="number" step="0.01" v-model.number="hemTop" /></label>
  <label>里衬下折边 <input type="number" step="0.01" v-model.number="hemBottom" /></label>
</template>
<button @click="go(false)">试算</button><button @click="go(true)">保存</button>
<p v-if="err" class="bad">{{ err }}</p>
<template v-if="out">
  <h2>主帘</h2>
  <PanelCut :panels="out.panels" :cut-height="out.cut_height" :meters="out.meters" />
  <template v-if="out.lining_enabled && out.lining">
    <h2>里衬</h2>
    <PanelCut :panels="out.lining.panels" :cut-height="out.lining.cut_height" :meters="out.lining.meters" />
  </template>
</template>
</div></template>
