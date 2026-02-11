# 🚀 COLOCAR ONLINE AGORA - NGROK

## Método mais rápido (5 minutos)

### PASSO 1: Baixar NGROK

1. Acesse: https://ngrok.com/download
2. Baixe a versão para Windows
3. Extraia o arquivo `ngrok.exe` para uma pasta (ex: C:\ngrok)

### PASSO 2: Criar Conta (Grátis)

1. Acesse: https://dashboard.ngrok.com/signup
2. Crie conta grátis
3. Copie seu token de autenticação

### PASSO 3: Configurar NGROK

Abra o terminal e execute:

```bash
# Navegar até a pasta do ngrok
cd C:\ngrok

# Autenticar (cole seu token)
ngrok config add-authtoken SEU_TOKEN_AQUI
```

### PASSO 4: Iniciar Aplicação

Em um terminal, na pasta do projeto:

```bash
cd Agendamento_Celulares
python app.py
```

Deixe esse terminal aberto!

### PASSO 5: Criar Túnel NGROK

Em OUTRO terminal:

```bash
cd C:\ngrok
ngrok http 5000
```

### PASSO 6: Acessar URL Pública

O NGROK vai mostrar algo assim:

```
Forwarding    https://xxxx-xxxx-xxxx.ngrok-free.app -> http://localhost:5000
```

**Essa é sua URL pública!** Compartilhe com qualquer pessoa!

---

## ⚠️ LIMITAÇÕES DO NGROK GRÁTIS

- URL muda toda vez que reinicia
- Máximo 40 conexões/minuto
- Sessão expira após 2 horas
- Banner do NGROK aparece

---

## ✅ VANTAGENS

- Online em 5 minutos
- Não precisa configurar nada
- Perfeito para testes
- Funciona de qualquer lugar

---

## 🔄 PARA MANTER ONLINE

Mantenha os 2 terminais abertos:
1. Terminal com `python app.py`
2. Terminal com `ngrok http 5000`

Se fechar, a URL para de funcionar!

---

## 📱 COMPARTILHAR

Envie a URL para testar:
- WhatsApp
- Email
- Redes sociais

Exemplo: https://abc123.ngrok-free.app
