function typeText(element, text, speed = 15) {
    element.textContent = '';
    return new Promise(resolve => {
        let i = 0;
        const timer = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(timer);
                resolve();
            }
        }, speed);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file-input');
    const preview = document.getElementById('preview');
    const analyzeBtn = document.getElementById('analyze-btn');
    const result = document.getElementById('result');
    const uploadBox = document.getElementById('upload-box');
    const fossilInfo = document.getElementById('fossil-info');
    const chatInterface = document.getElementById('chat-interface');
    const chatInput = document.getElementById('chat-input');
    const chatBtn = document.getElementById('chat-btn');
    const chatResult = document.getElementById('chat-result');

    // Store the analysis result for chat context
    let currentAnalysis = null;

    // Handle file upload
    uploadBox.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop functionality
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.classList.add('drag-over');
    });

    uploadBox.addEventListener('dragleave', () => {
        uploadBox.classList.remove('drag-over');
    });

    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.classList.remove('drag-over');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleFileSelect({ target: { files: [file] } });
        }
    });

    function handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
                analyzeBtn.style.display = 'inline-block';
                result.textContent = '';
                result.className = '';
                fossilInfo.style.display = 'none';
                chatInterface.style.display = 'none';
            };
            reader.readAsDataURL(file);
        }
    }

    // Analyze button handler
    analyzeBtn.addEventListener('click', async () => {
        const file = fileInput.files[0];
        if (!file) return;

        analyzeBtn.disabled = true;
        result.textContent = 'Analyzing...';
        result.className = 'loading';
        fossilInfo.style.display = 'none';
        chatInterface.style.display = 'none';

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.error) {
                await typeText(result, 'Error: ' + data.error);
                result.className = 'error';
            } else {
                currentAnalysis = data; // Store for chat context
                const roundedConfidence = Math.round(data.confidence);
                await typeText(result, `Identified as: ${data.class} (${roundedConfidence}% confidence)`);
                result.className = 'success';

                // Show chat interface
                chatInterface.style.display = 'block';
                
                // Automatically send initial analysis to chat
                setTimeout(() => {
                    simulateInitialChat(data.class, roundedConfidence);
                }, 500);
            }
        } catch (error) {
            await typeText(result, 'Error: ' + error.message);
            result.className = 'error';
        } finally {
            analyzeBtn.disabled = false;
        }
    });

    // Simulate initial chat message with analysis
    async function simulateInitialChat(fossilType, confidence) {    
        chatResult.innerHTML = ''; // Clear any previous content

        const botLoading = document.createElement('div');
        botLoading.className = 'chat-message fossilfinder';
        botLoading.innerHTML = `<span class="chat-sender">FossilFinder</span>Thinking...`;
        chatResult.appendChild(botLoading);
        chatResult.scrollTop = chatResult.scrollHeight;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    message: `Class: ${fossilType}, Accuracy: ${confidence}%`,
                    analysis: currentAnalysis 
                })
            });

            const data = await response.json();
            if (data.error) {
                botLoading.innerHTML = `<span class="chat-sender">FossilFinder</span>❌ ${data.error}`;
                botLoading.classList.add('error');
            } else {
                botLoading.innerHTML = `<span class="chat-sender">FossilFinder</span>${data.response}`;
            }
        } catch (err) {
            botLoading.innerHTML = `<span class="chat-sender">FossilFinder</span>⚠️ Error: ${err.message}`;
            botLoading.classList.add('error');
        }
    }

    // Chat functionality
    chatBtn.addEventListener('click', async () => {
        const message = chatInput.value.trim();
        if (!message) return;

        // User message bubble
        const userMessage = document.createElement('div');
        userMessage.className = 'chat-message user';
        userMessage.innerHTML = `<span class="chat-sender">You</span>${message}`;
        chatResult.appendChild(userMessage);
        chatInput.value = '';
        chatResult.scrollTop = chatResult.scrollHeight;

        // Bot loading bubble
        const botMessage = document.createElement('div');
        botMessage.className = 'chat-message fossilfinder';
        botMessage.innerHTML = `<span class="chat-sender">FossilFinder</span>Thinking...`;
        chatResult.appendChild(botMessage);
        chatResult.scrollTop = chatResult.scrollHeight;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    message: message,
                    analysis: currentAnalysis 
                })
            });

            const data = await response.json();
            if (data.error) {
                botMessage.innerHTML = `<span class="chat-sender">FossilFinder</span>❌ ${data.error}`;
                botMessage.classList.add('error');
            } else {
                botMessage.innerHTML = `<span class="chat-sender">FossilFinder</span>${data.response}`;
            }
        } catch (err) {
            botMessage.innerHTML = `<span class="chat-sender">FossilFinder</span>⚠️ Error: ${err.message}`;
            botMessage.classList.add('error');
        }

        chatResult.scrollTop = chatResult.scrollHeight;
    });

    // Allow pressing Enter to send message
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            chatBtn.click();
        }
    });
});