# 📱 COMO USAR O SISTEMA

## Passo a Passo para Iniciar

### 1️⃣ Abrir o Terminal na Pasta do Projeto
```bash
cd Agendamento_Celulares
```

### 2️⃣ Criar Ambiente Virtual (primeira vez apenas)
```bash
python -m venv venv
```

### 3️⃣ Ativar Ambiente Virtual
```bash
venv\Scripts\activate
```

### 4️⃣ Instalar Dependências (primeira vez apenas)
```bash
pip install -r requirements.txt
```

### 5️⃣ Executar o Sistema
```bash
python app.py
```

### 6️⃣ Abrir no Navegador
```
http://localhost:5000
```

---

## 🎯 Funcionalidades Principais

### Para Cadastrar uma Nova Loja:
1. Clique em "Cadastrar Loja" no menu
2. Preencha: Nome, Endereço, Telefone, E-mail
3. Clique em "Cadastrar Loja"

### Para Agendar um Conserto:
1. Na página inicial, escolha uma loja
2. Clique em "Agendar Conserto"
3. Preencha os dados:
   - Nome e telefone do cliente
   - Marca e modelo do celular
   - Descrição do problema
   - Data e hora desejada
4. Clique em "Confirmar Agendamento"

### Para Ver Agendamentos de uma Loja:
1. Na página inicial, clique em "Ver Agendamentos"
2. Você verá a lista de todos os agendamentos

### Para Atualizar Status de um Agendamento:
1. Clique em "Ver" no agendamento desejado
2. No painel lateral, altere o status
3. Informe o valor estimado (se necessário)
4. Clique em "Atualizar"

---

## 🔧 Comandos Úteis

### Parar o Servidor
Pressione `Ctrl + C` no terminal

### Desativar Ambiente Virtual
```bash
deactivate
```

### Limpar Banco de Dados (recomeçar do zero)
```bash
# Feche o servidor primeiro (Ctrl + C)
del agendamentos.db
python app.py
```

---

## 📊 Status Disponíveis

- **Pendente** (amarelo): Aguardando atendimento
- **Em Andamento** (azul): Conserto sendo realizado
- **Concluído** (verde): Serviço finalizado
- **Cancelado** (vermelho): Agendamento cancelado

---

## 💡 Dicas

- O sistema cria 3 lojas exemplo automaticamente na primeira execução
- Todos os dados ficam salvos no arquivo `agendamentos.db`
- O sistema funciona apenas localmente (localhost)
- Para acessar de outros computadores na mesma rede, use o IP da máquina

---

## ❓ Problemas Comuns

**Erro: "No module named flask"**
- Solução: Execute `pip install -r requirements.txt`

**Erro: "Address already in use"**
- Solução: Outra aplicação está usando a porta 5000. Feche-a ou mude a porta no `app.py`

**Página não carrega**
- Solução: Verifique se o servidor está rodando e acesse `http://localhost:5000`

---

## 📞 Suporte

Sistema desenvolvido para lojas de conserto de celulares em Cuiabá-MT.
