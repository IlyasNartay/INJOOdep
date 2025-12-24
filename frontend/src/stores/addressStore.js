import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAddressStore = defineStore('address', () => {
  const address = ref('')
  const entrance = ref('')
  const floor = ref('')
  const apartment = ref('')

  // Функция для установки всех данных сразу
  function setFullAddress(data) {
    address.value = data.address || ''
    entrance.value = data.entrance || ''
    floor.value = data.floor || ''
    apartment.value = data.apartment || ''
  }

  // Оставляем для совместимости, если нужно менять только строку адреса
  function setAddress(newAddress) {
    address.value = newAddress
  }

  return { address, entrance, floor, apartment, setAddress, setFullAddress }
})