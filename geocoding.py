"""
Serviço de geocodificação para busca de cidades
"""
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Location:
    """Classe para representar uma localização"""
    name: str
    latitude: float
    longitude: float
    country: str = ""
    state: str = ""
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'name': self.name,
            'lat': self.latitude,
            'lon': self.longitude,
            'country': self.country,
            'state': self.state
        }


class GeocodingService:
    """Serviço de geocodificação usando APIs gratuitas"""
    
    # Cidades brasileiras pré-definidas para fallback
    BRAZILIAN_CITIES = {
        'são paulo': Location('São Paulo, SP', -23.5505, -46.6333, 'Brasil', 'SP'),
        'rio de janeiro': Location('Rio de Janeiro, RJ', -22.9068, -43.1729, 'Brasil', 'RJ'),
        'brasília': Location('Brasília, DF', -15.7942, -47.8822, 'Brasil', 'DF'),
        'salvador': Location('Salvador, BA', -12.9714, -38.5014, 'Brasil', 'BA'),
        'fortaleza': Location('Fortaleza, CE', -3.7319, -38.5267, 'Brasil', 'CE'),
        'belo horizonte': Location('Belo Horizonte, MG', -19.9191, -43.9386, 'Brasil', 'MG'),
        'manaus': Location('Manaus, AM', -3.1190, -60.0217, 'Brasil', 'AM'),
        'curitiba': Location('Curitiba, PR', -25.4284, -49.2733, 'Brasil', 'PR'),
        'recife': Location('Recife, PE', -8.0476, -34.8770, 'Brasil', 'PE'),
        'porto alegre': Location('Porto Alegre, RS', -30.0346, -51.2177, 'Brasil', 'RS'),
        'goiânia': Location('Goiânia, GO', -16.6869, -49.2648, 'Brasil', 'GO'),
        'belém': Location('Belém, PA', -1.4558, -48.5044, 'Brasil', 'PA'),
        'guarulhos': Location('Guarulhos, SP', -23.4538, -46.5333, 'Brasil', 'SP'),
        'campinas': Location('Campinas, SP', -22.9056, -47.0608, 'Brasil', 'SP'),
        'são luís': Location('São Luís, MA', -2.5307, -44.3068, 'Brasil', 'MA'),
        'são gonçalo': Location('São Gonçalo, RJ', -22.8267, -43.0537, 'Brasil', 'RJ'),
        'maceió': Location('Maceió, AL', -9.6658, -35.7353, 'Brasil', 'AL'),
        'duque de caxias': Location('Duque de Caxias, RJ', -22.7856, -43.3117, 'Brasil', 'RJ'),
        'teresina': Location('Teresina, PI', -5.0892, -42.8019, 'Brasil', 'PI'),
        'natal': Location('Natal, RN', -5.7945, -35.2110, 'Brasil', 'RN'),
        'campo grande': Location('Campo Grande, MS', -20.4697, -54.6201, 'Brasil', 'MS'),
        'nova iguaçu': Location('Nova Iguaçu, RJ', -22.7592, -43.4511, 'Brasil', 'RJ'),
        'são bernardo do campo': Location('São Bernardo do Campo, SP', -23.6914, -46.5646, 'Brasil', 'SP'),
        'joão pessoa': Location('João Pessoa, PB', -7.1195, -34.8450, 'Brasil', 'PB'),
        'santo andré': Location('Santo André, SP', -23.6633, -46.5307, 'Brasil', 'SP'),
        'osasco': Location('Osasco, SP', -23.5329, -46.7918, 'Brasil', 'SP'),
        'jaboatão dos guararapes': Location('Jaboatão dos Guararapes, PE', -8.1130, -35.0147, 'Brasil', 'PE'),
        'contagem': Location('Contagem, MG', -19.9317, -44.0536, 'Brasil', 'MG'),
        'são josé dos campos': Location('São José dos Campos, SP', -23.2237, -45.9009, 'Brasil', 'SP'),
        'uberlândia': Location('Uberlândia, MG', -18.9113, -48.2622, 'Brasil', 'MG'),
        'sorocaba': Location('Sorocaba, SP', -23.5015, -47.4526, 'Brasil', 'SP'),
        'cuiabá': Location('Cuiabá, MT', -15.6014, -56.0979, 'Brasil', 'MT'),
        'aracaju': Location('Aracaju, SE', -10.9472, -37.0731, 'Brasil', 'SE'),
        'feira de santana': Location('Feira de Santana, BA', -12.2664, -38.9663, 'Brasil', 'BA'),
        'joinville': Location('Joinville, SC', -26.3044, -48.8487, 'Brasil', 'SC'),
        'ribeirão preto': Location('Ribeirão Preto, SP', -21.1775, -47.8208, 'Brasil', 'SP'),
        'juiz de fora': Location('Juiz de Fora, MG', -21.7642, -43.3467, 'Brasil', 'MG'),
        'londrina': Location('Londrina, PR', -23.3045, -51.1696, 'Brasil', 'PR'),
        'aparecida de goiânia': Location('Aparecida de Goiânia, GO', -16.8173, -49.2437, 'Brasil', 'GO'),
        'niterói': Location('Niterói, RJ', -22.8833, -43.1036, 'Brasil', 'RJ'),
        'porto velho': Location('Porto Velho, RO', -8.7612, -63.9004, 'Brasil', 'RO'),
        'florianópolis': Location('Florianópolis, SC', -27.5954, -48.5480, 'Brasil', 'SC'),
        'serra': Location('Serra, ES', -20.1288, -40.3075, 'Brasil', 'ES'),
        'betim': Location('Betim, MG', -19.9681, -44.1987, 'Brasil', 'MG'),
        'diadema': Location('Diadema, SP', -23.6861, -46.6228, 'Brasil', 'SP'),
        'maringá': Location('Maringá, PR', -23.4205, -51.9331, 'Brasil', 'PR'),
        'ananindeua': Location('Ananindeua, PA', -1.3656, -48.3722, 'Brasil', 'PA'),
        'campos dos goytacazes': Location('Campos dos Goytacazes, RJ', -21.7520, -41.3297, 'Brasil', 'RJ'),
        'vila velha': Location('Vila Velha, ES', -20.3297, -40.2925, 'Brasil', 'ES'),
        'mauá': Location('Mauá, SP', -23.6678, -46.4611, 'Brasil', 'SP'),
        'são josé do rio preto': Location('São José do Rio Preto, SP', -20.8197, -49.3794, 'Brasil', 'SP'),
        'mogi das cruzes': Location('Mogi das Cruzes, SP', -23.5222, -46.1880, 'Brasil', 'SP'),
        'vitória': Location('Vitória, ES', -20.3155, -40.3128, 'Brasil', 'ES'),
    }
    
    @classmethod
    def search_locations(cls, query: str, limit: int = 5) -> List[Location]:
        """
        Busca localizações baseadas na query
        
        Args:
            query: Termo de busca
            limit: Número máximo de resultados
            
        Returns:
            Lista de localizações encontradas
        """
        query_lower = query.lower().strip()
        results = []
        
        # Buscar nas cidades brasileiras pré-definidas
        for city_key, location in cls.BRAZILIAN_CITIES.items():
            if query_lower in city_key or city_key.startswith(query_lower):
                results.append(location)
                if len(results) >= limit:
                    break
        
        # Se não encontrou resultados suficientes, tentar busca mais flexível
        if len(results) < limit:
            for city_key, location in cls.BRAZILIAN_CITIES.items():
                if any(word in city_key for word in query_lower.split()) and location not in results:
                    results.append(location)
                    if len(results) >= limit:
                        break
        
        # Tentar geocodificação online como fallback (usando Nominatim)
        if len(results) == 0:
            try:
                online_results = cls._search_nominatim(query, limit)
                results.extend(online_results)
            except Exception as e:
                print(f"Erro na geocodificação online: {e}")
        
        return results[:limit]
    
    @classmethod
    def _search_nominatim(cls, query: str, limit: int = 5) -> List[Location]:
        """
        Busca usando a API Nominatim (OpenStreetMap)
        
        Args:
            query: Termo de busca
            limit: Número máximo de resultados
            
        Returns:
            Lista de localizações encontradas
        """
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': query,
                'format': 'json',
                'limit': limit,
                'addressdetails': 1,
                'accept-language': 'pt-BR,pt,en'
            }
            
            headers = {
                'User-Agent': 'WeatherApp/1.0 (Educational Project)'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data:
                try:
                    # Extrair informações da resposta
                    lat = float(item['lat'])
                    lon = float(item['lon'])
                    
                    # Construir nome da localização
                    address = item.get('address', {})
                    name_parts = []
                    
                    # Priorizar cidade, vila ou município
                    city = (address.get('city') or 
                           address.get('town') or 
                           address.get('village') or 
                           address.get('municipality'))
                    
                    if city:
                        name_parts.append(city)
                    
                    # Adicionar estado/região
                    state = (address.get('state') or 
                            address.get('region'))
                    
                    if state:
                        name_parts.append(state)
                    
                    # Se não conseguiu extrair nome, usar display_name
                    if not name_parts:
                        display_name = item.get('display_name', '')
                        name_parts = display_name.split(',')[:2]
                    
                    name = ', '.join(name_parts).strip()
                    if not name:
                        continue
                    
                    country = address.get('country', '')
                    state_code = address.get('state', '')
                    
                    location = Location(
                        name=name,
                        latitude=lat,
                        longitude=lon,
                        country=country,
                        state=state_code
                    )
                    
                    results.append(location)
                    
                except (KeyError, ValueError, TypeError) as e:
                    print(f"Erro ao processar resultado da geocodificação: {e}")
                    continue
            
            return results
            
        except requests.RequestException as e:
            print(f"Erro na requisição para Nominatim: {e}")
            return []
        except Exception as e:
            print(f"Erro inesperado na geocodificação: {e}")
            return []
    
    @classmethod
    def get_location_by_coordinates(cls, lat: float, lon: float) -> Optional[Location]:
        """
        Obtém informações de localização baseadas em coordenadas (geocodificação reversa)
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Location ou None se não encontrar
        """
        try:
            url = "https://nominatim.openstreetmap.org/reverse"
            params = {
                'lat': lat,
                'lon': lon,
                'format': 'json',
                'addressdetails': 1,
                'accept-language': 'pt-BR,pt,en'
            }
            
            headers = {
                'User-Agent': 'WeatherApp/1.0 (Educational Project)'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if 'error' in data:
                return None
            
            # Extrair informações da resposta
            address = data.get('address', {})
            
            # Construir nome da localização
            name_parts = []
            
            # Priorizar cidade, vila ou município
            city = (address.get('city') or 
                   address.get('town') or 
                   address.get('village') or 
                   address.get('municipality'))
            
            if city:
                name_parts.append(city)
            
            # Adicionar estado/região
            state = (address.get('state') or 
                    address.get('region'))
            
            if state:
                name_parts.append(state)
            
            # Se não conseguiu extrair nome, usar display_name
            if not name_parts:
                display_name = data.get('display_name', '')
                name_parts = display_name.split(',')[:2]
            
            name = ', '.join(name_parts).strip()
            if not name:
                name = f"Localização ({lat:.4f}, {lon:.4f})"
            
            country = address.get('country', '')
            state_code = address.get('state', '')
            
            return Location(
                name=name,
                latitude=lat,
                longitude=lon,
                country=country,
                state=state_code
            )
            
        except requests.RequestException as e:
            print(f"Erro na geocodificação reversa: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado na geocodificação reversa: {e}")
            return None

