<template>
  <div>
    <h3>创建进货单</h3>
    <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" style="max-width: 500px; margin-top: 16px">
      <el-form-item label="ISBN" prop="isbn">
        <el-input v-model="form.isbn" placeholder="书籍ISBN号" />
      </el-form-item>
      <el-form-item label="进货价格" prop="buy_price">
        <el-input-number v-model="form.buy_price" :min="0" :precision="2" style="width: 100%" />
      </el-form-item>
      <el-form-item label="进货数量" prop="purchase_quantity">
        <el-input-number v-model="form.purchase_quantity" :min="1" style="width: 100%" />
      </el-form-item>
      <el-divider content-position="left">新书信息（已有ISBN则无需填写）</el-divider>
      <el-form-item label="书名">
        <el-input v-model="form.title" placeholder="书名" />
      </el-form-item>
      <el-form-item label="出版社">
        <el-input v-model="form.publisher" placeholder="出版社" />
      </el-form-item>
      <el-form-item label="作者">
        <el-input v-model="form.author" placeholder="作者" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleAdd" :loading="loading">创建进货单</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { addPurchase } from '../../api/purchases'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const formRef = ref()

const form = reactive({
  isbn: '',
  buy_price: null,
  purchase_quantity: null,
  title: '',
  publisher: '',
  author: ''
})

const rules = {
  isbn: [{ required: true, message: '请输入ISBN', trigger: 'blur' }],
  buy_price: [{ required: true, message: '请输入进货价格', trigger: 'blur' }],
  purchase_quantity: [{ required: true, message: '请输入进货数量', trigger: 'blur' }]
}

async function handleAdd() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    const data = {
      isbn: form.isbn,
      buy_price: form.buy_price,
      purchase_quantity: form.purchase_quantity
    }
    if (form.title) data.title = form.title
    if (form.publisher) data.publisher = form.publisher
    if (form.author) data.author = form.author
    const res = await addPurchase(data)
    ElMessage.success(`进货单创建成功！订单号: ${res.data.order_id}`)
    Object.assign(form, { isbn: '', buy_price: null, purchase_quantity: null, title: '', publisher: '', author: '' })
    formRef.value?.resetFields()
  } catch (e) {
    // handled by interceptor
  } finally {
    loading.value = false
  }
}
</script>
