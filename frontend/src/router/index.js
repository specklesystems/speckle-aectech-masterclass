import Vue from "vue"
import VueRouter from "vue-router"
import Home from "../views/Home.vue"
import store from "../store/index.js"
import WelcomeView from "@/views/WelcomeView"
import StreamView from "@/views/StreamView"

Vue.use(VueRouter)

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: {
      requiresAuth: true,
      title: "Speckle AEC Tech Masterclass"
    }
  },
  {
    path: "/login",
    name: "Login",
    component: WelcomeView,
    meta: {
      requiresNoAuth: true,
      title: "Login | Speckle AEC Tech Masterclass"
    }
  },
  {
    path: "/streams/:id",
    name: "Streams",
    component: StreamView,
    meta: {
      requiresAuth: true,
      title: "Stream | Speckle Revit Dashboard"
    }
  }
]

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
})

router.beforeEach(async (to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title
  }

  if (to.query.access_code) {
    // If the route contains an access code, exchange it
    try {
      await store.dispatch("exchangeAccessCode", to.query.access_code)
    } catch (err) {
      console.warn("exchange failed", err)
    }
    // Whatever happens, go home.
    return next("/")
  }
  // Fetch if user is authenticated
  await store.dispatch("getUser")
  var isAuth = store.getters.isAuthenticated
  if (to.meta.requiresAuth && !isAuth) return next({ name: "Login" })
  else if (to.meta.requiresNoAuth && isAuth) return next("/")
  // Any other page
  next()
})

export default router
