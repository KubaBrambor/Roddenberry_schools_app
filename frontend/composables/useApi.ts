import { useRuntimeConfig } from "nuxt/app";

export function useApi<T>(endpoint: string, options = {}) {
    const config = useRuntimeConfig();
    return useFetch<T>(`${config.public.apiBase}${endpoint}`, {
        ...options,
        onRequest({ request, options: _options }) {
            console.log("Starting Request:", request);
        },
        onResponse({ request: _request, response, options: _options }) {
            console.log("Response:", response._data);
        },
        onRequestError({ request: _request, error, options: _options }) {
            console.log("Request Error:", error);
        },
    });
}
