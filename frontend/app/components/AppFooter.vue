<template>
    <footer class="bg-gray-900 text-white mt-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 text-center">
            <h3 class="feature-heading">Ranking Szkół</h3>
            <p class="text-gray-400 mb-8">
                Najlepsze narzędzie do znajdowania szkół w Polsce
            </p>
            <div class="flex flex-wrap justify-center gap-6 md:gap-8">
                <a href="#" class="footer-nav-link">O nas</a>
                <a href="#" class="footer-nav-link">Kontakt</a>
                <a href="#" class="footer-nav-link">Polityka prywatności</a>
            </div>
        </div>
    </footer>
</template>

<style scoped>
@reference "tailwindcss";

.footer-nav-link {
    @apply text-gray-400 hover:text-white transition-colors;
}
</style>
