export interface SourceItem {
  title: string;
  url: string;
  type?: string;
}

export interface Message {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  timestamp: string;
  intent?: string;
  confidence?: number;
  entities?: Record<string, any>;
  sources?: SourceItem[];
  isError?: boolean;
}

export interface ChatResponse {
  answer: string;
  intent: string;
  confidence: number;
  entities: Record<string, any>;
  sources: SourceItem[];
  session_id: string;
}
