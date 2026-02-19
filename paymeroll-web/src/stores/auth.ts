import { useAxios } from "@/axios/axios";
import type { FormSubmitEvent } from "@nuxt/ui";
import type { AxiosError } from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";
import { useRouter } from "vue-router";

export const useAuthStore = defineStore("auth", () => {
  //user token
  const userToken = ref<string | null>(null);
  const errorMessage = ref<string | null>(null)
  const loading = ref<boolean>(false)

  const router = useRouter()
  // login
  async function authLogin(form: FormData) {
    loading.value = true
    try {
      const { data } = await useAxios.post("/auth/login", form, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      userToken.value = data.access_token;
      localStorage.setItem("access_token", data.access_token)
      errorMessage.value = null
      router.push({name: 'dashboard'})
      return 
    } catch (error) {
      const errMessage = error as AxiosError;
       localStorage.removeItem("access_token")
      if(errMessage.status === 401){
        errorMessage.value = "Invalid username or password"
        return
      }
    }finally{
      loading.value = false
    }
  }

  return {
    userToken,
    authLogin,
    errorMessage,
    loading
  };
});
