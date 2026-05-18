<template>
  <div>
    <h3>书籍购买</h3>
    <el-form :model="form" label-width="100px" style="max-width: 400px; margin-top: 16px">
      <el-form-item label="ISBN">
        <el-input v-model="form.isbn" placeholder="书籍ISBN号" />
      </el-form-item>
      <el-form-item label="购买数量">
        <el-input-number v-model="form.quantity" :min="1" style="width: 100%" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSale" :loading="loading">确认购买</el-button>
      </el-form-item>
    </el-form>

    <el-alert type="info" :closable="false" style="margin-top: 16px; max-width: 400px">
      <template #title>说明</template>
      <p>购买后将自动从库存中扣减，并生成销售记录和收入账单。</p>
    </el-alert>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { saleBook } from '../../api/sales'
import { ElMessage } from 'element-plus'

const loading = ref(false)

const form = reactive({
  isbn: '',
  quantity: null
})

async function handleSale() {
  if (!form.isbn) {
    ElMessage.warning('请输入ISBN')
    return
  }
  if (!form.quantity) {
    ElMessage.warning('请输入购买数量')
    return
  }
  loading.value = true
  try {
    const res = await saleBook({ isbn: form.isbn, quantity: form.quantity })
    ElMessage.success(`购买成功！书名: ${res.data.title}, 数量: ${res.data.quantity}, 金额: ${res.data.amount}`)
    form.isbn = ''
    form.quantity = null
  } catch (e) {
    // handled by interceptor
  } finally {
    loading.value = false
  }
}
</script>
