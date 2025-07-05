/**
 * Aplicativo do Tempo com IA - JavaScript
 * Implementa toda a funcionalidade do frontend
 */

class WeatherApp {
    constructor() {
        this.apiBase = '/api/weather';
        this.currentLocation = null;
        this.savedCities = this.loadSavedCities();
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutos
        
        this.init();
    }

    /**
     * Inicializa o aplicativo
     */
    init() {
        this.bindEvents();
        this.loadDefaultLocation();
        this.renderSavedCities();
        this.updateLastUpdated();
        
        // Atualizar dados a cada 10 minutos
        setInterval(() => {
            if (this.currentLocation) {
                this.loadWeatherData(this.currentLocation);
            }
        }, 10 * 60 * 1000);
    }

    /**
     * Vincula eventos aos elementos da interface
     */
    bindEvents() {
        // Busca por cidade
        const searchBtn = document.getElementById('searchBtn');
        const searchInput = document.getElementById('citySearch');
        const locationBtn = document.getElementById('locationBtn');

        searchBtn.addEventListener('click', () => this.searchCity());
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.searchCity();
            }
        });
        searchInput.addEventListener('input', () => this.handleSearchInput());
        locationBtn.addEventListener('click', () => this.getCurrentLocation());

        // Controles de previsão
        const dailyBtn = document.getElementById('dailyBtn');
        const hourlyBtn = document.getElementById('hourlyBtn');
        
        dailyBtn.addEventListener('click', () => this.showDailyForecast());
        hourlyBtn.addEventListener('click', () => this.showHourlyForecast());

        // Cidades salvas
        const clearCitiesBtn = document.getElementById('clearCitiesBtn');
        clearCitiesBtn.addEventListener('click', () => this.clearSavedCities());

        // Modais
        this.bindModalEvents();

        // Navegação
        this.bindNavigationEvents();
    }

    /**
     * Vincula eventos dos modais
     */
    bindModalEvents() {
        const errorModal = document.getElementById('errorModal');
        const successModal = document.getElementById('successModal');
        
        // Fechar modais
        document.querySelectorAll('.modal-close, #errorOkBtn, #successOkBtn').forEach(btn => {
            btn.addEventListener('click', () => {
                errorModal.style.display = 'none';
                successModal.style.display = 'none';
            });
        });

        // Fechar modal clicando fora
        [errorModal, successModal].forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.style.display = 'none';
                }
            });
        });
    }

    /**
     * Vincula eventos de navegação
     */
    bindNavigationEvents() {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Atualizar navegação ativa
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                link.classList.add('active');
                
                // Rolar para seção
                const target = link.getAttribute('href');
                if (target && target.startsWith('#')) {
                    const section = document.querySelector(target);
                    if (section) {
                        section.scrollIntoView({ behavior: 'smooth' });
                    }
                }
            });
        });
    }

    /**
     * Carrega localização padrão (São Paulo)
     */
    async loadDefaultLocation() {
        const defaultLocation = {
            name: 'São Paulo, SP',
            lat: -23.5505,
            lon: -46.6333
        };
        
        await this.loadWeatherData(defaultLocation);
    }

    /**
     * Obtém localização atual do usuário
     */
    getCurrentLocation() {
        if (!navigator.geolocation) {
            this.showError('Geolocalização não é suportada pelo seu navegador');
            return;
        }

        const locationBtn = document.getElementById('locationBtn');
        const originalHTML = locationBtn.innerHTML;
        locationBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        locationBtn.disabled = true;

        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const location = {
                    name: 'Sua Localização',
                    lat: position.coords.latitude,
                    lon: position.coords.longitude
                };
                
                await this.loadWeatherData(location);
                locationBtn.innerHTML = originalHTML;
                locationBtn.disabled = false;
            },
            (error) => {
                this.showError('Não foi possível obter sua localização: ' + error.message);
                locationBtn.innerHTML = originalHTML;
                locationBtn.disabled = false;
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 300000 // 5 minutos
            }
        );
    }

    /**
     * Busca cidade digitada pelo usuário
     */
    async searchCity() {
        const searchInput = document.getElementById('citySearch');
        const query = searchInput.value.trim();
        
        if (!query) {
            this.showError('Digite o nome de uma cidade');
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Erro na busca');
            }
            
            this.showSearchResults(data.data);
        } catch (error) {
            this.showError('Erro ao buscar cidade: ' + error.message);
        }
    }

    /**
     * Manipula entrada de texto na busca
     */
    handleSearchInput() {
        const searchInput = document.getElementById('citySearch');
        const searchResults = document.getElementById('searchResults');
        
        if (searchInput.value.trim() === '') {
            searchResults.style.display = 'none';
        }
    }

    /**
     * Exibe resultados da busca
     */
    showSearchResults(cities) {
        const searchResults = document.getElementById('searchResults');
        
        if (!cities || cities.length === 0) {
            searchResults.innerHTML = '<div class="search-result-item">Nenhuma cidade encontrada</div>';
            searchResults.style.display = 'block';
            return;
        }

        const html = cities.map(city => `
            <div class="search-result-item" onclick="weatherApp.selectCity(${city.lat}, ${city.lon}, '${city.name}')">
                <div class="search-result-info">
                    <h4>${city.name}</h4>
                    <p>Lat: ${city.lat.toFixed(4)}, Lon: ${city.lon.toFixed(4)}</p>
                </div>
                <button class="save-city-btn ${this.isCitySaved(city) ? 'saved' : ''}" 
                        onclick="event.stopPropagation(); weatherApp.toggleSaveCity(${city.lat}, ${city.lon}, '${city.name}')">
                    <i class="fas fa-star"></i>
                </button>
            </div>
        `).join('');
        
        searchResults.innerHTML = html;
        searchResults.style.display = 'block';
    }

    /**
     * Seleciona uma cidade dos resultados da busca
     */
    async selectCity(lat, lon, name) {
        const searchResults = document.getElementById('searchResults');
        const searchInput = document.getElementById('citySearch');
        
        searchResults.style.display = 'none';
        searchInput.value = '';
        
        const location = { name, lat, lon };
        await this.loadWeatherData(location);
    }

    /**
     * Carrega dados meteorológicos para uma localização
     */
    async loadWeatherData(location) {
        this.currentLocation = location;
        
        try {
            // Carregar dados atuais e previsão em paralelo
            const [currentData, forecastData] = await Promise.all([
                this.fetchCurrentWeather(location),
                this.fetchForecast(location)
            ]);
            
            this.renderCurrentWeather(currentData);
            this.renderForecast(forecastData);
            this.updateLastUpdated();
            
        } catch (error) {
            this.showError('Erro ao carregar dados meteorológicos: ' + error.message);
        }
    }

    /**
     * Busca dados meteorológicos atuais
     */
    async fetchCurrentWeather(location) {
        const cacheKey = `current_${location.lat}_${location.lon}`;
        const cached = this.getFromCache(cacheKey);
        
        if (cached) {
            return cached;
        }

        const response = await fetch(
            `${this.apiBase}/current?lat=${location.lat}&lon=${location.lon}&location=${encodeURIComponent(location.name)}`
        );
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Erro ao obter dados atuais');
        }
        
        this.setCache(cacheKey, data.data);
        return data.data;
    }

    /**
     * Busca previsão meteorológica
     */
    async fetchForecast(location, days = 7) {
        const cacheKey = `forecast_${location.lat}_${location.lon}_${days}`;
        const cached = this.getFromCache(cacheKey);
        
        if (cached) {
            return cached;
        }

        const response = await fetch(
            `${this.apiBase}/forecast?lat=${location.lat}&lon=${location.lon}&location=${encodeURIComponent(location.name)}&days=${days}`
        );
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Erro ao obter previsão');
        }
        
        this.setCache(cacheKey, data.data);
        return data.data;
    }

    /**
     * Renderiza dados meteorológicos atuais
     */
    renderCurrentWeather(data) {
        const content = document.getElementById('currentWeatherContent');
        
        const weatherIcon = this.getWeatherIcon(data.weather_code);
        
        content.innerHTML = `
            <div class="current-weather">
                <div class="weather-main">
                    <div class="weather-icon">
                        <i class="${weatherIcon}"></i>
                    </div>
                    <div class="weather-info">
                        <h3>${data.location}</h3>
                        <p class="location">Lat: ${data.latitude.toFixed(4)}, Lon: ${data.longitude.toFixed(4)}</p>
                        <p class="description">${data.description}</p>
                    </div>
                </div>
                <div class="temperature">
                    ${Math.round(data.temperature)}°C
                </div>
            </div>
            <div class="weather-details">
                <div class="weather-detail">
                    <i class="fas fa-tint"></i>
                    <div class="weather-detail-info">
                        <h4>Umidade</h4>
                        <p>${data.humidity}%</p>
                    </div>
                </div>
                <div class="weather-detail">
                    <i class="fas fa-wind"></i>
                    <div class="weather-detail-info">
                        <h4>Vento</h4>
                        <p>${data.wind_speed} km/h</p>
                    </div>
                </div>
                <div class="weather-detail">
                    <i class="fas fa-compass"></i>
                    <div class="weather-detail-info">
                        <h4>Direção</h4>
                        <p>${this.getWindDirection(data.wind_direction)}</p>
                    </div>
                </div>
                <div class="weather-detail">
                    <i class="fas fa-thermometer-half"></i>
                    <div class="weather-detail-info">
                        <h4>Sensação</h4>
                        <p>${Math.round(data.temperature)}°C</p>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Renderiza previsão meteorológica
     */
    renderForecast(data) {
        this.forecastData = data;
        this.showDailyForecast(); // Mostrar previsão diária por padrão
    }

    /**
     * Mostra previsão diária
     */
    showDailyForecast() {
        const dailyBtn = document.getElementById('dailyBtn');
        const hourlyBtn = document.getElementById('hourlyBtn');
        const content = document.getElementById('forecastContent');
        
        dailyBtn.classList.add('active');
        hourlyBtn.classList.remove('active');
        
        if (!this.forecastData) {
            content.innerHTML = '<div class="loading"><div class="loading-spinner"></div><p>Carregando previsão...</p></div>';
            return;
        }
        
        const html = `
            <div class="forecast-grid">
                ${this.forecastData.daily_forecast.map(day => `
                    <div class="forecast-item">
                        <div class="forecast-date">${this.formatDate(day.date)}</div>
                        <div class="forecast-icon">
                            <i class="${this.getWeatherIcon(day.weather_code)}"></i>
                        </div>
                        <div class="forecast-temps">
                            <span class="temp-max">${Math.round(day.temperature_max)}°</span>
                            <span class="temp-min">${Math.round(day.temperature_min)}°</span>
                        </div>
                        <div class="forecast-description">${day.description}</div>
                        ${day.precipitation > 0 ? `<div class="precipitation"><i class="fas fa-cloud-rain"></i> ${day.precipitation}mm</div>` : ''}
                    </div>
                `).join('')}
            </div>
        `;
        
        content.innerHTML = html;
    }

    /**
     * Mostra previsão horária
     */
    showHourlyForecast() {
        const dailyBtn = document.getElementById('dailyBtn');
        const hourlyBtn = document.getElementById('hourlyBtn');
        const content = document.getElementById('forecastContent');
        
        dailyBtn.classList.remove('active');
        hourlyBtn.classList.add('active');
        
        if (!this.forecastData) {
            content.innerHTML = '<div class="loading"><div class="loading-spinner"></div><p>Carregando previsão...</p></div>';
            return;
        }
        
        const html = `
            <div class="hourly-forecast">
                ${this.forecastData.hourly_forecast.map(hour => `
                    <div class="hourly-item">
                        <div class="hourly-time">${this.formatTime(hour.time)}</div>
                        <div class="hourly-icon">
                            <i class="${this.getWeatherIcon(hour.weather_code)}"></i>
                        </div>
                        <div class="hourly-temp">${Math.round(hour.temperature)}°C</div>
                        <div class="hourly-humidity">${hour.humidity}%</div>
                    </div>
                `).join('')}
            </div>
        `;
        
        content.innerHTML = html;
    }

    /**
     * Alterna salvar/remover cidade
     */
    toggleSaveCity(lat, lon, name) {
        const city = { name, lat, lon };
        
        if (this.isCitySaved(city)) {
            this.removeSavedCity(city);
            this.showSuccess('Cidade removida dos favoritos');
        } else {
            this.addSavedCity(city);
            this.showSuccess('Cidade adicionada aos favoritos');
        }
        
        this.renderSavedCities();
    }

    /**
     * Verifica se cidade está salva
     */
    isCitySaved(city) {
        return this.savedCities.some(saved => 
            Math.abs(saved.lat - city.lat) < 0.01 && 
            Math.abs(saved.lon - city.lon) < 0.01
        );
    }

    /**
     * Adiciona cidade aos favoritos
     */
    addSavedCity(city) {
        if (!this.isCitySaved(city)) {
            this.savedCities.push(city);
            this.saveCitiesToStorage();
        }
    }

    /**
     * Remove cidade dos favoritos
     */
    removeSavedCity(city) {
        this.savedCities = this.savedCities.filter(saved => 
            !(Math.abs(saved.lat - city.lat) < 0.01 && Math.abs(saved.lon - city.lon) < 0.01)
        );
        this.saveCitiesToStorage();
    }

    /**
     * Renderiza cidades salvas
     */
    async renderSavedCities() {
        const content = document.getElementById('savedCitiesContent');
        
        if (this.savedCities.length === 0) {
            content.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-map-marker-alt"></i>
                    <p>Nenhuma cidade salva ainda</p>
                    <small>Pesquise por uma cidade e clique no ícone de favorito para salvá-la</small>
                </div>
            `;
            return;
        }

        content.innerHTML = '<div class="loading"><div class="loading-spinner"></div><p>Carregando cidades salvas...</p></div>';
        
        try {
            // Carregar dados de todas as cidades salvas
            const citiesData = await Promise.all(
                this.savedCities.map(async city => {
                    try {
                        const data = await this.fetchCurrentWeather(city);
                        return { ...city, weather: data };
                    } catch (error) {
                        return { ...city, weather: null };
                    }
                })
            );
            
            const html = `
                <div class="saved-cities-grid">
                    ${citiesData.map(city => `
                        <div class="saved-city-card" onclick="weatherApp.selectCity(${city.lat}, ${city.lon}, '${city.name}')">
                            <div class="saved-city-header">
                                <div class="saved-city-name">${city.name}</div>
                                <button class="remove-city-btn" onclick="event.stopPropagation(); weatherApp.removeSavedCity({lat: ${city.lat}, lon: ${city.lon}, name: '${city.name}'}); weatherApp.renderSavedCities();">
                                    <i class="fas fa-times"></i>
                                </button>
                            </div>
                            ${city.weather ? `
                                <div class="saved-city-weather">
                                    <div>
                                        <div class="saved-city-temp">${Math.round(city.weather.temperature)}°C</div>
                                        <div class="saved-city-desc">${city.weather.description}</div>
                                    </div>
                                    <div class="weather-icon">
                                        <i class="${this.getWeatherIcon(city.weather.weather_code)}"></i>
                                    </div>
                                </div>
                            ` : `
                                <div class="saved-city-weather">
                                    <div class="saved-city-desc">Erro ao carregar dados</div>
                                </div>
                            `}
                        </div>
                    `).join('')}
                </div>
            `;
            
            content.innerHTML = html;
            
        } catch (error) {
            content.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-exclamation-triangle"></i>
                    <p>Erro ao carregar cidades salvas</p>
                    <small>${error.message}</small>
                </div>
            `;
        }
    }

    /**
     * Limpa todas as cidades salvas
     */
    clearSavedCities() {
        if (this.savedCities.length === 0) {
            this.showError('Não há cidades salvas para limpar');
            return;
        }
        
        if (confirm('Tem certeza que deseja remover todas as cidades salvas?')) {
            this.savedCities = [];
            this.saveCitiesToStorage();
            this.renderSavedCities();
            this.showSuccess('Todas as cidades foram removidas');
        }
    }

    /**
     * Carrega cidades salvas do localStorage
     */
    loadSavedCities() {
        try {
            const saved = localStorage.getItem('weatherApp_savedCities');
            return saved ? JSON.parse(saved) : [];
        } catch (error) {
            console.error('Erro ao carregar cidades salvas:', error);
            return [];
        }
    }

    /**
     * Salva cidades no localStorage
     */
    saveCitiesToStorage() {
        try {
            localStorage.setItem('weatherApp_savedCities', JSON.stringify(this.savedCities));
        } catch (error) {
            console.error('Erro ao salvar cidades:', error);
        }
    }

    /**
     * Atualiza timestamp da última atualização
     */
    updateLastUpdated() {
        const element = document.getElementById('lastUpdated');
        const now = new Date();
        element.textContent = `Atualizado às ${now.toLocaleTimeString('pt-BR')}`;
    }

    /**
     * Obtém ícone do tempo baseado no código
     */
    getWeatherIcon(code) {
        const icons = {
            0: 'fas fa-sun',           // Céu limpo
            1: 'fas fa-sun',           // Principalmente limpo
            2: 'fas fa-cloud-sun',     // Parcialmente nublado
            3: 'fas fa-cloud',         // Nublado
            45: 'fas fa-smog',         // Neblina
            48: 'fas fa-smog',         // Neblina com geada
            51: 'fas fa-cloud-drizzle', // Garoa leve
            53: 'fas fa-cloud-rain',   // Garoa moderada
            55: 'fas fa-cloud-rain',   // Garoa intensa
            56: 'fas fa-cloud-rain',   // Garoa gelada leve
            57: 'fas fa-cloud-rain',   // Garoa gelada intensa
            61: 'fas fa-cloud-rain',   // Chuva leve
            63: 'fas fa-cloud-rain',   // Chuva moderada
            65: 'fas fa-cloud-showers-heavy', // Chuva intensa
            66: 'fas fa-cloud-rain',   // Chuva gelada leve
            67: 'fas fa-cloud-rain',   // Chuva gelada intensa
            71: 'fas fa-snowflake',    // Neve leve
            73: 'fas fa-snowflake',    // Neve moderada
            75: 'fas fa-snowflake',    // Neve intensa
            77: 'fas fa-cloud-meatball', // Granizo
            80: 'fas fa-cloud-rain',   // Pancadas de chuva leves
            81: 'fas fa-cloud-rain',   // Pancadas de chuva moderadas
            82: 'fas fa-cloud-showers-heavy', // Pancadas de chuva intensas
            85: 'fas fa-snowflake',    // Pancadas de neve leves
            86: 'fas fa-snowflake',    // Pancadas de neve intensas
            95: 'fas fa-bolt',         // Tempestade
            96: 'fas fa-bolt',         // Tempestade com granizo leve
            99: 'fas fa-bolt'          // Tempestade com granizo intenso
        };
        
        return icons[code] || 'fas fa-question';
    }

    /**
     * Converte direção do vento em graus para texto
     */
    getWindDirection(degrees) {
        const directions = [
            'N', 'NNE', 'NE', 'ENE',
            'E', 'ESE', 'SE', 'SSE',
            'S', 'SSW', 'SW', 'WSW',
            'W', 'WNW', 'NW', 'NNW'
        ];
        
        const index = Math.round(degrees / 22.5) % 16;
        return directions[index];
    }

    /**
     * Formata data para exibição
     */
    formatDate(dateString) {
        const date = new Date(dateString);
        const today = new Date();
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        
        if (date.toDateString() === today.toDateString()) {
            return 'Hoje';
        } else if (date.toDateString() === tomorrow.toDateString()) {
            return 'Amanhã';
        } else {
            return date.toLocaleDateString('pt-BR', { 
                weekday: 'short', 
                day: 'numeric', 
                month: 'short' 
            });
        }
    }

    /**
     * Formata hora para exibição
     */
    formatTime(timeString) {
        const date = new Date(timeString);
        return date.toLocaleTimeString('pt-BR', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }

    /**
     * Gerenciamento de cache
     */
    getFromCache(key) {
        const cached = this.cache.get(key);
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }
        return null;
    }

    setCache(key, data) {
        this.cache.set(key, {
            data,
            timestamp: Date.now()
        });
        
        // Limpar cache antigo
        if (this.cache.size > 50) {
            const oldestKey = this.cache.keys().next().value;
            this.cache.delete(oldestKey);
        }
    }

    /**
     * Exibe mensagem de erro
     */
    showError(message) {
        const modal = document.getElementById('errorModal');
        const messageElement = document.getElementById('errorMessage');
        messageElement.textContent = message;
        modal.style.display = 'block';
    }

    /**
     * Exibe mensagem de sucesso
     */
    showSuccess(message) {
        const modal = document.getElementById('successModal');
        const messageElement = document.getElementById('successMessage');
        messageElement.textContent = message;
        modal.style.display = 'block';
    }
}

// Inicializar aplicativo quando a página carregar
let weatherApp;
document.addEventListener('DOMContentLoaded', () => {
    weatherApp = new WeatherApp();
});

