<script>
import HeaderComp from '../components/HeaderComp.vue';
import InitComp from '../components/InitComp.vue';
import CreateTrip from '../components/CreateTripComp.vue';
import JoinTrip from '../components/JoinTripComp.vue';

export default {
  components: {
    HeaderComp,
    InitComp,
    CreateTrip,
    JoinTrip,
  },
  data() {
    return {
      current: null,
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
  <div class="bg-slate-200 flex flex-col h-screen">
    <HeaderComp name="wow" />
    <main class="pb-20 text-center bg-gradient-to-r from-yellow-300 via-orange-400 to-yellow-300 shadow-inline">
    <InitComp @show-create="showCreate" @show-join="showJoin" v-if="!current" />
    <CreateTrip v-if="current === 'create'" />
    <JoinTrip v-if="current === 'join'" />
    </main>
    <div class="p-10 font-sans bg-sky-200 flex flex-grow">
      <p>[BIO] Lorem ipsum dolor sit amet, consectetur adipiscing elit.
      In augue libero, venenatis quis enim nec, tempor pharetra ipsum. 
      Suspendisse aliquet erat id neque sagittis, sit amet bibendum nunc 
      consequat. Praesent at diam ligula. Curabitur et laoreet turpis. 
      Curabitur suscipit purus eget libero volutpat blandit. Nulla a 
      laoreet libero. Vestibulum eget libero sollicitudin, iaculis enim 
      sit amet, eleifend odio. Nam pellentesque varius lorem, ut rutrum 
      purus vulputate ut. Sed in nunc nec odio sagittis maximus ut at tortor. 
      Fusce pretium sapien eget bibendum fringilla. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
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
