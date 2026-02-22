<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';


const route = useRoute()
const auth = useAuthStore()
onMounted(async()=>{
    await auth.me()
})
</script>

<template>
   <div>{{ auth.userInfo }}</div>
</template>