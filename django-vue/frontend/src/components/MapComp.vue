<template>
  <div class="bg-white shadow-xl ring-1 ring-gray-900/5 rounded-lg p-4">
    <div class="flex items-center justify-between mb-3">
      <p class="text-base font-semibold text-navy">Map</p>
      <span class="text-xs text-gray-400">{{ activities.length }} stops</span>
    </div>
    <div ref="mapEl" class="w-full h-56 rounded-lg bg-gray-100"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

const props = defineProps({ code: String })

const mapEl = ref(null)
const activities = ref([])
let map = null

async function fetchActivities() {
  try {
    const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
    const response = await axios.get(`${API_BASE}/api/daytrips/${props.code}/`)
    activities.value = response.data.activities.filter(a => a.lat && a.lng)
    initMap()
  } catch (error) {
    console.error('Error fetching activities:', error)
  }
}

function initMap() {
    
  if (!mapEl.value || activities.value.length === 0) return

  const center = { lat: activities.value[0].lat, lng: activities.value[0].lng }

  map = new google.maps.Map(mapEl.value, {
    center,
    zoom: 13,
    disableDefaultUI: true,
    zoomControl: true,
  })

  activities.value.forEach((activity, index) => {
    const marker = new google.maps.Marker({
      position: { lat: activity.lat, lng: activity.lng },
      map,
      title: activity.name,
      label: {
        text: String(index + 1),
        color: '#fff',
        fontSize: '12px',
        fontWeight: '500',
      },
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        fillColor: '#f97316',
        fillOpacity: 1,
        strokeColor: '#fff',
        strokeWeight: 2,
        scale: 14,
      },
    })

    const infoWindow = new google.maps.InfoWindow({
      content: `<div style="font-size:13px;font-weight:500">${activity.name}</div><div style="font-size:11px;color:#6b7280">${activity.start_time.slice(0,5)}</div>`,
    })

    marker.addListener('click', () => {
      infoWindow.open(map, marker)
    })
  })

  // fit map to all markers
  if (activities.value.length > 1) {
    const bounds = new google.maps.LatLngBounds()
    activities.value.forEach(a => bounds.extend({ lat: a.lat, lng: a.lng }))
    map.fitBounds(bounds)
  }
}

onMounted(() => {
  fetchActivities()
})
</script>