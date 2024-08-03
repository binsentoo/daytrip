<script setup>

</script>

<template>
  <header>
    <img src="./assets/vacation.jpeg" alt="DayTrip 'Icon'" id="logo" width="200" height="200">
    <h1>DayTrip!</h1>
    <div class="buttons">
      <button id="bleft" @click="createPlan">Create Plan</button>
      <button id="bright" @click="joinPlan">Join Plan</button>
  </div>
  </header>
  <main>
    <p id="bio"> [BIO] Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    In augue libero, venenatis quis enim nec, tempor pharetra ipsum. 
    Suspendisse aliquet erat id neque sagittis, sit amet bibendum nunc 
    consequat. Praesent at diam ligula. Curabitur et laoreet turpis. 
    Curabitur suscipit purus eget libero volutpat blandit. Nulla a 
    laoreet libero. Vestibulum eget libero sollicitudin, iaculis enim 
    sit amet, eleifend odio. Nam pellentesque varius lorem, ut rutrum 
    purus vulputate ut. Sed in nunc nec odio sagittis maximus ut at tortor. 
    Fusce pretium sapien eget bibendum fringilla. </p>
  </main>
</template>

<style scoped>

#logo {
  display: block;
  margin: 0 auto 0;
  max-width: 50%;
  height: auto;
}

#bio {
  margin-left: 2em;
  margin-right: 2em;
}

header {
  margin: 0;
  padding-top: 2em;
}

h1 {
  margin: 0;
  text-align: center;
  padding-top: .25em;
  padding-bottom: .5em;
}

.buttons {
  display: flex;
  justify-content: center;
}

#bleft {
  margin: 0 2em 3em auto;
  color: rgb(60, 109, 109);
}

#bright {
  margin: 0 auto 3em 2em;
  color: rgb(141, 255, 255);
}

</style>