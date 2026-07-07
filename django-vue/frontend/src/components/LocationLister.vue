<template>
  <div class="relative bg-white p-4 shadow-xl ring-1 ring-gray-900/5 rounded-lg">
    <div class="items-center flex justify-between mb-2">
      <p class="font-serif font-bold text-xl">Activities</p>
      <div v-if="!addingLocation">
        <Button class="bg-brand-orange text-xs rounded-lg" @click="addPlace"><i class="ti ti-plus text-sm"></i> Add Activity</Button>
      </div>
    </div>
    <!-- timeline -->
    <ul v-if="!addingLocation" class="flex flex-col">
      <li v-for="(activity, index) in activities"> 
        <div class="flex flex-row justify-between">
          <p class="hover:text-red-400 hover:line-through inline-block font-semibold font-serif text-xl" @click="deleteActivity(activity.id)"> {{ activity.name }} </p>
          <p class="text-md"> {{ activity.start_time.slice(0, 5) }}</p>
        </div>
        <i class="ti ti-map-pin text-sm mr-1"></i>{{ activity.location }}
        <p class="text-xs"><i>{{ activity.note }}</i></p>
        <Separator v-if="index < activities.length - 1" class="my-2"/>
      </li>
    </ul>
    <!-- add location form -->
    <div v-if="addingLocation">
      <FieldSet class="mt-2">
          <Field orientation="horizontal">
              <FieldLabel>Place</FieldLabel>
              <Input required maxlength="48" size="48" placeholder="Marugame Monzo" v-model="placeName"/>
              <FieldLabel>Time</FieldLabel>
              <Input required type="time" v-model="placeTime" />
          </Field>
          <Field>
              <FieldLabel>Address</FieldLabel>
              <Input v-model="placeAddr" ref="addrInput" />
              <FieldLabel>Description</FieldLabel>
              <Textarea placeholder="A great fusion restaurant. $20-30 per!" v-model="description"/>
          </Field>
          <Field orientation="horizontal">
              <Button @click="createLocation">Create Activity</Button>
              <Button variant="secondary" @click="cancel">Cancel</Button>
          </Field>
      </FieldSet>
    </div>
  </div>
</template>
  
<script setup>
import {ref, onMounted, watch} from 'vue';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { Field, FieldSet, FieldDescription, FieldLabel, FieldGroup } from '@/components/ui/field';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';

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
const placeLat = ref('')
const placeLng = ref('')
const description = ref('')

const addrInput = ref(null)

watch(addingLocation, (val) => {
  if (val) {
    setTimeout(() => {
      const autocomplete = new google.maps.places.Autocomplete(addrInput.value.$el, {
        fields: ['formatted_address', 'name'],
      })
      autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace()
        placeAddr.value = place.formatted_address
        placeLat.value = place.geometry.location.lat()
        placeLng.value = place.geometry.location.lng()
        if (!placeName.value) {
          placeName.value = place.name
        }
      })
    }, 100)
  }
})

function addPlace() {
  addingLocation.value = true
}

async function fetchActivities() {
  try {
    const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
    const response = await axios.get(`${API_BASE}/api/daytrips/${props.code}/`)
    activities.value = response.data.activities.sort((a, b) => a.start_time.localeCompare(b.start_time))
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
            lat: placeLat.value ? parseFloat(placeLat.value) : null,
            lng: placeLng.value ? parseFloat(placeLng.value) : null,
            start_time: placeTime.value || "12:30",
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
  placeLat.value = null
  placeLng.value = null
  description.value = ''
  addingLocation.value = false
}

async function deleteActivity(id) {
  try {
    const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
    await axios.delete(`${API_BASE}/api/activity/${id}/`);
    fetchActivities();
  } catch(error) {
    console.error('Delete activity error:', error.response?.data || error.message)
  }
}
</script>