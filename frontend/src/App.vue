<script setup>
import { RouterView } from 'vue-router'
import LanguageSwitcher from './components/LanguageSwitcher.vue'
import Footer from './components/Footer.vue'
</script>

<template>
  <div class="fixed right-4 top-4 z-[70]">
    <LanguageSwitcher />
  </div>
  <RouterView />
  <Footer/>
</template>
