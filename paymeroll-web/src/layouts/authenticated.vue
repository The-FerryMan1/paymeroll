<script lang="ts" setup>
import type { NavigationMenuItem } from '@nuxt/ui';
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute()

const pageTItle = computed<string>(()=> route.meta.title as string)

const links = computed<NavigationMenuItem[]>(()=>{
     let items:NavigationMenuItem[]  = []
     route.matched.forEach((c)=>{
          c.children.forEach((ch) =>{
               items.push(
                    {
                         label: ch.meta?.title as string,
                         active: route.name === ch.name,
                         to: {name: ch.name}
                         
                    }
               )
          })
     })
     
     return items
})
</script>

<template>
       <UDashboardGroup>
          <UDashboardSidebar collapsible resizable>
               <template #header="{collapsed}" >
                    <div v-if="!collapsed" class="flex items-center gap-2">
                          <UIcon name="i-lucide-cog" class="size-6 text-primary mx-auto" />
                         <h1 class="font-bold text-xl">Paymeroll</h1>
                    </div>
                     <UIcon v-else name="i-lucide-cog" class="size-6 text-primary mx-auto" />
                    
               </template>
               <template #default="{collapsed}">
                    <UNavigationMenu orientation="vertical" :collapsed class="mx-5" :items="links"/>
               </template>
               <template #content>
                     <UNavigationMenu orientation="vertical" :items="links"/>
               </template>
          </UDashboardSidebar>

          <UDashboardPanel>
               <template #header>
                    <UDashboardNavbar resizable :title="pageTItle">
                         <template #leading>
                              <UDashboardSidebarCollapse variant="outline"/>
                         </template>
                         <template #right>
                              <UColorModeSelect/>
                         </template>
                    </UDashboardNavbar>
               </template>

               <template #body >
                    <RouterView/>
               </template>
          </UDashboardPanel>
       </UDashboardGroup>
</template>

