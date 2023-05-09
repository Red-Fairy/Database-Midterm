import { createApp } from 'vue';
import App from './App.vue';
import router from './router/router.js'; // Import the router configuration

const app = createApp(App);

app.use(router); // Use the router configuration when creating the app
app.mount('#app');
