// stores/addressStore.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAddressStore = defineStore('address', () => {
  const address = ref([])

  function setAddress(newAddress) {
    address.value = newAddress
  }

  return { address, setAddress }
})
