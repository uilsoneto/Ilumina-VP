# 💡 Ilumina VP

Web App Colaborativo para Mapeamento de Pontos com Baixa Iluminação Pública no Setor Vicente Pires, Distrito Federal.

## Sobre o Projeto

O **Ilumina VP** permite que moradores de Vicente Pires sinalizem, via geolocalização, locais com iluminação pública inexistente ou deficitária, gerando um inventário digital georreferenciado para facilitar a comunicação com a Administração Regional.

**ODS relacionados:** 11 (Cidades e Comunidades Sustentáveis) e 16 (Paz, Justiça e Instituições Eficazes)

## Tecnologias

- **Backend:** Python 3 + Flask
- **Banco de Dados:** SQLite (via SQLAlchemy)
- **Frontend:** Bootstrap 5 + Leaflet.js (mapas)
- **Autenticação:** Flask-Login

## Como Executar

```bash
# 1. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # macOS/Linux

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Popular banco com dados de exemplo (opcional)
python seed.py

# 4. Executar o app
python run.py
```

Acesse: http://localhost:5000

## Usuários de Teste

| Usuário | E-mail | Senha | Perfil |
|---------|--------|-------|--------|
| Administrador | admin@iluminavp.com | admin123 | Admin |
| Maria Silva | morador@email.com | 123456 | Morador |

## Funcionalidades

- ✅ Cadastro e login de moradores
- ✅ Mapa interativo com todas as ocorrências (Leaflet + OpenStreetMap)
- ✅ Registro de ocorrências com geolocalização (clique no mapa)
- ✅ Categorias: Poste Apagado, Área Escura, Iluminação Fraca, Poste Danificado
- ✅ Listagem com filtro por status e paginação
- ✅ Painel admin para atualizar status das ocorrências
- ✅ API JSON para consulta dos dados (`/api/reports`)
- ✅ Design responsivo (mobile-friendly)

## Estrutura do Projeto

```
Ilumina-VP/
├── app/
│   ├── __init__.py          # Factory do app Flask
│   ├── models.py            # Modelos (User, Report)
│   ├── routes/
│   │   ├── main.py          # Rotas principais (home, mapa, API)
│   │   ├── auth.py          # Autenticação (login, registro)
│   │   └── reports.py       # CRUD de ocorrências
│   ├── templates/           # Templates HTML (Jinja2)
│   └── static/css/          # Estilos customizados
├── config.py                # Configurações
├── run.py                   # Ponto de entrada
├── seed.py                  # Dados de exemplo
└── requirements.txt         # Dependências
```

## Contexto Acadêmico

- **Instituição:** Centro Universitário Internacional UNINTER
- **Curso:** CST em Análise e Desenvolvimento de Sistemas
- **Disciplina:** Atividade Extensionista I — Tecnologia Aplicada à Inclusão Digital (Levantamento)
- **Aluno:** Uilson Vasconcelos Neto — RU 1369200
