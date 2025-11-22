<template>
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
                        Regularnie aktualizowane wyniki i statystyki szkół
                    </p>
                </div>
                <div class="text-center">
                    <img
                        src="~/assets/images/location.png"
                        alt="Lokalizacja"
                        class="feature-image" />
                    <h3 class="feature-heading">Lokalizacja</h3>
                    <p class="text-indigo-100">
                        Znajdź szkoły w swojej okolicy na interaktywnej mapie
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
