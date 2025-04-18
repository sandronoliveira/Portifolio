from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

# Initialize Flask app
app = Flask(__name__)
app.static_folder = 'static'
app.static_url_path = '/static'

# Configure secret key - use environment variable in production
if os.environ.get('FLASK_ENV') == 'production':
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-default-production-key-change-this')
else:
    app.config['SECRET_KEY'] = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///portfolio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['LANGUAGES'] = ['pt-br', 'en-us']
app.config['DEFAULT_LANGUAGE'] = 'pt-br'

# Set up logging
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/portfolio.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Portfolio startup')

# Dicionários de tradução
translations = {
    'pt-br': {},  # O português é o idioma padrão, então usamos texto original
    'en-us': {
        # Navegação e cabeçalhos principais
        'Painel Administrativo': 'Administrative Panel',
        'Voltar ao Painel': 'Back to Panel',
        'Sair': 'Logout',
        'Usuário': 'Username',
        'Senha': 'Password',
        'Entrar': 'Login',
        'Área Administrativa': 'Administrative Area',
        'Digite suas credenciais para acessar': 'Enter your credentials to access',
        'Nome de usuário ou senha inválidos': 'Invalid username or password',
        'Início': 'Home',
        'Projetos': 'Projects',
        'Competências': 'Skills',
        'Formação': 'Education',
        'Contato': 'Contact',
        'Especialista em IA': 'AI Specialist',
        'Cientista de Dados': 'Data Scientist',
        'Transformando dados em soluções inteligentes': 'Transforming data into intelligent solutions',
        'Ver Projetos': 'View Projects',
        'Sobre Mim': 'About Me',
        'Desenvolvimento': 'Development',
        'Machine Learning': 'Machine Learning',
        'NLP': 'NLP',
        'Projetos em Destaque': 'Featured Projects',
        'Ver Todos os Projetos': 'View All Projects',
        'Confira os projetos que desenvolvi aplicando minhas habilidades em ciência de dados e inteligência artificial': 'Check out the projects I\'ve developed applying my skills in data science and artificial intelligence',
        'Em Andamento': 'In Progress',
        'Competências Profissionais': 'Professional Skills',
        'Conjunto de habilidades que adquiri ao longo da minha jornada profissional e acadêmica': 'Set of skills I\'ve acquired throughout my professional and academic journey',
        'Linguagens de Programação': 'Programming Languages',
        'Análise de Dados': 'Data Analysis',
        'Idiomas': 'Languages',
        'Competências Interpessoais': 'Interpersonal Skills',
        'Trabalho em Equipe': 'Teamwork',
        'Pensamento Crítico': 'Critical Thinking',
        'Resolução de Problemas': 'Problem Solving',
        'Formação Acadêmica': 'Academic Education',
        'Certificados e Cursos Complementares': 'Certificates and Complementary Courses',
        'Nenhum certificado cadastrado no momento.': 'No certificates registered at the moment.',
        'Entre em contato para oportunidades de trabalho, colaborações ou qualquer outra informação': 'Get in touch for job opportunities, collaborations or any other information',
        'E-mail': 'Email',
        'Telefone': 'Phone',
        'Localização': 'Location',
        'Envie uma mensagem': 'Send a message',
        'Preencha o formulário abaixo e entrarei em contato o mais breve possível': 'Fill out the form below and I\'ll get back to you as soon as possible',
        'Nome': 'Name',
        'Assunto': 'Subject',
        'Mensagem': 'Message',
        'Enviar Mensagem': 'Send Message',
        'Mensagem enviada com sucesso!': 'Message sent successfully!',
        'Obrigado por entrar em contato. Responderei sua mensagem o mais breve possível.': 'Thank you for contacting me. I will reply to your message as soon as possible.',
        'Voltar para o início': 'Back to Home',
        
        # Área administrativa - Perfil
        'Perfil': 'Profile',
        'Foto de Perfil': 'Profile Picture',
        'Nenhuma foto de perfil definida': 'No profile picture defined',
        'Selecione uma nova foto': 'Select a new photo',
        'Atualizar Foto de Perfil': 'Update Profile Picture',
        
        # Área administrativa - Certificados
        'Certificados': 'Certificates',
        'Adicionar Novo Certificado': 'Add New Certificate',
        'Título do Certificado': 'Certificate Title',
        'Título do Certificado em Inglês': 'Certificate Title in English',
        'Instituição': 'Institution',
        'Instituição em Inglês': 'Institution in English',
        'Data de Conclusão': 'Completion Date',
        'Marque esta opção se o certificado está em curso': 'Check this option if the certificate is in progress',
        'Descrição (opcional)': 'Description (optional)',
        'Descrição em Inglês (opcional)': 'Description in English (optional)',
        'Imagem do Certificado (opcional)': 'Certificate Image (optional)',
        'Adicionar Certificado': 'Add Certificate',
        'Certificados Existentes': 'Existing Certificates',
        'Nenhum certificado cadastrado.': 'No certificates registered.',
        'Atualizar Imagem': 'Update Image',
        'Adicionar Imagem': 'Add Image',
        'Tem certeza que deseja excluir este certificado?': 'Are you sure you want to delete this certificate?',
        'Editar Certificado': 'Edit Certificate',
        'Envie uma nova imagem para substituir a atual': 'Upload a new image to replace the current one',
        'Conteúdo em Português': 'Content in Portuguese',
        'Conteúdo em Inglês': 'Content in English',
        
        # Área administrativa - Projetos
        'Adicionar Novo Projeto': 'Add New Project',
        'Título do Projeto': 'Project Title',
        'Título do Projeto em Inglês': 'Project Title in English',
        'Subtítulo': 'Subtitle',
        'Subtítulo em Inglês': 'Subtitle in English',
        'Marque esta opção se o projeto está em desenvolvimento': 'Check this option if the project is in development',
        'Descrição': 'Description',
        'Descrição em Inglês': 'Description in English',
        'Use linhas separadas com marcadores (- item) para melhor formatação': 'Use separate lines with markers (- item) for better formatting',
        'Tecnologias Utilizadas': 'Technologies Used',
        'Separadas por vírgula (Ex: Python, Flask, TensorFlow)': 'Separated by comma (E.g.: Python, Flask, TensorFlow)',
        'Adicionar Projeto': 'Add Project',
        'Projetos Existentes': 'Existing Projects',
        'Nenhum projeto cadastrado.': 'No projects registered.',
        'Imagem do Projeto (opcional)': 'Project Image (optional)',
        'Tem certeza que deseja excluir este projeto?': 'Are you sure you want to delete this project?',
        'Editar Projeto': 'Edit Project',
        
        # Botões e ações comuns
        'Salvar Alterações': 'Save Changes',
        'Cancelar': 'Cancel',
        'Enviar': 'Submit',
        'Excluir': 'Delete',
        'Fechar': 'Close',
        'Próximo': 'Next',
        'Anterior': 'Previous',
        'Sim': 'Yes',
        'Não': 'No',
        'Este campo é obrigatório': 'This field is required',
        'Tem certeza que deseja excluir este item?': 'Are you sure you want to delete this item?',
        
        # Página de idiomas
        'Escolha seu idioma': 'Choose your language',
        'Selecione o idioma preferido': 'Select your preferred language',
        'Continuar': 'Continue',
        'Selecionar idioma': 'Select language',
        'Português': 'Portuguese', 
        'Inglês': 'English',
        'Brasil': 'Brazil',
        'United States': 'United States',
        'Espanhol': 'Spanish',
        'Chinês': 'Chinese',
        'Todos os direitos reservados': 'All rights reserved',
        'Portfolio desenvolvido com': 'Portfolio developed with',
        'por': 'by',
        
        # Níveis de proficiência em idiomas
        'Nativo': 'Native',
        'Avançado': 'Advanced',
        'Intermediário': 'Intermediate',
        'Básico': 'Basic',
        
        # Status do curso/certificado
        'Cursando': 'Ongoing',
        'Concluído': 'Completed',
        'Média': 'Average',
        'Cursando no período noturno': 'Attending night classes',
        
        # Elementos específicos da página de competências
        'Nível de Expertise': 'Expertise Level',
        'Áreas de Especialização': 'Areas of Expertise',
        'Ferramentas': 'Tools',
        'Frameworks & Plataformas de IA': 'AI Frameworks & Platforms',
        'Áreas de Especialização em IA': 'AI Specialization Areas',
        'Deep Learning Avançado': 'Advanced Deep Learning',
        'Processamento de Linguagem Natural': 'Natural Language Processing',
        'Visão Computacional': 'Computer Vision',
        'Engenharia de MLOps': 'MLOps Engineering',
        'AI Engineering': 'AI Engineering',
        'Análise Avançada de Dados': 'Advanced Data Analysis',
        'Comunicação Técnica': 'Technical Communication',
        'Veja minhas habilidades em ação': 'See my skills in action',
        'Confira meus projetos para ver como aplico essas competências em soluções reais de IA.': 'Check out my projects to see how I apply these skills in real AI solutions.',
        'Expertise em algoritmos avançados de aprendizado supervisionado, não-supervisionado e por reforço para soluções complexas de IA.': 'Expertise in advanced supervised, unsupervised, and reinforcement learning algorithms for complex AI solutions.',
        'Proficiência em linguagens de programação e frameworks para implementação de modelos e sistemas de IA escaláveis.': 'Proficiency in programming languages and frameworks for implementing scalable AI models and systems.',
        'Capacidade de projetar, implementar e otimizar sistemas complexos de IA para aplicações em escala empresarial.': 'Ability to design, implement, and optimize complex AI systems for enterprise-scale applications.',
        'Engenharia de IA': 'AI Engineering',
        
        # Elementos específicos da página de projetos
        'Destaque': 'Featured',
        'Inovação': 'Innovation',
        'Projeto S.A.L.V.A.': 'S.A.L.V.A. Project',
        'Sistema de Reconhecimento Visual': 'Visual Recognition System',
        'Sistema de visão computacional para auxílio em resgates de vítimas de inundações usando redes neurais convolucionais para detecção de pessoas em áreas alagadas.': 'Computer vision system to assist in rescuing flood victims using convolutional neural networks for detecting people in flooded areas.',
        'Banco de dados de ETFs com NLP': 'ETF database with NLP',
        'Vencedor do Challenge B3 - 1º Lugar': 'Winner of B3 Challenge - 1st Place',
        'Desenvolvimento de solução para integração ao FundosNET com técnicas avançadas de busca e NLP para análise de documentos financeiros.': 'Development of a solution for integration with FundosNET using advanced search techniques and NLP for financial document analysis.',
        
        # Página de contato e agradecimento
        'Mensagem Enviada': 'Message Sent',
        'Obrigado por entrar em contato. Responderei sua mensagem o mais breve possível.': 'Thank you for contacting me. I will reply to your message as soon as possible.',
        
        # Página inicial
        'Áreas de Especialização': 'Areas of Specialization',
        'Machine Learning': 'Machine Learning',
        'Desenvolvimento': 'Development',
        'Engenharia de IA': 'AI Engineering',
        'Desenvolvimento e implementação de algoritmos de ML para resolver problemas complexos de negócios.': 'Development and implementation of ML algorithms to solve complex business problems.',
        'Processamento de linguagem natural para análise de textos, classificação e extração de insights.': 'Natural language processing for text analysis, classification, and insight extraction.',
        'Transformação de dados brutos em insights acionáveis para tomada de decisões estratégicas.': 'Transforming raw data into actionable insights for strategic decision making.',
        'Implementação de redes neurais profundas para visão computacional e outras aplicações.': 'Implementation of deep neural networks for computer vision and other applications.',
        'Deep Learning': 'Deep Learning',
        'Especialista em Inteligência Artificial, apaixonado por criar soluções inovadoras através da análise de dados.': 'Artificial Intelligence specialist, passionate about creating innovative solutions through data analysis.',
        'Profissional em formação na área de Inteligência Artificial, com experiência em análise de dados, modelagem estatística e desenvolvimento de soluções baseadas em Machine Learning e NLP. Busco uma oportunidade como Cientista de Dados para aplicar técnicas avançadas de análise, modelagem preditiva e inteligência artificial na extração de insights estratégicos e na otimização de processos.': 'Professional in training in the field of Artificial Intelligence, with experience in data analysis, statistical modeling, and development of solutions based on Machine Learning and NLP. I am seeking an opportunity as a Data Scientist to apply advanced analysis techniques, predictive modeling, and artificial intelligence in extracting strategic insights and optimizing processes.',
        'Tenho perfil analítico, foco em solução de problemas e experiência no desenvolvimento de soluções escaláveis alinhadas aos objetivos do negócio.': 'I have an analytical profile, focus on problem solving, and experience in developing scalable solutions aligned with business objectives.',
        'Interessado em colaborar?': 'Interested in collaborating?',
        'Estou aberto a oportunidades de projetos e colaborações em ciência de dados e IA.': 'I am open to project opportunities and collaborations in data science and AI.',
        'Entre em Contato': 'Get in Touch',
        'Conquistas': 'Achievements',
        'Tecnologias': 'Technologies',
        'Vencedor do Challenge B3 - 1º Lugar, Next 2024': 'Winner of B3 Challenge - 1st Place, Next 2024',
        'Especialidades': 'Specialties',
        'Análise de dados, modelagem preditiva e NLP': 'Data analysis, predictive modeling, and NLP',
        'Tecnólogo em Inteligência Artificial - FIAP': 'Technologist in Artificial Intelligence - FIAP',
        'Certificado adicionado com sucesso!': 'Certificate added successfully!',
        'Certificado atualizado com sucesso!': 'Certificate updated successfully!',
        'Projeto adicionado com sucesso!': 'Project added successfully!',
        'Projeto atualizado com sucesso!': 'Project updated successfully!',
        'Desenvolvimento avançado de sistemas de IA, análise de dados e automação de processos': 'Advanced development of AI systems, data analysis and process automation',
        'Desenvolvimento e implementação de redes neurais complexas e modelos de deep learning': 'Development and implementation of complex neural networks and deep learning models',
        'Consultas complexas e manipulação de bancos de dados para análises e aplicações de Big Data': 'Complex queries and database manipulation for analyses and Big Data applications',
        'Pesquisa e desenvolvimento de modelos avançados de IA e deep learning': 'Research and development of advanced AI and deep learning models',
        'Análise estatística e visualização de dados para pesquisa em IA': 'Statistical analysis and data visualization for AI research',
        'Implantação e monitoramento de modelos de ML em ambientes de produção': 'Deployment and monitoring of ML models in production environments',
        'pandas': 'pandas',
        'scikit-learn': 'scikit-learn',
        'TensorFlow': 'TensorFlow',
        'NumPy': 'NumPy',
        'CNN': 'CNN',
        'RNN/LSTM': 'RNN/LSTM',
        'Transfer Learning': 'Transfer Learning',
        'TensorFlow Serving': 'TensorFlow Serving',
        'PostgreSQL': 'PostgreSQL',
        'MySQL': 'MySQL',
        'SQLite': 'SQLite',
        'Transformers': 'Transformers',
        'GANs': 'GANs',
        'Reinforcement Learning': 'Reinforcement Learning',
        'TorchServe': 'TorchServe',
        'ggplot2': 'ggplot2',
        'dplyr': 'dplyr',
        'tidyr': 'tidyr',
        'Docker': 'Docker',
        'Kubernetes': 'Kubernetes',
        'MLflow': 'MLflow',
        'Kubeflow': 'Kubeflow',
        'Expertise em algoritmos avançados de aprendizado supervisionado, não-supervisionado e por reforço para soluções complexas de IA.': 'Expertise in advanced supervised, unsupervised, and reinforcement learning algorithms for complex AI solutions.',
        'Proficiência em linguagens de programação e frameworks para implementação de modelos e sistemas de IA escaláveis.': 'Proficiency in programming languages and frameworks for implementing scalable AI models and systems.',
        'Capacidade de projetar, implementar e otimizar sistemas complexos de IA para aplicações em escala empresarial.': 'Ability to design, implement and optimize complex AI systems for enterprise-scale applications.',
        'Deep Learning Avançado': 'Advanced Deep Learning',
        'Arquiteturas de redes neurais complexas (CNN, RNN, Transformers)': 'Complex neural network architectures (CNN, RNN, Transformers)',
        'Modelos generativos (VAEs, GANs, Diffusion Models)': 'Generative models (VAEs, GANs, Diffusion Models)',
        'Redes neurais autorregressivas e modelos de linguagem': 'Autoregressive neural networks and language models',
        'Transfer learning e fine-tuning de modelos pré-treinados': 'Transfer learning and fine-tuning of pre-trained models',
        'Processamento de Linguagem Natural': 'Natural Language Processing',
        'Large Language Models (LLMs) e prompt engineering': 'Large Language Models (LLMs) and prompt engineering',
        'Embedding de texto e modelos semânticos': 'Text embeddings and semantic models',
        'RAG (Retrieval Augmented Generation)': 'RAG (Retrieval Augmented Generation)',
        'Análise de sentimento e classificação de texto': 'Sentiment analysis and text classification',
        'Visão Computacional': 'Computer Vision',
        'Detecção e segmentação de objetos (YOLO, Mask R-CNN)': 'Object detection and segmentation (YOLO, Mask R-CNN)',
        'Reconhecimento facial e análise de imagens': 'Facial recognition and image analysis',
        'Geração de imagens com modelos como Stable Diffusion': 'Image generation with models like Stable Diffusion',
        'Fusão multimodal de visão e linguagem': 'Multimodal fusion of vision and language',
        'Engenharia de MLOps': 'MLOps Engineering',
        'Desenvolvimento de pipelines de CI/CD para modelos de ML': 'Development of CI/CD pipelines for ML models',
        'Monitoramento de drift e performance em produção': 'Monitoring of drift and performance in production',
        'Escalabilidade de sistemas de IA em ambiente cloud': 'Scalability of AI systems in cloud environments',
        'Otimização de modelos para inferência eficiente': 'Optimization of models for efficient inference',
        'MLOps Tools': 'MLOps Tools',
        'AI Engineering': 'AI Engineering',
        'Desenvolvimento de agentes de IA e sistemas inteligentes': 'Development of AI agents and intelligent systems',
        'Integração de modelos de IA em aplicações empresariais': 'Integration of AI models in enterprise applications',
        'Arquitetura de sistemas baseados em IA e LLMs': 'Architecture of systems based on AI and LLMs',
        'Otimização de custos e eficiência de modelos grandes': 'Cost optimization and efficiency of large models',
        'Análise Avançada de Dados': 'Advanced Data Analysis',
        'Modelagem preditiva e série temporal': 'Predictive modeling and time series',
        'Técnicas de feature engineering para ML': 'Feature engineering techniques for ML',
        'Pipeline automatizados de dados para IA': 'Automated data pipelines for AI',
        'Interpretação e explicabilidade de modelos (XAI)': 'Interpretation and explainability of models (XAI)',
        'Competências Interpessoais': 'Interpersonal Skills',
        'Trabalho em Equipe': 'Teamwork',
        'Experiência em colaborar com equipes multidisciplinares e liderar projetos técnicos de IA que demandam comunicação clara e eficiente.': 'Experience collaborating with multidisciplinary teams and leading technical AI projects that require clear and efficient communication.',
        'Pensamento Crítico': 'Critical Thinking',
        'Habilidade para identificar desafios em dados complexos e propor soluções inovadoras de IA baseadas em análises aprofundadas.': 'Ability to identify challenges in complex data and propose innovative AI solutions based on in-depth analyses.',
        'Resolução de Problemas': 'Problem Solving',
        'Abordagem analítica e estruturada para solucionar problemas complexos com algoritmos de IA, com foco em soluções eficientes e escaláveis.': 'Analytical and structured approach to solving complex problems with AI algorithms, focusing on efficient and scalable solutions.',
        'Comunicação Técnica': 'Technical Communication',
        'Capacidade de traduzir conceitos complexos de IA em linguagem acessível para stakeholders e documentar soluções técnicas eficientemente.': 'Ability to translate complex AI concepts into accessible language for stakeholders and efficiently document technical solutions.',
        'Veja minhas habilidades em ação': 'See my skills in action',
        'Confira meus projetos para ver como aplico essas competências em soluções reais de IA.': 'Check out my projects to see how I apply these skills in real AI solutions.',
        '98%': '98%',
        '95%': '95%',
        '90%': '90%',
        '85%': '85%',
        '75%': '75%',

        
    }
};

# Funções de suporte ao multilinguismo

def get_locale():
    """Obtém o idioma da sessão ou o padrão."""
    return session.get('language', app.config['DEFAULT_LANGUAGE'])

def get_multilingual_field(obj, field_name):
    """
    Obtém o valor do campo no idioma atual, ou fallback para o valor padrão (português).
    
    Args:
        obj: Objeto do modelo (Project ou Certificate)
        field_name: Nome do campo (e.g., 'title', 'description')
    
    Returns:
        Valor do campo no idioma apropriado
    """
    current_lang = g.locale  # Obtém o idioma atual da sessão
    
    if current_lang == 'en-us':
        # Verificar se existe um campo correspondente com sufixo _en
        en_field_name = f"{field_name}_en"
        en_value = getattr(obj, en_field_name, None)
        
        # Retornar o valor em inglês se existir e não for vazio
        if en_value:
            return en_value
    
    # Fallback para o campo padrão (português)
    return getattr(obj, field_name)

# Adicione esta função ao contexto de todos os templates
@app.context_processor
def utility_processor():
    """Adiciona funções utilitárias aos templates."""
    return {
        '_': _,
        'get_locale': get_locale,
        'ml_field': get_multilingual_field  # Adicionar a nova função
    }

def _(text):
    """Função de tradução simples."""
    locale = get_locale()
    if locale == app.config['DEFAULT_LANGUAGE']:
        return text
    return translations[locale].get(text, text)

@app.before_request
def before_request():
    """Executa antes de cada requisição para configurar o idioma."""
    g.locale = get_locale()
    g._ = _  # Torna a função de tradução disponível nos templates


@app.route('/set_language/<language>')
def set_language(language):
    """Define o idioma do usuário."""
    if language in app.config['LANGUAGES']:
        session['language'] = language
        if request.referrer:
            return redirect(request.referrer)
    return redirect(url_for('index'))

@app.route('/language_prompt')
def language_prompt():
    """Página para seleção de idioma."""
    return render_template('language_prompt.html')


# Configurações de produção para Railway
if os.environ.get('RAILWAY_ENVIRONMENT'):
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    # Use as variáveis de ambiente para definir o host, caso necessário
    # app.config['SERVER_NAME'] = os.environ.get('SERVER_NAME', 'www.sandron.dev.br')

# Configurações para upload de imagens
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROFILE_PICS'] = os.path.join(app.config['UPLOAD_FOLDER'], 'profile')
app.config['PROJECT_IMGS'] = os.path.join(app.config['UPLOAD_FOLDER'], 'projects')
app.config['CERTIFICATE_IMGS'] = os.path.join(app.config['UPLOAD_FOLDER'], 'certificates')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16 MB para uploads

# Criação de diretórios de upload se não existirem
for directory in [app.config['UPLOAD_FOLDER'], app.config['PROFILE_PICS'], 
                 app.config['PROJECT_IMGS'], app.config['CERTIFICATE_IMGS']]:
    os.makedirs(directory, exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Função para verificar extensões de arquivo permitidas
def allowed_file(filename):
    """
    Verifica se o arquivo tem uma extensão permitida.
    
    Args:
        filename (str): Nome do arquivo
        
    Returns:
        bool: True se a extensão do arquivo é permitida, False caso contrário
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Função para gerar nomes de arquivo únicos
def generate_unique_filename(filename):
    """
    Gera um nome de arquivo único.
    
    Args:
        filename (str): Nome original do arquivo
        
    Returns:
        str: Nome de arquivo único com a mesma extensão
    """
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    return new_filename

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    profile_image = db.Column(db.String(255), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=True)  # Título em inglês
    institution = db.Column(db.String(100), nullable=False)
    institution_en = db.Column(db.String(100), nullable=True)  # Instituição em inglês
    date_completed = db.Column(db.Date)
    description = db.Column(db.Text, nullable=True)
    description_en = db.Column(db.Text, nullable=True)  # Descrição em inglês
    image = db.Column(db.String(255), nullable=True)
    in_progress = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=True)  # Título em inglês
    subtitle = db.Column(db.String(200), nullable=True)
    subtitle_en = db.Column(db.String(200), nullable=True)  # Subtítulo em inglês
    description = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text, nullable=True)  # Descrição em inglês
    technologies = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    in_progress = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
@login_manager.user_loader
def load_user(user_id):
    # Usar db.session.get em vez de query.get (recomendado na nova versão do SQLAlchemy)
    return db.session.get(User, int(user_id))

# Rota para servir arquivos de upload
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Manipulação de erros
@app.errorhandler(404)
def page_not_found(e):
    """Manipula erros 404 (página não encontrada)."""
    user = User.query.first()
    return render_template('error.html', error_code=404, 
                          error_message=_('Página não encontrada'), user=user), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Manipula erros 500 (erro interno do servidor)."""
    user = User.query.first()
    app.logger.error(f'Erro interno: {str(e)}')
    return render_template('error.html', error_code=500, 
                          error_message=_('Erro interno do servidor'), user=user), 500

@app.errorhandler(413)
def request_entity_too_large(e):
    """Manipula erros 413 (arquivo muito grande)."""
    user = User.query.first()
    flash(_('O arquivo enviado é muito grande. Tamanho máximo permitido: 16 MB.'))
    return redirect(request.referrer or url_for('admin'))

# Routes
@app.route('/')
def index():
    user = User.query.first()
    return render_template('index.html', user=user)

@app.route('/projects')
def projects():
    projects_list = Project.query.order_by(Project.created_at.desc()).all()
    user = User.query.first()
    return render_template('projects.html', projects=projects_list, user=user)

@app.route('/skills')
def skills():
    user = User.query.first()
    return render_template('skills.html', user=user)

@app.route('/education')
def education():
    certificates = Certificate.query.order_by(Certificate.date_completed.desc()).all()
    user = User.query.first()
    return render_template('education.html', certificates=certificates, user=user)

@app.route('/contact')
def contact():
    user = User.query.first()
    return render_template('contact.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin'))
        else:
            flash(_('Nome de usuário ou senha inválidos'))
            app.logger.warning(f'Tentativa de login malsucedida: {username}')
    
    user = User.query.first()
    return render_template('login.html', user=user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    certificates = Certificate.query.order_by(Certificate.date_completed.desc()).all()
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin.html', certificates=certificates, projects=projects, user=current_user)

@app.route('/admin/upload_profile_image', methods=['POST'])
@login_required
def upload_profile_image():
    if 'profile_image' not in request.files:
        flash(_('Nenhum arquivo enviado'))
        return redirect(url_for('admin'))
        
    file = request.files['profile_image']
    
    if file.filename == '':
        flash(_('Nenhum arquivo selecionado'))
        return redirect(url_for('admin'))
        
    if file and allowed_file(file.filename):
        try:
            # Excluir imagem antiga se existir
            user = User.query.get(current_user.id)
            if user.profile_image:
                old_image_path = os.path.join(app.config['PROFILE_PICS'], user.profile_image)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            # Salvar nova imagem
            filename = secure_filename(file.filename)
            unique_filename = generate_unique_filename(filename)
            file_path = os.path.join(app.config['PROFILE_PICS'], unique_filename)
            file.save(file_path)
            
            # Atualizar usuário
            user.profile_image = unique_filename
            db.session.commit()
            
            flash(_('Imagem de perfil atualizada com sucesso!'))
            app.logger.info(f'Imagem de perfil atualizada: {unique_filename}')
        except Exception as e:
            flash(_('Erro ao salvar a imagem de perfil'))
            app.logger.error(f'Erro ao salvar imagem de perfil: {str(e)}')
    else:
        flash(_('Tipo de arquivo não permitido'))
        
    return redirect(url_for('admin'))

# Função para adicionar certificado (CRUD - C)
@app.route('/admin/add_certificate', methods=['POST'])
@login_required
def add_certificate():
    try:
        # Obter dados do formulário
        title = request.form.get('title')
        title_en = request.form.get('title_en')
        institution = request.form.get('institution')
        institution_en = request.form.get('institution_en')
        date_completed = None
        
        # Converter a data se fornecida
        if request.form.get('date_completed'):
            try:
                date_completed = datetime.strptime(request.form.get('date_completed'), '%Y-%m-%d')
            except ValueError:
                flash(_('Formato de data inválido'))
                return redirect(url_for('admin'))
                
        description = request.form.get('description')
        description_en = request.form.get('description_en')
        in_progress = True if request.form.get('in_progress') else False
        
        # Criar novo certificado com suporte bilíngue
        new_certificate = Certificate(
            title=title,
            title_en=title_en,
            institution=institution,
            institution_en=institution_en,
            date_completed=date_completed,
            description=description,
            description_en=description_en,
            in_progress=in_progress
        )
        
        # Processar imagem se enviada
        if 'certificate_image' in request.files:
            file = request.files['certificate_image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = generate_unique_filename(filename)
                file_path = os.path.join(app.config['CERTIFICATE_IMGS'], unique_filename)
                file.save(file_path)
                new_certificate.image = unique_filename
        
        # Salvar no banco de dados
        db.session.add(new_certificate)
        db.session.commit()
        
        app.logger.info(f'Certificado adicionado: {title}')
        flash(_('Certificado adicionado com sucesso!'))
    except Exception as e:
        app.logger.error(f'Erro ao adicionar certificado: {str(e)}')
        flash(_('Erro ao adicionar certificado'))
        db.session.rollback()
        
    return redirect(url_for('admin'))

# Função para editar certificado (CRUD - U)
@app.route('/admin/edit_certificate/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_certificate(id):
    certificate = Certificate.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Atualizar campos em português e inglês
            certificate.title = request.form.get('title')
            certificate.title_en = request.form.get('title_en')
            certificate.institution = request.form.get('institution')
            certificate.institution_en = request.form.get('institution_en')
            
            # Converter a data se fornecida
            if request.form.get('date_completed'):
                try:
                    certificate.date_completed = datetime.strptime(request.form.get('date_completed'), '%Y-%m-%d')
                except ValueError:
                    flash(_('Formato de data inválido'))
                    return redirect(url_for('edit_certificate', id=id))
            else:
                certificate.date_completed = None
                
            certificate.description = request.form.get('description')
            certificate.description_en = request.form.get('description_en')
            certificate.in_progress = True if request.form.get('in_progress') else False
            
            # Processar imagem se enviada
            if 'certificate_image' in request.files:
                file = request.files['certificate_image']
                if file and file.filename != '' and allowed_file(file.filename):
                    # Excluir imagem antiga se existir
                    if certificate.image:
                        old_image_path = os.path.join(app.config['CERTIFICATE_IMGS'], certificate.image)
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                    
                    # Salvar nova imagem
                    filename = secure_filename(file.filename)
                    unique_filename = generate_unique_filename(filename)
                    file_path = os.path.join(app.config['CERTIFICATE_IMGS'], unique_filename)
                    file.save(file_path)
                    certificate.image = unique_filename
            
            # Salvar alterações
            db.session.commit()
            app.logger.info(f'Certificado atualizado: {certificate.title} (ID: {id})')
            flash(_('Certificado atualizado com sucesso!'))
            return redirect(url_for('admin'))
        except Exception as e:
            app.logger.error(f'Erro ao atualizar certificado: {str(e)}')
            flash(_('Erro ao atualizar certificado'))
            db.session.rollback()
            return redirect(url_for('edit_certificate', id=id))
    
    # Renderizar formulário de edição
    return render_template('edit_certificate.html', certificate=certificate, user=current_user)

# Função para excluir certificado (CRUD - D)
@app.route('/admin/delete_certificate/<int:id>', methods=['POST'])
@login_required
def delete_certificate(id):
    try:
        certificate = Certificate.query.get_or_404(id)
        
        # Remover imagem se existir
        if certificate.image:
            image_path = os.path.join(app.config['CERTIFICATE_IMGS'], certificate.image)
            if os.path.exists(image_path):
                os.remove(image_path)
        
        # Excluir do banco de dados
        db.session.delete(certificate)
        db.session.commit()
        
        app.logger.info(f'Certificado excluído: ID {id}')
        flash(_('Certificado excluído com sucesso!'))
    except Exception as e:
        app.logger.error(f'Erro ao excluir certificado: {str(e)}')
        flash(_('Erro ao excluir certificado'))
        db.session.rollback()
    
    return redirect(url_for('admin'))

# Função para adicionar projeto (CRUD - C)
@app.route('/admin/add_project', methods=['POST'])
@login_required
def add_project():
    try:
        # Obter dados do formulário
        title = request.form.get('title')
        title_en = request.form.get('title_en')
        subtitle = request.form.get('subtitle')
        subtitle_en = request.form.get('subtitle_en')
        description = request.form.get('description')
        description_en = request.form.get('description_en')
        technologies = request.form.get('technologies')
        in_progress = True if request.form.get('in_progress') else False
        
        # Criar novo projeto com suporte bilíngue
        new_project = Project(
            title=title,
            title_en=title_en,
            subtitle=subtitle,
            subtitle_en=subtitle_en,
            description=description,
            description_en=description_en,
            technologies=technologies,
            in_progress=in_progress
        )
        
        # Processar imagem se enviada
        if 'project_image' in request.files:
            file = request.files['project_image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = generate_unique_filename(filename)
                file_path = os.path.join(app.config['PROJECT_IMGS'], unique_filename)
                file.save(file_path)
                new_project.image = unique_filename
        
        # Salvar no banco de dados
        db.session.add(new_project)
        db.session.commit()
        
        app.logger.info(f'Projeto adicionado: {title}')
        flash(_('Projeto adicionado com sucesso!'))
    except Exception as e:
        app.logger.error(f'Erro ao adicionar projeto: {str(e)}')
        flash(_('Erro ao adicionar projeto'))
        db.session.rollback()
    
    return redirect(url_for('admin'))

# Função para editar projeto (CRUD - U)
@app.route('/admin/edit_project/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Atualizar campos em português e inglês
            project.title = request.form.get('title')
            project.title_en = request.form.get('title_en')
            project.subtitle = request.form.get('subtitle')
            project.subtitle_en = request.form.get('subtitle_en')
            project.description = request.form.get('description')
            project.description_en = request.form.get('description_en')
            project.technologies = request.form.get('technologies')
            project.in_progress = True if request.form.get('in_progress') else False
            
            # Processar imagem se enviada
            if 'project_image' in request.files:
                file = request.files['project_image']
                if file and file.filename != '' and allowed_file(file.filename):
                    # Excluir imagem antiga se existir
                    if project.image:
                        old_image_path = os.path.join(app.config['PROJECT_IMGS'], project.image)
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                    
                    # Salvar nova imagem
                    filename = secure_filename(file.filename)
                    unique_filename = generate_unique_filename(filename)
                    file_path = os.path.join(app.config['PROJECT_IMGS'], unique_filename)
                    file.save(file_path)
                    project.image = unique_filename
            
            # Salvar alterações
            db.session.commit()
            app.logger.info(f'Projeto atualizado: {project.title} (ID: {id})')
            flash(_('Projeto atualizado com sucesso!'))
            return redirect(url_for('admin'))
        except Exception as e:
            app.logger.error(f'Erro ao atualizar projeto: {str(e)}')
            flash(_('Erro ao atualizar projeto'))
            db.session.rollback()
            return redirect(url_for('edit_project', id=id))
    
    # Renderizar formulário de edição
    return render_template('edit_project.html', project=project, user=current_user)

# Função para excluir projeto (CRUD - D)
@app.route('/admin/delete_project/<int:id>', methods=['POST'])
@login_required
def delete_project(id):
    try:
        project = Project.query.get_or_404(id)
        
        # Remover imagem se existir
        if project.image:
            image_path = os.path.join(app.config['PROJECT_IMGS'], project.image)
            if os.path.exists(image_path):
                os.remove(image_path)
        
        # Excluir do banco de dados
        db.session.delete(project)
        db.session.commit()
        
        app.logger.info(f'Projeto excluído: ID {id}')
        flash(_('Projeto excluído com sucesso!'))
    except Exception as e:
        app.logger.error(f'Erro ao excluir projeto: {str(e)}')
        flash(_('Erro ao excluir projeto'))
        db.session.rollback()
    
    return redirect(url_for('admin'))

@app.route('/admin/update_certificate_image/<int:id>', methods=['POST'])
@login_required
def update_certificate_image(id):
    try:
        certificate = Certificate.query.get_or_404(id)
        
        if 'certificate_image' not in request.files:
            flash(_('Nenhum arquivo enviado'))
            return redirect(url_for('admin'))
            
        file = request.files['certificate_image']
        
        if file.filename == '':
            flash(_('Nenhum arquivo selecionado'))
            return redirect(url_for('admin'))
            
        if file and allowed_file(file.filename):
            # Excluir imagem antiga se existir
            if certificate.image:
                old_image_path = os.path.join(app.config['CERTIFICATE_IMGS'], certificate.image)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            # Salvar nova imagem
            filename = secure_filename(file.filename)
            unique_filename = generate_unique_filename(filename)
            file_path = os.path.join(app.config['CERTIFICATE_IMGS'], unique_filename)
            file.save(file_path)
            
            # Atualizar certificado
            certificate.image = unique_filename
            db.session.commit()
            
            app.logger.info(f'Imagem do certificado atualizada: ID {id}')
            flash(_('Imagem do certificado atualizada com sucesso!'))
        else:
            flash(_('Tipo de arquivo não permitido'))
    except Exception as e:
        app.logger.error(f'Erro ao atualizar imagem do certificado: {str(e)}')
        flash(_('Erro ao atualizar imagem do certificado'))
        db.session.rollback()
            
    return redirect(url_for('admin'))

@app.route('/admin/update_project_image/<int:id>', methods=['POST'])
@login_required
def update_project_image(id):
    try:
        project = Project.query.get_or_404(id)
        
        if 'project_image' not in request.files:
            flash(_('Nenhum arquivo enviado'))
            return redirect(url_for('admin'))
            
        file = request.files['project_image']
        
        if file.filename == '':
            flash(_('Nenhum arquivo selecionado'))
            return redirect(url_for('admin'))
            
        if file and allowed_file(file.filename):
            # Excluir imagem antiga se existir
            if project.image:
                old_image_path = os.path.join(app.config['PROJECT_IMGS'], project.image)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            # Salvar nova imagem
            filename = secure_filename(file.filename)
            unique_filename = generate_unique_filename(filename)
            file_path = os.path.join(app.config['PROJECT_IMGS'], unique_filename)
            file.save(file_path)
            
            # Atualizar projeto
            project.image = unique_filename
            db.session.commit()
            
            app.logger.info(f'Imagem do projeto atualizada: ID {id}')
            flash(_('Imagem do projeto atualizada com sucesso!'))
        else:
            flash(_('Tipo de arquivo não permitido'))
    except Exception as e:
        app.logger.error(f'Erro ao atualizar imagem do projeto: {str(e)}')
        flash(_('Erro ao atualizar imagem do projeto'))
        db.session.rollback()
            
    return redirect(url_for('admin'))

def migrate_bilingual_columns():
    """Adiciona colunas para suporte a conteúdo bilíngue nas tabelas existentes."""
    with app.app_context():
        from sqlalchemy import inspect, text
        
        inspector = inspect(db.engine)
        
        # Verificar e adicionar colunas bilíngues à tabela certificate
        certificate_columns = [col['name'] for col in inspector.get_columns('certificate')]
        project_columns = [col['name'] for col in inspector.get_columns('project')]
        
        with db.engine.connect() as conn:
            # Adicionar colunas à tabela certificate
            if 'title_en' not in certificate_columns:
                conn.execute(text("ALTER TABLE certificate ADD COLUMN title_en VARCHAR(200)"))
                app.logger.info("Coluna 'title_en' adicionada à tabela 'certificate'")
                
            if 'institution_en' not in certificate_columns:
                conn.execute(text("ALTER TABLE certificate ADD COLUMN institution_en VARCHAR(100)"))
                app.logger.info("Coluna 'institution_en' adicionada à tabela 'certificate'")
                
            if 'description_en' not in certificate_columns:
                conn.execute(text("ALTER TABLE certificate ADD COLUMN description_en TEXT"))
                app.logger.info("Coluna 'description_en' adicionada à tabela 'certificate'")
                
            # Adicionar colunas à tabela project
            if 'title_en' not in project_columns:
                conn.execute(text("ALTER TABLE project ADD COLUMN title_en VARCHAR(200)"))
                app.logger.info("Coluna 'title_en' adicionada à tabela 'project'")
                
            if 'subtitle_en' not in project_columns:
                conn.execute(text("ALTER TABLE project ADD COLUMN subtitle_en VARCHAR(200)"))
                app.logger.info("Coluna 'subtitle_en' adicionada à tabela 'project'")
                
            if 'description_en' not in project_columns:
                conn.execute(text("ALTER TABLE project ADD COLUMN description_en TEXT"))
                app.logger.info("Coluna 'description_en' adicionada à tabela 'project'")
            
            conn.commit()
            
        app.logger.info("Migração para colunas bilíngues concluída!")

def migrate_database():
    """Adiciona novas colunas às tabelas existentes."""
    with app.app_context():
        from sqlalchemy import inspect, text
        
        inspector = inspect(db.engine)
        
        # Verificar e adicionar coluna in_progress à tabela certificate
        if 'in_progress' not in [col['name'] for col in inspector.get_columns('certificate')]:
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE certificate ADD COLUMN in_progress BOOLEAN DEFAULT 0"))
                conn.commit()
                app.logger.info("Coluna 'in_progress' adicionada à tabela 'certificate'")
        
        # Verificar e adicionar coluna in_progress à tabela project
        if 'in_progress' not in [col['name'] for col in inspector.get_columns('project')]:
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE project ADD COLUMN in_progress BOOLEAN DEFAULT 0"))
                conn.commit()
                app.logger.info("Coluna 'in_progress' adicionada à tabela 'project'")
        
        app.logger.info("Migração do banco de dados concluída!")

def initialize_db():
    """
    Inicializa o banco de dados e cria dados iniciais se necessário.
    """
    with app.app_context():
        # Criar as tabelas
        db.create_all()
        
        # Executar migrações para adicionar novas colunas se necessário
        migrate_database()
        migrate_bilingual_columns()  # Nova migração para colunas bilíngues
        
        # Verificar se o usuário admin já existe
        admin_exists = User.query.filter_by(username='admin').first() is not None
        
        # Apenas adicionar dados iniciais se o admin não existir
        if not admin_exists:
            # Gerar uma senha segura para o admin em produção
            admin_password = os.environ.get('ADMIN_PASSWORD', 'change-this-in-production')
            
            admin = User(username='admin')
            admin.set_password(admin_password)
            db.session.add(admin)
            
            # Adicionar projetos iniciais do CV
            saturn = Project(
                title="Saturn",
                subtitle="Banco de dados de ETFs com NLP",
                description="- Vencedor do Challenge B3 - 1º Lugar, Next 2024.\n- Planejamento e desenvolvimento de solução para integração ao FundosNET.\n- Implantação de técnicas avançadas de busca e NLP para leitura e análise de documentos financeiros.\n- Desenvolvimento de interface intuitiva para acesso a informações complexas de forma acessível.",
                technologies="ElasticSearch, ChatGPT API, Python, HTML, Flask, PyPDF"
            )
            
            salva = Project(
                title="Projeto S.A.L.V.A.",
                subtitle="Sistema de Reconhecimento",
                description="- Desenvolvimento de um sistema de visão computacional para auxílio em resgates de vítimas de inundações.\n- Implementação de redes neurais convolucionais para reconhecimento de telhados e detecção de pessoas em áreas alagadas.\n- Otimização da identificação automática para auxiliar operações de salvamento com maior rapidez e eficiência.",
                technologies="Yolo V5, Python, HTML, OpenCV"
            )
            
            db.session.add(saturn)
            db.session.add(salva)
            
            # Adicionar certificados iniciais do CV
            certificates = [
                Certificate(
                    title="Formação em PowerBI",
                    institution="Alura",
                    date_completed=datetime.strptime("2023-01-01", "%Y-%m-%d")
                ),
                Certificate(
                    title="Computação Cognitiva Aplicada ao Marketing",
                    institution="FIAP",
                    date_completed=datetime.strptime("2023-01-01", "%Y-%m-%d")
                ),
                Certificate(
                    title="Formação Sustentável e Sustentabilidade Social",
                    institution="FIAP",
                    date_completed=datetime.strptime("2023-01-01", "%Y-%m-%d")
                ),
                Certificate(
                    title="Certificado de Qualificação Profissional em Aprendizado de Máquina",
                    institution="FIAP",
                    date_completed=datetime.strptime("2023-01-01", "%Y-%m-%d")
                ),
                Certificate(
                    title="Certificado de Qualificação Profissional em Serviços Cognitivos",
                    institution="FIAP",
                    date_completed=datetime.strptime("2023-01-01", "%Y-%m-%d")
                )
            ]
            
            for cert in certificates:
                db.session.add(cert)
                
            db.session.commit()
            app.logger.info("Banco de dados inicializado com dados padrão.")
        else:
            app.logger.info("Usuário admin já existe. Pulando inicialização de dados.")

@app.route('/obrigado')
def obrigado():
    return render_template('obrigado.html', user=User.query.first())

if __name__ == '__main__':
    initialize_db()
    
    # Configurar porta do servidor baseada em variável de ambiente ou padrão
    port = int(os.environ.get('PORT', 5000))
    
    # Ativar modo de debug apenas em ambiente de desenvolvimento
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug)