<template>
  <div>
    <h3>添加新书（到货入库）</h3>
    <el-form :model="form" label-width="120px" style="max-width: 500px; margin-top: 16px">
      <el-form-item label="订单号">
        <el-input-number v-model="form.order_id" :min="0" style="width: 100%" />
      </el-form-item>
      <el-form-item label="零售价">
        <el-input-number v-model="form.price" :min="0" :precision="2" style="width: 100%" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleAdd" :loading="loading">确认入库</el-button>
      </el-form-item>
    </el-form>

    <el-alert type="info" :closable="false" style="margin-top: 16px; max-width: 500px">
      <template #title>说明</template>
      <p>仅可对已付款的进货订单进行入库操作，入库后库存会自动增加，零售价必须大于进货价。</p>
    </el-alert>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { addBook } from '../../api/books'
import { ElMessage } from 'element-plus'

const loading = ref(false)

const form = reactive({
  order_id: null,
  price: null
})

async function handleAdd() {
  if (!form.order_id && form.order_id !== 0) {
    ElMessage.warning('请输入订单号')
    return
  }
  if (form.price === null || form.price === undefined) {
    ElMessage.warning('请输入零售价')
    return
  }
  loading.value = true
  try {
    const res = await addBook({ order_id: form.order_id, price: form.price })
    ElMessage.success(`入库成功！ISBN: ${res.data.isbn}, 书名: ${res.data.title}, 当前库存: ${res.data.stock_quantity}`)
    form.order_id = null
    form.price = null
  } catch (e) {
    // handled by interceptor
  } finally {
    loading.value = false
  }
}
</script>
