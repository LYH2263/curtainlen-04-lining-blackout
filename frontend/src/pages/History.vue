<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template><div class="page"><h1>记录</h1><ul><li v-for="r in items" :key="r.id">#{{ r.id }} {{ r.window_name }} / {{ r.fabric_name }} 主帘 {{ r.result?.meters }}m<template v-if="r.result?.lining_enabled && r.result?.lining"> 里衬 {{ r.result.lining.meters }}m（折边 {{ r.result.lining.hem_top }}/{{ r.result.lining.hem_bottom }}）</template><template v-else> 里衬 —</template></li></ul></div></template>
