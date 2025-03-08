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

// Função para criar o lightbox
function createLightbox() {
    // Criar o elemento do lightbox se ainda não existir
    if (!document.querySelector('.lightbox-overlay')) {
        const lightbox = document.createElement('div');
        lightbox.className = 'lightbox-overlay';
        
        const lightboxContent = document.createElement('div');
        lightboxContent.className = 'lightbox-content';
        
        const lightboxImg = document.createElement('img');
        lightboxImg.className = 'lightbox-image';
        
        const closeBtn = document.createElement('div');
        closeBtn.className = 'lightbox-close';
        closeBtn.innerHTML = '&times;';
        closeBtn.setAttribute('data-translate', 'Fechar'); // Adicionar atributo data-translate
        closeBtn.setAttribute('title', translateJS('Fechar')); // Traduzir o título imediatamente
        closeBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            closeLightbox();
        });
        
        lightboxContent.appendChild(lightboxImg);
        lightbox.appendChild(lightboxContent);
        lightbox.appendChild(closeBtn);
        
        // Fechar o lightbox ao clicar fora da imagem
        lightbox.addEventListener('click', function() {
            closeLightbox();
        });
        
        // Impedir o fechamento ao clicar na imagem
        lightboxContent.addEventListener('click', function(e) {
            e.stopPropagation();
        });
        
        // Fechar o lightbox com a tecla Esc
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeLightbox();
            }
        });
        
        document.body.appendChild(lightbox);
    }
    
    return {
        overlay: document.querySelector('.lightbox-overlay'),
        image: document.querySelector('.lightbox-image')
    };
}

// Função para abrir o lightbox
function openLightbox(imgSrc) {
    const { overlay, image } = createLightbox();
    image.src = imgSrc;
    
    // Aguardar o carregamento da imagem para mostrar o lightbox
    image.onload = function() {
        setTimeout(() => {
            overlay.classList.add('active');
        }, 50);
    };
    
    // Caso a imagem já esteja carregada
    if (image.complete) {
        setTimeout(() => {
            overlay.classList.add('active');
        }, 50);
    }
}

// Função para fechar o lightbox
function closeLightbox() {
    const overlay = document.querySelector('.lightbox-overlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
}

// Exemplo de modificação para mostrar mensagens de erro traduzidas
function showErrorMessage(field, message) {
    // Remover mensagem de erro existente, se houver
    const existingError = field.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Criar e adicionar nova mensagem de erro
    const errorMessage = document.createElement('div');
    errorMessage.className = 'error-message';
    errorMessage.textContent = translateJS(message || 'Este campo é obrigatório');
    field.parentNode.appendChild(errorMessage);
    
    // Adicionar classe de erro ao campo
    field.classList.add('error');
}

// Modificação para mensagem de confirmação
function confirmDelete(itemType) {
    let message = 'Tem certeza que deseja excluir este item?';
    
    if (itemType === 'certificate') {
        message = 'Tem certeza que deseja excluir este certificado?';
    } else if (itemType === 'project') {
        message = 'Tem certeza que deseja excluir este projeto?';
    }
    
    return confirm(translateJS(message));
}

// Função para configurar abas de idioma
function setupLanguageTabs() {
    const langTabs = document.querySelectorAll('.language-tab');
    const langContents = document.querySelectorAll('.language-content');
    
    if (langTabs.length === 0) return;
    
    // Sincronizar todas as abas de idioma na mesma página
    function syncLanguageTabs(selectedLang) {
        // Atualizar todas as abas
        langTabs.forEach(tab => {
            const tabLang = tab.getAttribute('data-lang');
            if (tabLang === selectedLang) {
                tab.classList.add('active');
            } else {
                tab.classList.remove('active');
            }
        });
        
        // Atualizar todo o conteúdo
        langContents.forEach(content => {
            const contentId = content.id;
            // Verifica se o ID termina com o idioma selecionado
            if (contentId.endsWith(`-${selectedLang}`) || contentId === `${selectedLang}-content`) {
                content.classList.add('active');
            } else {
                content.classList.remove('active');
            }
        });
        
        // Salvar preferência
        localStorage.setItem('admin_editor_language', selectedLang);
    }
    
    // Recuperar idioma preferido do administrador (se existir)
    const savedLang = localStorage.getItem('admin_editor_language');
    if (savedLang && (savedLang === 'pt' || savedLang === 'en')) {
        syncLanguageTabs(savedLang);
    }
    
    // Adicionar evento de clique às abas
    langTabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            const lang = this.getAttribute('data-lang');
            syncLanguageTabs(lang);
        });
    });
    
    // Botão para copiar texto entre idiomas
    document.querySelectorAll('.copy-to-translation').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const sourceField = document.getElementById(this.getAttribute('data-source'));
            const targetField = document.getElementById(this.getAttribute('data-target'));
            
            if (sourceField && targetField) {
                targetField.value = sourceField.value;
                
                // Efeito visual
                this.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-copy"></i>';
                }, 1500);
            }
        });
    });
}

// Função para tradução automática (placeholder - integraria com um serviço externo)
function setupAutoTranslate() {
    document.querySelectorAll('.auto-translate').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const sourceField = document.getElementById(this.getAttribute('data-source'));
            const targetField = document.getElementById(this.getAttribute('data-target'));
            
            if (sourceField && targetField) {
                // Em uma implementação real, aqui faria uma chamada para um serviço de tradução automática
                // Como Google Translate API, DeepL, etc.
                alert(translateJS('Em uma versão real, este botão enviaria o texto para um serviço de tradução automática.'));
                
                // Simulação simples (apenas para demonstração)
                targetField.value = '[Tradução automática] ' + sourceField.value;
                
                // Efeito visual
                this.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-language"></i>';
                }, 1500);
            }
        });
    });
}

// Detector de idioma do navegador e sugestão
function setupLanguageDetection() {
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
}

// Substituir strings traduzíveis em elementos específicos
function translateDOMElements() {
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
                        if (node.querySelectorAll) {
                            const translatableElements = node.querySelectorAll('[data-translate]');
                            translatableElements.forEach(element => {
                                const key = element.getAttribute('data-translate');
                                element.textContent = translateJS(key);
                            });
                        }
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
}

// Sobreescrever funções nativas para tradução automática
function overrideNativeFunctions() {
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
    
    // Substituir mensagens de confirmação nos formulários de exclusão
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
}

// Exibir indicador de idioma atual
function showLanguageIndicator() {
    const currentLang = document.documentElement.lang || 'pt-br';
    let langName, flagEmoji;
    
    if (currentLang === 'en-us') {
        langName = 'EN';
        flagEmoji = '🇺🇸';
    } else {
        langName = 'PT';
        flagEmoji = '🇧🇷';
    }
    
    // Criar indicador se não existir
    if (!document.querySelector('.lang-indicator')) {
        const indicator = document.createElement('div');
        indicator.className = 'lang-indicator';
        indicator.innerHTML = `${flagEmoji} ${langName}`;
        
        indicator.addEventListener('click', function() {
            // Alternar para o outro idioma
            const newLang = currentLang === 'en-us' ? 'pt-br' : 'en-us';
            window.location.href = `/set_language/${newLang}`;
        });
        
        document.body.appendChild(indicator);
        
        // Esconder após alguns segundos
        setTimeout(() => {
            indicator.style.opacity = '0';
            setTimeout(() => {
                indicator.remove();
            }, 500);
        }, 5000);
    }
}

// Event listener principal - inicialização
document.addEventListener('DOMContentLoaded', function() {
    // Funcionalidades de tradução e multilíngue
    translateDOMElements();
    overrideNativeFunctions();
    setupLanguageTabs();
    setupAutoTranslate();
    setupLanguageDetection();
    showLanguageIndicator();
    
    // Admin tabs functionality
    const adminTabLinks = document.querySelectorAll('.admin-tabs-nav a');
    const adminTabContents = document.querySelectorAll('.admin-content .tab-content');
    
    if (adminTabLinks.length > 0 && adminTabContents.length > 0) {
        adminTabLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all links and contents
                adminTabLinks.forEach(l => l.classList.remove('active'));
                adminTabContents.forEach(c => c.classList.remove('active'));
                
                // Add active class to clicked link
                this.classList.add('active');
                
                // Get tab ID and show corresponding content
                const tabId = this.getAttribute('data-tab');
                document.getElementById(`${tabId}-tab`).classList.add('active');
            });
        });
    }
    
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-messages .message');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(message => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.remove();
                }, 300);
            });
        }, 5000);
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                e.preventDefault();
                const target = document.querySelector(targetId);
                if (target) {
                    window.scrollTo({
                        top: target.offsetTop - 20,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    // Adicionar funcionalidade de lightbox para imagens
    const imageContainers = [
        '.project-image img',
        '.certificate-image img',
        '.admin-item-image img',
        '.current-image-preview img'
    ];
    
    imageContainers.forEach(selector => {
        document.querySelectorAll(selector).forEach(img => {
            img.addEventListener('click', function() {
                openLightbox(this.src);
            });
        });
    });
    
    // Redirect confirmation
    const confirmLinks = document.querySelectorAll('a[data-confirm]');
    confirmLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm');
            if (!confirm(translateJS(message))) {
                e.preventDefault();
            }
        });
    });
    
    // Mobile navigation toggle
    const toggleNavBtn = document.querySelector('.toggle-nav');
    const sidebar = document.querySelector('.sidebar');
    
    if (toggleNavBtn && sidebar) {
        toggleNavBtn.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            document.body.classList.toggle('nav-open');
        });
    }
    
    // Dynamic year for copyright
    const yearElement = document.querySelector('.current-year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
    
    // Form validation
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('input[required], textarea[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                    
                    // Add error message if it doesn't exist
                    let errorMessage = field.parentNode.querySelector('.error-message');
                    if (!errorMessage) {
                        errorMessage = document.createElement('div');
                        errorMessage.className = 'error-message';
                        errorMessage.textContent = translateJS('Este campo é obrigatório');
                        field.parentNode.appendChild(errorMessage);
                    }
                } else {
                    field.classList.remove('error');
                    const errorMessage = field.parentNode.querySelector('.error-message');
                    if (errorMessage) {
                        errorMessage.remove();
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
    
    // Remove error class on input when typing
    document.querySelectorAll('input, textarea').forEach(field => {
        field.addEventListener('input', function() {
            this.classList.remove('error');
            const errorMessage = this.parentNode.querySelector('.error-message');
            if (errorMessage) {
                errorMessage.remove();
            }
        });
    });
    
    // Project filter functionality (if applicable)
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectItems = document.querySelectorAll('.project-item');
    
    if (filterButtons.length > 0 && projectItems.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                const filter = this.getAttribute('data-filter');
                
                // Remove active class from all buttons
                filterButtons.forEach(btn => btn.classList.remove('active'));
                
                // Add active class to clicked button
                this.classList.add('active');
                
                // Filter projects
                projectItems.forEach(item => {
                    if (filter === 'all') {
                        item.style.display = 'block';
                    } else {
                        const categories = item.getAttribute('data-category').split(' ');
                        if (categories.includes(filter)) {
                            item.style.display = 'block';
                        } else {
                            item.style.display = 'none';
                        }
                    }
                });
            });
        });
    }
});