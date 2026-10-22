// Rails API 클라이언트 — 프론트엔드는 Rails만 호출한다.
import axios from 'axios'

const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000'}/api`,
})

// Rails의 { error } 응답을 사용자 메시지로 변환
export function errorMessage(err) {
  if (err.response?.data?.error) return err.response.data.error
  if (err.code === 'ERR_NETWORK') return '서버에 연결할 수 없습니다. Rails 서버(:3000)가 실행 중인지 확인하세요.'
  return err.message || '알 수 없는 오류가 발생했습니다.'
}

export async function listDocuments() {
  const { data } = await api.get('/documents')
  return data
}

export async function getDocument(id) {
  const { data } = await api.get(`/documents/${id}`)
  return data
}

export async function uploadDocument(file, onProgress) {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/documents', form, {
    onUploadProgress: (e) => e.total && onProgress?.(Math.round((e.loaded / e.total) * 100)),
  })
  return data
}

export async function listQuestions(documentId) {
  const { data } = await api.get(`/documents/${documentId}/questions`)
  return data
}

export async function askQuestion(documentId, question) {
  const { data } = await api.post(`/documents/${documentId}/questions`, { question })
  return data
}
