<script setup lang="ts">
import HeaderBar from './components/HeaderBar.vue'
</script>

<template>
  <div class="app">
    <HeaderBar />
    <main>
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}
</style>
