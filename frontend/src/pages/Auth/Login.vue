<template>
  <div
    class="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-blue-900 flex items-center justify-center p-4 animated-gradient"
  >
    <div class="relative w-full max-w-sm">
      <div
        class="absolute inset-0 bg-gradient-to-br from-white/20 via-white/10 to-white/5 rounded-3xl backdrop-blur-xl border border-white/20 shadow-2xl"
      ></div>

      <div class="relative p-8 pt-12">
        <div class="flex justify-center mb-12">
          <div
            class="w-24 h-24 rounded-full bg-gradient-to-br from-pink-300/60 to-pink-400/40 flex items-center justify-center backdrop-blur-sm"
          >
            <div
              class="w-16 h-16 rounded-full bg-pink-200/60 flex items-center justify-center"
            >
              <svg
                class="w-10 h-10 text-pink-100/80"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
                />
              </svg>
            </div>
          </div>
        </div>

       <div class="mb-8">
  <div class="flex items-center space-x-3 pb-2">
    <!-- Флаг -->
    <span class="w-6 h-6 flex items-center justify-center text-white text-sm">
      🇰🇿
    </span>

    <!-- Префикс +7 с другим цветом -->
    <span class="text-pink-300 text-lg font-semibold">+7</span>

    <!-- Поле телефона -->
    <input
      v-model="displayPhone"
      type="tel"
      placeholder="706 607 05 59"
      class="flex-1 bg-transparent text-white placeholder-white/60 text-lg focus:outline-none"
    />
  </div>
  <div class="h-px bg-gradient-to-r from-transparent via-white/40 to-transparent"></div>
</div>


        <div class="mb-8">
          <div class="flex items-center space-x-3 pb-2">
            <LockIcon class="w-5 h-5 text-white/70" />
            <input
              v-model="data.password"
              type="password"
              placeholder="Пароль"
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
              Вход не удался!
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
        <div class="flex items-center justify-between mb-8">
          <label
            class="flex items-center space-x-2 cursor-pointer"
            @click="toggleRememberMe"
          >
          </label>

          <button
            type="button"
            class="text-white/60 text-sm italic hover:text-white/80 transition-colors"
            @click="router.push('/auth')"
          >
            Зарегистрироваться
          </button>
        </div>

        <button
          type="submit"
          class="w-full py-4 rounded-2xl bg-gradient-to-r from-purple-600 via-purple-700 to-blue-600 text-white font-semibold text-lg tracking-wider shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] active:scale-[0.98]"
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
import { useRouter } from "vue-router";
import { ref, reactive, watch } from "vue";
import Loader from "@/components/Loader.vue";
import CustomModal from "@/components/CustomModal.vue";

const router = useRouter();
const isLoading = ref(false);
const failModal = ref(false);

const data = reactive({
  phone: "", // для отправки на сервер
  password: "",
});

const displayPhone = ref(""); // для отображения в input

// Форматирование: 7066070559 → 706 607 05 59
watch(displayPhone, (val) => {
  // Убираем все кроме цифр
  const digits = val.replace(/\D/g, "");

  // Ограничиваем до 9 цифр (без +7)
  const sliced = digits.slice(0, 10);
  data.phone = "%2B7" + sliced; // слитно для сервера

  // Форматируем красиво для отображения
  const part1 = sliced.slice(0, 3);
  const part2 = sliced.slice(3, 6);
  const part3 = sliced.slice(6, 8);
  const part4 = sliced.slice(8, 10); // последняя цифра
  displayPhone.value = [part1, part2, part3, part4].filter(Boolean).join(" ");
});


const login = async () => {
  isLoading.value = true;
  try {
    const response = await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}auth/login?phone=${data.phone}&password=${data.password}`
    );
    const token = response.data.access_token;
    const user_role = response.data.user_role;
    if (token) {
      localStorage.setItem("authToken", token);
      localStorage.setItem("userRole", user_role);
    }
    if (user_role === "customer") {
      router.push("/CliMain");
    } else if (user_role === "admin") {
      router.push("/CliMain");
    } else {
      console.log("no route");
    }
    return response.data;
  } catch (error) {
    failModal.value = true;
    setTimeout(() => {
      failModal.value = false;
    }, 3000);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Additional custom styles if needed */
.backdrop-blur-xl {
  backdrop-filter: blur(20px);
}

/* Custom focus styles for inputs */
input:focus {
  outline: none;
}

/* Smooth transitions for all interactive elements */
* {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Custom gradient animations */
@keyframes gradient-shift {
  0%,
  100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.bg-gradient-to-r {
  background-size: 200% 200%;
  animation: gradient-shift 3s ease infinite;
}
</style>
