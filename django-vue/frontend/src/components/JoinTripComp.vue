<script setup>
import axios from 'axios';
import {ref} from 'vue';
import router from '@/router';

const code = ref('')

async function getDaytrip() {
    try {
        const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
        const response = await axios.get(`${API_BASE}/api/daytrips/${code}/`)
        router.push(`/daytrip/${code.value}`)
        return response.data
    } catch(error) {
        // TODO: display error
        console.error('Error fetching daytrip: ', error)
    }
}

</script>

<template>
    <p class="font-serif text-2xl">View Daytrip</p>
    <p class="text-left font-semibold">Invite Code:</p>
    <form @submit.prevent="getDaytrip">
        <input required class="font-sans pl-2 border-amber-300" type="text" v-model="code">
    <button class="rounded-md p-2.5 text-white bg-orange-500 hover:bg-orange-700">
        Submit
    </button>
    </form>
</template>