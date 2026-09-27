<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const s = ref({}); const hemTop = ref(''); const hemBottom = ref(''); const msg = ref(''); const err = ref('')
onMounted(async () => {
  s.value = await getJSON('/api/settings')
  hemTop.value = s.value.lining_hem_top ?? ''
  hemBottom.value = s.value.lining_hem_bottom ?? ''
})
async function save(){
  msg.value = ''; err.value = ''
  try {
    s.value = await postJSON('/api/settings', { lining_hem_top: String(hemTop.value), lining_hem_bottom: String(hemBottom.value) })
    msg.value = '已保存'
  } catch(e){ err.value = String(e.message || e) }
}
</script>
<template><div class="page"><h1>设置</h1>
<p>默认褶倍 {{ s.default_fullness }}</p>
<label>默认里衬上折边 <input type="number" step="0.01" v-model="hemTop" /></label>
<label>默认里衬下折边 <input type="number" step="0.01" v-model="hemBottom" /></label>
<button @click="save">保存</button>
<span v-if="msg">{{ msg }}</span><p v-if="err" class="bad">{{ err }}</p>
</div></template>
