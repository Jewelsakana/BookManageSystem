<template>
  <div>
    <h3>图书列表</h3>
    <div style="display: flex; align-items: center; gap: 12px; margin-top: 16px">
      <el-button type="primary" @click="loadBooks" :loading="loading">刷新列表</el-button>
      <el-tag v-if="alertCount > 0" type="danger" effect="dark" round>
        库存预警：{{ alertCount }} 本书库存不足（≤ {{ STOCK_ALERT }} 本）
      </el-tag>
    </div>

    <el-table :data="books" border style="width: 100%; margin-top: 12px" v-loading="loading">
      <el-table-column prop="book_id" label="编号" width="70" />
      <el-table-column prop="isbn" label="ISBN" width="150" />
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
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button type="success" size="small" :disabled="!row.stock_quantity || row.stock_quantity <= 0" @click="openBuyDialog(row)">
            购买
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="buyDialogVisible" title="购买图书" width="400px">
      <el-descriptions :column="2" border style="margin-bottom: 16px">
        <el-descriptions-item label="ISBN">{{ buyForm.isbn }}</el-descriptions-item>
        <el-descriptions-item label="书名">{{ buyForm.title }}</el-descriptions-item>
        <el-descriptions-item label="单价">{{ buyForm.price }}</el-descriptions-item>
        <el-descriptions-item label="库存">{{ buyForm.stock }}</el-descriptions-item>
      </el-descriptions>
      <el-form label-width="80px">
        <el-form-item label="购买数量">
          <el-input-number v-model="buyForm.quantity" :min="1" :max="buyForm.stock" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="buyDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleBuy" :loading="buying">确认购买</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { searchAllBooks } from '../../api/books'
import { saleBook } from '../../api/sales'
import { ElMessage } from 'element-plus'

const STOCK_ALERT = 5

const loading = ref(false)
const buying = ref(false)
const books = ref([])
const buyDialogVisible = ref(false)

const alertCount = computed(() => books.value.filter(b => b.stock_quantity <= STOCK_ALERT).length)

const buyForm = reactive({
  isbn: '',
  title: '',
  price: 0,
  stock: 0,
  quantity: 1
})

onMounted(() => {
  loadBooks()
})

async function loadBooks() {
  loading.value = true
  try {
    const res = await searchAllBooks()
    books.value = res.data
    ElMessage.success(`共 ${res.data.length} 本图书`)
  } catch (e) {
    books.value = []
  } finally {
    loading.value = false
  }
}

function openBuyDialog(row) {
  buyForm.isbn = row.isbn
  buyForm.title = row.title
  buyForm.price = row.price
  buyForm.stock = row.stock_quantity
  buyForm.quantity = 1
  buyDialogVisible.value = true
}

async function handleBuy() {
  buying.value = true
  try {
    const res = await saleBook({ isbn: buyForm.isbn, quantity: buyForm.quantity })
    ElMessage.success(`购买成功！金额: ${res.data.amount}`)
    buyDialogVisible.value = false
    loadBooks()
  } catch (e) {
    // handled by interceptor
  } finally {
    buying.value = false
  }
}
</script>
