<script setup>
import { useWebSocket } from "../composables/useWebSocket";
const ws = useWebSocket()
</script>

<template>
  <div class="flex flex-row grow gap-4 w-full items-center justify-between max-h-4/8">
    <div
      v-for="teacher in ws.receivedMessage.value"
      :key="teacher.card_id"
      :id="teacher.card_id"
      class="drop-shadow-2xl  backdrop-blur-3xl rounded-xl py-4 px-2 w-36 h-fit min-h-56 grid justify-center content-start border-2 border-blue-200"
    >
      <img
        :src="
          teacher.card_id
            ? 'http://192.168.2.17:8002/picture/employee/' +
            teacher.card_id
            : '/dash/placeholders.png'
        "
        alt=""
        class="h-[16vh] object-contain self-center"
      />
      <label class="justify-self-center self-center pt-4">{{
        teacher.name ? teacher.name : ""
      }}</label>
      <label class="justify-self-center self-center">{{ teacher.school ? teacher.school : "" }}</label>
    </div>
  </div>
</template>
