<template>

  <div
    class="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-blue-900 flex items-center justify-center p-4 animated-gradient"
  >
    <!-- Glassmorphism Card -->
    <div class="relative w-full max-w-md">
      <div
        class="absolute inset-0 bg-gradient-to-br from-white/20 via-white/10 to-white/5 rounded-3xl backdrop-blur-xl border border-white/20 shadow-2xl"
      ></div>

      <div class="relative p-8 pt-10">
        <!-- User Avatar -->
        <div class="flex justify-center mb-8">
          <div
            class="w-20 h-20 rounded-full bg-gradient-to-br from-pink-300/60 to-pink-400/40 flex items-center justify-center backdrop-blur-sm"
          >
            <div
              class="w-14 h-14 rounded-full bg-pink-200/60 flex items-center justify-center"
            >
              <UserPlusIcon class="w-8 h-8 text-pink-100/80" />
            </div>
          </div>
        </div>

        <!-- Title -->
        <div class="text-center mb-8">
          <h2 class="text-2xl font-semibold text-white/90 mb-2">
            Создать аккаунт
          </h2>
          <!-- <p class="text-white/60 text-sm">Join us today and get started</p> -->
        </div>

        <!-- First Name Input -->
        <div class="mb-6">
          <div class="flex items-center space-x-3 pb-2">
            <UserIcon class="w-5 h-5 text-white/70" />
            <input
              v-model="data.full_name"
              type="text"
              placeholder="Имя"
              class="flex-1 bg-transparent text-white placeholder-white/60 text-lg focus:outline-none"
            />
          </div>
          <div
            class="h-px bg-gradient-to-r from-transparent via-white/40 to-transparent"
          ></div>
        </div>
      <Loader v-if="isLoading" />
<CustomModal v-if="failModal">
<div
        class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center"
      >
        <img
          src="/fail-modal.svg"
          alt="Успешно"
          class="w-16 h-16 mx-auto mb-4"
        />
        <h3 class="text-xl font-semibold text-black mb-2">
          Регестрация не удалась!
        </h3>
        <p class="text-black mb-4">Повторите попытку позже</p>
        <button
          @click="failModal = false"
          class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold"
        >
          Закрыть
        </button>
      </div>
</CustomModal>
        <!-- Last Name Input -->
        <div class="mb-6">
          <div class="flex items-center space-x-3 pb-2">
            <UserIcon class="w-5 h-5 text-white/70" />
            <input
              v-model="data.phone"
              type="text"
              placeholder="Номер Телефона"
              class="flex-1 bg-transparent text-white placeholder-white/60 text-lg focus:outline-none"
            />
          </div>
          <div
            class="h-px bg-gradient-to-r from-transparent via-white/40 to-transparent"
          ></div>
        </div>

        <div class="mb-6">
          <div class="flex items-center space-x-3 pb-2">
            <LockIcon class="w-5 h-5 text-white/70" />
            <input
              v-model="data.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Пароль"
              class="flex-1 bg-transparent text-white placeholder-white/60 text-lg focus:outline-none"
            />
            <button
              type="button"
              @click="togglePasswordVisibility"
              class="text-white/60 hover:text-white/80 transition-colors"
            >
              <EyeIcon v-if="!showPassword" class="w-5 h-5" />
              <EyeOffIcon v-else class="w-5 h-5" />
            </button>
          </div>
          <div
            class="h-px bg-gradient-to-r from-transparent via-white/40 to-transparent"
          ></div>
        </div>
        <div class="mb-8">
          <label
            class="flex items-start space-x-3 cursor-pointer"
            @click="toggleTermsAccepted"
          >
            <div class="relative mt-0.5">
              <input v-model="termsAccepted" type="checkbox" class="sr-only" />
            </div>
          </label>
        </div>

        <!-- Register Button -->
        <button
          type="submit"
          :class="[
            'w-full py-4 rounded-2xl font-semibold text-lg tracking-wider shadow-lg transition-all duration-300 bg-gradient-to-r from-purple-600 via-purple-700 to-blue-600 text-white hover:shadow-xl hover:scale-[1.02] active:scale-[0.98]',
          ]"
          @click="regis"
        >
          СОЗДАТЬ АККАУНТ
        </button>

        <!-- Login Link -->
        <div class="text-center mt-6">
          <p class="text-white/60 text-sm">
            <button
              type="button"
              class="text-pink-300 hover:text-pink-200 font-medium transition-colors ml-1"
              @click="router.push('/login')"
            >
              Уже есть аккаунт? Войти
            </button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { computed, reactive, ref } from "vue";
import Loader from "@/components/Loader.vue";
import { useRouter } from "vue-router";

const router = useRouter();
const failModal = ref(false)
const isLoading = ref(false);
const data = reactive({
  full_name: "",
  phone: "",
  password: "",
});
// const isFormValid = computed(() => {
//   return data.full_name.trim() !== '' &&
//          data.email.trim() !== '' &&
//          data.password.length >= 4 &&

// })
// const register = () => {
//   if (!name.value || !email.value || !password.value) {
//     alert('Пожалуйста, заполните все поля')
//     return
//   }

//   // Здесь логика регистрации
//   alert(`Регистрация выполнена: ${name.value} (${email.value})`)
// }

const regis = async () => {
  const details = { ...data };
  isLoading.value = true;

  try {
    const response = await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}auth/register`,
      details
    );

    // Проверка статуса ответа
    if (response.status === 200) {
      router.push("/login");
    }

    return response.data;
  } catch (error) {
    console.error("Ошибка при регистрации:", error);
    failModal.value = true
    setTimeout(() => {
      failModal.value = false;
    }, 3000);
  } finally {
    isLoading.value = false;
  }
};
</script>
