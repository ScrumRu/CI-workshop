"""Проверка slot-machine.txt на green/red build (правила в RULES.md / README)."""

import re
from pathlib import Path

SLOT_MACHINE_FILE = Path(__file__).parent / "slot-machine.txt"

MERGE_CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")

PAYOUT_LINE_RE = (
    r"^-\s+(\w+)\s+\1\s+\1\s+=\s+(x\d+|JACKPOT)$"
)


def validate_slot_machine(content: str) -> list[str]:
    """Возвращает список ошибок. Пустой список = green build."""
    errors: list[str] = []
    lines = content.splitlines()

    for marker in MERGE_CONFLICT_MARKERS:
        if any(marker in line for line in lines):
            errors.append(f"найден маркер merge conflict: {marker}")
            return errors

    if not lines or lines[0].strip() != "SLOT GAME":
        errors.append('первая строка должна быть "SLOT GAME"')
        return errors

    try:
        symbols_idx = next(
            i for i, line in enumerate(lines) if line.strip() == "Symbols:"
        )
        payouts_idx = next(
            i for i, line in enumerate(lines) if line.strip() == "Payouts:"
        )
    except StopIteration:
        errors.append("отсутствует секция Symbols: или Payouts:")
        return errors

    if symbols_idx >= payouts_idx:
        errors.append("секция Symbols: должна идти перед Payouts:")
        return errors

    symbols: list[str] = []
    for line in lines[symbols_idx + 1 : payouts_idx]:
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.startswith("- "):
            errors.append(f"неверная строка в Symbols: {line!r}")
            continue
        symbol = stripped[2:].strip()
        if not symbol or " " in symbol:
            errors.append(f"неверный symbol: {line!r}")
            continue
        if symbol in symbols:
            errors.append(f"дубликат symbol: {symbol}")
        symbols.append(symbol)

    if not symbols:
        errors.append("секция Symbols: пуста")

    payout_pattern = re.compile(PAYOUT_LINE_RE)
    payout_symbols: list[str] = []

    for line in lines[payouts_idx + 1 :]:
        stripped = line.strip()
        if not stripped:
            continue
        if not payout_pattern.match(stripped):
            errors.append(f"неверная строка payout: {line!r}")
            continue
        symbol = stripped.split()[1]
        payout_symbols.append(symbol)

    if not payout_symbols and not errors:
        errors.append("секция Payouts: пуста")

    symbol_set = set(symbols)
    payout_set = set(payout_symbols)

    for symbol in symbol_set:
        if symbol not in payout_set:
            errors.append(f"symbol {symbol!r} не описан в payouts")

    for symbol in payout_set:
        if symbol not in symbol_set:
            errors.append(f"payout для {symbol!r}, но symbol отсутствует в Symbols")

    return errors


def test_slot_machine_is_green_build():
    """Читает slot-machine.txt и проверяет green build."""
    assert SLOT_MACHINE_FILE.is_file(), f"файл не найден: {SLOT_MACHINE_FILE}"

    content = SLOT_MACHINE_FILE.read_text(encoding="utf-8")
    errors = validate_slot_machine(content)

    assert not errors, "red build:\n" + "\n".join(f"  - {e}" for e in errors)
