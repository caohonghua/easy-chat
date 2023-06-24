<script setup>
import {RouterLink, RouterView} from 'vue-router';
</script>

<template>
    <div>
        <RouterLink to="/">Chat</RouterLink>
        |
        <RouterLink to="/repl">Python</RouterLink>
    </div>
    <RouterView />
</template>

<style scoped>
</style>
