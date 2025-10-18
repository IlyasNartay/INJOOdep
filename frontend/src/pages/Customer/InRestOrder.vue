<template>
  <div
    class="min-h-screen w-full bg-gradient-to-br from-purple-900 via-purple-800 to-pink-800 relative"
  >
    <!-- Header -->
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
              <SofaIcon class="w-3 h-3 sm:w-4 sm:h-4 flex-shrink-0" />
              <span
                class="text-xs sm:text-sm truncate max-w-[120px] sm:max-w-none"
              >
                {{ `Ваш столик №${selectedTable}` || 'Выберите номер столика'}}
              </span>
              <ChevronDownIcon class="w-3 h-3 sm:w-4 sm:h-4 flex-shrink-0" />
            </div>
          </div>

          <div
            v-if="isModalOpen"
            class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 min-h-screen"
          >
            <div
              class="flex flex-col w-full max-w-[800px] h-[90vh] max-h-[1000px] bg-white rounded-lg overflow-hidden"
            >
              <!-- Хедер -->
              <div class="flex justify-between items-center p-4 border-b">
                <h3 class="text-lg font-semibold">Выберите столик</h3>
                <button
                  @click="closeModal"
                  class="p-2 hover:bg-gray-100 rounded-full transition-colors"
                >
                  ✕
                </button>
              </div>

              <!-- Контент -->
              <div class="flex-1 p-4">
                <!-- Легенда -->
                <div class="flex items-center gap-4 mb-4 text-sm">
                  <div class="flex items-center gap-2">
                    <span
                      class="w-4 h-4 rounded bg-gray-100 border border-gray-300 inline-block"
                    ></span>
                    Свободно
                  </div>
                  <div class="flex items-center gap-2">
                    <span
                      class="w-4 h-4 rounded bg-cyan-100 border border-cyan-400 inline-block"
                    ></span>
                    Выбрано
                  </div>
                </div>

                <!-- Сетка столиков -->
                <div class="grid grid-cols-4 sm:grid-cols-6 gap-3">
                  <button
                    v-for="n in tables"
                    :key="n"
                    @click="pickTable(n)"
                    class="relative h-12 rounded-lg border transition hover:shadow-sm focus:outline-none focus:ring-2 focus:ring-cyan-500 flex items-center justify-center select-none"
                    :class="[
                      selectedTable === n
                        ? 'bg-cyan-100 border-cyan-400 text-cyan-900'
                        : 'bg-gray-100 border-gray-300 text-gray-900',
                    ]"
                  >
                    {{ n }}
                    <span
                      v-if="selectedTable === n"
                      class="absolute -top-2 -right-2 bg-cyan-500 text-white text-[10px] px-1.5 py-0.5 rounded-full"
                    >
                      выбрано
                    </span>
                  </button>
                </div>
              </div>

              <!-- Футер -->
              <div class="p-4 border-t flex items-center justify-between">
                <div class="text-sm text-gray-600">
                  Текущий выбор:
                  <span class="font-medium">{{ tableLabel }}</span>
                </div>
                <div class="flex gap-2">
                  <button
                    @click="closeModal"
                    class="px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50 transition"
                  >
                    Отмена
                  </button>
                  <button
                    @click="saveTable"
                    :disabled="!selectedTable"
                    class="px-4 py-2 rounded-lg bg-cyan-600 text-white hover:bg-cyan-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
                  >
                    Сохранить
                  </button>
                </div>
              </div>
            </div>
          </div>
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
import {
  Search as SearchIcon,
  MapPin as MapPinIcon,
  ChevronDown as ChevronDownIcon,
  X as CrossIcon,
  Sofa as SofaIcon,
} from "lucide-vue-next";
import axios from "axios";
const role = localStorage.getItem("userRole");
// Reactive data
const activeSection = ref("recommendations");
const searchQuery = ref("");
const showMobileSearch = ref(false);
const router = useRouter();
const address = ref([{ address: "" }]);
const selectedAddress = ref("");

const isModalOpen = ref(false);
function openModal() {
  selectedAddress.value = address.value[0]?.address ?? "";
  isModalOpen.value = true;
}
function closeModal() {
  isModalOpen.value = false;
}

const tables = ref(Array.from({ length: 20 }, (_, i) => i + 1)); // столики 1..20
const selectedTable = ref(null);

const tableLabel = computed(() =>
  selectedTable.value ? `Столик №${selectedTable.value}` : "Столик не выбран"
);

function pickTable(n) {
  selectedTable.value = n;
}

function saveTable() {
  if (!selectedTable.value) return;
  localStorage.setItem("selectedTable", selectedTable.value);
  console.log("Сохранено:", selectedTable.value);
  closeModal();
}

onMounted(() => {
   localStorage.setItem('userRole', 'guest')
  console.log('✅ Гостевая роль установлена')
  const saved = localStorage.getItem("selectedTable");
  if (saved) selectedTable.value = Number(saved);
  
});
</script>

<style scoped>
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
</style>
