# 獎學金申請工作台

把真實經歷整理為可驗證、有說服力、符合各獎學金要求的申請資料。此工作台以 agent 執行與本機檔案為核心；不需要架網站或申請 API 金鑰。

## 現在開始

**在這個專案的 agent chat 直接貼整份獎學金公告、郵件、連結或附件即可。** 不需要案件 ID、特殊 prompt、填模板或維護檔案。Agent 會自行建案／接續舊案，完成資格核對、資料盤點、客製文稿、PDF／官定格式、附件整理與送件步驟。

你的背景以兩個網站為主，每次產生申請文件都重新讀取：

- 個人網站：https://me.jjmowlab.com
- GitHub：https://github.com/egger-meow

你照常更新網站與 GitHub 即可，不必再更新本地背景檔。直接貼獎學金說明，或說「繼續玉山」，agent 會讀取最新網站、相關作品與當案規則，產生需要的文件。

網站沒有的必要資訊或正式證明，才由 agent 在對話中向你取得。已收到的附件與答案不重複索取，案件進度由 agent 接續處理。

每次也會讀取 `private/export-background.md`（或 `private/background-export.md`），把 GPT 對你的動機、個性與長期目標的理解用於申請敘事。網站與 GitHub 負責最新公開經歷，背景匯出補充個人脈絡，正式證明支持資格與成果；三者一起使用。你有新版匯出直接貼給 agent，它會負責保存與整合，不需要自己改檔。

本地保留必要附件、背景匯出、申請草稿、PDF 與案件紀錄；由 agent 維護。既有 profile 也可補充，沒有背景匯出時不會阻止其他工作。

Agent 會一路做到可交付；只有必要資料缺漏、登入／簽名／驗證或最後送件授權需要你參與。正式提交後以收據確認完成。這套入口適用於開在本專案的 agent 對話，其他聊天不會自動取得此 repo 的私人檔案。

## 結構與資料流

`背景與證據 → 資格檢查 → 官方要求對照 → 案件策略 → Markdown 草稿 → 事實與格式審查 → PDF → 人工確認並送件 → 收據與結果 → 學期追蹤`

- `templates/`：可重用的空白模板，不放個資。
- `prompts/`：背景匯出與每次申請的操作 prompt。
- `private/`：個人背景、原始附件、私人連結、跨案追蹤；只存在本機。
- `applications/<年度>-<名稱>/`：公開規則與來源。
- 每案 `private/`、`drafts/`、`output/`、`submission/`：分別放私人策略與進度、草稿、PDF、送件快照及收據；均排除 Git。
- `scripts/workflow.py`：建立案件、檢查 Markdown、輸出 PDF。

## 指令

使用 Python 3；PDF 功能需要 `reportlab`（目前 Codex 隨附環境已有）。一般環境可用 `python -m pip install -r requirements.txt` 安裝。

```text
python scripts/workflow.py init 2027-example
python scripts/workflow.py check applications/2027-example/drafts/application.md
python scripts/workflow.py pdf applications/2027-example/drafts/application.md --output applications/2027-example/output/application.pdf
```

PDF 支援標題、一般段落與清單，繁體中文使用 ReportLab CJK 字型。表格、圖片、複雜 Markdown 會被拒絕，交由 agent 採適合的文件工具處理。PDF 是一般附件版型；官方若指定表格、欄位、字數或檔案限制，必須另外依規格製作。輸出 PDF 不等於通過送件審查；需檢查每頁中文與分頁。

## 取得填空資料

- 學校、系所、入學年度、學位／在職狀態：錄取通知、學籍系統、在學證明。
- 成績與排名：教務處正式成績單／排名證明；保留滿分尺度及統計期間。
- 專案與研究：GitHub、論文、簡報、展示頁；寫清楚本人貢獻、時間與可驗證成果。
- 服務與領導：服務證明、活動紀錄、主辦單位確認；記錄對象、時數、成果。
- 戶籍與身分附件：按當案官方要求取得；玉山要求最近三個月內戶籍謄本，不要過早申請而過期。
- 推薦信：僅當案要求或允許時準備；先取得推薦人同意，agent 可協助擬邀請稿。

Git 排除不是備份；請自行將私人資料備份至你信任的位置。共用版控只存你確認可公開的內容。狀態在對話開始與結束時更新；沒有背景排程，離線時不會持續讀網站、信箱或主動提醒。若之後要求定時提醒，再使用 Codex 排程。
