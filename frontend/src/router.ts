import { createWebHistory, createRouter } from "vue-router";
import HomeView from "./views/HomeView.vue";
import EditView from "./views/EditView.vue";
import MainLayout from "./layouts/MainLayout.vue";
export default createRouter({
  history: createWebHistory("/dash/"),
  routes: [
    {
      path: "/",
      component: MainLayout,
      children: [{ path: '', components: { default: HomeView } }, {path: 'edit', components: {default:EditView}}],
    },
  ],
});
