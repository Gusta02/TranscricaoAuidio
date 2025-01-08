document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const audioFileInput = document.getElementById('audioFile');
    const modelSelect = document.getElementById('modelSelect');
    const uploadButton = document.getElementById('uploadButton');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.querySelector('.progress-bar');
    const statusMessage = document.getElementById('statusMessage');
    const resultContainer = document.getElementById('resultContainer');
    const transcriptionResult = document.getElementById('transcriptionResult');
    const processingTime = document.getElementById('processingTime');
    const newTranscriptionBtn = document.getElementById('newTranscriptionBtn');

    // Load system info on startup
    loadSystemInfo();

    // File upload handling
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const file = audioFileInput.files[0];
        if (!file) {
            showError('Por favor, selecione um arquivo de áudio.');
            return;
        }

        // Validate file type
        const validTypes = ['.mp3', '.wav', '.m4a'];
        const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
        if (!validTypes.includes(fileExtension)) {
            showError('Formato de arquivo inválido. Use MP3, WAV ou M4A.');
            return;
        }

        // Prepare form data
        const formData = new FormData();
        formData.append('file', file);
        formData.append('model', modelSelect.value);

        try {
            // Show progress UI
            uploadForm.classList.add('d-none');
            progressContainer.classList.remove('d-none');
            updateProgress(50, 'Processando transcrição...');

            // Upload and process file
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Show result
            updateProgress(100, 'Transcrição concluída!');
            resultContainer.classList.remove('d-none');
            transcriptionResult.textContent = data.transcription;
            processingTime.textContent = `${data.processing_time} segundos`;

        } catch (error) {
            console.error('Error:', error);
            showError('Erro ao processar o arquivo. Por favor, tente novamente.');
            resetUI();
        }
    });

    // New transcription button
    newTranscriptionBtn.addEventListener('click', function() {
        resetUI();
    });

    // File input change handler
    audioFileInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            uploadButton.textContent = `Transcrever "${file.name}"`;
        } else {
            uploadButton.textContent = 'Transcrever Áudio';
        }
    });

    // Helper functions
    function updateProgress(percent, message) {
        progressBar.style.width = `${percent}%`;
        progressBar.setAttribute('aria-valuenow', percent);
        statusMessage.textContent = message;
    }

    function showError(message) {
        alert(message);
    }

    function resetUI() {
        uploadForm.classList.remove('d-none');
        progressContainer.classList.add('d-none');
        resultContainer.classList.add('d-none');
        audioFileInput.value = '';
        uploadButton.textContent = 'Transcrever Áudio';
    }

    async function loadSystemInfo() {
        try {
            const response = await fetch('/system-info');
            const data = await response.json();
            
            const systemInfoContent = document.getElementById('systemInfoContent');
            systemInfoContent.innerHTML = `
                <ul class="list-group">
                    <li class="list-group-item">
                        <strong>Dispositivo:</strong> ${data.device}
                    </li>
                    <li class="list-group-item">
                        <strong>Modelo:</strong> ${data.model}
                    </li>
                    <li class="list-group-item">
                        <strong>GPU Disponível:</strong> ${data.cuda_available ? 'Sim' : 'Não'}
                    </li>
                    ${data.cuda_available ? `
                    <li class="list-group-item">
                        <strong>GPU:</strong> ${data.cuda_device_name}
                    </li>
                    ` : ''}
                </ul>
            `;
        } catch (error) {
            console.error('Error loading system info:', error);
        }
    }

    // Função para copiar a transcrição
    function copyTranscription() {
        const transcriptionText = document.getElementById('transcriptionResult').textContent;
        navigator.clipboard.writeText(transcriptionText).then(() => {
            alert('Texto copiado para a área de transferência!');
        }).catch(err => {
            console.error('Erro ao copiar texto:', err);
            alert('Não foi possível copiar o texto. Por favor, tente selecionar e copiar manualmente.');
        });
    }
});
