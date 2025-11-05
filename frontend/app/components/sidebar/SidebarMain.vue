<script setup lang="ts">
import type { SzkolaPublicWithRelations } from "~/types/schools"

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

            <SidebarExamResults
                v-if="selectedPoint"
                :wyniki-e8="selectedPoint.wyniki_e8"
                :wyniki-em="selectedPoint.wyniki_em" />
            <SidebarSchoolInfo
                v-if="selectedPoint"
                :selected-point="selectedPoint" />
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
</style>
