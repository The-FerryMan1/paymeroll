<script lang="ts" setup>
import { useAuthStore } from "@/stores/auth";
import type { NavigationMenuItem } from "@nuxt/ui";
import { computed, resolveComponent, h } from "vue";
import { useRoute } from "vue-router";
const route = useRoute();
const overlay = useOverlay();

const UModal = resolveComponent("UModal");
const UButton = resolveComponent("UButton");
const auth = useAuthStore();
const modal = overlay.create(
  h(
    UModal,
    { title: "Are you sure you want to logout?" },
    {
      body: ()=> [
        h(UButton, {label: "Cancel",color: 'neutral'}),
        h(UButton, { label: "Logout",color: 'error', class:"ms-2", onClick: ()=>{ 
          modal.close()
          auth.authSignOut()
        }}),
      ],
    }
  ),
);

const token = computed(() => localStorage.getItem("access_token"));

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
        <UNavigationMenu orientation="vertical" :collapsed :items="links" />
      </template>
    
    </UDashboardSidebar>

    <UDashboardPanel>
      <template #header>
        <UDashboardNavbar resizable :title="pageTItle">
          <template #leading>
            <UDashboardSidebarCollapse variant="outline" />
          </template>
          <template #right>
            <UColorModeSelect />
            <UButton
              @click="modal.open"
              v-if="token"
              color="neutral"
              variant="subtle"
              icon="i-lucide-log-out"
              label="Sign out"
            />
          </template>
        </UDashboardNavbar>
      </template>

      <template #body>
        <RouterView />
      </template>
    </UDashboardPanel>
  </UDashboardGroup>
</template>
