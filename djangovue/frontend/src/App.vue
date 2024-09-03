<script setup>
import HeaderComp from './components/HeaderComp.vue';
</script>

<template>
  <div class="bg-slate-200 flex flex-col h-screen">
    <HeaderComp name="wow" />
    <main class="pb-20 text-center bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 shadow-inline">
      <div class="bg-white inline-block mt-16 rounded-lg shadow-2xl">
        <div>
          <img class="mx-auto p-7 pb-2" src="/static/vue/assets/vacation.jpeg" alt="DayTrip 'Icon'" width="250" height="250">
        </div>
        <div class="flex items-center justify-center mt-6 gap-x-6 pb-5">
          <button class="rounded-md p-2.5 text-white bg-sky-500 hover:bg-sky-700" @click="createPlan">
            <a href="/login/">Create Plan</a>
          </button>
          <button class="rounded-md p-2.5 text-white bg-violet-500 hover:bg-violet-700" @click="joinPlan">
            <a href="/login">Join Plan</a>
          </button>
        </div>
      </div>
    </main>
    <div class="p-10 font-sans bg-sky-300 flex flex-grow">
      <p>[BIO] Lorem ipsum dolor sit amet, consectetur adipiscing elit.
      In augue libero, venenatis quis enim nec, tempor pharetra ipsum. 
      Suspendisse aliquet erat id neque sagittis, sit amet bibendum nunc 
      consequat. Praesent at diam ligula. Curabitur et laoreet turpis. 
      Curabitur suscipit purus eget libero volutpat blandit. Nulla a 
      laoreet libero. Vestibulum eget libero sollicitudin, iaculis enim 
      sit amet, eleifend odio. Nam pellentesque varius lorem, ut rutrum 
      purus vulputate ut. Sed in nunc nec odio sagittis maximus ut at tortor. 
      Fusce pretium sapien eget bibendum fringilla. </p>
      </div>
  </div>
</template>
