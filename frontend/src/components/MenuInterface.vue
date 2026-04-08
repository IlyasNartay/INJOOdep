<script setup>
import { onMounted, ref, computed, watch, nextTick } from "vue";
import axios from "axios";
import {
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  UtensilsCrossed as UtensilsCrossedIcon,
  ShoppingCart as ShoppingCartIcon,
  Minus as MinusIcon,
  Pen as PenIcon,
  PlusIcon as PlusIcon,
} from "lucide-vue-next";
import Loader from "./Loader.vue";
import { useCartStore } from "@/stores/Basket.js";
import { RouterLink, useRouter } from "vue-router";
import CustomModal from "./CustomModal.vue";
import { useAutoClose } from "@/stores/useAutoClose";
import { t } from "@/i18n";
import { USER_ROLES, canUseCustomerUi, currentUserRole } from "@/utils/roles";

const filterName = ref(null);
const isLoading = ref(false);
const menu = ref([]);
const scrollContainer = ref(null);
const image_url = `${import.meta.env.VITE_API_BASE_URL}`;
const cart = useCartStore();
const role = currentUserRole;
const editingDish = ref(null); // РѕР±СЉРµРєС‚ СЂРµРґР°РєС‚РёСЂСѓРµРјРѕРіРѕ Р±Р»СЋРґР°
const showEditModal = ref(false);
const router = useRouter();
const categories = computed(() => [
  { id: "all", name: t("menu.categories.all"), icon: "/all-food.svg" },
  { id: "vegetarian", name: t("menu.categories.vegetarian"), icon: "/vegetables.svg" },
  { id: "salads", name: t("menu.categories.salads"), icon: "/salad.png" },
  { id: "hot_food", name: t("menu.categories.hot_food"), icon: "/hot-food.png" },
  { id: "tebyan", name: t("menu.categories.tebyan"), icon: "/tebyan.svg" },
  { id: "soup", name: t("menu.categories.soup"), icon: "/soup.png" },
  { id: "lagman", name: t("menu.categories.lagman"), icon: "/lagman.png" },
  { id: "comyan", name: t("menu.categories.comyan"), icon: "/comyan.svg" },
  { id: "european", name: t("menu.categories.european"), icon: "/beef.png" },
  { id: "pizza", name: t("menu.categories.pizza"), icon: "/pizza.svg" },
  { id: "moti", name: t("menu.categories.moti"), icon: "/moti.png" },
  { id: "drinks", name: t("menu.categories.drinks"), icon: "/drink.png" },
  { id: "chicken_wings", name: t("menu.categories.chicken_wings"), icon: "/chicken.png" },
  { id: "pasta", name: t("menu.categories.pasta"), icon: "/pasta.svg" },
  { id: "Sushi", name: t("menu.categories.Sushi"), icon: "/sushi.png" },
  { id: "chinese", name: t("menu.categories.chinese"), icon: "/fish.png" },
  { id: "fastfood", name: t("menu.categories.fastfood"), icon: "/fries.png" },
]);
const cartIcon = ref(null);

const successEdit = ref(false);
const successDelete = ref(false);
const fail = ref(false);

function animateToCart(event) {
  const cart = cartIcon.value;
  if (!cart) {
    return;
  }

  // РљРѕРѕСЂРґРёРЅР°С‚С‹ РјРµСЃС‚Р° РєР»РёРєР°
  const startX = event.clientX;
  const startY = event.clientY;

  // РљРѕРѕСЂРґРёРЅР°С‚С‹ РєРѕСЂР·РёРЅС‹
  const cartRect = cart.getBoundingClientRect();
  const endX = cartRect.left + cartRect.width / 2;
  const endY = cartRect.top + cartRect.height / 2;

  // РЎРѕР·РґР°С‘Рј Р»РµС‚Р°СЋС‰РёР№ СЌР»РµРјРµРЅС‚ (РјРѕР¶РЅРѕ Р·Р°РјРµРЅРёС‚СЊ РЅР° РєР°СЂС‚РёРЅРєСѓ Р±Р»СЋРґР°)
  const fly = document.createElement("div");
  fly.style.position = "fixed";
  fly.style.left = startX + "px";
  fly.style.top = startY + "px";
  fly.style.width = "30px";
  fly.style.height = "30px";
  fly.style.borderRadius = "50%";
  fly.style.background = "#4ade80"; // Р·РµР»С‘РЅС‹Р№ РєСЂСѓР¶РѕРє
  fly.style.zIndex = "9999";
  fly.style.transition = "all 0.7s cubic-bezier(0.4, 0, 0.2, 1)";

  document.body.appendChild(fly);

  // Р—Р°РїСѓСЃРє Р°РЅРёРјР°С†РёРё
  setTimeout(() => {
    fly.style.left = endX + "px";
    fly.style.top = endY + "px";
    fly.style.transform = "scale(0.3)";
    fly.style.opacity = "0";
  }, 10);

  // РЈРґР°Р»СЏРµРј РїРѕСЃР»Рµ Р·Р°РІРµСЂС€РµРЅРёСЏ Р°РЅРёРјР°С†РёРё
  setTimeout(() => {
    fly.remove();
  }, 800);
}
const totalCount = computed(() =>
  cart.items.reduce((sum, item) => sum + item.quantity, 0)
);
const handleAddToCart = (event, restaurant) => {
  animateToCart(event); // Р·Р°РїСѓСЃРєР°РµРј РїРѕР»С‘С‚
  cart.toggleItem(restaurant); // РґРѕР±Р°РІР»СЏРµРј РІ РєРѕСЂР·РёРЅСѓ
};
const isInCart = (id) => {
  return cart.isInCart(id);
};
const filterLabel = computed(() => {
  const cat = categories.value.find((c) => c.id === filterName.value);
  return cat ? cat.name : "";
});
function selectCategory(category) {
  filterName.value = category.id;
  getExact();
}
const openEditModal = (dish) => {
  editingDish.value = { ...dish }; // РєРѕРїРёСЏ, С‡С‚РѕР±С‹ РЅРµ РјСѓС‚РёСЂРѕРІР°С‚СЊ РЅР°РїСЂСЏРјСѓСЋ
  showEditModal.value = true;
};
const scrollLeft = () => {
  const scrollAmount =
    window.innerWidth < 640 ? 240 : window.innerWidth < 1024 ? 260 : 280;
  scrollContainer.value?.scrollBy({ left: -scrollAmount, behavior: "smooth" });
};

const scrollRight = () => {
  const scrollAmount =
    window.innerWidth < 640 ? 240 : window.innerWidth < 1024 ? 260 : 280;
  scrollContainer.value?.scrollBy({ left: scrollAmount, behavior: "smooth" });
};

const getMenu = async () => {
  isLoading.value = true;

  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_BASE_URL}menu/`
    );
    menu.value = response.data;
  } catch (error) {
    console.error("РћС€РёР±РєР° РїСЂРё РїРѕР»СѓС‡РµРЅРёРё РјРµРЅСЋ:", error);
  } finally {
    isLoading.value = false;
  }
};
const getExact = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_BASE_URL}menu/category/${filterName.value}`
    );
    menu.value = response.data;
  } catch (error) {
    console.error("РћС€РёР±РєР° РїСЂРё РїРѕР»СѓС‡РµРЅРёРё РјРµРЅСЋ:", error);
  } finally {
    isLoading.value = false;
  }
};
const deleteDish = async (id) => {
  isLoading.value = true;
  try {
    const response = await axios.delete(
      `${import.meta.env.VITE_API_BASE_URL}menu/${id}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("authToken")}`,
        },
      }
    );

    if (response.status === 200) {
      menu.value = menu.value.filter((item) => item.id !== id);
    }
    successDelete.value = true;
    return response.data;
  } catch (error) {
    console.error("РћС€РёР±РєР° РїСЂРё СѓРґР°Р»РµРЅРёРё:", error);
    fail.value = true;
  } finally {
    isLoading.value = false;
  }
};
const toggleAvailability = async (restaurant) => {
  if (!restaurant) return;

  const newStatus = !restaurant.available;

  // 1. РЎРѕР·РґР°РµРј РѕР±СЉРµРєС‚ РїР°СЂР°РјРµС‚СЂРѕРІ С„РѕСЂРјС‹ (x-www-form-urlencoded)
  const params = new URLSearchParams();
  params.append("available", newStatus);

  try {
    const response = await axios.patch(
      `${import.meta.env.VITE_API_BASE_URL}menu/${restaurant.id}/availability`,
      params, // РџРµСЂРµРґР°РµРј РїР°СЂР°РјРµС‚СЂС‹ РІРјРµСЃС‚Рѕ РѕР±С‹С‡РЅРѕРіРѕ РѕР±СЉРµРєС‚Р°
      {
        headers: {
          // 2. РЈРєР°Р·С‹РІР°РµРј РїСЂР°РІРёР»СЊРЅС‹Р№ Content-Type, РєРѕС‚РѕСЂС‹Р№ С‚СЂРµР±СѓРµС‚ РІР°С€ СЃРµСЂРІРµСЂ
          "Content-Type": "application/x-www-form-urlencoded",
          Authorization: `Bearer ${localStorage.getItem("authToken")}`,
          Accept: "application/json",
        },
      }
    );

    if (response.status === 200 || response.status === 204) {
      restaurant.available = newStatus;
    }
  } catch (error) {
    console.error("Р”РµС‚Р°Р»Рё РѕС€РёР±РєРё СЃРµСЂРІРµСЂР°:", error.response?.data);
    alert("РќРµ СѓРґР°Р»РѕСЃСЊ РѕР±РЅРѕРІРёС‚СЊ СЃС‚Р°С‚СѓСЃ. РџСЂРѕРІРµСЂСЊС‚Рµ РєРѕРЅСЃРѕР»СЊ.");
  }
};

const file = ref(null);

const handleFileChange = (event) => {
  file.value = event.target.files[0];
};

const saveEdit = async () => {
  const formData = new FormData();
  formData.append("name", editingDish.value.name);
  formData.append("description", editingDish.value.description);
  formData.append("price", editingDish.value.price);
  formData.append("category", editingDish.value.category);

  // РµСЃР»Рё РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ РІС‹Р±СЂР°Р» РЅРѕРІРѕРµ РёР·РѕР±СЂР°Р¶РµРЅРёРµ
  if (file.value) {
    formData.append("images", file.value); // РєР°Рє РІ POST
  }

  isLoading.value = true;
  try {
    const response = await axios.put(
      `${import.meta.env.VITE_API_BASE_URL}menu/${editingDish.value.id}`,
      formData,
      {
        headers: {
          Accept: "application/json",
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${localStorage.getItem("authToken")}`,
        },
      }
    );

    showEditModal.value = false;

    // Р»РѕРєР°Р»СЊРЅРѕ РѕР±РЅРѕРІРёРј Р±Р»СЋРґРѕ
    const index = menu.value.findIndex(
      (item) => item.id === editingDish.value.id
    );
    if (index !== -1) {
      menu.value[index] = { ...editingDish.value };
    }
    successEdit.value = true;
  } catch (error) {
    console.error(
      "вќЊ РћС€РёР±РєР° РїСЂРё РѕР±РЅРѕРІР»РµРЅРёРё:",
      error.response?.data || error.message
    );
    fail.value = true;
  } finally {
    isLoading.value = false;
  }
};
useAutoClose(successEdit, 2000);
useAutoClose(fail, 2500);
useAutoClose(successDelete, 3000);

watch(filterName, (newVal) => {
  if (newVal === "all") {
    getMenu();
  } else {
    console.log("рџ”Ќ Р¤РёР»СЊС‚СЂР°С†РёСЏ РїРѕ РєР°С‚РµРіРѕСЂРёРё:", newVal);
    // РµСЃР»Рё РЅСѓР¶РЅРѕ, РјРѕР¶РµС€СЊ РІС‹Р·РІР°С‚СЊ РґСЂСѓРіСѓСЋ С„СѓРЅРєС†РёСЋ (РЅР°РїСЂРёРјРµСЂ getMenuByCategory(newVal))
  }
});
onMounted(() => {
  getMenu();
  console.log(menu, "res");
});
</script>

<template>
  <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-8 py-4 sm:py-6 lg:py-8">
    <Loader v-if="isLoading" />
    <div class="mb-6 sm:mb-8">
      <div class="flex gap-6 sm:gap-8 overflow-y-hiden overflow-x-scroll">
        <div
          v-for="category in categories"
          :key="category.id"
          class="flex flex-col items-center space-y-1 sm:space-y-2 cursor-pointer group"
          @click="selectCategory(category)"
        >
          <div
            class="w-12 h-12 sm:w-14 sm:h-14 lg:w-16 lg:h-16 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl sm:rounded-2xl flex items-center justify-center group-hover:scale-105 transition-transform"
          >
            <img
              :src="category.icon"
              class="w-6 h-6 sm:w-7 sm:h-7 lg:w-8 lg:h-8"
            />
          </div>
          <span
            class="text-[10px] sm:text-xs text-white text-center leading-tight"
          >
            {{ category.name }}
          </span>
        </div>
      </div>
    </div>

    <!-- Restaurant Sections -->
    <div class="space-y-6 sm:space-y-8">
      <!-- РџРѕР·РґРЅРёР№ РїРµСЂРµРєСѓСЃ РЅРµРїРѕРґР°Р»С‘РєСѓ -->
      <section>
        <div class="flex items-center justify-between mb-4 sm:mb-6">
          <h2 class="text-lg sm:text-xl lg:text-2xl font-bold text-white">
            {{ t("menu.selectedCategory") }}: {{ filterLabel || t("common.all") }}
          </h2>
          <div class="flex items-center space-x-1 sm:space-x-2">
            <button
              @click="scrollLeft"
              class="text-white hover:text-cyan-400 p-1 sm:p-2 rounded transition-colors"
            >
              <ChevronLeftIcon class="w-4 h-4" />
            </button>
            <button
              @click="scrollRight"
              class="text-white hover:text-cyan-400 p-1 sm:p-2 rounded transition-colors"
            >
              <ChevronRightIcon class="w-4 h-4" />
            </button>
          </div>
        </div>
        <Loader v-if="isLoading" />
        <div
          ref="scrollContainer"
          class="flex flex-wrap gap-3 sm:gap-4 lg:gap-6 overflow-x-auto scroll-smooth pb-2"
        >
          <div
            v-for="restaurant in menu"
            :key="restaurant.id"
            class="w-[280px] max-[650px]:w-[210px] max-[450px]:w-[170px] max-[400px]:w-[160px] max-[350px]:w-[140px] max-[450px]:h-full bg-gray-800/50 border border-gray-700 mx-auto rounded-lg overflow-hidden hover:bg-gray-800/70 transition-colors cursor-pointer flex-shrink-0"
          >
            <div class="relative">
              <CustomModal v-if="successEdit">
                <div
                  class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center"
                >
                  <img
                    src="/sucsess-modal.svg"
                    alt="РЈСЃРїРµС€РЅРѕ"
                    class="w-16 h-16 mx-auto mb-4"
                  />
                  <h3 class="text-xl font-semibold text-black mb-2">
                    Р’С‹ СѓСЃРїРµС€РЅРѕ РїРѕРјРµРЅСЏР»Рё Р±Р»СЋРґРѕ!
                  </h3>
                  <button
                    @click="success = false"
                    class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold"
                  >
                    Р—Р°РєСЂС‹С‚СЊ
                  </button>
                </div>
              </CustomModal>
              <CustomModal v-if="fail">
                <div
                  class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center"
                >
                  <img
                    src="/fail-modal.svg"
                    alt="РќРµ РЈСЃРїРµС€РЅРѕ"
                    class="w-16 h-16 mx-auto mb-4"
                  />
                  <h3 class="text-xl font-semibold text-black mb-2">
                    Р§С‚Рѕ-С‚Рѕ РїРѕС€Р»Рѕ РЅРµ С‚Р°Рє!
                  </h3>
                  <button
                    @click="success = false"
                    class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold"
                  >
                    Р—Р°РєСЂС‹С‚СЊ
                  </button>
                </div>
              </CustomModal>
              <CustomModal v-if="successDelete">
                <div
                  class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center"
                >
                  <img
                    src="/sucsess-modal.svg"
                    alt="РЈСЃРїРµС€РЅРѕ"
                    class="w-16 h-16 mx-auto mb-4"
                  />
                  <h3 class="text-xl font-semibold text-black mb-2">
                    Р’С‹ СѓСЃРїРµС€РЅРѕ СѓРґР°Р»РёР»Рё Р±Р»СЋРґРѕ!
                  </h3>
                  <button
                    @click="success = false"
                    class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold"
                  >
                    Р—Р°РєСЂС‹С‚СЊ
                  </button>
                </div>
              </CustomModal>
              <div
                class="relative w-full aspect-[4/3] overflow-hidden rounded-xl"
              >
                <img
                  v-if="restaurant.images?.length"
                  :src="image_url + restaurant.images[0].image_url"
                  :alt="restaurant.name"
                  class="w-full h-full object-cover object-center transition-transform duration-500"
                />
              </div>
            </div>
            <div class="p-3 sm:p-4">
              <h3 class="font-semibold text-white mb-1 text-sm sm:text-base">
                {{ restaurant.name }}
              </h3>
              <p
                class="text-xs sm:text-sm text-gray-400 mb-2 sm:mb-3 line-clamp-2"
              >
                {{ restaurant.description }}
              </p>
              <div
                class="flex items-center justify-end gap-4 text-xs sm:text-sm"
              >
                <div class="flex items-center space-x-2 sm:space-x-4">
                  <div class=" ">
                    <button
                      @click.stop="toggleAvailability(restaurant)"
                      class="px-2 py-1 rounded-xl transition-all max-[450px]:text-[8px]"
                      :class="[
                        // Р‘Р°Р·РѕРІС‹Рµ С†РІРµС‚Р° Р·Р°РІРёСЃСЏС‚ С‚РѕР»СЊРєРѕ РѕС‚ РЅР°Р»РёС‡РёСЏ С‚РѕРІР°СЂР°
                        restaurant.available
                          ? 'bg-green-500 text-white'
                          : 'bg-red-500 text-white',

                        // Р”РёРЅР°РјРёС‡РµСЃРєРёРµ СЌС„С„РµРєС‚С‹ Р·Р°РІРёСЃСЏС‚ РўРћР›Р¬РљРћ РѕС‚ СЂРѕР»Рё
                        role === USER_ROLES.ADMIN
                          ? 'cursor-pointer active:scale-95 hover:brightness-110 shadow-md'
                          : 'cursor-default pointer-events-none',
                      ]"
                    >
                      {{ restaurant.available ? "Р’ РЅР°Р»РёС‡РёРё" : "РќРµС‚ РІ РЅР°Р»РёС‡РёРё" }}
                    </button>
                  </div>
                  <div
                    class="max-[450px]:right-8 max-[450px]:top-[10px] top-3 z-10"
                    v-if="role === USER_ROLES.ADMIN"
                  >
                    <PenIcon
                      @click.stop="openEditModal(restaurant)"
                      class="w-5 h-5 sm:w-6 sm:h-6 max-[450px]:h-[12px] max-[450px]:w-[12px] cursor-pointer transition-colors text-white"
                    />
                  </div>
                  <div
                    v-if="role === USER_ROLES.ADMIN"
                    class="w-8 h-8 max-[450px]:h-4 max-[450px]:w-4 rounded-full bg-red-400 flex justify-center items-center"
                  >
                    <MinusIcon
                      @click.stop="deleteDish(restaurant.id)"
                      class="w-5 h-5 sm:w-6 sm:h-6 max-[450px]:h-[12px] max-[450px]:w-[12px] cursor-pointer transition-colors"
                    />
                  </div>
                  <div
                  v-show="canUseCustomerUi()"
                  class="inline-block"
                >
                  <div
  @click.stop="restaurant.available && handleAddToCart($event, restaurant)"
  class="w-5 h-5 sm:w-6 sm:h-6 cursor-pointer"
  :class="{ 'opacity-50 cursor-not-allowed': !restaurant.available }"
>
  <PlusIcon
    v-if="!isInCart(restaurant.id)"
    class="w-full h-full text-white"
  />
  <MinusIcon v-else class="w-full h-full text-red-400" />
</div>

                </div>
                  <span class="text-gray-300 text-sm sm:text-[18px] max-[450px]:text-[12px]"
                    >{{ restaurant.price }}в‚ё</span
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
    <CustomModal v-if="showEditModal" @close="showEditModal = false">
      <div
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
      >
        <div class="relative p-4 bg-white rounded-lg w-[90vw] max-w-md">
          <!-- РљРЅРѕРїРєР° Р·Р°РєСЂС‹С‚РёСЏ -->
          <button
            @click="showEditModal = false"
            class="absolute top-2 right-2 text-gray-500 hover:text-gray-700 p-1 rounded-full hover:bg-gray-200 transition"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>

          <h2 class="text-lg font-semibold mb-4">Р РµРґР°РєС‚РёСЂРѕРІР°С‚СЊ Р±Р»СЋРґРѕ</h2>

          <label class="block mb-2">
            РќР°Р·РІР°РЅРёРµ:
            <input v-model="editingDish.name" class="border p-1 w-full" />
          </label>

          <label class="block mb-2">
            РћРїРёСЃР°РЅРёРµ:
            <textarea
              v-model="editingDish.description"
              class="border p-1 w-full"
            />
          </label>

          <label class="block mb-2">
            Р¦РµРЅР°:
            <input
              type="number"
              v-model="editingDish.price"
              class="border p-1 w-full"
            />
          </label>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              РљР°С‚РµРіРѕСЂРёСЏ
            </label>
            <select
              v-model="editingDish.category"
              class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400"
            >
              <option disabled value="">Р’С‹Р±РµСЂРёС‚Рµ РєР°С‚РµРіРѕСЂРёСЋ</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
          </div>

          <label class="block mb-2">
            РР·РѕР±СЂР°Р¶РµРЅРёРµ:
            <input
              type="file"
              @change="handleFileChange"
              class="border p-1 w-full"
            />
          </label>

          <button
            @click="saveEdit"
            class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          >
            РЎРѕС…СЂР°РЅРёС‚СЊ
          </button>
        </div>
      </div>
    </CustomModal>
    <div
      class="fixed bottom-4 right-4 w-12 h-12 z-50"
      ref="cartIcon"
      v-show="canUseCustomerUi()"
    >
      <div class="relative w-full h-full" @click="router.push('/customer/basket')">
        <ShoppingCartIcon class="w-12 h-12 max-[450px]:w-8 max-[450px]:h-8 text-white" />

        <!-- Р‘РµР№РґР¶ -->
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


