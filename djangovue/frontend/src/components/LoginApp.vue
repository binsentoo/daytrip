<template>
  <HeaderComp name="ok"></HeaderComp>
  <div :style="backgroundStyle">
    <h1 :class="h1Class">Good {{ timeOfDay }}!</h1>
    
    <div class="form-container">
      <div class="form-row">
        <input 
          type="text" 
          class="input-field" 
          placeholder="First Name" 
          v-model="firstName"
          @blur="validateField('firstName')"
          :class="{'border-red-500': !validFields.firstName}"
        >
        <input 
          type="text" 
          class="input-field" 
          placeholder="Last Name" 
          v-model="lastName"
          @blur="validateField('lastName')"
          :class="{'border-red-500': !validFields.lastName}"
        >
      </div>

      <input 
        type="text" 
        class="input-field" 
        style="width: 600px;" 
        placeholder="Address" 
        v-model="address"
        @blur="validateField('address')"
        :class="{'border-red-500': !validFields.address}"
      >
      <a href="#" :class="linkClass">Currently at home? Click here.</a>
    </div>

    <button class="rounded-md p-2.5 text-white bg-sky-500 hover:bg-sky-700 text-bold" 
    @click="submitInfo">
      Start The Adventures
    </button>
  </div>
</template>

<script>
import HeaderComp from './HeaderComp.vue';
import axios from 'axios';
export default {
  components: {
      HeaderComp
  },
  data() {
    return {
      timeOfDay: '',
      firstName: '',
      lastName: '',
      address: '',
      validFields: {
        firstName: true,
        lastName: true,
        address: true
      }
    };
  },
  mounted() {
    if (localStorage.firstName) {
      this.firstName = localStorage.firstName;
    }
    if (localStorage.lastName) {
      this.lastName = localStorage.lastName;
    }
  },
  watch: {
    firstName(newName) {
      localStorage.firstName = newName;
    },
    lastName(newName) {
      localStorage.lastName = newName;
    },
  },
  computed: {
    backgroundStyle() {
      const backgroundImage = this.getBackgroundImage();
      return {
        backgroundImage: `url('/static/vue/assets/${backgroundImage}')`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        height: '100vh',
        margin: '0',
        padding: '0'
      };
    },
    h1Class() {
      return {
        'text-white': this.timeOfDay === 'night',
        'text-black': this.timeOfDay !== 'night',
        '-translate-y-[120px]': true,
        'font-poppins': true,
        'text-9xl': true,
        'opacity-0': true,
        'fade-in-move': true
      };
    },
    linkClass() {
      return {
        'font-medium': true,
        'text-2xl': true,
        'hover:underline': true,
        'text-white': this.timeOfDay === 'morning' || this.timeOfDay === 'afternoon' || this.timeOfDay === 'night'
      };
    }
  },
  methods: {
    updateTimeOfDay() {
      const hour = new Date().getHours();
      if (hour >= 0 && hour < 6 || hour >= 19) {
        this.timeOfDay = 'night';
      } else if (hour >= 6 && hour < 11) {
        this.timeOfDay = 'morning';
      } else if (hour >= 11 && hour < 15) {
        this.timeOfDay = 'noon';
      } else {
        this.timeOfDay = 'afternoon';
      }
    },
    getBackgroundImage() {
      const hour = new Date().getHours();
      if (hour >= 0 && hour < 6 || hour >= 19) {
        return 'night.jpg';
      } else if (hour >= 6 && hour < 11) {
        return 'morning.jpg';
      } else if (hour >= 11 && hour < 15) {
        return 'noon.jpg';
      } else {
        return 'afternoon.jpg';
      }
    },
    validateField(field) {
      this.validFields[field] = !!this[field];
    },
    async submitInfo() {
      console.log("test");
      alert('It works!');
      try{
      const response = await axios.post('http://127.0.0.1:8000/adduser/',{
            "first_name": this.firstName,
            "password": "null",
            "username": "null",
            "last_name": this.lastName,
            "email": "null@gmail.com",
            "address": this.address});
      }
      catch (error) {
        console.log(error.response.data);
      }
    }
  },
  created() {
    this.updateTimeOfDay();
  },
};
</script>

<style scoped>

div {
  display: flex;
  flex-direction: column; 
  align-items: center; 
  justify-content: center; 
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 10px; 
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  flex-direction: row;
  gap: 5px;
  margin-bottom: 0%;
}

.input-field {
  width: 300px; 
  padding: 20px; 
  border: 2px solid #cccccc; 
  border-radius: 135px; 
}

.border-red-500 {
  border-color: #f56565;
}

@keyframes fadeInMove {
  from {
    opacity: 0;
    transform: translateY(-40px);
  }
  to {
    opacity: 1;
    transform: translateY(-120px);
  }
}

.fade-in-move {
  animation: fadeInMove 2s ease-in-out forwards;
}

</style>
