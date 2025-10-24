<script setup lang="ts">
import type {
    SzkolaPublicWithRelations,
    SzkolaPublicShort,
} from "~/types/schools"

const route = useRoute()

// Create a computed property for query parameters to refetch data after changing them
const queryParams = computed(() => ({
    ...route.query,
}))

const { data, status } = useApi<SzkolaPublicShort[]>("/schools", {
    // useFetch will automatically unwrap the .value of the computed property
    // and re-run the fetch when the computed value changes.
    query: queryParams,
})

// Reactive state for sidebar
const isSidebarOpen = ref(false)
const selectedSchool = ref<SzkolaPublicWithRelations | null>(null)

const handlePointClick = (school: SzkolaPublicWithRelations) => {
    selectedSchool.value = school
    isSidebarOpen.value = true
}

const handleSidebarClose = () => {
    isSidebarOpen.value = false
    selectedSchool.value = null
}
</script>

<template>
    <div>
        <NavBar transparent />

        <!-- Sidebar -->
        <MapSidebar
            :is-open="isSidebarOpen"
            :selected-point="selectedSchool"
            @close="handleSidebarClose" />
        <UserMessage
            v-if="status === 'pending'"
            message="Loading map data, please wait..." />
        <UserMessage
            v-if="status === 'error'"
            type="error"
            message="An error occurred while loading map data." />

        <!-- MapView taking full remaining space with dynamic margin for sidebar -->
        <div :class="['transition-all duration-300']">
            <MapView :schools="data" @point-clicked="handlePointClick" />
        </div>
    </div>
</template>
