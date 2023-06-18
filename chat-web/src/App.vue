<script setup>
import {RouterLink, RouterView} from 'vue-router';
</script>

<template>
    <div>
        <RouterLink to="/">Chat</RouterLink>
        |
        <RouterLink to="/python-repl">Python</RouterLink>
        |
        <RouterLink to="/meteo">Meteo</RouterLink>
    </div>
    <RouterView />
</template>

<style scoped>
</style>
