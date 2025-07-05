"""
Testes unitários para o serviço meteorológico
"""
import pytest
from unittest.mock import patch, Mock
from src.models.weather import WeatherService, WeatherData, ForecastData
from datetime import datetime


class TestWeatherService:
    """Testes para a classe WeatherService"""
    
    def test_weather_codes_mapping(self):
        """Testa se os códigos de tempo estão mapeados corretamente"""
        assert WeatherService.WEATHER_CODES[0] == "Céu limpo"
        assert WeatherService.WEATHER_CODES[61] == "Chuva leve"
        assert WeatherService.WEATHER_CODES[95] == "Tempestade"
    
    @patch('src.models.weather.requests.get')
    def test_get_current_weather_success(self, mock_get):
        """Testa obtenção bem-sucedida de dados meteorológicos atuais"""
        # Mock da resposta da API
        mock_response = Mock()
        mock_response.json.return_value = {
            'current': {
                'time': '2025-07-04T20:00:00',
                'temperature_2m': 25.5,
                'relative_humidity_2m': 65,
                'wind_speed_10m': 10.2,
                'wind_direction_10m': 180,
                'weather_code': 1
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Executar teste
        result = WeatherService.get_current_weather(-23.5505, -46.6333, "São Paulo")
        
        # Verificações
        assert result is not None
        assert isinstance(result, WeatherData)
        assert result.temperature == 25.5
        assert result.humidity == 65
        assert result.wind_speed == 10.2
        assert result.wind_direction == 180
        assert result.weather_code == 1
        assert result.location == "São Paulo"
        assert result.description == "Principalmente limpo"
    
    @patch('src.models.weather.requests.get')
    def test_get_current_weather_api_error(self, mock_get):
        """Testa tratamento de erro da API"""
        # Mock de erro na requisição
        mock_get.side_effect = Exception("Erro de conexão")
        
        # Executar teste
        result = WeatherService.get_current_weather(-23.5505, -46.6333, "São Paulo")
        
        # Verificações
        assert result is None
    
    @patch('src.models.weather.requests.get')
    def test_get_forecast_success(self, mock_get):
        """Testa obtenção bem-sucedida de previsão meteorológica"""
        # Mock da resposta da API
        mock_response = Mock()
        mock_response.json.return_value = {
            'daily': {
                'time': ['2025-07-04', '2025-07-05'],
                'temperature_2m_max': [28.0, 30.0],
                'temperature_2m_min': [18.0, 20.0],
                'weather_code': [1, 2],
                'precipitation_sum': [0.0, 2.5]
            },
            'hourly': {
                'time': ['2025-07-04T20:00', '2025-07-04T21:00'],
                'temperature_2m': [25.0, 24.0],
                'relative_humidity_2m': [65, 70],
                'wind_speed_10m': [10.0, 8.0],
                'weather_code': [1, 1]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Executar teste
        result = WeatherService.get_forecast(-23.5505, -46.6333, "São Paulo", 2)
        
        # Verificações
        assert result is not None
        assert isinstance(result, ForecastData)
        assert len(result.daily_forecast) == 2
        assert len(result.hourly_forecast) == 2
        assert result.daily_forecast[0]['temperature_max'] == 28.0
        assert result.daily_forecast[0]['temperature_min'] == 18.0
        assert result.hourly_forecast[0]['temperature'] == 25.0
    
    def test_weather_data_to_dict(self):
        """Testa conversão de WeatherData para dicionário"""
        weather_data = WeatherData(
            location="São Paulo",
            latitude=-23.5505,
            longitude=-46.6333,
            temperature=25.0,
            humidity=65,
            wind_speed=10.0,
            wind_direction=180,
            weather_code=1,
            timestamp=datetime(2025, 7, 4, 20, 0, 0),
            description="Principalmente limpo"
        )
        
        result = weather_data.to_dict()
        
        assert result['location'] == "São Paulo"
        assert result['temperature'] == 25.0
        assert result['humidity'] == 65
        assert result['description'] == "Principalmente limpo"
        assert 'timestamp' in result
    
    def test_forecast_data_to_dict(self):
        """Testa conversão de ForecastData para dicionário"""
        forecast_data = ForecastData(
            location="São Paulo",
            latitude=-23.5505,
            longitude=-46.6333,
            daily_forecast=[
                {
                    'date': '2025-07-04',
                    'temperature_max': 28.0,
                    'temperature_min': 18.0,
                    'weather_code': 1,
                    'precipitation': 0.0,
                    'description': 'Principalmente limpo'
                }
            ],
            hourly_forecast=[
                {
                    'time': '2025-07-04T20:00',
                    'temperature': 25.0,
                    'humidity': 65,
                    'wind_speed': 10.0,
                    'weather_code': 1,
                    'description': 'Principalmente limpo'
                }
            ]
        )
        
        result = forecast_data.to_dict()
        
        assert result['location'] == "São Paulo"
        assert len(result['daily_forecast']) == 1
        assert len(result['hourly_forecast']) == 1
        assert result['daily_forecast'][0]['temperature_max'] == 28.0

