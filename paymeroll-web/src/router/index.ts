import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'


const routes: RouteRecordRaw[] =[
  {
    path: '/',
    name: 'login',
    component: ()=> import("@/pages/login.vue"),
    meta: {
      title: "Login"
    }
  }
] 

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})


router.beforeEach((to)=>{
  document.title = `Paymeroll | ${to.meta.title}`
})

export default router
