<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from "vue";
import axios from "axios";

// Retry settings
const RETRY_DELAY = 2000; // 2 seconds delay

const fileName = ref("");
const videoURL = computed(() => "http://" + import.meta.env.VITE_VIDEO_URL + "/video/" + fileName.value);
const videoPlayerRef = ref(null);

let stopped = false;
let retryInProgress = false;
let abortController = null;
let inactivityTimeout = null;

// Function to retry an action indefinitely until it succeeds
const retryAction = async (action) => {
  if (retryInProgress) return;

  retryInProgress = true;

  while (!stopped) {
    try {
      // Cancel any pending request before retrying
      if (abortController) abortController.abort();

      abortController = new AbortController();
      await action(abortController.signal);
      retryInProgress = false;
      return; // Success — exit loop
    } catch (error) {
      if (axios.isCancel(error)) {
        console.warn("[VideoPlayer.vue] Request aborted, skipping retry...");
        retryInProgress = false;
        return;
      }

      console.error("[VideoPlayer.vue] Retry failed:", error);
      await new Promise((resolve) => setTimeout(resolve, RETRY_DELAY));
    }
  }

  retryInProgress = false;
};

// Function to get the next video
const attemptGetNext = async (signal) => {
  console.log("[VideoPlayer.vue] [" + new Date().toISOString() + "] Executing getNext()");

  const response = await axios.get(
    "http://" + import.meta.env.VITE_VIDEO_URL + "/next",
    { signal }
  );

  if (response.status !== 200 || response.data === null) {
    throw new Error("Failed to get next video or data is null");
  }

  console.log("[VideoPlayer.vue] [" + new Date().toISOString() + "] Video file name received: ", response.data);

  if (videoPlayerRef.value) {
    videoPlayerRef.value.src = '';
    fileName.value = response.data;
    videoPlayerRef.value.src = videoURL.value;
    videoPlayerRef.value.load();
    videoPlayerRef.value.play();
  }
};

// Function to handle video player errors
const handleError = (event) => {
  console.error("[VideoPlayer.vue] Video playback error:", event);
  retryAction(attemptGetNext);
};

// Function to detect inactivity (paused or stopped state)
const setupInactivityWatch = () => {
  if (inactivityTimeout) clearTimeout(inactivityTimeout);

  inactivityTimeout = setTimeout(() => {
    if (
      videoPlayerRef.value &&
      videoPlayerRef.value.paused &&
      !videoPlayerRef.value.ended
    ) {
      console.warn("[VideoPlayer.vue] Detected inactivity — retrying...");
      retryAction(attemptGetNext);
    }
  }, 5000); // 5 seconds of inactivity triggers retry
};

// Watch video state to detect inactivity
watch(
  () => videoPlayerRef.value?.paused,
  (paused) => {
    if (paused) setupInactivityWatch();
  }
);

onMounted(async () => {
  console.log("[VideoPlayer.vue] Component mounted, calling getNext()");
  await retryAction(attemptGetNext);

  // Attach error and inactivity watchers
  if (videoPlayerRef.value) {
    videoPlayerRef.value.addEventListener("error", handleError);
    videoPlayerRef.value.addEventListener("play", setupInactivityWatch);
    videoPlayerRef.value.addEventListener("pause", setupInactivityWatch);
  }
});

onUnmounted(() => {
  console.log("[VideoPlayer.vue] Component unmounted, stopping retries...");
  stopped = true;
  if (abortController) abortController.abort(); // Cancel any ongoing request
  if (inactivityTimeout) clearTimeout(inactivityTimeout);
});
</script>
<template>
  <div className="grow-0 flex flex-row items-center justify-between w-full max-h-[52vh]">
    <video ref="videoPlayerRef"  autoplay className="h-full object-contain rounded-xl drop-shadow-2xl"  @ended="retryAction(attemptGetNext)">
      <source :src="videoURL" type="video/mp4" />
    </video>
<div></div>
  </div>
</template>
