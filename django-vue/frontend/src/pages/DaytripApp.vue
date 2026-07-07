<script setup>
import TripOverview from '@/components/TripOverview.vue';
import AddAttendees from '../components/AddAttendees.vue';
import HeaderComp from '../components/HeaderComp.vue';
import LocationLister from '../components/LocationLister.vue';
import MapComp from '@/components/MapComp.vue'

import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const code = ref(route.params.code)

</script>

<template>
  <div class="bg-gradient-to-br from-page-yellow to-page-yellow-dark flex flex-col h-screen">
    <HeaderComp />
    <div class="grid grid-cols-1 md:grid-cols-[300px_1fr_1fr] md:grid-rows-2 flex-1 gap-3 md:gap-8 py-6 px-2 md:px-10 items-start">
      <TripOverview :code="code" />
      <LocationLister :code="code" />
      <AddAttendees :code="code" />
      <MapComp :code="code" />
    </div>
  </div>
</template>
