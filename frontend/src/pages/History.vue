<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template><div class="page"><h1>记录</h1>
<table>
<tr><th>编号</th><th>窗</th><th>面料</th><th>主帘(m)</th><th>里衬(m)</th><th>里衬折边(m)</th></tr>
<tr v-for="r in items" :key="r.id">
<td>{{ r.id }}</td><td>{{ r.window_name }}</td><td>{{ r.fabric_name }}</td>
<td>{{ r.result?.meters }}</td>
<template v-if="r.result?.lining?.enabled">
<td>{{ r.result.lining.meters }}</td><td>{{ r.result.lining.hem }}</td>
</template>
<template v-else><td>—</td><td>—</td></template>
</tr>
</table>
</div></template>
