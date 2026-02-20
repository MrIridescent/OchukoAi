/**
 * Frontend TypeScript Types
 * Defines all data structures used in the React application
 */

export type MessageRole = 'user' | 'assistant';

export type Emotion = 'happy' | 'sad' | 'angry' | 'surprised' | 'neutral' | 'fearful' | 'disgusted';

export type Intent = 
  | 'query'
  | 'command'
  | 'statement'
  | 'emotion'
  | 'request'
  | 'clarification'
  | 'unknown';

export type ActionType = 
  | 'send_email'
  | 'get_weather'
  | 'play_music'
  | 'schedule_event'
  | 'set_reminder'
  | 'search_web'
  | 'create_task'
  | 'none';

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: Date;
  thinking?: string;
  action?: string;
  emotion?: string;
  confidence?: number;
}

export interface APIResponse<T = any> {
  status: 'success' | 'error';
  data?: T;
  error?: string;
  message?: string;
}

export interface ProcessTextRequest {
  text: string;
  context?: string;
}

export interface ProcessTextResponse {
  status: string;
  response: string;
  action?: string;
  confidence: number;
  thinking?: string;
  intent?: Intent;
  timestamp: string;
}

export interface FaceRecognitionResponse {
  status: string;
  identified_user?: string;
  confidence: number;
  emotion?: Emotion;
  all_faces?: FaceResult[];
  action_recommended?: string;
  error?: string;
}

export interface FaceResult {
  user_id: string;
  confidence: number;
  emotion: Emotion;
  emotion_confidence: number;
  bounding_box: BoundingBox;
  landmarks?: Point[];
}

export interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface Point {
  x: number;
  y: number;
}

export interface ProcessVoiceResponse {
  status: string;
  recognized_text: string;
  response_text: string;
  response_audio: string; // base64
  action?: string;
}

export interface WebSocketMessage {
  type: 'text' | 'command' | 'response' | 'command_result' | 'error';
  content?: string;
  text?: string;
  action?: string;
  thinking_process?: string;
  status?: string;
  result?: any;
  error?: string;
}

export interface MemoryData {
  conversation_history: Message[];
  learned_patterns: LearnedPattern[];
  user_preferences: UserPreferences;
}

export interface LearnedPattern {
  type: string;
  pattern: string;
  confidence: number;
  learned_at: string;
}

export interface UserPreferences {
  [key: string]: any;
  language?: string;
  timezone?: string;
  theme?: 'light' | 'dark';
  communication_style?: 'formal' | 'casual' | 'technical';
}

export interface Capability {
  name: string;
  enabled: boolean;
  description?: string;
}

export interface SystemStatus {
  status: 'operational' | 'degraded' | 'offline';
  systems: {
    ai_orchestrator: boolean;
    face_recognition: boolean;
    speech: boolean;
  };
  version: string;
}

export interface LearnRequest {
  type: string;
  data: any;
}

export interface LearnResponse {
  status: 'success' | 'error';
  message: string;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  created_at: string;
  updated_at: string;
  assigned_to?: string;
}

export interface User {
  id: string;
  name: string;
  email?: string;
  preferences?: UserPreferences;
  face_encodings?: number[];
  created_at: string;
}

export interface ConversationContext {
  conversation_id: string;
  user_id: string;
  started_at: string;
  last_activity: string;
  messages: Message[];
  context_data: Record<string, any>;
}

export interface CommandExecution {
  command: string;
  params: Record<string, any>;
  status: 'pending' | 'executing' | 'completed' | 'failed';
  result?: any;
  error?: string;
  executed_at?: string;
}

export interface IntentAnalysis {
  primary_intent: Intent;
  sub_intents: string[];
  sentiment: 'positive' | 'neutral' | 'negative';
  requires_action: boolean;
  action_type?: ActionType;
  action_params?: Record<string, any>;
  priority: 'low' | 'medium' | 'high' | 'critical';
  confidence: number;
}
