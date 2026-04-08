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

app.use(createPinia())
app.use(router)

initializeLocale()

hydrateAuthState().finally(() => {
  app.mount('#app')
})
