# 💡 Ilumina VP

Web App colaborativo para mapeamento de pontos com baixa iluminação pública no Setor Vicente Pires, Distrito Federal.

## Sobre o Projeto

O **Ilumina VP** permite que qualquer morador de Vicente Pires sinalize, via geolocalização, locais com iluminação pública inexistente ou deficitária — sem necessidade de cadastro. Cada ocorrência registrada é automaticamente encaminhada por e-mail para a Administração Regional de Vicente Pires e para a Neoenergia Brasília.

**ODS relacionados:** 11 (Cidades e Comunidades Sustentáveis) e 16 (Paz, Justiça e Instituições Eficazes)

## Tecnologias

- **Backend:** Python 3 + Flask
- **Banco de Dados:** SQLite (via SQLAlchemy)
- **Frontend:** Bootstrap 5 + Leaflet.js + OpenStreetMap
- **E-mail:** SMTP Gmail (envio automático para ouvidoria)

## Como Executar

```bash
# 1. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # macOS/Linux

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais Gmail (senha de app)

# 4. Popular banco com dados de exemplo (opcional)
python seed.py

# 5. Executar o app
python run.py
```

Acesse: http://localhost:5001

## Configuração de E-mail (SMTP Gmail)

Para ativar o envio automático de e-mails, configure no arquivo `.env`:

```
MAIL_USERNAME=seu-email@gmail.com
MAIL_PASSWORD=sua-senha-de-app-16-caracteres
```

Para gerar a senha de app do Gmail:
1. Acesse https://myaccount.google.com/apppasswords
2. Crie uma senha para "Outro" (nome: Ilumina VP)
3. Copie a senha gerada para o `.env`

Destinatários configurados:
- `ouvidoria@vicentepires.df.gov.br`
- `ouvidoria.bsb@neoenergia.com`

## Funcionalidades

- ✅ Mapa fullscreen com localização do usuário em tempo real
- ✅ Registro de ocorrências direto no mapa (popup com formulário)
- ✅ Sem necessidade de cadastro ou login para reportar
- ✅ Categorias: Poste Apagado, Área Escura, Iluminação Fraca, Poste Danificado
- ✅ Envio automático de e-mail para ouvidoria a cada nova ocorrência
- ✅ Campo de e-mail opcional para o cidadão receber retorno
- ✅ Listagem de ocorrências com filtro por status e paginação
- ✅ Painel administrativo (`/admin`) com dashboard e gestão de status
- ✅ Exportação de dados em CSV
- ✅ API JSON (`/api/reports`)
- ✅ Design responsivo (mobile-friendly)
- ✅ Geração de PDF da proposta acadêmica (`python gerar_proposta.py`)

## Painel Administrativo

Acesse `/admin` no navegador. Senha padrão: `iluminavp2024`

Funcionalidades do admin:
- Dashboard com estatísticas (total, pendentes, em análise, resolvidos)
- Alterar status das ocorrências
- Enviar dados por e-mail para destinatários específicos
- Exportar relatório CSV

## Estrutura do Projeto

```
Ilumina-VP/
├── app/
│   ├── __init__.py          # Factory do app Flask
│   ├── models.py            # Modelo Report
│   ├── mail.py              # Envio de e-mail via SMTP
│   ├── routes/
│   │   ├── main.py          # Rotas principais (home/mapa, API)
│   │   ├── reports.py       # CRUD de ocorrências
│   │   └── admin.py         # Painel administrativo
│   ├── templates/           # Templates HTML (Jinja2)
│   └── static/css/          # Estilos customizados
├── docs/                    # PDF da proposta gerado
├── fonts/                   # Fontes para geração de PDF
├── config.py                # Configurações (SMTP, DB)
├── run.py                   # Ponto de entrada (porta 5001)
├── seed.py                  # Dados de exemplo
├── gerar_proposta.py        # Gerador do PDF acadêmico
├── requirements.txt         # Dependências Python
├── .env.example             # Modelo de variáveis de ambiente
└── .gitignore
```

## Contexto Acadêmico

- **Instituição:** Centro Universitário Internacional UNINTER
- **Curso:** CST em Análise e Desenvolvimento de Sistemas
- **Disciplina:** Atividade Extensionista I — Tecnologia Aplicada à Inclusão Digital (Levantamento)
- **Aluno:** Uilson Vasconcelos Neto — RU 1369200
- **Local de aplicação:** Setor Vicente Pires, DF
