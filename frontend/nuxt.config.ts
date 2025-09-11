import { defineNuxtConfig } from "nuxt/config";
export default defineNuxtConfig({

    compatibilityDate: "2025-08-23",

    devtools: {
        enabled: true,
        timeline: {
            enabled: true,
        },
    },

    css: [
        'maplibre-gl/dist/maplibre-gl.css'
    ],

    runtimeConfig: {
        public: {
            apiBase: process.env.NUXT_PUBLIC_API_BASE || "/api",
            apiRspo: process.env.NUXT_PUBLIC_API_RSPO || "https://api-rspo.men.gov.pl/api",
        },
    },
    
    modules: ["@nuxt/eslint"],
    vite: {
        server: {
            fs: {
                allow: [
                    '..'
                ]
            }
        }
    }
});