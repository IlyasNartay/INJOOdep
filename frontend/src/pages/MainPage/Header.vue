<template>
  <!-- Navigation Header -->
  <div class="relative overflow-hidden">
    <!-- 🔴 Видео на фоне -->
    <video
      autoplay
      muted
      loop
      playsinline
      class="absolute top-0 left-0 w-full min-h-screen object-cover z-0"
    >
      <source src="@/assets/bubbleteaVideo.mp4" type="video/mp4" />
      Ваш браузер не поддерживает видео.
    </video>
    <div class="relative z-20 min-h-screen">
      <nav
        class="absolute flex items-start justify-between px-6 py-4 z-20 w-full h-12"
      >
        <!-- Logo -->
        <img class="w-[80px] h-auto" src="/src/assets/injoo-logo.png" />

        <a href="/auth">
          <button
            @click="check"
            class="bg-green-200 hover:bg-green-300 text-gray-900 px-2 py-1 text-sm rounded-lg font-medium transition-colors sm:px-6 sm:py-2 sm:text-base max-[370px]:text-[10px] max-[370px]:max-w-[100px]"
          >
            Вход / Регистрация
          </button>
        </a>

        <!-- Mobile Menu Button -->
        <!-- <button
          @click="toggleMobileMenu"
          class="md:hidden bg-green-200 hover:bg-green-300 text-gray-900 px-4 py-2 rounded-lg"
        >
          <svg
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            ></path>
          </svg>
        </button> -->
      </nav>

      <!-- Mobile Navigation Menu -->
      <div
        v-if="mobileMenuOpen"
        class="fixed inset-0 z-50 md:hidden bg-white bg-opacity-95 backdrop-blur-sm flex flex-col"
      >
        <!-- Header -->
        <div class="flex items-center justify-between px-6 py-4 border-b">
          <!-- Логотип -->
          <h1 class="text-xl font-bold text-gray-900">INJOO</h1>

          <!-- Кнопка закрытия -->
          <button
            @click="mobileMenuOpen = false"
            class="p-2 rounded-full hover:bg-gray-200 transition-colors"
          >
            <!-- Иконка крестика -->
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6 text-gray-800"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        <!-- Navigation -->
        <div class="flex flex-col items-center justify-center flex-1 space-y-8">
          <a
            href="#"
            class="text-2xl font-semibold text-gray-900 hover:text-cyan-600 transition-colors"
          >
            Главная
          </a>
          <a
            href="#"
            class="text-2xl font-semibold text-gray-900 hover:text-cyan-600 transition-colors"
          >
            О нас
          </a>
          <a
            href="#"
            class="text-2xl font-semibold text-gray-900 hover:text-cyan-600 transition-colors"
          >
            Меню
          </a>
          <a
            href="#"
            class="text-2xl font-semibold text-gray-900 hover:text-cyan-600 transition-colors"
          >
            Контакты
          </a>
        </div>

        <!-- Footer (например, соцсети или копирайт) -->
        <div class="px-6 py-4 border-t text-center text-sm text-gray-500">
          © 2025 INJOO. Все права защищены.
        </div>
      </div>

      <!-- Main Content -->
      <main
        class="absolute z-10 inset-0 flex items-center justify-center px-6 text-center"
      >
        <div class="max-w-4xl mx-auto relative">
          <!-- Main Heading -->
          <div>
            <img
              class="w-[120px] h-auto absloute mx-auto"
              src="/src/assets/injoo-logo.png"
            />
          </div>
          <h1
            class="text-6xl md:text-8xl font-bold text-gray-900 mb-6 leading-tight"
          >
            Injoo Bubble Tea
          </h1>

          <!-- Subtitle -->
          <p class="text-xl md:text-2xl text-gray-800 mb-12 max-w-2xl mx-auto">
            Попробуйте лучший чай с шариками в городе!
          </p>

          <!-- Call to Action Button -->
          <button
            @click="router.push('/auth')"
            class="bg-green-200 hover:bg-green-300 text-gray-900 px-8 py-4 rounded-lg text-lg font-semibold transition-colors shadow-lg hover:shadow-xl transform hover:scale-105 transition-transform"
          >
            Заказать Сейчас
          </button>
        </div>
      </main>
    </div>
    <router-view />
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();
const mobileMenuOpen = ref(false);
const check = () => {
  console.log("1");
};
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
};
</script>

<style scoped>
/* Additional custom styles if needed */
</style>
