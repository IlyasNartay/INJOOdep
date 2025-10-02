<script setup></script>

<template>
  <div class="loader-overlay">
    <span class="loader"></span>
  </div>
</template>

<style scoped>
.loader-overlay {
  position: fixed;
  inset: 0; /* top: 0; left: 0; right: 0; bottom: 0 */
  background-color: rgba(0, 0, 0, 0.4); /* полупрозрачный чёрный */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* поверх всего */
}

.loader {
  height: 48px;
  width: 48px;
  border: 5px solid #fff;
  border-bottom-color: #0059C1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  box-sizing: border-box;
}

/* Ключевые кадры для анимации вращения */
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
