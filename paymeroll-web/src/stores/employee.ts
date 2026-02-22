import { useAxios } from "@/axios/axios";
import type { AxiosError } from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";


    // "full_name": "Juan Alberto Dela Cruz",
    // "tin_no": "123-456-789-000",
    // "sss_no": "34-1234567-8",
    // "philhealth_no": "12-0500001234-9",
    // "pagibig_no": "1210-4567-8901",
    // "pay_basis": "Monthly",
    // "pay_frequency": "Semi-Monthly",
    // "base_rate": 45000,
    // "de_minimis_allowance": 2500,
    // "is_active": true,
    // "hire_date": "2026-02-17",
    // "id": 1,
    // "employee_no": "f6f893d3-d170-84be-bd2c-1fbed2667b22"


export interface Employee {
    id: number,
    employee_no: string,
    full_name: string,
    tin_no: string,
    sss_no: string,
    philhealth_no:string,
    pagibig_no: string,
    pay_basis:string,
    pay_frequency:string,
    base_rate:number,
    de_minimis_allowance:number,
    is_active: boolean,
    hire_date: string
}

export const useEmployeeStore = defineStore('employee', ()=>{
    const employees = ref<Employee[]>([])
    const loading_employee = ref<boolean>(false)
    async function getEmployees(limit:number = 10) {
        try {
            loading_employee.value = true
            const {data} = await useAxios.get("/employee", {
                params:{
                    limit: limit
                }
            })

            employees.value = data
        } catch (error) {
            const axiosErr = error as AxiosError
            console.log(axiosErr.message) 
        }finally{
            loading_employee.value = false
        }
    }




    return {
        employees,
        getEmployees,
        loading_employee

    }
})