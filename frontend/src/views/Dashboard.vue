<template>
  <div>
    <h2>欢迎使用图书销售管理系统</h2>
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>图书管理</template>
          <p>查询、修改图书信息，添加新书入库</p>
          <el-button type="primary" @click="$router.push('/books/search')">进入</el-button>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>进货管理</template>
          <p>创建进货单、付款、退货处理</p>
          <el-button type="primary" @click="$router.push('/purchases/add')">进入</el-button>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>销售管理</template>
          <p>图书销售出库，自动生成账单</p>
          <el-button type="primary" @click="$router.push('/sales/book')">进入</el-button>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>财务管理</template>
          <p>按时间范围查询收支账单</p>
          <el-button type="primary" @click="$router.push('/bills/check')">进入</el-button>
        </el-card>
      </el-col>
      <el-col :span="8" v-if="userStore.isSuperAdmin">
        <el-card shadow="hover">
          <template #header>用户管理</template>
          <p>查看、注册管理员用户</p>
          <el-button type="primary" @click="$router.push('/users/list')">进入</el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { useUserStore } from '../stores/user'
const userStore = useUserStore()
</script>
