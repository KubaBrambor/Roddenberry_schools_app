<script setup lang="ts">
import { NAVIGATION_LINKS } from "~/constants/links"

const props = defineProps({
    isDisplayBlock: Boolean,
})
</script>

<template>
    <NuxtLink
        v-for="link in NAVIGATION_LINKS"
        :key="link.href"
        :to="link.href"
        :class="{ block: props.isDisplayBlock }"
        class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">
        {{ link.label }}
    </NuxtLink>
</template>
