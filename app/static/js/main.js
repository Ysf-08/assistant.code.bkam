document.addEventListener('DOMContentLoaded', function() {
    const chatHistoryDiv = document.getElementById('chat-history');
    const resultsDiv = document.getElementById('results');
    const chatHistory = [];

    function updateChatHistory(messages) {
        chatHistoryDiv.innerHTML = '';
        messages.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.textContent = `${message.user}: ${message.message}`;
            chatHistoryDiv.appendChild(messageElement);
        });
    }

    function loadChatHistory() {
        fetch('/get-chat-history')
            .then(response => {
                console.log('Response from /get-chat-history:', response);
                return response.json();
            })
            .then(data => {
                console.log('Chat history data:', data);
                updateChatHistory(data);
                data.forEach(message => chatHistory.push(message));
            })
            .catch(error => {
                console.error('Error fetching chat history:', error);
                resultsDiv.innerHTML = "<p>  .</p>";
            });
    }

    function handleButtonClick(url, successCallback, errorMessage) {
        const formData = new FormData(document.getElementById('code-form'));
        console.log('Sending data:', Array.from(formData.entries())); // Log data being sent

        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            console.log(`Response from ${url}:`, response);
            return response.json();
        })
        .then(data => {
            console.log('Server response data:', data); // Log server response
            if (data.success) {
                successCallback(data);
            } else {
                resultsDiv.innerHTML = `<p>${data.message}</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultsDiv.innerHTML = "<p>  .</p>";
        });
    }

    function handleGenerateTests(data) {
        resultsDiv.innerHTML = `<pre>${data.tests}</pre>`;
        chatHistory.push({user: 'User', message: `Générer Tests: ${new FormData(document.getElementById('code-form')).get('code')}`});
        chatHistory.push({user: 'Bot', message: data.tests});
        updateChatHistory(chatHistory);
    }

    function handleGenerateDocs(data) {
        resultsDiv.innerHTML = `<pre>${data.docs}</pre>`;
        chatHistory.push({user: 'User', message: `Générer Documentation: ${new FormData(document.getElementById('code-form')).get('code')}`});
        chatHistory.push({user: 'Bot', message: data.docs});
        updateChatHistory(chatHistory);
    }

    function handleOptimizeCode(data) {
        resultsDiv.innerHTML = `<pre>${data.optimized_code}</pre>`;
        chatHistory.push({user: 'User', message: `Optimiser Code: ${new FormData(document.getElementById('code-form')).get('code')}`});
        chatHistory.push({user: 'Bot', message: data.optimized_code});
        updateChatHistory(chatHistory);
    }

    function handleGenerateCode(data) {
        resultsDiv.innerHTML = `<pre>${data.generated_code}</pre>`;
        chatHistory.push({user: 'User', message: `Générer Code: ${new FormData(document.getElementById('code-form')).get('description')}`});
        chatHistory.push({user: 'Bot', message: data.generated_code});
        updateChatHistory(chatHistory);
    }

    document.getElementById('generate-tests').onclick = () => handleButtonClick('/generate-tests', handleGenerateTests, 'Erreur lors de la génération des tests.');
    document.getElementById('generate-docs').onclick = () => handleButtonClick('/generate-docs', handleGenerateDocs, 'Erreur lors de la génération de la documentation.');
    document.getElementById('optimize-code').onclick = () => handleButtonClick('/optimize-code', handleOptimizeCode, 'Erreur lors de l\'optimisation du code.');
    document.getElementById('generate-code').onclick = () => handleButtonClick('/generate-code', handleGenerateCode, 'Erreur lors de la génération du code.');

    loadChatHistory();
});
