import http from './http'

export const pedidosApi = {
  listar: () => http.get('/pedidos'),
  obtener: (id) => http.get(`/pedidos/${id}`),
  crear: (pedido) => http.post('/pedidos', pedido),
  actualizar: (id, pedido) => http.put(`/pedidos/${id}`, pedido),
  eliminar: (id) => http.delete(`/pedidos/${id}`),
}