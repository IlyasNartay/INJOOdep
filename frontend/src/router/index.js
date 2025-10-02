import { createRouter, createWebHistory } from 'vue-router'
import Header from '@/pages/MainPage/Header.vue'
import Home from '@/pages/MainPage/Index.vue'
import Register from '@/pages/Auth/Register.vue'
import Login from '@/pages/Auth/Login.vue'
import SideBar from '@/components/SideBar.vue'
import Main from '@/pages/Customer/Main.vue'
import Basket from '@/pages/Customer/Basket.vue'
import AddDishes from '@/pages/Admin/AddDishes.vue'
import MyOrder from '@/pages/Customer/MyOrder.vue'
import InRestOrder from '@/pages/Customer/InRestOrder.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
    path: "/",
    component: Header,
    meta: {
      auth: false,
    },
    children: [
      {
        path: "",
        name: "Home",
        component: Home,
      },
    ],
  },
{
    path: "/auth",
    component: Register,
    meta: {
      auth: false,
    },
  },
  {
    path: "/login",
    component: Login,
    meta: {
      auth: false,
    },
  },
  {
    path: "/customer",
    component: SideBar,
    meta: {
      auth: false,
    },
    children: [
      {
        path: "/CliMain",
        name: "CliMain",
        component: Main,
      },
      {
        path: "/Basket",
        name: "Basket",
        component: Basket,
      },
      {
        path: "/myorder",
        name: "MyOrder",
        component: MyOrder,
      },
    ],
  },
  {
    path: "/admin",
    component: SideBar,
    meta: {
      auth: false,
    },
    children: [
      {
        path: "/CliMain",
        name: "CliMain",
        component: Main,
      },
      {
        path: "/adddishes",
        name: "AddDishes",
        component: AddDishes,
      },
    ],
  },
  {
    path: "/guest",
    component: SideBar,
    meta: {
      auth: false,
    },
    children: [
      {
        path: "/GuestOrder",
        name: "GuestOrder",
        component: InRestOrder,
      },
    ],
  },
  ],
})

export default router
