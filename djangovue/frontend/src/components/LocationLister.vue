<template>
  <div class="relative bg-white px-10 pt-10 pb-8 shadow-xl ring-1 ring-gray-900/5 mx-auto max-w-3xl rounded-lg">
    <div>
      <p class="font-serif font-bold text-2xl">Locations</p>
      <p class="font-serif text-xl">Where ya headed?</p>
    </div>
    <div>
      <ul>
        <li v-for="location in locations"> 
          <p class="hover:text-red-400 hover:line-through inline-block" @click="deletePerson(name)"> {{ location.name }} {{ location.time }} {{ location.address }} {{ location.description }}</p>
        </li>
      </ul>
      <div v-if="!addingLocation">
        <button class="rounded-md p-2.5 text-white bg-orange-500 hover:bg-orange-700" @click="addPlace">Add Location</button>
      </div>
    </div>
    <div v-if="addingLocation">
      <div class="flex">
        <p class="font-semibold">Place:</p>
        <input class="font-sans  text-gray-400 border-2 border-gray-700" maxlength="48" size="48" placeholder="Marugame Monzo" v-model="placeName"/>
        <p class="font-semibold">Time:</p>
        <input class="font-sans pl-2" type="time" v-model="placeTime">
      </div>
        <p class="font-semibold">Address:</p>
        <input type="text" class="border-2 border-gray-700" size="48" v-model="placeAddr"/>
        <img
          class="powered-by-google"
          src="https://storage.googleapis.com/geo-devrel-public-buckets/powered_by_google_on_white.png"
          alt="Powered by Google"
        />
        <p class="font-semibold">Description:</p>
        <textarea class="block w-full px-3 py-2 text-black placeholder-gray-400 transition duration-100 ease-in-out bg-white border border-gray-300 rounded shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none focus:ring-opacity-50" placeholder="A great fusion restaurant. $20-30 per!" v-model="description"></textarea>
        <button class="rounded-md p-2.5 text-white bg-orange-500 hover:bg-orange-700" @click="createLocation">Create Location</button>
        <button class="rounded-md p-1.5 text-black border-4 border-red-500 hover:border-red-700" @click="cancel">Cancel</button>
    </div>
  </div>
</template>
  
<script>
  export default {
    data() {
      return {
        locations: [],
        addingLocation: false
      }
    },
    methods: {
      addPlace() {
        this.addingLocation = true
      },
      createLocation() {
          let location = {
            "name": this.placeName,
            "time": this.placeTime,
            "address": this.placeAddr,
            "description": this.description
          }
          this.locations.push(location)
          this.cancel()
      },
      cancel() {
        this.placeName = ""
        this.placeTime = ""
        this.placeAddr = ""
        this.description = ""
        this.addingLocation = false
      }
  }
}
</script>