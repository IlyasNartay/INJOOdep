<template>
  <div
    class="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-pink-800 py-8 animated-gradient"
  >
    <div class="max-w-6xl mx-auto px-4">
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-0">
          <div class="lg:col-span-2 p-8 max-[335px]:p-2">
            <div
              class="flex justify-between w-[80%] max-[480px]:w-[100%] gap-4 pb-4 mb-6 border-b border-gray-200 text-sm max-[480px]:text-[10px] font-medium text-gray-500 uppercase tracking-wide"
            >
              <div class="col-span-5">Продукт</div>
              <div class="col-span-2 text-center">Цена</div>
              <div class="col-span-2 text-center">Количество</div>
            </div>
            <div v-if="cartI.items.length === 0" class="text-gray-400">
              Корзина пуста
            </div>

            <div class="space-y-6">
              <div
                v-for="item in cartI.itemsWithTotal"
                :key="item.id"
                class="flex gap-4 justify-between items-center py-4 w-[90%]"
              >
                <div class="col-span-5 flex items-center space-x-4">
                  <div
                    class="max-[480px]:w-[40px] max-[480px]:h-[40px] w-20 h-20 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0"
                  >
                    <img
                      v-if="item.images && item.images.length > 0"
                      :src="image_url + item.images[0].image_url"
                      :alt="item.name"
                      class="w-full h-full object-cover max-[480px]:w-[40px] max-[480px]:h-[40px]"
                    />
                  </div>
                  <div class="flex-1 min-w-0">
                    <h3
                      class="font-medium text-gray-900 mb-1 max-[480px]:text-[10px]"
                    >
                      {{ item.name }}
                    </h3>
                    <p class="text-sm text-gray-500 max-[480px]:text-[10px]">
                      {{ item.description }}
                    </p>
                  </div>
                </div>

                <div class="col-span-3 text-right">
                  <span
                    class="font-medium text-gray-900 max-[480px]:text-[10px]"
                  >
                    {{ item.total }} ₸
                  </span>
                </div>

                <div
                  class="col-span-2 flex max-[380px]:flex-col items-center justify-center gap-4"
                >
                  <div
                    class="flex max-[380px]:flex-col items-center border border-gray-300 rounded-lg max-[480px]:w-[80px] max-[350px]:w-[50px] max-[480px]:text-[10px]"
                  >
                    <button
                      @click="decreaseQuantity(item.id)"
                      class="w-8 h-8 flex items-center justify-center text-gray-500 hover:text-gray-700 hover:bg-gray-50 transition-colors"
                      :disabled="item.quantity <= 1"
                    >
                      <MinusIcon class="w-4 h-4" />
                    </button>
                    <span class="w-12 text-center text-sm font-medium">
                      {{ item.quantity }}
                    </span>
                    <button
                      @click="increaseQuantity(item.id)"
                      class="w-8 h-8 flex items-center justify-center text-gray-500 hover:text-gray-700 hover:bg-gray-50 transition-colors"
                    >
                      <PlusIcon class="w-4 h-4" />
                    </button>
                  </div>
                  <MinusIcon
                    @click="remove(item.id)"
                    class="w-8 h-8 text-red-500 max-[480px]:w-4 max-[480px]:h-4"
                  />
                </div>
              </div>

              <div class="text-right font-bold text-lg mt-8">
                Общая сумма: {{ cartI.totalPrice }} ₸
              </div>
            </div>

            <div class="mt-8 pt-6 border-t border-gray-200">
              <h4
                @click="console.log(cartI)"
                class="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3"
              >
                Добавить коментарий
              </h4>
              <textarea
                v-model="orderNote"
                placeholder="Добавить коментарий к заказу"
                class="w-full p-3 border border-gray-300 rounded-lg text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent resize-none"
                rows="3"
              ></textarea>
            </div>
          </div>
          <CustomModal v-if="success">
            <div
              class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center"
            >
              <img
                src="/sucsess-modal.svg"
                alt="Успешно"
                class="w-16 h-16 mx-auto mb-4"
              />
              <h3 class="text-xl font-semibold text-black mb-2">
                Ваш заказ принят!
              </h3>
              <p class="text-black mb-4">
                Спасибо за заказ. Доставим как можно скорее!
              </p>
              <button
                @click="success = false"
                class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold"
              >
                Закрыть
              </button>
            </div>
          </CustomModal>

          <CustomModal v-if="failInRest">
            <div
              class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center"
            >
              <img
                src="/fail-modal.svg"
                alt="Успешно"
                class="w-16 h-16 mx-auto mb-4"
              />
              <h3 class="text-xl font-semibold text-black mb-2">
                Что то пошло не так!
              </h3>
              <p class="text-black mb-4">
                {{ getTableTitle(userRole) }}
              </p>
              <button
                @click="failInRest = false"
                class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold"
              >
                Закрыть
              </button>
            </div>
          </CustomModal>
          <Loader v-if="isLoading" />

          <div class="bg-rose-50 p-8">
            <div class="sticky top-8">
              <div class="w-16 h-0.5 bg-gray-900 mb-8"></div>

              <div class="mb-6">
                <div class="flex justify-between items-center mb-2">
                  <span
                    class="text-sm font-medium text-gray-600 uppercase tracking-wide"
                  >
                    Итого в корзине
                  </span>
                </div>
                <p class="text-sm text-gray-500">
                  Доставка и налоги будут рассчитаны при оформлении заказа
                </p>
              </div>

              <div class="mb-6">
                <label class="flex items-start space-x-3 cursor-pointer">
                  <input
                    v-model="agreeToTerms"
                    type="checkbox"
                    class="mt-1 w-4 h-4 text-gray-900 border-gray-300 rounded focus:ring-gray-900 focus:ring-2"
                  />
                  <span class="text-sm text-gray-600">
                    Я согласен с условиями
                  </span>
                </label>
              </div>
              <button
                @click="makeOrderGuestorCustomer"
                :disabled="!agreeToTerms || cartI.length === 0"
                class="w-full bg-gray-900 text-white py-4 px-6 rounded-lg font-medium uppercase tracking-wide hover:bg-gray-800 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors mb-4"
              >
                Оформить заказ
              </button>
            </div>
          </div>
        </div>
        <CustomModal v-if="showPhoneModal" @click.self="showPhoneModal = false">
          <div
            class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
          >
            <div
              class="relative w-[90vw] max-w-md rounded-2xl bg-white shadow-2xl p-6 animate-fadeIn"
            >
              <!-- Close -->
              <button
                @click="showPhoneModal = false"
                class="absolute top-3 right-3 text-gray-400 hover:text-gray-700 transition"
              >
                ✕
              </button>

              <!-- Header -->
              <div class="flex items-center gap-3 mb-4">
                <div
                  class="w-10 h-10 flex items-center justify-center rounded-full bg-green-100 text-green-600 text-xl"
                >
                  <img
                    class="w-10 h-10 flex items-center justify-center rounded-full bg-green-100 text-green-600 text-xl"
                    src="/kaspiPhoto2.webp"
                  />
                </div>
                <h2 class="text-lg font-semibold text-gray-800">Kaspi</h2>
              </div>

              <!-- Input -->
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Номер счета для оплаты
              </label>
              <input
                v-model="kaspiPhone"
                type="tel"
                placeholder="87070000000"
                @input="kaspiPhone = kaspiPhone.replace(/\D/g, '')"
                class="w-full rounded-lg border border-gray-300 px-4 py-2 mb-5 outline-none focus:ring-2 focus:ring-green-400 focus:border-green-400 transition"
              />

              <!-- Button -->
              <button
                @click="handleCheckout"
                class="w-full rounded-lg bg-green-500 py-3 font-semibold text-white hover:bg-green-600 active:scale-[0.98] transition"
              >
                Отправить счёт
              </button>
            </div>
          </div>
        </CustomModal>
<CustomModal v-if="emptyModal">
          <div
            class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center"
          >
            <img
              src="/fail-modal.svg"
              alt="Успешно"
              class="w-16 h-16 mx-auto mb-4"
            />
            <h3 class="text-xl font-semibold text-black mb-2">
              Что то пошло не так!
            </h3>
            <p class="text-black mb-4">Выберите блюдо для заказа!</p>
            <button
              @click="emptyModal = false"
              class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold"
            >
              Закрыть
            </button>
          </div>
        </CustomModal>
        <CustomModal v-if="fail">
          <div
            class="relative z-10 backdrop-blur-md bg-white/20 border border-white/30 p-6 rounded-2xl shadow-xl w-[90%] max-w-md text-center"
          >
            <img
              src="/fail-modal.svg"
              alt="Успешно"
              class="w-16 h-16 mx-auto mb-4"
            />
            <h3 class="text-xl font-semibold text-black mb-2">
              Что то пошло не так!
            </h3>
            <p class="text-black mb-4">Укажите адрес доставки!</p>
            <button
              @click="fail = false"
              class="bg-white/80 text-blue-700 px-6 py-2 rounded-lg hover:bg-white transition font-semibold"
            >
              Закрыть
            </button>
          </div>
        </CustomModal>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from "vue";
import { Plus as PlusIcon, Minus as MinusIcon } from "lucide-vue-next";
import { useCartStore } from "/src/stores/Basket.js";
import CustomModal from "@/components/CustomModal.vue";
import axios from "axios";
import Loader from "@/components/Loader.vue";
import { useAddressStore } from "@/stores/addressStore";
import { useAutoClose } from "@/stores/useAutoClose";

const cartI = useCartStore();
const isLoading = ref(false);
const image_url = `${import.meta.env.VITE_API_BASE_URL}`;
const success = ref(false);
const failInRest = ref(false);
const userRole = localStorage.getItem("userRole");
const fail = ref(false);
const orderNote = ref("");
const agreeToTerms = ref(false);
const store = useAddressStore();
const role = localStorage.getItem("userRole");
const showPhoneModal = ref(false);
const address = ref([{ address: "" }]);
const kaspiPhone = ref("");
const emptyModal = ref(false);
let table_id = ref(localStorage.getItem("selectedTable"));
let timer = null;

const getTableTitle = (userRole) => {
  if (role === "guest") return "Выберите свой стол!";
  if (role === "customer") return "По пробуйте сделать заказ чуть позже!";
};

const openPhoneModal = () => {
  showPhoneModal.value = true;
};

const makeOrderGuestorCustomer = () => {
  if (!cartI.items || cartI.items.length === 0) {
    emptyModal.value = true;
    return; // Останавливаем выполнение функции
  } else if (localStorage.getItem("userRole") === "guest") {
    handleCheckoutForGuest();
  } else {
    openPhoneModal();
  }
};
function remove(id) {
  cartI.removeItem(id);
}
const toggleCartItem = (item) => {
  const index = cartItems.value.findIndex((i) => i.id === item.id);
  if (index !== -1) {
    // Если уже есть в корзине — удалить
    cartItems.value.splice(index, 1);
  } else {
    // Если нет — добавить
    cartItems.value.push({ ...item, quantity: 1 });
  }
};
const closeModal = () => {};
// Methods
const increaseQuantity = (itemId) => {
  const item = cartI.items.find((item) => item.id === itemId);
  if (item) {
    item.quantity++;
  }
};

const decreaseQuantity = (itemId) => {
  const item = cartI.items.find((item) => item.id === itemId);
  if (item && item.quantity > 1) {
    item.quantity--;
  }
};
const handleCheckoutForGuest = async () => {
  isLoading.value = true;

  const checkoutData = {
    table_id: Number(localStorage.getItem("selectedTable")), // замените на реальный ID адреса
    dishes: cartI.items.map((item) => ({
      dish_id: item.id,
      quantity: item.quantity || 1, // или другое поле, если у тебя есть quantity
    })),
  };
  try {
    const response = await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}orders/table`,
      checkoutData
    );

    console.log("✅ Заказ успешно оформлен:", response.data);
    success.value = true;

    cartI.clearCart();
  } catch (error) {
    console.error(
      "❌ Ошибка при оформлении заказа:",
      error.response?.data || error.message
    );
    failInRest.value = true;
  } finally {
    isLoading.value = false;
  }
};

const handleCheckout = async () => {
  if (!store.address || store.address.length === 0 || !store.address[0].id) {
    console.error("❌ Не найден address_id для оформления заказа!");
    showPhoneModal.value = false;
    fail.value = true;
    return;
  }
  const checkoutData = {
    address_id: store.address[0].id, // замените на реальный ID адреса
    kaspi_number: kaspiPhone.value,
    dishes: cartI.items.map((item) => ({
      dish_id: item.id,
      quantity: item.quantity || 1, // или другое поле, если у тебя есть quantity
    })),
  };
  isLoading.value = true;

  try {
    const response = await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}orders/`,
      checkoutData,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("authToken")}`,
          "Content-Type": "application/json",
        },
      }
    );
    showPhoneModal.value = false;

    success.value = true;
    // можно очистить корзину:
    cartI.clearCart();
  } catch (error) {
    console.error(
      "❌ Ошибка при оформлении заказа:",
      error.response?.data || error.message
    );
    fail.value = true;
  } finally {
    isLoading.value = false;
  }
};
const makeCheckout = () => {
  if (role == "guest") {
    handleCheckoutForGuest();
  } else {
    handleCheckout();
  }
};
watch(address, (newVal) => {
  // твоя логика
  store.address = [{ address: newVal[0].address }];

  // показать модалку
  success.value = true;

  // перезапуск таймера
  if (timer) clearTimeout(timer);

  timer = setTimeout(() => {
    success.value = false;
  }, 2000);
});
// watch([success, failInRest], ([successVal, failVal]) => {
//   if (!successVal && !failVal) return;

//   if (timer) clearTimeout(timer);

//   timer = setTimeout(() => {
//     success.value = false;
//     failInRest.value = false;
//   }, 2000);
// });

// onBeforeUnmount(() => {
//   if (timer) clearTimeout(timer);
// });
useAutoClose(success, 2000);
useAutoClose(fail, 2500);
useAutoClose(failInRest, 3000);
</script>

<style scoped>
/* Custom checkbox styling */
input[type="checkbox"]:checked {
  background-color: #111827;
  border-color: #111827;
}

/* Smooth transitions */
button {
  transition: all 0.2s ease-in-out;
}

/* Custom scrollbar for textarea */
textarea::-webkit-scrollbar {
  width: 6px;
}

textarea::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

textarea::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

textarea::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
