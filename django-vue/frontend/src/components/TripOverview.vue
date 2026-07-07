<template>
  <div class="relative bg-white p-4 shadow-xl ring-1 ring-gray-900/5 rounded-lg">
    <!-- normal state -->
    <template v-if="!editMode">
      <div class="items-center flex justify-between">
        <p class="font-extrabold font-serif text-xl mt-0.5 text-navy"> {{ title }}</p>
        <button @click="startEdit" class="text-gray-400 hover:text-navy transition">
            <i class="ti ti-pencil text-base"></i>
        </button>
      </div>
      <Badge> {{ day }} · {{ dateTime }}</Badge>
      <div class="bg-gray-50 border-l-5 border-brand-orange rounded-r-lg p-4 text-gray-700 leading-relaxed shadow-sm my-4"> {{ description }}</div>
      <div class="flex items-center justify-between bg-gray-50 rounded-lg px-3 py-2">
        <span class="text-xs font-medium text-gray-400 uppercase tracking-wide">Invite code</span>
        <span class="text-sm font-semibold text-navy font-mono tracking-widest">{{ code }}</span>
      </div>
    </template>
    <!-- edit state -->
    <template v-else>
      <div class="flex items-center justify-between">
        <p class="text-gray-400">Editing trip</p>
        <button @click="cancelEdit" class="text-gray-400 hover:text-navy transition">
          <i class="ti ti-x text-base"></i>
        </button>
      </div>
      <FieldSet>
        <FieldGroup>
          <Field>
            <FieldLabel>Title</FieldLabel>
            <Input v-model="editForm.title"/>
            <FieldLabel>Date</FieldLabel>
            <Input type="date" v-model="editForm.date"/>
            <FieldLabel>Description</FieldLabel>
            <Textarea v-model="editForm.description"/>
          </Field>
          <Field orientation="horizontal">
            <Button @click="saveEdit" type="submit">Submit</Button>
            <Button @click="cancelEdit" variant="outline" type="button">
              Cancel
            </Button>
          </Field>
        </FieldGroup>
      </FieldSet>
    
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Badge } from "@/components/ui/badge"
import { Field, FieldContent, FieldDescription, FieldGroup, FieldLabel, FieldSet, FieldTitle } from "@/components/ui/field"
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'

const title = ref('')
const dateTime = ref('')
const day = ref('')
const description = ref('')

const { code } = defineProps({
  code: String
})

async function fetchDaytrip() {
  try {
    const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
    const response = await axios.get(`${API_BASE}/api/daytrips/${code}/`)
    title.value = response.data.title
    dateTime.value = response.data.date
    description.value = response.data.desc
    findDay()
  } catch (error) {
    console.error('Error fetching daytrip:', error);
  }
}

function findDay() {
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
  const [year, month, day_] = dateTime.value.split('-').map(Number)
  const x = new Date(year, month - 1, day_)
  day.value = days[x.getDay()]
}

onMounted(() => {
  fetchDaytrip()
})

const editMode = ref(false)
const editForm = ref({ title: '', date: '', description: '' })

function startEdit() {
  editForm.value = { title: title.value, date: dateTime.value, description: description.value }
  editMode.value = true
}

function cancelEdit() {
  editMode.value = false
}

async function saveEdit() {
  try { 
    const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
    await axios.patch(`${API_BASE}/api/daytrips/${code}/`, {
        title: editForm.value.title,
        date: editForm.value.date,
        desc: editForm.value.description,
    })
    findDay()
    editMode.value = false
    title.value = editForm.value.title
    dateTime.value = editForm.value.date
    description.value = editForm.value.description
  } catch (error) {
      console.error('Error patching daytrip: ', error)
  } 
}

</script>