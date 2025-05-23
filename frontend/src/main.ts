import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config';
import { definePreset } from "@primeuix/themes";
import Material from '@primeuix/themes/material';
import 'primeicons/primeicons.css'
import 'vue-advanced-cropper/dist/style.css';
import ToastService from 'primevue/toastservice';
const MyPreset = definePreset(Material, {
  semantic: {
    primary: {
      50: "{indigo.50}",
      100: "{indigo.100}",
      200: "{indigo.200}",
      300: "{indigo.300}",
      400: "{indigo.400}",
      500: "{indigo.500}",
      600: "{indigo.600}",
      700: "{indigo.700}",
      800: "{indigo.800}",
      900: "{indigo.900}",
      950: "{indigo.950}",
    },
  },
});

createApp(App).use(router).use(PrimeVue, {
    ripple: true,
    theme: {
      preset: MyPreset,
      options: { darkModeSelector: ".fake-dark-selector" },
    },
  }).use(ToastService).mount('#app')
