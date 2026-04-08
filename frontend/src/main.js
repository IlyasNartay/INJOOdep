import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import 'leaflet/dist/leaflet.css'

import App from './App.vue'
import router from './router'
import "cropperjs/dist/cropper.css";
import { hydrateAuthState } from '@/utils/roles'
import { initializeLocale } from '@/i18n'

const app = createApp(App)

async function clearLegacyBrowserCache() {
  if (typeof window === "undefined") return;

  if ("serviceWorker" in navigator) {
    const registrations = await navigator.serviceWorker.getRegistrations();
    await Promise.all(registrations.map((registration) => registration.unregister()));
  }

  if ("caches" in window) {
    const keys = await caches.keys();
    await Promise.all(keys.map((key) => caches.delete(key)));
  }
}

app.use(createPinia())
app.use(router)

initializeLocale()

clearLegacyBrowserCache().catch(() => {
  // If cache cleanup fails, the app still continues normally.
})

hydrateAuthState().finally(() => {
  app.mount('#app')
})
