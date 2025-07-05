"""
Modelo para dados meteorológicos
"""
from datetime import datetime
from typing import Dict, List, Optional
import requests
from dataclasses import dataclass
from flask import Blueprint, jsonify, request


@dataclass
class WeatherData:
    """Classe para representar dados meteorológicos"""
    location: str
    latitude: float
    longitude: float
    temperature: float
    humidity: float
    wind_speed: float
    wind_direction: float
    weather_code: int
    timestamp: datetime
    description: str = ""
    
    def to_dict(self) -> Dict:
        """Converte os dados para dicionário"""
        return {
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'wind_speed': self.wind_speed,
            'wind_direction': self.wind_direction,
            'weather_code': self.weather_code,
            'timestamp': self.timestamp.isoformat(),
            'description': self.description
        }


@dataclass
class ForecastData:
    """Classe para representar previsão meteorológica"""
    location: str
    latitude: float
    longitude: float
    daily_forecast: List[Dict]
    hourly_forecast: List[Dict]
    
    def to_dict(self) -> Dict:
        """Converte os dados para dicionário"""
        return {
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'daily_forecast': self.daily_forecast,
            'hourly_forecast': self.hourly_forecast
        }


class WeatherService:
    """Serviço para obter dados meteorológicos da Open-Meteo API"""
    
    BASE_URL = "https://api.open-meteo.com/v1"
    
    # Códigos de tempo WMO para descrições
    WEATHER_CODES = {
        0: "Céu limpo",
        1: "Principalmente limpo",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Neblina",
        48: "Neblina com geada",
        51: "Garoa leve",
        53: "Garoa moderada",
        55: "Garoa intensa",
        56: "Garoa gelada leve",
        57: "Garoa gelada intensa",
        61: "Chuva leve",
        63: "Chuva moderada",
        65: "Chuva intensa",
        66: "Chuva gelada leve",
        67: "Chuva gelada intensa",
        71: "Neve leve",
        73: "Neve moderada",
        75: "Neve intensa",
        77: "Granizo",
        80: "Pancadas de chuva leves",
        81: "Pancadas de chuva moderadas",
        82: "Pancadas de chuva intensas",
        85: "Pancadas de neve leves",
        86: "Pancadas de neve intensas",
        95: "Tempestade",
        96: "Tempestade com granizo leve",
        99: "Tempestade com granizo intenso"
    }
    
    @classmethod
    def get_current_weather(cls, latitude: float, longitude: float, location: str = "") -> Optional[WeatherData]:
        """
        Obtém dados meteorológicos atuais para uma localização
        
        Args:
            latitude: Latitude da localização
            longitude: Longitude da localização
            location: Nome da localização (opcional)
            
        Returns:
            WeatherData ou None em caso de erro
        """
        try:
            url = f"{cls.BASE_URL}/forecast"
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'current': 'temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,weather_code',
                'timezone': 'auto'
            }
            
            print(f"Fazendo requisição para: {url}")
            print(f"Parâmetros: {params}")
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            print(f"Resposta da API: {data}")
            current = data.get('current', {})
            
            if not current:
                print("ERRO: 'current' não encontrado na resposta da API")
                return None
            
            weather_data = WeatherData(
                location=location or f"{latitude}, {longitude}",
                latitude=latitude,
                longitude=longitude,
                temperature=current.get('temperature_2m', 0),
                humidity=current.get('relative_humidity_2m', 0),
                wind_speed=current.get('wind_speed_10m', 0),
                wind_direction=current.get('wind_direction_10m', 0),
                weather_code=current.get('weather_code', 0),
                timestamp=datetime.fromisoformat(current['time']) if current.get('time') else datetime.now(),
                description=cls.WEATHER_CODES.get(current.get('weather_code', 0), "Desconhecido")
            )
            
            print(f"WeatherData criado: {weather_data.to_dict()}")
            return weather_data
            
        except requests.RequestException as e:
            print(f"Erro na requisição da API: {e}")
            return None
        except KeyError as e:
            print(f"Erro ao processar dados da API: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return None
    
    @classmethod
    def get_forecast(cls, latitude: float, longitude: float, location: str = "", days: int = 7) -> Optional[ForecastData]:
        """
        Obtém previsão meteorológica para uma localização
        
        Args:
            latitude: Latitude da localização
            longitude: Longitude da localização
            location: Nome da localização (opcional)
            days: Número de dias de previsão (padrão: 7)
            
        Returns:
            ForecastData ou None em caso de erro
        """
        try:
            url = f"{cls.BASE_URL}/forecast"
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'daily': 'temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum',
                'hourly': 'temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code',
                'timezone': 'auto',
                'forecast_days': days
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Processar previsão diária
            daily_data = data['daily']
            daily_forecast = []
            for i in range(len(daily_data['time'])):
                daily_forecast.append({
                    'date': daily_data['time'][i],
                    'temperature_max': daily_data['temperature_2m_max'][i],
                    'temperature_min': daily_data['temperature_2m_min'][i],
                    'weather_code': daily_data['weather_code'][i],
                    'precipitation': daily_data['precipitation_sum'][i],
                    'description': cls.WEATHER_CODES.get(daily_data['weather_code'][i], "Desconhecido")
                })
            
            # Processar previsão horária (próximas 24 horas)
            hourly_data = data['hourly']
            hourly_forecast = []
            for i in range(min(24, len(hourly_data['time']))):
                hourly_forecast.append({
                    'time': hourly_data['time'][i],
                    'temperature': hourly_data['temperature_2m'][i],
                    'humidity': hourly_data['relative_humidity_2m'][i],
                    'wind_speed': hourly_data['wind_speed_10m'][i],
                    'weather_code': hourly_data['weather_code'][i],
                    'description': cls.WEATHER_CODES.get(hourly_data['weather_code'][i], "Desconhecido")
                })
            
            forecast_data = ForecastData(
                location=location or f"{latitude}, {longitude}",
                latitude=latitude,
                longitude=longitude,
                daily_forecast=daily_forecast,
                hourly_forecast=hourly_forecast
            )
            
            return forecast_data
            
        except requests.RequestException as e:
            print(f"Erro na requisição da API: {e}")
            return None
        except KeyError as e:
            print(f"Erro ao processar dados da API: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return None


# Blueprint para as rotas da API de clima
weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/current')
def get_current_weather():
    """Endpoint para obter clima atual"""
    try:
        # Obter parâmetros da requisição
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        location = request.args.get('location', '')
        
        print(f"Recebida requisição: lat={lat}, lon={lon}, location={location}")
        
        if lat is None or lon is None:
            return jsonify({'error': 'Parâmetros lat e lon são obrigatórios'}), 400
        
        # Usar o WeatherService para obter dados
        weather_data = WeatherService.get_current_weather(lat, lon, location)
        
        if weather_data is None:
            print("ERRO: WeatherService retornou None")
            return jsonify({'error': 'Erro ao obter dados meteorológicos'}), 500
        
        result = weather_data.to_dict()
        print(f"Retornando dados: {result}")
        return jsonify({'data': result})  # CORRIGIDO: envolver em 'data'
        
    except Exception as e:
        print(f"ERRO na rota /current: {str(e)}")
        return jsonify({'error': str(e)}), 500

@weather_bp.route('/forecast')
def get_forecast():
    """Endpoint para obter previsão do tempo"""
    try:
        # Obter parâmetros da requisição
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        location = request.args.get('location', '')
        days = request.args.get('days', default=7, type=int)
        
        if lat is None or lon is None:
            return jsonify({'error': 'Parâmetros lat e lon são obrigatórios'}), 400
        
        # Usar o WeatherService para obter previsão
        forecast_data = WeatherService.get_forecast(lat, lon, location, days)
        
        if forecast_data is None:
            return jsonify({'error': 'Erro ao obter previsão meteorológica'}), 500
        
        result = forecast_data.to_dict()
        return jsonify({'data': result})  # CORRIGIDO: envolver em 'data'
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@weather_bp.route('/test')
def test():
    """Endpoint de teste"""
    return jsonify({'message': 'Weather API funcionando!', 'status': 'OK'})

@weather_bp.route('/search')
def search_cities():
    """Endpoint para buscar cidades"""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({'error': 'Parâmetro q (query) é obrigatório'}), 400
        
        # Usar API de geocoding do Open-Meteo
        geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            'name': query,
            'count': 10,
            'language': 'pt',
            'format': 'json'
        }
        
        print(f"Buscando cidades: {query}")
        
        response = requests.get(geocoding_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Processar resultados
        cities = []
        if 'results' in data:
            for result in data['results']:
                city = {
                    'name': result.get('name', ''),
                    'lat': result.get('latitude', 0),
                    'lon': result.get('longitude', 0),
                    'country': result.get('country', ''),
                    'admin1': result.get('admin1', ''),  # Estado/província
                }
                
                # Criar nome completo da cidade
                name_parts = [city['name']]
                if city['admin1']:
                    name_parts.append(city['admin1'])
                if city['country']:
                    name_parts.append(city['country'])
                
                city['name'] = ', '.join(name_parts)
                cities.append(city)
        
        print(f"Encontradas {len(cities)} cidades")
        return jsonify({'data': cities})
        
    except requests.RequestException as e:
        print(f"Erro na requisição de geocoding: {e}")
        return jsonify({'error': 'Erro ao buscar cidades'}), 500
    except Exception as e:
        print(f"ERRO na rota /search: {str(e)}")
        return jsonify({'error': str(e)}), 500