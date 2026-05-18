<template>
  <div>
    <h3>查看账单</h3>
    <el-form inline style="margin-top: 16px">
      <el-form-item label="开始时间">
        <el-date-picker v-model="first_time" type="datetime" placeholder="选择开始时间" format="YYYY-MM-DD HH:mm:ss" value-format="YYYY-MM-DDTHH:mm:ss" />
      </el-form-item>
      <el-form-item label="结束时间">
        <el-date-picker v-model="last_time" type="datetime" placeholder="选择结束时间" format="YYYY-MM-DD HH:mm:ss" value-format="YYYY-MM-DDTHH:mm:ss" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleCheck" :loading="loading">查询</el-button>
        <el-button v-if="userStore.isSuperAdmin" type="warning" @click="handleCheckAll" :loading="loadingAll">查看所有账单</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="bills" border style="width: 100%; margin-top: 16px" v-loading="loading">
      <el-table-column prop="bill_id" label="账单号" width="80" />
      <el-table-column prop="bill_type" label="类型" width="100">
        <template #default="{ row }">
          <el-tag v-if="row.bill_type === 'income'" type="success">收入</el-tag>
          <el-tag v-else-if="row.bill_type === 'refund'" type="warning">退款</el-tag>
          <el-tag v-else type="danger">支出</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="amount" label="金额" width="120" />
      <el-table-column prop="related_id" label="关联订单ID" width="120" />
      <el-table-column prop="billed_at" label="时间" min-width="180" />
    </el-table>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { checkBills, checkAllBills } from '../../api/bills'
import { useUserStore } from '../../stores/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const loading = ref(false)
const loadingAll = ref(false)
const first_time = ref('')
const last_time = ref('')
const bills = ref([])

async function handleCheck() {
  if (!first_time.value || !last_time.value) {
    ElMessage.warning('请选择开始和结束时间')
    return
  }
  loading.value = true
  try {
    const res = await checkBills({ first_time: first_time.value, last_time: last_time.value })
    bills.value = res.data
    if (res.data.length === 0) {
      ElMessage.info('该时间段内无账单记录')
    } else {
      ElMessage.success(`查询到 ${res.data.length} 条账单`)
    }
  } catch (e) {
    bills.value = []
  } finally {
    loading.value = false
  }
}

async function handleCheckAll() {
  loadingAll.value = true
  try {
    const res = await checkAllBills()
    bills.value = res.data
    if (res.data.length === 0) {
      ElMessage.info('无账单记录')
    } else {
      ElMessage.success(`共 ${res.data.length} 条账单`)
    }
  } catch (e) {
    bills.value = []
  } finally {
    loadingAll.value = false
  }
}
</script>
