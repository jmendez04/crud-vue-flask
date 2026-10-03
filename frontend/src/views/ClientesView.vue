<template>
  <section>
    <h2>Clientes</h2>

    <AlertMessage :message="error" />

    <form class="card form-grid" @submit.prevent="guardar">
      <BaseInput
        v-model="form.nombre"
        label="Nombre"
      />

      <BaseInput
        v-model="form.correo"
        label="Correo"
        type="email"
      />

      <BaseInput
        v-model="form.telefono"
        label="Teléfono"
      />

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
      :rows="clientes"
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

import { clientesApi } from '../api/clientes'

import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import DataTable from '../components/DataTable.vue'

const clientes = ref([])
const error = ref('')
const guardando = ref(false)
const editando = ref(false)
const idEditando = ref(null)

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'correo', label: 'Correo' },
  { key: 'telefono', label: 'Teléfono' },
]

const form = reactive({
  nombre: '',
  correo: '',
  telefono: '',
})

function limpiar() {
  Object.assign(form, {
    nombre: '',
    correo: '',
    telefono: '',
  })

  editando.value = false
  idEditando.value = null
}

async function cargar() {
  error.value = ''

  try {
    console.log(
      'API URL:',
      import.meta.env.VITE_API_URL,
    )

    const response = await clientesApi.listar()

    console.log(
      'Respuesta clientes:',
      response,
    )

    clientes.value = response.data
  } catch (err) {
    console.error(
      'Error Axios:',
      err,
    )

    error.value = err.message
  }
}

async function guardar() {
  error.value = ''
  guardando.value = true

  try {
    if (editando.value) {
      await clientesApi.actualizar(
        idEditando.value,
        form,
      )
    } else {
      await clientesApi.crear(form)
    }

    limpiar()
    await cargar()
  } catch (err) {
    console.error(
      'Error al guardar:',
      err,
    )

    error.value = err.message
  } finally {
    guardando.value = false
  }
}

function editar(cliente) {
  Object.assign(form, {
    nombre: cliente.nombre,
    correo: cliente.correo,
    telefono: cliente.telefono,
  })

  editando.value = true
  idEditando.value = cliente.id
}

function cancelar() {
  limpiar()
}

async function eliminar(cliente) {
  const confirmar = window.confirm(
    `¿Eliminar a ${cliente.nombre}?`,
  )

  if (!confirmar) {
    return
  }

  try {
    await clientesApi.eliminar(
      cliente.id,
    )

    await cargar()
  } catch (err) {
    console.error(
      'Error al eliminar:',
      err,
    )

    error.value = err.message
  }
}

onMounted(cargar)
</script>