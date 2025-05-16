<script setup>
import { Dashboard } from "@uppy/vue";
import Uppy from "@uppy/core";
import { ref, watch, onMounted } from "vue";
import XHR from "@uppy/xhr-upload";
import DragDrop from "@uppy/drag-drop";
import ImageEditor from "@uppy/image-editor";
import "@uppy/image-editor/dist/style.min.css";
import { resolveCardholderImage } from "../composables/useImage";
// Don't forget the CSS: core and UI components + plugins you are using
import "@uppy/core/dist/style.css";
import "@uppy/dashboard/dist/style.css";
import { RouterView } from "vue-router";

const uppy = new Uppy({
  restrictions: {
    allowedFileTypes: ["image/*"],
  },
})
  .use(XHR, { endpoint: "http://localhost:8000/picture/200024" })
  .use(ImageEditor, {
    quality: 0.8,
    actions: {
      revert: true,
      rotate: true,
      granularRotate: true,
      flip: true,
      zoomIn: true,
      zoomOut: true,
      cropSquare: false,
      cropWidescreen: false,
      cropWidescreenVertical: false,
    },
    cropperOptions: {
      viewMode: 1,
      dragMode: "move",
      aspectRatio: 320 / 240,
      autoCropArea: 1,
      minCropBoxWidth: 320,
      minCropBoxHeight: 240,
      ready() {
        // This ensures the crop box is forced to 320x240
        this.cropper.setCropBoxData({
          width: 320,
          height: 240,
        });
      },
    },
  });
const showDash = ref(false);
const inputNum = ref("");
const imageSrc = ref("");
onMounted(() => {
  watch(
    () => inputNum.value,
    async (cardId) => {
      if (cardId.length < 6) {
        return;
      }

      imageSrc.value = await resolveCardholderImage(cardId);
    },
    { immediate: true }
  );
});
</script>

<template>
  <div class="flex flex-col items-start justify-start w-full h-full p-4 gap-4">
    <h1>Edit details</h1>
    <div class="w-full flex flex-row gap-4 items-center justify-start">
      <label for="input">sign ehre:</label
      ><input class="p-4 rounded-full" v-model="inputNum" />
    </div>
    <div class="w-full flex flex-row gap-4 items-start justify-start">
      <label for="img">Your image: </label>
      <transition name="fade" mode="out-in">
        <img
          v-if="imageSrc != ''"
          :src="imageSrc"
          alt=""
          class="object-contain"
        />

        <img v-else src="/dash/placeholder.png" alt="" />
      </transition>
      <button @click="showDash = !showDash">open</button>
      <Dashboard
        v-show="showDash"
        :props="{
          proudlyDisplayPoweredByUppy: false,
          autoOpen: 'imageEditor',
          inline: true,
        }"
        :uppy="uppy"
      />
    </div>

    {{ inputNum }}
  </div>
</template>
