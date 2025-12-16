<script setup>
import TripOverview from '@/components/TripOverview.vue';
import AddAttendees from '../components/AddAttendees.vue';
import HeaderComp from '../components/HeaderComp.vue';
import LocationLister from '../components/LocationLister.vue';

import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const code = ref(route.params.code)

</script>

<template>
  <div class="bg-gradient-to-br from-blue-300 via-white-200 to-blue-300 flex flex-col h-screen">
    <HeaderComp />
    <div class="grid grid-cols-1 md:grid-cols-2 grid-rows-2 flex-1 gap-8 py-6 px-15">
      <TripOverview :code="code" />
      <LocationLister :code="code" />
      <AddAttendees :code="code" />
    </div>
  </div>
</template>
