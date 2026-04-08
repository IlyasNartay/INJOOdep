<script setup>
import { computed, onMounted, ref, watch } from "vue";
import axios from "axios";
import {
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  ShoppingCart as ShoppingCartIcon,
  Minus as MinusIcon,
  Pen as PenIcon,
  PlusIcon as PlusIcon,
} from "lucide-vue-next";
import Loader from "./Loader.vue";
import { useCartStore } from "@/stores/Basket.js";
import { useRouter } from "vue-router";
import CustomModal from "./CustomModal.vue";
import ImageEditor from "@/components/ImageEditor.vue";
import { useAutoClose } from "@/stores/useAutoClose";
import { currentSessionMode, currentUserRole, SESSION_MODES, USER_ROLES } from "@/utils/roles";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
const imageUrl = apiBaseUrl;
const cart = useCartStore();
const router = useRouter();

const isLoading = ref(false);
const menu = ref([]);
const filterName = ref("all");
const scrollContainer = ref(null);
const cartIcon = ref(null);

const editingDish = ref(null);
const showEditModal = ref(false);
const successEdit = ref(false);
const successDelete = ref(false);
const fail = ref(false);
const file = ref(null);
const previewUrl = ref(null);

const role = computed(() => {
  if (currentSessionMode.value === SESSION_MODES.GUEST) {
    return "guest";
  }

  return currentUserRole.value || USER_ROLES.CUSTOMER;
});

const categories = ref([
  { id: "all", name: "Все блюда", icon: "/all-food.svg" },
  { id: "salads", name: "Салаты", icon: "/salad.png" },
  { id: "hot_food", name: "Горячее", icon: "/hot-food.png" },
  { id: "soup", name: "Супы", icon: "/soup.png" },
  { id: "lagman", name: "Лагман", icon: "/lagman.png" },
  { id: "comyan", name: "Цомян", icon: "/comyan.svg" },
  { id: "european", name: "Европейские", icon: "/beef.png" },
  { id: "pizza", name: "Пицца", icon: "/pizza.svg" },
  { id: "moti", name: "Моти", icon: "/moti.png" },
  { id: "sushi", name: "Суши", icon: "/sushi.png" },
  { id: "fastfood", name: "Фастфуд", icon: "/fries.png" },
  { id: "tore_tabak", name: "Торе табак", icon: "/tore-tabak.png" },
  { id: "grill", name: "Гриль", icon: "/grill.png" },
]);

const normalizedCategory = (value) => (value || "").trim().toLowerCase();

const filteredMenu = computed(() => {
  if (filterName.value === "all") {
    return menu.value;
  }

  return menu.value.filter((item) => normalizedCategory(item.category) === normalizedCategory(filterName.value));
});

const filterLabel = computed(() => {
  const category = categories.value.find((item) => item.id === filterName.value);
  return category ? category.name : "Все";
});

const totalCount = computed(() =>
  cart.items.reduce((sum, item) => sum + (item.quantity || 1), 0)
);

const isCustomerMode = computed(() => role.value === USER_ROLES.CUSTOMER || role.value === "guest");
const isAdminMode = computed(() => role.value === USER_ROLES.ADMIN);

function selectCategory(category) {
  filterName.value = category.id;
}

function scrollLeft() {
  const scrollAmount = window.innerWidth < 640 ? 240 : window.innerWidth < 1024 ? 260 : 280;
  scrollContainer.value?.scrollBy({ left: -scrollAmount, behavior: "smooth" });
}

function scrollRight() {
  const scrollAmount = window.innerWidth < 640 ? 240 : window.innerWidth < 1024 ? 260 : 280;
  scrollContainer.value?.scrollBy({ left: scrollAmount, behavior: "smooth" });
}

async function getMenu() {
  isLoading.value = true;
  try {
    const response = await axios.get(`${apiBaseUrl}menu/`);
    menu.value = Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error("Ошибка при получении меню:", error);
    fail.value = true;
  } finally {
    isLoading.value = false;
  }
}

async function deleteDish(id) {
  isLoading.value = true;
  try {
    const response = await axios.delete(`${apiBaseUrl}menu/${id}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
      },
    });

    if (response.status === 200) {
      menu.value = menu.value.filter((item) => item.id !== id);
      successDelete.value = true;
    }
  } catch (error) {
    console.error("Ошибка при удалении блюда:", error);
    fail.value = true;
  } finally {
    isLoading.value = false;
  }
}

async function toggleAvailability(dish) {
  if (!dish) return;

  const newStatus = !dish.available;
  const params = new URLSearchParams();
  params.append("available", String(newStatus));

  try {
    const response = await axios.patch(`${apiBaseUrl}menu/${dish.id}/availability`, params, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
        Accept: "application/json",
      },
    });

    if (response.status === 200 || response.status === 204) {
      dish.available = newStatus;
    }
  } catch (error) {
    console.error("Ошибка при обновлении доступности:", error.response?.data || error.message);
    fail.value = true;
  }
}

function openEditModal(dish) {
  editingDish.value = { ...dish };
  previewUrl.value = null;
  file.value = null;
  showEditModal.value = true;
}

function closeEditModal() {
  showEditModal.value = false;
  previewUrl.value = null;
  file.value = null;
}

async function saveEdit() {
  if (!editingDish.value) return;

  const formData = new FormData();
  formData.append("name", editingDish.value.name);
  formData.append("description", editingDish.value.description || "");
  formData.append("price", editingDish.value.price);
  formData.append("category", editingDish.value.category || "");

  if (file.value) {
    formData.append("images", file.value);
  }

  isLoading.value = true;

  try {
    await axios.put(`${apiBaseUrl}menu/${editingDish.value.id}`, formData, {
      headers: {
        Accept: "application/json",
        "Content-Type": "multipart/form-data",
        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
      },
    });

    const index = menu.value.findIndex((item) => item.id === editingDish.value.id);
    if (index !== -1) {
      const currentImages = menu.value[index].images || [];
      menu.value[index] = {
        ...menu.value[index],
        ...editingDish.value,
        images: currentImages,
      };
    }

    closeEditModal();
    successEdit.value = true;
  } catch (error) {
    console.error("Ошибка при обновлении блюда:", error.response?.data || error.message);
    fail.value = true;
  } finally {
    isLoading.value = false;
  }
}

function animateToCart(event) {
  const cartEl = cartIcon.value;
  if (!cartEl) return;

  const startX = event.clientX;
  const startY = event.clientY;
  const cartRect = cartEl.getBoundingClientRect();
  const endX = cartRect.left + cartRect.width / 2;
  const endY = cartRect.top + cartRect.height / 2;

  const fly = document.createElement("div");
  fly.style.position = "fixed";
  fly.style.left = `${startX}px`;
  fly.style.top = `${startY}px`;
  fly.style.width = "30px";
  fly.style.height = "30px";
  fly.style.borderRadius = "50%";
  fly.style.background = "#4ade80";
  fly.style.zIndex = "9999";
  fly.style.transition = "all 0.7s cubic-bezier(0.4, 0, 0.2, 1)";
  document.body.appendChild(fly);

  setTimeout(() => {
    fly.style.left = `${endX}px`;
    fly.style.top = `${endY}px`;
    fly.style.transform = "scale(0.3)";
    fly.style.opacity = "0";
  }, 10);

  setTimeout(() => {
    fly.remove();
  }, 800);
}

function handleAddToCart(event, dish) {
  animateToCart(event);
  cart.toggleItem(dish);
}

function isInCart(id) {
  return cart.isInCart(id);
}

useAutoClose(successEdit, 2000);
useAutoClose(fail, 2500);
useAutoClose(successDelete, 3000);

watch([currentUserRole, currentSessionMode], () => {
  getMenu();
}, { immediate: true });

onMounted(() => {
  getMenu();
});
</script>

<template>
  <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-8 py-4 sm:py-6 lg:py-8">
    <Loader v-if="isLoading" />

    <div class="mb-6 sm:mb-8">
      <div class="flex gap-6 sm:gap-8 overflow-y-hidden overflow-x-scroll">
        <div
          v-for="category in categories"
          :key="category.id"
          class="flex flex-col items-center space-y-1 sm:space-y-2 cursor-pointer group"
          @click="selectCategory(category)"
        >
          <div
            class="w-12 h-12 sm:w-14 sm:h-14 lg:w-16 lg:h-16 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl sm:rounded-2xl flex items-center justify-center group-hover:scale-105 transition-transform"
          >
            <img :src="category.icon" :alt="category.name" class="w-6 h-6 sm:w-7 sm:h-7 lg:w-8 lg:h-8 object-contain" />
          </div>
          <span class="text-[10px] sm:text-xs text-white text-center leading-tight">
            {{ category.name }}
          </span>
        </div>
      </div>
    </div>

    <section>
      <div class="flex items-center justify-between mb-4 sm:mb-6">
        <h2 class="text-lg sm:text-xl lg:text-2xl font-bold text-white">
          Выбранная категория: {{ filterLabel }}
        </h2>
        <div class="flex items-center space-x-1 sm:space-x-2">
          <button
            type="button"
            @click="scrollLeft"
            class="text-white hover:text-cyan-400 p-1 sm:p-2 rounded transition-colors"
          >
            <ChevronLeftIcon class="w-4 h-4" />
          </button>
          <button
            type="button"
            @click="scrollRight"
            class="text-white hover:text-cyan-400 p-1 sm:p-2 rounded transition-colors"
          >
            <ChevronRightIcon class="w-4 h-4" />
          </button>
        </div>
      </div>

      <div
        v-if="!filteredMenu.length && !isLoading"
        class="rounded-2xl border border-dashed border-white/20 bg-white/5 px-6 py-10 text-center text-white/70"
      >
        Блюда не найдены
      </div>

      <div
        v-else
        ref="scrollContainer"
        class="flex flex-wrap gap-3 sm:gap-4 lg:gap-6 overflow-x-auto scroll-smooth pb-2"
      >
        <div
          v-for="restaurant in filteredMenu"
          :key="restaurant.id"
          class="w-[280px] max-[650px]:w-[210px] max-[450px]:w-[170px] max-[400px]:w-[160px] max-[350px]:w-[140px] bg-gray-800/50 border border-gray-700 mx-auto rounded-lg overflow-hidden hover:bg-gray-800/70 transition-colors cursor-pointer flex-shrink-0"
        >
          <div class="relative">
            <CustomModal v-if="successEdit">
              <div class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center">
                <img src="/sucsess-modal.svg" alt="Успешно" class="w-16 h-16 mx-auto mb-4" />
                <h3 class="text-xl font-semibold text-black mb-2">Вы успешно изменили блюдо!</h3>
                <button @click="successEdit = false" class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold">Закрыть</button>
              </div>
            </CustomModal>

            <CustomModal v-if="fail">
              <div class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center">
                <img src="/fail-modal.svg" alt="Ошибка" class="w-16 h-16 mx-auto mb-4" />
                <h3 class="text-xl font-semibold text-black mb-2">Что-то пошло не так!</h3>
                <button @click="fail = false" class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold">Закрыть</button>
              </div>
            </CustomModal>

            <CustomModal v-if="successDelete">
              <div class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center">
                <img src="/sucsess-modal.svg" alt="Успешно" class="w-16 h-16 mx-auto mb-4" />
                <h3 class="text-xl font-semibold text-black mb-2">Вы успешно удалили блюдо!</h3>
                <button @click="successDelete = false" class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold">Закрыть</button>
              </div>
            </CustomModal>

            <div class="relative w-full aspect-[4/3] overflow-hidden rounded-xl">
              <img
                v-if="restaurant.images?.length"
                :src="imageUrl + restaurant.images[0].image_url"
                :alt="restaurant.name"
                class="w-full h-full object-cover object-center transition-transform duration-500"
                :class="isAdminMode ? 'cursor-pointer hover:brightness-75' : ''"
                @click.stop="isAdminMode && openEditModal(restaurant)"
              />
              <div
                v-else
                class="flex h-full w-full items-center justify-center bg-gradient-to-br from-orange-500/20 to-pink-500/20 text-white font-semibold text-sm"
                @click.stop="isAdminMode && openEditModal(restaurant)"
              >
                {{ restaurant.name }}
              </div>
              <div
                v-if="isAdminMode"
                class="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity pointer-events-none"
              >
                <span class="bg-black/60 text-white text-xs px-3 py-1 rounded-full">Редактировать</span>
              </div>
            </div>
          </div>

          <div class="p-3 sm:p-4">
            <h3 class="font-semibold text-white mb-1 text-sm sm:text-base">
              {{ restaurant.name }}
            </h3>
            <p class="text-xs sm:text-sm text-gray-400 mb-2 sm:mb-3 line-clamp-2">
              {{ restaurant.description }}
            </p>
            <div class="flex items-center justify-end gap-4 text-xs sm:text-sm">
              <div class="flex items-center space-x-2 sm:space-x-4">
                <button
                  type="button"
                  @click.stop="isAdminMode && toggleAvailability(restaurant)"
                  class="px-2 py-1 rounded-xl transition-all max-[450px]:text-[8px]"
                  :class="[
                    restaurant.available ? 'bg-green-500 text-white' : 'bg-red-500 text-white',
                    isAdminMode
                      ? 'cursor-pointer active:scale-95 hover:brightness-110 shadow-md'
                      : 'cursor-default pointer-events-none',
                  ]"
                >
                  {{ restaurant.available ? 'В наличии' : 'Нет в наличии' }}
                </button>

                <div v-if="isAdminMode" class="max-[450px]:right-8 max-[450px]:top-[10px] top-3 z-10">
                  <PenIcon
                    @click.stop="openEditModal(restaurant)"
                    class="w-5 h-5 sm:w-6 sm:h-6 max-[450px]:h-[12px] max-[450px]:w-[12px] cursor-pointer transition-colors text-white"
                  />
                </div>

                <div
                  v-if="isAdminMode"
                  class="w-8 h-8 max-[450px]:h-4 max-[450px]:w-4 rounded-full bg-red-400 flex justify-center items-center"
                >
                  <MinusIcon
                    @click.stop="deleteDish(restaurant.id)"
                    class="w-5 h-5 sm:w-6 sm:h-6 max-[450px]:h-[12px] max-[450px]:w-[12px] cursor-pointer transition-colors"
                  />
                </div>

                <div v-show="isCustomerMode" class="inline-block">
                  <div
                    @click.stop="restaurant.available && handleAddToCart($event, restaurant)"
                    class="w-5 h-5 sm:w-6 sm:h-6 cursor-pointer"
                    :class="{ 'opacity-50 cursor-not-allowed': !restaurant.available }"
                  >
                    <PlusIcon v-if="!isInCart(restaurant.id)" class="w-full h-full text-white" />
                    <MinusIcon v-else class="w-full h-full text-red-400" />
                  </div>
                </div>

                <span class="text-gray-300 text-sm sm:text-[18px] max-[450px]:text-[12px]">
                  {{ restaurant.price }}?
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <CustomModal v-if="showEditModal" @close="closeEditModal">
      <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
        <div class="relative p-4 bg-white rounded-lg w-[90vw] max-w-md max-h-[90vh] overflow-y-auto">
          <button
            type="button"
            @click="closeEditModal"
            class="absolute top-2 right-2 text-gray-500 hover:text-gray-700 p-1 rounded-full hover:bg-gray-200 transition"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          <h2 class="text-lg font-semibold mb-4">Редактировать блюдо</h2>

          <label class="block mb-2">
            Название:
            <input v-model="editingDish.name" class="border p-1 w-full rounded" />
          </label>

          <label class="block mb-2">
            Описание:
            <textarea v-model="editingDish.description" class="border p-1 w-full rounded" />
          </label>

          <label class="block mb-2">
            Цена:
            <input type="number" v-model="editingDish.price" class="border p-1 w-full rounded" />
          </label>

          <div class="mb-3">
            <label class="block text-sm font-medium text-gray-700 mb-1">Категория</label>
            <select
              v-model="editingDish.category"
              class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400"
            >
              <option disabled value="">Выберите категорию</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Изображение</label>
            <ImageEditor
              :current-image-url="editingDish.images?.length ? imageUrl + editingDish.images[0].image_url : null"
              :aspect-ratio="4 / 3"
              @update:file="file = $event"
              @update:preview="previewUrl = $event"
            />
          </div>

          <button
            type="button"
            @click="saveEdit"
            class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 w-full font-semibold"
          >
            Сохранить
          </button>
        </div>
      </div>
    </CustomModal>

    <div
      v-show="isCustomerMode"
      ref="cartIcon"
      class="fixed bottom-4 right-4 w-12 h-12 z-50"
    >
      <div class="relative w-full h-full" @click="router.push('/customer/basket')">
        <ShoppingCartIcon class="w-12 h-12 max-[450px]:w-8 max-[450px]:h-8 text-white" />
        <span
          v-if="totalCount > 0"
          class="absolute -top-1 -right-1 bg-red-500 text-white text-xs w-6 h-6 flex items-center justify-center rounded-full font-bold shadow"
        >
          {{ totalCount }}
        </span>
      </div>
    </div>
  </div>
</template>
