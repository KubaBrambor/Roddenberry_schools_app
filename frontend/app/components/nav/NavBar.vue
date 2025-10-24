<template>
    <nav
        class="top-0 z-50"
        :class="
            transparent
                ? 'fixed w-full bg-white/80'
                : 'sticky bg-white shadow-lg'
        ">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <!-- Logo/Brand -->
                <div class="flex items-center">
                    <div class="flex-shrink-0">
                        <h1 class="text-2xl font-bold">
                            <NuxtLink to="/" class="group">
                                <span
                                    class="text-gray-800 group-hover:text-indigo-600 transition-colors duration-200"
                                    >Ranking</span
                                >
                                <span
                                    class="text-indigo-600 group-hover:text-indigo-900 transition-colors duration-200"
                                    >Szkół</span
                                >
                            </NuxtLink>
                        </h1>
                    </div>
                </div>

                <!-- Navigation Links -->
                <div class="hidden md:block">
                    <div class="ml-10 flex items-baseline space-x-8">
                        <NavLinks :is-display-block="false" />
                    </div>
                </div>

                <!-- Mobile menu button -->
                <div class="md:hidden">
                    <button
                        type="button"
                        class="bg-white p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
                        :aria-expanded="isMobileMenuOpen"
                        aria-label="Otwórz menu główne"
                        @click="toggleMobileMenu">
                        <svg
                            v-if="!isMobileMenuOpen"
                            class="h-6 w-6"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                        <svg
                            v-else
                            class="h-6 w-6"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            </div>

            <!-- Mobile menu dropdown -->
            <Transition
                enter-active-class="transition duration-200 ease-out"
                enter-from-class="transform scale-95 opacity-0"
                enter-to-class="transform scale-100 opacity-100"
                leave-active-class="transition duration-150 ease-in"
                leave-from-class="transform scale-100 opacity-100"
                leave-to-class="transform scale-95 opacity-0">
                <div v-if="isMobileMenuOpen" class="md:hidden">
                    <div
                        class="px-2 pt-2 pb-3 space-y-1"
                        @click="closeMobileMenu">
                        <NavLinks :is-display-block="true" />
                    </div>
                </div>
            </Transition>
        </div>
    </nav>
</template>

<script setup lang="ts">
interface Props {
    transparent?: boolean
}

// directly destructuring props with default values
const { transparent = false } = defineProps<Props>()

const isMobileMenuOpen = ref(false)

// Toggle mobile menu visibility
const toggleMobileMenu = () => {
    isMobileMenuOpen.value = !isMobileMenuOpen.value
}

// Close mobile menu when dropdown item is clicked
const closeMobileMenu = () => {
    isMobileMenuOpen.value = false
}
</script>
