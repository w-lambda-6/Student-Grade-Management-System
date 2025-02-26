import { createApp } from 'vue'
import ViewUIPlus from 'view-ui-plus'
import axios from 'axios'
import App from './App.vue'
import 'view-ui-plus/dist/styles/viewuiplus.css'
import * as VueRouter from 'vue-router'
import routes from './router'

const router = VueRouter.createRouter({
  history: VueRouter.createWebHashHistory(),
  routes: routes,
})

//import './assets/main.css'
const app = createApp(App)
app.config.globalProperties.$axios = axios

app.use(ViewUIPlus).use(router).mount('#app')