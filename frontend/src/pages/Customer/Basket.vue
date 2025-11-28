<script setup>
import {ref} from "vue";
import {Plus as PlusIcon, Minus as MinusIcon} from "lucide-vue-next";
import {useCartStore} from "/src/stores/Basket.js";
import CustomModal from "@/components/CustomModal.vue";
import axios from "axios";
import Loader from "@/components/Loader.vue";
import {useAddressStore} from '@/stores/addressStore';

const cartI = useCartStore();
const store = useAddressStore();

const isLoading = ref(false);
const success = ref(false);
const orderNote = ref("");
const agreeToTerms = ref(false);

const role = localStorage.getItem("userRole");
const table_id = ref(localStorage.getItem("selectedTable"));

const image_url = `${import.meta.env.VITE_API_BASE_URL}`;

/* ------------ METHODS ------------- */

function remove(id) {
  cartI.removeItem(id);
}

const increaseQuantity = (itemId) => {
  const item = cartI.items.find((item) => item.id === itemId);
  if (item) item.quantity++;
};

const decreaseQuantity = (itemId) => {
  const item = cartI.items.find((item) => item.id === itemId);
  if (item && item.quantity > 1) item.quantity--;
};

/* ---------- Checkout (Guest) ---------- */

const handleCheckoutForGuest = async () => {
  if (!table_id.value) {
    console.error("❌ table_id not found");
    return;
  }

  isLoading.value = true;

  const checkoutData = {
    table_id: Number(table_id.value),
    order_dishes: cartI.items.map((item) => ({
      dish_id: item.id,
      quantity: item.quantity,
    })),
    note: orderNote.value || ""
  };

  try {
    const response = await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}orders/table`,
        checkoutData
    );

    console.log("Guest order success:", response.data);

    success.value = true;
    cartI.clearCart();
  } catch (error) {
    console.error("Guest checkout error:", error.response?.data || error);
  } finally {
    isLoading.value = false;
  }
};

/* ---------- Checkout (Authorized User) ---------- */

const handleCheckout = async () => {
  if (!store.address?.[0]?.id) {
    alert("❗ Выберите адрес перед оформлением заказа.");
    return;
  }

  isLoading.value = true;

  const checkoutData = {
    address_id: store.address[0].id,
    dishes: cartI.items.map((item) => ({
      dish_id: item.id,
      quantity: item.quantity
    })),
    note: orderNote.value || ""
  };

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

    console.log("Checkout success:", response.data);
    success.value = true;
    cartI.clearCart();
  } catch (error) {
    console.error("Checkout error:", error.response?.data || error);
  } finally {
    isLoading.value = false;
  }
};

/* ---------- Button Handler ---------- */
const makeCheckout = () => {
  if (role === "guest") {
    handleCheckoutForGuest();
  } else {
    handleCheckout();
  }
};
</script>
