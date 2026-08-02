# Hướng dẫn cài đặt AI Log Hook cho đồ án nhóm

> **Mục đích**: Mỗi prompt sinh viên gửi cho Cursor/Antigravity + mỗi lần `git push` đều được ghi nhận tự động lên server chấm bài của giảng viên.
> **Server URL**: `https://ai-logs.note.transformerlabs.ai/api/ingest`
> **Áp dụng cho**: Đăng, Lý, Khôi, Hải — ai cũng cài 1 lần sau khi clone repo.

---

## 1. Bạn sẽ cài gì?


| Thành phần                   | Vai trò                                                                    | Khi nào chạy                             |
| ---------------------------- | -------------------------------------------------------------------------- | ---------------------------------------- |
| `.cursor/hooks.json`         | Cursor IDE hook — capture mỗi prompt bạn gửi cho AI                        | Tự động, mỗi khi nhấn Enter trong Cursor |
| `scripts/log_antigravity.py` | Quét lịch sử chat Antigravity (file `~/.gemini/antigravity-ide/brain/...`) | Tự động, mỗi lần `git push`              |
| `scripts/submit_log.py`      | POST JSON lên server chấm bài                                              | Tự động, mỗi lần `git push`              |
| `.git/hooks/pre-push.cmd`    | Git hook trên Windows — trigger 2 script ở trên                            | Tự động, mỗi lần `git push`              |


**Cài xong 1 lần → chạy mãi mãi, không cần làm gì thêm.**

---



## 2. Cài đặt từng bước (Windows)



### 2.1. Clone repo (nếu chưa có)

```powershell
cd D:\AI_THUCCHIEN
git clone https://github.com/dangitcntt55-a11y/P167-Puttugao.git BTNHOM
cd BTNHOM
```



### 2.2. Tạo file `.env`

Copy từ bạn Đăng hoặc tự tạo:

```powershell
Copy-Item .env.example .env -Force
notepad .env
```

Điền 2 dòng cuối (đã có sẵn trong repo root .env nhưng trong `.env.example` chưa có):

```ini
AI_LOG_SERVER=https://ai-logs.note.transformerlabs.ai/api/ingest
AI_LOG_API_KEY=
AI_LOG_DIR=.ai-log
```

> ⚠️ **Key này là key nhóm** — ai cũng dùng chung. KHÔNG tự ý rotate.
> Nếu key lộ (commit lên public repo) → ping Đăng ngay để rotate.



### 2.3. Cấu hình git credential (chỉ cần làm 1 lần)

Nếu bạn chưa push được lần nào, chạy 2 lệnh này:

```powershell
git config --global credential.credentialStore dpapi
```

Giải thích: git trên Windows thường set `wincred` (Windows Credential Manager) nhưng trong một số môi trường không có GUI manager → phải fallback `dpapi` (file mã hoá).

### 2.4. Cài git pre-push hook

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_hooks.ps1
```

Output mong đợi:

```
[ai-log] Git pre-push hook installed.
[ai-log] Setup complete. Configure AI_LOG_SERVER in your .env file.
```

**Kiểm tra**:

```powershell
dir .git\hooks\pre-push*
```

→ Phải thấy `pre-push.cmd` (KHÔNG phải `pre-push` không extension). Nếu thấy `pre-push` thì đổi tên:

```powershell
ren .git\hooks\pre-push pre-push.cmd
```



### 2.5. Cài Cursor hook

Cursor đọc `.cursor/hooks.json` **ở workspace root**. File này đã có sẵn trong repo. Bạn chỉ cần **mở lại Cursor** sau khi clone xong để nó pick up hook.

**Kiểm tra**: mở bất kỳ file nào trong `D:\AI_THUCCHIEN\BTNHOM`, gõ thử 1 message cho AI rồi Enter → check file `.ai-log/session.jsonl` có entry mới không:

```powershell
Get-Content .ai-log/session.jsonl
```

→ Phải thấy 1 dòng JSON với `"tool": "cursor"`.

---



## 3. Verify setup (chạy 1 lần sau khi cài)



### 3.1. Test thủ công submit_log

```powershell
python scripts\submit_log.py
```

Output mong đợi (nếu session.jsonl có entries):

```
[ai-log] Submitted N entries → 202
```

**Giải thích status code**:

- `202 Accepted` = server đã nhận (OK!)
- `200` = cũng OK (server trả tùy phiên bản)
- `401` = sai key → check `.env`
- `422` = payload invalid → ping Đăng
- Connection refused / timeout = server chưa lên (lỗi mạng, KHÔNG chặn push)



### 3.2. Test push thật

```powershell
echo test_log_setup > test_push.txt
git add test_push.txt
git commit -m "test: verify ai-log hook"
git push origin main:main
```

Khi push, terminal sẽ in ra:

```
[antigravity-log] Logged X prompt(s) from Antigravity IDE.
[ai-log] Submitted N entries → 202
```

(nếu bạn đang ở Cursor và vừa nhập prompt trước đó).

### 3.3. Check archive

```powershell
dir .ai-log\archive
```

→ Phải thấy file `YYYY-MM-DD.jsonl`. Mỗi entry là 1 dòng JSON, đại diện 1 prompt.

---



## 4. Cấu trúc file log

```
.ai-log/
├── session.jsonl          # log "sống" — Cursor hook append vào đây
├── .gitkeep               # git placeholder (file trống)
└── archive/
    └── 2026-08-02.jsonl   # đã submit thành công, rotate ra đây (append-only)
```

**Mỗi entry** có dạng:

```json
{
  "ts": "2026-08-02T20:00:49.980895+07:00",
  "tool": "cursor",                       // hoặc "antigravity"
  "event": "beforeSubmitPrompt",          // hoặc "UserPrompt" / "TaskComplete"
  "entry_id": "...",
  "session_id": "...",
  "model": "claude-fable-5",              // hoặc "gemini"
  "repo": "P167-Puttugao",
  "branch": "main",
  "commit": "782269d",
  "student": "dangitcntt55@gmail.com",    // lấy từ git config user.email
  "prompt": "Test setup AI log cho dự án BTNHOM",
  "response_summary": "..."
}
```

---



## 5. Câu hỏi thường gặp



### Q: Push xong không thấy log trên server?

1. Check session.jsonl có entries không:
  ```powershell
   Get-Content .ai-log/session.jsonl
  ```
   → Nếu rỗng → Cursor hook chưa chạy → mở lại Cursor rồi gõ 1 prompt test.
2. Test submit thủ công:
  ```powershell
   python scripts\submit_log.py
  ```
   → Phải in `[ai-log] Submitted N entries → 202`.
3. Check `.env` đã có `AI_LOG_SERVER` + `AI_LOG_API_KEY`:
  ```powershell
   Get-Content .env | Select-String "AI_LOG"
  ```



### Q: Bị lỗi `Unknown credential store 'wincred'` khi push?

Chạy:

```powershell
git config --global credential.credentialStore dpapi
```



### Q: Bị lỗi `cannot spawn .git/hooks/pre-push`?

File hook phải có extension `.cmd`:

```powershell
dir .git\hooks\pre-push*
```

→ Phải có `pre-push.cmd`. Nếu chỉ thấy `pre-push`:

```powershell
ren .git\hooks\pre-push pre-push.cmd
```



### Q: Status `202` có phải lỗi không?

Không! `202 Accepted` nghĩa là server đã nhận payload thành công và sẽ xử lý async. Đây là response bình thường.

### Q: Tôi không dùng Cursor/Antigravity mà dùng tool khác (Claude Code, Codex, Grok…)?

`scripts/log_antigravity.py` chỉ sweep 2 IDE trên. Với tool khác, cần thêm bộ hook riêng — báo Đăng để integrate.

### Q: session.jsonl đầy quá (gần 500 entries)?

`submit_log.py` tự batch 500 entries/lần. Phần còn lại sẽ tự động submit ở push sau. Không cần lo.

---



## 6. Quy trình làm việc hằng ngày

1. **Sáng**: Kéo code mới nhất về (`git pull`).
2. **Trong ngày**: Code bình thường, gửi prompt cho AI bình thường — không cần làm gì thêm.
3. **Cuối ngày / khi xong task**: `git add` → `git commit` → `git push`.
  → Hook tự động scan + submit log. Bạn sẽ thấy 1–2 dòng `[ai-log] Submitted N entries → 202` ở terminal.
4. **Không cần làm gì khác**.

---



## 7. Không commit những thứ này

Đã được `.gitignore` filter, nhưng nhắc lại để khỏi lo:

- `.env` (file thật) → dùng `.env.example`
- `.ai-log/session.jsonl` (log chưa submit)
- `.ai-log/archive/*.jsonl` (log đã submit, dùng để debug offline thôi)

---



## 8. Khi gặp vấn đề

Làm theo thứ tự:

1. Xem lại **§3 Verify setup** ở trên.
2. Check **§5 FAQ**.
3. Chạy `python scripts\submit_log.py` thủ công, copy output lỗi gửi Đăng.

---

> 📌 **Tổng kết**: Sau khi cài 1 lần, bạn sẽ không cần quan tâm đến AI log nữa. Mỗi push = 1 lần submit tự động.
> 📌 **Server trả 202 = OK**, không phải lỗi.
> 📌 **Key nhóm** nằm trong `.env` ở repo root — ai cũng dùng chung.

