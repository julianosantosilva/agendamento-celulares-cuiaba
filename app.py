"""
Sistema de Ranking de Lojas de Conserto de Celulares
Cuiabá - MT
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production-12345')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///agendamentos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos do Banco de Dados
class Loja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200))
    bairro = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    email = db.Column(db.String(100))
    site = db.Column(db.String(200))
    instagram = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    
    # Fotos
    foto_principal = db.Column(db.String(300))
    foto_2 = db.Column(db.String(300))
    foto_3 = db.Column(db.String(300))
    
    # Especialidades (marcas que conserta)
    especialidades = db.Column(db.Text)  # Armazenado como string separada por vírgulas
    
    # Horário de funcionamento
    horario_funcionamento = db.Column(db.String(200))
    
    # Descrição
    descricao = db.Column(db.Text)
    
    # Avaliações Google
    google_rating = db.Column(db.Float, default=0.0)
    google_reviews = db.Column(db.Integer, default=0)
    google_url = db.Column(db.String(300))
    
    # Avaliações Reclame Aqui
    reclameaqui_rating = db.Column(db.Float, default=0.0)
    reclameaqui_reclamacoes = db.Column(db.Integer, default=0)
    reclameaqui_respondidas = db.Column(db.Integer, default=0)
    reclameaqui_url = db.Column(db.String(300))
    
    # Ranking calculado
    ranking_score = db.Column(db.Float, default=0.0)
    ranking_posicao = db.Column(db.Integer, default=0)
    
    # Verificação (loja verificada pelo admin)
    verificada = db.Column(db.Boolean, default=False)
    
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def calcular_ranking(self):
        """Calcula o score de ranking baseado em Google e Reclame Aqui"""
        # Peso: Google 60%, Reclame Aqui 40%
        google_score = (self.google_rating / 5.0) * 60 if self.google_rating > 0 else 0
        
        # Reclame Aqui: considera nota e % de respostas
        if self.reclameaqui_reclamacoes > 0:
            taxa_resposta = (self.reclameaqui_respondidas / self.reclameaqui_reclamacoes) * 100
            reclameaqui_score = ((self.reclameaqui_rating / 10.0) * 0.7 + (taxa_resposta / 100) * 0.3) * 40
        else:
            reclameaqui_score = (self.reclameaqui_rating / 10.0) * 40 if self.reclameaqui_rating > 0 else 0
        
        self.ranking_score = round(google_score + reclameaqui_score, 2)
        return self.ranking_score
    
    def get_especialidades_list(self):
        """Retorna lista de especialidades"""
        if self.especialidades:
            return [e.strip() for e in self.especialidades.split(',')]
        return []

# Rotas
@app.route('/')
def index():
    # Atualizar ranking de todas as lojas
    lojas = Loja.query.all()
    for loja in lojas:
        loja.calcular_ranking()
    db.session.commit()
    
    # Ordenar por ranking
    lojas_ordenadas = sorted(lojas, key=lambda x: x.ranking_score, reverse=True)
    
    # Atualizar posições
    for idx, loja in enumerate(lojas_ordenadas, 1):
        loja.ranking_posicao = idx
    db.session.commit()
    
    return render_template('index.html', lojas=lojas_ordenadas)

@app.route('/loja/<int:loja_id>')
def loja_detalhes(loja_id):
    loja = Loja.query.get_or_404(loja_id)
    return render_template('loja_detalhes.html', loja=loja)

@app.route('/cadastrar_loja', methods=['GET', 'POST'])
def cadastrar_loja():
    if request.method == 'POST':
        # Processar especialidades
        especialidades_selecionadas = request.form.getlist('especialidades')
        especialidades_str = ', '.join(especialidades_selecionadas)
        
        nova_loja = Loja(
            nome=request.form['nome'],
            endereco=request.form['endereco'],
            bairro=request.form.get('bairro', ''),
            telefone=request.form['telefone'],
            whatsapp=request.form.get('whatsapp', ''),
            email=request.form['email'],
            site=request.form.get('site', ''),
            instagram=request.form.get('instagram', ''),
            facebook=request.form.get('facebook', ''),
            foto_principal=request.form.get('foto_principal', ''),
            foto_2=request.form.get('foto_2', ''),
            foto_3=request.form.get('foto_3', ''),
            especialidades=especialidades_str,
            horario_funcionamento=request.form.get('horario_funcionamento', ''),
            descricao=request.form.get('descricao', ''),
            google_rating=float(request.form.get('google_rating', 0)),
            google_reviews=int(request.form.get('google_reviews', 0)),
            google_url=request.form.get('google_url', ''),
            reclameaqui_rating=float(request.form.get('reclameaqui_rating', 0)),
            reclameaqui_reclamacoes=int(request.form.get('reclameaqui_reclamacoes', 0)),
            reclameaqui_respondidas=int(request.form.get('reclameaqui_respondidas', 0)),
            reclameaqui_url=request.form.get('reclameaqui_url', '')
        )
        nova_loja.calcular_ranking()
        db.session.add(nova_loja)
        db.session.commit()
        flash('Loja cadastrada com sucesso! Aguarde verificação.', 'success')
        return redirect(url_for('index'))
    
    return render_template('cadastrar_loja.html')

@app.route('/cadastrar_loja', methods=['GET', 'POST'])
def cadastrar_loja():
    if request.method == 'POST':
        nova_loja = Loja(
            nome=request.form['nome'],
            endereco=request.form['endereco'],
            telefone=request.form['telefone'],
            email=request.form['email'],
            google_rating=float(request.form.get('google_rating', 0)),
            google_reviews=int(request.form.get('google_reviews', 0)),
            google_url=request.form.get('google_url', ''),
            reclameaqui_rating=float(request.form.get('reclameaqui_rating', 0)),
            reclameaqui_reclamacoes=int(request.form.get('reclameaqui_reclamacoes', 0)),
            reclameaqui_respondidas=int(request.form.get('reclameaqui_respondidas', 0)),
            reclameaqui_url=request.form.get('reclameaqui_url', '')
        )
        nova_loja.calcular_ranking()
        db.session.add(nova_loja)
        db.session.commit()
        flash('Loja cadastrada com sucesso!', 'success')
        return redirect(url_for('index'))
    
    return render_template('cadastrar_loja.html')

@app.route('/atualizar_avaliacoes/<int:loja_id>', methods=['GET', 'POST'])
def atualizar_avaliacoes(loja_id):
    loja = Loja.query.get_or_404(loja_id)
    
    if request.method == 'POST':
        loja.google_rating = float(request.form.get('google_rating', 0))
        loja.google_reviews = int(request.form.get('google_reviews', 0))
        loja.google_url = request.form.get('google_url', '')
        loja.reclameaqui_rating = float(request.form.get('reclameaqui_rating', 0))
        loja.reclameaqui_reclamacoes = int(request.form.get('reclameaqui_reclamacoes', 0))
        loja.reclameaqui_respondidas = int(request.form.get('reclameaqui_respondidas', 0))
        loja.reclameaqui_url = request.form.get('reclameaqui_url', '')
        loja.calcular_ranking()
        db.session.commit()
        flash('Avaliações atualizadas com sucesso!', 'success')
        return redirect(url_for('loja_detalhes', loja_id=loja_id))
    
    return render_template('atualizar_avaliacoes.html', loja=loja)

@app.route('/ranking')
def ranking():
    lojas = Loja.query.all()
    for loja in lojas:
        loja.calcular_ranking()
    db.session.commit()
    
    lojas_ordenadas = sorted(lojas, key=lambda x: x.ranking_score, reverse=True)
    for idx, loja in enumerate(lojas_ordenadas, 1):
        loja.ranking_posicao = idx
    db.session.commit()
    
    return render_template('ranking.html', lojas=lojas_ordenadas)

@app.route('/buscar')
def buscar():
    termo = request.args.get('q', '')
    marca = request.args.get('marca', '')
    
    lojas = Loja.query
    
    if termo:
        lojas = lojas.filter(
            (Loja.nome.contains(termo)) | 
            (Loja.bairro.contains(termo)) |
            (Loja.endereco.contains(termo))
        )
    
    if marca:
        lojas = lojas.filter(Loja.especialidades.contains(marca))
    
    lojas = lojas.all()
    
    for loja in lojas:
        loja.calcular_ranking()
    
    lojas_ordenadas = sorted(lojas, key=lambda x: x.ranking_score, reverse=True)
    
    return render_template('buscar.html', lojas=lojas_ordenadas, termo=termo, marca=marca)

def init_db():
    with app.app_context():
        # Criar pasta de uploads
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        db.create_all()
        
        # Criar lojas exemplo se não existirem
        if Loja.query.count() == 0:
            lojas_exemplo = [
                Loja(
                    nome='Tech Cell CPA',
                    endereco='Rua das Flores, 456',
                    bairro='CPA',
                    telefone='(65) 3344-5678',
                    whatsapp='(65) 99944-5678',
                    email='cpa@techcell.com',
                    instagram='@techcellcpa',
                    especialidades='Samsung, Apple, Motorola, Xiaomi, LG',
                    horario_funcionamento='Seg-Sex: 8h-18h | Sáb: 8h-12h',
                    descricao='Especializada em consertos de alta qualidade com garantia de 90 dias.',
                    foto_principal='https://via.placeholder.com/800x600?text=Tech+Cell+CPA',
                    google_rating=4.8,
                    google_reviews=203,
                    reclameaqui_rating=9.2,
                    reclameaqui_reclamacoes=8,
                    reclameaqui_respondidas=8,
                    verificada=True
                ),
                Loja(
                    nome='Cell Repair Cuiabá Centro',
                    endereco='Av. Getúlio Vargas, 123',
                    bairro='Centro',
                    telefone='(65) 3322-1234',
                    whatsapp='(65) 99922-1234',
                    email='centro@cellrepair.com',
                    instagram='@cellrepaircuiaba',
                    especialidades='Samsung, Apple, Motorola, Asus, Positivo',
                    horario_funcionamento='Seg-Sex: 9h-19h | Sáb: 9h-14h',
                    descricao='Mais de 10 anos de experiência no mercado de Cuiabá.',
                    foto_principal='https://via.placeholder.com/800x600?text=Cell+Repair+Centro',
                    google_rating=4.5,
                    google_reviews=127,
                    reclameaqui_rating=8.5,
                    reclameaqui_reclamacoes=15,
                    reclameaqui_respondidas=14,
                    verificada=True
                ),
                Loja(
                    nome='Conserta Fácil Goiabeiras',
                    endereco='Av. Fernando Corrêa, 789',
                    bairro='Goiabeiras',
                    telefone='(65) 3366-9012',
                    whatsapp='(65) 99966-9012',
                    email='goiabeiras@consertafacil.com',
                    instagram='@consertafacilcba',
                    especialidades='Samsung, Motorola, Xiaomi, Realme, Poco',
                    horario_funcionamento='Seg-Sex: 8h-17h | Sáb: 8h-13h',
                    descricao='Preços acessíveis e atendimento rápido.',
                    foto_principal='https://via.placeholder.com/800x600?text=Conserta+Facil',
                    google_rating=4.2,
                    google_reviews=89,
                    reclameaqui_rating=7.8,
                    reclameaqui_reclamacoes=22,
                    reclameaqui_respondidas=18,
                    verificada=True
                )
            ]
            for loja in lojas_exemplo:
                loja.calcular_ranking()
                db.session.add(loja)
            db.session.commit()
            print('✅ Lojas exemplo criadas com rankings!')

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
