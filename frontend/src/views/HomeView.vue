<script setup>
import People from "../components/People.vue";
import VideoPlayer from "../components/VideoPlayer.vue";
const dummy = [
  {
    id: "1000",
    code: "f230fh0g3",
    name: "Bamboo Watch",
    description: "Product Description",
    image: "bamboo-watch.jpg",
    price: 65,
    category: "Accessories",
    quantity: 24,
    inventoryStatus: "INSTOCK",
    rating: 5,
  },
  {
    id: "1000",
    code: "f230fh0g3",
    name: "Bamboo Watch",
    description: "Product Description",
    image: "bamboo-watch.jpg",
    price: 65,
    category: "Accessories",
    quantity: 24,
    inventoryStatus: "INSTOCK",
    rating: 5,
  },
  {
    id: "1000",
    code: "f230fh0g3",
    name: "Bamboo Watch",
    description: "Product Description",
    image: "bamboo-watch.jpg",
    price: 65,
    category: "Accessories",
    quantity: 24,
    inventoryStatus: "INSTOCK",
    rating: 5,
  },
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
        <Card class="flex h-full w-fit rounded-2xl">
          <template #content>
            <p class="m-0">
              Lorem ipsum dolor sit amet, consectetur adipisicing elit.
              Inventore sed consequuntur error repudiandae numquam deserunt
              quisquam repellat libero asperiores earum nam nobis, culpa ratione
              quam perferendis esse, cupiditate neque quas!
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
</style>
