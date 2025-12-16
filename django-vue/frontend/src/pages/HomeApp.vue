<script>
import HeaderComp from '../components/HeaderComp.vue';
import InitComp from '../components/InitComp.vue';
import CreateTrip from '../components/CreateTripComp.vue';
import JoinTrip from '../components/JoinTripComp.vue';
import vacation from '../assets/vacation.jpeg'

export default {
  components: {
    HeaderComp,
    InitComp,
    CreateTrip,
    JoinTrip,
  },
  data() {
    return {
      current: null,
      vacation,
    }
  },
  methods: {
    showCreate() {
        this.current = 'create';
    },
    showJoin() {
        this.current = 'join';
    }
  }
}
</script>

<template>
  <div class="bg-slate-200 flex flex-col h-screen">
    <HeaderComp/>
    <main class="bg-gradient-to-br from-yellow-100 to-orange-200 px-6 py-14">
      <div class="mx-auto max-w-6xl grid grid-cols-1 gap-10 md:grid-cols-2 md:items-center">
        <!-- left side -->
        <div>
          <h1 class="text-xl md:text-5xl font-semibold">
            Plan out the perfect day, together!
          </h1>
          <p class="mt-4 text-lg max-w-xl">
            Create the perfect day with your friends. 
            Don't know what to do during your trip? Indecisive? DayTrip is for you. 
          </p>
          <div class="mt-6 flex flex-col sm:flex-row gap-4">
            <button class="rounded-full bg-orange-500 px-8 py-3 font-semibold text-white shadow hover:bg-orange-600 transition" @click="showCreate">
              Create a DayTrip
            </button>
            <button class="rounded-full border border-orange-500 px-8 py-3 font-semibold text-orange-600 hover:bg-orange-50 transition" @click="showJoin">
              Join a DayTrip
            </button>
          </div>
        </div>
        <!-- right side -->
        <div>
          <div class="bg-white rounded-2xl shadow-lg p-6 h-72 flex-col flex overflow-hidden">
            <img class="mx-auto p-7 pb-2" :src="vacation" alt="DayTrip Icon" width="250" height="250" v-if="current != 'create' && current !='join'">
            <CreateTrip v-if="current === 'create'" />
            <JoinTrip v-if="current === 'join'" />
          </div>
        </div>
      </div>
    </main>
    <div class="bg-blue-300 flex-1">
      <h1 class="text-3xl font-bold text-center mt-10">How it Works</h1>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-10 mt-10 place-items-center flex-1 mb-10 md:mb-0">
        <div class="bg-white w-full max-w-xs rounded-xl shadow-lg flex items-center justify-center h-full p-10">
            <div class="flex flex-col items-center">
              <h2 class="text-2xl font-semibold">Plan a Daytrip</h2>
              <p class="text-lg mt-3">i don't know what to put here</p>
            </div>
        </div>
        <div class="bg-white w-full max-w-xs rounded-xl shadow-lg flex items-center justify-center h-full p-10">
            <div class="flex flex-col items-center">
              <h2 class="text-2xl font-semibold">Plan a Daytrip</h2>
              <p class="text-lg mt-3">i don't know what to put here</p>
            </div>
        </div><div class="bg-white w-full max-w-xs rounded-xl shadow-lg flex items-center justify-center h-full p-10">
            <div class="flex flex-col items-center">
              <h2 class="text-2xl font-semibold">Plan a Daytrip</h2>
              <p class="text-lg mt-3">i don't know what to put here</p>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>
