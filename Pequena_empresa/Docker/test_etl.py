from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from incremental_carga import (
    _log,
    _resultado_para_dataframe,
    executar_etl,
    obter_engine,
)


def test_obter_engine():
    with patch("incremental_carga.create_engine") as mock_create:
        obter_engine()
        mock_create.assert_called_once()
        args, kwargs = mock_create.call_args
        assert "sslmode=require" in args[0]
        assert "postgresql+psycopg2://" in args[0]


def test_resultado_para_dataframe():
    # Mocking a SQLAlchemy result object
    mock_result = MagicMock()
    mock_result.keys.return_value = ["id", "nome", "status"]
    mock_result.fetchall.return_value = [
        (1, "Teste 1", "Ativo"),
        (2, "Teste 2", "Inativo"),
    ]

    df = _resultado_para_dataframe(mock_result)

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["id", "nome", "status"]
    assert len(df) == 2
    assert df.loc[0, "nome"] == "Teste 1"


def test_log_with_context():
    mock_context = MagicMock()
    _log(mock_context, "Mensagem de teste")
    mock_context.log.info.assert_called_once_with("Mensagem de teste")


def test_log_without_context(capsys):
    _log(None, "Mensagem de teste sem contexto")
    captured = capsys.readouterr()
    assert "Mensagem de teste sem contexto" in captured.out


def test_executar_etl_connection_failure():
    # Mocking obter_engine to raise a database connection exception on begin
    mock_engine = MagicMock()
    mock_engine.begin.side_effect = Exception("Banco inacessível")

    with (
        patch("incremental_carga.obter_engine", return_value=mock_engine),
        patch("incremental_carga._log") as mock_log,
        pytest.raises(Exception, match="Banco inacessível"),
    ):
        executar_etl()

    # Verify that we logged our user-friendly error tips
    called_messages = [call[0][1] for call in mock_log.call_args_list]
    assert any(
        "❌ Erro ao conectar ao banco de dados" in msg for msg in called_messages
    )
    assert any("💡 DICA DE SOLUÇÃO" in msg for msg in called_messages)
