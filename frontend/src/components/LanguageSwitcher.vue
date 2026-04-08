<template>
  <label class="flex items-center gap-2 rounded-2xl border border-white/10 bg-slate-950/70 px-3 py-2 text-sm text-white shadow-xl backdrop-blur">
    <span class="text-white/60">{{ t("lang.label") }}</span>
    <select :value="locale" class="bg-transparent outline-none" @change="setLocale($event.target.value)">
      <option v-for="option in languageOptions" :key="option.value" :value="option.value" class="text-slate-950">
        {{ option.label }}
      </option>
    </select>
  </label>
</template>

<script setup>
import { languageOptions, locale, setLocale, t } from "@/i18n";
</script>
