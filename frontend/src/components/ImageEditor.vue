<script setup>
import { ref } from "vue";
import VueCropper from "vue-cropperjs";

const props = defineProps({
  currentImageUrl: { type: String, default: null },
  aspectRatio: { type: Number, default: 1 },
  maxSizeMB: { type: Number, default: 5 },
  maxWidth: { type: Number, default: 1920 },
});

const emit = defineEmits(["update:file", "update:preview"]);

const isDragging = ref(false);
const showCropper = ref(false);
const imageForCropper = ref(null);
const previewUrl = ref(null);
const fileInput = ref(null);
const cropperRef = ref(null);

const compressImage = (file) => {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = (e) => {
      const img = new Image();
      img.src = e.target.result;
      img.onload = () => {
        const canvas = document.createElement("canvas");
        let width = img.width;
        let height = img.height;
        if (width > props.maxWidth) {
          height = Math.round((height * props.maxWidth) / width);
          width = props.maxWidth;
        }
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, width, height);
        let quality = 0.9;
        const compress = () => {
          canvas.toBlob(
            (blob) => {
              if (blob.size > props.maxSizeMB * 1024 * 1024 && quality > 0.1) {
                quality -= 0.1;
                compress();
              } else {
                resolve(new File([blob], file.name || "image.jpg", {
                  type: "image/jpeg",
                  lastModified: Date.now(),
                }));
              }
            },
            "image/jpeg",
            quality
          );
        };
        compress();
      };
    };
  });
};

const openCropper = async (selectedFile) => {
  let fileToRead = selectedFile;
  if (selectedFile.size > props.maxSizeMB * 1024 * 1024) {
    fileToRead = await compressImage(selectedFile);
  }
  const reader = new FileReader();
  reader.onload = () => {
    imageForCropper.value = reader.result;
    showCropper.value = true;
  };
  reader.readAsDataURL(fileToRead);
};

const cropImage = () => {
  const canvas = cropperRef.value.getCroppedCanvas({
    width: 1024,
    height: 1024,
    imageSmoothingQuality: "high",
  });
  canvas.toBlob(
    (blob) => {
      const finalFile = new File([blob], "dish.jpg", {
        type: "image/jpeg",
        lastModified: Date.now(),
      });
      const url = URL.createObjectURL(finalFile);
      previewUrl.value = url;
      emit("update:file", finalFile);
      emit("update:preview", url);
      showCropper.value = false;
      imageForCropper.value = null;
    },
    "image/jpeg",
    0.85
  );
};

const cancelCrop = () => {
  showCropper.value = false;
  imageForCropper.value = null;
};

const reset = () => {
  previewUrl.value = null;
  emit("update:file", null);
  emit("update:preview", null);
};

const onFileSelect = (e) => {
  const f = e.target.files[0];
  if (f) openCropper(f);
  e.target.value = "";
};

const onDrop = (e) => {
  isDragging.value = false;
  const f = e.dataTransfer.files[0];
  if (f && f.type.startsWith("image/")) openCropper(f);
};

const onDragOver = () => { isDragging.value = true; };
const onDragLeave = () => { isDragging.value = false; };

const onPaste = (e) => {
  const items = e.clipboardData?.items;
  if (!items) return;
  for (const item of items) {
    if (item.type.startsWith("image/")) {
      openCropper(item.getAsFile());
      break;
    }
  }
};

const triggerFileInput = () => fileInput.value?.click();
</script>

<template>
  <div
    @click="triggerFileInput"
    @dragover.prevent="onDragOver"
    @dragleave="onDragLeave"
    @drop.prevent="onDrop"
    @paste="onPaste"
    tabindex="0"
    @keydown.enter="triggerFileInput"
    class="relative w-full rounded-xl border-2 border-dashed transition-all duration-200 cursor-pointer overflow-hidden focus:outline-none focus:ring-2 focus:ring-purple-400"
    :class="isDragging ? 'border-purple-400 bg-purple-50/10 scale-[1.01]' : 'border-gray-500 hover:border-purple-400 hover:bg-white/5'"
    style="min-height: 180px;"
  >
    <img v-if="previewUrl" :src="previewUrl" class="absolute inset-0 w-full h-full object-cover" />
    <img v-else-if="currentImageUrl" :src="currentImageUrl" class="absolute inset-0 w-full h-full object-cover opacity-50" />

    <div
      class="relative z-10 flex flex-col items-center justify-center gap-2 py-10 px-4 text-center pointer-events-none select-none"
      :class="previewUrl || currentImageUrl ? 'opacity-0 hover:opacity-100 transition-opacity' : ''"
    >
      <svg class="w-10 h-10 text-purple-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909M3 20.25h18M3.75 3h16.5A.75.75 0 0121 3.75v12a.75.75 0 01-.75.75H3.75A.75.75 0 013 16.5V3.75A.75.75 0 013.75 3z" />
      </svg>
      <p class="text-sm text-gray-300 leading-relaxed">
        Перетащи фото сюда, вставь
        <kbd class="bg-white/20 text-white text-xs px-1.5 py-0.5 rounded font-mono">Ctrl+V</kbd>
        <br />или нажми для выбора файла
      </p>
    </div>

    <div v-if="previewUrl" class="absolute top-2 left-2 z-20 bg-green-500 text-white text-xs px-2 py-1 rounded-full font-semibold shadow">
      ✓ Новое фото
    </div>
    <button v-if="previewUrl" @click.stop="reset" class="absolute top-2 right-2 z-20 bg-red-500 hover:bg-red-600 text-white text-xs px-2 py-1 rounded-lg shadow transition">
      Отменить
    </button>

    <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileSelect" />
  </div>

  <Teleport to="body">
    <div v-if="showCropper" class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 backdrop-blur-sm" @click.self="cancelCrop">
      <div class="bg-gray-900 border border-white/10 rounded-2xl p-4 w-[90vw] max-w-lg shadow-2xl">
        <h3 class="text-white font-semibold mb-3 text-center">Обрежь фото</h3>
        <VueCropper ref="cropperRef" :src="imageForCropper" :aspect-ratio="aspectRatio" :auto-crop-area="0.9" view-mode="1" drag-mode="move" class="w-full rounded-xl overflow-hidden" style="height: 320px;" />
        <div class="flex gap-3 mt-4">
          <button @click="cropImage" class="flex-1 bg-purple-600 hover:bg-purple-700 text-white py-2.5 rounded-xl font-semibold transition">✂️ Сохранить кадр</button>
          <button @click="cancelCrop" class="flex-1 bg-gray-700 hover:bg-gray-600 text-white py-2.5 rounded-xl transition">Отмена</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
