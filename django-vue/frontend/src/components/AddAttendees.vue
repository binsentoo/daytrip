<template>
  <div class="bg-white shadow-xl ring-1 ring-gray-900/5 rounded-lg p-4">
    <div class="flex justify-between">
      <p class="font-serif text-2xl mr-20 font-extrabold">Invite List</p>
      <button @click="addPerson">
        <svg class="h-8 w-8 text-slate-900 flex" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round">
          <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
          <circle cx="8.5" cy="7" r="4" />
          <line x1="20" y1="8" x2="20" y2="14" />
          <line x1="23" y1="11" x2="17" y2="11" />
        </svg>
      </button>
    </div>
    <ul>
      <li v-for="attendee in attendees">
        <p class="hover:text-red-400 hover:line-through inline-block font-serif font-bold text-xl"
          @click="deletePerson(attendee.id)"> {{ attendee.name }} </p>
        <div class="flex space-x-1">
        <div v-if="attendee.is_going">
          Going
        </div>
        <div v-else>
          Not Going
        </div>
        <div v-if="attendee.is_driver">
          Driving
        </div>
        </div>
        <hr class="border-t border-gray-300 my-4">
      </li>
    </ul>
    <div v-if="invitePerson" class="flex flex-col">
      <div class="flex align-middle">
        <input class="font-sans focus:text-gray-500 text-gray-400 border-2 border-gray-700" maxlength="16" size="16"
          placeholder="Name" v-model="personName" />
        <button @click="createPerson">
          <svg class="h-6 w-6 text-slate-900" width="24" height="24" viewBox="0 0 24 24" stroke-width="2"
            stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <path stroke="none" d="M0 0h24v24H0z" />
            <path d="M5 12l5 5l10 -10" />
          </svg>
        </button>
        <button @click="cancelPerson">
          <svg class="h-6 w-6 text-slate-900" width="24" height="24" viewBox="0 0 24 24" stroke-width="2"
            stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <path stroke="none" d="M0 0h24v24H0z" />
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>
      <div class="flex space-x-4 items-center">
        <input type="checkbox" id="going" v-model="going">
        <label for="going">Going</label>
        </input>
        <input type="checkbox" v-model="driving">
        <label for="driving">Driving</label>
        </input>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const invitePerson = ref(false)
const attendees = ref([])
const personName = ref('')
const going = ref(false)
const driving = ref(false)

const props = defineProps({
  code: String,
})

async function fetchAttendees() {
  try {
    const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
    const response = await axios.get(`${API_BASE}/api/daytrips/${props.code}/`);
    attendees.value = response.data.attendees;
  } catch (error) {
    console.error('Error fetching attendees:', error);
  }
}

onMounted(() => {
  fetchAttendees()
})

function addPerson() {
  invitePerson.value = true
}

async function createPerson() {
  if (personName.value.trim() !== '') {
    try {
      const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
      const response = await axios.post(`${API_BASE}/api/attendees/`, {
        name: personName.value.trim(),
        is_going: going.value,
        is_driver: driving.value,
        daytrip: props.code,
      })
      cancelPerson()
      fetchAttendees()
    } catch (error) {
      console.error('Create attendee error:', error.response.data || error.message)
    }
  }
}

function cancelPerson() {
  personName.value = ''
  going.value = false;
  driving.value = false;
  invitePerson.value = false
}

async function deletePerson(id) {
  try {
    const response = await axios.delete(`http://127.0.0.1:8000/api/attendees/${id}/`);
    fetchAttendees();
  } catch (error) {

  }
}
</script>