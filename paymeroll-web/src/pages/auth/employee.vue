<script setup lang="ts">
import { useRoute } from 'vue-router';

const route = useRoute()
</script>

<template>
    <div v-for="link in route.matched">{{link.name}}</div>
</template>