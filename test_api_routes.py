"""
Testes de integração para as rotas da API
"""
import pytest
import json
from unittest.mock import patch, Mock


class TestWeatherAPIRoutes:
    """Testes para as rotas da API meteorológica"""
    
    def test_health_check(self, client):
        """Testa endpoint de verificação de saúde"""
        response = client.get('/api/weather/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
    
    @patch('src.models.weather.WeatherService.get_current_weather')
    def test_current_weather_success(self, mock_weather, client):
        """Testa endpoint de dados meteorológicos atuais com sucesso"""
        # Mock do serviço meteorológico
        mock_weather_data = Mock()
        mock_weather_data.to_dict.return_value = {
            'location': 'São Paulo',
            'temperature': 25.0,
            'humidity': 65,
            'wind_speed': 10.0,
            'description': 'Principalmente limpo'
        }
        mock_weather.return_value = mock_weather_data
        
        # Fazer requisição
        response = client.get('/api/weather/current?lat=-23.5505&lon=-46.6333&location=São Paulo')
        
        # Verificações
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['location'] == 'São Paulo'
        assert data['data']['temperature'] == 25.0
    
    def test_current_weather_missing_params(self, client):
        """Testa endpoint de dados atuais com parâmetros faltando"""
        response = client.get('/api/weather/current')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_current_weather_invalid_coords(self, client):
        """Testa endpoint de dados atuais com coordenadas inválidas"""
        response = client.get('/api/weather/current?lat=invalid&lon=-46.6333')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    @patch('src.models.weather.WeatherService.get_current_weather')
    def test_current_weather_service_error(self, mock_weather, client):
        """Testa endpoint de dados atuais com erro no serviço"""
        # Mock retornando None (erro)
        mock_weather.return_value = None
        
        # Fazer requisição
        response = client.get('/api/weather/current?lat=-23.5505&lon=-46.6333')
        
        # Verificações
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'error' in data
    
    @patch('src.models.weather.WeatherService.get_forecast')
    def test_forecast_success(self, mock_forecast, client):
        """Testa endpoint de previsão com sucesso"""
        # Mock do serviço de previsão
        mock_forecast_data = Mock()
        mock_forecast_data.to_dict.return_value = {
            'location': 'São Paulo',
            'daily_forecast': [
                {
                    'date': '2025-07-04',
                    'temperature_max': 28.0,
                    'temperature_min': 18.0,
                    'description': 'Principalmente limpo'
                }
            ],
            'hourly_forecast': []
        }
        mock_forecast.return_value = mock_forecast_data
        
        # Fazer requisição
        response = client.get('/api/weather/forecast?lat=-23.5505&lon=-46.6333&days=3')
        
        # Verificações
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['location'] == 'São Paulo'
        assert len(data['data']['daily_forecast']) == 1
    
    def test_forecast_invalid_days(self, client):
        """Testa endpoint de previsão com número de dias inválido"""
        response = client.get('/api/weather/forecast?lat=-23.5505&lon=-46.6333&days=20')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    @patch('src.models.geocoding.GeocodingService.search_locations')
    def test_search_location_success(self, mock_search, client):
        """Testa endpoint de busca de localização com sucesso"""
        # Mock do serviço de geocodificação
        mock_location = Mock()
        mock_location.to_dict.return_value = {
            'name': 'São Paulo, SP',
            'lat': -23.5505,
            'lon': -46.6333,
            'country': 'Brasil',
            'state': 'SP'
        }
        mock_search.return_value = [mock_location]
        
        # Fazer requisição
        response = client.get('/api/weather/search?q=São Paulo')
        
        # Verificações
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['count'] == 1
        assert data['data'][0]['name'] == 'São Paulo, SP'
    
    def test_search_location_missing_query(self, client):
        """Testa endpoint de busca sem query"""
        response = client.get('/api/weather/search')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    @patch('src.models.geocoding.GeocodingService.search_locations')
    def test_search_location_not_found(self, mock_search, client):
        """Testa endpoint de busca sem resultados"""
        # Mock retornando lista vazia
        mock_search.return_value = []
        
        # Fazer requisição
        response = client.get('/api/weather/search?q=CidadeInexistente')
        
        # Verificações
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    @patch('src.models.geocoding.GeocodingService.get_location_by_coordinates')
    def test_reverse_geocode_success(self, mock_reverse, client):
        """Testa endpoint de geocodificação reversa com sucesso"""
        # Mock do serviço de geocodificação reversa
        mock_location = Mock()
        mock_location.to_dict.return_value = {
            'name': 'São Paulo, SP',
            'lat': -23.5505,
            'lon': -46.6333,
            'country': 'Brasil',
            'state': 'SP'
        }
        mock_reverse.return_value = mock_location
        
        # Fazer requisição
        response = client.get('/api/weather/reverse-geocode?lat=-23.5505&lon=-46.6333')
        
        # Verificações
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['name'] == 'São Paulo, SP'
    
    def test_reverse_geocode_missing_params(self, client):
        """Testa geocodificação reversa com parâmetros faltando"""
        response = client.get('/api/weather/reverse-geocode?lat=-23.5505')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_reverse_geocode_invalid_coords(self, client):
        """Testa geocodificação reversa com coordenadas inválidas"""
        response = client.get('/api/weather/reverse-geocode?lat=100&lon=-46.6333')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data


class TestStaticRoutes:
    """Testes para rotas estáticas"""
    
    def test_index_page(self, client):
        """Testa se a página inicial carrega"""
        response = client.get('/')
        
        assert response.status_code == 200
        assert b'Aplicativo do Tempo com IA' in response.data
    
    def test_css_file(self, client):
        """Testa se o arquivo CSS carrega"""
        response = client.get('/styles.css')
        
        assert response.status_code == 200
        assert response.content_type == 'text/css; charset=utf-8'
    
    def test_js_file(self, client):
        """Testa se o arquivo JavaScript carrega"""
        response = client.get('/script.js')
        
        assert response.status_code == 200
        assert response.content_type == 'application/javascript; charset=utf-8'

