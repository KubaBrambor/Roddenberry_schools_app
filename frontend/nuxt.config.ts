import tailwindcss from "@tailwindcss/vite"
import { defineNuxtConfig } from "nuxt/config"
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: "2025-08-23",
    devtools: { enabled: true },

    // Runtime environment configuration
    runtimeConfig: {
        public: {
            apiBase: process.env.NUXT_PUBLIC_API_BASE || "/api",
        },
    },

    // Add tailwind as Vite plugin
    css: ["~/assets/css/main.css"],
    icon: {
        mode: "css",
        cssLayer: "base",
    },
    vite: {
        plugins: [tailwindcss()],
    },

    modules: ["@nuxt/eslint", "nuxt-maplibre", "@nuxt/icon"],
})
