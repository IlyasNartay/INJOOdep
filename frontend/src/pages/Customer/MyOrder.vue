<template>
  <div
    class="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-pink-800 py-6 px-4 animated-gradient"
  >
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-8">
        <h1
          class="text-3xl md:text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2"
        >
          {{ t('orders.title') }}
        </h1>
        <p class="text-white text-lg">{{ t('orders.subtitle') }}</p>
      </div>

      <div class="space-y-6">
        <div
          v-for="order in orders"
          :key="order.id"
          class="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 overflow-hidden hover:shadow-3xl transition-all duration-300"
        >
          <div class="bg-gradient-to-r from-blue-500/10 to-purple-500/10 p-6 border-b border-gray-200/30">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div class="flex items-center space-x-4">
                <div class="bg-gradient-to-r from-blue-500 to-purple-600 p-3 rounded-2xl">
                  <ShoppingBagIcon class="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 class="text-xl font-semibold text-gray-800">
                    {{ t('orders.order') }} #{{ order.id }}
                  </h3>
                </div>
              </div>

              <div class="flex items-center space-x-4">
                <span
                  :class="getStatusClass(order.status)"
                  class="px-4 py-2 rounded-full text-sm font-semibold"
                >
                  {{ getStatusText(order.status) }}
                </span>

                <div class="text-right">
                  <p class="text-2xl font-bold text-gray-800">
                    {{ order.total_price }} ₸
                  </p>
                  <p class="text-sm text-gray-500">{{ t('orders.total') }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="p-6">
            <h4 class="text-lg font-semibold text-gray-800 mb-4 flex items-center space-x-2">
              <UtensilsIcon class="h-5 w-5 text-blue-500" />
              <span>{{ t('orders.dishesInOrder') }}</span>
            </h4>

            <div class="space-y-4">
              <div
                v-for="orderDish in order.order_dishes"
                :key="orderDish.dish.id"
                class="flex items-center space-x-4 p-4 bg-gradient-to-r from-gray-50/80 to-blue-50/50 rounded-2xl border border-gray-200/30 hover:shadow-lg transition-all duration-200"
              >
                <div class="flex-shrink-0">
                  <div class="relative">
                    <img
                      v-if="orderDish.dish.images && orderDish.dish.images.length > 0"
                      :src="getImageUrl(orderDish.dish.images[0]?.image_url)"
                      :alt="orderDish.dish.name"
                      class="w-20 h-20 md:w-24 md:h-24 object-cover rounded-2xl shadow-lg"
                    />
                    <div
                      v-else
                      class="w-20 h-20 md:w-24 md:h-24 bg-gradient-to-br from-gray-200 to-gray-300 rounded-2xl flex items-center justify-center shadow-lg"
                    >
                      <ImageIcon class="h-8 w-8 text-gray-400" />
                    </div>

                    <div
                      class="absolute -top-2 -right-2 bg-gradient-to-r from-orange-500 to-red-500 text-white text-xs font-bold rounded-full w-6 h-6 flex items-center justify-center shadow-lg"
                    >
                      {{ orderDish.quantity }}
                    </div>
                  </div>
                </div>

                <div class="flex-1 min-w-0">
                  <h5 class="text-lg font-semibold text-gray-800 mb-1">
                    {{ orderDish.dish.name }}
                  </h5>
                  <p class="text-gray-600 text-sm mb-2 line-clamp-2">
                    {{ orderDish.dish.description }}
                  </p>

                  <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-3">
                      <span class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-medium">
                        {{ orderDish.dish.category }}
                      </span>
                    </div>

                    <div class="text-right">
                      <p class="text-lg font-bold text-gray-800">
                        {{ orderDish.dish.price }} ₸
                      </p>
                      <p class="text-xs text-gray-500">{{ t('orders.perItem') }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <Loader v-if="isLoading" />

      <div v-if="orders.length === 0" class="text-center py-16">
        <div class="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-12">
          <ShoppingBagIcon class="h-24 w-24 text-gray-300 mx-auto mb-6" />
          <h3 class="text-2xl font-semibold text-gray-800 mb-4">
            {{ t('orders.noOrders') }}
          </h3>
          <p class="text-gray-600 mb-8">{{ t('orders.noOrdersHint') }}</p>
          <button
            class="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-semibold py-3 px-8 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-200"
          >
            {{ t('orders.goToMenu') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import Loader from "@/components/Loader.vue";
import { ref, onMounted } from "vue";
import { t } from "@/i18n";
import { fetchOrderMeta, getOrderStatusLabel } from "@/utils/orderStatus";
import {
  ShoppingBag as ShoppingBagIcon,
  Utensils as UtensilsIcon,
  Image as ImageIcon,
} from "lucide-vue-next";

const getImageUrl = (path) => `${import.meta.env.VITE_API_BASE_URL}${path}`;

const isLoading = ref(false);
const statusOptions = ref([]);
const orders = ref([]);

const loadOrderMeta = async () => {
  try {
    const meta = await fetchOrderMeta();
    statusOptions.value = meta.statuses || [];
  } catch (error) {
    console.error("Не удалось загрузить метаданные заказов:", error);
  }
};

const getOrders = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}orders/my`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
        Accept: "application/json",
      },
    });

    orders.value = response.data.reverse();
  } catch (error) {
    console.error("Ошибка при получении заказов:", error.response?.data || error.message);
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  await loadOrderMeta();
  await getOrders();
});

const getStatusClass = (status) => {
  const statusClasses = {
    pending: "bg-yellow-100 text-yellow-800 border border-yellow-200",
    accepted: "bg-blue-100 text-blue-800 border border-blue-200",
    ready: "bg-orange-100 text-orange-800 border border-orange-200",
    done: "bg-green-100 text-green-800 border border-green-200",
    cancelled: "bg-red-100 text-red-800 border border-red-200",
  };
  return statusClasses[status] || "bg-gray-100 text-gray-800 border border-gray-200";
};

const getStatusText = (status) => {
  return getOrderStatusLabel(status, statusOptions.value) || t("orders.unknown");
};
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.shadow-3xl {
  box-shadow: 0 35px 60px -12px rgba(0, 0, 0, 0.25);
}

* {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

.backdrop-blur-xl {
  backdrop-filter: blur(20px);
}
</style>
