<template>
  <div class="relative bg-white p-4 shadow-xl ring-1 ring-gray-900/5 rounded-lg">
    <div>
      <p class="font-serif font-bold text-2xl">Activities</p>
      <p class="font-serif text-xl">What are we doing?</p>
    </div>
    <div>
      <ul>
        <li v-for="activity in activities"> 
          <!--<p class="hover:text-red-400 hover:line-through inline-block" @click="deleteActivity(location.id)"> {{ location.name }} {{ location.start_time }} {{ location.location }} {{ location.note }}</p>-->
          <div class="flex flex-row justify-between">
            <p class="hover:text-red-400 hover:line-through inline-block font-serif text-2xl" @click="deleteActivity(activity.id)"> {{ activity.name }} </p>
            <p class="font-serif text-xl"> {{ activity.start_time }}</p>
          </div>
          <p class="font-serif text-lg"> {{ activity.location }}</p>
          <p class="font-sans"> {{ activity.note }}</p>
          <hr class="border-t border-gray-300 my-4">
        </li>
      </ul>
      <div v-if="!addingLocation">
        <button class="rounded-md p-2.5 text-white bg-orange-500 hover:bg-orange-700" @click="addPlace">Add Activity</button>
      </div>
    </div>
    <div v-if="addingLocation">
      <div class="flex">
        <p class="font-semibold">Place:</p>
        <input class="font-sans  text-gray-400 border-2 border-gray-700" maxlength="48" size="48" placeholder="Marugame Monzo" v-model="placeName"/>
        <p class="font-semibold">Time:</p>
        <input class="font-sans pl-2" type="time" v-model="placeTime">
      </div>
        <p class="font-semibold">Address:</p>
        <input type="text" class="border-2 border-gray-700" size="48" v-model="placeAddr"/>
        <img
          class="powered-by-google"
          src="https://storage.googleapis.com/geo-devrel-public-buckets/powered_by_google_on_white.png"
          alt="Powered by Google"
        />
        <p class="font-semibold">Description:</p>
        <textarea class="block w-full px-3 py-2 text-black placeholder-gray-400 transition duration-100 ease-in-out bg-white border border-gray-300 rounded shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none focus:ring-opacity-50" placeholder="A great fusion restaurant. $20-30 per!" v-model="description"></textarea>
        <button class="rounded-md p-2.5 text-white bg-orange-500 hover:bg-orange-700" @click="createLocation">Create Activity</button>
        <button class="rounded-md p-1.5 text-black border-4 border-red-500 hover:border-red-700" @click="cancel">Cancel</button>
    </div>
  </div>
</template>
  
<script setup>
import {ref, onMounted} from 'vue';
import axios from 'axios';

const props = defineProps({
  code: String,
})

onMounted(() => {
  fetchActivities()
})

const activities = ref([])
const addingLocation = ref(false)

const placeName = ref('')
const placeTime = ref('')
const placeAddr = ref('')
const description = ref('')

function addPlace() {
  addingLocation.value = true
}

async function fetchActivities() {
  try {
    const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
    const response = await axios.get(`${API_BASE}/api/daytrips/${props.code}/`)
    activities.value = response.data.activities;
  } catch (error) {
    console.error('Error fetching activities:', error);
  }
}

async function createLocation() {
    try {
        const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
        const response = await axios.post(`${API_BASE}/api/activity/`, {
            name: placeName.value,
            location: placeAddr.value,
            start_time: "12:30",
            note: description.value,
            daytrip: props.code,
        })
        console.log(response);
        cancel()
        fetchActivities()
    } catch(error) {
      console.error('Create location error:', error.response?.data || error.message)
    }
}

function cancel() {
  placeName.value = ''
  placeTime.value = ''
  placeAddr.value = ''
  description.value = ''
  addingLocation.value = false
}

async function deleteActivity(id) {
  try {
    const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
    const response = await axios.delete(`${API_BASE}/api/daytrips/${id}/`);
    fetchActivities();
  } catch(error) {

  }
}
</script>