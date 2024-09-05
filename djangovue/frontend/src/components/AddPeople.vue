<template>
    <div class="relative bg-white px-10 pt-10 pb-8 shadow-xl ring-1 ring-gray-900/5 mx-auto max-w-xs rounded-lg">
      <div class="flex justify-between">
        <p class="font-serif text-2xl">Invite List</p>
        <button @click="addPerson">
          <svg class="h-8 w-8 text-slate-900 flex"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round">  <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />  <circle cx="8.5" cy="7" r="4" />  <line x1="20" y1="8" x2="20" y2="14" />  <line x1="23" y1="11" x2="17" y2="11" /></svg>
        </button>
      </div>
      <ul>
        <li v-for="name in names" :key="name"> {{ name }} </li>
      </ul>
      <div v-if="invitePerson" class="flex justify-between">
        <div>
          <input class="font-sans focus:text-gray-500 text-gray-400 border-2 border-gray-700" maxlength="16" size="16" placeholder="Name" v-model="personName"/>
        </div>
        <div class="flex align-middle">
          <button @click="createPerson">
            <svg class="h-6 w-6 text-slate-900"  width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">  <path stroke="none" d="M0 0h24v24H0z"/>  <path d="M5 12l5 5l10 -10" /></svg>
          </button>
          <button @click="cancelPerson">
            <svg class="h-6 w-6 text-slate-900"  width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">  <path stroke="none" d="M0 0h24v24H0z"/>  <line x1="18" y1="6" x2="6" y2="18" />  <line x1="6" y1="6" x2="18" y2="18" /></svg>
          </button>
        </div>
      </div>
      <div>
        <p>invite link here?</p>
      </div>
    </div>
  </template>
    
  <script>
  export default {
    data() {
      return {
        invitePerson: false,
        names: []
      }
    },
    methods: {
      addPerson() {
        this.invitePerson = true
      },
      createPerson() {
        this.names.push(this.personName)
        this.personName = ""
        this.invitePerson = false
      },
      cancelPerson() {
        this.invitePerson = false
      }
    }
  }
  </script>