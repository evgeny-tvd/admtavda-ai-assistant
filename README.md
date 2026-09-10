# admtavda-ai-assistant

ИИ-ассистент администрации Тавдинского муниципального округа: бот в MAX, отвечает жителям по базе знаний (режим работы, контакты, порядок обращений), позже — погода и новости сайта.

## Статус

Учебный проект DevOps-курса. Закрыты шаги 0, 0.5 и 1:

- **Шаг 0** — каркас: эхо-бот в MAX (Long Polling), работа только через PR, commitlint на двух въездах (локальный хук + CI), main защищён;
- **Шаг 0.5** — серверы проекта на офисном pve1: **CT104** `ai-assistant` (10.10.20.50) — бот, CI-runner, registry; **CT105** `gateway` (10.10.20.60) — общий публичный вход офиса (443, маршрутизация по поддоменам);
- **Шаг 1** — команда `/ask`: вопрос → GigaChat → ответ в чат (системный промпт, graceful degradation при сбое LLM).

Сейчас в работе **Шаг 2 — база знаний**: вопросы жителей → карточки в `knowledge/faq/`, набор вопросов для оценки → `evals/`.

## Стек

- Python **3.12** (venv проекта — 3.12.3; SDK `gigachat` заявляет поддержку до 3.13)
- MAX Bot API — `maxapi==1.2.2`
- GigaChat API (Сбер, РФ) — `gigachat==0.2.3`
- `python-dotenv==1.2.3`

## Структура

- `src/` — код бота
- `evals/` — набор вопросов для оценки качества ответов (материал Шага 6)
- `knowledge/faq/` — база знаний: один файл = одна карточка (Шаг 2, в работе)
- `package.json`, `.husky/` — commitlint (формат коммитов), `commitlint.config.cjs`
- `.env` — секреты (не в git!)

## Быстрый старт (dev)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # заполнить BOT_TOKEN и GIGACHAT_CREDENTIALS
chmod 600 .env

python src/bot.py
```

Получение событий в dev — **Long Polling**: бот сам опрашивает MAX, публичный URL не нужен. Для production MAX рекомендует **Webhook** (Long Polling ограничен по скорости и сроку хранения событий) — подключается на Шаге 8 через gateway CT105.

## Секреты

Токен бота и ключ GigaChat — только в `.env` (права 600, файл в `.gitignore`). Прод-секреты живут на сервере (CT104) и в GitHub не передаются. Перед коммитом: `git diff` глазами и `git diff --cached --check`.

## Правила работы

- В `main` — только через PR: короткая ветка `feature/...`, ревью, squash-merge, ветка удаляется.
- Коммиты — Conventional Commits (`feat:`/`fix:`/`docs:`/`chore:`/`test:`/`ci:`), проверяет commitlint.
