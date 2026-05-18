<template>
  <div>
    <h3>注册用户</h3>
    <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" style="max-width: 500px; margin-top: 16px">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="form.username" placeholder="用户名" />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="form.password" type="password" placeholder="密码" show-password />
      </el-form-item>
      <el-form-item label="真实姓名">
        <el-input v-model="form.real_name" placeholder="真实姓名" />
      </el-form-item>
      <el-form-item label="年龄">
        <el-input-number v-model="form.age" :min="0" :max="120" style="width: 100%" />
      </el-form-item>
      <el-form-item label="性别" prop="gender">
        <el-radio-group v-model="form.gender">
          <el-radio value="male">男</el-radio>
          <el-radio value="female">女</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleRegister" :loading="loading">注册</el-button>
      </el-form-item>
    </el-form>

    <el-alert type="info" :closable="false" style="margin-top: 16px; max-width: 500px">
      <template #title>说明</template>
      <p>仅超级管理员可注册新管理员账号，注册后默认为普通管理员。</p>
    </el-alert>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { register } from '../../api/users'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const formRef = ref()

const form = reactive({
  username: '',
  password: '',
  real_name: '',
  age: null,
  gender: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }]
}

async function handleRegister() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    await register({ ...form })
    ElMessage.success('注册用户成功')
    Object.assign(form, { username: '', password: '', real_name: '', age: null, gender: '' })
    formRef.value?.resetFields()
  } catch (e) {
    // handled by interceptor
  } finally {
    loading.value = false
  }
}
</script>
