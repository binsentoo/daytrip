<script>
import vacation from '@/assets/vacation.jpeg'
export default {
  data() {
    return {
      vacation,
    }
  }
}
</script>

<template>
    <div class="bg-white inline-block mt-16 rounded-lg shadow-2xl">
        <div>
            <img class="mx-auto p-7 pb-2" :src="vacation" alt="DayTrip 'Icon'" width="250" height="250">
        </div>
        <div class="flex items-center justify-center mt-6 gap-x-6 pb-5">
            <button class="rounded-md p-2.5 text-white bg-yellow-500 hover:bg-yellow-700" @click="$emit('show-create')">
                Create Plan
            </button>
            <button class="rounded-md p-2.5 text-white bg-orange-500 hover:bg-orange-700" @click="$emit('show-join')">
                Join Plan
            </button>
        </div>
    </div>
</template>