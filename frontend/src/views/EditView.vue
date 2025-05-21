<script setup>
import { ref, watch, onMounted } from "vue";
import { resolveCardholderImage } from "../composables/useImage";
import { Cropper } from "vue-advanced-cropper";
import "vue-advanced-cropper/dist/style.css";
import FileUpload from "primevue/fileupload";
import InputGroup from 'primevue/inputgroup';
import InputGroupAddon from 'primevue/inputgroupaddon';
import InputText from 'primevue/inputtext';
import { validate } from "uuid";

const inputNum = ref("");
const imageSrc = ref("");
const rawImage = ref(null);
const showEditor = ref(false);
const cropperRef = ref(null);
const croppedCanvas = ref(null);

const onSelect = ({ files }) => {
  console.log("selected")
  try {
    const file = files[0];
    console.log(file)
  if (file && file.type.startsWith("image/")) {
    const reader = new FileReader();
    reader.onload = () => {
      rawImage.value = reader.result;
      showEditor.value = true;
    };
    reader.readAsDataURL(file);
  }
  } catch (error) {
    console.error(error)
  }
  
};

const cropImage = () => {
  if (cropperRef.value) {
    const canvas = cropperRef.value.getResult().canvas;
    if (canvas) {
      croppedCanvas.value = canvas.toDataURL("image/jpeg");
      uploadCroppedImage(canvas);
      showEditor.value = false;
    }
  }
};

const uploadCroppedImage = async (canvas) => {
  const blob = await new Promise(resolve => canvas.toBlob(resolve, "image/jpeg", 0.8));
  const formData = new FormData();
  formData.append("file", blob, "cropped.jpg");

  await fetch(`http://localhost:8000/picture/200024`, {
    method: "POST",
    body: formData,
  });
};

onMounted(() => {
  watch(
    () => inputNum.value,
    async (cardId) => {
      if (cardId.length < 6) return;
      imageSrc.value = await resolveCardholderImage(cardId);
    },
    { immediate: true }
  );
});
</script>

<template>
  <div class="flex flex-col items-start justify-start w-full h-full p-4 gap-4">
    <InputGroup>
      <InputGroupAddon>
        <i class="pi pi-user"></i>
      </InputGroupAddon>
      <InputText v-model="inputNum" placeholder="員工編號" />
    </InputGroup>

    <div class="w-full flex flex-row gap-4 items-center justify-start">
      <label for="input"></label>
      <input
        class="p-4 rounded-full w-28 text-2xl"
        v-model="inputNum"
        autofocus
      />
    </div>

    <div class="w-full flex flex-row gap-4 items-start justify-start">
      <label for="img">員工照片: </label>
      <transition name="fade" mode="out-in">
        <img
          v-if="imageSrc !== ''"
          :src="imageSrc"
          alt=""
          class="object-contain h-60"
        />
        <img v-else src="/dash/placeholder.png" alt="" />
      </transition>
    </div>

    <FileUpload
      mode="basic"
      name="image"
      accept="image/*"
      customUpload
      @select="onSelect"
  
      chooseLabel="選擇圖片"
    />
    <!-- <img  alt=""> -->

    <Dialog v-model:visible="showEditor" modal >
      <Cropper
        ref="cropperRef"
        :src="rawImage"
        :stencil-props="{ aspectRatio: 320 / 240, minWidth: 320, minHeight: 240 }"
        :autoZoom="true"
        :resizeImage="true"
        image-restriction="fill-area"
        class="cropper h-[400px] w-[600px]"
      />
      <button class="mt-2 px-4 py-2 bg-green-600 text-white rounded" @click="cropImage">裁剪並上傳</button>
    </Dialog>
  </div>
</template>
