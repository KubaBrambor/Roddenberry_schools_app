<script setup lang="ts">
import { useApi } from "../composables/useApi";

interface BackendResponse {
    message: string;
}

const { data, error, status } = useApi<BackendResponse>("/users");
</script>

<template>
  <div>
    <div>
      <h1>Test połączenia z backendem</h1>
      <div v-if="status === 'pending'">Ładowanie...</div>
      <div v-else-if="error">Błąd: {{ error }}</div>
      <div v-else>
        <p>Odpowiedź z backendu: {{ data?.message }}</p>
      </div>
    </div>
    <div>
      <h1>Tu masz przejscie do mapy \/</h1>
      <NuxtLink to="/map">Przejdź do mapy</NuxtLink>
    </div>
  </div>
</template>

<style scoped>
</style>