<script setup>
import { onMounted, ref } from 'vue'
import DocumentUpload from '../components/DocumentUpload.vue'
import SummaryCard from '../components/SummaryCard.vue'
import ChatInterface from '../components/ChatInterface.vue'
import RecentDocuments from '../components/RecentDocuments.vue'
import { getDocument, listDocuments, errorMessage } from '../api/document'

const documents = ref([])
const current = ref(null)
const error = ref('')

async function refreshList() {
  try {
    documents.value = await listDocuments()
  } catch (err) {
    error.value = errorMessage(err)
  }
}

async function select(id) {
  error.value = ''
  try {
    current.value = await getDocument(id)
  } catch (err) {
    error.value = errorMessage(err)
  }
}

function onUploaded(doc) {
  current.value = doc
  refreshList()
}

onMounted(refreshList)
</script>

<template>
  <main class="layout">
    <RecentDocuments :documents="documents" :selected-id="current?.id ?? null" @select="select" />

    <div class="main-col">
      <DocumentUpload @uploaded="onUploaded" />
      <p v-if="error" class="error">{{ error }}</p>

      <template v-if="current">
        <SummaryCard :document="current" />
        <ChatInterface :document-id="current.id" />
      </template>
    </div>
  </main>
</template>
