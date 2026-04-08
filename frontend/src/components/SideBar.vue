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
      <!-- Toggle button inside the sidebar -->
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
      <div class="text-2xl font-bold mb-6">INJOO</div>

      <!-- Menu -->
      <component
        v-for="(item, index) in filteredMenu"
        :key="index"
        :is="item.action === 'logout' ? 'button' : RouterLink"
        :to="item.action === 'logout' ? undefined : item.to"
        @click="item.action === 'logout' && logout()"
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
import { computed, ref, watch } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";
import { Icon } from "@iconify/vue";
import { t } from "@/i18n";
import { ADMIN_ROLES, ADMIN_STAFF_ROLES, AUTH_USER_ROLES, CUSTOMER_ROLES, SESSION_MODES, clearAuthStorage, currentSessionMode, currentUserRole, setSessionMode } from "@/utils/roles";

const userRole = currentUserRole;
const sessionMode = currentSessionMode;
const route = useRoute();
const router = useRouter();

watch(
  () => route.path,
  (path) => {
    setSessionMode(path.startsWith("/guest") ? SESSION_MODES.GUEST : SESSION_MODES.AUTH);
  },
  { immediate: true }
);

// Состояние сайдбара
const isCollapsed = ref(false);
function toggleSidebar() {
  isCollapsed.value = !isCollapsed.value;
}

// Все пункты меню + маршруты
const menuItems = computed(() => [
  {
    label: t("common.home"),
    to: sessionMode.value === SESSION_MODES.GUEST ? "/guest/order" : "/customer/main",
    roles: AUTH_USER_ROLES,
    modes: [SESSION_MODES.GUEST, SESSION_MODES.AUTH],
    icon: "line-md:home-md",
  },
  { label: t("common.statistics"), to: "/admin/stats", roles: ADMIN_ROLES, icon: "line-md:chart-bar" },
  { label: t("common.users"), to: "/admin/users", roles: ADMIN_ROLES, icon: "line-md:account" },
  { label: t("common.addDishes"), to: "/admin/adddishes", roles: ADMIN_STAFF_ROLES, icon: "line-md:document-add" },
  { label: t("common.makeOrder"), to: "/customer/basket", roles: CUSTOMER_ROLES, modes: [SESSION_MODES.GUEST], icon: "line-md:document-list" },
  { label: t("common.myOrders"), to: "/customer/myorder", roles: CUSTOMER_ROLES, icon: "line-md:document-list" },
  { label: t("common.logout"), to: "/", roles: AUTH_USER_ROLES, modes: [SESSION_MODES.GUEST], icon: "line-md:clipboard-arrow", action: "logout" },
]);
const logout = () => {
  clearAuthStorage();
  router.push("/");
};
const filteredMenu = computed(() =>
  menuItems.value.filter((item) => {
    const roleAllowed = item.roles.includes(userRole.value);
    const modeAllowed = item.modes ? item.modes.includes(sessionMode.value) : false;
    return roleAllowed || modeAllowed;
  })
);
</script>

