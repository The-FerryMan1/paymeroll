import axios from "axios";
import type { constants } from "fs";


export const useAxios = axios.create({
    baseURL: "http://127.0.0.1:8000",
    withCredentials: true,
    headers: {
        "Content-Type": "application/json"
    }
})