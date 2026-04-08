<template>
  <div
    class="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-blue-900 flex items-center justify-center p-4 animated-gradient"
  >
    <div class="relative w-full max-w-sm">
      <!-- Glass background -->
      <div
        class="absolute inset-0 bg-gradient-to-br from-white/20 via-white/10 to-white/5 rounded-3xl backdrop-blur-xl border border-white/20 shadow-2xl"
      ></div>

      <div class="relative p-8 pt-12">
        <!-- Avatar -->
        <div class="flex justify-center mb-12">
          <div
            class="w-24 h-24 rounded-full bg-gradient-to-br from-pink-300/60 to-pink-400/40 flex items-center justify-center"
          >
            <div class="w-16 h-16 rounded-full bg-pink-200/60 flex items-center justify-center">
              <svg class="w-10 h-10 text-pink-100/80" fill="currentColor" viewBox="0 0 24 24">
                <path
                  d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
                />
              </svg>
            </div>
          </div>
        </div>

        <!-- PHONE -->
        <div class="mb-6">
          <div class="flex items-center space-x-3 pb-2">
            <span class="text-white">🇰🇿</span>
            <span class="text-pink-300 text-lg font-semibold">+7</span>

            <input
              v-model="displayPhone"
              type="tel"
              placeholder="706 607 05 59"
              class="flex-1 bg-transparent text-white placeholder-white/60 text-lg focus:outline-none"
              @input="errors.common = ''"
            />
          </div>
          <div class="h-px bg-gradient-to-r from-transparent via-white/40 to-transparent"></div>
        </div>

        <!-- PASSWORD -->
        <div class="mb-6">
          <div class="flex items-center space-x-3 pb-2">
            <LockIcon class="w-5 h-5 text-white/70" />

            <input
              v-model="data.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Пароль"
              class="flex-1 bg-transparent text-white placeholder-white/60 text-lg focus:outline-none"
              @input="errors.common = ''"
            />

            <button type="button" @click="showPassword = !showPassword">
              <EyeIcon v-if="!showPassword" class="w-5 h-5 text-white/70" />
              <EyeSlashIcon v-else class="w-5 h-5 text-white/70" />
            </button>
          </div>
          <div class="h-px bg-gradient-to-r from-transparent via-white/40 to-transparent"></div>

          <!-- ERROR -->
          <p v-if="errors.common" class="text-red-400 text-sm mt-2">
            {{ errors.common }}
          </p>
        </div>

        <!-- Loader -->
        <Loader v-if="isLoading" />

        <!-- REGISTER -->
        <div class="flex justify-end mb-6">
          <button
            class="text-white/60 text-sm hover:text-white"
            @click="router.push('/auth')"
          >
            Зарегистрироваться
          </button>
        </div>

        <!-- SUBMIT -->
        <button
          class="w-full py-4 rounded-2xl bg-gradient-to-r from-purple-600 via-purple-700 to-blue-600 text-white font-semibold text-lg tracking-wider shadow-lg hover:shadow-xl transition-all"
          @click="login"
        >
          ВОЙТИ
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, reactive, watch } from "vue";
import { useRouter } from "vue-router";
import Loader from "@/components/Loader.vue";
import { EyeIcon, EyeSlashIcon, LockClosedIcon as LockIcon } from "@heroicons/vue/24/solid";

const router = useRouter();
const isLoading = ref(false);
const showPassword = ref(false);

const data = reactive({
  phone: "",
  password: "",
});

const errors = reactive({
  common: "",
});

const displayPhone = ref("");

// Форматирование номера
watch(displayPhone, (val) => {
  const digits = val.replace(/\D/g, "").slice(0, 10);
  data.phone = "+7" + digits;

  const p1 = digits.slice(0, 3);
  const p2 = digits.slice(3, 6);
  const p3 = digits.slice(6, 8);
  const p4 = digits.slice(8, 10);

  displayPhone.value = [p1, p2, p3, p4].filter(Boolean).join(" ");
});

const login = async () => {
  isLoading.value = true;
  errors.common = "";

  try {
    const response = await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}auth/login`,
        { phone: data.phone, password: data.password }
    );

    const {access_token, user_role} = response.data;

    localStorage.setItem("authToken", access_token);
    localStorage.setItem("userRole", user_role);

    router.push("/CliMain");
  } catch (error) {
    const detail = error?.response?.data?.detail;

    if (detail === "Неверный номер или пароль") {
      errors.common = "Неверный номер телефона или пароль";
    } else {
      errors.common = "Ошибка входа. Попробуйте позже";
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.backdrop-blur-xl {
  backdrop-filter: blur(20px);
}
</style>
