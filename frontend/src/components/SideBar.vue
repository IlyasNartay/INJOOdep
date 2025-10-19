<template>
  <div class="flex relative">
    <!-- Overlay (optional) -->
    <div
      v-if="!isCollapsed"
      class="fixed inset-0 bg-black/40 z-30"
      @click="toggleSidebar"
    ></div>

    <!-- Sidebar -->
    <aside
      :class="[
        'bg-gray-800 text-white fixed top-0 left-0 h-full z-40 transition-all duration-300 ease-in-out',
        isCollapsed ? '-translate-x-full' : 'translate-x-0',
      ]"
      class="w-64 p-4"
    >
      <!-- Toggle Button (показать только внутри сайдбара) -->
      <button
        @click="toggleSidebar"
        class="absolute -right-4 top-16 bg-gray-700 text-white rounded-full p-1 shadow z-50"
      >
        <svg
          v-if="!isCollapsed"
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>

      <!-- Logo -->
      <div class="text-2xl font-bold mb-6">🧋 Injoo</div>

      <!-- Menu -->
      <component
        v-for="(item, index) in filteredMenu"
        :key="index"
        :is="item.label === 'Выход' ? 'button' : RouterLink"
        :to="item.label === 'Выход' ? undefined : item.to"
        @click="item.label === 'Выход' && logout()"
        class="hover:bg-gray-700 px-3 py-2 rounded cursor-pointer flex items-center space-x-2 w-full text-left"
      >
        <span class="w-8 h-8 bg-white/20 rounded-full flex justify-center items-center">
          <Icon :icon="item.icon" class="w-[20px] h-[20px]" />
        </span>
        <span>{{ item.label }}</span>
      </component>
    </aside>

    <!-- Main content -->
    <div class="w-full">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { Icon } from "@iconify/vue";
const userRole = ref("guest");
const router = useRouter();
onMounted(() => {
  const savedRole = localStorage.getItem("userRole") || "guest";
  userRole.value = savedRole;
});

// Состояние сайдбара
const isCollapsed = ref(false);
function toggleSidebar() {
  isCollapsed.value = !isCollapsed.value
}

// Все пункты меню + маршруты
const menuItems = computed(() => [
  {
    label: "Главная",
    to: userRole.value === "guest" ? "/guest/order" : "/CliMain",
    roles: ["admin", "customer", "guest"],
    icon: "line-md:home-md",
  },
  { label: "Добавить блюда", to: "/adddishes", roles: ["admin", "manager"], icon: "line-md:document-add" },
  { label: "Сделать заказ", to: "/Basket", roles: ["customer", "guest"], icon: "line-md:document-list" },
  { label: "Мои заказы", to: "/myorder", roles: ["customer", "guest"], icon: "line-md:document-list" },
  { label: "Выход", to: "/", roles: ["admin", "manager", "customer", "guest"], icon: "line-md:clipboard-arrow" },
]);
const logout = () => {
  localStorage.removeItem("authToken"); // или как он у тебя называется
  localStorage.removeItem("userRole"); // если ты сохраняешь роль
  router.push("/"); // редирект на главную или на login
};
const filteredMenu = computed(() =>
  menuItems.value.filter((item) => item.roles.includes(userRole.value))
);
</script>
