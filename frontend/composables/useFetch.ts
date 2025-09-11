import { useRuntimeConfig } from "nuxt/app";
import { ref } from 'vue';
import type { RspoResponse, Institution } from '../types/rspo';

export function useApiFetcher() {
  const institutions = ref<Institution[]>([]);
  const isLoading = ref(false);
  const error = ref<Error | null>(null);
  const config = useRuntimeConfig();

  async function fetchInstitutions(endpoint: string, options = {}) {
    isLoading.value = true;
    error.value = null;

    try {
      const data = await $fetch<RspoResponse>(`${config.public.apiRspo}${endpoint}`, options);

      if (data) {
        institutions.value = data['hydra:member'];
      }
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Unknown error occurred');
      console.error('Failed to fetch RSPO data:', err);
    } finally {
      isLoading.value = false;
    }

    return { institutions, error, isLoading };
  }

  return {
    institutions,
    isLoading,
    error,
    fetchInstitutions,
  };
}