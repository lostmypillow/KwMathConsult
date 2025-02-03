<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";

const data = ref(
  Array.from({ length: 6 }, (_, i) => ({
    device: i + 1,
    teacher: "",
    school: "",
    image: "",
  }))
);

const connectWebSocket = () => {
  const socket = new WebSocket("ws://192.168.2.6:8001/ws");

  socket.onmessage = (event) => {
    const receivedData = JSON.parse(event.data);
    console.log(receivedData);
    data.value = data.value.map((item) =>
      item.device === receivedData["device"] ? { ...receivedData } : item
    );
    console.log(data.value);
  };

  onUnmounted(() => {
    if (socket.readyState === WebSocket.OPEN) {
      socket.close();
    }
  });
};

onMounted(() => {
  connectWebSocket();
  // interval.value = setInterval(updateTime, 1000);
});
</script>

<template>
  <div class="flex flex-row grow gap-4 w-full items-center justify-between max-h-4/8">
    <div
      v-for="(datum, index) in data"
      :key="index"
      :id="index"
      class="drop-shadow-2xl h-fit backdrop-blur-3xl rounded-xl py-4 px-2 w-36 h-48 grid justify-center content-start border-2"
    >
      <img
        :src="
          datum.image
            ? 'http://192.168.2.7/kwweb/classpeople/other/stuphoto.asp?check=emp&id=' +
              datum.image
            : '/placeholder.png'
        "
        alt=""
        class="h-[16vh] object-contain self-center"
      />
      <label class="justify-self-center self-center pt-4">{{
        datum.teacher
      }}</label>
      <label class="justify-self-center self-center">{{ datum.school }}</label>
    </div>
  </div>
</template>
