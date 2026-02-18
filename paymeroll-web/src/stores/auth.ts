import { useAxios } from "@/axios/axios";
import type { FormSubmitEvent } from "@nuxt/ui";
import type { AxiosError } from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useAuthStore = defineStore("auth", () => {
  //user token
  const userToken = ref<string | null>(null);
  // login
  async function authLogin(form: FormData) {
    console.log(form);
    try {
      const { data } = await useAxios.post("/auth/login", form, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      userToken.value = data.access_token;
    } catch (error) {
      const errMessage = error as AxiosError;
      if(errMessage.status === 401){
        console.log("Invalid username or password")
        return
      }

      console.log(error);
    }
  }

  return {
    userToken,
    authLogin,
  };
});
