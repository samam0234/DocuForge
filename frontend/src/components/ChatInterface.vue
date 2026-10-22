<script setup>
import { nextTick, ref, watch } from 'vue'
import { askQuestion, listQuestions, errorMessage } from '../api/document'

const props = defineProps({
  documentId: { type: Number, required: true },
})

const history = ref([])
const question = ref('')
const pending = ref(null) // 답변 대기 중인 질문
const error = ref('')
const scroller = ref(null)

async function scrollToBottom() {
  await nextTick()
  if (scroller.value) scroller.value.scrollTop = scroller.value.scrollHeight
}

watch(
  () => props.documentId,
  async (id) => {
    history.value = []
    error.value = ''
    try {
      history.value = await listQuestions(id)
      scrollToBottom()
    } catch (err) {
      error.value = errorMessage(err)
    }
  },
  { immediate: true },
)

async function submit() {
  const text = question.value.trim()
  if (!text || pending.value) return
  pending.value = text
  question.value = ''
  error.value = ''
  scrollToBottom()
  try {
    history.value.push(await askQuestion(props.documentId, text))
  } catch (err) {
    error.value = errorMessage(err)
    question.value = text
  } finally {
    pending.value = null
    scrollToBottom()
  }
}

function onKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) {
    e.preventDefault()
    submit()
  }
}
</script>

<template>
  <section class="card chat">
    <h2>문서에 질문하기</h2>

    <div ref="scroller" class="messages">
      <p v-if="!history.length && !pending" class="muted empty">요약에 없는 세부 내용도 물어보세요.</p>

      <div v-for="qa in history" :key="qa.id" class="turn">
        <div class="bubble user">{{ qa.question }}</div>
        <div class="bubble bot">
          <p>{{ qa.answer }}</p>
          <details v-if="qa.sources?.length" class="sources">
            <summary>근거 문장 {{ qa.sources.length }}개</summary>
            <blockquote v-for="(src, i) in qa.sources" :key="i">
              <span class="tag">발췌 {{ i + 1 }}</span>{{ src.text }}
            </blockquote>
          </details>
        </div>
      </div>

      <div v-if="pending" class="turn">
        <div class="bubble user">{{ pending }}</div>
        <div class="bubble bot typing"><span /><span /><span /></div>
      </div>
    </div>

    <p v-if="error" class="error">{{ error }}</p>

    <form class="composer" @submit.prevent="submit">
      <textarea
        v-model="question"
        rows="2"
        placeholder="질문을 입력하세요 (Enter 전송, Shift+Enter 줄바꿈)"
        :disabled="!!pending"
        @keydown="onKeydown"
      />
      <button type="submit" :disabled="!question.trim() || !!pending">전송</button>
    </form>
  </section>
</template>
