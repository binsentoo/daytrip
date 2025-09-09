import { createRouter, createWebHistory } from "vue-router";
import HomepageApp from "@/pages/HomeApp.vue";
import DaytripApp from "@/pages/DaytripApp.vue";

const routes = [
    { path: '/', name: 'Home', component: HomepageApp },
    { path: '/daytrip/:code', name: 'Daytrip', component: DaytripApp }
]

export const router = createRouter({
  history: createWebHistory(''),
  routes,
})

export default router