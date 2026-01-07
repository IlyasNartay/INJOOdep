<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-pink-800 py-8">
    <div class="max-w-6xl mx-auto px-4">
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden">
        <div class="grid grid-cols-1 lg:grid-cols-3">

          <!-- LEFT: CART -->
          <div class="lg:col-span-2 p-8 max-[335px]:p-2">

            <div
              class="flex justify-between w-[80%] max-[480px]:w-full gap-4 pb-4 mb-6
                     border-b border-gray-200 text-sm max-[480px]:text-[10px]
                     font-medium text-gray-500 uppercase tracking-wide"
            >
              <div class="col-span-5">Продукт</div>
              <div class="col-span-2 text-center">Цена</div>
              <div class="col-span-2 text-center">Количество</div>
            </div>

            <!-- EMPTY -->
            <div v-if="cartI.items.length === 0" class="text-gray-400">
              Корзина пуста
            </div>

            <!-- ITEMS -->
            <div class="space-y-6">
              <div
                v-for="item in cartI.itemsWithTotal"
                :key="item.id"
                class="flex gap-4 justify-between items-center py-4 w-[90%]"
              >
                <!-- PRODUCT -->
                <div class="flex items-center space-x-4 flex-1">
                  <div
                    class="w-20 h-20 max-[480px]:w-[40px] max-[480px]:h-[40px]
                           bg-gray-100 rounded-lg overflow-hidden flex-shrink-0"
                  >
                    <img
                      v-if="item.images && item.images.length > 0"
                      :src="image_url + item.images[0].image_url"
                      :alt="item.name"
                      class="w-full h-full object-cover"
                    />
                    <div v-else class="w-full h-full flex items-center justify-center text-gray-400 text-sm">
                      Нет фото
                    </div>
                  </div>

                  <div class="min-w-0">
                    <h3 class="font-medium text-gray-900 mb-1 max-[480px]:text-[10px]">
                      {{ item.name }}
                    </h3>
                    <p class="text-sm text-gray-500 max-[480px]:text-[10px]">
                      {{ item.description }}
                    </p>
                  </div>
                </div>

                <!-- PRICE -->
                <div class="text-right">
                  <span class="font-medium text-gray-900 max-[480px]:text-[10px]">
                    {{ item.total }} ₸
                  </span>
                </div>

                <!-- QUANTITY -->
                <div class="flex items-center gap-4 max-[380px]:flex-col">
                  <div
                    class="flex items-center border border-gray-300 rounded-lg
                           max-[480px]:w-[80px] max-[350px]:w-[50px]"
                  >
                    <button
                      @click="decreaseQuantity(item.id)"
                      class="w-8 h-8 flex items-center justify-center
                             text-gray-500 hover:bg-gray-50"
                      :disabled="item.quantity <= 1"
                    >
                      −
                    </button>

                    <span class="w-12 text-center text-sm font-medium">
                      {{ item.quantity }}
                    </span>

                    <button
                      @click="increaseQuantity(item.id)"
                      class="w-8 h-8 flex items-center justify-center
                             text-gray-500 hover:bg-gray-50"
                    >
                      +
                    </button>
                  </div>

                  <!-- REMOVE -->
                  <button
                    @click="remove(item.id)"
                    class="text-red-500 hover:text-red-700 text-sm"
                  >
                    ✕
                  </button>
                </div>
              </div>

              <!-- TOTAL -->
              <div class="text-right font-bold text-lg mt-8">
                Общая сумма: {{ cartI.totalPrice }} ₸
              </div>
            </div>

            <!-- COMMENT -->
            <div class="mt-8 pt-6 border-t border-gray-200">
              <h4 class="text-sm font-medium text-gray-500 uppercase mb-3">
                Добавить комментарий
              </h4>
              <textarea
                v-model="orderNote"
                placeholder="Комментарий к заказу"
                rows="3"
                class="w-full p-3 border border-gray-300 rounded-lg text-sm
                       focus:outline-none focus:ring-2 focus:ring-gray-900"
              />
            </div>

          </div>

          <!-- RIGHT: CHECKOUT -->
<div class="bg-rose-50 p-8">
  <div class="sticky top-8 space-y-6">

    <div class="w-16 h-0.5 bg-gray-900"></div>

    <!-- ADDRESS -->
    <div>
      <h3 class="text-sm font-medium text-gray-600 uppercase mb-3">
        Адрес доставки
      </h3>

      <div v-if="addresses.length === 0" class="text-sm text-gray-400">
        Адреса не найдены
      </div>

      <div
        v-for="addr in addresses"
        :key="addr.id"
        class="flex justify-between gap-3 p-3 mb-2 rounded-xl border cursor-pointer"
        :class="selectedAddressId === addr.id
          ? 'border-gray-900 bg-white'
          : 'border-gray-200 bg-white/70'"
        @click="selectAddress(addr)"
      >
        <label class="flex gap-2 cursor-pointer flex-1">
          <input type="radio" :checked="selectedAddressId === addr.id" />
          <div class="text-sm">
            <p class="font-medium">{{ addr.address }}</p>
            <p class="text-xs text-gray-500">
              кв. {{ addr.apartment || '-' }},
              подъезд {{ addr.entrance || '-' }},
              этаж {{ addr.floor || '-' }}
            </p>
          </div>
        </label>

        <button
          @click.stop="confirmDelete(addr.id)"
          class="text-red-500 hover:text-red-700"
        >
          ✕
        </button>
      </div>
    </div>

    <!-- KASPI NUMBER -->
    <div>
      <label class="text-sm font-medium text-gray-600 mb-1 block">Kaspi номер</label>
      <input
        type="tel"
        v-model="kaspiPhone"
        placeholder="87070000000"
        @input="kaspiPhone = kaspiPhone.replace(/\D/g, '')"
        class="w-full rounded-lg border border-gray-300 px-4 py-2 mb-3 focus:outline-none focus:ring-2 focus:ring-green-400 focus:border-green-400"
      />
    </div>

    <!-- TERMS -->
    <label class="flex items-start gap-2 text-sm text-gray-600">
      <input type="checkbox" v-model="agreeToTerms" />
      Я согласен с условиями
    </label>

    <!-- BUTTON -->
    <button
      @click="makeOrder"
      :disabled="!agreeToTerms || !selectedAddressId || cartI.items.length === 0 || !kaspiPhone"
      class="w-full bg-gray-900 text-white py-4 rounded-lg font-medium disabled:bg-gray-400"
    >
      Оформить заказ
    </button>

  </div>
</div>


        </div>
      </div>
    </div>

    <!-- DELETE MODAL -->
    <CustomModal v-if="deleteModal">
      <div class="fixed inset-0 flex items-center justify-center bg-black/50">
        <div class="bg-white p-6 rounded-2xl w-[90%] max-w-sm">
          <h3 class="text-lg font-semibold mb-4">Удалить адрес?</h3>
          <div class="flex gap-3">
            <button @click="closeDelete" class="flex-1 bg-gray-100 py-2 rounded">
              Отмена
            </button>
            <button @click="deleteAddress" class="flex-1 bg-red-600 text-white py-2 rounded">
              Удалить
            </button>
          </div>
        </div>
      </div>
    </CustomModal>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useCartStore } from "@/stores/Basket";
import { useAddressStore } from "@/stores/addressStore";
import CustomModal from "@/components/CustomModal.vue";

const cartI = useCartStore();
const store = useAddressStore();

const addresses = ref([]);
const selectedAddressId = ref(null);

const agreeToTerms = ref(false);

const deleteModal = ref(false);
const addressToDelete = ref(null);

const orderNote = ref("");

const image_url = import.meta.env.VITE_API_BASE_URL;

/* LOAD ADDRESSES */
const loadAddresses = async () => {
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}addresses/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
      },
    });
    addresses.value = res.data;
  } catch (err) {
    console.error("Ошибка загрузки адресов", err);
  }
};

onMounted(loadAddresses);

/* SELECT */
const selectAddress = (addr) => {
  selectedAddressId.value = addr.id;
  store.address = [addr];
};

/* DELETE */
const confirmDelete = (id) => {
  addressToDelete.value = id;
  deleteModal.value = true;
  document.body.style.overflow = "hidden";
};

const closeDelete = () => {
  deleteModal.value = false;
  addressToDelete.value = null;
  document.body.style.overflow = "";
};

const deleteAddress = async () => {
  try {
    await axios.delete(`${import.meta.env.VITE_API_BASE_URL}addresses/${addressToDelete.value}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
      },
    });
    addresses.value = addresses.value.filter(a => a.id !== addressToDelete.value);
    closeDelete();
  } catch (err) {
    console.error("Ошибка удаления адреса", err);
  }
};

/* CART */
const increaseQuantity = (id) => {
  const item = cartI.items.find(i => i.id === id);
  if (item) item.quantity++;
};

const decreaseQuantity = (id) => {
  const item = cartI.items.find(i => i.id === id);
  if (item && item.quantity > 1) item.quantity--;
};

const remove = (id) => {
  cartI.removeItem(id);
};

/* ORDER */
const makeOrder = async () => {
  if (!selectedAddressId.value) return;

  try {

    const kaspiPhone = ref(""); // состояние для номера Kaspi

// При makeOrder добавляем в тело запроса:
await axios.post(`${import.meta.env.VITE_API_BASE_URL}orders/`, {
  address_id: selectedAddressId.value,
  kaspi_number: kaspiPhone.value,
  dishes: cartI.items.map(i => ({
    dish_id: i.id,
    quantity: i.quantity
  })),
  note: orderNote.value
}, {
  headers: {
    Authorization: `Bearer ${localStorage.getItem("authToken")}`,
  },
});


    cartI.clearCart();
    alert("Заказ успешно оформлен!");
  } catch (err) {
    console.error("Ошибка оформления заказа", err);
    alert("Ошибка оформления заказа");
  }

};
</script>
