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

defineProps<Props>()

// Define emits for closing the sidebar
const emit = defineEmits<{
    close: []
}>()

const closeSidebar = () => {
    emit("close")
}

// Helper function to determine if school is public
const isPublicSchool = (status: string) => {
    return status.toLowerCase().includes("publiczn")
}

// Helper function to get score color
const getScoreColor = (score: number) => {
    if (score >= 75) return "text-green-600"
    if (score >= 50) return "text-yellow-600"
    return "text-red-600"
}

const getScoreBgColor = (score: number) => {
    if (score >= 75) return "bg-green-100"
    if (score >= 50) return "bg-yellow-100"
    return "bg-red-100"
}

// Group exam results by year
const groupResultsByYear = (
    results: WynikE8PublicWithPrzedmiot[] | WynikEMPublicWithPrzedmiot[],
) => {
    return results.reduce(
        (acc, result) => {
            if (!acc[result.rok]) {
                acc[result.rok] = []
            }
            acc[result.rok]?.push(result)
            return acc
        },
        {} as Record<
            number,
            WynikE8PublicWithPrzedmiot[] | WynikEMPublicWithPrzedmiot[]
        >,
    )
}

// Format address
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
            'w-72 md:w-96 border-r border-gray-200',
            isOpen ? 'transform translate-x-0' : 'transform -translate-x-full',
        ]">
        <!-- Sidebar Header -->
        <div class="sticky top-0 bg-white z-10 border-b border-gray-200">
            <div class="flex items-center justify-between p-4">
                <h2 class="text-lg font-semibold text-gray-900">
                    Szczegóły szkoły
                </h2>
                <button
                    class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    aria-label="Zamknij panel"
                    @click="closeSidebar">
                    <svg
                        class="w-5 h-5 text-gray-500"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
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
                    <span
                        class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        <svg
                            class="w-3 h-3 mr-1.5"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z" />
                        </svg>
                        {{ selectedPoint.typ?.nazwa || "Szkoła" }}
                    </span>

                    <!-- Public/Private Status Badge -->
                    <span
                        :class="[
                            'inline-flex items-center px-3 py-1 rounded-full text-xs font-medium',
                            isPublicSchool(
                                selectedPoint.status_publicznoprawny?.nazwa ||
                                    '',
                            )
                                ? 'bg-green-100 text-green-800'
                                : 'bg-purple-100 text-purple-800',
                        ]">
                        <svg
                            class="w-3 h-3 mr-1.5"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                v-if="
                                    isPublicSchool(
                                        selectedPoint.status_publicznoprawny
                                            ?.nazwa || '',
                                    )
                                "
                                fill-rule="evenodd"
                                d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                clip-rule="evenodd" />
                            <path
                                v-else
                                fill-rule="evenodd"
                                d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                                clip-rule="evenodd" />
                        </svg>
                        {{
                            selectedPoint.status_publicznoprawny?.nazwa ||
                            "Status nieznany"
                        }}
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
                                    :class="[
                                        'text-3xl font-bold',
                                        getScoreColor(selectedPoint.score),
                                    ]">
                                    {{ Math.round(selectedPoint.score) }}
                                </span>
                                <span class="text-sm text-gray-500 ml-1"
                                    >/ 100</span
                                >
                            </div>
                        </div>
                        <div
                            :class="[
                                'w-16 h-16 rounded-full flex items-center justify-center',
                                getScoreBgColor(selectedPoint.score),
                            ]">
                            <svg
                                :class="[
                                    'w-8 h-8',
                                    getScoreColor(selectedPoint.score),
                                ]"
                                fill="currentColor"
                                viewBox="0 0 20 20">
                                <path
                                    d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                            </svg>
                        </div>
                    </div>
                    <!-- Score Bar -->
                    <div class="mt-3">
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div
                                :class="[
                                    'h-2 rounded-full transition-all duration-500',
                                    selectedPoint.score >= 75
                                        ? 'bg-green-500'
                                        : selectedPoint.score >= 50
                                          ? 'bg-yellow-500'
                                          : 'bg-red-500',
                                ]"
                                :style="{ width: `${selectedPoint.score}%` }" />
                        </div>
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
                <h4
                    class="text-sm font-semibold text-gray-900 uppercase tracking-wide mb-4">
                    Wyniki egzaminów
                </h4>

                <!-- E8 Results -->
                <div v-if="selectedPoint.wyniki_e8?.length" class="mb-6">
                    <h5
                        class="text-sm font-medium text-gray-700 mb-3 flex items-center">
                        <svg
                            class="w-4 h-4 mr-2 text-blue-500"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                fill-rule="evenodd"
                                d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                                clip-rule="evenodd" />
                        </svg>
                        Egzamin ósmoklasisty
                    </h5>
                    <div
                        v-for="(results, year) in groupResultsByYear(
                            selectedPoint.wyniki_e8,
                        )"
                        :key="`e8-${year}`"
                        class="mb-4">
                        <p class="text-xs font-medium text-gray-500 mb-2">
                            Rok {{ year }}
                        </p>
                        <div class="bg-gray-50 rounded-lg overflow-x-auto">
                            <table class="min-w-full">
                                <thead>
                                    <tr class="bg-gray-100">
                                        <th
                                            class="px-3 py-2 text-left text-xs font-medium text-gray-700">
                                            Przedmiot
                                        </th>
                                        <th
                                            class="px-3 py-2 text-center text-xs font-medium text-gray-700">
                                            Średnia
                                        </th>
                                        <th
                                            class="px-3 py-2 text-center text-xs font-medium text-gray-700">
                                            Mediana
                                        </th>
                                        <th
                                            class="px-3 py-2 text-center text-xs font-medium text-gray-700">
                                            Zdających
                                        </th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-gray-200">
                                    <tr
                                        v-for="result in results"
                                        :key="result.id"
                                        class="hover:bg-gray-50">
                                        <td
                                            class="px-3 py-2 text-xs text-gray-900">
                                            {{ result.przedmiot.nazwa }}
                                        </td>
                                        <td
                                            class="px-3 py-2 text-xs text-center font-medium text-gray-900">
                                            {{
                                                result.wynik_sredni?.toFixed(
                                                    1,
                                                ) || "-"
                                            }}%
                                        </td>
                                        <td
                                            class="px-3 py-2 text-xs text-center text-gray-600">
                                            {{
                                                result.mediana?.toFixed(1) ||
                                                "-"
                                            }}%
                                        </td>
                                        <td
                                            class="px-3 py-2 text-xs text-center text-gray-600">
                                            {{ result.liczba_zdajacych || "-" }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- Matura Results -->
                <div v-if="selectedPoint.wyniki_em?.length">
                    <h5
                        class="text-sm font-medium text-gray-700 mb-3 flex items-center">
                        <svg
                            class="w-4 h-4 mr-2 text-green-500"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762z" />
                        </svg>
                        Egzamin maturalny
                    </h5>
                    <div
                        v-for="(results, year) in groupResultsByYear(
                            selectedPoint.wyniki_em,
                        )"
                        :key="`em-${year}`"
                        class="mb-4">
                        <p class="text-xs font-medium text-gray-500 mb-2">
                            Rok {{ year }}
                        </p>
                        <div class="bg-gray-50 rounded-lg overflow-x-auto">
                            <table class="min-w-full">
                                <thead>
                                    <tr class="bg-gray-100">
                                        <th
                                            class="px-3 py-2 text-left text-xs font-medium text-gray-700">
                                            Przedmiot
                                        </th>
                                        <th
                                            class="px-3 py-2 text-center text-xs font-medium text-gray-700">
                                            Średnia
                                        </th>
                                        <th
                                            class="px-3 py-2 text-center text-xs font-medium text-gray-700">
                                            Zdawalność
                                        </th>
                                        <th
                                            class="px-3 py-2 text-center text-xs font-medium text-gray-700">
                                            Zdających
                                        </th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-gray-200">
                                    <tr
                                        v-for="result in results"
                                        :key="result.id"
                                        class="hover:bg-gray-50">
                                        <td
                                            class="px-3 py-2 text-xs text-gray-900">
                                            {{ result.przedmiot.nazwa }}
                                        </td>
                                        <td
                                            class="px-3 py-2 text-xs text-center font-medium text-gray-900">
                                            {{
                                                result.sredni_wynik?.toFixed(
                                                    1,
                                                ) || "-"
                                            }}%
                                        </td>
                                        <td
                                            class="px-3 py-2 text-xs text-center">
                                            <span
                                                v-if="result.zdawalnosc"
                                                :class="[
                                                    'inline-flex px-2 py-0.5 rounded-full font-medium',
                                                    result.zdawalnosc >= 90
                                                        ? 'bg-green-100 text-green-800'
                                                        : result.zdawalnosc >=
                                                            70
                                                          ? 'bg-yellow-100 text-yellow-800'
                                                          : 'bg-red-100 text-red-800',
                                                ]">
                                                {{
                                                    result.zdawalnosc.toFixed(
                                                        0,
                                                    )
                                                }}%
                                            </span>
                                            <span v-else>-</span>
                                        </td>
                                        <td
                                            class="px-3 py-2 text-xs text-center text-gray-600">
                                            {{ result.liczba_zdajacych || "-" }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <!-- School Information Section -->
            <div class="p-6 space-y-4">
                <h4
                    class="text-sm font-semibold text-gray-900 uppercase tracking-wide mb-4">
                    Informacje o szkole
                </h4>

                <!-- Basic Info -->
                <div class="space-y-3">
                    <!-- Student Count -->
                    <div
                        v-if="selectedPoint.liczba_uczniow"
                        class="flex items-start">
                        <svg
                            class="w-4 h-4 text-gray-400 mt-0.5 mr-3 flex-shrink-0"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z" />
                        </svg>
                        <div class="flex-1">
                            <p class="text-xs text-gray-500">Liczba uczniów</p>
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
                        class="flex items-start">
                        <svg
                            class="w-4 h-4 text-gray-400 mt-0.5 mr-3 flex-shrink-0"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                fill-rule="evenodd"
                                d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                                clip-rule="evenodd" />
                        </svg>
                        <div class="flex-1">
                            <p class="text-xs text-gray-500">Dyrektor</p>
                            <p class="text-sm text-gray-900 font-medium">
                                {{ selectedPoint.dyrektor_imie }}
                                {{ selectedPoint.dyrektor_nazwisko }}
                            </p>
                        </div>
                    </div>

                    <!-- Address -->
                    <div class="flex items-start">
                        <svg
                            class="w-4 h-4 text-gray-400 mt-0.5 mr-3 flex-shrink-0"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                fill-rule="evenodd"
                                d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
                                clip-rule="evenodd" />
                        </svg>
                        <div class="flex-1">
                            <p class="text-xs text-gray-500">Adres</p>
                            <p class="text-sm text-gray-900">
                                {{ formatAddress(selectedPoint).addressLine1 }}
                            </p>
                            <p class="text-sm text-gray-900">
                                {{ formatAddress(selectedPoint).addressLine2 }}
                            </p>
                        </div>
                    </div>

                    <!-- Contact Info -->
                    <div v-if="selectedPoint.telefon" class="flex items-start">
                        <svg
                            class="w-4 h-4 text-gray-400 mt-0.5 mr-3 flex-shrink-0"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
                        </svg>
                        <div class="flex-1">
                            <p class="text-xs text-gray-500">Telefon</p>
                            <p class="text-sm text-gray-900">
                                {{ selectedPoint.telefon }}
                            </p>
                        </div>
                    </div>

                    <div v-if="selectedPoint.email" class="flex items-start">
                        <svg
                            class="w-4 h-4 text-gray-400 mt-0.5 mr-3 flex-shrink-0"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                            <path
                                d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                        </svg>
                        <div class="flex-1">
                            <p class="text-xs text-gray-500">Email</p>
                            <a
                                :href="`mailto:${selectedPoint.email}`"
                                class="text-sm text-blue-600 hover:text-blue-800">
                                {{ selectedPoint.email }}
                            </a>
                        </div>
                    </div>

                    <div
                        v-if="selectedPoint.strona_internetowa"
                        class="flex items-start">
                        <svg
                            class="w-4 h-4 text-gray-400 mt-0.5 mr-3 flex-shrink-0"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                fill-rule="evenodd"
                                d="M4.083 9h1.946c.089-1.546.383-2.97.837-4.118A6.004 6.004 0 004.083 9zM10 2a8 8 0 100 16 8 8 0 000-16zm0 2c-.076 0-.232.032-.465.262-.238.234-.497.623-.737 1.182-.389.907-.673 2.142-.766 3.556h3.936c-.093-1.414-.377-2.649-.766-3.556-.24-.56-.5-.948-.737-1.182C10.232 4.032 10.076 4 10 4zm3.971 5c-.089-1.546-.383-2.97-.837-4.118A6.004 6.004 0 0115.917 9h-1.946zm-2.003 2H8.032c.093 1.414.377 2.649.766 3.556.24.56.5.948.737 1.182.233.23.389.262.465.262.076 0 .232-.032.465-.262.238-.234.498-.623.737-1.182.389-.907.673-2.142.766-3.556zm1.166 4.118c.454-1.147.748-2.572.837-4.118h1.946a6.004 6.004 0 01-2.783 4.118zm-6.268 0C6.412 13.97 6.118 12.546 6.029 11H4.083a6.004 6.004 0 002.783 4.118z"
                                clip-rule="evenodd" />
                        </svg>
                        <div class="flex-1">
                            <p class="text-xs text-gray-500">
                                Strona internetowa
                            </p>
                            <a
                                :href="selectedPoint.strona_internetowa"
                                target="_blank"
                                class="text-sm text-blue-600 hover:text-blue-800 break-all">
                                {{ selectedPoint.strona_internetowa }}
                            </a>
                        </div>
                    </div>

                    <!-- Educational Stages -->
                    <div
                        v-if="selectedPoint.etapy_edukacji?.length"
                        class="flex items-start">
                        <svg
                            class="w-4 h-4 text-gray-400 mt-0.5 mr-3 flex-shrink-0"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
                        </svg>
                        <div class="flex-1">
                            <p class="text-xs text-gray-500 mb-1">
                                Etapy edukacji
                            </p>
                            <div class="flex flex-wrap gap-1">
                                <span
                                    v-for="etap in selectedPoint.etapy_edukacji"
                                    :key="etap.id"
                                    class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-indigo-100 text-indigo-800">
                                    {{ etap.nazwa }}
                                </span>
                            </div>
                        </div>
                    </div>

                    <!-- Professional Education -->
                    <div
                        v-if="selectedPoint.ksztalcenie_zawodowe?.length"
                        class="flex items-start">
                        <svg
                            class="w-4 h-4 text-gray-400 mt-0.5 mr-3 flex-shrink-0"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                fill-rule="evenodd"
                                d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z"
                                clip-rule="evenodd" />
                            <path
                                d="M2 13.692V16a2 2 0 002 2h12a2 2 0 002-2v-2.308A24.974 24.974 0 0110 15c-2.796 0-5.487-.46-8-1.308z" />
                        </svg>
                        <div class="flex-1">
                            <p class="text-xs text-gray-500 mb-1">
                                Kształcenie zawodowe
                            </p>
                            <div class="flex flex-wrap gap-1">
                                <span
                                    v-for="ksztalcenie in selectedPoint.ksztalcenie_zawodowe"
                                    :key="ksztalcenie.id"
                                    class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-orange-100 text-orange-800">
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

        <!-- Empty State -->
        <div v-else class="flex items-center justify-center h-full p-6">
            <div class="text-center">
                <svg
                    class="mx-auto h-12 w-12 text-gray-400"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                <p class="mt-2 text-sm text-gray-500">
                    Wybierz szkołę na mapie
                </p>
            </div>
        </div>
    </div>

    <!-- Overlay for mobile -->
    <div
        v-if="isOpen"
        class="fixed inset-0 bg-black opacity-25 z-40 lg:hidden"
        @click="closeSidebar" />
</template>
