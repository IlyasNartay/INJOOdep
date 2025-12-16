<script setup>
import { ref } from "vue";
import axios from "axios";
import Loader from "@/components/Loader.vue";
import CustomModal from "@/components/CustomModal.vue";
import { useAutoClose } from '@/stores/useAutoClose'

const name = ref("");
const description = ref("");
const price = ref("");
const category = ref("");
const file = ref(null);
const isLoading = ref(false);
const success = ref(false);
const fail = ref(false);
const handleFileChange = (event) => {
  file.value = event.target.files[0];
};
const categories = ref([
  { id: "all", name: "Все блюда", icon: "/all-food.svg" },
  { id: "vegetarian", name: "Вегетерианские", icon: "/vegetarian.png" },
  { id: "salads", name: "Салат", icon: "/salad.png" },
  { id: "hot_food", name: "Горячие", icon: "/hot-food.png" },
  { id: "tebyan", name: "Тебян", icon: "/tebyan.png" },
  { id: "soup", name: "Суп", icon: "/soup.png" },
  { id: "lagman", name: "Лагман", icon: "/lagman.png" },
  { id: "comyan", name: "Цомиян", icon: "/comyan.png" },
  { id: "european", name: "Европейские", icon: "/europe.png" },
  { id: "pizza", name: "Пицца", icon: "/pizza.png" },
  { id: "moti", name: "Моти", icon: "/moti.png" },
  { id: "drinks", name: "Напитки", icon: "/drinks.png" },
  { id: "chicken_wings", name: "Крылышки куриные", icon: "/chicken-wings.png" },
  { id: "pasta", name: "Паста", icon: "/pasta.png" },
  { id: "Sushi", name: "Суши", icon: "/pasta.png" },
  { id: "european", name: "европиски", icon: "/pasta.png" },
  { id: "chinese", name: "Қытайски кухния", icon: "/pasta.png" },
  { id: "fastfood", name: "фасд фуд", icon: "/pasta.png" },

])


const submitDish = async () => {
  const formData = new FormData();
  formData.append("name", name.value);
  formData.append("description", description.value);
  formData.append("price", price.value);
  formData.append("category", category.value);
  formData.append("images", file.value); // ✅ ключ как в Postman
  isLoading.value = true;

  try {
    const response = await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}menu/`,
      formData,
      {
        headers: {
          Accept: "application/json",
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${localStorage.getItem("authToken")}`,
        },
      }
    );
    success.value = true;
    setTimeout(() => {
      success.value = false;
    }, 3000);
    console.log("✅ Успех", response.data);
  } catch (error) {
    console.error("❌ Ошибка отправки:", error.response?.data || error.message);
    fail.value = true;
    setTimeout(() => {
      fail.value = false;
    }, 3000);
  } finally {
    isLoading.value = false;
  }
};
useAutoClose(success, 2000)
useAutoClose(fail, 2500)
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-900 via-purple-800 to-pink-800 animated-gradient">
    <div
      class="max-w-md w-full mx-6  bg-white shadow-xl rounded-2xl p-6 space-y-4"
    >
    <h2 class="text-2xl font-bold text-gray-800 text-center mb-4">
      Добавление блюда
    </h2>

    <!-- Название -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1"
        >Название</label
      >
      <input
        v-model="name"
        type="text"
        placeholder="Введите название"
        class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
    </div>

    <!-- Описание -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1"
        >Описание</label
      >
      <input
        v-model="description"
        type="text"
        placeholder="Введите описание"
        class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
    </div>

    <!-- Цена -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Цена</label>
      <input
        v-model="price"
        type="number"
        placeholder="Введите цену"
        class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
    </div>
    <Loader v-if="isLoading" />

    <!-- Категория -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Категория
      </label>
      <select
        v-model="category"
        class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400"
      >
        <option disabled value="">Выберите категорию</option>
        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
          {{ cat.name }}
        </option>
      </select>
    </div>

    <!-- Файл -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1"
        >Изображение блюда</label
      >
      <input
        type="file"
        @change="handleFileChange"
        class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
      />
    </div>
    <CustomModal v-if="success">
      <div
        class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center"
      >
        <img
          src="/sucsess-modal.svg"
          alt="Успешно"
          class="w-16 h-16 mx-auto mb-4"
        />
        <h3 class="text-xl font-semibold text-black mb-2">Блюдо добавлено!</h3>
        <p class="text-black mb-4">Вы успешно добавили новое блюдо.</p>
        <button
          @click="success = false"
          class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold"
        >
          Закрыть
        </button>
      </div>
    </CustomModal>
    <CustomModal v-if="fail">
      <div
        class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center"
      >
        <img
          src="/fail-modal.svg"
          alt="Успешно"
          class="w-16 h-16 mx-auto mb-4"
        />
        <h3 class="text-xl font-semibold text-black mb-2">
          Блюдо не добавлено!
        </h3>
        <p class="text-black mb-4">Повторите попытку позже</p>
        <button
          @click="fail = false"
          class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold"
        >
          Закрыть
        </button>
      </div>
    </CustomModal>
    <!-- Кнопка -->
    <div class="text-center">
      <button
        @click="submitDish"
        class="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition"
      >
        Добавить блюдо
      </button>
    </div>
  </div>
</div>
</template>
