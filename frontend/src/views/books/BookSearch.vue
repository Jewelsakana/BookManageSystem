<template>
  <div>
    <h3>图书查询</h3>
    <el-form :model="form" inline style="margin-top: 16px">
      <el-form-item label="书籍编号">
        <el-input v-model="form.book_id" placeholder="书籍编号" clearable />
      </el-form-item>
      <el-form-item label="ISBN">
        <el-input v-model="form.isbn" placeholder="ISBN号" clearable />
      </el-form-item>
      <el-form-item label="书名">
        <el-input v-model="form.title" placeholder="书名" clearable />
      </el-form-item>
      <el-form-item label="作者">
        <el-input v-model="form.author" placeholder="作者" clearable />
      </el-form-item>
      <el-form-item label="出版社">
        <el-input v-model="form.publisher" placeholder="出版社" clearable />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSearch" :loading="loading">查询</el-button>
        <el-button @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="books" border style="width: 100%; margin-top: 16px" v-loading="loading">
      <el-table-column prop="book_id" label="编号" width="80" />
      <el-table-column prop="isbn" label="ISBN" width="160" />
      <el-table-column prop="title" label="书名" min-width="200" />
      <el-table-column prop="author" label="作者" width="120" />
      <el-table-column prop="publisher" label="出版社" width="150" />
      <el-table-column prop="price" label="零售价" width="100" />
      <el-table-column label="库存" width="90">
        <template #default="{ row }">
          <el-tag v-if="row.stock_quantity === 0" type="info">已售罄</el-tag>
          <el-tag v-else-if="row.stock_quantity <= STOCK_ALERT" type="danger">{{ row.stock_quantity }} 本</el-tag>
          <span v-else style="color: #67c23a">{{ row.stock_quantity }} 本</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { searchBooks } from '../../api/books'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const books = ref([])

const STOCK_ALERT = 5

const form = reactive({
  book_id: '',
  isbn: '',
  title: '',
  author: '',
  publisher: ''
})

async function handleSearch() {
  const params = {}
  for (const [k, v] of Object.entries(form)) {
    if (v !== '' && v !== null && v !== undefined) params[k] = v
  }
  if (Object.keys(params).length === 0) {
    ElMessage.warning('至少输入一种查询条件')
    return
  }

  loading.value = true
  try {
    const res = await searchBooks(params)
    books.value = res.data
    if (res.data.length === 0) {
      ElMessage.info('没有找到书籍')
    } else {
      ElMessage.success(`找到 ${res.data.length} 本书籍`)
    }
  } catch (e) {
    books.value = []
  } finally {
    loading.value = false
  }
}

function handleReset() {
  Object.keys(form).forEach(k => form[k] = '')
  books.value = []
}
</script>
