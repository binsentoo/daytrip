<template>
<div class="relative bg-white px-10 pt-10 pb-8 shadow-xl ring-1 ring-gray-900/5 mx-auto max-w-lg rounded-lg">
  <div class="flex pb-1">
      <div v-if="!editMode">
        <p class="font-serif text-2xl">{{title}}</p>
        <button @click="editTitle">
          <svg class="h-8 w-8 text-slate-900 float-right" width="24"  height="24"  viewBox="0 0 24 24"  xmlns="http://www.w3.org/2000/svg"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round">  <path d="M12 20h9" />  <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" /></svg>
        </button>
      </div>
      <div v-if="editMode">
        <input v-model="tempValue" class="font-serif text-2xl"/>
        <button @click="saveTitle">
          <svg class="h-8 w-8 text-slate-900"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round">  <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" />  <polyline points="17 21 17 13 7 13 7 21" />  <polyline points="7 3 7 8 15 8" /></svg>
        </button>
      </div>
  </div>
  <div>
    <div class="flex pb-1">
      <p class="font-semibold">Date:</p>
      <input class="font-sans pl-2" type="datetime-local"> 
    </div>
    <div>
      <p class="font-semibold pb-1">Length:</p>
    </div>
    <p class="font-semibold">Description:</p>
    <textarea class="block w-full px-3 py-2 text-black placeholder-gray-400 transition duration-100 ease-in-out bg-white border border-gray-300 rounded shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none focus:ring-opacity-50" placeholder="Describe your event!" v-model="description"></textarea>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      title: 'Event Name',
      editMode: false,
    }
  },
  methods: {
    editTitle() {
      this.editMode = true
    },
    saveTitle() {
      this.editMode = false
    }
  }
}
</script>