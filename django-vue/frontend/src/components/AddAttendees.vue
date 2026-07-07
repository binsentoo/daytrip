<template>
  <div class="bg-white shadow-xl ring-1 ring-gray-900/5 rounded-lg p-4">
    <div class="flex items-center justify-between">
      <p class="font-serif text-xl mr-20 font-extrabold">Invite List</p>
      <button @click="addPerson" class="text-gray-400 hover:text-navy transition">
        <i class="ti ti-user-plus text-lg"></i>
      </button>
    </div>
    <p class="text-xs mb-2">Hover over to delete.</p>
    <ul>
      <li v-for="(attendee, index) in attendees" class="group my-2">
        <!-- name and badges-->
        <div class="flex items-center gap-2">
          <p class="inline-block text-l"> {{ attendee.name }} </p>
          <!-- toggle groups (RSVP and Driving)-->
          <Select :model-value="attendee.is_going ? 'going' : 'notgoing'"
              @update:model-value="(val) => updateAttendee(attendee, 'is_going', val === 'going')">
              <SelectTrigger class="px-2 text-xs gap-0"
                :class="attendee.is_going ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="going">Going</SelectItem>
                <SelectItem value="notgoing">Not Going</SelectItem>
              </SelectContent>
          </Select>
          <Select :model-value="attendee.is_driver ? 'driving' : 'notdriving'"
              @update:model-value="(val) => updateAttendee(attendee, 'is_driver', val === 'driving')">
              <SelectTrigger class="px-2 text-xs gap-0"
                :class="attendee.is_driver ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700'">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="driving">Driving</SelectItem>
                <SelectItem value="notdriving">Not Driving</SelectItem>
              </SelectContent>
          </Select>
          <button @click="deletePerson(attendee.id)"
            class="text-red-300 hover:text-red-500 transition opacity-0 group-hover:opacity-100">
            <i class="ti ti-trash text-sm"></i>
          </button>
        </div>
      </li>
    </ul>
    <!-- add person form -->
    <div v-if="invitePerson" class="flex flex-col">
      <Field>
        <Input maxlength="16" size="16" v-model="personName" placeholder="Name"/>
        <div class="flex ml-1 space-x-4 items-center">
          <input class="accent-brand-orange" type="checkbox" id="going" v-model="going">
            <label for="going">Going</label>
          </input>
          <input class="accent-blue-500" type="checkbox" v-model="driving">
            <label for="driving">Driving</label>
          </input>
        </div>
        <div class="flex align-middle gap-2"> 
          <Button @click="createPerson">Submit</Button>
          <Button @click="cancelPerson" variant="secondary">Cancel</Button>
        </div>
      </Field>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { Separator } from "@/components/ui/separator"
import { Select, SelectContent, SelectTrigger, SelectItem, SelectValue } from "@/components/ui/select"
import { Field } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Button } from '@/components/ui/button';

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
      await axios.post(`${API_BASE}/api/attendees/`, {
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
    const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
    const response = await axios.delete(`${API_BASE}/api/attendees/${id}/`);
    fetchAttendees();
  } catch (error) {
    console.error('Delete attendee error: ', error)
  }
}

async function updateAttendee(attendee, field, value) {
  try {
    const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
    await axios.patch(`${API_BASE}/api/attendees/${attendee.id}/`, {[field]: value});
    attendee[field] = value
  } catch (error) {
    console.error('Update attendee error: ', error)
  }
}
</script>