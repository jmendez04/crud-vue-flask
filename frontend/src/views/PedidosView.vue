<template>
  <section>
    <h2>Pedidos</h2>

    <AlertMessage :message="error" />
    <p v-if="cargando">
      Cargando...
    </p>"

    <form class="card form-grid" @submit.prevent="crearPedido">
      <label class="field">
        <span>Cliente</span>

        <select v-model.number="form.cliente_id" required>
          <option disabled value="">
            Seleccione un cliente
          </option>

          <option
            v-for="cliente in clientes"
            :key="cliente.id"
            :value="cliente.id"
          >
            {{ cliente.nombre }}
          </option>
        </select>
      </label>

      <label class="field">
        <span>Producto</span>

        <select v-model.number="form.producto_id" required>
          <option disabled value="">
            Seleccione un producto
          </option>

          <option
            v-for="producto in productos"
            :key="producto.id"
            :value="producto.id"
          >
            {{ producto.nombre }} — Q{{ producto.precio }}
          </option>
        </select>
      </label>

      <BaseInput
        v-model="form.cantidad"
        label="Cantidad"
        type="number"
      />

      <div class="form-actions">
        <BaseButton
          type="submit"
          :disabled="guardando"
        >
          Crear pedido
        </BaseButton>
      </div>
    </form>

    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Cliente</th>
            <th>Producto</th>
            <th>Cantidad</th>
            <th>Total</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>

        <tbody>
          <tr v-if="!pedidos.length">
            <td colspan="7">
              No hay registros.
            </td>
          </tr>

          <tr
            v-for="pedido in pedidos"
            :key="pedido.id"
          >
            <td>{{ pedido.id }}</td>
            <td>{{ pedido.cliente }}</td>
            <td>{{ pedido.producto }}</td>
            <td>{{ pedido.cantidad }}</td>
            <td>Q{{ pedido.total }}</td>

            <td>
              <select
                :value="pedido.estado"
                @change="cambiarEstado(
                  pedido,
                  $event.target.value
                )"
              >
                <option value="pendiente">
                  Pendiente
                </option>

                <option value="pagado">
                  Pagado
                </option>

                <option value="enviado">
                  Enviado
                </option>

                <option value="cancelado">
                  Cancelado
                </option>
              </select>
            </td>

            <td>
              <BaseButton
                variant="danger"
                @click="eliminar(pedido)"
              >
                Eliminar
              </BaseButton>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'

import { clientesApi } from '../api/clientes'
import { pedidosApi } from '../api/pedidos'
import { productosApi } from '../api/productos'

import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'

const pedidos = ref([])
const clientes = ref([])
const productos = ref([])
const error = ref('')
const guardando = ref(false)
const cargando = ref(false)

const form = reactive({
  cliente_id: '',
  producto_id: '',
  cantidad: 1,
})

async function cargarDatos() {
  error.value = ''
  cargando.value = true

  try {
    const [
      respuestaPedidos,
      respuestaClientes,
      respuestaProductos,
    ] = await Promise.all([
      pedidosApi.listar(),
      clientesApi.listar(),
      productosApi.listar(),
    ])

    pedidos.value = respuestaPedidos.data
    clientes.value = respuestaClientes.data
    productos.value = respuestaProductos.data
  } catch (err) {
    error.value = err.message
  } finally {
    cargando.value = false
  }
}

async function crearPedido() {
  error.value = ''
  guardando.value = true

  try {
    const datos = {
      cliente_id: Number(form.cliente_id),
      producto_id: Number(form.producto_id),
      cantidad: Number(form.cantidad),
    }

    await pedidosApi.crear(datos)

    form.cliente_id = ''
    form.producto_id = ''
    form.cantidad = 1

    await cargarDatos()
  } catch (err) {
    error.value = err.message
  } finally {
    guardando.value = false
  }
}

async function cambiarEstado(pedido, estado) {
  error.value = ''

  try {
    await pedidosApi.actualizar(
      pedido.id,
      { estado },
    )

    await cargarDatos()
  } catch (err) {
    error.value = err.message
  }
}

async function eliminar(pedido) {
  const confirmar = window.confirm(
    `¿Eliminar el pedido #${pedido.id}?`,
  )

  if (!confirmar) {
    return
  }

  try {
    await pedidosApi.eliminar(pedido.id)
    await cargarDatos()
  } catch (err) {
    error.value = err.message
  }
}

onMounted(cargarDatos)
</script>