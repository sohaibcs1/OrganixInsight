// layouts
import MainLayout from '../layouts/MainLayout.vue';

// pages
import ErrorPage from '../pages/Error404.vue';
import Login from '../pages/Login.vue';
import Resources from '../pages/Resources.vue';
import design from '../pages/Design.vue';
import admin from '../components/admin/addUserDetails.vue';


const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      { path: '', redirect: '/design'},
      {
        path: 'login', component: Login, meta: { guest: true }
      },
      {
        path: 'resources', component: Resources, meta: { auth: true }
      },
      {
        path: 'design', component: design, meta: { auth: true },
      
        
      },
      {
        path: 'admin', component: admin, meta: { auth: true }
        
      },

    
   
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: ErrorPage
  }
]

export default routes
