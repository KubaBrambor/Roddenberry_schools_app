<script setup lang="ts">
import type {
    WynikEMPublicWithPrzedmiot,
    SzkolaPublicWithRelations,
    WynikE8PublicWithPrzedmiot,
} from "~/types/schools"

interface Props {
    isOpen: boolean
    selectedPoint: SzkolaPublicWithRelations | null
}

const props = defineProps<Props>()

// Define emits for closing the sidebar
const emit = defineEmits<{
    close: []
}>()

const closeSidebar = () => {
    emit("close")
}

// Helper function to determine if school is public
const isPublicSchool = (status: string) => {
    return !status.toLowerCase().includes("nie")
}

const { getColor } = useScoreColor()

// Computed property for selected point score color
const scoreColor = computed(() => {
    return props.selectedPoint ? getColor(props.selectedPoint.score) : ""
})

// Group exam results by subject
const groupResultsBySubject = (
    results: WynikE8PublicWithPrzedmiot[] | WynikEMPublicWithPrzedmiot[],
) => {
    const grouped: Record<
        string,
        Record<number, WynikE8PublicWithPrzedmiot | WynikEMPublicWithPrzedmiot>
    > = {}
    const years = new Set<number>()

    results.forEach((result) => {
        const subjectName = result.przedmiot.nazwa
        years.add(result.rok)

        if (!grouped[subjectName]) {
            grouped[subjectName] = {}
        }
        grouped[subjectName][result.rok] = result
    })

    return { grouped, years: Array.from(years).sort() }
}

const formatAddress = (school: SzkolaPublicWithRelations) => {
    const parts = []
    if (school.ulica?.nazwa) parts.push(school.ulica.nazwa)
    if (school.numer_budynku) parts.push(school.numer_budynku)
    if (school.numer_lokalu) parts.push(`lok. ${school.numer_lokalu}`)

    const addressLine1 = parts.join(" ")
    const addressLine2 = `${school.kod_pocztowy} ${school.miejscowosc?.nazwa || ""}`

    return { addressLine1, addressLine2 }
}
</script>

<template>
    <div
        :class="[
            'fixed top-0 left-0 h-full bg-white shadow-2xl transition-transform duration-300 z-50',
            'max-w-md min-w-xs  border-r border-gray-200',
            isOpen ? 'transform translate-x-0' : 'transform -translate-x-full',
        ]">
        <!-- Sidebar Header -->
        <div
            class="sticky top-0 bg-white z-10 border-b border-gray-200 flex items-center justify-between p-4">
            <h2 class="text-lg font-semibold text-gray-900">
                Szczegóły szkoły
            </h2>
            <button
                class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                aria-label="Zamknij panel"
                @click="closeSidebar">
                <Icon name="mdi:close" class="w-6 h-6 text-gray-600" />
            </button>
        </div>

        <!-- Sidebar Content - Scrollable -->
        <div v-if="selectedPoint" class="h-full overflow-y-auto pb-20">
            <!-- School Header Section -->
            <div
                class="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 border-b">
                <h3 class="text-xl font-bold text-gray-900 mb-3">
                    {{ selectedPoint.nazwa }}
                </h3>

                <div class="flex flex-wrap gap-2 mb-4">
                    <!-- School Type Badge -->
                    <span class="badge badge-blue">
                        <Icon name="mdi:school-outline" class="badge-icon" />
                        {{ selectedPoint.typ?.nazwa || "Szkoła" }}
                    </span>

                    <!-- Public/Private Status Badge -->
                    <span
                        class="badge"
                        :class="[
                            isPublicSchool(
                                selectedPoint.status_publicznoprawny.nazwa ||
                                    '',
                            )
                                ? 'badge-green'
                                : 'badge-purple',
                        ]">
                        <Icon
                            v-if="
                                isPublicSchool(
                                    selectedPoint.status_publicznoprawny
                                        .nazwa || '',
                                )
                            "
                            name="mdi:check-decagram" />
                        <Icon v-else name="mdi:lock" />
                        {{ selectedPoint.status_publicznoprawny.nazwa }}
                    </span>
                </div>

                <!-- Score Display -->
                <div class="bg-white rounded-xl p-4 shadow-sm">
                    <div class="flex items-center justify-between">
                        <div>
                            <p
                                class="text-xs text-gray-500 uppercase tracking-wide mb-1">
                                Wynik ogólny
                            </p>
                            <div class="flex items-baseline">
                                <span
                                    :class="'text-3xl font-bold'"
                                    :style="{
                                        color: scoreColor,
                                    }">
                                    {{ Math.round(selectedPoint.score) }}
                                </span>
                                <span class="text-sm text-gray-500 ml-1"
                                    >/ 100</span
                                >
                            </div>
                        </div>
                    </div>
                    <!-- Score Bar -->
                    <div class="mt-3 w-full bg-gray-200 rounded-full h-2">
                        <div
                            :class="[
                                'h-2 rounded-full transition-all duration-500',
                            ]"
                            :style="{
                                width: `${selectedPoint.score}%`,
                                'background-color': scoreColor,
                            }" />
                    </div>
                </div>
            </div>

            <!-- Exam Results Section -->
            <div
                v-if="
                    selectedPoint.wyniki_e8?.length ||
                    selectedPoint.wyniki_em?.length
                "
                class="p-6 border-b">
                <h4 class="exam-title">
                    <Icon name="mdi:school" class="exam-icon text-green-500" />
                    Wyniki z egzaminów
                </h4>

                <!-- E8 Results Table -->
                <div
                    v-if="selectedPoint.wyniki_e8?.length"
                    class="overflow-x-auto">
                    <table class="w-full text-sm">
                        <thead>
                            <tr class="border-b border-gray-300">
                                <th
                                    class="text-left py-2 px-2 font-semibold text-gray-700">
                                    Przedmiot
                                </th>
                                <th
                                    v-for="year in groupResultsBySubject(
                                        selectedPoint.wyniki_e8,
                                    ).years"
                                    :key="`year-${year}`"
                                    class="text-center py-2 px-2 font-semibold text-gray-700">
                                    {{ year }}
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="(
                                    yearData, subject
                                ) in groupResultsBySubject(
                                    selectedPoint.wyniki_e8,
                                ).grouped"
                                :key="`e8-${subject}`"
                                class="border-b border-gray-200">
                                <td class="py-3 px-2 text-gray-900">
                                    <div class="font-medium">{{ subject }}</div>
                                </td>
                                <td
                                    v-for="year in groupResultsBySubject(
                                        selectedPoint.wyniki_e8,
                                    ).years"
                                    :key="`e8-${subject}-${year}`"
                                    class="text-center py-3 px-2">
                                    <template v-if="yearData[year]">
                                        <div
                                            class="text-2xl font-bold mb-1"
                                            :style="{
                                                color: getColor(
                                                    yearData[year]
                                                        .wynik_sredni || 0,
                                                ),
                                            }">
                                            {{
                                                Math.round(
                                                    yearData[year]
                                                        .wynik_sredni || 0,
                                                )
                                            }}
                                        </div>
                                        <div class="text-xs text-gray-500">
                                            {{
                                                yearData[year].liczba_zdajacych
                                                    ? `#${yearData[year].liczba_zdajacych}`
                                                    : ""
                                            }}
                                        </div>
                                    </template>
                                    <span v-else class="text-gray-300">-</span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Matura Results Table -->
                <div
                    v-if="selectedPoint.wyniki_em?.length"
                    class="overflow-x-auto">
                    <table class="w-full text-sm">
                        <thead>
                            <tr class="border-b border-gray-300">
                                <th
                                    class="text-left py-2 px-2 font-semibold text-gray-700">
                                    Przedmiot
                                </th>
                                <th
                                    v-for="year in groupResultsBySubject(
                                        selectedPoint.wyniki_em,
                                    ).years"
                                    :key="`year-${year}`"
                                    class="text-center py-2 px-2 font-semibold text-gray-700">
                                    {{ year }}
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="(
                                    yearData, subject
                                ) in groupResultsBySubject(
                                    selectedPoint.wyniki_em,
                                ).grouped"
                                :key="`em-${subject}`"
                                class="border-b border-gray-200">
                                <td class="py-3 px-2 text-gray-900">
                                    <div class="font-medium">{{ subject }}</div>
                                </td>
                                <td
                                    v-for="year in groupResultsBySubject(
                                        selectedPoint.wyniki_em,
                                    ).years"
                                    :key="`em-${subject}-${year}`"
                                    class="text-center py-3 px-2">
                                    <template v-if="yearData[year]">
                                        <div
                                            class="text-2xl font-bold mb-1"
                                            :style="{
                                                color: getColor(
                                                    yearData[year]
                                                        .sredni_wynik || 0,
                                                ),
                                            }">
                                            {{
                                                Math.round(
                                                    yearData[year]
                                                        .sredni_wynik || 0,
                                                )
                                            }}
                                        </div>
                                        <div class="text-xs text-gray-500">
                                            {{
                                                yearData[year].liczba_zdajacych
                                                    ? `#${yearData[year].liczba_zdajacych}`
                                                    : ""
                                            }}
                                        </div>
                                    </template>
                                    <span v-else class="text-gray-300">-</span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

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
                                {{ formatAddress(selectedPoint).addressLine1 }}
                            </p>
                            <p class="text-sm text-gray-900">
                                {{ formatAddress(selectedPoint).addressLine2 }}
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

                    <div
                        v-if="selectedPoint.strona_internetowa"
                        class="info-item">
                        <Icon name="mdi:web" class="info-item-icon" />
                        <div class="flex-1">
                            <p class="info-item-label">Strona internetowa</p>
                            <a
                                :href="
                                    selectedPoint.strona_internetowa.startsWith(
                                        'http',
                                    )
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
                    <div
                        v-if="selectedPoint.etapy_edukacji?.length"
                        class="info-item">
                        <Icon
                            name="mdi:book-open-variant"
                            class="info-item-icon" />
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
                        <Icon
                            name="mdi:briefcase-variant"
                            class="info-item-icon" />
                        <div class="flex-1">
                            <p class="info-item-label mb-1">
                                Kształcenie zawodowe
                            </p>
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
        </div>
    </div>

    <!-- Overlay for mobile -->
    <div
        v-if="isOpen"
        class="fixed inset-0 bg-black opacity-25 z-40 lg:hidden"
        @click="closeSidebar" />
</template>

<style scoped>
@reference "tailwindcss";

.badge-icon {
    @apply w-3 h-3 mr-1.5;
}
.badge {
    @apply inline-flex items-center px-3 py-1 rounded-full text-xs font-medium;
}
.badge-blue {
    @apply bg-blue-100 text-blue-800;
}
.badge-green {
    @apply bg-green-100 text-green-800;
}
.badge-purple {
    @apply bg-purple-100 text-purple-800;
}
.section-title {
    @apply text-sm font-semibold text-gray-900 uppercase tracking-wide mb-4;
}
.exam-title {
    @apply text-sm font-medium text-gray-700 mb-3 flex items-center;
}
.exam-icon {
    @apply w-4 h-4 mr-2;
}
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
