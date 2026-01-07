<template>
  <div
    class="min-h-screen overflow-y-auto bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-100 py-6 px-4"
  >
    <div class="max-w-4xl mx-auto space-y-6">

      <!-- Header -->
      <div class="text-center space-y-2">
        <h1
          class="text-3xl md:text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"
        >
          Выберите адрес
        </h1>
        <p class="text-gray-600 text-lg">
          Нажмите на карту или используйте геолокацию
        </p>
      </div>

      <!-- Main Card -->
      <div
        class="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 overflow-hidden"
      >
        <!-- Controls -->
        <div class="p-6 flex flex-col sm:flex-row gap-3">
          <button
            @click="getCurrentLocation"
            class="flex-1 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-semibold py-3 rounded-xl shadow-lg transition"
          >
            Моё местоположение
          </button>

          <button
            @click="openConfirm"
            :disabled="!address"
            class="flex-1 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white font-semibold py-3 rounded-xl shadow-lg transition disabled:opacity-50"
          >
            Подтвердить адрес
          </button>
        </div>

        <!-- Address input -->
        <div class="px-6 pb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Адрес (можно исправить вручную)
          </label>
          <input
            v-model="address"
            placeholder="Улица, дом"
            class="w-full p-4 rounded-2xl border border-gray-200 bg-white/80 focus:outline-none focus:ring-4 focus:ring-blue-500/20 transition"
          />
        </div>

        <!-- Map -->
        <div class="p-6">
          <div
            id="yandex-map"
            class="h-[450px] w-full rounded-2xl shadow-xl border border-white"
          ></div>
        </div>
      </div>
    </div>

    <!-- CONFIRM MODAL -->
    <div
      v-if="confirmModal"
      class="fixed inset-0 z-50 flex items-center justify-center"
    >
      <div class="absolute inset-0 bg-black/40 backdrop-blur-sm"></div>

      <div
        class="relative z-10 bg-white rounded-2xl p-6 w-[90%] max-w-md shadow-2xl"
      >
        <h3 class="text-xl font-semibold text-gray-800 mb-2">
          Проверьте адрес
        </h3>
        <p class="text-gray-700 mb-6">{{ address }}</p>

        <div class="flex gap-3">
          <button
            @click="closeConfirm"
            class="flex-1 py-2 rounded-xl bg-gray-100 hover:bg-gray-200 transition"
          >
            Отмена
          </button>
          <button
            @click="sendAddress"
            class="flex-1 py-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700 transition"
          >
            Подтвердить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const address = ref("");
const confirmModal = ref(false);

let map = null;
let placemark = null;

const ALLOWED_CITIES = ["Каскелен", "Kaskelen"];

/* =======================
   Scroll lock helpers
======================= */
const lockBody = () => {
  document.body.style.overflow = "hidden";
};
const unlockBody = () => {
  document.body.style.overflow = "";
};

/* =======================
   Modal controls
======================= */
const openConfirm = () => {
  confirmModal.value = true;
  lockBody();
};

const closeConfirm = () => {
  confirmModal.value = false;
  unlockBody();
};

/* =======================
   Yandex Maps
======================= */
const loadYandexMap = () => {
  if (window.ymaps) return initMap();

  const script = document.createElement("script");
  script.src = "https://api-maps.yandex.ru/2.1/?lang=ru_RU";
  script.onload = initMap;
  document.head.appendChild(script);
};

const initMap = () => {
  window.ymaps.ready(() => {
    map = new window.ymaps.Map("yandex-map", {
      center: [43.2004, 76.6213], // Каскелен
      zoom: 13,
      controls: ["zoomControl"],
    });

    map.events.add("click", async (e) => {
      const coords = e.get("coords");
      await handlePoint(coords);
    });
  });
};

const handlePoint = async (coords) => {
  const res = await window.ymaps.geocode(coords, { results: 1 });
  const geo = res.geoObjects.get(0);
  if (!geo) return;

  const city =
    geo.getLocalities()?.[0] ||
    geo.getAdministrativeAreas()?.[0] ||
    "";

  if (!ALLOWED_CITIES.includes(city)) {
    alert("Можно выбрать адрес только в Каскелене");
    return;
  }

  const street = geo.getThoroughfare() || "";
  const house = geo.getPremiseNumber() || "";

  address.value = street
    ? house
      ? `${street}, ${house}`
      : street
    : geo.getAddressLine();

  if (!placemark) {
    placemark = new window.ymaps.Placemark(
      coords,
      {},
      { draggable: true }
    );
    placemark.events.add("dragend", async () => {
      const newCoords = placemark.geometry.getCoordinates();
      await handlePoint(newCoords);
    });
    map.geoObjects.add(placemark);
  } else {
    placemark.geometry.setCoordinates(coords);
  }
};

const getCurrentLocation = () => {
  if (!navigator.geolocation) {
    alert("Геолокация не поддерживается");
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async (pos) => {
      const coords = [pos.coords.latitude, pos.coords.longitude];
      map.setCenter(coords, 17, { duration: 300 });
      await handlePoint(coords);
    },
    () => alert("Не удалось получить местоположение")
  );
};

/* =======================
   Send to backend
======================= */
const sendAddress = async () => {
  try {
    const res = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}addresses/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("authToken")}`,
          },
          body: JSON.stringify({address: address.value}),
        }
    );

    if (res.ok) {
      alert("Адрес сохранён");
      closeConfirm();
    } else {
      alert("Ошибка сохранения адреса");
    }
  } catch (e) {
    console.error(e);
    alert("Ошибка сети");
  }
};

onMounted(loadYandexMap);
</script>

<style scoped>
#yandex-map {
  min-height: 400px;
}
</style>
