<script setup>
import HomeView from './views/HomeView.vue'
</script>

<template>
  <header class="app-header">
    <div class="brand">
      <img src="/favicon.svg" alt="" width="28" height="28" />
      <span>DocuForge</span>
    </div>
    <p class="tagline">문서를 올리면 요약하고, 질문하면 답합니다 · Ollama gemma4:12b</p>
  </header>
  <HomeView />
</template>
