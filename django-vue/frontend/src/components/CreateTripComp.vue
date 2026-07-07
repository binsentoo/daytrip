<template>
  <form @submit.prevent="submitDaytrip">
    <p class="font-semibold">Event Title:</p>
    <input required placeholder="A DayTrip Outside" v-model="form.title"/>
    <div>
      <div class="flex pb-0.5">
        <p class="font-semibold">Date:</p>
        <input required class="font-sans pl-2" type="date" v-model="form.date">
      </div>
      <div>
        <p class="text-left font-semibold">Description:</p>
        <textarea required
          class="block w-full px-3 py-2 text-black placeholder-gray-400 transition duration-100 ease-in-out bg-white border border-gray-300 rounded shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none focus:ring-opacity-50"
          placeholder="Describe your event!" v-model="form.description"></textarea>
      </div>
    </div>
    <div class="mt-3 flex justify-center">
      <button class="mt-3 mb-4 rounded-md p-2.5 px-20 font-semibold text-white bg-orange-500 hover:bg-orange-700">Create DayTrip</button>
    </div>
    <p v-if="message">{{ message }}</p>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const form = ref({
  title: '',
  date: '',
  description: '',
})

const message = ref('')

async function submitDaytrip() {
  try {
    const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
    const response = await axios.post(`${API_BASE}/api/daytrips/`, {
      title: form.value.title,
      date: form.value.date,
      desc: form.value.description,
    })

    message.value = 'Itinerary created with Invite Code: ' + response.data.code
  } catch (error) {
    message.value = 'Error: ' + (error.response?.data?.detail || error.message)
  }
}

</script>