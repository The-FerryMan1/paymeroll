import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import Authenticated from '@/layouts/authenticated.vue'

const routes: RouteRecordRaw[] =[
  {
    path: '/',
    name: 'login',
    component: ()=> import("@/pages/login.vue"),
    meta: {
      title: "Login"
    }
  },
  {
    path: '/auth/admin',
    component: Authenticated,
    meta: {
       isRequiresAuth: true
    },
    children:[
        {
          path: '/',
          name: 'dashboard',
          component: ()=>import('@/pages/auth/dashboard.vue'),
          meta:{
            title: 'Dashboard',
            isRequiresAuth: true
          }
        },
        {
          path: '/employee',
          name: 'employee',
          component: ()=>import('@/pages/auth/employee.vue'),
          meta:{
            title: 'Employee',
            isRequiresAuth: true
          }
        },
    ]
  }
] 

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})


router.beforeEach((to)=>{
  document.title = `Paymeroll | ${to.meta.title}`
})

router.beforeEach((to)=>{
 const token = localStorage.getItem('access_token')
  console.log(token)
 if(!token && to.meta.isRequiresAuth){
    return '/'
 }

 if(token && !to.meta.isRequiresAuth){
  return {name:"dashboard"}
 }
 
})

export default router
