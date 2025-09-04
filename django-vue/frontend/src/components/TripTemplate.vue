<template>
  <div class="max-w-4xl mx-auto p-6 bg-white shadow-md rounded-lg mt-8">
    <!-- Loading State -->
    <div v-if="loading" class="text-center text-gray-500 text-lg">
      Loading trip details...
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
      <strong class="font-bold">Error:</strong>
      <span class="block sm:inline">{{ error }}</span>
    </div>

    <!-- Trip Details -->
    <div v-else>
      <!-- Trip Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-800">{{ trip.name }}</h1>
        <p class="text-gray-600 mt-2">{{ trip.description }}</p>
      </div>

      <!-- Trip Metadata -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
          <span class="font-semibold">Trip UID:</span> {{ trip.UID }}
        </div>
        <div>
          <span class="font-semibold">Duration:</span>
          {{ formatDate(trip.start_time) }} to {{ formatDate(trip.end_time) }}
        </div>
        <div>
          <span class="font-semibold">Total Cost:</span>
          ${{ trip.final_min_cost.toFixed(2) }} - ${{ trip.final_max_cost.toFixed(2) }}
        </div>
      </div>

      <!-- Events Section -->
      <div>
        <h2 class="text-2xl font-semibold text-gray-700 mb-4">Events</h2>
        <div class="space-y-4">
          <div v-for="event in trip.events" :key="event.id" class="border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
            <h3 class="text-xl font-bold text-indigo-600">{{ event.name }}</h3>
            <p class="text-gray-600 mt-2">{{ event.description }}</p>
            <div class="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2">
              <div>
                <span class="font-semibold">Time:</span>
                {{ formatDate(event.start_time) }} - {{ formatDate(event.end_time) }}
              </div>
              <div>
                <span class="font-semibold">Location:</span> {{ event.location }}
              </div>
              <div>
                <span class="font-semibold">Cost:</span> ${{ event.min_cost }} - ${{ event.max_cost }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TripDetails',
  data() {
    return {
      trip: null,
      loading: true,
      error: null,
    };
  },
  methods: {
    async fetchTripDetails() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/gettrip/000000/');
        this.trip = response.data;
      } catch (err) {
        if (err.response) {
          // Server responded with a status other than 2xx
          this.error = `Error ${err.response.status}: ${err.response.data.detail || err.response.statusText}`;
        } else if (err.request) {
          // Request was made but no response received
          this.error = 'No response from the server. Please check your network connection or the server status.';
        } else {
          // Something happened in setting up the request
          this.error = `Request Error: ${err.message}`;
        }
      } finally {
        this.loading = false;
      }
    },  
    formatDate(dateString) {
      const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },  
  },
  mounted() {
    this.fetchTripDetails();
  },  
};
</script>


<style scoped>

</style>