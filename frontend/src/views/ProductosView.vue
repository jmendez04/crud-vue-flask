<template>
  <section>
    <h2>Productos</h2>

    <AlertMessage :message="error" />

    <form class="card form-grid" @submit.prevent="guardar">
      <BaseInput
        v-model="form.nombre"
        label="Nombre"
      />

      <BaseInput
        v-model="form.descripcion"
        label="Descripción"
      />

      <BaseInput
        v-model="form.precio"
        label="Precio"
        type="number"
      />

      <BaseInput
        v-model="form.stock"
        label="Stock"
        type="number"
      />

      <label class="field">
        <span>Activo</span>

        <select v-model="form.activo">
          <option :value="true">Sí</option>
          <option :value="false">No</option>
        </select>
      </label>

      <div class="form-actions">
        <BaseButton
          type="submit"
          :disabled="guardando"
        >
          {{ editando ? 'Actualizar' : 'Crear' }}
        </BaseButton>

        <BaseButton
          v-if="editando"
          variant="secondary"
          @click="cancelar"
        >
          Cancelar
        </BaseButton>
      </div>
    </form>

    <DataTable
      :rows="productos"
      :columns="columns"
    >
      <template #actions="{ row }">
        <BaseButton
          variant="secondary"
          @click="editar(row)"
        >
          Editar
        </BaseButton>

        <BaseButton
          variant="danger"
          @click="eliminar(row)"
        >
          Eliminar
        </BaseButton>
      </template>
    </DataTable>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'

import { productosApi } from '../api/productos'

import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import DataTable from '../components/DataTable.vue'

const productos = ref([])
const error = ref('')
const guardando = ref(false)
const editando = ref(false)
const idEditando = ref(null)

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'precio', label: 'Precio' },
  { key: 'stock', label: 'Stock' },
  { key: 'activo', label: 'Activo' },
]

const form = reactive({
  nombre: '',
  descripcion: '',
  precio: 0,
  stock: 0,
  activo: true,
})

function limpiar() {
  Object.assign(form, {
    nombre: '',
    descripcion: '',
    precio: 0,
    stock: 0,
    activo: true,
  })

  editando.value = false
  idEditando.value = null
}

async function cargar() {
  error.value = ''

  try {
    const response = await productosApi.listar()
    productos.value = response.data
  } catch (err) {
    error.value = err.message
  }
}

async function guardar() {
  error.value = ''
  guardando.value = true

  try {
    const datos = {
      nombre: form.nombre,
      descripcion: form.descripcion,
      precio: Number(form.precio),
      stock: Number(form.stock),
      activo: form.activo,
    }

    if (editando.value) {
      await productosApi.actualizar(
        idEditando.value,
        datos,
      )
    } else {
      await productosApi.crear(datos)
    }

    limpiar()
    await cargar()
  } catch (err) {
    error.value = err.message
  } finally {
    guardando.value = false
  }
}

function editar(producto) {
  Object.assign(form, {
    nombre: producto.nombre,
    descripcion: producto.descripcion,
    precio: producto.precio,
    stock: producto.stock,
    activo: producto.activo,
  })

  editando.value = true
  idEditando.value = producto.id
}

function cancelar() {
  limpiar()
}

async function eliminar(producto) {
  const confirmar = window.confirm(
    `¿Eliminar ${producto.nombre}?`,
  )

  if (!confirmar) {
    return
  }

  try {
    await productosApi.eliminar(producto.id)
    await cargar()
  } catch (err) {
    error.value = err.message
  }
}

onMounted(cargar)
</script>