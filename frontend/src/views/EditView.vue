<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import { resolveImage } from "../composables/useImage";
import { Cropper } from "vue-advanced-cropper";
import "vue-advanced-cropper/dist/style.css";
import FileUpload from "primevue/fileupload";
import InputGroup from "primevue/inputgroup";
import InputText from "primevue/inputtext";
import axios from "axios";
import { placeholderUrl } from "../composables/useImage";
import { useAPI } from "../composables/useAPI";
import { useToast } from "primevue";
import type { teacherData } from "../types/teacherData";
import { defaultTeacher } from "../types/teacherData";
const api = useAPI();
const fileUploadRef = ref();
const inputNum = ref("");
const imageSrc = ref("");
const rawImage = ref(null);
const showEditor = ref(false);
const cropperRef = ref(null);
const croppedCanvas = ref(null);
const toast = useToast();
const updateBtnStatus = ref("");
const updateBtnDisabled = ref(false);
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
  try {
    await api.uploadImage(canvas, inputNum.value);
    fileUploadRef.value?.clear();
    imageSrc.value = "";
    imageSrc.value = await resolveImage(inputNum.value);
    toast.add({
      severity: "success",
      summary: "Success",
      detail: "Image upload successful!",
      life: 3000,
    });
  } catch (error) {
    console.error(error);
    toast.add({
      severity: "error",
      summary: "Error",
      detail: "Image upload unsuccessful!",
      life: 3000,
    });
  }
};
const teacherData = ref<teacherData>({
  ...defaultTeacher,
});

const updateCollege = async () => {
  updateBtnDisabled.value = true;
  try {
    await api.updateCollege(teacherData.value);
    toast.add({
      severity: "success",
      summary: "Success",
      detail: "College update successful!",
      life: 3000,
    });
  } catch (error) {
    console.error(error);
    toast.add({
      severity: "error",
      summary: "Error",
      detail: "College update unsuccessful!",
      life: 3000,
    });
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
      imageSrc.value = await resolveImage(cardId);
      teacherData.value = await api.getTeacherInfo(inputNum.value);
    },
    { immediate: true }
  );
});
const announcementText = ref("");
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
          autoFocus
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
        />
      </div>

      <InputGroup class="px-7 self-end">
        <Textarea
          :disabled="inputNum.length < 6"
          v-model="teacherData.大學"
          placeholder="輸入學歷" />

        <Button
          class="shrink-0"
          icon="pi pi-sync"
          size="small"
          @click="updateCollege"
          :severity="updateBtnStatus"
          :disabled="inputNum.length < 6"
          label="更新"
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
        <template #end>
          <Button disabled severity="success" icon="pi pi-save" label="存檔"
        /></template>
      </Toolbar>
      <Button @click="console.log(announcementText)"></Button>
      <Editor v-model="announcementText" class="flex-1 w-full">
        <template #toolbar>
          <span class="ql-formats">
            <select class="ql-header">
              <option selected></option>
              <option value="1"></option>
              <option value="2"></option>
              <option value="3"></option>
            </select>
          </span>
          <span class="ql-formats">
            <button class="ql-bold"></button>
            <button class="ql-italic"></button>
          </span>
        </template>
      </Editor>
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
