import axios from "axios";
import { ref } from "vue";

export const USER_ROLES = Object.freeze({
  ADMIN: "admin",
  STAFF: "staff",
  CUSTOMER: "customer",
});

export const ROLE_LABELS = Object.freeze({
  [USER_ROLES.ADMIN]: "Администратор",
  [USER_ROLES.STAFF]: "Менеджер",
  [USER_ROLES.CUSTOMER]: "Клиент",
});

export const ROLE_OPTIONS = Object.freeze([
  { value: USER_ROLES.ADMIN, label: ROLE_LABELS[USER_ROLES.ADMIN] },
  { value: USER_ROLES.STAFF, label: ROLE_LABELS[USER_ROLES.STAFF] },
  { value: USER_ROLES.CUSTOMER, label: ROLE_LABELS[USER_ROLES.CUSTOMER] },
]);

export const AUTH_USER_ROLES = Object.freeze(Object.values(USER_ROLES));
export const ADMIN_ROLES = Object.freeze([USER_ROLES.ADMIN]);
export const ADMIN_STAFF_ROLES = Object.freeze([USER_ROLES.ADMIN, USER_ROLES.STAFF]);
export const CUSTOMER_ROLES = Object.freeze([USER_ROLES.CUSTOMER]);

export const SESSION_MODES = Object.freeze({
  AUTH: "auth",
  GUEST: "guest",
});

const KNOWN_USER_ROLES = new Set(Object.values(USER_ROLES));
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

const readStoredUserRole = () => normalizeUserRole(localStorage.getItem("userRole"));
const readStoredSessionMode = () => localStorage.getItem("sessionMode") || (readStoredUserRole() ? SESSION_MODES.AUTH : SESSION_MODES.GUEST);

export const currentUserRole = ref(readStoredUserRole());
export const currentSessionMode = ref(readStoredSessionMode());

export function normalizeUserRole(role) {
  return KNOWN_USER_ROLES.has(role) ? role : null;
}

export function getRoleLabel(role) {
  return ROLE_LABELS[role] || role || "";
}

export function getStoredUserRole() {
  return currentUserRole.value;
}

export function getSessionMode() {
  return currentSessionMode.value;
}

export function canUseCustomerUi() {
  const role = currentUserRole.value;
  return !role || role === USER_ROLES.CUSTOMER;
}

export function setSessionMode(mode) {
  const nextMode = mode === SESSION_MODES.AUTH ? SESSION_MODES.AUTH : SESSION_MODES.GUEST;
  currentSessionMode.value = nextMode;
  localStorage.setItem("sessionMode", nextMode);
  return nextMode;
}

export function syncAuthStorage(role) {
  const normalizedRole = normalizeUserRole(role);

  if (normalizedRole) {
    currentUserRole.value = normalizedRole;
    currentSessionMode.value = SESSION_MODES.AUTH;
    localStorage.setItem("userRole", normalizedRole);
    localStorage.setItem("sessionMode", SESSION_MODES.AUTH);
  } else {
    currentUserRole.value = null;
    currentSessionMode.value = SESSION_MODES.GUEST;
    localStorage.removeItem("userRole");
    localStorage.setItem("sessionMode", SESSION_MODES.GUEST);
  }

  return normalizedRole;
}

export function clearAuthStorage() {
  currentUserRole.value = null;
  currentSessionMode.value = SESSION_MODES.GUEST;
  localStorage.removeItem("authToken");
  localStorage.removeItem("userRole");
  localStorage.removeItem("userStatus");
  localStorage.setItem("sessionMode", SESSION_MODES.GUEST);
}

export function sanitizeAuthStorage() {
  const storedRole = localStorage.getItem("userRole");
  const normalizedRole = normalizeUserRole(storedRole);

  if (storedRole && !normalizedRole) {
    localStorage.removeItem("userRole");
  }

  currentUserRole.value = normalizedRole;
  return normalizedRole;
}

export async function fetchAuthMeta() {
  const response = await axios.get(`${API_BASE_URL}auth/meta`);
  return response.data;
}

export async function hydrateAuthState() {
  const token = localStorage.getItem("authToken");
  if (!token) {
    currentUserRole.value = null;
    currentSessionMode.value = SESSION_MODES.GUEST;
    return null;
  }

  try {
    const response = await axios.get(`${API_BASE_URL}auth/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: "application/json",
      },
    });

    const user = response.data;
    const normalizedRole = normalizeUserRole(user.role);

    if (!normalizedRole) {
      throw new Error("Unknown role from auth/me");
    }

    currentUserRole.value = normalizedRole;
    currentSessionMode.value = SESSION_MODES.AUTH;
    localStorage.setItem("userRole", normalizedRole);
    localStorage.setItem("userStatus", user.status);
    localStorage.setItem("sessionMode", SESSION_MODES.AUTH);
    return user;
  } catch (error) {
    clearAuthStorage();
    return null;
  }
}

if (typeof window !== "undefined") {
  window.addEventListener("storage", (event) => {
    if (event.key === "userRole") {
      currentUserRole.value = normalizeUserRole(event.newValue);
    }

    if (event.key === "sessionMode") {
      currentSessionMode.value = event.newValue || (currentUserRole.value ? SESSION_MODES.AUTH : SESSION_MODES.GUEST);
    }
  });
}
