# Transcrição de Áudio com Whisper

Uma aplicação web para transcrição de áudio usando FastAPI e Whisper, com interface amigável e processamento eficiente.

## 🚀 Funcionalidades

- Upload de arquivos de áudio (MP3, WAV, M4A)
- Transcrição automática usando OpenAI Whisper
- Interface web moderna e responsiva
- Suporte a GPU para processamento acelerado
- Sistema de logging completo
- Medição de tempo de processamento
- Cópia fácil do texto transcrito

## 📋 Pré-requisitos

- Python 3.8+
- FFmpeg instalado e no PATH
- GPU (opcional, para melhor performance)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/TranscricaoAudio.git
cd TranscricaoAudio
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🎯 Uso

1. Inicie o servidor:
```bash
uvicorn src.main:app --reload
```

2. Acesse a aplicação:
- Interface Web: http://localhost:8000
- Documentação da API: http://localhost:8000/docs

## 📁 Estrutura do Projeto

```
TranscricaoAudio/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   └── transcriber.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   ├── __init__.py
│   └── main.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   └── index.html
├── input/
├── output/
├── logs/
└── requirements.txt
```

## 🛠️ Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web
- [Whisper](https://github.com/openai/whisper) - Modelo de transcrição
- [PyTorch](https://pytorch.org/) - Framework de deep learning
- [Bootstrap](https://getbootstrap.com/) - Framework CSS

## ✨ Recursos

- Interface responsiva
- Feedback em tempo real
- Validação de arquivos
- Gestão eficiente de memória
- Suporte a múltiplos formatos de áudio

## 📊 Melhorias Implementadas

- [x] Otimização de performance
- [x] Sistema de logging robusto
- [x] Melhor gestão de arquivos
- [x] Interface mais responsiva
- [x] Feedback mais detalhado
- [x] Contador de tempo de processamento

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Faça o Commit de suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça o Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ✍️ Autores

* **Seu Nome** - *Trabalho Inicial* - [SeuUsuario](https://github.com/SeuUsuario)

## 🎁 Expressões de Gratidão

* Compartilhe este projeto com outras pessoas 📢
* Convide alguém da equipe para uma café ☕ 
* Um agradecimento publicamente 🤓
