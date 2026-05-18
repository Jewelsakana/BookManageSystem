import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('../layout/MainLayout.vue'),
    meta: { requiresAuth: true },
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue')
      },
      {
        path: 'books/search',
        name: 'BookSearch',
        component: () => import('../views/books/BookSearch.vue')
      },
      {
        path: 'books/update',
        name: 'BookUpdate',
        component: () => import('../views/books/BookUpdate.vue')
      },
      {
        path: 'books/add',
        name: 'BookAdd',
        component: () => import('../views/books/BookAdd.vue')
      },
      {
        path: 'purchases/add',
        name: 'PurchaseAdd',
        component: () => import('../views/purchases/PurchaseAdd.vue')
      },
      {
        path: 'purchases/pay',
        name: 'PurchasePay',
        component: () => import('../views/purchases/PurchasePay.vue')
      },
      {
        path: 'purchases/return',
        name: 'PurchaseReturn',
        component: () => import('../views/purchases/PurchaseReturn.vue')
      },
      {
        path: 'sales/book',
        name: 'SaleBook',
        component: () => import('../views/sales/SaleBook.vue')
      },
      {
        path: 'bills/check',
        name: 'BillCheck',
        component: () => import('../views/bills/BillCheck.vue')
      },
      {
        path: 'users/list',
        name: 'UserList',
        component: () => import('../views/users/UserList.vue'),
        meta: { role: 'super_admin' }
      },
      {
        path: 'users/register',
        name: 'UserRegister',
        component: () => import('../views/users/UserRegister.vue'),
        meta: { role: 'super_admin' }
      },
      {
        path: 'users/profile',
        name: 'UserProfile',
        component: () => import('../views/users/UserProfile.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth !== false && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
