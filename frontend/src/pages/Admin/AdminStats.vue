<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-emerald-950 text-white">
    <div class="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
      <div class="mb-8 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p class="text-emerald-300 uppercase tracking-[0.35em] text-xs mb-3">Admin dashboard</p>
          <h1 class="text-3xl sm:text-4xl font-bold">Статистика ресторана</h1>
          <p class="text-white/70 mt-3 max-w-2xl">
            Выручка, заказы, средний чек, новые пользователи, динамика по дням и топ блюд.
          </p>
        </div>

        <div class="flex flex-col sm:flex-row gap-3 rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur">
          <label class="flex flex-col gap-1 text-sm">
            <span class="text-white/60">С</span>
            <input v-model="dateFrom" type="date" class="input" />
          </label>
          <label class="flex flex-col gap-1 text-sm">
            <span class="text-white/60">По</span>
            <input v-model="dateTo" type="date" class="input" />
          </label>
          <button @click="loadStats" class="self-end rounded-xl bg-emerald-500 px-4 py-3 font-semibold text-slate-950 hover:bg-emerald-400 transition">
            Обновить
          </button>
        </div>
      </div>

      <div v-if="isLoading" class="py-20 text-center text-white/70">
        Загрузка статистики...
      </div>

      <div v-else class="space-y-6">
        <section class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <article v-for="card in overviewCards" :key="card.label" class="rounded-2xl border border-white/10 bg-white/6 p-5 shadow-2xl backdrop-blur">
            <p class="text-sm text-white/60">{{ card.label }}</p>
            <div class="mt-3 flex items-end justify-between gap-3">
              <div>
                <div class="text-3xl font-bold">{{ card.value }}</div>
                <p class="mt-1 text-xs text-white/45">{{ card.hint }}</p>
              </div>
              <div class="rounded-2xl bg-emerald-400/15 p-3 text-emerald-300">
                <component :is="card.icon" class="h-6 w-6" />
              </div>
            </div>
          </article>
        </section>

        <section class="grid gap-6 xl:grid-cols-[1.6fr_1fr]">
          <article class="rounded-3xl border border-white/10 bg-slate-950/70 p-5 shadow-2xl backdrop-blur">
            <div class="mb-5 flex items-center justify-between gap-3">
              <div>
                <h2 class="text-xl font-semibold">Выручка по дням</h2>
                <p class="text-sm text-white/55">Динамика продаж за выбранный период</p>
              </div>
              <div class="rounded-full bg-white/5 px-3 py-1 text-xs text-white/65">
                {{ revenueByDay.length }} точек
              </div>
            </div>

            <div v-if="!revenueByDay.length" class="rounded-2xl border border-dashed border-white/10 p-10 text-center text-white/50">
              Нет данных за выбранный период
            </div>

            <div v-else class="overflow-x-auto">
              <svg :viewBox="`0 0 ${chartWidth} ${chartHeight}`" class="min-w-[720px] w-full">
                <defs>
                  <linearGradient id="revenueFill" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stop-color="#34d399" stop-opacity="0.45" />
                    <stop offset="100%" stop-color="#34d399" stop-opacity="0.03" />
                  </linearGradient>
                </defs>
                <g v-for="tick in yTicks" :key="tick.value">
                  <line :x1="padding.left" :x2="chartWidth - padding.right" :y1="tick.y" :y2="tick.y" stroke="rgba(255,255,255,0.08)" stroke-width="1" />
                  <text :x="padding.left - 10" :y="tick.y + 4" text-anchor="end" fill="rgba(255,255,255,0.45)" font-size="12">
                    {{ formatMoney(tick.value) }}
                  </text>
                </g>
                <path :d="areaPath" fill="url(#revenueFill)" />
                <path :d="linePath" fill="none" stroke="#34d399" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
                <g v-for="point in chartPoints" :key="point.label">
                  <circle :cx="point.x" :cy="point.y" r="4.5" fill="#34d399" />
                  <text :x="point.x" :y="chartHeight - 18" text-anchor="middle" fill="rgba(255,255,255,0.55)" font-size="11">
                    {{ point.label }}
                  </text>
                </g>
              </svg>
            </div>
          </article>

          <article class="rounded-3xl border border-white/10 bg-white/6 p-5 shadow-2xl backdrop-blur">
            <div class="mb-5 flex items-center justify-between">
              <div>
                <h2 class="text-xl font-semibold">Статусы заказов</h2>
                <p class="text-sm text-white/55">Распределение заказов по этапам</p>
              </div>
            </div>

            <div class="space-y-4">
              <div v-for="item in orderStatuses" :key="item.status" class="rounded-2xl bg-slate-950/60 p-4">
                <div class="flex items-center justify-between gap-3">
                  <div>
                    <p class="font-medium">{{ statusLabel(item.status) }}</p>
                    <p class="text-xs text-white/50">{{ item.count }} заказов</p>
                  </div>
                  <span class="rounded-full px-3 py-1 text-xs font-semibold" :class="statusBadgeClass(item.status)">
                    {{ statusPercent(item.count) }}
                  </span>
                </div>
                <div class="mt-3 h-2 rounded-full bg-white/8">
                  <div class="h-2 rounded-full" :class="statusBarClass(item.status)" :style="{ width: statusWidth(item.count) }"></div>
                </div>
              </div>
            </div>
          </article>
        </section>

        <section class="grid gap-6 xl:grid-cols-[1.2fr_1fr]">
          <article class="rounded-3xl border border-white/10 bg-white/6 p-5 shadow-2xl backdrop-blur">
            <div class="mb-5">
              <h2 class="text-xl font-semibold">Топ-5 блюд</h2>
              <p class="text-sm text-white/55">По количеству заказов и сумме</p>
            </div>

            <div v-if="!topDishes.length" class="rounded-2xl border border-dashed border-white/10 p-10 text-center text-white/50">
              Нет данных для топа блюд
            </div>

            <div v-else class="space-y-3">
              <div v-for="(dish, index) in topDishes" :key="dish.name" class="rounded-2xl bg-slate-950/60 p-4">
                <div class="flex items-start justify-between gap-4">
                  <div class="flex items-start gap-4">
                    <div class="flex h-10 w-10 items-center justify-center rounded-2xl bg-emerald-500/15 text-emerald-300 font-bold">
                      {{ index + 1 }}
                    </div>
                    <div>
                      <h3 class="font-semibold">{{ dish.name }}</h3>
                      <p class="text-sm text-white/55">{{ dish.quantity }} заказов</p>
                    </div>
                  </div>
                  <div class="text-right">
                    <p class="font-semibold">{{ formatMoney(dish.revenue) }}</p>
                    <p class="text-xs text-white/45">Выручка</p>
                  </div>
                </div>
                <div class="mt-3 h-2 rounded-full bg-white/8">
                  <div class="h-2 rounded-full bg-emerald-400" :style="{ width: dishWidth(dish.revenue) }"></div>
                </div>
              </div>
            </div>
          </article>

          <article class="rounded-3xl border border-white/10 bg-slate-950/70 p-5 shadow-2xl backdrop-blur">
            <div class="mb-5">
              <h2 class="text-xl font-semibold">Детали периода</h2>
              <p class="text-sm text-white/55">Сводка по выбранному диапазону дат</p>
            </div>

            <div class="space-y-3 text-sm text-white/75">
              <div class="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3">
                <span>Период</span>
                <span class="text-white">{{ periodLabel }}</span>
              </div>
              <div class="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3">
                <span>Всего заказов</span>
                <span class="text-white">{{ stats?.overview.total_orders ?? 0 }}</span>
              </div>
              <div class="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3">
                <span>Новые пользователи</span>
                <span class="text-white">{{ stats?.overview.new_users ?? 0 }}</span>
              </div>
              <div class="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3">
                <span>Средний чек</span>
                <span class="text-white">{{ formatMoney(stats?.overview.avg_check ?? 0) }}</span>
              </div>
            </div>
          </article>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { computed, onMounted, ref } from "vue";
import { fetchOrderMeta, getOrderStatusLabel } from "@/utils/orderStatus";
import { BarChart3, CircleDollarSign, ShoppingBag, Users } from "lucide-vue-next";

const stats = ref(null);
const orderMeta = ref({ statuses: [], flow: [] });
const isLoading = ref(false);
const dateFrom = ref("");
const dateTo = ref("");

const chartWidth = 900;
const chartHeight = 280;
const padding = { top: 20, right: 20, bottom: 40, left: 70 };

const formatMoney = (value) =>
  new Intl.NumberFormat("ru-RU", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(Number(value || 0)) + " ₸";

const loadStats = async () => {
  isLoading.value = true;
  try {
    const params = {};
    if (dateFrom.value) params.date_from = dateFrom.value;
    if (dateTo.value) params.date_to = dateTo.value;

    const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}admin/stats`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
        Accept: "application/json",
      },
      params,
    });
    stats.value = response.data;
  } catch (error) {
    console.error("Не удалось загрузить статистику", error);
  } finally {
    isLoading.value = false;
  }
};

const loadOrderMeta = async () => {
  try {
    orderMeta.value = await fetchOrderMeta();
  } catch (error) {
    console.error("�� ������� ��������� order meta", error);
  }
};

onMounted(async () => {
  await loadOrderMeta();
  await loadStats();
});

const revenueByDay = computed(() => stats.value?.revenue_by_day ?? []);
const topDishes = computed(() => stats.value?.top_dishes ?? []);
const orderStatuses = computed(() => stats.value?.order_statuses ?? []);

const overviewCards = computed(() => [
  {
    label: "Выручка",
    value: formatMoney(stats.value?.overview.total_revenue ?? 0),
    hint: "Сумма всех заказов",
    icon: CircleDollarSign,
  },
  {
    label: "Заказы",
    value: String(stats.value?.overview.total_orders ?? 0),
    hint: "Количество заказов",
    icon: ShoppingBag,
  },
  {
    label: "Средний чек",
    value: formatMoney(stats.value?.overview.avg_check ?? 0),
    hint: "Средняя сумма заказа",
    icon: BarChart3,
  },
  {
    label: "Новые пользователи",
    value: String(stats.value?.overview.new_users ?? 0),
    hint: "За выбранный период",
    icon: Users,
  },
]);

const values = computed(() => revenueByDay.value.map((item) => Number(item.revenue || 0)));
const maxRevenue = computed(() => Math.max(1, ...values.value, 0));
const minRevenue = computed(() => Math.min(...values.value, 0));

const chartPoints = computed(() => {
  const data = revenueByDay.value;
  if (!data.length) return [];

  const usableWidth = chartWidth - padding.left - padding.right;
  const usableHeight = chartHeight - padding.top - padding.bottom;
  const step = data.length === 1 ? 0 : usableWidth / (data.length - 1);
  const range = Math.max(1, maxRevenue.value - minRevenue.value);

  return data.map((item, index) => {
    const value = Number(item.revenue || 0);
    const x = padding.left + step * index;
    const y = padding.top + usableHeight - ((value - minRevenue.value) / range) * usableHeight;
    return {
      x,
      y,
      label: new Date(item.date).toLocaleDateString("ru-RU", { month: "short", day: "numeric" }),
      value,
    };
  });
});

const linePath = computed(() => {
  if (!chartPoints.value.length) return "";
  return chartPoints.value
    .map((point, index) => `${index === 0 ? "M" : "L"} ${point.x} ${point.y}`)
    .join(" ");
});

const areaPath = computed(() => {
  if (!chartPoints.value.length) return "";
  const first = chartPoints.value[0];
  const last = chartPoints.value[chartPoints.value.length - 1];
  return `${linePath.value} L ${last.x} ${chartHeight - padding.bottom} L ${first.x} ${chartHeight - padding.bottom} Z`;
});

const yTicks = computed(() => {
  const ticks = 4;
  const usableHeight = chartHeight - padding.top - padding.bottom;
  const range = Math.max(1, maxRevenue.value - minRevenue.value);
  return Array.from({ length: ticks + 1 }, (_, index) => {
    const ratio = index / ticks;
    const value = maxRevenue.value - range * ratio;
    return {
      value,
      y: padding.top + usableHeight * ratio,
    };
  });
});

const periodLabel = computed(() => {
  if (dateFrom.value && dateTo.value) return `${dateFrom.value} - ${dateTo.value}`;
  if (dateFrom.value) return `с ${dateFrom.value}`;
  if (dateTo.value) return `до ${dateTo.value}`;
  return "весь период";
});

const statusLabel = (status) =>
  getOrderStatusLabel(status, orderMeta.value.statuses) || status;

const statusBadgeClass = (status) => {
  const map = {
    pending: "bg-amber-400/15 text-amber-200",
    accepted: "bg-sky-400/15 text-sky-200",
    ready: "bg-violet-400/15 text-violet-200",
    done: "bg-emerald-400/15 text-emerald-200",
    cancelled: "bg-rose-400/15 text-rose-200",
  };
  return map[status] || "bg-white/10 text-white/70";
};

const statusBarClass = (status) => {
  const map = {
    pending: "bg-amber-400",
    accepted: "bg-sky-400",
    ready: "bg-violet-400",
    done: "bg-emerald-400",
    cancelled: "bg-rose-400",
  };
  return map[status] || "bg-white/40";
};

const statusWidth = (count) => {
  const total = Math.max(1, stats.value?.overview.total_orders ?? 1);
  return `${Math.max(6, Math.round((count / total) * 100))}%`;
};

const statusPercent = (count) => {
  const total = Math.max(1, stats.value?.overview.total_orders ?? 1);
  return `${Math.round((count / total) * 100)}%`;
};

const dishWidth = (revenue) => {
  const max = Math.max(1, ...topDishes.value.map((item) => Number(item.revenue || 0)));
  return `${Math.max(8, Math.round((Number(revenue || 0) / max) * 100))}%`;
};
</script>

<style scoped>
.input {
  min-width: 180px;
  border-radius: 0.9rem;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.06);
  padding: 0.75rem 1rem;
  color: white;
  outline: none;
}

.input::-webkit-calendar-picker-indicator {
  filter: invert(1);
  opacity: 0.8;
}
</style>




