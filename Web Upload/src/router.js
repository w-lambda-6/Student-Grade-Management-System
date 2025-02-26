import Login from './views/Login.vue';
import Teachers from './views/Teachers.vue';
import Students from './views/Students.vue';

const routes = [
    {path : '/', component : Login},
    {path : '/login', component : Login},
    {path : '/students', component : Students},
    {path : '/teachers', component : Teachers},
];

export default routes;