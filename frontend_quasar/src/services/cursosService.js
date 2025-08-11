import { api } from 'boot/axios'

export const cursosService = {
  // Obtener todos los cursos
  async getCursos() {
    try {
      const response = await api.get('cursos/')
      return response.data
    } catch (error) {
      console.error('Error al obtener cursos:', error)
      throw error
    }
  },

  // Obtener un curso por ID
  async getCurso(id) {
    try {
      const response = await api.get(`cursos/${id}/`)
      return response.data
    } catch (error) {
      console.error('Error al obtener curso:', error)
      throw error
    }
  },

  // Crear un nuevo curso
  async createCurso(cursoData) {
    try {
      const response = await api.post('cursos/', cursoData)
      return response.data
    } catch (error) {
      console.error('Error al crear curso:', error)
      throw error
    }
  },

  // Actualizar un curso
  async updateCurso(id, cursoData) {
    try {
      const response = await api.put(`cursos/${id}/`, cursoData)
      return response.data
    } catch (error) {
      console.error('Error al actualizar curso:', error)
      throw error
    }
  },

  // Eliminar un curso
  async deleteCurso(id) {
    try {
      await api.delete(`cursos/${id}/`)
      return true
    } catch (error) {
      console.error('Error al eliminar curso:', error)
      throw error
    }
  }
}