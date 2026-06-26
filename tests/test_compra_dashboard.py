from unittest.mock import Mock

from app.app import App


class DummyVendaDAO:
    def vender(self, isbn, quantidade):
        return {
            "titulo": "Livro Teste",
            "quantidade": quantidade,
            "valor_total": quantidade * 15.0,
        }


def test_registrar_venda_atualiza_dashboard():
    app = App.__new__(App)
    app.venda_dao = DummyVendaDAO()
    app.dashboard = Mock()

    venda = app.registrar_venda("123", 2)

    assert venda["quantidade"] == 2
    assert venda["valor_total"] == 30.0
    app.dashboard.assert_called_once()
