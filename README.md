# CI Workshop — Slot Machine

Мини-практика CI для двух человек: оба редактируют один файл `slot-machine.txt` и учатся держать **green build** через частую интеграцию и автоматическую проверку.

Пошаговый сценарий (раунды без CI и с CI, роли A/B) — в [RULES.md](RULES.md).

## Структура репозитория

| Файл | Назначение |
|------|------------|
| `slot-machine.txt` | Конфиг слот-машины: symbols и payouts |
| `test_slot_machine.py` | Проверка файла на green/red build |
| `RULES.md` | Правила воркшопа и упражнения |
| `requirements.txt` | Зависимости для тестов (`pytest`) |

## Формат `slot-machine.txt`

```
SLOT GAME

Symbols:
- CHERRY
- STAR

Payouts:
- CHERRY CHERRY CHERRY = x2
- STAR STAR STAR = x5
```

Строка payout: `- SYMBOL SYMBOL SYMBOL = xN` или `= JACKPOT`.

## Green / Red build

**Green** — проверка проходит, если:

- структура файла валидна (`SLOT GAME`, секции `Symbols:` и `Payouts:`);
- каждый symbol из `Symbols:` описан в `Payouts:`;
- нет маркеров merge conflict (`<<<<<<<`, `=======`, `>>>>>>>`).

**Red** — проверка падает, если:

- payout есть, а соответствующего symbol в `Symbols:` нет;
- файл сломан (неверная структура или формат строк);
- остались маркеры конфликта после merge.

## Запуск проверки

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -v
```

Успешный прогон — **green build**. Падение теста с перечислением ошибок — **red build**; исправьте `slot-machine.txt` и запустите снова.

## Роли в воркшопе

- **Человек A** — секция `Symbols:`
- **Человек B** — секция `Payouts:`

В раунде с CI после каждого изменения: sync → merge → `pytest`. Сначала добавляют symbol, затем payout — так сборка остаётся зелёной.
