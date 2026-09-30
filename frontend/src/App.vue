<script setup>
import { ref, onMounted } from 'vue'

const API_URL = 'http://localhost:8000/sessions'

// State management
const sessions = ref([])
const loading = ref(false)
const error = ref(null)
const page = ref(1)
const totalPages = ref(1)
const searchQuery = ref('')

// Form state
const form = ref({
  passenger_name: '',
  route: '',
  date: '',
  time: ''
})
const formError = ref('')
const formLoading = ref(false)

// Fetch data
const fetchSessions = async () => {
  loading.value = true
  error.value = null
  try {
    let url = `${API_URL}?page=${page.value}&limit=5`
    if (searchQuery.value) {
      url += `&q=${encodeURIComponent(searchQuery.value)}`
    }
    const response = await fetch(url)
    if (!response.ok) throw new Error('Gagal mengambil data dari server')
    const data = await response.json()
    sessions.value = data.data
    totalPages.value = Math.ceil(data.total / data.limit)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  page.value = 1
  fetchSessions()
}

const changePage = (newPage) => {
  if (newPage >= 1 && newPage <= totalPages.value) {
    page.value = newPage
    fetchSessions()
  }
}

// Create new session
const submitForm = async () => {
  formError.value = ''
  if (!form.value.passenger_name || !form.value.route || !form.value.date || !form.value.time) {
    formError.value = 'Semua field harus diisi!'
    return
  }

  formLoading.value = true
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(form.value)
    })

    if (!response.ok) throw new Error('Gagal menyimpan data')
    
    // Reset form and refresh data
    form.value = { passenger_name: '', route: '', date: '', time: '' }
    fetchSessions()
  } catch (err) {
    formError.value = err.message
  } finally {
    formLoading.value = false
  }
}

// Delete session
const deleteSession = async (id) => {
  if (!confirm('Apakah Anda yakin ingin menghapus pesanan ini?')) return

  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: 'DELETE'
    })
    if (!response.ok) throw new Error('Gagal menghapus data')
    fetchSessions()
  } catch (err) {
    alert(err.message)
  }
}

onMounted(() => {
  fetchSessions()
})
</script>

<template>
  <div class="container">
    <h1>Pemesanan Shuttle Kampus</h1>

    <div class="main-content">
      <!-- Left Column: Form -->
      <div class="form-section">
        <h2>Buat Pesanan Baru</h2>
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label>Nama Penumpang</label>
            <input type="text" v-model="form.passenger_name" placeholder="Masukkan nama..." />
          </div>
          <div class="form-group">
            <label>Rute</label>
            <select v-model="form.route">
              <option value="">-- Pilih Rute --</option>
              <option value="Asrama -> Kampus Utama">Asrama -> Kampus Utama</option>
              <option value="Kampus Utama -> Asrama">Kampus Utama -> Asrama</option>
              <option value="Kampus Utama -> Stasiun">Kampus Utama -> Stasiun</option>
              <option value="Stasiun -> Kampus Utama">Stasiun -> Kampus Utama</option>
              <option value="Asrama -> Stasiun">Asrama -> Stasiun</option>
              <option value="Stasiun -> Asrama">Stasiun -> Asrama</option>
            </select>
          </div>
          <div class="form-group">
            <label>Tanggal</label>
            <input type="date" v-model="form.date" />
          </div>
          <div class="form-group">
            <label>Waktu</label>
            <input type="time" v-model="form.time" />
          </div>
          
          <div v-if="formError" class="error-msg">{{ formError }}</div>
          
          <button type="submit" :disabled="formLoading" class="btn-primary">
            {{ formLoading ? 'Menyimpan...' : 'Pesan Shuttle' }}
          </button>
        </form>
      </div>

      <!-- Right Column: List -->
      <div class="list-section">
        <h2>Daftar Pesanan</h2>
        
        <div class="search-box">
          <input 
            type="text" 
            v-model="searchQuery" 
            @keyup.enter="handleSearch"
            placeholder="Cari nama atau rute..." 
          />
          <button @click="handleSearch" class="btn-secondary">Cari</button>
        </div>

        <!-- State 1: Loading -->
        <div v-if="loading" class="state-box loading">
          Memuat data...
        </div>

        <!-- State 2: Error -->
        <div v-else-if="error" class="state-box error">
          <p>{{ error }}</p>
          <button @click="fetchSessions" class="btn-retry">Coba Lagi</button>
        </div>

        <!-- State 3: Empty -->
        <div v-else-if="sessions.length === 0" class="state-box empty">
          Belum ada data pesanan.
        </div>

        <!-- State 4: Data -->
        <div v-else class="data-box">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Penumpang</th>
                <th>Rute</th>
                <th>Tanggal/Waktu</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="session in sessions" :key="session.id">
                <td>{{ session.id }}</td>
                <td>{{ session.passenger_name }}</td>
                <td>{{ session.route }}</td>
                <td>{{ session.date }} {{ session.time }}</td>
                <td>
                  <button @click="deleteSession(session.id)" class="btn-danger">Hapus</button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination -->
          <div class="pagination">
            <button 
              @click="changePage(page - 1)" 
              :disabled="page === 1"
              class="btn-page"
            >
              Sebelumnya
            </button>
            <span>Halaman {{ page }} dari {{ totalPages || 1 }}</span>
            <button 
              @click="changePage(page + 1)" 
              :disabled="page >= totalPages"
              class="btn-page"
            >
              Selanjutnya
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  color: #333;
}
h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
}
.main-content {
  display: flex;
  gap: 30px;
  flex-wrap: wrap;
}
.form-section {
  flex: 1;
  min-width: 300px;
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  height: fit-content;
}
.list-section {
  flex: 2;
  min-width: 400px;
}
.form-group {
  margin-bottom: 15px;
}
.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}
.form-group input, .form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
button {
  cursor: pointer;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-weight: bold;
}
.btn-primary {
  background: #42b983;
  color: white;
  width: 100%;
  padding: 10px;
  font-size: 16px;
}
.btn-primary:disabled {
  background: #a8d5c2;
  cursor: not-allowed;
}
.btn-secondary {
  background: #2c3e50;
  color: white;
}
.btn-danger {
  background: #e74c3c;
  color: white;
  padding: 5px 10px;
}
.btn-retry {
  background: #f39c12;
  color: white;
  margin-top: 10px;
}
.btn-page {
  background: #ecf0f1;
  color: #333;
  border: 1px solid #ccc;
}
.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.error-msg {
  color: #e74c3c;
  margin-bottom: 10px;
  font-size: 14px;
}
.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
.search-box input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.state-box {
  padding: 40px;
  text-align: center;
  border-radius: 8px;
  background: #f9f9f9;
  border: 1px dashed #ccc;
}
.state-box.error {
  color: #e74c3c;
  border-color: #e74c3c;
  background: #fdf2f1;
}
.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}
.data-table th, .data-table td {
  padding: 12px;
  border-bottom: 1px solid #eee;
  text-align: left;
}
.data-table th {
  background-color: #f8f9fa;
  font-weight: bold;
}
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
}
</style>
