// Este arquivo deve ser incluído após main.js
// Traduções para JavaScript
const jsTranslations = {
    'pt-br': {
        // Mensagens de erro e validação
        'Este campo é obrigatório': 'Este campo é obrigatório',
        'Campo inválido': 'Campo inválido',
        'Formato de e-mail inválido': 'Formato de e-mail inválido',
        'Data inválida': 'Data inválida',
        
        // Mensagens de confirmação
        'Tem certeza que deseja excluir este item?': 'Tem certeza que deseja excluir este item?',
        'Tem certeza que deseja excluir este certificado?': 'Tem certeza que deseja excluir este certificado?',
        'Tem certeza que deseja excluir este projeto?': 'Tem certeza que deseja excluir este projeto?',
        
        // Mensagens de lightbox
        'Fechar': 'Fechar',
        'Anterior': 'Anterior',
        'Próximo': 'Próximo',
        'Imagem': 'Imagem',
        'de': 'de',
        
        // Estados de projetos e certificados
        'Em Andamento': 'Em Andamento',
        'Concluído': 'Concluído',
        
        // Outros textos dinâmicos
        'Carregando...': 'Carregando...',
        'Enviando...': 'Enviando...',
        'Aguarde...': 'Aguarde...',
        'Sucesso!': 'Sucesso!',
        'Erro!': 'Erro!',
        'Nenhum resultado encontrado': 'Nenhum resultado encontrado'
    },
    'en-us': {
        // Mensagens de erro e validação
        'Este campo é obrigatório': 'This field is required',
        'Campo inválido': 'Invalid field',
        'Formato de e-mail inválido': 'Invalid email format',
        'Data inválida': 'Invalid date',
        
        // Mensagens de confirmação
        'Tem certeza que deseja excluir este item?': 'Are you sure you want to delete this item?',
        'Tem certeza que deseja excluir este certificado?': 'Are you sure you want to delete this certificate?',
        'Tem certeza que deseja excluir este projeto?': 'Are you sure you want to delete this project?',
        
        // Mensagens de lightbox
        'Fechar': 'Close',
        'Anterior': 'Previous',
        'Próximo': 'Next',
        'Imagem': 'Image',
        'de': 'of',
        
        // Estados de projetos e certificados
        'Em Andamento': 'In Progress',
        'Concluído': 'Completed',
        
        // Outros textos dinâmicos
        'Carregando...': 'Loading...',
        'Enviando...': 'Sending...',
        'Aguarde...': 'Please wait...',
        'Sucesso!': 'Success!',
        'Erro!': 'Error!',
        'Nenhum resultado encontrado': 'No results found'
    }
};

// Obter o idioma atual do site
const currentLanguage = document.documentElement.lang || 'pt-br';

// Função de tradução para JavaScript
function translateJS(text) {
    if (currentLanguage === 'pt-br') {
        return text;
    }
    
    const translations = jsTranslations[currentLanguage] || {};
    return translations[text] || text;
}

// Substituir todas as strings traduzíveis em elementos específicos
document.addEventListener('DOMContentLoaded', function() {
    // Substituir mensagens de erro de validação
    const replaceErrorMessage = function() {
        if (this.classList.contains('error')) {
            const errorMessage = this.parentNode.querySelector('.error-message');
            if (errorMessage) {
                errorMessage.textContent = translateJS('Este campo é obrigatório');
            }
        }
    };

    document.querySelectorAll('input, textarea').forEach(field => {
        field.addEventListener('invalid', replaceErrorMessage);
    });
    
    // Substituir mensagens de confirmação
    document.querySelectorAll('form[onsubmit*="confirm"]').forEach(form => {
        const originalOnsubmit = form.onsubmit;
        form.onsubmit = function() {
            // Buscar o texto da mensagem de confirmação
            let confirmText = 'Tem certeza que deseja excluir este item?';
            
            // Tentar encontrar um texto mais específico baseado no contexto
            if (form.action.includes('delete_certificate')) {
                confirmText = 'Tem certeza que deseja excluir este certificado?';
            } else if (form.action.includes('delete_project')) {
                confirmText = 'Tem certeza que deseja excluir este projeto?';
            }
            
            return confirm(translateJS(confirmText));
        };
    });
    
    // Substituir textos em elementos com o atributo data-translate
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        element.textContent = translateJS(key);
    });
    
    // Traduzir placeholders
    document.querySelectorAll('input[placeholder], textarea[placeholder]').forEach(element => {
        const placeholder = element.getAttribute('placeholder');
        if (placeholder) {
            element.setAttribute('placeholder', translateJS(placeholder));
        }
    });
    
    // Adicionar um observador de mutações para traduzir conteúdo dinâmico
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // É um elemento
                        // Traduzir data-translate
                        if (node.hasAttribute && node.hasAttribute('data-translate')) {
                            const key = node.getAttribute('data-translate');
                            node.textContent = translateJS(key);
                        }
                        
                        // Procurar elementos dentro do nó adicionado
                        const translatableElements = node.querySelectorAll('[data-translate]');
                        translatableElements.forEach(element => {
                            const key = element.getAttribute('data-translate');
                            element.textContent = translateJS(key);
                        });
                    }
                });
            }
        });
    });
    
    // Configurar o observador
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Sobreescrever função de alerta nativa com versão traduzida
    const originalAlert = window.alert;
    window.alert = function(message) {
        return originalAlert(translateJS(message));
    };
    
    // Sobreescrever função de confirmação nativa com versão traduzida
    const originalConfirm = window.confirm;
    window.confirm = function(message) {
        return originalConfirm(translateJS(message));
    };
});