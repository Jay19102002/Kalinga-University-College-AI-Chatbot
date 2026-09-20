import { ChatResponse } from '../types/chat';

const API_BASE_URL = '/api';

export async function sendMessage(message: string, sessionId: string): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      session_id: sessionId,
    }),
  });

  if (!response.ok) {
    throw new Error(`Server returned error status ${response.status}`);
  }

  return response.json();
}

export async function getHealthStatus() {
  const response = await fetch(`${API_BASE_URL}/health`);
  return response.json();
}

export async function getKnowledgeData(type: string, params: Record<string, any> = {}) {
  const queryStr = new URLSearchParams(
    Object.entries(params).filter(([_, v]) => v !== undefined && v !== null && v !== '')
  ).toString();
  const url = queryStr ? `${API_BASE_URL}/${type}?${queryStr}` : `${API_BASE_URL}/${type}`;
  const response = await fetch(url);
  return response.json();
}

export async function getDatabaseStats() {
  const response = await fetch(`${API_BASE_URL}/database/stats`);
  return response.json();
}

export async function searchDatabase(q: string, entityType?: string, limit: number = 25) {
  const params = new URLSearchParams({ q });
  if (entityType) params.append('entity_type', entityType);
  if (limit) params.append('limit', limit.toString());
  const response = await fetch(`${API_BASE_URL}/database/search?${params.toString()}`);
  return response.json();
}

export async function getResearchPapers(page: number = 1, limit: number = 20, query?: string, department?: string, year?: string) {
  return getKnowledgeData('research-papers', { page, limit, query, department, year });
}

export async function getBooks(page: number = 1, limit: number = 20, query?: string, department?: string, year?: string) {
  return getKnowledgeData('books', { page, limit, query, department, year });
}

export async function getNewsEvents(query?: string, category?: string) {
  return getKnowledgeData('news-events', { query, category });
}

export async function getWebPages(query?: string) {
  return getKnowledgeData('pages', { query });
}

export async function getDataTables(query?: string) {
  return getKnowledgeData('catalogue', { query });
}
