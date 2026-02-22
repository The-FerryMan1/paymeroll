<script lang="ts" setup>
import type { NavigationMenuItem } from "@nuxt/ui";
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const pageTItle = computed<string>(() => route.meta.title as string);

const links = computed<NavigationMenuItem[]>(() => [
  {
    label: "Dashboard",
    icon: "i-lucide-home",
    to: { name: "dashboard" },
    active: route.name == "dashboard",
  },
  {
    label: "Employee",
    icon: "i-lucide-user",
    to: { name: "employee" },
    active: route.name == "employee",
  },
]);
</script>

<template>
  <UDashboardGroup>
    <UDashboardSidebar collapsible resizable>
      <template #header="{ collapsed }">
        <div v-if="!collapsed" class="flex items-center gap-2">
          <UIcon name="i-lucide-cog" class="size-6 text-primary mx-auto" />
          <h1 class="font-bold text-xl">Paymeroll</h1>
        </div>
        <UIcon v-else name="i-lucide-cog" class="size-6 text-primary mx-auto" />
      </template>
      <template #default="{ collapsed }">
        <UNavigationMenu
          orientation="vertical"
          :collapsed
          :items="links"
        />
      </template>
      <template #content>
        <UNavigationMenu orientation="vertical" :items="links" class="p-5" />
      </template>
    </UDashboardSidebar>

    <UDashboardPanel>
      <template #header>
        <UDashboardNavbar resizable :title="pageTItle">
          <template #leading>
            <UDashboardSidebarCollapse variant="outline"/>
          </template>
          <template #right>
            <UColorModeSelect />
          </template>
        </UDashboardNavbar>
      </template>

      <template #body>
        <RouterView />
      </template>
    </UDashboardPanel>
  </UDashboardGroup>
</template>
