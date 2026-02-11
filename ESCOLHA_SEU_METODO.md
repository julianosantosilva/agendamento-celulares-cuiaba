# 🌐 ESCOLHA COMO COLOCAR ONLINE

---

## 🚀 MÉTODO 1: NGROK (Mais Rápido - 5 minutos)

### ✅ Vantagens:
- Online em 5 minutos
- Não precisa criar conta em vários lugares
- Perfeito para testar e mostrar para amigos

### ❌ Desvantagens:
- URL muda toda vez
- Precisa deixar computador ligado
- Não é permanente

### 📋 Como fazer:
1. Baixe NGROK: https://ngrok.com/download
2. Crie conta grátis: https://dashboard.ngrok.com/signup
3. Execute:
```bash
# Terminal 1
cd Agendamento_Celulares
python app.py

# Terminal 2
ngrok http 5000
```
4. Copie a URL que aparecer (ex: https://abc123.ngrok-free.app)
5. Compartilhe!

**Use este método se:** Quer testar agora ou mostrar para alguém

---

## 🏆 MÉTODO 2: RENDER (Recomendado - 30 minutos)

### ✅ Vantagens:
- 100% grátis
- URL permanente
- Não precisa deixar PC ligado
- Profissional

### ❌ Desvantagens:
- Precisa criar conta GitHub
- Precisa subir código
- Demora um pouco mais

### 📋 Como fazer:

**PASSO 1: GitHub**
1. Crie conta: https://github.com/signup
2. Crie repositório: https://github.com/new
   - Nome: `agendamento-celulares-cuiaba`
   - Público
   - Criar

**PASSO 2: Subir Código**
```bash
cd Agendamento_Celulares
git init
git add .
git commit -m "Primeiro commit"
git remote add origin https://github.com/SEU_USUARIO/agendamento-celulares-cuiaba.git
git branch -M main
git push -u origin main
```

**PASSO 3: Render**
1. Acesse: https://render.com
2. Login com GitHub
3. New + → Web Service
4. Conecte seu repositório
5. Configure:
   - Name: `agendamento-celulares-cuiaba`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
   - Free plan
6. Create Web Service
7. Aguarde 5-10 minutos

**Sua URL será:** https://agendamento-celulares-cuiaba.onrender.com

**Use este método se:** Quer algo permanente e profissional

---

## 💻 MÉTODO 3: SEU PRÓPRIO PC (Rede Local)

### ✅ Vantagens:
- Grátis
- Controle total
- Sem limites

### ❌ Desvantagens:
- Só funciona na sua rede WiFi
- PC precisa ficar ligado
- Não acessível pela internet

### 📋 Como fazer:
1. Execute: `python app.py`
2. Descubra seu IP local:
```bash
ipconfig
# Procure por "IPv4 Address" (ex: 192.168.1.100)
```
3. Acesse de outros dispositivos na mesma rede:
   `http://192.168.1.100:5000`

**Use este método se:** Quer apenas testar localmente

---

## 🎯 MINHA RECOMENDAÇÃO

### Para TESTAR AGORA:
→ Use **NGROK** (Método 1)

### Para USAR DE VERDADE:
→ Use **RENDER** (Método 2)

### Para DESENVOLVIMENTO:
→ Use **PC Local** (Método 3)

---

## 📞 PRECISA DE AJUDA?

Me diga qual método você escolheu e eu te ajudo passo a passo!

**Opções:**
1. "Quero usar NGROK" - Te ajudo a configurar
2. "Quero usar Render" - Te guio no GitHub
3. "Tenho dúvida sobre..." - Explico melhor
