import axios from "axios";
import { config } from "zod/v4/core";



export const useAxios = axios.create({
    baseURL: "http://127.0.0.1:8000",
    withCredentials: true,
    headers: {
        "Content-Type": "application/json"
    }
})

useAxios.interceptors.request.use((config)=>{
    const token = localStorage.getItem("access_token")

    if(token){
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

useAxios.interceptors.response.use(res =>res, (error)=>{
    if(error.response && error.response.status == 401){
        localStorage.removeItem('access_token')
        window.location.href = '/'
    }

    return Promise.reject(error)
})