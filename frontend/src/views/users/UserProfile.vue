<template>
  <div>
    <h3>个人信息修改</h3>

    <el-form v-if="userStore.isSuperAdmin" :inline="true" style="margin-top: 16px">
      <el-form-item label="目标用户ID">
        <el-input-number v-model="targetUserId" :min="1" style="width: 200px" placeholder="留空为修改自己" />
      </el-form-item>
      <el-form-item>
        <el-button @click="loadUser" :loading="loadingUser">加载用户信息</el-button>
      </el-form-item>
    </el-form>

    <el-divider />

    <el-form :model="form" label-width="100px" style="max-width: 500px">
      <el-form-item label="用户名">
        <el-input v-model="form.username" placeholder="用户名" clearable />
      </el-form-item>
      <el-form-item label="新密码">
        <el-input v-model="form.password" type="password" placeholder="留空则不修改" show-password />
      </el-form-item>
      <el-form-item v-if="form.password" label="旧密码">
        <el-input v-model="form.oldPassword" type="password" placeholder="修改密码需验证旧密码" show-password />
      </el-form-item>
      <el-form-item label="真实姓名">
        <el-input v-model="form.real_name" placeholder="真实姓名" clearable />
      </el-form-item>
      <el-form-item label="年龄">
        <el-input-number v-model="form.age" :min="0" :max="120" style="width: 100%" />
      </el-form-item>
      <el-form-item label="性别">
        <el-radio-group v-model="form.gender">
          <el-radio value="male">男</el-radio>
          <el-radio value="female">女</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleUpdate" :loading="loading">提交修改</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useUserStore } from '../../stores/user'
import { updateUser, getUserView } from '../../api/users'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const loading = ref(false)
const loadingUser = ref(false)
const targetUserId = ref(null)

const form = reactive({
  username: '',
  password: '',
  oldPassword: '',
  real_name: '',
  age: null,
  gender: ''
})

onMounted(() => {
  loadSelf()
})

function loadSelf() {
  form.username = userStore.user?.username || ''
  form.real_name = userStore.user?.real_name || ''
  form.age = userStore.user?.age || null
  form.gender = userStore.user?.gender || ''
  form.password = ''
  form.oldPassword = ''
}

async function loadUser() {
  if (!targetUserId.value) {
    loadSelf()
    ElMessage.info('已加载自己的信息')
    return
  }
  loadingUser.value = true
  try {
    const res = await getUserView({ target_user_id: targetUserId.value })
    const u = res.data
    form.username = u.user_name || ''
    form.real_name = u.real_name || ''
    form.age = u.age || null
    form.gender = u.gender || ''
    form.password = ''
    form.oldPassword = ''
    ElMessage.success('用户信息加载成功')
  } catch (e) {
    // handled by interceptor
  } finally {
    loadingUser.value = false
  }
}

async function handleUpdate() {
  const data = {
    target_user_id: userStore.isSuperAdmin && targetUserId.value ? targetUserId.value : userStore.user?.user_id
  }
  if (form.username) data.username = form.username
  if (form.password) {
    data.password = form.password
    if (form.oldPassword) data.old_password = form.oldPassword
  }
  if (form.real_name) data.real_name = form.real_name
  if (form.age !== null && form.age !== undefined) data.age = form.age
  if (form.gender) data.gender = form.gender

  loading.value = true
  try {
    await updateUser(data)
    ElMessage.success('用户信息修改成功')
    if (!userStore.isSuperAdmin || !targetUserId.value) {
      userStore.user.username = form.username
      userStore.user.real_name = form.real_name
      userStore.user.age = form.age
      userStore.user.gender = form.gender
      localStorage.setItem('user', JSON.stringify(userStore.user))
    }
    form.password = ''
    form.oldPassword = ''
  } catch (e) {
    // handled by interceptor
  } finally {
    loading.value = false
  }
}
</script>
