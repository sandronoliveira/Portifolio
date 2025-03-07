from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurações para upload de imagens
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROFILE_PICS'] = os.path.join(app.config['UPLOAD_FOLDER'], 'profile')
app.config['PROJECT_IMGS'] = os.path.join(app.config['UPLOAD_FOLDER'], 'projects')
app.config['CERTIFICATE_IMGS'] = os.path.join(app.config['UPLOAD_FOLDER'], 'certificates')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Criação de diretórios de upload se não existirem
for directory in [app.config['UPLOAD_FOLDER'], app.config['PROFILE_PICS'], 
                 app.config['PROJECT_IMGS'], app.config['CERTIFICATE_IMGS']]:
    os.makedirs(directory, exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Função para verificar extensões de arquivo permitidas
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Função para gerar nomes de arquivo únicos
def generate_unique_filename(filename):
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
    institution = db.Column(db.String(100), nullable=False)
    date_completed = db.Column(db.Date)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)
    in_progress = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=False)
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
            flash('Nome de usuário ou senha inválidos')
    
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
        flash('Nenhum arquivo enviado')
        return redirect(url_for('admin'))
        
    file = request.files['profile_image']
    
    if file.filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('admin'))
        
    if file and allowed_file(file.filename):
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
        
        flash('Imagem de perfil atualizada com sucesso!')
    else:
        flash('Tipo de arquivo não permitido')
        
    return redirect(url_for('admin'))

@app.route('/admin/add_certificate', methods=['POST'])
@login_required
def add_certificate():
    title = request.form.get('title')
    institution = request.form.get('institution')
    date_completed = datetime.strptime(request.form.get('date_completed'), '%Y-%m-%d') if request.form.get('date_completed') else None
    description = request.form.get('description')
    in_progress = True if request.form.get('in_progress') else False
    
    new_certificate = Certificate(
        title=title,
        institution=institution,
        date_completed=date_completed,
        description=description,
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
    
    db.session.add(new_certificate)
    db.session.commit()
    
    flash('Certificado adicionado com sucesso!')
    return redirect(url_for('admin'))

@app.route('/admin/edit_certificate/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_certificate(id):
    certificate = Certificate.query.get_or_404(id)
    
    if request.method == 'POST':
        certificate.title = request.form.get('title')
        certificate.institution = request.form.get('institution')
        certificate.date_completed = datetime.strptime(request.form.get('date_completed'), '%Y-%m-%d') if request.form.get('date_completed') else None
        certificate.description = request.form.get('description')
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
        
        db.session.commit()
        flash('Certificado atualizado com sucesso!')
        return redirect(url_for('admin'))
    
    return render_template('edit_certificate.html', certificate=certificate, user=current_user)


@app.route('/admin/delete_certificate/<int:id>', methods=['POST'])
@login_required
def delete_certificate(id):
    certificate = Certificate.query.get_or_404(id)
    
    # Remover imagem se existir
    if certificate.image:
        image_path = os.path.join(app.config['CERTIFICATE_IMGS'], certificate.image)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(certificate)
    db.session.commit()
    
    flash('Certificado excluído com sucesso!')
    return redirect(url_for('admin'))

@app.route('/admin/add_project', methods=['POST'])
@login_required
def add_project():
    title = request.form.get('title')
    subtitle = request.form.get('subtitle')
    description = request.form.get('description')
    technologies = request.form.get('technologies')
    in_progress = True if request.form.get('in_progress') else False
    
    new_project = Project(
        title=title,
        subtitle=subtitle,
        description=description,
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
    
    db.session.add(new_project)
    db.session.commit()
    
    flash('Projeto adicionado com sucesso!')
    return redirect(url_for('admin'))

@app.route('/admin/edit_project/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.subtitle = request.form.get('subtitle')
        project.description = request.form.get('description')
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
        
        db.session.commit()
        flash('Projeto atualizado com sucesso!')
        return redirect(url_for('admin'))
    
    return render_template('edit_project.html', project=project, user=current_user)

@app.route('/admin/delete_project/<int:id>', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    
    # Remover imagem se existir
    if project.image:
        image_path = os.path.join(app.config['PROJECT_IMGS'], project.image)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(project)
    db.session.commit()
    
    flash('Projeto excluído com sucesso!')
    return redirect(url_for('admin'))

@app.route('/admin/update_certificate_image/<int:id>', methods=['POST'])
@login_required
def update_certificate_image(id):
    certificate = Certificate.query.get_or_404(id)
    
    if 'certificate_image' not in request.files:
        flash('Nenhum arquivo enviado')
        return redirect(url_for('admin'))
        
    file = request.files['certificate_image']
    
    if file.filename == '':
        flash('Nenhum arquivo selecionado')
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
        
        flash('Imagem do certificado atualizada com sucesso!')
    else:
        flash('Tipo de arquivo não permitido')
        
    return redirect(url_for('admin'))

@app.route('/admin/update_project_image/<int:id>', methods=['POST'])
@login_required
def update_project_image(id):
    project = Project.query.get_or_404(id)
    
    if 'project_image' not in request.files:
        flash('Nenhum arquivo enviado')
        return redirect(url_for('admin'))
        
    file = request.files['project_image']
    
    if file.filename == '':
        flash('Nenhum arquivo selecionado')
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
        
        flash('Imagem do projeto atualizada com sucesso!')
    else:
        flash('Tipo de arquivo não permitido')
        
    return redirect(url_for('admin'))

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
                print("Coluna 'in_progress' adicionada à tabela 'certificate'")
        
        # Verificar e adicionar coluna in_progress à tabela project
        if 'in_progress' not in [col['name'] for col in inspector.get_columns('project')]:
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE project ADD COLUMN in_progress BOOLEAN DEFAULT 0"))
                conn.commit()
                print("Coluna 'in_progress' adicionada à tabela 'project'")
        
        print("Migração do banco de dados concluída!")



def initialize_db():
    with app.app_context():
        # Criar as tabelas
        db.create_all()
        
        # Executar migrações para adicionar novas colunas se necessário
        migrate_database()
        
        # Verificar se admin existe, se não criar um
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('password')  # CHANGE THIS PASSWORD IN PRODUCTION
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

@app.route('/obrigado')
def obrigado():
    return render_template('obrigado.html', user=User.query.first())


if __name__ == '__main__':
    app.run(debug=True)  # Apenas para desenvolvimento local