<script setup>
import { ref } from 'vue'

const name = ref('test')
</script>

<template>
    <div class="bg-yellow-200 shadow-md hover:shadow-2xl p-2 flex justify-between">
        <div class="font-serif text-3xl">
            <a href="/">DayTrip!</a>
        </div>
        <div class="font-serif text-sm">
            Enjoy your trip, {{ name }}!
        </div>
    </div>
</template>