<script setup lang="ts">
import type { SzkolaPublicWithRelations } from "~/types/schools"

interface Props {
    selectedPoint: SzkolaPublicWithRelations
}

const props = defineProps<Props>()

const formatAddress = (school: SzkolaPublicWithRelations) => {
    const parts = []
    if (school.ulica?.nazwa) parts.push(school.ulica.nazwa)
    if (school.numer_budynku) parts.push(school.numer_budynku)
    if (school.numer_lokalu) parts.push(`lok. ${school.numer_lokalu}`)

    const addressLine1 = parts.join(" ")
    const addressLine2 = `${school.kod_pocztowy} ${school.miejscowosc?.nazwa || ""}`

    return { addressLine1, addressLine2 }
}

const formattedAddress = computed(() => formatAddress(props.selectedPoint))
</script>
<template>
    <!-- School Information Section -->
    <div class="p-6 space-y-4">
        <h4 class="section-title">Informacje o szkole</h4>

        <!-- Basic Info -->
        <div class="space-y-3">
            <!-- Student Count -->
            <div v-if="selectedPoint.liczba_uczniow" class="info-item">
                <Icon name="mdi:account-group" class="info-item-icon" />
                <div class="flex-1">
                    <p class="info-item-label">Liczba uczniów</p>
                    <p class="text-sm text-gray-900 font-medium">
                        {{ selectedPoint.liczba_uczniow }}
                    </p>
                </div>
            </div>

            <!-- Director -->
            <div
                v-if="
                    selectedPoint.dyrektor_imie ||
                    selectedPoint.dyrektor_nazwisko
                "
                class="info-item">
                <Icon name="mdi:account-tie" class="info-item-icon" />
                <div class="flex-1">
                    <p class="info-item-label">Dyrektor</p>
                    <p class="text-sm text-gray-900 font-medium">
                        {{ selectedPoint.dyrektor_imie }}
                        {{ selectedPoint.dyrektor_nazwisko }}
                    </p>
                </div>
            </div>

            <!-- Address -->
            <div class="info-item">
                <Icon name="mdi:map-marker" class="info-item-icon" />
                <div class="flex-1">
                    <p class="info-item-label">Adres</p>
                    <p class="text-sm text-gray-900">
                        {{ formattedAddress.addressLine1 }}
                    </p>
                    <p class="text-sm text-gray-900">
                        {{ formattedAddress.addressLine2 }}
                    </p>
                </div>
            </div>

            <!-- Contact Info -->
            <div v-if="selectedPoint.telefon" class="info-item">
                <Icon name="mdi:phone" class="info-item-icon" />
                <div class="flex-1">
                    <p class="info-item-label">Telefon</p>
                    <p class="text-sm text-gray-900">
                        {{ selectedPoint.telefon }}
                    </p>
                </div>
            </div>

            <div v-if="selectedPoint.email" class="info-item">
                <Icon name="mdi:email" class="info-item-icon" />
                <div class="flex-1">
                    <p class="info-item-label">Email</p>
                    <a
                        :href="`mailto:${selectedPoint.email}`"
                        class="contact-link">
                        {{ selectedPoint.email }}
                    </a>
                </div>
            </div>

            <div v-if="selectedPoint.strona_internetowa" class="info-item">
                <Icon name="mdi:web" class="info-item-icon" />
                <div class="flex-1">
                    <p class="info-item-label">Strona internetowa</p>
                    <a
                        :href="
                            selectedPoint.strona_internetowa.startsWith('http')
                                ? selectedPoint.strona_internetowa
                                : `https://${selectedPoint.strona_internetowa}`
                        "
                        target="_blank"
                        class="contact-link break-all">
                        {{ selectedPoint.strona_internetowa }}
                    </a>
                </div>
            </div>

            <!-- Educational Stages -->
            <div v-if="selectedPoint.etapy_edukacji?.length" class="info-item">
                <Icon name="mdi:book-open-variant" class="info-item-icon" />
                <div class="flex-1">
                    <p class="info-item-label mb-1">Etapy edukacji</p>
                    <div class="flex flex-wrap gap-1">
                        <span
                            v-for="etap in selectedPoint.etapy_edukacji"
                            :key="etap.id"
                            class="tag tag-indigo">
                            {{ etap.nazwa }}
                        </span>
                    </div>
                </div>
            </div>

            <!-- Professional Education -->
            <div
                v-if="selectedPoint.ksztalcenie_zawodowe?.length"
                class="info-item">
                <Icon name="mdi:briefcase-variant" class="info-item-icon" />
                <div class="flex-1">
                    <p class="info-item-label mb-1">Kształcenie zawodowe</p>
                    <div class="flex flex-wrap gap-1">
                        <span
                            v-for="ksztalcenie in selectedPoint.ksztalcenie_zawodowe"
                            :key="ksztalcenie.id"
                            class="tag tag-orange">
                            {{ ksztalcenie.nazwa }}
                        </span>
                    </div>
                </div>
            </div>

            <!-- IDs -->
            <div class="pt-3 border-t border-gray-200 space-y-2">
                <div
                    v-if="selectedPoint.numer_rspo"
                    class="flex justify-between text-xs">
                    <span class="text-gray-500">RSPO:</span>
                    <span class="text-gray-700 font-mono">{{
                        selectedPoint.numer_rspo
                    }}</span>
                </div>
                <div
                    v-if="selectedPoint.regon"
                    class="flex justify-between text-xs">
                    <span class="text-gray-500">REGON:</span>
                    <span class="text-gray-700 font-mono">{{
                        selectedPoint.regon
                    }}</span>
                </div>
                <div
                    v-if="selectedPoint.nip"
                    class="flex justify-between text-xs">
                    <span class="text-gray-500">NIP:</span>
                    <span class="text-gray-700 font-mono">{{
                        selectedPoint.nip
                    }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
@reference "tailwindcss";
.info-item {
    @apply flex items-start;
}
.info-item-icon {
    @apply w-4 h-4 text-gray-400 mt-0.5 mr-3 flex-shrink-0;
}
.info-item-label {
    @apply text-xs text-gray-500;
}
.contact-link {
    @apply text-sm text-blue-600 hover:text-blue-800;
}
.tag {
    @apply inline-flex items-center px-2 py-0.5 rounded text-xs font-medium;
}
.tag-indigo {
    @apply bg-indigo-100 text-indigo-800;
}
.tag-orange {
    @apply bg-orange-100 text-orange-800;
}
</style>
