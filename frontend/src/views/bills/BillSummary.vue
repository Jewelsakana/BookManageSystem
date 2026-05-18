<template>
  <div>
    <h3>收支汇总</h3>

    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :span="8">
        <el-card shadow="hover">
          <div style="text-align: center">
            <div style="font-size: 14px; color: #909399">总收入</div>
            <div style="font-size: 28px; font-weight: bold; color: #67c23a; margin-top: 8px">{{ summary.totalIncome.toFixed(2) }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <div style="text-align: center">
            <div style="font-size: 14px; color: #909399">总支出</div>
            <div style="font-size: 28px; font-weight: bold; color: #f56c6c; margin-top: 8px">{{ summary.totalExpense.toFixed(2) }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <div style="text-align: center">
            <div style="font-size: 14px; color: #909399">净利润</div>
            <div style="font-size: 28px; font-weight: bold; margin-top: 8px" :style="{ color: summary.netProfit >= 0 ? '#409eff' : '#f56c6c' }">{{ summary.netProfit.toFixed(2) }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <div style="display: flex; align-items: center; gap: 12px; margin-top: 20px">
      <el-radio-group v-model="groupBy" @change="doAggregate">
        <el-radio-button value="day">按日</el-radio-button>
        <el-radio-button value="week">按周</el-radio-button>
        <el-radio-button value="month">按月</el-radio-button>
      </el-radio-group>
      <el-button type="primary" @click="loadBills" :loading="loading">刷新数据</el-button>
    </div>

    <el-table :data="grouped" border style="width: 100%; margin-top: 12px" v-loading="loading">
      <el-table-column prop="period" label="时间段" min-width="160" />
      <el-table-column prop="income" label="收入" width="140">
        <template #default="{ row }">
          <span style="color: #67c23a">{{ row.income.toFixed(2) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="expense" label="支出" width="140">
        <template #default="{ row }">
          <span style="color: #f56c6c">{{ row.expense.toFixed(2) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="net" label="净额" width="140">
        <template #default="{ row }">
          <span :style="{ color: row.net >= 0 ? '#409eff' : '#f56c6c' }">{{ row.net.toFixed(2) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="count" label="笔数" width="80" />
    </el-table>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { checkAllBills } from '../../api/bills'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const groupBy = ref('day')
const bills = ref([])

const summary = reactive({ totalIncome: 0, totalExpense: 0, netProfit: 0 })
const grouped = ref([])

onMounted(() => { loadBills() })

async function loadBills() {
  loading.value = true
  try {
    const res = await checkAllBills()
    bills.value = res.data
    doAggregate()
  } catch (e) {
    bills.value = []
  } finally {
    loading.value = false
  }
}

function getPeriodKey(dateStr, mode) {
  const d = new Date(dateStr)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  if (mode === 'day') return `${y}-${m}-${day}`
  if (mode === 'week') {
    const dow = d.getDay()
    const monday = new Date(d)
    monday.setDate(d.getDate() - (dow === 0 ? 6 : dow - 1))
    const sun = new Date(monday)
    sun.setDate(monday.getDate() + 6)
    return `${monday.getFullYear()}-${String(monday.getMonth() + 1).padStart(2, '0')}-${String(monday.getDate()).padStart(2, '0')} ~ ${sun.getFullYear()}-${String(sun.getMonth() + 1).padStart(2, '0')}-${String(sun.getDate()).padStart(2, '0')}`
  }
  if (mode === 'month') return `${y}-${m}`
  return dateStr
}

function doAggregate() {
  const map = new Map()
  let totalIncome = 0
  let totalExpense = 0

  for (const b of bills.value) {
    const amt = Number(b.amount)
    const key = getPeriodKey(b.billed_at, groupBy.value)
    if (!map.has(key)) {
      map.set(key, { income: 0, expense: 0, count: 0 })
    }
    const entry = map.get(key)
    if (b.bill_type === 'income') {
      entry.income += amt
      totalIncome += amt
    } else if (b.bill_type === 'refund') {
      entry.expense += amt
      totalExpense += amt
    } else {
      entry.expense += amt
      totalExpense += amt
    }
    entry.count++
  }

  summary.totalIncome = totalIncome
  summary.totalExpense = totalExpense
  summary.netProfit = totalIncome - totalExpense

  grouped.value = [...map.entries()]
    .map(([period, v]) => ({ period, ...v, net: v.income - v.expense }))
    .sort((a, b) => a.period.localeCompare(b.period))

  ElMessage.success(`共 ${bills.value.length} 条账单，${grouped.value.length} 个时间段`)
}
</script>
