import { createRouter, createWebHistory } from 'vue-router'
import Header from '@/pages/MainPage/Header.vue'
import Home from '@/pages/MainPage/Index.vue'
import Register from '@/pages/Auth/Register.vue'
import Login from '@/pages/Auth/Login.vue'
import SideBar from '@/components/SideBar.vue'
import Main from '@/pages/Customer/Main.vue'
import Basket from '@/pages/Customer/Basket.vue'
import AddDishes from '@/pages/Admin/AddDishes.vue'
import AdminStats from '@/pages/Admin/AdminStats.vue'
import AdminUsers from '@/pages/Admin/AdminUsers.vue'
import MyOrder from '@/pages/Customer/MyOrder.vue'
import InRestOrder from '@/pages/Customer/InRestOrder.vue'
import { SESSION_MODES, sanitizeAuthStorage, setSessionMode } from '@/utils/roles'
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
    redirect: "/customer/main",
    children: [
      {
        path: "main",
        name: "CliMain",
        component: Main,
      },
      {
        path: "basket",
        name: "Basket",
        component: Basket,
      },
      {
        path: "myorder",
        name: "MyOrder",
        component: MyOrder,
      },
    ],
  },
  {
    path: "/CliMain",
    redirect: "/customer/main",
  },
  {
    path: "/Basket",
    redirect: "/customer/basket",
  },
  {
    path: "/myorder",
    redirect: "/customer/myorder",
  },
  {
    path: "/admin",
    component: SideBar,
    meta: {
      auth: false,
    },
    children: [
      {
        path: "",
        name: "AdminStats",
        component: AdminStats,
      },
      {
        path: "stats",
        name: "AdminStatsPage",
        component: AdminStats,
      },
      {
        path: "users",
        name: "AdminUsers",
        component: AdminUsers,
      },
      {
        path: "adddishes",
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
      path: "order", // в†ђ РЅРµ РѕР±СЏР·Р°С‚РµР»СЊРЅРѕ РїРёСЃР°С‚СЊ /GuestOrder (РёРЅР°С‡Рµ РїРѕР»СѓС‡РёС‚СЃСЏ //guest//GuestOrder)
      name: "GuestOrder",
      component: InRestOrder,

      beforeEnter: (to, from, next) => {
        setSessionMode(SESSION_MODES.GUEST);
        sanitizeAuthStorage();

        if (to.query.table) {
          localStorage.setItem('selectedTable', to.query.table);
        }

        next();
      },
    },
  ],
}

  ],
})

export default router

