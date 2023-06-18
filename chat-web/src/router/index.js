import {createRouter, createWebHistory} from 'vue-router';

const router = createRouter({
    mode: 'hash',
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'ChatGPT',
            component: () => import('../views/ChatGPT.vue')
        },
        {
            path: '/python-repl',
            name: 'Python REPL',
            component: () => import('../views/PythonREPL.vue')
        },
        {
            path: '/meteo',
            name: 'Meteo',
            component: () => import('../views/Meteo.vue')
        }
    ]
})

export default router