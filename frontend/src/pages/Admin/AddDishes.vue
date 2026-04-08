<script setup>
import { ref } from "vue";
import axios from "axios";

import Loader from "@/components/Loader.vue";
import CustomModal from "@/components/CustomModal.vue";
import { useAutoClose } from "@/stores/useAutoClose";
import ImageEditor from "@/components/ImageEditor.vue";

/* ================== FORM STATE ================== */
const name = ref("");
const description = ref("");
const price = ref("");
const category = ref("");
const file = ref(null);
const previewSrc = ref(null);

/* ================== PREVIEW ================== */

/* ================== LOADING & MODALS ================== */
const isLoading = ref(false);
const success = ref(false);
const fail = ref(false);

/* ================== CATEGORIES ================== */
const categories = ref([
  { id: "all", name: "Все блюда", icon: "/all-food.svg" },
  { id: "salads", name: "Салаты", icon: "/salad.png" },
  { id: "hot_food", name: "Горячие блюда", icon: "/hot-food.png" },
  { id: "tebyan", name: "Тебян", icon: "/tebyan.png" },
  { id: "soup", name: "Супы", icon: "/soup.png" },
  { id: "lagman", name: "Лагман", icon: "/lagman.png" },
  { id: "comyan", name: "Цомиян", icon: "/comyan.png" },
  { id: "european", name: "Европейская кухня", icon: "/europe.png" },
  { id: "pizza", name: "Пицца", icon: "/pizza.png" },
  { id: "moti", name: "Моти", icon: "/moti.png" },
  { id: "drinks", name: "Напитки", icon: "/drinks.png" },
  { id: "sushi", name: "Суши", icon: "/sushi.png" },
  { id: "fastfood", name: "Фастфуд", icon: "/fastfood.png" },
  { id: "tore_tabak", name: "Төре табақтар", icon: "/tore-tabak.png" },
  { id: "grill", name: "Кәуаптар", icon: "/grill.png" },	
]);


/* ================== SUBMIT ================== */
const submitDish = async () => {
  if (!file.value) {
    alert("Добавьте изображение");
    return;
  }

  isLoading.value = true;

  try {
    const formData = new FormData();
    formData.append("name", name.value);
    formData.append("description", description.value);
    formData.append("price", price.value);
    formData.append("category", category.value);
    formData.append("images", file.value);

    await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}menu/`,
      formData,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("authToken")}`,
        },
      }
    );

    success.value = true;
  } catch (e) {
    console.error(e);
    fail.value = true;
  } finally {
    isLoading.value = false;
  }
};

useAutoClose(success, 2000);
useAutoClose(fail, 2500);
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-900 via-purple-800 to-pink-800">
    <div class="max-w-md w-full bg-white rounded-2xl p-6 shadow-xl space-y-4">

      <h2 class="text-2xl font-bold text-center">Добавление блюда</h2>

      <!-- Название -->
      <input v-model="name" placeholder="Название" class="input" />
      <!-- Описание -->
      <input v-model="description" placeholder="Описание" class="input" />
      <!-- Цена -->
      <input v-model="price" type="number" placeholder="Цена" class="input" />
      <!-- Категория -->
      <select v-model="category" class="input">
        <option disabled value="">Категория</option>
        <option v-for="c in categories" :key="c.id" :value="c.id">
          {{ c.name }}
        </option>
      </select>
      <!-- ================== IMAGE EDITOR ================== -->
      <ImageEditor
        :aspect-ratio="1"
        @update:file="file = $event"
        @update:preview="previewSrc = $event"
      />

      <Loader v-if="isLoading" />

      <button
        @click="submitDish"
        class="w-full bg-blue-600 text-white py-2 rounded-xl"
      >
        Добавить блюдо
      </button>
    </div>
  </div>
  <!-- ================== SUCCESS ================== -->
  <CustomModal v-if="success">
    <div class="bg-white p-6 rounded-xl text-center">
      <h3 class="text-xl font-semibold">Блюдо добавлено ✅</h3>
    </div>
  </CustomModal>

  <!-- ================== FAIL ================== -->
  <CustomModal v-if="fail">
    <div class="bg-white p-6 rounded-xl text-center">
      <h3 class="text-xl font-semibold text-red-600">Ошибка ❌</h3>
    </div>
  </CustomModal>
</template>

<style scoped>
.input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 12px;
  margin-bottom: 0.5rem;
}
</style>
