<script setup>
import { computed } from 'vue'

const props = defineProps({
  document: { type: Object, required: true },
})

// 모델이 반환한 간단한 마크다운(## 제목, - 불릿)을 블록 단위로 나눈다. (v-html 미사용)
const blocks = computed(() => {
  const result = []
  for (const raw of (props.document.summary || '').split('\n')) {
    const line = raw.trim()
    if (!line) continue
    if (line.startsWith('#')) {
      result.push({ type: 'heading', text: line.replace(/^#+\s*/, '') })
    } else if (/^[-*•]\s+/.test(line)) {
      const last = result.at(-1)
      const item = line.replace(/^[-*•]\s+/, '').replace(/\*\*/g, '')
      if (last?.type === 'list') last.items.push(item)
      else result.push({ type: 'list', items: [item] })
    } else {
      result.push({ type: 'text', text: line.replace(/\*\*/g, '') })
    }
  }
  return result
})

const meta = computed(() => {
  const kb = ((props.document.byte_size || 0) / 1024).toFixed(1)
  const chars = (props.document.char_count || 0).toLocaleString()
  return `${kb} KB · ${chars}자`
})
</script>

<template>
  <section class="card summary">
    <div class="summary-head">
      <h2>{{ document.filename }}</h2>
      <span class="muted">{{ meta }}</span>
    </div>
    <div class="summary-body">
      <template v-for="(block, i) in blocks" :key="i">
        <h3 v-if="block.type === 'heading'">{{ block.text }}</h3>
        <ul v-else-if="block.type === 'list'">
          <li v-for="(item, j) in block.items" :key="j">{{ item }}</li>
        </ul>
        <p v-else>{{ block.text }}</p>
      </template>
    </div>
  </section>
</template>
