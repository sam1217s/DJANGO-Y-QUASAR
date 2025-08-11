const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: '/cursos', component: () => import('pages/CursosPage.vue') },
      { path: '/servicios', component: () => import('src/pages/CapacitacionPage.vue') },
      { path: '/asesoria', component: () => import('pages/AsesoriaPage.vue') }

      

    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes