export const AI_ENGINES = ["chatgpt", "gemini", "claude", "tavily"] as const;
export const AI_ENGINE_LABELS: Record<string, string> = {
  chatgpt: "ChatGPT",
  gemini: "Gemini",
  claude: "Claude",
  tavily: "Tavily",
};

export const PROMPT_GROUPS = ["uy_tin", "gia", "so_sanh", "review", "ship"] as const;
export const PROMPT_GROUP_LABELS: Record<string, string> = {
  uy_tin: "Uy tín",
  gia: "Giá",
  so_sanh: "So sánh",
  review: "Review",
  ship: "Ship",
};

export const ACTION_TYPES = ["listing_update", "content_add", "schema_add", "outreach", "content_pr"] as const;
export const ACTION_LABELS: Record<string, string> = {
  listing_update: "Cập nhật listing",
  content_add: "Thêm nội dung",
  schema_add: "Thêm schema",
  outreach: "Outreach",
  content_pr: "Bài PR",
};

export const TASK_STATUS = ["todo", "in_progress", "done", "cancelled"] as const;
export const TASK_STATUS_LABELS: Record<string, string> = {
  todo: "Cần làm",
  in_progress: "Đang làm",
  done: "Xong",
  cancelled: "Hủy",
};
