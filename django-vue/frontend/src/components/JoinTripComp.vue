<script setup>
import axios from 'axios';
import {ref} from 'vue';
import router from '@/router';

const code = ref('')

async function getDaytrip() {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/daytrips/${code.value}/`)
        router.push(`/daytrip/${code.value}`)
        return response.data
    } catch(error) {
        // TODO: display error
        console.error('Error fetching daytrip: ', error)
    }
}

</script>

<template>
    <div class="relative bg-white px-10 pt-10 pb-8 shadow-xl ring-1 ring-gray-900/5 mx-auto max-w-lg rounded-lg mt-16">
    <p class="font-serif text-2xl">View Daytrip</p>
    <p class="text-left font-semibold">Invite Code:</p>
    <form @submit.prevent="getDaytrip">
        <input required class="font-sans pl-2 border-amber-300" type="text" v-model="code">
    <button class="rounded-md p-2.5 text-white bg-orange-500 hover:bg-orange-700">
        Submit
    </button>
    </form>
    </div>
</template>