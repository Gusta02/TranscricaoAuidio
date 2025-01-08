# API de Transcrição de Áudio

API desenvolvida para transcrição de arquivos de áudio utilizando o modelo Whisper da OpenAI. A API é capaz de processar arquivos de áudio em diferentes formatos e fornecer uma transcrição precisa do conteúdo, além de informações detalhadas sobre o tempo de processamento de cada etapa.

## Funcionalidades

- Aceita arquivos de áudio nos formatos `.wav`, `.mp3` e `.flac`
- Limite configurável de tamanho de arquivo (padrão: 50MB)
- Diferentes modelos de transcrição disponíveis (base, small, medium, large)
- Monitoramento detalhado do tempo de processamento de cada etapa
- Interface Swagger para testes e documentação

## Requisitos

- Python 3.8+
- FFmpeg (para processamento de diferentes formatos de áudio)
- Dependências Python listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Gusta02/TranscricaoAuidio.git
cd TranscricaoAuidio
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Configure as variáveis de ambiente:
- Copie o arquivo `.env.example` para `.env`
- Ajuste as variáveis conforme necessário

## Executando a API

Para iniciar o servidor de desenvolvimento:

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

## Endpoints

### POST /transcribe

Endpoint para transcrição de arquivos de áudio.

**Parâmetros:**
- `file`: Arquivo de áudio (formatos suportados: .wav, .mp3, .flac)
- `model_size`: Tamanho do modelo Whisper (opcional, padrão: "base")

**Limitações:**
- Tamanho máximo do arquivo: 50MB
- Formatos suportados: .wav, .mp3, .flac

**Exemplo de Resposta:**
```json
{
    "filename": "audio.mp3",
    "text": "Texto transcrito do áudio...",
    "status": "success",
    "processing_time": {
        "steps": {
            "validação_formato": {
                "timestamp": "2025-01-08 17:35:43",
                "elapsed_seconds": 0.05,
                "step_duration": 0.05
            },
            "validação_tamanho": {
                "timestamp": "2025-01-08 17:35:43",
                "elapsed_seconds": 0.10,
                "step_duration": 0.05
            }
        },
        "total_time_seconds": 5.5
    }
}
```

## Monitoramento de Tempo

A API monitora o tempo de processamento das seguintes etapas:

1. `validação_formato`: Validação do formato do arquivo
2. `validação_tamanho`: Verificação do tamanho do arquivo
3. `salvamento_arquivo`: Salvamento do arquivo temporário
4. `carregamento_modelo`: Carregamento do modelo Whisper
5. `transcrição`: Processo de transcrição do áudio
6. `limpeza`: Remoção de arquivos temporários

## Documentação da API

Acesse a documentação interativa em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contribuindo

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
