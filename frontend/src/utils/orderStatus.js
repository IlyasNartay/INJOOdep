import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

export async function fetchOrderMeta() {
  const response = await axios.get(`${API_BASE_URL}orders/meta`);
  return response.data;
}

export function getOrderStatusLabel(status, statusOptions = []) {
  return statusOptions.find((item) => item.value === status || item.key === status)?.label || status;
}

export function getOrderStatusClass(status, classMap = {}) {
  return classMap[status] || "bg-gray-100 text-gray-800 border border-gray-200";
}
