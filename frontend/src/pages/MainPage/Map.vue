<template>
  <div
    class="min-h-screen  overflow-y-auto bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-100 py-6 px-4"
  >
    <div class="max-w-4xl mx-auto space-y-8">
      <!-- Header Section -->

      <div class="text-center space-y-2">
        <h1
          class="text-3xl md:text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"
        >
          Выберите адрес
        </h1>
        <p class="text-gray-600 text-lg">
          Найдите точное местоположение на карте
        </p>
      </div>

      <!-- Main Content Card -->
      <div
        class="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 overflow-hidden"
      >
        <!-- Address Search Section -->
        <div
          class="p-6 md:p-8 bg-gradient-to-r from-blue-500/5 to-purple-500/5"
        >
          <div class="space-y-6">
            <!-- Search Input with Icon -->
            <div class="relative">
              <div
                class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none"
              >
                <SearchIcon class="h-5 w-5 text-gray-400" />
              </div>
              <input
                v-model="address"
                @input="fetchSuggestions"
                placeholder="Введите адрес для поиска..."
                class="w-full pl-12 pr-4 py-4 bg-white/70 backdrop-blur-sm border border-gray-200/50 rounded-2xl text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500/50 transition-all duration-300 text-lg shadow-lg"
              />

              <!-- Loading Spinner -->
              <div
                v-if="isLoading"
                class="absolute inset-y-0 right-0 pr-4 flex items-center"
              >
                <div
                  class="animate-spin rounded-full h-5 w-5 border-2 border-blue-500 border-t-transparent"
                ></div>
              </div>
            </div>

            <!-- Suggestions Dropdown -->
            <div v-if="suggestions.length" class="relative">
              <ul
                class="absolute top-0 left-0 right-0 bg-white/95 backdrop-blur-xl border border-gray-200/50 rounded-2xl shadow-2xl z-30 max-h-64 overflow-auto"
              >
                <li
                  v-for="(item, index) in suggestions"
                  :key="index"
                  @click="selectSuggestion(item)"
                  class="px-6 py-4 hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50 cursor-pointer transition-all duration-200 border-b border-gray-100/50 last:border-b-0 flex items-center space-x-3"
                >
                  <MapPinIcon class="h-4 w-4 text-blue-500 flex-shrink-0" />
                  <span class="text-gray-700 text-sm">{{
                    item.display_name
                  }}</span>
                </li>
              </ul>
            </div>
            <CustomModal v-if="succesModal">
              <div
                class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center"
              >
                <img
                  src="/sucsess-modal.svg"
                  alt="Успешно"
                  class="w-16 h-16 mx-auto mb-4"
                />
                <h3 class="text-xl font-semibold text-black mb-2">
                  Ваш адрес добавлен!
                </h3>
                <p class="text-black mb-4">Можете делать заказы!</p>
                <button
                  @click="succesModal = false"
                  class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold"
                >
                  Закрыть
                </button>
              </div>
            </CustomModal>
            <CustomModal v-if="failModal">
              <div
                class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center"
              >
                <img
                  src="/fail-modal.svg"
                  alt="Успешно"
                  class="w-16 h-16 mx-auto mb-4"
                />
                <h3 class="text-xl font-semibold text-black mb-2">
                  Ваш адрес не добавлен!
                </h3>
                <p class="text-black mb-4">Повторите попытку позже!</p>
                <button
                  @click="failModal = false"
                  class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold"
                >
                  Закрыть
                </button>
              </div>
            </CustomModal>
            <!-- Action Buttons -->
            <div class="flex flex-col sm:flex-row gap-3">
              <button
                @click="searchAddress"
                class="flex-1 flex items-center justify-center space-x-2 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-semibold py-3 px-6 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-200"
              >
                <SearchIcon class="h-5 w-5" />
                <span>Найти адрес</span>
              </button>

              <button
                @click="getCurrentLocation"
                class="flex-1 flex items-center justify-center space-x-2 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-semibold py-3 px-6 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-200"
              >
                <NavigationIcon class="h-5 w-5" />
                <span>Моё местоположение</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Address Details Form -->
        <div class="p-6 md:p-8 border-t border-gray-200/30">
          <h3
            class="text-xl font-semibold text-gray-800 mb-6 flex items-center space-x-2"
          >
            <HomeIcon class="h-5 w-5 text-blue-500" />
            <span>Детали адреса</span>
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="space-y-2">
              <label
                class="text-sm font-medium text-gray-700 flex items-center space-x-1"
              >
                <BuildingIcon class="h-4 w-4 text-gray-500" />
                <span>Подьезд</span>
              </label>
              <input
                v-model="entrance"
                placeholder="Номер подьезда"
                class="w-full p-3 bg-gray-50/80 border border-gray-200/50 rounded-xl text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-3 focus:ring-blue-500/20 focus:border-blue-500/50 transition-all duration-200"
              />
            </div>
            <div class="space-y-2">
              <label
                class="text-sm font-medium text-gray-700 flex items-center space-x-1"
              >
                <MapPinIcon class="h-4 w-4 text-gray-500" />
                <span>Этаж</span>
              </label>
              <input
                v-model="floor"
                placeholder="Этаж"
                class="w-full p-3 bg-gray-50/80 border border-gray-200/50 rounded-xl text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-3 focus:ring-blue-500/20 focus:border-blue-500/50 transition-all duration-200"
              />
            </div>

            <div class="space-y-2">
              <label
                class="text-sm font-medium text-gray-700 flex items-center space-x-1"
              >
                <KeyIcon class="h-4 w-4 text-gray-500" />
                <span>Квартира</span>
              </label>
              <input
                v-model="apartment"
                placeholder="Номер квартиры"
                class="w-full p-3 bg-gray-50/80 border border-gray-200/50 rounded-xl text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-3 focus:ring-blue-500/20 focus:border-blue-500/50 transition-all duration-200"
              />
            </div>
          </div>
        </div>
        <div
          class="p-6 md:p-8 bg-gradient-to-r from-cyan-500/5 to-blue-500/5 border-t border-gray-200/30"
        >
          <button
            @click="sendAddress"
            :class="[
              'w-full flex items-center justify-center  space-x-3 font-semibold py-4 px-8 max-[650px]:py-2 max-[650px]:px-4  rounded-2xl shadow-xl transform transition-all duration-300 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white hover:scale-[1.02] hover:shadow-2xl',
            ]"
          >

            <span class="text-lg max-[650px]:text-[12px]">Подтвердить адрес</span>
          </button>
        </div>
        <!-- Map Section -->
        <div class="p-6 md:p-8 bg-gradient-to-b from-gray-50/30 to-gray-100/30">
          <h3
            class="text-xl font-semibold text-gray-800 mb-6 flex items-center space-x-2"
          >
            <MapIcon class="h-5 w-5 text-blue-500" />
            <span>Карта</span>
          </h3>

          <div class="relative">
            <div
              id="map"
              class="h-96 md:h-[500px] w-full rounded-2xl shadow-2xl border-4 border-white/50 overflow-hidden"
            />

            <!-- Map Overlay Controls -->
            <div class="absolute top-4 right-4 space-y-2">
              <button
                class="bg-white/90 backdrop-blur-sm p-3 rounded-xl shadow-lg hover:bg-white transition-all duration-200"
              >
                <PlusIcon class="h-5 w-5 text-gray-600" />
              </button>
              <button
                class="bg-white/90 backdrop-blur-sm p-3 rounded-xl shadow-lg hover:bg-white transition-all duration-200"
              >
                <MinusIcon class="h-5 w-5 text-gray-600" />
              </button>
            </div>
          </div>
        </div>

        <!-- Submit Button -->
      </div>

      <!-- Success Message -->
      <div
        v-if="showSuccess"
        class="fixed top-4 right-4 bg-green-500 text-white px-6 py-4 rounded-2xl shadow-2xl transform transition-all duration-500 z-50"
      >
        <div class="flex items-center space-x-2">
          <CheckCircleIcon class="h-5 w-5" />
          <span>Адрес успешно сохранен!</span>
        </div>
      </div>
      <CustomModal v-if="succesModal">
              <div
                class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center"
              >
                <img
                  src="/sucsess-modal.svg"
                  alt="Успешно"
                  class="w-16 h-16 mx-auto mb-4"
                />
                <h3 class="text-xl font-semibold text-black mb-2">
                  Ваш адрес добавлен!
                </h3>
                <p class="text-black mb-4">Можете делать заказы!</p>
                <button
                  @click="succesModal = false"
                  class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold"
                >
                  Закрыть
                </button>
              </div>
            </CustomModal>
            <CustomModal v-if="failModal">
              <div
                class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center"
              >
                <img
                  src="/fail-modal.svg"
                  alt="Успешно"
                  class="w-16 h-16 mx-auto mb-4"
                />
                <h3 class="text-xl font-semibold text-black mb-2">
                  Ваш адрес не добавлен!
                </h3>
                <p class="text-black mb-4">Повторите попытку позже!</p>
                <button
                  @click="failModal = false"
                  class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold"
                >
                  Закрыть
                </button>
              </div>
            </CustomModal>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import L from "leaflet";
import CustomModal from "@/components/CustomModal.vue";
import { useAutoClose } from '@/stores/useAutoClose'

const suggestions = ref([]);

const succesModal = ref(false);
const failModal = ref(false);
const props = defineProps({
  address: String,
  entrance: [String, Number], // Позволяем и строку, и число
  apartment: [String, Number],
  floor: [String, Number]
});

// Эмиттер
// const emit = defineEmits(["update:address"]);

// Локальное состояние
const address = ref(props.address || "");
const entrance = ref(props.entrance || "");
const floor = ref(props.floor || "")
const apartment = ref(props.apartment || "");
// Следим за внешними изменениями
watch(
  () => props.address,
  (val) => {
    address.value = val;
  }
);

// Эмитим наружу, когда address меняется внутри
watch(address, (val) => {
  emit("update:address", val);
});
// Предположим, сюда вы сохраняете ответ от сервера
const allAddresses = ref([]); 

const lastAddress = computed(() => {
  // Проверяем, что массив существует и в нем есть элементы
  if (!allAddresses.value || allAddresses.value.length === 0) return null;
  
  // Берем последний элемент массива
  return allAddresses.value[allAddresses.value.length - 1];
});
let map,
  marker,
  debounceTimer = null;

const allowedCities = ["Алматы", "Almaty", "Каскелен", "Kaskelen"];

const getCurrentLocation = () => {
  if (!navigator.geolocation) {
    alert("Геолокация не поддерживается браузером");
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const { latitude, longitude } = position.coords;

      if (marker) {
        marker.setLatLng([latitude, longitude]);
      } else {
        marker = L.marker([latitude, longitude]).addTo(map);
      }

      map.setView([latitude, longitude], 17); // Увеличил зум до 17 для точности

      // ВАЖНО: Добавлен addressdetails=1
      const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&addressdetails=1&accept-language=ru`;

      try {
        const res = await fetch(url);
        const data = await res.json();
        
        const isAllowed = allowedCities.some((city) =>
          data.display_name.includes(city)
        );

        if (!isAllowed) {
          address.value = "";
          alert("Этот город недоступен для выбора");
          return;
        }

        // ЛОГИКА СБОРКИ АДРЕСА:
        // ЛОГИКА СБОРКИ АДРЕСА:
        const addr = data.address;
        const street = addr.road || addr.pedestrian || addr.suburb || "";
        const house = addr.house_number || "";
        const city = addr.city || addr.town || addr.village || "Каскелен";

        if (street) {
          // Если есть улица, пишем "Улица, номер, Город"
          address.value = house ? `${street}, ${house}, ${city}` : `${street}, ${city}`;
        } else {
          // Если кликнули в поле или на здание без улицы, берем первые 2 значимые части
          // Это уберет индекс, область и страну
          address.value = data.display_name.split(',').slice(0, 2).join(', ');
        }

      } catch (err) {
        console.error(err);
        address.value = "Ошибка при получении адреса";
      }
    },
    (err) => {
      console.error(err);
      alert("Не удалось получить геопозицию");
    }
  );
};
const sendAddress = async () => {
  const payload = {
    address: address.value,
    entrance: entrance.value,
    floor: floor.value,
    apartment: apartment.value,
  };

  try {
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}addresses/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (response.ok) {
      console.log("✅ Адрес отправлен:", data);
      succesModal.value = true;
    } else {
      console.error("❌ Ошибка:", data);
      failModal.value = true;
    }
  } catch (err) {
    console.error("❌ Ошибка сети:", err);
    failModal.value = true;
  }
};

onMounted(() => {
  console.log(address, 'adres')
    console.log(entrance, 'entr')

  map = L.map("map", {
    maxBounds: [
      [40.0, 66.0],
      [56.0, 87.0],
    ],
    maxBoundsViscosity: 1.0,
    minZoom: 5,
    maxZoom: 18,
  }).setView([43.25, 76.95], 12);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
  }).addTo(map);

  map.on("click", async (e) => {
    const { lat, lng } = e.latlng;

    if (marker) {
      marker.setLatLng([lat, lng]);
    } else {
      marker = L.marker([lat, lng]).addTo(map);
    }

    // ВАЖНО: Добавлен addressdetails=1
    const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&addressdetails=1&accept-language=ru`;

    try {
      const res = await fetch(url);
      const data = await res.json();
      
      const isAllowed = allowedCities.some((city) =>
        data.display_name.includes(city)
      );

      if (!isAllowed) {
        address.value = "";
        alert("Этот город недоступен для выбора");
        return;
      }

      // ЛОГИКА СБОРКИ АДРЕСА:
      const addr = data.address;
      const street = addr.road || addr.pedestrian || addr.suburb || "";
      const house = addr.house_number || "";

      if (street) {
        address.value = house ? `${street}, ${house}` : street;
      } else {
        // Если улица не определена, берем первую значимую часть
        address.value = data.display_name.split(',')[0];
      }
      
    } catch (err) {
      console.error(err);
      address.value = "Ошибка при получении адреса";
    }
  });
  getSavedAddresses();
});

const searchAddress = async () => {
  if (!address.value) return;

  const query = encodeURIComponent(address.value);
  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${query}&accept-language=ru`;

  try {
    const response = await fetch(url);
    const data = await response.json();

    if (data && data.length > 0) {
      const result = data[0];
      const displayName = result.display_name || "";

      const isAllowed = allowedCities.some((city) =>
        displayName.includes(city)
      );
      if (!isAllowed) {
        alert("Этот город недоступен для выбора");
        return;
      }

      const latNum = parseFloat(result.lat);
      const lonNum = parseFloat(result.lon);

      map.setView([latNum, lonNum], 15);

      if (marker) {
        marker.setLatLng([latNum, lonNum]);
      } else {
        marker = L.marker([latNum, lonNum]).addTo(map);
      }
    } else {
      alert("Адрес не найден");
    }
  } catch (err) {
    alert("Ошибка при поиске адреса");
    console.error(err);
  }
};
// Добавьте это в script setup
const getSavedAddresses = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}addresses/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
      },
    });
    const data = await response.json();
    allAddresses.value = data;

    // Если есть адреса, берем последний и записываем в инпут
    if (data.length > 0) {
      const last = data[data.length - 1];
      address.value = last.address; // Вот здесь мы наполняем v-model
      
      // Наполняем остальные поля, если они объявлены
      if (typeof entrance !== 'undefined') entrance.value = last.entrance || "";
      if (typeof floor !== 'undefined') floor.value = last.floor || "";
      if (typeof apartment !== 'undefined') apartment.value = last.apartment || "";
      
      // Двигаем карту к этому адресу
      searchAddress();
    }
  } catch (err) {
    console.error("Ошибка загрузки адресов:", err);
  }
};


const fetchSuggestions = () => {
  if (debounceTimer) clearTimeout(debounceTimer);

  if (address.value.length < 3) {
    suggestions.value = [];
    return;
  }

  debounceTimer = setTimeout(async () => {
    const query = encodeURIComponent(address.value);
    const url = `https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&q=${query}&accept-language=ru`;

    try {
      const res = await fetch(url);
      const data = await res.json();

      suggestions.value = data.filter((item) =>
        allowedCities.some((city) => item.display_name.includes(city))
      );
    } catch (err) {
      console.error(err);
    }
  }, 500);
};

const selectSuggestion = (item) => {
  address.value = item.display_name;
  suggestions.value = [];

  const lat = parseFloat(item.lat);
  const lon = parseFloat(item.lon);

  map.setView([lat, lon], 15);

  if (marker) {
    marker.setLatLng([lat, lon]);
  } else {
    marker = L.marker([lat, lon]).addTo(map);
  }
};
// Следим за изменениями пропсов из родителя (Main.vue)
// const props = defineProps({
//   address: String,
//   entrance: [String, Number], 
//   apartment: [String, Number],
//   floor: [String, Number]
// });

// 1. Добавляем все необходимые эмиты
const emit = defineEmits([
  "update:address", 
  "update:entrance", 
  "update:apartment", 
  "update:floor"
]);

// Локальное состояние
// const address = ref(props.address || "");
// const entrance = ref(props.entrance || "");
// const floor = ref(props.floor || "");
// const apartment = ref(props.apartment || "");

// --- СИНХРОНИЗАЦИЯ: Из родителя в Map (когда открываем модалку) ---
watch(() => props.address, (val) => address.value = val);
watch(() => props.entrance, (val) => entrance.value = val);
watch(() => props.floor, (val) => floor.value = val);
watch(() => props.apartment, (val) => apartment.value = val);

// --- СИНХРОНИЗАЦИЯ: Из Map в родителя (когда пишем в инпуты) ---
watch(address, (val) => emit("update:address", val));
watch(entrance, (val) => emit("update:entrance", val));
watch(floor, (val) => emit("update:floor", val));
watch(apartment, (val) => emit("update:apartment", val));
useAutoClose(succesModal, 2000)
useAutoClose(failModal, 2500)

</script>

<style scoped>
#map {
  min-height: 400px;
}
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: rgba(59, 130, 246, 0.3);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(59, 130, 246, 0.5);
}

/* Smooth animations */
* {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Backdrop blur support */
.backdrop-blur-xl {
  backdrop-filter: blur(20px);
}

.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
</style>
