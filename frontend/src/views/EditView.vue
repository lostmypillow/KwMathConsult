<script setup>
import { ref, watch, onMounted, reactive } from "vue";
import { resolveCardholderImage } from "../composables/useImage";
import { Cropper } from "vue-advanced-cropper";
import "vue-advanced-cropper/dist/style.css";
import FileUpload from "primevue/fileupload";
import InputGroup from "primevue/inputgroup";
import InputGroupAddon from "primevue/inputgroupaddon";
import InputText from "primevue/inputtext";
import { validate } from "uuid";
import axios from "axios";
const fileUploadRef = ref();
const inputNum = ref("");
const imageSrc = ref("");
const rawImage = ref(null);
const showEditor = ref(false);
const cropperRef = ref(null);
const croppedCanvas = ref(null);

const onSelect = ({ files }) => {
  console.log("selected");
  try {
    const file = files[0];
    console.log(file);
    if (file && file.type.startsWith("image/")) {
      const reader = new FileReader();
      reader.onload = () => {
        rawImage.value = reader.result;
        showEditor.value = true;
      };
      reader.readAsDataURL(file);
    }
  } catch (error) {
    console.error(error);
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
  const blob = await new Promise((resolve) =>
    canvas.toBlob(resolve, "image/jpeg", 1)
  );
  const formData = new FormData();
  formData.append("file", blob, "cropped.jpg");

  await fetch(`http://${window.location.host}/picture/${inputNum.value}`, {
    method: "POST",
    body: formData,
  });
  fileUploadRef.value?.clear();
  imageSrc.value = "";
  imageSrc.value = await resolveCardholderImage(inputNum.value);
};
const college = ref("");
const teacherData = ref({
  姓名: "",
  大學: "",
});
const updateBtnStatus = ref("");
const updateBtnText = ref("更新");
const updateBtnDisabled = ref(false);
const updateCollege = async () => {
  updateBtnDisabled.value = true;
  try {
    const x = teacherData.value;

    await axios.post(`http://${window.location.host}/update`, x);
    updateBtnStatus.value = "success";
    updateBtnText.value = "更新成功!";
    setTimeout(() => {
      updateBtnStatus.value = "";
      updateBtnText.value = "更新";
    }, 3000);
  } catch (error) {
    console.error(error);
    updateBtnStatus.value = "success";
    updateBtnText.value = "更新失敗!";
    setTimeout(() => {
      updateBtnStatus.value = "danger";
      updateBtnText.value = "更新";
    }, 3000);
  }
  updateBtnDisabled.value = false;
};
onMounted(() => {
  watch(
    () => inputNum.value,
    async (cardId) => {
      if (cardId.length < 6) {
        imageSrc.value = "";
        teacherData.value = { 姓名: "", 大學: "" };
        return;
      }
      imageSrc.value = await resolveCardholderImage(cardId);
      teacherData.value = await (
        await fetch(`http://${window.location.host}/0/${inputNum.value}`, {
          method: "GET",
        })
      ).json();
    },
    { immediate: true }
  );
});
</script>

<template>
  <div class="flex flex-row items-center justify-center w-full h-full p-4">
    <div
      class="drop-shadow-2xl backdrop-blur-3xl rounded-xl py-4 px-2 w-72 h-full flex flex-col items-center justify-center gap-4 border-2 border-blue-200"
    >
      <transition name="fade" mode="out-in">
        <img
          v-if="imageSrc !== ''"
          :src="imageSrc"
          alt=""
          class="h-[32vh] object-contain self-center"
        />
        <img v-else :src="`${window.location.host}/dash/placeholder.png`" alt="" />
      </transition>

      <InputGroup class="px-7">
        <InputText
          v-if="teacherData.姓名 === ''"
          class="w-full"
          v-model="inputNum"
          placeholder="輸入員工編號"
        />
        <div v-else class="flex flex-row gap-2 w-full items-center px-2">
          <p class="flex flex-grow">
            {{ teacherData.姓名 }}
            <!-- meow -->
          </p>
          <Button @click="inputNum = ''">Change</Button>
        </div>
      </InputGroup>
      <div class="px-7">
        <FileUpload
          class="px-7"
          ref="fileUploadRef"
          mode="basic"
          :disabled="inputNum.length < 6"
          name="image"
          accept="image/*"
          customUpload
          @select="onSelect"
          chooseLabel="選擇圖片"
          :pt="{
            filename: { style: 'display: none' },
          }"
        >
        </FileUpload>
      </div>

      <InputGroup class="px-7">
        <InputText
          :disabled="inputNum.length < 6"
          v-model="teacherData.大學"
          placeholder="XX大學" />

        <Button
          @click="updateCollege"
          :severity="updateBtnStatus"
          :disabled="inputNum.length < 6"
          :label="updateBtnText"
        ></Button
      ></InputGroup>
    </div>

    <div class="flex flex-col items-start justify-start gap-4"></div>

    <Dialog header="裁剪" v-model:visible="showEditor" modal>
      <Cropper
        ref="cropperRef"
        :src="rawImage"
        :stencil-props="{
          aspectRatio: 320 / 240,
          minWidth: 320,
          minHeight: 240,
        }"
        :autoZoom="true"
        :resizeImage="true"
        image-restriction="none"
        class="cropper h-[400px] w-[600px]"
      />
      <button
        class="mt-2 px-4 py-2 bg-green-600 text-white rounded"
        @click="cropImage"
      >
        裁剪並上傳
      </button>
    </Dialog>
  </div>
</template>
<style scoped></style>
