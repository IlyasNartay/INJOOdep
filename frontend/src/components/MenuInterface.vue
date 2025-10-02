<script setup>
import { onMounted, ref, computed } from "vue";
import axios from "axios";
import {
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  UtensilsCrossed as UtensilsCrossedIcon,
  ShoppingCart as ShoppingCartIcon,
  Minus as MinusIcon,
  Pen as PenIcon,
} from "lucide-vue-next";

import { useCartStore } from "/src/stores/Basket.js";

const filterName = ref(null);
const isLoading = ref(false);
const menu = ref([]);
const scrollContainer = ref(null);
const image_url = "${import.meta.env.VITE_API_BASE_URL}";
const cart = useCartStore();
const role = localStorage.getItem("userRole");
const editingDish = ref(null); // объект редактируемого блюда
const showEditModal = ref(false);

const categories = ref([
  { id: "all", name: "Все блюда", icon: "/all-food.svg" },
  { id: "vegetarian", name: "Вегетерианские", icon: "/vegetables.svg" },
  { id: "salads", name: "Салат", icon: "/salad.png" },
  { id: "hot_food", name: "Горячие", icon: "/hot-food.png" },
  { id: "tebyan", name: "Тебян", icon: "/tebyan.svg" },
  { id: "fish", name: "Рыба", icon: "/fish.png" },
  { id: "soup", name: "Суп", icon: "/soup.png" },
  { id: "holiday", name: "Праздничное", icon: "/holiday.png" },
  { id: "lagman", name: "Лагман", icon: "/lagman.png" },
  { id: "comyan", name: "Цомиян", icon: "/comyan.svg" },
  { id: "european", name: "Европейские", icon: "/europe.png" },
  { id: "pizza", name: "Пицца", icon: "/pizza.svg" },
  { id: "moti", name: "Моти", icon: "/moti.png" },
  { id: "drinks", name: "Напитки", icon: "/drink.png" },
  { id: "chicken_wings", name: "Крылышки куриные", icon: "/chicken.png" },
  { id: "pasta", name: "Паста", icon: "/pasta.svg" },
  { id: "fries", name: "Картофель фри", icon: "/fries.png" },
])
const menu1 = [
  {
    id: 1,
    name: "Маргарита",
    description: "Классическая пицца с томатным соусом, моцареллой и свежим базиликом.",
    price: 2500,
    images: [
      { image_url: "/Milk-tea-removebg-preview.png" }
    ]
  },
  {
    id: 2,
    name: "Чизбургер",
    description: "Сочный бифштекс из говядины, сыр чеддер, свежие овощи и фирменный соус.",
    price: 2000,
    images: [
      { image_url: "/Milk-tea-removebg-preview.png" }
    ]
  },
  {
    id: 3,
    name: "Филадельфия",
    description: "Ролл с лососем, сливочным сыром и авокадо, завернутый в рис и нори.",
    price: 3000,
    images: [
      { image_url: "/Milk-tea-removebg-preview.png" }
    ]
  },
  {
    id: 4,
    name: "Стейк Рибай",
    description: "Стейк средней прожарки из мраморной говядины с овощами-гриль.",
    price: 7500,
    images: [
      { image_url: "/Milk-tea-removebg-preview.png" }
    ]
  },
  {
    id: 5,
    name: "Салат Цезарь",
    description: "Курица гриль, листья салата, сухарики и пармезан под классическим соусом.",
    price: 1800,
    images: [
      { image_url: "/public/Milk-tea-removebg-preview.png" }
    ]
  }
]


const toggleCart = (restaurant) => {
  cart.toggleItem(restaurant);
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
  console.log(filterName.value, "filterName");
  getExact();
}
const openEditModal = (dish) => {
  editingDish.value = { ...dish }; // копия, чтобы не мутировать напрямую
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

const selectRestaurant = (restaurantId) => {
  console.log("Selected restaurant:", restaurantId);
};

const getMenu = async () => {
  isLoading.value = true;

  try {
    const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}menu/`);
    menu.value = response.data;
  } catch (error) {
    console.error("Ошибка при получении меню:", error);
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
    console.error("Ошибка при получении меню:", error);
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
      console.log("Удалено:", id);
      // ⬇️ Удаляем из локального списка меню
      menu.value = menu.value.filter((item) => item.id !== id);
    }

    return response.data;
  } catch (error) {
    console.error("Ошибка при удалении:", error);
  } finally {
    isLoading.value = false;
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

  // если пользователь выбрал новое изображение
  if (file.value) {
    formData.append("images", file.value); // как в POST
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

    console.log("✅ Обновлено:", response.data);

    showEditModal.value = false;

    // локально обновим блюдо
    const index = menu.value.findIndex(
      (item) => item.id === editingDish.value.id
    );
    if (index !== -1) {
      menu.value[index] = { ...editingDish.value };
    }
  } catch (error) {
    console.error(
      "❌ Ошибка при обновлении:",
      error.response?.data || error.message
    );
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  getMenu();
});
</script>

<template>
  <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-8 py-4 sm:py-6 lg:py-8">
    <div class="mb-6 sm:mb-8">
      <div
        class="flex gap-6 sm:gap-8 overflow-y-scroll"
      >
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

    <!-- Promotional Banners -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 mb-6 sm:mb-8">
      <div
        class="bg-gradient-to-r from-orange-500 to-red-500 rounded-lg p-4 sm:p-6 text-white"
      >
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <div
              class="bg-cyan-400 text-black px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-bold mb-2 inline-block"
            >
              -30%
            </div>
            <h3 class="text-sm sm:text-lg font-bold mb-2">
              Скидка 30% на позиции в SF Shaurma Food!
            </h3>
          </div>
          <div
            class="w-16 h-16 sm:w-20 sm:h-20 lg:w-24 lg:h-24 bg-white/20 rounded-full flex items-center justify-center ml-4"
          >
            <UtensilsCrossedIcon
              class="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12"
            />
          </div>
        </div>
      </div>

      <div
        class="bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg p-4 sm:p-6 text-white"
      >
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <div
              class="bg-orange-400 text-black px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-bold mb-2 inline-block"
            >
              -20%
            </div>
            <h3 class="text-sm sm:text-lg font-bold mb-2">
              Скидка 20% и позиции в подарок в KFC!
            </h3>
          </div>
          <div
            class="w-16 h-16 sm:w-20 sm:h-20 lg:w-24 lg:h-24 bg-white/20 rounded-full flex items-center justify-center ml-4"
          >
            <UtensilsCrossedIcon
              class="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Restaurant Sections -->
    <div class="space-y-6 sm:space-y-8">
      <!-- Поздний перекус неподалёку -->
      <section>
        <div class="flex items-center justify-between mb-4 sm:mb-6">
          <h2 class="text-lg sm:text-xl lg:text-2xl font-bold text-white">
            Выбранная каттегория: {{ filterLabel || "Все" }}
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
            class="w-[280px] max-[650px]:w-[210px] max-[450px]:w-[170px] max-[400px]:w-[160px] max-[450px]:h-[260px] bg-gray-800/50 border border-gray-700 mx-auto rounded-lg overflow-hidden hover:bg-gray-800/70 transition-colors cursor-pointer flex-shrink-0 pt-2"
            @click="selectRestaurant(restaurant.id)"
          >
            <div class="relative ">
              <div
                class="absolute right-2 top-2 z-10"
                v-if="role == 'customer'"
              >
                <ShoppingCartIcon
                  @click.stop="toggleCart(restaurant)"
                  class="w-5 h-5 sm:w-6 sm:h-6 cursor-pointer transition-colors"
                  :class="
                    isInCart(restaurant.id) ? 'text-green-500' : 'text-white'
                  "
                />
              </div>
              <div class="absolute right-14 max-[450px]:right-8 max-[450px]:top-[10px] top-3 z-10" v-if="role == 'admin'">
                <PenIcon
                  @click.stop="openEditModal(restaurant)"
                  class="w-5 h-5 sm:w-6 sm:h-6 max-[450px]:h-[12px]  max-[450px]:w-[12px] cursor-pointer transition-colors text-white"
                />
              </div>
              <div class="absolute right-2 top-2 z-10" v-if="role == 'admin'">
                <div
                  class="w-8 h-8 max-[450px]:h-4  max-[450px]:w-4 rounded-full bg-red-400 flex justify-center items-center"
                >
                  <MinusIcon
                    @click.stop="deleteDish(restaurant.id)"
                    class="w-5 h-5 sm:w-6 sm:h-6  max-[450px]:h-[12px]  max-[450px]:w-[12px] cursor-pointer transition-colors"
                  />
                </div>
              </div>
              <img
                v-if="restaurant.images && restaurant.images.length"

                src="/Milk-tea-removebg-preview.png"
                :alt="restaurant.name"
                class="h-[180px] max-[450px]:h-[145px] sm:h-[220px] lg:h-[300px] w-full object-cover"
              />
              <!-- <p>image_url + restaurant.images[0].image_url</p> -->
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
              <div class="flex items-center justify-end text-xs sm:text-sm">
                <div class="flex items-center space-x-2 sm:space-x-4">
                  <span class="text-gray-300 text-sm sm:text-[18px]"
                    >{{ restaurant.price }}₸</span
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
          <!-- Кнопка закрытия -->
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

          <h2 class="text-lg font-semibold mb-4">Редактировать блюдо</h2>

          <label class="block mb-2">
            Название:
            <input v-model="editingDish.name" class="border p-1 w-full" />
          </label>

          <label class="block mb-2">
            Описание:
            <textarea
              v-model="editingDish.description"
              class="border p-1 w-full"
            />
          </label>

          <label class="block mb-2">
            Цена:
            <input
              type="number"
              v-model="editingDish.price"
              class="border p-1 w-full"
            />
          </label>

          <label class="block mb-2">
            Категория:
            <input v-model="editingDish.category" class="border p-1 w-full" />
          </label>

          <label class="block mb-2">
            Изображение:
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
            Сохранить
          </button>
        </div>
      </div>
    </CustomModal>
  </div>
</template>
