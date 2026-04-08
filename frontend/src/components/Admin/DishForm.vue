<script setup>
import { ref, watch } from "vue";
import VueCropper from "vue-cropperjs";
import 'cropperjs/dist/cropper.css';
import { PRODUCT_CATEGORIES } from "@/constants/categories";

const props = defineProps({
  initialData: { type: Object, default: () => ({ name: '', description: '', price: '', category: '' }) },
  submitText: { type: String, default: 'Сохранить' }
});

const emit = defineEmits(['submit', 'cancel']);

// Состояние полей
const form = ref({ ...props.initialData });
const file = ref(null);
const previewSrc = ref(null);
const isDragging = ref(false);

// Cropper logic
const cropperRef = ref(null);
const imagePreview = ref(null);
const showCropper = ref(false);

const openCropper = (selectedFile) => {
  const reader = new FileReader();
  reader.onload = () => { imagePreview.value = reader.result; showCropper.value = true; };
  reader.readAsDataURL(selectedFile);
};

const onFileSelect = (e) => { if (e.target.files[0]) openCropper(e.target.files[0]); };
const onDrop = (e) => { isDragging.value = false; if (e.dataTransfer.files[0]) openCropper(e.dataTransfer.files[0]); };

const cropImage = () => {
  const canvas = cropperRef.value.getCroppedCanvas({ width: 1024, height: 1024 });
  canvas.toBlob((blob) => {
    file.value = new File([blob], "dish.jpg", { type: "image/jpeg" });
    previewSrc.value = URL.createObjectURL(file.value);
    showCropper.value = false;
  }, "image/jpeg", 0.8);
};

const handleSubmit = () => {
  const formData = new FormData();
  formData.append("name", form.value.name);
  formData.append("description", form.value.description);
  formData.append("price", form.value.price);
  formData.append("category", form.value.category);
  if (file.value) formData.append("images", file.value);
  emit('submit', formData);
};
</script>

<template>
  <div class="space-y-4 text-left">
    <input v-model="form.name" placeholder="Название" class="w-full p-2 border rounded-xl" />
    <textarea v-model="form.description" placeholder="Описание" class="w-full p-2 border rounded-xl" />
    <input v-model="form.price" type="number" placeholder="Цена" class="w-full p-2 border rounded-xl" />
    
    <select v-model="form.category" class="w-full p-2 border rounded-xl">
      <option disabled value="">Выберите категорию</option>
      <option v-for="c in PRODUCT_CATEGORIES" :key="c.id" :value="c.id">{{ c.name }}</option>
    </select>

    <div 
      @drop.prevent="onDrop" @dragover.prevent="isDragging = true" @dragleave="isDragging = false"
      class="border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all"
      :class="isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'"
      @click="$refs.fileInput.click()"
    >
      <p v-if="!previewSrc" class="text-gray-500 text-sm">Перетащите фото или нажмите для выбора</p>
      <img v-else :src="previewSrc" class="h-32 mx-auto object-cover rounded-lg" />
      <input ref="fileInput" type="file" class="hidden" @change="onFileSelect" accept="image/*" />
    </div>

    <button @click="handleSubmit" class="w-full bg-blue-600 text-white py-2 rounded-xl font-bold">
      {{ submitText }}
    </button>

    <div v-if="showCropper" class="fixed inset-0 z-[60] bg-black/80 flex items-center justify-center p-4">
      <div class="bg-white p-4 rounded-xl max-w-lg w-full">
        <VueCropper ref="cropperRef" :src="imagePreview" :aspect-ratio="1" view-mode="1" class="h-80" />
        <div class="flex gap-2 mt-4">
          <button @click="cropImage" class="flex-1 bg-blue-600 text-white py-2 rounded-lg">Обрезать</button>
          <button @click="showCropper = false" class="flex-1 bg-gray-200 py-2 rounded-lg">Отмена</button>
        </div>
      </div>
    </div>
  </div>
</template>

