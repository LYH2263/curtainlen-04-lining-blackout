<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const s = ref({}); const hem = ref(0.1); const msg = ref(''); const err = ref('')
onMounted(async () => {
  s.value = await getJSON('/api/settings')
  if (s.value.default_lining_hem !== undefined) hem.value = Number(s.value.default_lining_hem)
})
async function save(){
  msg.value = ''; err.value = ''
  try { s.value = await postJSON('/api/settings',{default_lining_hem:hem.value}); msg.value = '已保存' }
  catch(e){ err.value = String(e) }
}
</script>
<template><div class="page"><h1>设置</h1>
<p>默认褶倍 {{ s.default_fullness }}</p>
<label>默认里衬折边(m) <input type="number" step="0.01" min="0" v-model.number="hem"></label>
<button @click="save">保存</button>
<span>{{ msg }}</span>
<p v-if="err" class="bad">{{ err }}</p>
</div></template>
