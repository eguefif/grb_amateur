<script setup lang="ts">
import HeaderBar from './components/HeaderBar.vue'
import ObservationList from './components/ObservationList.vue'
</script>

<template>
  <div class="app">
    <HeaderBar />
    <main>
      <ObservationList />
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
