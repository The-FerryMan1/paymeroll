<script setup lang="ts">
import type { AuthFormField, FormSubmitEvent } from '@nuxt/ui';
import Default from '@/layouts/default.vue';
import z from 'zod';
import { useAuthStore } from '@/stores/auth';


const toast = useToast()
const auth = useAuthStore()

const fields: AuthFormField[] = [
    {
        name: "email",
        type: "email",
        label: "Email",
        placeholder: "Enter your emeil",
        required: true,
    },
    {
        name: "password",
        type: "password",
        label: "Password",
        placeholder: "Enter your password",
        required: true,
    },
    {
        name: "remember",
        label: "Remember me",
        type: "checkbox"
    }
]

const schema = z.object({
    email: z.email('Invalid Email'),
    password: z.string('Password is required!').min(8, 'Must be at least 8 characters.')
})

type Schema = z.output<typeof schema>

async function onsubmit(event: FormSubmitEvent<Schema>) {

    const form = new FormData()
    form.append('username', event.data.email)
    form.append('password', event.data.password)
    await auth.authLogin(form)

    if (auth.errorMessage) {
        toast.add(
            {
                title: "Login Failed",
                description: auth.errorMessage,
                color: "error"
            }
        )
        return
    }

    toast.add(
        {

            title: "Login success",
            color: "success"
        }
    )


}


</script>

<template>
    <Default>
        <UPageHero orientation="horizontal" class="h-screen items-center flex">
            <template #title>
                <h1 class="text-primary w-full text-center">Paymeroll.</h1>
            </template>

            <template #description>
                <h2 class="text-neutral w-full text-center">Payroll system for small enterprise.</h2>
            </template>

            <template #default>
                <UPageCard orientation="vertical">
                    <UAuthForm @submit="onsubmit" :loading="auth.loading" :schema="schema" title="Welcome back!"
                        icon="i-lucide-user" description="Enter your credentials to access your accoint"
                        :fields="fields" />
                </UPageCard>
            </template>

        </UpageHero>
    </Default>
</template>