<script setup lang="ts">
export interface UserMessageProps {
    message: string
    type?: "success" | "error" | "warning" | "info"
    autoDismiss?: boolean
    duration?: number
    showProgress?: boolean
}

const props = withDefaults(defineProps<UserMessageProps>(), {
    type: "info",
    autoDismiss: true,
    duration: 5000,
    showProgress: true,
})

const emit = defineEmits<{
    close: []
}>()

const isVisible = ref(false)
const progress = ref(100)
const timeoutId = ref<NodeJS.Timeout | null>(null)
const intervalId = ref<NodeJS.Timeout | null>(null)

/**
 * Computed property for message type styling
 */
const messageTypeClasses = computed(() => {
    switch (props.type) {
        case "success":
            return "bg-gradient-to-r from-emerald-500 to-green-500 border-emerald-400 text-white"
        case "error":
            return "bg-gradient-to-r from-red-500 to-rose-500 border-red-400 text-white"
        case "warning":
            return "bg-gradient-to-r from-amber-500 to-yellow-500 border-amber-400 text-amber-900"
        case "info":
        default:
            return "bg-gradient-to-r from-blue-500 to-indigo-500 border-blue-400 text-white"
    }
})

/**
 * Computed property for message icon
 */
const messageIcon = computed(() => {
    switch (props.type) {
        case "success":
            return "✓"
        case "error":
            return "⚠"
        case "warning":
            return "!"
        case "info":
        default:
            return "i"
    }
})

/**
 * Closes the message
 */
const closeMessage = () => {
    clearTimers()
    isVisible.value = false
    emit("close")
}

/**
 * Clears all active timers
 */
const clearTimers = () => {
    if (timeoutId.value) {
        clearTimeout(timeoutId.value)
        timeoutId.value = null
    }
    if (intervalId.value) {
        clearInterval(intervalId.value)
        intervalId.value = null
    }
}

/**
 * Starts the auto-dismiss timer with progress tracking
 */
const startAutoDismiss = () => {
    if (!props.autoDismiss) return

    const startTime = Date.now()
    const updateInterval = 50

    intervalId.value = setInterval(() => {
        const elapsed = Date.now() - startTime
        const remaining = Math.max(0, props.duration - elapsed)
        progress.value = (remaining / props.duration) * 100

        if (remaining <= 0) {
            closeMessage()
        }
    }, updateInterval)

    timeoutId.value = setTimeout(() => {
        closeMessage()
    }, props.duration)
}

onMounted(() => {
    // Add a small delay to make the slide-in animation more visible
    setTimeout(() => {
        isVisible.value = true
        startAutoDismiss()
    }, 200)
})

onUnmounted(() => {
    clearTimers()
})
</script>

<template>
    <Transition name="slide">
        <div
            v-if="isVisible"
            :class="[
                'fixed top-6 left-1/2 -translate-x-1/2 max-w-sm w-auto min-w-80 z-50',
                'rounded-xl shadow-2xl border backdrop-blur-sm overflow-hidden',
                messageTypeClasses,
            ]"
            role="alert"
            :aria-live="type === 'error' ? 'assertive' : 'polite'">
            <!-- Progress bar -->
            <div
                v-if="showProgress && autoDismiss"
                class="absolute top-0 left-0 h-1 bg-white/20 rounded-t-xl overflow-hidden"
                style="width: 100%">
                <div
                    class="h-full bg-white/60 shadow-sm transition-all duration-75 ease-linear relative"
                    :style="{ width: `${progress}%` }">
                    <div
                        class="absolute inset-0 bg-gradient-to-r from-transparent via-white/40 to-transparent"></div>
                </div>
            </div>

            <!-- Message content -->
            <div class="flex items-start gap-4 p-5">
                <!-- Icon -->
                <div
                    class="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full bg-white/20 backdrop-blur-sm">
                    <span
                        class="text-lg font-bold drop-shadow-sm"
                        :aria-label="`${type} message`">
                        {{ messageIcon }}
                    </span>
                </div>

                <!-- Message text -->
                <div class="flex-1 min-w-0">
                    <p
                        class="text-sm font-medium leading-relaxed break-words drop-shadow-sm">
                        {{ message }}
                    </p>
                </div>

                <!-- Close button -->
                <button
                    class="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full hover:bg-white/25 active:bg-white/35 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-white/60 focus:ring-offset-1 focus:ring-offset-transparent group"
                    :aria-label="'Close notification'"
                    type="button"
                    @click="closeMessage">
                    <svg
                        class="w-4 h-4 transition-transform duration-200 group-hover:scale-110"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg">
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2.5"
                            d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <!-- Bottom glow -->
            <div
                class="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white/30 to-transparent"></div>
        </div>
    </Transition>
</template>

<style scoped>
@reference "tailwindcss";
.slide-enter-active {
    @apply transition duration-500 ease-out;
}
.slide-leave-active {
    @apply transition duration-400 ease-in;
}
.slide-enter-from {
    @apply -translate-x-2/1 opacity-0 scale-95;
}
.slide-enter-to,
.slide-leave-from {
    @apply -translate-x-1/2 left-1/2 opacity-100 scale-100;
}
.slide-leave-to {
    @apply translate-x-full opacity-0 scale-95;
}
</style>
