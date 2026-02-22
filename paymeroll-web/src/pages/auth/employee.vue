<script setup lang="ts">
import { useEmployeeStore, type Employee } from "@/stores/employee";
import type { SelectItem, TableColumn } from "@nuxt/ui";
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const employee = useEmployeeStore()
//filters
const limit = ref<number>(10);
const search = ref<string | null>(null)
const items = computed<SelectItem[]>(() => [
  {
    label: "no-filter",
    value: "no_filter",
    icon: "i-lucide-x"
  },
  {
    label: "desc-date",
    value: "desc_date",
    icon: "i-lucide-arrow-down-narrow-wide"
  },
  {
    label: "asc-date",
    value: "asc_date",
     icon: "i-lucide-arrow-up-narrow-wide"
  },
  {
    label: "desc-id",
    value: "desc_id",
     icon: "i-lucide-arrow-down-0-1"
  },
  {
    label: "asc-id",
    value: "asc_id",
     icon: "i-lucide-arrow-up-0-1"
  },
  {
    label: "asc-hired-date",
    value: "asc_hired_date",
     icon: "i-lucide-calendar-arrow-up"
  },
   {
    label: "desc-hired-date",
    value: "desc_hired_date",
     icon: "i-lucide-calendar-arrow-down"
  },
  {
    label: "alphabetical-order-name",
    value: "alphabetical_order_name",
     icon: "i-lucide-arrow-down-a-z"
  },
]);

const headers: TableColumn<Employee>[] = [
  {
    accessorKey: 'id',
    header: '#',
    cell: ({ row }) => `#${row.getValue('id')}`
  },
   {
    accessorKey: 'employee_no',
    header: 'Employee no.',
    cell: ({ row }) => `${row.getValue('employee_no')}`
  },
  {
    accessorKey: 'full_name',
    header: 'Full name',
    cell: ({ row }) => `${row.getValue('full_name')}`
  },
    {
    accessorKey: 'base_rate',
    header: 'Base rate',
    cell: ({ row }) => `${row.getValue('base_rate')}`
  },
   {
    accessorKey: 'pay_basis',
    header: 'Pay basis',
    cell: ({ row }) => `${row.getValue('pay_basis')}`
  },
  {
    accessorKey: 'pay_frequency',
    header: 'Pay frequency',
    cell: ({ row }) => `${row.getValue('pay_frequency')}`
  },
  {
    accessorKey: 'sss_no',
    header: 'SSS no.',
    cell: ({ row }) => `${row.getValue('sss_no')}`
  },
    {
    accessorKey: 'philhealth_no',
    header: 'Philhealth no.',
    cell: ({ row }) => `${row.getValue('philhealth_no')}`
  },
     {
    accessorKey: 'tin_no',
    header: 'Tin no.',
    cell: ({ row }) => `${row.getValue('tin_no')}`
  },
      {
    accessorKey: 'pagibig_no',
    header: 'Pag-Ibig no.',
    cell: ({ row }) => `${row.getValue('pagibig_no')}`
  },
     {
    accessorKey: 'de_minimis_allowance',
    header: 'De minimis allowance',
    cell: ({ row }) => `${row.getValue('de_minimis_allowance')}`
  },
       {
    accessorKey: 'is_active',
    header: 'Active',
    cell: ({ row }) => `${row.getValue('is_active')}`
  },


] 


onMounted(async()=>{
  await employee.getEmployees()
})
</script>

<template>
  <div>
    <!-- tools -->
    <section>
      <div class="flex justify-end items-center gap-2">
        <UInput v-model="search" class="w-full" type="search" icon="" placeholder="Search...." leading-icon="i-lucide-search"/>
        <USelect :items="items" placeholder="apply filters" leading-icon="i-lucide-funnel" />
        <UInput v-model="limit" type="number" :placeholder="'limit:10'" leading-icon="i-lucide-pin" />
        <UButton label="CSV Export" leading-icon="i-lucide-file-up"/>
        <UButton label="Add" leading-icon="i-lucide-plus"/>
      </div>
      <!-- search -->

      <div>
          <UTable :data="employee.employees" :columns="headers" :loading="true" class="flex-1"/>

      </div>
    </section>
  </div>
</template>
