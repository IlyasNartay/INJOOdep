<template>
  <div
    class="min-h-screen w-full bg-gradient-to-br from-purple-900 via-purple-800 to-pink-800 relative animated-gradient"
  >
    <header
      class="bg-gray-900/90 backdrop-blur-sm border-b border-gray-800 sticky top-0 z-40"
    >
      <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-8">
        <div class="flex items-center justify-between h-14 sm:h-16">
          <!-- Logo and Location -->

          <div class="flex items-center space-x-2 sm:space-x-4 flex-1 min-w-0">
            <h1 class="text-lg sm:text-2xl font-bold text-white">INJOO</h1>

            <div
              class="flex items-center space-x-1 sm:space-x-2 text-cyan-400 cursor-pointer min-w-0"
              @click="openModal"
            >
              <MapPinIcon class="w-3 h-3 sm:w-4 sm:h-4 flex-shrink-0" />
              <span
                class="text-xs sm:text-sm truncate max-w-[120px] sm:max-w-none"
              >
                <span
                  class="text-xs sm:text-sm truncate max-w-[120px] sm:max-w-none"
                >
                  {{ shortAddress(address) }}
                </span>
              </span>
              <ChevronDownIcon class="w-3 h-3 sm:w-4 sm:h-4 flex-shrink-0" />
            </div>
          </div>
          <teleport to="body">
            <div
              v-if="isModalOpen"
              @click.self="closeModal"
              class="fixed inset-0 z-50 flex items-center justify-center w-full h-full bg-black/50 backdrop-blur-sm p-4"
            >
              <div
                class="flex flex-col w-full max-w-[800px] h-[90vh] max-h-[1000px] bg-white rounded-lg overflow-scroll"
              >
                <div class="flex justify-between items-center p-4 border-b">
                  <h3 class="text-lg font-semibold">Выберите адрес</h3>
                  <button
                    @click="closeModal()"
                    class="p-2 hover:bg-gray-100 rounded-full transition-colors"
                  >
                    <CrossIcon class="w-5 h-5" />
                  </button>
                </div>

                <div class="flex-1">
                  <Map
                    v-model:address="selectedAddress"
                    v-model:entrance="entrance"
                    v-model:floor="floor"
                    v-model:apartment="apartment"
                  />
                </div>
              </div>
            </div>
          </teleport>
          <div class="hidden md:flex flex-1 max-w-md mx-4 lg:mx-8">
            <div class="relative w-full">
              <SearchIcon
                class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4"
              />
              <input
                v-model="searchQuery"
                placeholder="Поиск в INJOO..."
                class="w-full pl-10 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
              />
            </div>
          </div>

          <!-- Mobile Search Button -->
          <button
            class="md:hidden p-2 text-white"
            @click="showMobileSearch = !showMobileSearch"
          >
            <SearchIcon class="w-5 h-5" />
          </button>
        </div>

        <!-- Mobile Search Bar -->
        <div v-if="showMobileSearch" class="md:hidden pb-3">
          <div class="relative">
            <SearchIcon
              class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4"
            />
            <input
              v-model="searchQuery"
              placeholder="Поиск в INJOO..."
              class="w-full pl-10 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>
    </header>

    <!-- Address Modal -->

    <!-- Main Content -->
    <MenuInterface />
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import Map from "../MainPage/Map.vue";
import MenuInterface from "../../components/MenuInterface.vue";
import axios from "axios";
import {
  Search as SearchIcon,
  MapPin as MapPinIcon,
  ChevronDown as ChevronDownIcon,
  X as CrossIcon,
} from "lucide-vue-next";
import { useAddressStore } from "@/stores/addressStore";

// Reactive data
const searchQuery = ref("");
const showMobileSearch = ref(false);
const selectedAddress = ref("");
const address = ref("");
const entrance = ref("");
const floor = ref("");
const apartment = ref("");

const store = useAddressStore();
const isModalOpen = ref(false);

// В Main.vue исправьте это:
function openModal() {
  selectedAddress.value = address.value; // У вас было .value[0] - это неверно для строки
  // entrance, floor, apartment в Main.vue уже содержат данные из getAdress()
  // и они автоматически передадутся в Map через v-model
  isModalOpen.value = true;
}
function closeModal() {
  isModalOpen.value = false;
}
const shortAddress = (fullAddress) => {
  if (!fullAddress) return "";
  return fullAddress.split(",").slice(0, 2).join(",").trim();
};
const getAdress = async () => {
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_BASE_URL}addresses/`,
      {
        headers: {
          Accept: "application/json",
          Authorization: `Bearer ${localStorage.getItem("authToken")}`,
        },
      }
    );

    const data = response.data;

    if (data && data.length > 0) {
      const lastEntry = data[data.length - 1];

      // 1. Заполняем локальные переменные (те, что в v-model)
      address.value = lastEntry.address || "";
      entrance.value = lastEntry.entrance || "";
      floor.value = lastEntry.floor || "";
      apartment.value = lastEntry.apartment || "";

      // 2. Передаем всё в стор одним объектом
      store.setFullAddress({
        address: address.value,
        entrance: entrance.value,
        floor: floor.value,
        apartment: apartment.value,
      });

      // 3. Синхронизируем карту (если функция объявлена)
      if (typeof searchAddress === "function") {
        searchAddress();
      }
    }
  } catch (error) {
    console.error("Ошибка при получении адресов:", error);
  }
};
onMounted(() => {
  getAdress();
});
</script>

<style>
/* Custom scrollbar for webkit browsers */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Smooth transitions for all interactive elements */
* {
  transition-property: color, background-color, border-color, transform, opacity;
  transition-duration: 150ms;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Line clamp utility */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Hide scrollbar on mobile for cleaner look */
@media (max-width: 640px) {
  .overflow-x-auto::-webkit-scrollbar {
    display: none;
  }
  .overflow-x-auto {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
}
@keyframes gradientMove {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.animated-gradient {
  background: linear-gradient(-45deg, #2e1065, #3b0764, #7e22ce, #be185d);
  background-size: 500% 500%;
  animation: gradientMove 15s ease-in-out infinite;
}
</style>
