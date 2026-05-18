import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'

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
        path: 'books/list',
        name: 'BookList',
        component: () => import('../views/books/BookList.vue')
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
        path: 'purchases/list',
        name: 'PurchaseList',
        component: () => import('../views/purchases/PurchaseList.vue')
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
        path: 'sales/list',
        name: 'SaleList',
        component: () => import('../views/sales/SaleList.vue')
      },
      {
        path: 'bills/check',
        name: 'BillCheck',
        component: () => import('../views/bills/BillCheck.vue')
      },
      {
        path: 'bills/summary',
        name: 'BillSummary',
        component: () => import('../views/bills/BillSummary.vue'),
        meta: { role: 'super_admin' }
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
  const user = JSON.parse(localStorage.getItem('user') || 'null')

  if (to.meta.requiresAuth !== false && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/dashboard')
  } else if (to.meta.role === 'super_admin' && user?.user_role !== 'super_admin') {
    next('/dashboard')
    ElMessage.warning('仅超级管理员可访问')
  } else {
    next()
  }
})

export default router
