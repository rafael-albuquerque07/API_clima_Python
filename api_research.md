# Pesquisa de APIs Meteorológicas

## APIs Analisadas

### 1. OpenWeatherMap API
- **Plano Gratuito**: 1.000 chamadas por dia
- **Custo adicional**: $0.0015 USD por chamada extra
- **Requer**: Chave de API (registro necessário)
- **Recursos**: Dados atuais, previsão, histórico
- **Documentação**: Completa e bem estruturada

### 2. Open-Meteo API ⭐ **ESCOLHIDA**
- **Plano Gratuito**: Ilimitado para uso não comercial
- **Custo**: Totalmente gratuita
- **Requer**: Nenhuma chave de API ou registro
- **Recursos**: 
  - Dados meteorológicos atuais e previsão
  - Resolução de 1-11 km
  - Dados históricos de 80 anos
  - Atualizações horárias
  - Formato JSON simples
- **Vantagens**:
  - Sem limitações de chamadas para uso não comercial
  - Código aberto (AGPLv3)
  - Sem necessidade de registro
  - Documentação excelente
  - Suporte a múltiplas localizações

## Decisão Final

**Open-Meteo API** foi escolhida pelos seguintes motivos:
1. Totalmente gratuita sem limitações
2. Não requer chave de API ou registro
3. Excelente documentação
4. Dados precisos e atualizados
5. Suporte completo para o projeto

## Exemplo de URL da API
```
https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m
```

## Parâmetros Principais
- `latitude` e `longitude`: Coordenadas da localização
- `current`: Dados meteorológicos atuais
- `hourly`: Previsão horária
- `daily`: Previsão diária
- `timezone`: Fuso horário (opcional)

