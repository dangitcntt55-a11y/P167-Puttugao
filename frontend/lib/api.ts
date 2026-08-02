const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function fetchApi<T>(path: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_URL}${path}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });
  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

// Brands
export async function listBrands() {
  return fetchApi<Brand[]>("/brands/");
}

export async function getBrandVisibility(brandId: number, days = 7) {
  return fetchApi<VisibilityData>(`/visibility/${brandId}?days=${days}`);
}

// Diagnoses
export async function listDiagnoses(params: { brandId?: number; stableOnly?: boolean } = {}) {
  const searchParams = new URLSearchParams();
  if (params.brandId) searchParams.set("brand_id", params.brandId.toString());
  if (params.stableOnly !== undefined) searchParams.set("stable_only", params.stableOnly.toString());
  return fetchApi<Diagnosis[]>(`/diagnoses/?${searchParams.toString()}`);
}

export async function approveDiagnosis(diagnosisId: number) {
  return fetchApi<{ status: string }>(`/diagnoses/${diagnosisId}/approve`, { method: "POST" });
}

export async function rejectDiagnosis(diagnosisId: number) {
  return fetchApi<{ status: string }>(`/diagnoses/${diagnosisId}/reject`, { method: "POST" });
}

// Tasks
export async function listTasks(params: { brandId?: number; status?: string } = {}) {
  const searchParams = new URLSearchParams();
  if (params.brandId) searchParams.set("brand_id", params.brandId.toString());
  if (params.status) searchParams.set("status", params.status);
  return fetchApi<Task[]>(`/tasks/?${searchParams.toString()}`);
}

export async function updateTaskStatus(taskId: number, status: string) {
  return fetchApi<{ status: string }>(`/tasks/${taskId}`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });
}

// Evaluation
export async function getEvaluationReport(taskId: number) {
  return fetchApi<EvaluationReportData>(`/evaluation/${taskId}`);
}

// Scan
export async function triggerScan(brandId: number, nRuns = 3) {
  return fetchApi<ScanResponse>("/scan/", {
    method: "POST",
    body: JSON.stringify({ brand_id: brandId, n_runs: nRuns }),
  });
}

// Types
export interface Brand {
  id: number;
  name: string;
  name_variants: string[];
  brand_type: string;
  is_target: boolean;
  category: string;
  shopee_url: string | null;
  lazada_url: string | null;
  website_url: string | null;
}

export interface VisibilityData {
  brand_id: number;
  period_days: number;
  visibility_rate: number;
  sov: number;
  avg_stability: number;
  n_responses: number;
  trend: Array<{ date: string; visibility_rate: number; stability: number }>;
  computed_at: string;
}

export interface Diagnosis {
  id: number;
  brand_id: number;
  prompt_id: number;
  is_stable: boolean;
  stability_score: number;
  hypotheses: Array<{ hypothesis: string; confidence: number; evidence_urls: string[] }>;
  evidence_package: Record<string, unknown>;
  recommended_actions: Array<{ action_type: string; target_url: string; suggested_change: string }>;
  severity: string;
  status: string;
  created_at: string;
}

export interface Task {
  id: number;
  brand_id: number;
  diagnosis_id: number | null;
  action_type: string;
  owner_team: string | null;
  status: string;
  result: string | null;
  ci_lower: number | null;
  ci_upper: number | null;
  pre_visibility: number | null;
  post_visibility: number | null;
  created_at: string;
}

export interface EvaluationReportData {
  task_id: number;
  brand_id: number;
  action_type: string;
  pre_visibility: number | null;
  post_visibility: number | null;
  ci_lower: number | null;
  ci_upper: number | null;
  result: string | null;
  completed_at: string | null;
}

export interface ScanResponse {
  task_id: string;
  status: string;
  brand_id: number;
  n_prompts: number;
  n_engines: number;
}
