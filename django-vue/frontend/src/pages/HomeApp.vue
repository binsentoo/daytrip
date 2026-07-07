<script>
import HeaderComp from '../components/HeaderComp.vue';
import CreateTrip from '../components/CreateTripComp.vue';
import JoinTrip from '../components/JoinTripComp.vue';
import vacation from '../assets/vacation.jpeg'

export default {
  components: {
    HeaderComp,
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
  <div class="flex flex-col h-screen">
    <HeaderComp/>
    <main class="bg-gradient-to-br from-page-yellow to-page-yellow-dark px-8 py-16">
      <div class="mx-auto max-w-6xl grid grid-cols-1 gap-10 md:grid-cols-2 md:items-center">
        <!-- left side -->
        <div>
          <p class="text-xs font-medium text-brand-orange uppercase tracking-widest mb-3">Plan together</p>
          <h1 class="text-4xl md:text-5xl font-semibold font-serif text-navy tracking-tight">
            Plan out the perfect day, <span class="text-brand-orange">together!</span>
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
          <div v-if="current !== null" class="bg-white rounded-2xl shadow-lg p-6 flex-col flex h-70">
            <CreateTrip v-if="current === 'create'" @return="current = null" />
            <JoinTrip v-if="current === 'join'" @return="current = null" />
          </div>
          <div v-if="current === null" class="bg-white rounded-2xl shadow-lg p-6 flex flex-col h-70">
            <div class="flex items-center justify-between">
              <p class="font-semibold text-navy text-lg">A day in Little Tokyo</p>
              <span class="text-xs font-medium text-brand-orange bg-brand-orange-light border border-brand-orange-border rounded-md px-2 py-1">August 4, 2026</span>
            </div>
            <div class="flex flex-col gap-0">
              <div class="flex gap-3 items-start py-2 relative">
                <div class="flex flex-col items-center gap-1 min-w-[20px]">
                  <div class="w-2 h-2 rounded-full bg-brand-orange mt-1 shrink-0"></div>
                  <div class="w-px flex-1 bg-gray-200"></div>
                </div>
                <div><p class="text-sm font-medium text-navy">Marugame Monzo</p><p class="text-xs text-gray-400">11:00 am - 12:30 pm</p></div>
              </div>
              <div class="flex gap-3 items-start py-2 relative">
                <div class="flex flex-col items-center gap-1 min-w-[20px]">
                  <div class="w-2 h-2 rounded-full bg-brand-orange mt-1 shrink-0"></div>
                  <div class="w-px flex-1 bg-gray-200"></div>
                </div>
                <div><p class="text-sm font-medium text-navy">Shopping</p><p class="text-xs text-gray-400">12:30 pm - 4:00 pm</p></div>
              </div>
              <div class="flex gap-3 items-start py-2 relative">
                <div class="flex flex-col items-center gap-1 min-w-[20px]">
                  <div class="w-2 h-2 rounded-full bg-brand-orange mt-1 shrink-0"></div>
                  <div class="w-px flex-1 bg-gray-200"></div>
                </div>
                <div><p class="text-sm font-medium text-navy">Head Home</p><p class="text-xs text-gray-400">4:00 pm</p></div>
              </div> 
            </div>
            <!--attendees-->
            <div class="flex items-center gap-2 pt-2 border-t border-gray-100">
              <div class="w-7 h-7 rounded-full bg-blue-100 text-blue-700 text-xs font-medium flex items-center justify-center">DP</div>
              <div class="w-7 h-7 rounded-full bg-green-100 text-green-700 text-xs font-medium flex items-center justify-center -ml-2">TV</div>
              <div class="w-7 h-7 rounded-full bg-pink-100 text-pink-700 text-xs font-medium flex items-center justify-center -ml-2">GK</div>
              <p class="text-xs text-gray-400 ml-2">3 attendees</p>
            </div>
          </div>
        </div>
      </div>
    </main>
    <div class="bg-page-yellow border-t border-black/5 px-8 py-6 flex-1">
      <h1 class="text-3xl font-semibold text-navy text-center">How it works</h1>
      <div class="grid grid-cols-1 sm:grid-cols-4 gap-4 mt-4 place-items-center flex-1 mb-6 md:mb-0">
        <div class="bg-white rounded-xl p-6 border border-black/5">
            <div class="flex flex-col items-center">
              <div class="w-8 h-8 rounded-lg bg-brand-orange-light border border-brand-orange-border flex items-center justify-center text-sm font-semibold text-brand-orange mb-4">1</div>
              <h3 class="text-base font-semibold text-navy mb-2">Create a trip</h3>
              <p class="text-sm text-gray-500 leading-relaxed">Set a date, write a description, and get a shareable invite code in seconds.</p>
            </div>
        </div>
        <div class="bg-white rounded-xl p-6 border border-black/5">
            <div class="flex flex-col items-center">
              <div class="w-8 h-8 rounded-lg bg-brand-orange-light border border-brand-orange-border flex items-center justify-center text-sm font-semibold text-brand-orange mb-4">2</div>
              <h3 class="text-base font-semibold text-navy mb-2">Invite your friends</h3>
              <p class="text-sm text-gray-500 leading-relaxed">Share the invite code and allow your friends to join in and add their ideas.</p>
            </div>
        </div>
        <div class="bg-white rounded-xl p-6 border border-black/5">
            <div class="flex flex-col items-center">
              <div class="w-8 h-8 rounded-lg bg-brand-orange-light border border-brand-orange-border flex items-center justify-center text-sm font-semibold text-brand-orange mb-4">3</div>
              <h3 class="text-base font-semibold text-navy mb-2">Build your DayTrip</h3>
              <p class="text-sm text-gray-500 leading-relaxed">Add locations, times, and plan out your itinerary--watch your Day come together.</p>
            </div>
        </div>
        <div class="bg-white rounded-xl p-6 border border-black/5">
            <div class="flex flex-col items-center">
              <div class="w-8 h-8 rounded-lg bg-brand-orange-light border border-brand-orange-border flex items-center justify-center text-sm font-semibold text-brand-orange mb-4">4</div>
              <h3 class="text-base font-semibold text-navy mb-2">Have fun!</h3>
              <p class="text-sm text-gray-500 leading-relaxed">On DayTrip day, you can keep track and alter your plan spontaneously.</p>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>
