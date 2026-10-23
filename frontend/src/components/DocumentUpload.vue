<script setup>
import { ref } from 'vue'
import { uploadDocument, errorMessage } from '../api/document'

const emit = defineEmits(['uploaded'])

// Rails(Document::ALLOWED_EXTENSIONS), FastAPI(document_parser.py)와 같은 형식이어야 한다.
const ALLOWED = ['.txt', '.md', '.markdown', '.pdf', '.docx', '.pptx']
const ALLOWED_LABEL = 'TXT, MD, PDF, DOCX, PPTX'
const ACCEPT = ALLOWED.join(',')
// 구형 Office 형식은 지원하지 않고 변환을 안내한다.
const LEGACY = { '.doc': '.docx', '.ppt': '.pptx' }
const MAX_MB = 10

const dragging = ref(false)
const progress = ref(0)
const phase = ref('idle') // idle | uploading | summarizing
const error = ref('')
const input = ref(null)

function validate(file) {
  const dot = file.name.lastIndexOf('.')
  const ext = dot < 0 ? '' : file.name.slice(dot).toLowerCase()
  if (LEGACY[ext]) return `구형 ${ext} 형식은 지원하지 않습니다. ${LEGACY[ext]}로 저장한 뒤 업로드해 주세요.`
  if (!ALLOWED.includes(ext)) return `${ALLOWED_LABEL} 파일만 업로드할 수 있습니다.`
  if (file.size > MAX_MB * 1024 * 1024) return `파일이 너무 큽니다. (최대 ${MAX_MB}MB)`
  return ''
}

async function handle(file) {
  if (!file || phase.value !== 'idle') return
  error.value = validate(file)
  if (error.value) return

  phase.value = 'uploading'
  progress.value = 0
  try {
    const doc = await uploadDocument(file, (p) => {
      progress.value = p
      if (p >= 100) phase.value = 'summarizing'
    })
    emit('uploaded', doc)
  } catch (err) {
    error.value = errorMessage(err)
  } finally {
    phase.value = 'idle'
    if (input.value) input.value.value = ''
  }
}

function onDrop(e) {
  dragging.value = false
  handle(e.dataTransfer.files[0])
}
</script>

<template>
  <section
    class="card upload"
    :class="{ dragging, busy: phase !== 'idle' }"
    @dragover.prevent="dragging = true"
    @dragleave.prevent="dragging = false"
    @drop.prevent="onDrop"
    @click="phase === 'idle' && input.click()"
  >
    <input ref="input" type="file" :accept="ACCEPT" hidden @change="handle($event.target.files[0])" />

    <template v-if="phase === 'idle'">
      <div class="upload-icon">⇪</div>
      <p class="upload-title">파일을 끌어다 놓거나 클릭해서 선택하세요</p>
      <p class="muted">{{ ALLOWED_LABEL }} · 최대 {{ MAX_MB }}MB</p>
    </template>

    <template v-else>
      <p class="upload-title">{{ phase === 'uploading' ? '업로드 중…' : 'AI가 문서를 요약하고 있습니다…' }}</p>
      <div class="progress"><div class="bar" :class="{ pulse: phase === 'summarizing' }" :style="{ width: progress + '%' }" /></div>
      <p class="muted">{{ phase === 'uploading' ? `${progress}%` : '긴 문서는 1분 이상 걸릴 수 있습니다.' }}</p>
    </template>

    <p v-if="error" class="error" @click.stop>{{ error }}</p>
  </section>
</template>
