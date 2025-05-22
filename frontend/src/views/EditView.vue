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
import { placeholderUrl } from "../composables/useImage";
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

  await fetch(
    `http://${import.meta.env.VITE_FASTAPI_URL}/picture/${inputNum.value}`,
    {
      method: "POST",
      body: formData,
    }
  );
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

    await axios.post(`http://${import.meta.env.VITE_FASTAPI_URL}/update`, x);
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
        await fetch(
          `http://${import.meta.env.VITE_FASTAPI_URL}/0/${inputNum.value}`,
          {
            method: "GET",
          }
        )
      ).json();
    },
    { immediate: true }
  );
});
</script>

<template>
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
      class="mt-2 px-4 py-2 bg-green-600 text-white rounded mr-0"
      @click="cropImage"
    >
      裁剪並上傳
    </button>
  </Dialog>
  <div
    class="flex flex-row items-start justify-between gap-4 w-full h-full max-h-svh p-4"
  >
    <div
      class="drop-shadow-2xl backdrop-blur-3xl rounded-xl py-4 px-2 w-72 h-full flex flex-col items-center justify-between gap-4 border-2 border-blue-200"
    >
      <transition name="fade" mode="out-in">
        <img
          v-if="imageSrc !== ''"
          :src="imageSrc"
          alt=""
          class="h-[32vh] object-contain self-center"
        />
        <img
          class="h-[32vh] object-contain self-center"
          v-else
          :src="placeholderUrl"
          alt=""
        />
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
          </p>
          <Button @click="inputNum = ''">Change</Button>
        </div>
      </InputGroup>
      <div class="px-4">
        <FileUpload
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
        />
      </div>

      <InputGroup class="px-7 self-end">
        <Textarea
          :disabled="inputNum.length < 6"
          v-model="teacherData.大學"
          placeholder="輸入學歷" />

        <Button
          class="shrink-0"
          @click="updateCollege"
          :severity="updateBtnStatus"
          :disabled="inputNum.length < 6"
          :label="updateBtnText"
        ></Button
      ></InputGroup>
    </div>
    <div
      class="flex flex-col items-center justify-start w-full h-[60vh] drop-shadow-2xl backdrop-blur-3xl rounded-xl gap-4"
    >
      <Toolbar class="w-full">
        <template #start>
          <Button severity="info" icon="pi pi-plus" label="新增公告" />
          <Button severity="danger" icon="pi pi-times" label="取消新增" />
        </template>
        <template #center>
          <Button disabled icon="pi pi-eye" label="預覽"
        /></template>
        <template #end> <Button disabled severity="success" icon="pi pi-save" label="存檔" /></template>
      </Toolbar>
      
      <Editor v-model="value" class="flex-1 w-full" />
    </div>
  </div>
</template>
<style scoped>
::v-deep(span[class=""]) {
  display: none;
}

::v-deep(.ql-editor) {
  font-size: 16px;
}
</style>
