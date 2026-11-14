"""Testes adicionais: defeitos encontrados durante a revisão."""

from decimal import Decimal

import pytest
from helpers import run_cli

from onfly_report.exceptions import InputFileError
from onfly_report.services.currency_converter import convert_to_brl


def test_all_reservations_are_read_from_large_file(tmp_path):
    """O relatório considera todas as linhas, sem truncar a entrada."""
    rows = [{"reservation_id": f"R-{index:03d}"} for index in range(205)]

    report = run_cli(tmp_path, rows)

    assert report["summary"]["total_reservations"] == 205
    assert report["summary"]["confirmed_reservations"] == 205
    assert report["summary"]["total_room_nights"] == 205
    assert report["summary"]["total_amount_brl"] == "20500.00"


def test_top_hotels_ties_are_broken_by_hotel_id_ascending(tmp_path):
    """Empate no total usa hotel_id ascendente, mesmo com o ranking decrescente."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H02", "hotel_name": "Hotel B", "amount": "100.00"},
            {"reservation_id": "R-2", "hotel_id": "H01", "hotel_name": "Hotel A", "amount": "100.00"},
        ],
    )

    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H01", "H02"]


def test_currency_is_case_insensitive(tmp_path):
    """A moeda é normalizada antes da consulta à tabela de câmbio."""
    report = run_cli(
        tmp_path,
        [{"reservation_id": "R-1", "currency": "usd", "amount": "100.00"}],
    )

    assert report["summary"]["total_amount_brl"] == "542.00"


def test_missing_rate_is_an_input_error():
    """Moeda sem taxa é entrada inválida, não erro inesperado."""
    with pytest.raises(InputFileError):
        convert_to_brl(Decimal("10.00"), "GBP", {"BRL": Decimal("1.000000")})
