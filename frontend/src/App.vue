<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Header from './pages/MainPage/Header.vue';
import Menu from './pages/MainPage/Menu.vue';
import FAQ from './pages/MainPage/FAQ.vue';
import Map from './pages/MainPage/Map.vue';
</script>

<template>
  <!-- <header>

<Menu/>
<FAQ/>
  </header>
<div>
<Map/>

</div> -->
  <RouterView />
</template>

<style scoped>

</style>
