"""Testes adicionais: defeitos encontrados durante a revisão."""

from helpers import run_cli


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
