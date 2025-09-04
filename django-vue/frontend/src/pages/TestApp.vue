<script>
import AddPeople from '../components/AddPeople.vue';
import HeaderComp from '../components/HeaderComp.vue';
import ItineraryMaker from '../components/ItineraryMaker.vue';
import LocationLister from '../components/LocationLister.vue';
import TripTemplate from '../components/TripTemplate.vue';
export default {
  components: {
    AddPeople,
    HeaderComp,
    ItineraryMaker,
    LocationLister,
    TripTemplate,
  }
}
</script>

<template>
    <AddPeople/>
    <HeaderComp/>
    <ItineraryMaker/>
    <LocationLister/>
    <TripTemplate/>
</template>
