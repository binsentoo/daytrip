<template>
  <div class="relative bg-white p-4 shadow-xl ring-1 ring-gray-900/5 rounded-lg">
    <p class="font-serif font-extrabold text-2xl mt-0.5"> {{ title }}</p>
    <div>
      <div class="flex-column pb-0.5">
        <p class="font-serif font-semibold"> {{ dateTime }}</p>
      </div>
      <div class="bg-gray-50 border border-gray-200 rounded-xl p-4 text-gray-700 leading-relaxed shadow-sm"> {{ description }}</div>
    </div>
    <p class="text-left font-semibold">Invite Code: {{ code }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const title = ref('')
const dateTime = ref('')
const description = ref('')

const props = defineProps({
  code: String,
})

async function fetchDaytrip() {
  try {
    const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
    const response = await axios.get(`${API_BASE}/api/daytrips/${code}/`)
    console.log(response.data)
    title.value = response.data.title
    dateTime.value = response.data.date
    description.value = response.data.desc
  } catch (error) {
    console.error('Error fetching daytrip:', error);
  }
}

onMounted(() => {
  fetchDaytrip()
})



</script>