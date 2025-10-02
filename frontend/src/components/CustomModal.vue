<script setup>
const props = defineProps({
  success: Boolean,
});
</script>

<template>
  <div class="fixed inset-0 flex justify-center items-center z-50">
    <div class="absolute inset-0 backdrop-blur-sm"></div>
    <div
      class="relative inset-0 backdrop-blur-sm z-10 w-[500px] flex justify-center items-center"
    >
      <slot></slot>
    </div>
  </div>
</template>
