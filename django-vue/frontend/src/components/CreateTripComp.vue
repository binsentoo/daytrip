<template>
  <form @submit.prevent="submitDaytrip">
    <div v-if="!editMode" class="flex pb-1">
      <p class="font-serif text-2xl">{{ title }}</p>
      <button @click="editTitle">
        <svg class="h-8 w-8 text-slate-900 float-right" width="24" height="24" viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
          stroke-linejoin="round">
          <path d="M12 20h9" />
          <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
          </svg>
        </button>
    </div>
    <div v-if="editMode" class="flex pb-1">
      <input required v-model="tempValue" maxlength="25"
        class="font-serif text-2xl focus:text-gray-500 text-gray-400 border-2 border-gray-700" />
      <button @click="saveTitle">
        <svg class="h-8 w-8 text-slate-900" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" />
          <polyline points="17 21 17 13 7 13 7 21" />
          <polyline points="7 3 7 8 15 8" />
        </svg>
      </button>
    </div>
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
    <div class="mt-3 flex justify-center gap-6">
      <button class="mx-10 mt-5 rounded-md p-2.5 text-white bg-blue-500 hover:bg-blue-700">Return</button>
      <button class="mx-10 mt-5 rounded-md p-2.5 text-white bg-orange-500 hover:bg-orange-700">Create DayTrip</button>
    </div>
    <p v-if="message">{{ message }}</p>
  </form>
</template>

<script setup>

import { ref } from 'vue'
import axios from 'axios'

const title = ref('Event Name')
const tempValue = ref(null)
const editMode = ref(false)

const form = ref({
  date: '',
  description: '',
})

const message = ref('')

async function submitDaytrip() {
  try {
    const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
    const response = await axios.post(`${API_BASE}/api/daytrips/`, {
      title: title.value,
      date: form.value.date,
      desc: form.value.description,
    })

    message.value = 'Itinerary created with Invite Code: ' + response.data.code
  } catch (error) {
    message.value = 'Error: ' + (error.response?.data?.detail || error.message)
  }
}

function editTitle() {
  tempValue.value = title.value
  editMode.value = true
}

function saveTitle() {
  if (tempValue.value == "") {
    title.value = "Event Name";
  } else {
    title.value = tempValue.value
  }
  editMode.value = false
  tempValue.value = null
}

</script>