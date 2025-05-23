<script setup>
import { onMounted, ref, watch } from "vue";
import { useWebSocket } from "../composables/useWebSocket";
import { resolveImage, placeholderUrl } from "../composables/useImage";
const ws = useWebSocket();
const images = ref({});

onMounted(() => {
  watch(
    () => ws.receivedMessage.value,
    async (teachers) => {
      

      for (const teacher of teachers) {
        if (!teacher.card_id) {
          continue;
        }
        console.log("Resolving teacher");
        images.value[teacher.card_id.trim()] = await resolveImage(
          teacher.card_id.trim()
        );
      }
      console.log(images.value);
    },
    { immediate: true }
  );
});
</script>

<template>
  <div
    class="flex flex-row grow gap-4 w-full items-center justify-between max-h-4/8 "
  >
    <div
      v-for="teacher in ws.receivedMessage.value"
      :key="teacher.card_id"
      :id="teacher.card_id"
      class="drop-shadow-2xl backdrop-blur-3xl rounded-xl py-4 px-2 w-36 h-fit min-h-52 grid justify-center content-start border-2 border-blue-200"
    >
      <transition name="fade" mode="out-in">
        <img
          v-if="images[teacher.card_id?.trim?.()]"
          :src="images[teacher.card_id.trim()]"
          :key="teacher.card_id ? teacher.card_id + Math.random() : Math.random()"
          alt=""
          class="h-[16vh] object-contain self-center"
        />

        <img class="h-[16vh] object-contain self-center" v-else :src="placeholderUrl" alt="" />
      </transition>

      <label class="justify-self-center self-center pt-4">{{
        teacher.name ? teacher.name : ""
      }}</label>
      <label class="justify-self-center self-center">
        {{
        teacher.school ? teacher.school : ""
      }}
      </label>
    </div>
  </div>
</template>
<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
