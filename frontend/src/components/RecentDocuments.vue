<script setup>
defineProps({
  documents: { type: Array, required: true },
  selectedId: { type: Number, default: null },
})
defineEmits(['select'])

function formatDate(value) {
  return new Date(value).toLocaleString('ko-KR', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>

<template>
  <aside class="card recent">
    <h2>최근 문서</h2>
    <p v-if="!documents.length" class="muted">아직 업로드한 문서가 없습니다.</p>
    <ul>
      <li v-for="doc in documents" :key="doc.id">
        <button :class="{ active: doc.id === selectedId }" @click="$emit('select', doc.id)">
          <strong>{{ doc.filename }}</strong>
          <span class="muted">{{ formatDate(doc.created_at) }}</span>
        </button>
      </li>
    </ul>
  </aside>
</template>
