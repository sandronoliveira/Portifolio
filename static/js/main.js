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

document.addEventListener('DOMContentLoaded', function() {
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
            if (!confirm(message)) {
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
                        errorMessage.textContent = 'Este campo é obrigatório';
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
    
    // Confirmation dialogs for delete actions
    document.querySelectorAll('form[onsubmit*="confirm"]').forEach(form => {
        form.onsubmit = function() {
            return confirm('Tem certeza que deseja excluir este item?');
        };
    });
});