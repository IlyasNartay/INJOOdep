<template>
  <div
    class="min-h-screen bg-gradient-to-br from-rose-200 via-rose-300 to-rose-400 relative overflow-hidden"
  >
    <!-- Background Bubble Decorations -->
    <div class="absolute inset-0 opacity-10">
      <div
        class="absolute top-10 left-10 w-20 h-20 border-4 border-white rounded-full"
      ></div>
      <div
        class="absolute top-32 left-32 w-16 h-16 border-4 border-white rounded-full"
      ></div>
      <div
        class="absolute top-20 right-20 w-24 h-24 border-4 border-white rounded-full"
      ></div>
      <div
        class="absolute bottom-20 left-20 w-18 h-18 border-4 border-white rounded-full"
      ></div>
      <div
        class="absolute bottom-32 right-32 w-22 h-22 border-4 border-white rounded-full"
      ></div>
    </div>

    <div class="relative z-10 px-4 py-8">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-6xl font-bold text-gray-900 mb-2">tea</h1>
        <div class="text-right">
          <span class="text-5xl font-bold text-pink-500">injoo</span>
          <div class="text-lg text-gray-600">bubble tea</div>
        </div>
      </div>

      <!-- Pearl Tea Section -->
      <div class="mb-12">
        <div
          class="bg-orange-400 text-white text-center py-3 rounded-full mb-8 max-w-md mx-auto"
        >
          <h2 class="text-xl font-semibold">с жемчугом</h2>
        </div>

        <div
          class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6 max-w-7xl mx-auto"
        >
          <div
            v-for="drink in pearlTeas"
            :key="drink.id"
            class="text-center"
            @click="router.push('/auth')"
          >
            <div class="mb-4">
              <img
                :src="drink.image"
                :alt="drink.name"
                class="w-40 h-[180px] mx-auto object-cover rounded-lg"
              />
            </div>
            <h3 class="font-semibold text-gray-900 mb-2">{{ drink.name }}</h3>
            <p class="text-sm text-gray-700 mb-3 px-2">
              {{ drink.description }}
            </p>
            <div class="flex justify-center space-x-2">
              <span
                class="bg-orange-300 text-gray-900 px-3 py-1 rounded-full text-sm"
                >{{ drink.price1 }}</span
              >
              <span
                class="bg-purple-400 text-white px-3 py-1 rounded-full text-sm"
                >{{ drink.price2 }}</span
              >
            </div>
          </div>
        </div>
      </div>

      <!-- Fruit Tea Section -->
      <div class="mb-12">
        <div
          class="bg-orange-500 text-white text-center py-3 rounded-full mb-8 max-w-md mx-auto"
        >
          <h2 class="text-xl font-semibold">фруктовый</h2>
        </div>

        <div
          class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6 max-w-7xl mx-auto"
        >
          <div
            v-for="drink in fruitTeas"
            :key="drink.id"
            class="text-center"
            @click="router.push('/auth')"
          >
            <div class="mb-4">
              <img
                :src="drink.image"
                :alt="drink.name"
                class="w-40 h-40 mx-auto object-cover rounded-lg"
              />
            </div>
            <h3 class="font-semibold text-gray-900 mb-2">{{ drink.name }}</h3>
            <p class="text-sm text-gray-700 mb-3 px-2">
              {{ drink.description }}
            </p>
            <div class="flex justify-center space-x-2">
              <span
                class="bg-orange-300 text-gray-900 px-3 py-1 rounded-full text-sm"
                >{{ drink.price1 }}</span
              >
              <span
                class="bg-purple-400 text-white px-3 py-1 rounded-full text-sm"
                >{{ drink.price2 }}</span
              >
            </div>
          </div>
        </div>
      </div>

      <!-- Milkshake Section -->
      <div class="mb-12">
        <div
          class="bg-yellow-500 text-white text-center py-3 rounded-full mb-8 max-w-md mx-auto"
        >
          <h2 class="text-xl font-semibold">милкшейк</h2>
        </div>

        <div
          class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6 max-w-7xl mx-auto"
        >
          <div
            v-for="drink in milkshakes"
            :key="drink.id"
            class="text-center"
            @click="router.push('/auth')"
          >
            <div class="mb-4 flex justify-center">
              <img
                :src="drink.image"
                :alt="drink.name"
                class="w-40 h-40 mx-auto object-cover rounded-lg"
              />
            </div>
            <h3 class="font-semibold text-gray-900 mb-2">{{ drink.name }}</h3>
            <p class="text-sm text-gray-700 mb-3 px-2">
              {{ drink.description }}
            </p>
            <div class="flex justify-center space-x-2">
              <span
                class="bg-orange-300 text-gray-900 px-3 py-1 rounded-full text-sm"
                >{{ drink.price1 }}</span
              >
              <span
                class="bg-purple-400 text-white px-3 py-1 rounded-full text-sm"
                >{{ drink.price2 }}</span
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

import { ref } from "vue";
const router = useRouter();

const pearlTeas = ref([
  {
    id: 1,
    name: "Матча зеленый",
    description: "Матча чай, молоко, сахарный сироп, лед, жемчуг",
    price1: "1700",
    price2: "1800",
    image: "/Green-Matcha-removebg-preview.png",
  },
  {
    id: 2,
    name: "Тайский чай с тапиокой",
    description: "Тайский чай, молоко, тростниковый сахар",
    price1: "1600",
    price2: "1800",
    image: "/Thai-tea-removebg-preview.png",
  },
  {
    id: 3,
    name: "Молочный чай с тапиокой",
    description: "Черный чай, молоко, сахарный сироп, лед, жемчуг",
    price1: "1400",
    price2: "1700",
    image: "/Milk-tea-removebg-preview.png",
  },
  {
    id: 4,
    name: "Орео",
    description: "Орео молоко, лед, карамельная шапка",
    price1: "1600",
    price2: "1800",
    image: "/Oreo-removebg-preview.png",
  },
  {
    id: 5,
    name: "Сливочный Улун",
    description: "Чай улун, молоко, сахарный сироп, лед, жемчуг",
    price1: "1400",
    price2: "1600",
    image: "/Sliv-Ulun-removebg-preview.png",
  },
]);

const fruitTeas = ref([
  {
    id: 6,
    name: "Чай с ананасом",
    description: "Зеленый чай, лед, ананас, лимон, лайм, сахарный сироп, лед",
    price1: "1400",
    price2: "1700",
    image: "/Pinapple-tea-removebg-preview.png",
  },
  {
    id: 7,
    name: "Чай с апельсином",
    description: "Зеленый чай, апельсин, лимон, лайм, сахарный сироп, лед",
    price1: "1400",
    price2: "1700",
    image: "/Orange-tea-removebg-preview.png",
  },
  {
    id: 8,
    name: "Чай с лаймом",
    description: "Зеленый чай, лайм, лайм, сахарный сироп, лед",
    price1: "1400",
    price2: "1700",
    image: "/Lime-tea-removebg-preview.png",
  },
  {
    id: 9,
    name: "Чай с клубникой",
    description: "Зеленый чай, клубника, лимон, лайм, сахарный сироп, лед",
    price1: "1400",
    price2: "1700",
    image: "/Strawberry-tea-removebg-preview.png",
  },
  {
    id: 10,
    name: "Чай с малиной",
    description: "Зеленый чай, малина, лимон, лайм, сахарный сироп, лед",
    price1: "1400",
    price2: "1700",
    image: "/Malina-tea-removebg-preview.png",
  },
]);

const milkshakes = ref([
  {
    id: 11,
    name: "Молочный манго",
    description: "Манго, молоко, лед, шапка",
    price1: "1600",
    price2: "1800", 
    image: "/Milk-mago-removebg-preview.png",
  },
  {
    id: 12,
    name: "Горячий матча латте",
    description: "",
    price1: "1700",
    price2: "1900",
    image: "/Matcha-Latte-removebg-preview.png",
  },
  {
    id: 13,
    name: "Смузи Манго",
    description: "Манго, молоко, молоко, сахарный сироп, лед",
    price1: "1600",
    price2: "1800",
    image: "/Mango-removebg-preview.png",
  },
  {
    id: 14,
    name: "Фреш с ананасом",
    description: "Зеленый чай, ананас, лед",
    price1: "1600",
    price2: "1800",
    image: "/Pineapple-fresh-removebg-preview.png",
  },
  {
    id: 15,
    name: "Клубничный смузи с сырной шапкой",
    description: "Клубника, лед, молоко, сырная шапка",
    price1: "1600",
    price2: "1800",
    image: "/Strawberry-removebg-preview.png",
  },
  {
    id: 16,
    name: "Фрапучино шоколадный",
    description: "",
    price1: "1600",
    price2: "1800",
    image: "/Frapuchino-chocco-removebg-preview.png",
  },
  {
    id: 17,
    name: "Малиновый смузи с сырной шапкой",
    description: "Малина, лед, молоко, сырная шапка",
    price1: "1400",
    price2: "1800",
    image: "/Malina-removebg-preview.png",
  },
]);
</script>

<style scoped>
/* Additional custom styles if needed */
</style>
