// stores/cart.js
import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
  }),

  actions: {
    clearCart() {
      this.items = [];
    },
    increaseQuantity(id) {
      const item = this.items.find((entry) => entry.id === id);
      if (item) {
        item.quantity += 1;
      }
    },
    decreaseQuantity(id) {
      const item = this.items.find((entry) => entry.id === id);
      if (item && item.quantity > 1) {
        item.quantity -= 1;
      }
    },
    toggleItem(restaurant) {
      const index = this.items.findIndex((item) => item.id === restaurant.id)
      if (index !== -1) {
        this.items.splice(index, 1) // удалить
      } else {
        this.items.push({
          ...restaurant,
          quantity: 1,
        })
      }
    },
    isInCart(id) {
      return this.items.some((item) => item.id === id)
    },
    removeItem(id) {
      this.items = this.items.filter((item) => item.id !== id)
    },
  },

  getters: {
    // Считает итоговую сумму всех товаров
    totalPrice(state) {
      return state.items.reduce((total, item) => {
        return total + item.price * item.quantity
      }, 0)
    },

    // Возвращает товары с индивидуальной ценой total
    itemsWithTotal(state) {
      return state.items.map((item) => ({
        ...item,
        total: item.price * item.quantity,
      }))
    }
  }
})
