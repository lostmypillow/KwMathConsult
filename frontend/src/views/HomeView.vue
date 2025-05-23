<script setup>
import People from "../components/People.vue";
import VideoPlayer from "../components/VideoPlayer.vue";
const dummy = [
  // {
  //   id: 2,
  //   content: "efwssdsefwfwfw",
  //   author: "200024",
  //   created_at: "2025-05-23T19:39:47.002344",
  //   updated_at: null,
  // },
  // {
  //   id: 4,
  //   content: "212122121213 <p>meow</p>",
  //   author: "300003",
  //   created_at: "2025-05-23T20:02:11.848863",
  //   updated_at: null,
  // },
  // {
  //   id: 11,
  //   content: "212122121213 <p>meow</p>",
  //   author: "300003",
  //   created_at: "2025-05-23T20:07:36.056527",
  //   updated_at: null,
  // },

  {
    id: 11,
    content: `
   <h3 style="font-weight: revert; color: revert;">
  This should have its original font-weight (bold) and color: black
</h3>
<p>Just some text</p>

<p>Just some text</p>

`,
    author: "300003",
    created_at: "2025-05-23T20:07:36.056527",
    updated_at: null,
  }
];
</script>

<template>
  <People />
  <div
    className="grow-0 flex flex-row items-center justify-between max-w-svw gap-2 max-h-[52vh]"
  >
    <VideoPlayer />

    <Carousel
      class="flex w-full max-w-[60vw] h-full overflow-hidden"
      :value="dummy"
      :numVisible="1"
      :numScroll="1"
      :showIndicators="false"
      :showNavigators="false"
      circular
      :autoplayInterval="3000"
    >
      <template #item="slotProps">
        <Card class="flex h-full w-full rounded-2xl">
          <template #content>
            <p class="no-preflight" v-html="slotProps.data.content">
            </p>
          </template>
        </Card>
      </template>
    </Carousel>
  </div>
</template>
<style scoped>
::v-deep(.p-carousel-content-container),
::v-deep(.p-carousel-content),
::v-deep(.p-carousel-viewport),
::v-deep(.p-carousel-item-list) {
  height: 100%;
}

::v-deep(.p-card) {
  border-radius: 1rem;
}

.no-preflight, .no-preflight * {
  all: revert;
}
</style>
