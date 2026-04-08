<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-cyan-950 text-white">
    <div class="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
      <div class="mb-8 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p class="text-cyan-300 uppercase tracking-[0.35em] text-xs mb-3">User management</p>
          <h1 class="text-3xl sm:text-4xl font-bold">Пользователи</h1>
          <p class="text-white/70 mt-3 max-w-2xl">
            Поиск, фильтры, блокировка, смена роли и подробная карточка пользователя с заказами.
          </p>
        </div>

        <div class="grid gap-3 rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur sm:grid-cols-2 xl:grid-cols-4">
          <label class="field">
            <span>Поиск</span>
            <input v-model="searchInput" @keyup.enter="applyFilters" type="text" class="input" placeholder="Имя или телефон" />
          </label>
          <label class="field">
            <span>Роль</span>
            <select v-model="roleFilter" class="input">
              <option value="">Все роли</option>
              <option v-for="option in roleOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </label>
          <label class="field">
            <span>Статус</span>
            <select v-model="statusFilter" class="input">
              <option value="">Все статусы</option>
              <option v-for="option in statusOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </label>
          <button @click="applyFilters" class="self-end rounded-xl bg-cyan-400 px-4 py-3 font-semibold text-slate-950 hover:bg-cyan-300 transition">
            Применить
          </button>
        </div>
      </div>

      <div v-if="isLoading" class="py-20 text-center text-white/70">
        Загрузка пользователей...
      </div>

      <div v-else class="rounded-3xl border border-white/10 bg-white/5 shadow-2xl backdrop-blur overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full text-left">
            <thead class="bg-white/5 text-white/70 text-sm uppercase tracking-wider">
              <tr>
                <th class="px-4 py-4">Пользователь</th>
                <th class="px-4 py-4">Роль</th>
                <th class="px-4 py-4">Статус</th>
                <th class="px-4 py-4">Заказы</th>
                <th class="px-4 py-4">Сумма</th>
                <th class="px-4 py-4">Создан</th>
                <th class="px-4 py-4 text-right">Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="user in users"
                :key="user.id"
                class="border-t border-white/8 hover:bg-white/5 cursor-pointer"
                @click="openDetails(user.id)"
              >
                <td class="px-4 py-4">
                  <div>
                    <p class="font-semibold">{{ user.full_name || 'Без имени' }}</p>
                    <p class="text-sm text-white/55">{{ user.phone }}</p>
                  </div>
                </td>
                <td class="px-4 py-4">
                  <select
                    class="select"
                    :value="user.role"
                    @click.stop
                    @change="onRoleChange(user, $event)"
                  >
                    <option v-for="option in roleOptions" :key="option.value" :value="option.value">
                      {{ option.label }}
                    </option>
                  </select>
                </td>
                <td class="px-4 py-4">
                  <span class="badge" :class="statusClass(user.status)">
                    {{ statusLabel(user.status) }}
                  </span>
                </td>
                <td class="px-4 py-4">{{ user.orders_count }}</td>
                <td class="px-4 py-4">{{ formatMoney(user.total_spent) }}</td>
                <td class="px-4 py-4 text-sm text-white/65">{{ formatDate(user.created_at) }}</td>
                <td class="px-4 py-4">
                  <div class="flex items-center justify-end gap-2">
                    <button
                      @click.stop="toggleStatus(user)"
                      class="rounded-xl px-3 py-2 text-sm font-semibold transition"
                      :class="user.status === 'blocked'
                        ? 'bg-emerald-400/15 text-emerald-200 hover:bg-emerald-400/25'
                        : 'bg-rose-400/15 text-rose-200 hover:bg-rose-400/25'"
                    >
                      {{ user.status === 'blocked' ? 'Разблок.' : 'Заблок.' }}
                    </button>
                    <button
                      @click.stop="openDetails(user.id)"
                      class="rounded-xl bg-white/10 px-3 py-2 text-sm font-semibold hover:bg-white/15 transition"
                    >
                      Детали
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="!users.length">
                <td colspan="7" class="px-4 py-16 text-center text-white/55">
                  Пользователи не найдены
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="flex flex-col gap-4 border-t border-white/10 px-4 py-4 sm:flex-row sm:items-center sm:justify-between">
          <p class="text-sm text-white/60">
            Всего: {{ total }} | Страница {{ page }} из {{ pages }}
          </p>
          <div class="flex flex-wrap items-center gap-2">
            <button class="pager" :disabled="page === 1" @click="goToPage(page - 1)">Назад</button>
            <button
              v-for="p in pageButtons"
              :key="p"
              class="pager"
              :class="p === page ? 'bg-cyan-400 text-slate-950 border-cyan-300' : ''"
              @click="goToPage(p)"
            >
              {{ p }}
            </button>
            <button class="pager" :disabled="page === pages" @click="goToPage(page + 1)">Вперёд</button>
          </div>
        </div>
      </div>

      <div class="mt-8 rounded-3xl border border-white/10 bg-white/5 shadow-2xl backdrop-blur overflow-hidden">
        <div class="flex items-center justify-between border-b border-white/10 px-4 py-4">
          <div>
            <h2 class="text-xl font-semibold">Telegram Users</h2>
            <p class="text-sm text-white/55">Управление ролями Telegram admin, kitchen и courier.</p>
          </div>
          <p class="text-sm text-white/60">Всего: {{ tgUsers.length }}</p>
        </div>

        <div class="overflow-x-auto">
          <table class="min-w-full text-left">
            <thead class="bg-white/5 text-white/70 text-sm uppercase tracking-wider">
              <tr>
                <th class="px-4 py-4">Chat ID</th>
                <th class="px-4 py-4">Роль</th>
                <th class="px-4 py-4">Создан</th>
                <th class="px-4 py-4 text-right">Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="tgUser in tgUsers" :key="tgUser.id" class="border-t border-white/8 hover:bg-white/5">
                <td class="px-4 py-4 font-medium">{{ tgUser.chat_id }}</td>
                <td class="px-4 py-4">
                  <select class="select" :value="tgUser.role" @change="onTelegramRoleChange(tgUser, $event)">
                    <option v-for="option in telegramRoleOptions" :key="option.value" :value="option.value">
                      {{ option.label }}
                    </option>
                  </select>
                </td>
                <td class="px-4 py-4 text-sm text-white/65">{{ formatDateTime(tgUser.created_at) }}</td>
                <td class="px-4 py-4">
                  <div class="flex justify-end">
                    <button
                      @click="deleteTelegramUser(tgUser)"
                      class="rounded-xl bg-rose-400/15 px-3 py-2 text-sm font-semibold text-rose-200 hover:bg-rose-400/25 transition"
                    >
                      Удалить
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="!tgUsers.length">
                <td colspan="4" class="px-4 py-12 text-center text-white/55">
                  Telegram users не найдены
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-if="detailsOpen" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm p-4" @click.self="closeDetails">
      <div class="mx-auto max-w-5xl rounded-3xl border border-white/10 bg-slate-950 text-white shadow-2xl overflow-hidden max-h-[90vh] flex flex-col">
        <div class="flex items-center justify-between border-b border-white/10 px-5 py-4">
          <div>
            <h2 class="text-2xl font-bold">{{ detail?.full_name || 'Пользователь' }}</h2>
            <p class="text-sm text-white/55">{{ detail?.phone }}</p>
          </div>
          <button class="rounded-xl bg-white/10 px-4 py-2 hover:bg-white/15 transition" @click="closeDetails">Закрыть</button>
        </div>

        <div class="flex-1 overflow-y-auto p-5">
          <div v-if="detailsLoading" class="py-20 text-center text-white/70">
            Загрузка деталей...
          </div>

          <div v-else-if="detail" class="space-y-6">
            <section class="grid gap-4 md:grid-cols-4">
              <article class="detail-card">
                <p class="detail-label">Роль</p>
                <p class="detail-value">{{ roleLabel(detail.role) }}</p>
              </article>
              <article class="detail-card">
                <p class="detail-label">Статус</p>
                <p class="detail-value">{{ statusLabel(detail.status) }}</p>
              </article>
              <article class="detail-card">
                <p class="detail-label">Заказы</p>
                <p class="detail-value">{{ detail.stats.total_orders }}</p>
              </article>
              <article class="detail-card">
                <p class="detail-label">Средний чек</p>
                <p class="detail-value">{{ formatMoney(detail.stats.avg_check) }}</p>
              </article>
            </section>

            <section class="grid gap-4 md:grid-cols-3">
              <article class="detail-card">
                <p class="detail-label">Всего потратил</p>
                <p class="detail-value">{{ formatMoney(detail.stats.total_spent) }}</p>
              </article>
              <article class="detail-card">
                <p class="detail-label">Создан</p>
                <p class="detail-value text-lg">{{ formatDate(detail.created_at) }}</p>
              </article>
              <article class="detail-card">
                <p class="detail-label">Последний заказ</p>
                <p class="detail-value text-lg">{{ formatDateTime(detail.stats.last_order_at) }}</p>
              </article>
            </section>

            <section>
              <div class="mb-4 flex items-center justify-between">
                <h3 class="text-xl font-semibold">Заказы</h3>
                <p class="text-sm text-white/55">{{ detail.orders.length }} записей</p>
              </div>

              <div v-if="!detail.orders.length" class="rounded-2xl border border-dashed border-white/10 p-8 text-center text-white/55">
                У пользователя нет заказов
              </div>

              <div v-else class="space-y-4">
                <article v-for="order in detail.orders" :key="order.id" class="rounded-2xl border border-white/10 bg-white/5 p-4">
                  <div class="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                    <div>
                      <p class="font-semibold">Заказ #{{ order.id }}</p>
                      <p class="text-sm text-white/55">{{ formatDateTime(order.rate_at) }}</p>
                    </div>
                    <div class="flex items-center gap-3">
                      <span class="badge" :class="statusClass(order.status)">{{ order.status }}</span>
                      <span class="font-semibold">{{ formatMoney(order.total_price) }}</span>
                    </div>
                  </div>

                  <div class="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
                    <div
                      v-for="item in order.order_dishes"
                      :key="`${order.id}-${item.dish.id}`"
                      class="rounded-xl bg-slate-950/70 p-3"
                    >
                      <p class="font-medium">{{ item.dish.name }}</p>
                      <p class="text-sm text-white/55">{{ item.quantity }} шт. · {{ formatMoney(item.dish.price) }}</p>
                    </div>
                  </div>
                </article>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { computed, onMounted, ref, watch } from "vue";
import { fetchAuthMeta, ROLE_OPTIONS, getRoleLabel } from "@/utils/roles";

const users = ref([]);
const tgUsers = ref([]);
const total = ref(0);
const page = ref(1);
const pages = ref(1);
const limit = 10;
const searchInput = ref("");
const search = ref("");
const roleFilter = ref("");
const statusFilter = ref("");
const isLoading = ref(false);

const detailsOpen = ref(false);
const detailsLoading = ref(false);
const detail = ref(null);
const roleOptions = ref([...ROLE_OPTIONS]);
const statusOptions = ref([
  { value: "active", label: "Активен" },
  { value: "blocked", label: "Заблокирован" },
]);
const telegramRoleOptions = [
  { value: "admin", label: "Админ" },
  { value: "kitchen", label: "Кухня" },
  { value: "courier", label: "Курьер" },
];

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    Authorization: `Bearer ${localStorage.getItem("authToken")}`,
    Accept: "application/json",
  },
});

const formatMoney = (value) =>
  new Intl.NumberFormat("ru-RU", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(Number(value || 0)) + " ₸";

const formatDate = (value) => {
  if (!value) return "-";
  return new Date(value).toLocaleDateString("ru-RU");
};

const formatDateTime = (value) => {
  if (!value) return "-";
  return new Date(value).toLocaleString("ru-RU");
};

const loadUsers = async () => {
  isLoading.value = true;
  try {
    const response = await api.get("admin/users", {
      params: {
        search: search.value || undefined,
        role: roleFilter.value || undefined,
        status: statusFilter.value || undefined,
        page: page.value,
        limit,
      },
    });
    users.value = response.data.items;
    total.value = response.data.total;
    page.value = response.data.page;
    pages.value = response.data.pages;
  } catch (error) {
    console.error("Не удалось загрузить пользователей", error);
  } finally {
    isLoading.value = false;
  }
};

const loadTelegramUsers = async () => {
  try {
    const response = await api.get("admin/tg-users");
    tgUsers.value = response.data.items || [];
  } catch (error) {
    console.error("Не удалось загрузить telegram users", error);
  }
};

const loadMeta = async () => {
  try {
    const meta = await fetchAuthMeta();
    if (Array.isArray(meta.roles) && meta.roles.length) {
      roleOptions.value = meta.roles.map((item) => ({
        value: item.key,
        label: item.label,
      }));
    }

    if (Array.isArray(meta.statuses) && meta.statuses.length) {
      statusOptions.value = meta.statuses.map((item) => ({
        value: item.key,
        label: item.label,
      }));
    }
  } catch (error) {
    console.error("Не удалось загрузить auth meta", error);
  }
};

const applyFilters = () => {
  search.value = searchInput.value.trim();
  page.value = 1;
  loadUsers();
};

const goToPage = (nextPage) => {
  if (nextPage < 1 || nextPage > pages.value) return;
  page.value = nextPage;
  loadUsers();
};

const openDetails = async (userId) => {
  detailsOpen.value = true;
  detailsLoading.value = true;
  detail.value = null;
  try {
    const response = await api.get(`admin/users/${userId}`);
    detail.value = response.data;
  } catch (error) {
    console.error("Не удалось загрузить детали пользователя", error);
  } finally {
    detailsLoading.value = false;
  }
};

const closeDetails = () => {
  detailsOpen.value = false;
  detail.value = null;
};

const toggleStatus = async (user) => {
  const nextStatus = user.status === "blocked" ? "active" : "blocked";
  try {
    await api.patch(`admin/users/${user.id}/status`, { status: nextStatus });
    user.status = nextStatus;
    if (detail.value?.id === user.id) {
      await openDetails(user.id);
    }
  } catch (error) {
    console.error("Не удалось изменить статус", error);
  }
};

const onRoleChange = async (user, event) => {
  const nextRole = event.target.value;
  try {
    await api.patch(`admin/users/${user.id}/role`, { role: nextRole });
    user.role = nextRole;
    if (detail.value?.id === user.id) {
      detail.value.role = nextRole;
    }
  } catch (error) {
    console.error("Не удалось изменить роль", error);
  }
};

const onTelegramRoleChange = async (tgUser, event) => {
  const nextRole = event.target.value;
  try {
    const response = await api.patch(`admin/tg-users/${tgUser.id}/role`, { role: nextRole });
    tgUsers.value = response.data.items || [];
  } catch (error) {
    console.error("Не удалось изменить telegram роль", error);
    event.target.value = tgUser.role;
  }
};

const deleteTelegramUser = async (tgUser) => {
  try {
    const response = await api.delete(`admin/tg-users/${tgUser.id}`);
    tgUsers.value = response.data.items || [];
  } catch (error) {
    console.error("Не удалось удалить telegram user", error);
  }
};

const statusClass = (status) => {
  if (status === "blocked") return "bg-rose-400/15 text-rose-200";
  if (status === "cancelled") return "bg-rose-400/15 text-rose-200";
  return "bg-emerald-400/15 text-emerald-200";
};

const roleLabel = (role) => getRoleLabel(role);
const statusLabel = (status) => statusOptions.value.find((item) => item.value === status)?.label || status;

const pageButtons = computed(() => {
  const start = Math.max(1, page.value - 2);
  const end = Math.min(pages.value, start + 4);
  const buttons = [];
  for (let i = start; i <= end; i += 1) buttons.push(i);
  return buttons;
});

watch([roleFilter, statusFilter], () => {
  page.value = 1;
  loadUsers();
});

onMounted(async () => {
  await loadMeta();
  await Promise.all([loadUsers(), loadTelegramUsers()]);
});
</script>

<style scoped>
.field {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
}

.input {
  min-width: 180px;
  border-radius: 0.85rem;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.06);
  padding: 0.75rem 1rem;
  color: white;
  outline: none;
}

.input option {
  color: #0f172a;
}

.select {
  border-radius: 0.85rem;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.06);
  padding: 0.6rem 0.8rem;
  color: white;
  outline: none;
}

.select option {
  color: #0f172a;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  padding: 0.35rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 700;
}

.pager {
  border-radius: 0.85rem;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.06);
  padding: 0.55rem 0.9rem;
  color: white;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.pager:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.detail-card {
  border-radius: 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.05);
  padding: 1rem;
}

.detail-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: rgba(255, 255, 255, 0.45);
}

.detail-value {
  margin-top: 0.45rem;
  font-size: 1.5rem;
  font-weight: 700;
}
</style>
