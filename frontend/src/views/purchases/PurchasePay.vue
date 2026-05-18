<template>
  <div>
    <h3>进货付款</h3>
    <el-form :model="form" label-width="100px" style="max-width: 400px; margin-top: 16px">
      <el-form-item label="订单号">
        <el-input-number v-model="form.order_id" :min="0" style="width: 100%" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handlePay" :loading="loading">确认付款</el-button>
      </el-form-item>
    </el-form>

    <el-alert type="warning" :closable="false" style="margin-top: 16px; max-width: 400px">
      <template #title>提示</template>
      <p>仅可对状态为"未付款"的订单进行付款，付款后将生成支出账单。</p>
    </el-alert>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { payPurchase } from '../../api/purchases'
import { ElMessage } from 'element-plus'

const loading = ref(false)

const form = reactive({
  order_id: null
})

async function handlePay() {
  if (!form.order_id && form.order_id !== 0) {
    ElMessage.warning('请输入订单号')
    return
  }
  loading.value = true
  try {
    const res = await payPurchase({ order_id: form.order_id })
    ElMessage.success(`付款成功！账单号: ${res.data.bill_id}, 金额: ${res.data.amount}`)
    form.order_id = null
  } catch (e) {
    // handled by interceptor
  } finally {
    loading.value = false
  }
}
</script>
