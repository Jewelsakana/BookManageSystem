<template>
  <div>
    <h3>查看所有用户</h3>
    <el-button type="primary" @click="loadUsers" :loading="loading" style="margin-top: 16px">加载用户列表</el-button>

    <el-table :data="users" border style="width: 100%; margin-top: 16px" v-loading="loading">
      <el-table-column prop="user_id" label="用户ID" width="80" />
      <el-table-column prop="user_name" label="用户名" width="150" />
      <el-table-column prop="user_role" label="角色" width="120">
        <template #default="{ row }">
          <el-tag :type="row.user_role === 'super_admin' ? 'danger' : 'info'">
            {{ row.user_role === 'super_admin' ? '超级管理员' : '普通管理员' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="real_name" label="真实姓名" width="120" />
      <el-table-column prop="age" label="年龄" width="80" />
      <el-table-column prop="gender" label="性别" width="80" />
    </el-table>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { getUserView } from '../../api/users'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const users = ref([])

async function loadUsers() {
  loading.value = true
  try {
    const res = await getUserView({ all_user: true })
    users.value = res.data
    ElMessage.success(`共 ${res.data.length} 名用户`)
  } catch (e) {
    users.value = []
  } finally {
    loading.value = false
  }
}
</script>
