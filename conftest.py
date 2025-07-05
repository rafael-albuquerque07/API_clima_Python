"""
Configuração do pytest para testes do aplicativo do tempo
"""
import pytest
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app


@pytest.fixture
def client():
    """Fixture para cliente de teste do Flask"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def app_context():
    """Fixture para contexto da aplicação"""
    with app.app_context():
        yield app

