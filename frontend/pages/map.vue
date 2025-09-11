// plik: pages/map.vue

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { useApiFetcher } from "~/composables/useFetch";
import { useSchoolMap } from "~/composables/useSchoolMap";
import type { Institution, School } from "~/types/rspo";

const { institutions, isLoading, error, fetchInstitutions } = useApiFetcher();
const { initializeMap } = useSchoolMap();

const schoolsForMap = ref<School[]>([]);

onMounted(() => {
  fetchInstitutions("/placowki/", {
    method: "GET",
    params: {
      page: 30,
    },
  });
});

watch(institutions, (newInstitutions) => {
  if (newInstitutions && newInstitutions.length > 0) {
    schoolsForMap.value = newInstitutions.map((institution: Institution) => {
      return {
        name: institution.nazwa,
        type: institution.typ.nazwa,
        lat: institution.geolokalizacja.latitude,
        lon: institution.geolokalizacja.longitude,
        value: Math.floor(Math.random() * 100), 
      };
    });

    initializeMap('map', schoolsForMap.value);
  }
});
</script>

<template>
  <div class="map-container">
    <h1>Mapa OpenStreetMap (MapLibre) - Szkoły</h1>
    <div v-if="isLoading" class="status-message loading">Ładowanie danych...</div>
    <div v-else-if="error" class="status-message error">Błąd: {{ error.message }}</div>
    <div v-else-if="schoolsForMap.length === 0 && !isLoading" class="status-message">Brak szkół do wyświetlenia</div>
    
    <div id="map"></div>
  </div>
</template>
<style scoped src="~/assets/css/map.css"></style>