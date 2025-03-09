# translate_content.py
from app import app, db, Certificate, Project
from sqlalchemy.exc import SQLAlchemyError

def translate_certificates():
    """Add English translations for existing certificates."""
    
    # Dictionary of translations (Portuguese title -> English fields)
    translations = {
        "Formação em PowerBI": {
            "title_en": "Power BI Training",
            "institution_en": "Alura",
            "description_en": "Comprehensive training in Microsoft Power BI for data visualization and business intelligence."
        },
        "Computação Cognitiva Aplicada ao Marketing": {
            "title_en": "Cognitive Computing Applied to Marketing",
            "institution_en": "FIAP",
            "description_en": "Study of cognitive computing technologies and their applications in marketing strategies and customer behavior analysis."
        },
        "Formação Social e Sustentabilidade": {
            "title_en": "Sustainable Training and Social Sustainability",
            "institution_en": "FIAP",
            "description_en": "Course focused on sustainable practices and social responsibility in business environments."
        },
        "Certificado de Qualificação Profissional em Aprendizado de Máquina": {
            "title_en": "Professional Qualification Certificate in Machine Learning",
            "institution_en": "FIAP",
            "description_en": "Professional qualification focusing on machine learning algorithms, model development, and practical applications."
        },
        "Certificado de Qualificação Profissional em Serviços Cognitivos": {
            "title_en": "Professional Qualification Certificate in Cognitive Services",
            "institution_en": "FIAP",
            "description_en": "Professional qualification in cognitive services implementation and integration with business solutions."
        }
    }
    
    # Get all certificates from database
    certificates = Certificate.query.all()
    
    # Update translations
    updated_count = 0
    
    for cert in certificates:
        # Check if we have translations for this certificate
        if cert.title in translations:
            trans = translations[cert.title]
            
            # Update fields if they don't already have translations
            if not cert.title_en:
                cert.title_en = trans["title_en"]
            
            if not cert.institution_en:
                cert.institution_en = trans["institution_en"]
            
            if not cert.description_en and "description_en" in trans:
                cert.description_en = trans["description_en"]
            
            updated_count += 1
        else:
            # For certificates not in our dictionary, create a basic translation
            if not cert.title_en:
                cert.title_en = cert.title  # Keep original if no translation available
            
            if not cert.institution_en:
                cert.institution_en = cert.institution
    
    print(f"Updated {updated_count} certificates with translations")

def translate_projects():
    """Add English translations for existing projects."""
    
    # Dictionary of translations (Portuguese title -> English fields)
    translations = {
        "Saturn": {
            "title_en": "Saturn",
            "subtitle_en": "ETF Database with NLP",
            "description_en": "- Winner of the B3 Challenge - 1st Place, Next 2024.\n- Planning and development of a solution for integration with FundosNET.\n- Implementation of advanced search techniques and NLP for reading and analyzing financial documents.\n- Development of an intuitive interface for accessing complex information in an accessible way."
        },
        "Projeto S.A.L.V.A.": {
            "title_en": "Project S.A.L.V.A.",
            "subtitle_en": "Visual Recognition System",
            "description_en": "- Development of a computer vision system to aid in rescuing flood victims.\n- Implementation of convolutional neural networks for roof recognition and detection of people in flooded areas.\n- Optimization of automatic identification to assist rescue operations with increased speed and efficiency."
        }
    }
    
    # Get all projects from database
    projects = Project.query.all()
    
    # Update translations
    updated_count = 0
    
    for project in projects:
        # Check if we have translations for this project
        if project.title in translations:
            trans = translations[project.title]
            
            # Update fields if they don't already have translations
            if not project.title_en:
                project.title_en = trans["title_en"]
            
            if not project.subtitle_en and "subtitle_en" in trans and project.subtitle:
                project.subtitle_en = trans["subtitle_en"]
            
            if not project.description_en and "description_en" in trans:
                project.description_en = trans["description_en"]
            
            updated_count += 1
        else:
            # For projects not in our dictionary, create a basic translation
            if not project.title_en:
                project.title_en = project.title  # Keep original if no translation available
            
            if not project.subtitle_en and project.subtitle:
                project.subtitle_en = project.subtitle
    
    print(f"Updated {updated_count} projects with translations")

def main():
    """Execute the translation process."""
    with app.app_context():
        try:
            translate_certificates()
            translate_projects()
            
            # Commit all changes to database
            db.session.commit()
            print("All translations have been successfully saved to the database.")
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"An error occurred: {str(e)}")
            
        except Exception as e:
            db.session.rollback()
            print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()