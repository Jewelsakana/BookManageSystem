<template>
  <el-container style="height: 100vh">
    <el-aside width="220px" style="background-color: #304156">
      <div style="height: 60px; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 18px; font-weight: bold; border-bottom: 1px solid #4a5568">
        图书销售管理系统
      </div>
      <el-menu
        :default-active="route.path"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409eff"
        router
        style="border-right: none"
      >
        <el-menu-item index="/dashboard">
          <el-icon><HomeFilled /></el-icon>
          <span>主控台</span>
        </el-menu-item>

        <el-sub-menu index="books">
          <template #title>
            <el-icon><Reading /></el-icon>
            <span>图书管理</span>
          </template>
          <el-menu-item index="/books/search">图书查询</el-menu-item>
          <el-menu-item index="/books/update">图书修改</el-menu-item>
          <el-menu-item index="/books/add">添加新书</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="purchases">
          <template #title>
            <el-icon><Goods /></el-icon>
            <span>进货管理</span>
          </template>
          <el-menu-item index="/purchases/add">创建进货单</el-menu-item>
          <el-menu-item index="/purchases/pay">进货付款</el-menu-item>
          <el-menu-item index="/purchases/return">进货退货</el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/sales/book">
          <el-icon><Sell /></el-icon>
          <span>销售管理</span>
        </el-menu-item>

        <el-menu-item index="/bills/check">
          <el-icon><Money /></el-icon>
          <span>财务管理</span>
        </el-menu-item>

        <el-sub-menu index="users" v-if="userStore.isSuperAdmin">
          <template #title>
            <el-icon><UserFilled /></el-icon>
            <span>用户管理</span>
          </template>
          <el-menu-item index="/users/list">查看用户</el-menu-item>
          <el-menu-item index="/users/register">注册用户</el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/users/profile">
          <el-icon><Edit /></el-icon>
          <span>个人信息</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header style="display: flex; align-items: center; justify-content: flex-end; border-bottom: 1px solid #e4e7ed; background: #fff">
        <span style="margin-right: 16px">
          {{ userStore.user?.real_name || userStore.user?.username }}
          <el-tag size="small" :type="userStore.isSuperAdmin ? 'danger' : 'info'" style="margin-left: 8px">
            {{ userStore.isSuperAdmin ? '超级管理员' : '普通管理员' }}
          </el-tag>
        </span>
        <el-button type="danger" text @click="handleLogout">退出登录</el-button>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'
import { logout } from '../api/users'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

async function handleLogout() {
  try {
    await logout()
  } catch (e) {
    // ignore
  }
  userStore.clearAuth()
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>
