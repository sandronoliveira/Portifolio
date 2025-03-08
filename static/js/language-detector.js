// Adicionar ao final de main.js ou como um arquivo separado
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se já visitou o site antes (usando localStorage)
    const hasVisited = localStorage.getItem('site_visited');
    
    if (!hasVisited) {
        // Marcar como visitado
        localStorage.setItem('site_visited', 'true');
        
        // Obter o idioma atual do site
        const currentLanguage = document.documentElement.lang || 'pt-br';
        
        // Obter o idioma do navegador
        const browserLanguage = navigator.language.toLowerCase();
        
        // Verificar se o idioma do navegador é diferente do idioma atual
        let suggestedLanguage = null;
        
        if (browserLanguage.startsWith('en') && currentLanguage !== 'en-us') {
            suggestedLanguage = 'en-us';
        } else if (browserLanguage.startsWith('pt') && currentLanguage !== 'pt-br') {
            suggestedLanguage = 'pt-br';
        }
        
        // Se tiver um idioma sugerido diferente do atual, mostrar uma mensagem
        if (suggestedLanguage) {
            // Criar elemento de notificação
            const notification = document.createElement('div');
            notification.className = 'language-suggestion';
            notification.style.position = 'fixed';
            notification.style.bottom = '20px';
            notification.style.right = '20px';
            notification.style.backgroundColor = '#fff';
            notification.style.padding = '15px';
            notification.style.borderRadius = '8px';
            notification.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.2)';
            notification.style.zIndex = '9999';
            notification.style.maxWidth = '300px';
            
            // Texto da notificação
            const message = suggestedLanguage === 'en-us' 
                ? 'Would you like to view this page in English?' 
                : 'Gostaria de visualizar esta página em Português?';
                
            const languageName = suggestedLanguage === 'en-us' ? 'English' : 'Português';
            
            notification.innerHTML = `
                <p style="margin-top: 0; margin-bottom: 10px;">${message}</p>
                <div style="display: flex; justify-content: space-between;">
                    <a href="/set_language/${suggestedLanguage}" style="background-color: #1e3a8a; color: white; padding: 8px 12px; text-decoration: none; border-radius: 4px; font-weight: 500;">${languageName}</a>
                    <button class="close-notification" style="background: none; border: none; cursor: pointer; color: #64748b; font-weight: 500; padding: 8px 12px;">✕</button>
                </div>
            `;
            
            // Adicionar ao corpo da página
            document.body.appendChild(notification);
            
            // Adicionar evento para fechar a notificação
            notification.querySelector('.close-notification').addEventListener('click', function() {
                notification.style.display = 'none';
            });
            
            // Fechar automaticamente após 10 segundos
            setTimeout(function() {
                notification.style.opacity = '0';
                notification.style.transition = 'opacity 0.5s ease';
                
                setTimeout(function() {
                    notification.remove();
                }, 500);
            }, 10000);
        }
    }
});