<template>
  <div>
    <h3>进货退货</h3>
    <el-form :model="form" label-width="100px" style="max-width: 400px; margin-top: 16px">
      <el-form-item label="订单号">
        <el-input-number v-model="form.order_id" :min="0" style="width: 100%" />
      </el-form-item>
      <el-form-item>
        <el-button type="danger" @click="handleReturn" :loading="loading">确认退货</el-button>
      </el-form-item>
    </el-form>

    <el-alert type="warning" :closable="false" style="margin-top: 16px; max-width: 400px">
      <template #title>提示</template>
      <p>仅可对状态为"未付款"的订单进行退货，退货后状态将变为"已退货"。</p>
    </el-alert>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { returnPurchase } from '../../api/purchases'
import { ElMessage } from 'element-plus'

const loading = ref(false)

const form = reactive({
  order_id: null
})

async function handleReturn() {
  if (!form.order_id && form.order_id !== 0) {
    ElMessage.warning('请输入订单号')
    return
  }
  loading.value = true
  try {
    await returnPurchase({ order_id: form.order_id })
    ElMessage.success('退货成功')
    form.order_id = null
  } catch (e) {
    // handled by interceptor
  } finally {
    loading.value = false
  }
}
</script>
