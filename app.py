"""
Sistema de Ranking de Lojas de Conserto de Celulares - Cuiabá MT
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

# Modelo de Loja
class Loja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    
    # Avaliações Google
    google_rating = db.Column(db.Float, default=0.0)
    google_reviews = db.Column(db.Integer, default=0)
    google_url = db.Column(db.String(300))
    
    # Avaliações Reclame Aqui
    reclameaqui_rating = db.Column(db.Float, default=0.0)
    reclameaqui_reclamacoes = db.Column(db.Integer, default=0)
    reclameaqui_respondidas = db.Column(db.Integer, default=0)
    reclameaqui_url = db.Column(db.String(300))
    
    # Ranking
    ranking_score = db.Column(db.Float, default=0.0)
    ranking_posicao = db.Column(db.Integer, default=0)
    
    def calcular_ranking(self):
        google_score = (self.google_rating / 5.0) * 60 if self.google_rating > 0 else 0
        
        if self.reclameaqui_reclamacoes > 0:
            taxa_resposta = (self.reclameaqui_respondidas / self.reclameaqui_reclamacoes) * 100
            reclameaqui_score = ((self.reclameaqui_rating / 10.0) * 0.7 + (taxa_resposta / 100) * 0.3) * 40
        else:
            reclameaqui_score = (self.reclameaqui_rating / 10.0) * 40 if self.reclameaqui_rating > 0 else 0
        
        self.ranking_score = round(google_score + reclameaqui_score, 2)
        return self.ranking_score

# Rotas
@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'Servidor funcionando!'}, 200

@app.route('/')
def index():
    try:
        lojas = Loja.query.all()
        for loja in lojas:
            loja.calcular_ranking()
        db.session.commit()
        
        lojas_ordenadas = sorted(lojas, key=lambda x: x.ranking_score, reverse=True)
        for idx, loja in enumerate(lojas_ordenadas, 1):
            loja.ranking_posicao = idx
        db.session.commit()
        
        return render_template('index.html', lojas=lojas_ordenadas)
    except Exception as e:
        return f"Erro: {str(e)}", 500

@app.route('/loja/<int:loja_id>')
def loja_detalhes(loja_id):
    loja = Loja.query.get_or_404(loja_id)
    return render_template('loja_detalhes.html', loja=loja)

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
        flash('Avaliações atualizadas!', 'success')
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

def init_db():
    with app.app_context():
        try:
            db.create_all()
            print('✅ Banco de dados criado!')
            
            if Loja.query.count() == 0:
                lojas_exemplo = [
                    Loja(
                        nome='Tech Cell CPA',
                        endereco='Rua das Flores, 456 - CPA',
                        telefone='(65) 3344-5678',
                        email='cpa@techcell.com',
                        google_rating=4.8,
                        google_reviews=203,
                        reclameaqui_rating=9.2,
                        reclameaqui_reclamacoes=8,
                        reclameaqui_respondidas=8
                    ),
                    Loja(
                        nome='Cell Repair Cuiabá Centro',
                        endereco='Av. Getúlio Vargas, 123 - Centro',
                        telefone='(65) 3322-1234',
                        email='centro@cellrepair.com',
                        google_rating=4.5,
                        google_reviews=127,
                        reclameaqui_rating=8.5,
                        reclameaqui_reclamacoes=15,
                        reclameaqui_respondidas=14
                    ),
                    Loja(
                        nome='Conserta Fácil Goiabeiras',
                        endereco='Av. Fernando Corrêa, 789 - Goiabeiras',
                        telefone='(65) 3366-9012',
                        email='goiabeiras@consertafacil.com',
                        google_rating=4.2,
                        google_reviews=89,
                        reclameaqui_rating=7.8,
                        reclameaqui_reclamacoes=22,
                        reclameaqui_respondidas=18
                    )
                ]
                for loja in lojas_exemplo:
                    loja.calcular_ranking()
                    db.session.add(loja)
                db.session.commit()
                print('✅ Lojas exemplo criadas!')
        except Exception as e:
            print(f'❌ Erro ao inicializar banco: {e}')
            db.session.rollback()

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
