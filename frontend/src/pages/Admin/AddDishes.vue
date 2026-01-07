<script setup>
import { ref } from "vue";
import axios from "axios";

import Loader from "@/components/Loader.vue";
import CustomModal from "@/components/CustomModal.vue";
import { useAutoClose } from "@/stores/useAutoClose";
import VueCropper from "vue-cropperjs";

/* ================== FORM STATE ================== */
const name = ref("");
const description = ref("");
const price = ref("");
const category = ref("");
const file = ref(null);

/* ================== PREVIEW ================== */
const previewSrc = ref(null);

/* ================== LOADING & MODALS ================== */
const isLoading = ref(false);
const success = ref(false);
const fail = ref(false);

/* ================== CATEGORIES ================== */
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


/* ================== CROPPER ================== */
const cropperRef = ref(null);
const imagePreview = ref(null);
const showCropper = ref(false);

/* ================== DRAG & DROP ================== */
const fileInput = ref(null);
const isDragging = ref(false);

const onDragOver = () => (isDragging.value = true);
const onDragLeave = () => (isDragging.value = false);

const openCropper = (selectedFile) => {
  const reader = new FileReader();
  reader.onload = () => {
    imagePreview.value = reader.result;
    showCropper.value = true;
  };
  reader.readAsDataURL(selectedFile);
};

const onDrop = (e) => {
  isDragging.value = false;
  const droppedFile = e.dataTransfer.files[0];
  if (droppedFile) openCropper(droppedFile);
};

const onFileSelect = (e) => {
  const selectedFile = e.target.files[0];
  if (selectedFile) openCropper(selectedFile);
};

const triggerFileInput = () => {
  fileInput.value.click();
};

/* ================== CROP IMAGE ================== */
const cropImage = () => {
  const canvas = cropperRef.value.getCroppedCanvas({
    width: 1024,
    height: 1024,
    imageSmoothingQuality: "high",
  });

  canvas.toBlob(
    (blob) => {
      file.value = new File([blob], "dish.jpg", {
        type: "image/jpeg",
        lastModified: Date.now(),
      });
      previewSrc.value = URL.createObjectURL(file.value);
      showCropper.value = false;
      imagePreview.value = null;
    },
    "image/jpeg",
    0.8
  );
};

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

      <!-- ================== DRAG & DROP ================== -->
      <div
        @click="triggerFileInput"
        @dragover.prevent="onDragOver"
        @dragleave="onDragLeave"
        @drop.prevent="onDrop"
        class="border-2 border-dashed rounded-xl p-6 text-center cursor-pointer
               transition-all duration-200"
        :class="isDragging
          ? 'border-blue-500 bg-blue-50'
          : 'border-gray-300 hover:border-blue-400'"
      >
        <svg class="w-12 h-12 mx-auto mb-3 text-blue-500"
          fill="none" stroke="currentColor" stroke-width="1.8"
          viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M3 16l4-4a3 3 0 014 0l4 4M7 8h10a2 2 0 012 2v8a2 2 0 01-2 2H7a2 2 0 01-2-2V10a2 2 0 012-2z" />
        </svg>

        <p class="text-gray-600">
          Перетащите изображение или
          <span class="text-blue-600 font-semibold">нажмите</span>
        </p>

        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          class="hidden"
          @change="onFileSelect"
        />
      </div>

      <!-- ================== PREVIEW ================== -->
      <div v-if="previewSrc" class="relative mt-4">
        <img :src="previewSrc" class="w-full h-40 object-cover rounded-xl" />
        <button
          @click="file = null; previewSrc = null;"
          class="absolute top-2 right-2 bg-black/60 text-white rounded-full px-2"
        >
          ✕
        </button>
      </div>

      <Loader v-if="isLoading" />

      <button
        @click="submitDish"
        class="w-full bg-blue-600 text-white py-2 rounded-xl"
      >
        Добавить блюдо
      </button>
    </div>
  </div>

  <!-- ================== CROPPER MODAL ================== -->
  <CustomModal v-if="showCropper">
    <div class="bg-white p-4 rounded-xl max-w-lg w-full">
      <VueCropper
        ref="cropperRef"
        :src="imagePreview"
        :aspect-ratio="1"
        :auto-crop-area="1"
        view-mode="1"
        drag-mode="move"
        class="w-full h-80"
      />

      <div class="flex gap-2 mt-4">
        <button
          @click="cropImage"
          class="flex-1 bg-blue-600 text-white py-2 rounded-xl"
        >
          Сохранить
        </button>
        <button
          @click="showCropper = false; imagePreview = null"
          class="flex-1 bg-gray-300 py-2 rounded-xl"
        >
          Отмена
        </button>
      </div>
    </div>
  </CustomModal>

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
