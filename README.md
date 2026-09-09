# 獎學金申請工作台

把真實經歷整理為可驗證、有說服力、符合各獎學金要求的申請資料。此工作台以 agent 執行與本機檔案為核心；不需要架網站或申請 API 金鑰。

## 現在開始

1. 將 `templates/profile.md` 複製至 `private/profile.md`，填入背景與連結。`private/` 內檔案不進 Git。
2. 把 `prompts/export-background.md` 貼到最了解你的 ChatGPT 對話，將回覆存成 `private/background-export.md`。自行核對事實後，再整合至 profile。
3. 將自傳、履歷、成績單、獎狀等放進 `private/evidence/`，按照 `templates/evidence.md` 建立 `private/evidence-index.md`。
4. 上傳郵件提到的玉山 PDF 原檔，放到 `applications/2026-esun/private/source/`。目前只有郵件文字及官網資訊，附件尚未收到。
5. 將 `prompts/apply.md` 的案件名稱改成 `2026-esun` 並貼給 agent；未填完的資料可以先留空，agent 會整理缺口。

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

Git 排除不是備份；請自行將私人資料備份至你信任的位置。共用版控只存你確認可公開的內容。沒有設定背景排程；追蹤由每次啟動 agent 更新。
