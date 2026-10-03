import http from './http'

export const productosApi = {
  listar: () => http.get('/productos'),
  obtener: (id) => http.get(`/productos/${id}`),
  crear: (producto) => http.post('/productos', producto),
  actualizar: (id, producto) => http.put(`/productos/${id}`, producto),
  eliminar: (id) => http.delete(`/productos/${id}`),
}