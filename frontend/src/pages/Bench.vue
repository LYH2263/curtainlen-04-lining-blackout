<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const windows = ref([]); const fabrics = ref([]); const wid = ref(1); const fid = ref(1); const out = ref(null)
const lining = ref(false); const liningHem = ref(0.1); const err = ref('')
onMounted(async () => {
  windows.value = (await getJSON('/api/windows')).items.filter(x=>x.data_quality==='clean')
  fabrics.value = (await getJSON('/api/fabrics')).items.filter(x=>x.data_quality==='clean')
  if (windows.value.length) wid.value = windows.value[0].id
  if (fabrics.value.length) fid.value = fabrics.value[0].id
  const s = await getJSON('/api/settings')
  if (s.default_lining_hem !== undefined) liningHem.value = Number(s.default_lining_hem)
})
async function go(save){
  err.value = ''; out.value = null
  try {
    if (save) {
      out.value = await postJSON('/api/estimate',{window_id:wid.value,fabric_id:fid.value,save:true,lining:lining.value,lining_hem:lining.value?liningHem.value:null})
    } else {
      let url = `/api/estimate?window_id=${wid.value}&fabric_id=${fid.value}&lining=${lining.value}`
      if (lining.value) url += `&lining_hem=${liningHem.value}`
      out.value = await getJSON(url)
    }
  } catch(e){ err.value = String(e) }
}
</script>
<template><div class="page"><h1>算料</h1>
<select v-model.number="wid"><option v-for="x in windows" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<select v-model.number="fid"><option v-for="x in fabrics" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<label><input type="checkbox" v-model="lining"> 遮光里衬</label>
<label v-if="lining">里衬折边(m) <input type="number" step="0.01" min="0" v-model.number="liningHem"></label>
<button @click="go(false)">试算</button><button @click="go(true)">保存</button>
<p v-if="err" class="bad">{{ err }}</p>
<template v-if="out">
<h2>主帘</h2>
<PanelCut :panels="out.panels" :cut-height="out.cut_height" :meters="out.meters" />
<template v-if="out.lining && out.lining.enabled">
<h2>里衬</h2>
<PanelCut :panels="out.lining.panels" :cut-height="out.lining.cut_height" :meters="out.lining.meters" />
</template>
</template>
</div></template>
