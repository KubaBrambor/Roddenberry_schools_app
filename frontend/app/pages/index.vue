<script setup lang="ts">
import { ref } from "vue"
import { VOIVODESHIP_NAMES } from "~/constants/voivodeships"

const isMobileMenuOpen = ref(false)

const selectedVoivodeship = ref<string>("")

const handleVoivodeshipSelect = (voivodeshipId: string) => {
    selectedVoivodeship.value = voivodeshipId
}

const handleSearchSubmit = async (searchParams: {
    schoolType: number
    voivodeship: string
}) => {
    const voivodeshipData = VOIVODESHIP_NAMES[searchParams.voivodeship]
    if (!voivodeshipData) {
        console.error("Voivodeship not found:", searchParams.voivodeship)
        return
    }

    const coordinates = voivodeshipData.coordinates
    const bbox = `${coordinates.min_lng},${coordinates.min_lat},${coordinates.max_lng},${coordinates.max_lat}`

    await navigateTo({
        path: "/map",
        query: {
            bbox: bbox,
            type: searchParams.schoolType,
        },
    })
}
</script>

<template>
    <div
        class="min-h-screen bg-linear-to-br from-blue-100 via-white to-indigo-200">
        <!-- Navigation Bar -->
        <NavBar @toggle-menu="isMobileMenuOpen = !isMobileMenuOpen" />

        <!-- Main Content -->
        <main class="max-w-7xl mx-auto px-2 sm:px-5 lg:px-8 py-8">
            <!-- Hero Section -->
            <div class="text-center mb-12">
                <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-4">
                    Ranking
                    <span class="text-indigo-600">Szkół</span>
                    w Polsce
                </h1>
                <p class="text-xl text-gray-600 max-w-3xl mx-auto leading-8">
                    Znajdź najlepsze szkoły w swojej okolicy. Porównuj wyniki,
                    sprawdzaj rankingi i podejmuj świadome decyzje dotyczące
                    dalszej edukacji.
                </p>
            </div>

            <!-- Main Content Grid -->
            <div class="grid lg:grid-cols-2 gap-12 items-start">
                <!-- Form Section -->
                <SchoolSearchForm
                    :selected-voivodeship="selectedVoivodeship"
                    @submit="handleSearchSubmit"
                    @clear-voivodeship="selectedVoivodeship = ''" />

                <!-- Map Section -->
                <div class="content-card">
                    <div class="mb-2">
                        <h2 class="text-2xl font-bold text-gray-900 mb-2">
                            Mapa województw
                        </h2>
                        <p class="text-gray-600">
                            Kliknij na województwo, aby je wybrać
                        </p>
                    </div>

                    <div class="relative p-2">
                        <VoivodeshipsMap
                            @path-click="handleVoivodeshipSelect" />

                        <!-- Map overlay for selected voivodeship -->
                        <div
                            v-if="selectedVoivodeship"
                            class="absolute top-0 right-0 bg-indigo-100 text-indigo-800 px-3 py-2 rounded-lg text-sm border border-indigo-200">
                            <p>
                                Wybrano:
                                {{
                                    VOIVODESHIP_NAMES[selectedVoivodeship]?.name
                                }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Additional Info Section -->
            <div
                class="mt-16 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl p-8 text-white">
                <div class="text-center">
                    <h2 class="text-3xl font-bold mb-4">
                        Dlaczego warto korzystać z naszego rankingu?
                    </h2>
                    <div class="grid md:grid-cols-3 gap-8 mt-8">
                        <div class="text-center">
                            <img
                                src="~/assets/images/up-to-date_data.png"
                                alt="Aktualne dane"
                                class="feature-image" />
                            <h3 class="feature-heading">Aktualne dane</h3>
                            <p class="text-indigo-100">
                                Regularnie aktualizowane wyniki i statystyki
                                szkół
                            </p>
                        </div>
                        <div class="text-center">
                            <img
                                src="~/assets/images/location.png"
                                alt="Lokalizacja"
                                class="feature-image" />
                            <h3 class="feature-heading">Lokalizacja</h3>
                            <p class="text-indigo-100">
                                Znajdź szkoły w swojej okolicy na interaktywnej
                                mapie
                            </p>
                        </div>
                        <div class="text-center">
                            <img
                                src="~/assets/images/school_comparison.png"
                                alt="Łatwa porównywarka"
                                class="feature-image" />
                            <h3 class="feature-heading">Łatwa porównywarka</h3>
                            <p class="text-indigo-100">
                                Porównuj szkoły według różnych kryteriów
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <AppFooter />
    </div>
</template>

<style scoped>
@reference "tailwindcss";

.feature-image {
    @apply w-24 h-24 rounded-full mb-4 mx-auto object-cover border-2 border-white/30;
}

.feature-heading {
    @apply text-xl font-semibold mb-2;
}
</style>
