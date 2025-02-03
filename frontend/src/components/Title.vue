<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
const time = ref(new Date());
const updateTime = () => {
  time.value = new Date();
};

const interval = ref(null);
const formatTime = (date) => {
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  const seconds = String(date.getSeconds()).padStart(2, "0");
  return `${hours}:${minutes}:${seconds}`;
};
const formatDate = (date) => {
  const options = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  };
  return date.toLocaleDateString("zh-TW", options);
};
const formattedTime = computed(() => formatTime(time.value));
const formattedDate = computed(() => formatDate(time.value));
onUnmounted(() => clearInterval(interval.value));
onMounted(() => (interval.value = setInterval(updateTime, 1000)));
</script>

<template>
  <div class="flex items-center justify-between h-1/8 w-full px-2">
    <div class="flex flex-row gap-4 items-center justify-center">
      <img src="/logo.webp" alt="logo" />
      <p class="text-2xl">高偉數學輔導系统</p>
    </div>

    <p>
      {{ formattedDate }} 
      <span class="font-mono">{{ formattedTime }}</span>
    </p>
  </div>
</template>