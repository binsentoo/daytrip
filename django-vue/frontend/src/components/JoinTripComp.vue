<script setup>
import axios from 'axios';
import {ref} from 'vue';
import router from '@/router';
import { Input } from '@/components/ui/input'

const code = ref('')

async function getDaytrip() {
    try {
        const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
        const response = await axios.get(`${API_BASE}/api/daytrips/${code.value}/`)
        router.push(`/daytrip/${code.value}`)
        return response.data
    } catch(error) {
        console.error('Error fetching daytrip: ', error)
    }
}

</script>

<template>
    <div>
        <p class="font-serif text-2xl">View Daytrip</p>
        <p class="text-left font-semibold">Invite Code:</p>
        <form @submit.prevent="getDaytrip">
            <Input required type="text" v-model="code" />
            <div class="mt-3 flex justify-center">
                <button class="mt-3 mb-4 rounded-md p-2.5 px-20 font-semibold text-white bg-orange-500 hover:bg-orange-700">Submit</button>
            </div>
        </form>
    </div>
</template>