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
        </div>

        <!-- Full Name Input -->
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
          <div class="h-px bg-gradient-to-r from-transparent via-white/40 to-transparent"></div>
        </div>

        <!-- Phone Input -->
        <div class="mb-6">
          <div class="flex items-center space-x-3 pb-2">
            <!-- Flag -->
            <span class="w-6 h-6 flex items-center justify-center text-white text-sm">
              🇰🇿
            </span>

            <!-- Prefix +7 -->
            <span class="text-pink-300 text-lg font-semibold">+7</span>

            <!-- Phone Field -->
            <input
              v-model="displayPhone"
              type="tel"
              placeholder="706 607 05 59"
              class="flex-1 bg-transparent text-white placeholder-white/60 text-lg focus:outline-none"
            />
          </div>
          <div class="h-px bg-gradient-to-r from-transparent via-white/40 to-transparent"></div>
        </div>

        <!-- Password Input -->
        <div class="mb-6">
          <div class="flex items-center space-x-3 pb-2">
            <LockClosedIcon class="w-5 h-5 text-white/70" />
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
              <EyeSlashIcon v-else class="w-5 h-5" />
            </button>
          </div>
          <div class="h-px bg-gradient-to-r from-transparent via-white/40 to-transparent"></div>
        </div>

        <!-- Terms Checkbox -->
       <div class="mb-8">
  <label class="flex items-center space-x-3 cursor-pointer">
    <div
      class="w-5 h-5 border-2 border-white/70 rounded-md flex items-center justify-center bg-transparent"
      :class="{'bg-white/80': termsAccepted}"
    >
      <!-- Галочка -->
      <svg
        v-if="termsAccepted"
        xmlns="http://www.w3.org/2000/svg"
        class="w-3 h-3 text-blue-700"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fill-rule="evenodd"
          d="M16.707 5.293a1 1 0 00-1.414 0L8 12.586 4.707 9.293a1 1 0 00-1.414 1.414l4 4a1 1 0 001.414 0l8-8a1 1 0 000-1.414z"
          clip-rule="evenodd"
        />
      </svg>
    </div>
    <span class="text-white/80 select-none text-sm">Я принимаю условия использования</span>
    <input
      type="checkbox"
      v-model="termsAccepted"
      class="absolute opacity-0 w-0 h-0"
    />
  </label>
</div>


        <!-- Loader -->
        <Loader v-if="isLoading" />

        <!-- Fail Modal -->
        <CustomModal v-if="failModal">
          <div
            class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center"
          >
            <img src="/fail-modal.svg" alt="Ошибка" class="w-16 h-16 mx-auto mb-4" />
            <h3 class="text-xl font-semibold text-black mb-2">
              Регистрация не удалась!
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

        <!-- Register Button -->
        <button
          type="submit"
          class="w-full py-4 rounded-2xl font-semibold text-lg tracking-wider shadow-lg transition-all duration-300 bg-gradient-to-r from-purple-600 via-purple-700 to-blue-600 text-white hover:shadow-xl hover:scale-[1.02] active:scale-[0.98]"
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
import { reactive, ref, watch } from "vue";
import Loader from "@/components/Loader.vue";
import CustomModal from "@/components/CustomModal.vue";
import { useRouter } from "vue-router";
import {
  UserPlusIcon,
  UserIcon,
  LockClosedIcon,
  EyeIcon,
  EyeSlashIcon,
} from "@heroicons/vue/24/solid";

const router = useRouter();
const failModal = ref(false);
const isLoading = ref(false);
const showPassword = ref(false);
const termsAccepted = ref(false);

const data = reactive({
  full_name: "",
  phone: "",
  password: "",
});

const displayPhone = ref(""); // визуальное отображение с пробелами

watch(displayPhone, (val) => {
  // оставляем только цифры
  const digits = val.replace(/\D/g, "");
  const sliced = digits.slice(0, 10); // 10 цифр после +7
  data.phone = "+7" + sliced; // слитно для сервера

  // форматируем красиво для отображения
  const part1 = sliced.slice(0, 3);
  const part2 = sliced.slice(3, 6);
  const part3 = sliced.slice(6, 8);
  const part4 = sliced.slice(8, 10);
  displayPhone.value = [part1, part2, part3, part4].filter(Boolean).join(" ");
});

// Toggle password visibility
const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

// Toggle terms checkbox
const toggleTermsAccepted = () => {
  termsAccepted.value = !termsAccepted.value;
};

// Registration function
const regis = async () => {
  if (!termsAccepted.value) {
    alert("Пожалуйста, примите условия использования");
    return;
  }

  isLoading.value = true;
  try {
    const response = await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}auth/register`,
      data
    );

    if (response.status === 200) {
      router.push("/login");
    }
    return response.data;
  } catch (error) {
    console.error("Ошибка при регистрации:", error.detail);
    failModal.value = true;
    setTimeout(() => {
      failModal.value = false;
    }, 3000);
  } finally {
    isLoading.value = false;
  }
};
</script>
