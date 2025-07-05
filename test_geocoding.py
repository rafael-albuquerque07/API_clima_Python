"""
Testes para o serviço de geocodificação
"""
import pytest
from unittest.mock import patch, Mock
from src.models.geocoding import GeocodingService, Location


class TestGeocodingService:
    """Testes para a classe GeocodingService"""
    
    def test_location_to_dict(self):
        """Testa conversão de Location para dicionário"""
        location = Location(
            name="São Paulo, SP",
            latitude=-23.5505,
            longitude=-46.6333,
            country="Brasil",
            state="SP"
        )
        
        result = location.to_dict()
        
        assert result['name'] == "São Paulo, SP"
        assert result['lat'] == -23.5505
        assert result['lon'] == -46.6333
        assert result['country'] == "Brasil"
        assert result['state'] == "SP"
    
    def test_search_brazilian_cities_exact_match(self):
        """Testa busca exata por cidades brasileiras"""
        results = GeocodingService.search_locations("são paulo")
        
        assert len(results) >= 1
        assert results[0].name == "São Paulo, SP"
        assert results[0].latitude == -23.5505
        assert results[0].longitude == -46.6333
    
    def test_search_brazilian_cities_partial_match(self):
        """Testa busca parcial por cidades brasileiras"""
        results = GeocodingService.search_locations("rio")
        
        assert len(results) >= 1
        # Deve encontrar Rio de Janeiro
        rio_found = any("Rio de Janeiro" in result.name for result in results)
        assert rio_found
    
    def test_search_brazilian_cities_case_insensitive(self):
        """Testa busca case-insensitive"""
        results_lower = GeocodingService.search_locations("são paulo")
        results_upper = GeocodingService.search_locations("SÃO PAULO")
        results_mixed = GeocodingService.search_locations("São Paulo")
        
        assert len(results_lower) >= 1
        assert len(results_upper) >= 1
        assert len(results_mixed) >= 1
        
        # Todos devem retornar o mesmo resultado
        assert results_lower[0].name == results_upper[0].name == results_mixed[0].name
    
    def test_search_limit_parameter(self):
        """Testa parâmetro de limite de resultados"""
        results_3 = GeocodingService.search_locations("são", limit=3)
        results_1 = GeocodingService.search_locations("são", limit=1)
        
        assert len(results_3) <= 3
        assert len(results_1) <= 1
    
    def test_search_empty_query(self):
        """Testa busca com query vazia"""
        results = GeocodingService.search_locations("")
        
        assert len(results) == 0
    
    def test_search_nonexistent_city(self):
        """Testa busca por cidade inexistente"""
        results = GeocodingService.search_locations("CidadeQueNaoExiste123")
        
        # Pode retornar lista vazia ou tentar busca online
        assert isinstance(results, list)
    
    @patch('src.models.geocoding.requests.get')
    def test_search_nominatim_success(self, mock_get):
        """Testa busca online via Nominatim com sucesso"""
        # Mock da resposta do Nominatim
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'lat': '-23.5505',
                'lon': '-46.6333',
                'display_name': 'São Paulo, São Paulo, Brasil',
                'address': {
                    'city': 'São Paulo',
                    'state': 'São Paulo',
                    'country': 'Brasil'
                }
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Testar método privado diretamente
        results = GeocodingService._search_nominatim("São Paulo")
        
        assert len(results) == 1
        assert results[0].name == "São Paulo, São Paulo"
        assert results[0].latitude == -23.5505
        assert results[0].longitude == -46.6333
    
    @patch('src.models.geocoding.requests.get')
    def test_search_nominatim_error(self, mock_get):
        """Testa tratamento de erro na busca online"""
        # Mock de erro na requisição
        mock_get.side_effect = Exception("Erro de conexão")
        
        # Testar método privado diretamente
        results = GeocodingService._search_nominatim("São Paulo")
        
        assert results == []
    
    @patch('src.models.geocoding.requests.get')
    def test_reverse_geocode_success(self, mock_get):
        """Testa geocodificação reversa com sucesso"""
        # Mock da resposta do Nominatim
        mock_response = Mock()
        mock_response.json.return_value = {
            'display_name': 'São Paulo, São Paulo, Brasil',
            'address': {
                'city': 'São Paulo',
                'state': 'São Paulo',
                'country': 'Brasil'
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Executar teste
        result = GeocodingService.get_location_by_coordinates(-23.5505, -46.6333)
        
        # Verificações
        assert result is not None
        assert isinstance(result, Location)
        assert result.latitude == -23.5505
        assert result.longitude == -46.6333
        assert "São Paulo" in result.name
    
    @patch('src.models.geocoding.requests.get')
    def test_reverse_geocode_error(self, mock_get):
        """Testa tratamento de erro na geocodificação reversa"""
        # Mock de erro na requisição
        mock_get.side_effect = Exception("Erro de conexão")
        
        # Executar teste
        result = GeocodingService.get_location_by_coordinates(-23.5505, -46.6333)
        
        # Verificações
        assert result is None
    
    @patch('src.models.geocoding.requests.get')
    def test_reverse_geocode_api_error_response(self, mock_get):
        """Testa resposta de erro da API na geocodificação reversa"""
        # Mock da resposta com erro
        mock_response = Mock()
        mock_response.json.return_value = {'error': 'Localização não encontrada'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Executar teste
        result = GeocodingService.get_location_by_coordinates(-23.5505, -46.6333)
        
        # Verificações
        assert result is None

