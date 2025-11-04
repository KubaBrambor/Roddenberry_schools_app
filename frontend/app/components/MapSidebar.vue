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
    return status.toLowerCase().includes("publiczn")
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
            'w-72 md:w-96 border-r border-gray-200',
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
                        <svg
                            class="badge-icon"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z" />
                        </svg>
                        {{ selectedPoint.typ?.nazwa || "Szkoła" }}
                    </span>

                    <!-- Public/Private Status Badge -->
                    <span
                        class="badge"
                        :class="[
                            isPublicSchool(
                                selectedPoint.status_publicznoprawny?.nazwa ||
                                    '',
                            )
                                ? 'badge-green'
                                : 'badge-purple',
                        ]">
                        <svg
                            class="badge-icon"
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
                <h4 class="section-title">Wyniki egzaminów</h4>

                <!-- E8 Results -->
                <div v-if="selectedPoint.wyniki_e8?.length" class="mb-6">
                    <h5 class="exam-title">
                        <svg
                            class="exam-icon text-blue-500"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                fill-rule="evenodd"
                                d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                                clip-rule="evenodd" />
                        </svg>
                        Egzamin ósmoklasisty
                    </h5>
                    <div class="overflow-x-auto">
                        <table class="min-w-full results-table">
                            <thead class="border-b border-gray-200">
                                <tr>
                                    <th
                                        class="px-1 py-2 text-left text-xs font-medium text-gray-700">
                                        Przedmiot
                                    </th>
                                    <th
                                        v-for="year in groupResultsBySubject(
                                            selectedPoint.wyniki_e8,
                                        ).years"
                                        :key="`e8-year-${year}`"
                                        class="px-1 py-2 text-center text-xs font-medium text-gray-700">
                                        {{ year }}
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">
                                <tr
                                    v-for="(
                                        yearData, subject
                                    ) in groupResultsBySubject(
                                        selectedPoint.wyniki_e8,
                                    ).grouped"
                                    :key="`e8-${subject}`">
                                    <td class="table-cell whitespace-nowrap">
                                        {{ subject }}
                                    </td>
                                    <td
                                        v-for="year in groupResultsBySubject(
                                            selectedPoint.wyniki_e8,
                                        ).years"
                                        :key="`e8-${subject}-${year}`"
                                        class="table-cell text-center">
                                        <template v-if="yearData[year]">
                                            <div
                                                class="font-medium text-gray-900">
                                                {{
                                                    yearData[
                                                        year
                                                    ].wynik_sredni?.toFixed(
                                                        1,
                                                    ) || "-"
                                                }}%
                                            </div>
                                            <div class="text-gray-500">
                                                {{
                                                    yearData[
                                                        year
                                                    ].mediana?.toFixed(1) ||
                                                    "-"
                                                }}%
                                            </div>
                                            <div
                                                class="text-gray-400 text-[10px]">
                                                ({{
                                                    yearData[year]
                                                        .liczba_zdajacych ||
                                                    "-"
                                                }})
                                            </div>
                                        </template>
                                        <span v-else class="text-gray-400"
                                            >-</span
                                        >
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Matura Results -->
                <div v-if="selectedPoint.wyniki_em?.length">
                    <h5 class="exam-title">
                        <svg
                            class="exam-icon text-green-500"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762z" />
                        </svg>
                        Egzamin maturalny
                    </h5>
                    <div class="overflow-x-auto">
                        <table class="min-w-full results-table">
                            <thead class="border-b border-gray-200">
                                <tr>
                                    <th
                                        class="px-1 py-2 text-left text-xs font-medium text-gray-700">
                                        Przedmiot
                                    </th>
                                    <th
                                        v-for="year in groupResultsBySubject(
                                            selectedPoint.wyniki_em,
                                        ).years"
                                        :key="`em-year-${year}`"
                                        class="px-1 py-2 text-center text-xs font-medium text-gray-700">
                                        {{ year }}
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">
                                <tr
                                    v-for="(
                                        yearData, subject
                                    ) in groupResultsBySubject(
                                        selectedPoint.wyniki_em,
                                    ).grouped"
                                    :key="`em-${subject}`">
                                    <td class="table-cell whitespace-nowrap">
                                        {{ subject }}
                                    </td>
                                    <td
                                        v-for="year in groupResultsBySubject(
                                            selectedPoint.wyniki_em,
                                        ).years"
                                        :key="`em-${subject}-${year}`"
                                        class="table-cell text-center">
                                        <template v-if="yearData[year]">
                                            <div
                                                class="font-medium text-gray-900">
                                                {{
                                                    yearData[
                                                        year
                                                    ].sredni_wynik?.toFixed(
                                                        1,
                                                    ) || "-"
                                                }}%
                                            </div>
                                            <div
                                                v-if="yearData[year].zdawalnosc"
                                                :style="{
                                                    color: getColor(
                                                        yearData[year]
                                                            .zdawalnosc,
                                                    ),
                                                }">
                                                {{
                                                    yearData[
                                                        year
                                                    ].zdawalnosc.toFixed(0)
                                                }}%
                                            </div>
                                            <div
                                                class="text-gray-400 text-[10px]">
                                                ({{
                                                    yearData[year]
                                                        .liczba_zdajacych ||
                                                    "-"
                                                }})
                                            </div>
                                        </template>
                                        <span v-else class="text-gray-400"
                                            >-</span
                                        >
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- School Information Section -->
            <div class="p-6 space-y-4">
                <h4 class="section-title">Informacje o szkole</h4>

                <!-- Basic Info -->
                <div class="space-y-3">
                    <!-- Student Count -->
                    <div v-if="selectedPoint.liczba_uczniow" class="info-item">
                        <svg
                            class="info-item-icon"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z" />
                        </svg>
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
                        <svg
                            class="info-item-icon"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                fill-rule="evenodd"
                                d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                                clip-rule="evenodd" />
                        </svg>
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
                        <svg
                            class="info-item-icon"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                fill-rule="evenodd"
                                d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
                                clip-rule="evenodd" />
                        </svg>
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
                        <svg
                            class="info-item-icon"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
                        </svg>
                        <div class="flex-1">
                            <p class="info-item-label">Telefon</p>
                            <p class="text-sm text-gray-900">
                                {{ selectedPoint.telefon }}
                            </p>
                        </div>
                    </div>

                    <div v-if="selectedPoint.email" class="info-item">
                        <svg
                            class="info-item-icon"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                            <path
                                d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                        </svg>
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
                        <svg
                            class="info-item-icon"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                fill-rule="evenodd"
                                d="M4.083 9h1.946c.089-1.546.383-2.97.837-4.118A6.004 6.004 0 004.083 9zM10 2a8 8 0 100 16 8 8 0 000-16zm0 2c-.076 0-.232.032-.465.262-.238.234-.497.623-.737 1.182-.389.907-.673 2.142-.766 3.556h3.936c-.093-1.414-.377-2.649-.766-3.556-.24-.56-.5-.948-.737-1.182C10.232 4.032 10.076 4 10 4zm3.971 5c-.089-1.546-.383-2.97-.837-4.118A6.004 6.004 0 0115.917 9h-1.946zm-2.003 2H8.032c.093 1.414.377 2.649.766 3.556.24.56.5.948.737 1.182.233.23.389.262.465.262.076 0 .232-.032.465-.262.238-.234.498-.623.737-1.182.389-.907.673-2.142.766-3.556zm1.166 4.118c.454-1.147.748-2.572.837-4.118h1.946a6.004 6.004 0 01-2.783 4.118zm-6.268 0C6.412 13.97 6.118 12.546 6.029 11H4.083a6.004 6.004 0 002.783 4.118z"
                                clip-rule="evenodd" />
                        </svg>
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
                        <svg
                            class="info-item-icon"
                            fill="currentColor"
                            viewBox="0 0 20 20">
                            <path
                                d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
                        </svg>
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
                        <svg
                            class="info-item-icon"
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

        <!-- Empty State -->
        <div
            v-else
            class="flex items-center justify-center h-full p-6 text-center">
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
            <p class="mt-2 text-sm text-gray-500">Wybierz szkołę na mapie</p>
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
.table-cell {
    @apply px-3 py-2 text-xs;
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
