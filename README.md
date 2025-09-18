# Radar Pet 🐾

![Status do Projeto](https://img.shields.io/badge/status-ativo-brightgreen)
![Versão do Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Framework](https://img.shields.io/badge/framework-Flask-black.svg)
![Licença](https://img.shields.io/badge/license-MIT-lightgrey)

**Uma plataforma web full-stack para ajudar a comunidade a encontrar animais de estimação perdidos e reuní-los com suas famílias.**

### ➡️ **[Acesse a Aplicação Online](https://radarpet.onrender.com)** ⬅️

O Radar Pet foi desenvolvido como uma solução completa para o problema comum de animais perdidos. A plataforma permite que usuários se cadastrem, publiquem anúncios detalhados de pets perdidos ou encontrados e gerenciem seus posts, tudo isso com um sistema de moderação para garantir um ambiente seguro.

![Vídeo de Demonstração do RadarPet](https://caminho/para/seu/gif_ou_video.mp4)

---

## 📋 Tabela de Conteúdos

* [Funcionalidades Principais](#-funcionalidades-principais)
* [Stack de Tecnologias](#️-stack-de-tecnologias)
* [Rodando o Projeto Localmente](#-rodando-o-projeto-localmente)
* [Administração do Sistema](#-administração-do-sistema)
* [Estrutura do Projeto](#-estrutura-do-projeto)
* [Roadmap (Próximos Passos)](#-roadmap)

---

## ✨ Funcionalidades Principais

* **Autenticação Completa:** Sistema de cadastro e login de usuários para gerenciamento de conteúdo.
* **Criação de Anúncios:** Formulários detalhados para pets perdidos ou encontrados, com upload de imagens e informações essenciais.
* **Galeria Dinâmica:** Uma página principal que exibe todos os anúncios, carregados de forma assíncrona via API.
* **Sistema de Moderação (Admin):**
    * **Painel de Administrador:** Rota protegida onde apenas administradores podem visualizar e gerenciar denúncias.
    * **Sistema de Denúncias:** Usuários podem denunciar anúncios por conteúdo impróprio.
    * **Gestão de Conteúdo:** Administradores podem deletar anúncios que violam os termos de uso.
* **Design Responsivo:** Interface adaptável para uma experiência de usuário consistente em desktops e dispositivos móveis.

## 🛠️ Stack de Tecnologias

O projeto foi construído com um stack moderno e robusto, separando claramente as responsabilidades.

* **Backend:**
    * **Linguagem:** Python 3
    * **Framework:** Flask
    * **Servidor de Produção:** Gunicorn
* **Frontend:**
    * HTML5, CSS3, JavaScript
* **Banco de Dados:**
    * PostgreSQL
    * **Driver:** `psycopg2`
* **Infraestrutura & Deploy:**
    * **Plataforma:** Render
    * **Gerenciamento de Ambiente:** `python-dotenv`

---

## 🚀 Rodando o Projeto Localmente

Siga os passos abaixo para configurar e executar o projeto em seu ambiente.

### Pré-requisitos
* Python 3.8+
* Git
* PostgreSQL

### Guia de Instalação

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/gabriel-wav/RadarPet.git](https://github.com/gabriel-wav/RadarPet.git)
    cd RadarPet
    ```

2.  **Crie e Ative um Ambiente Virtual:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    ```

3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente (`.env`):**
    Crie um arquivo `.env` na raiz do projeto e configure suas credenciais do PostgreSQL local.
    ```ini
    DB_USER=seu_usuario_postgres
    DB_PASSWORD=sua_senha
    DB_HOST=localhost
    DB_PORT=5432
    DB_DATABASE=radar_pet
    ```

5.  **Inicialize o Banco de Dados:**
    Este comando criará o banco `radar_pet` e todas as tabelas necessárias.
    ```bash
    python database.py
    ```

6.  **Execute a Aplicação:**
    ```bash
    flask run
    ```
    Acesse: [http://1227.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔑 Administração do Sistema

### Tornando um Usuário Administrador

O sistema não possui uma interface para criar administradores por segurança. A operação é feita diretamente no banco de dados.

1.  **Cadastre-se** na aplicação web normalmente.
2.  **Conecte-se** ao seu banco de dados PostgreSQL usando uma ferramenta como DBeaver ou pgAdmin.
3.  **Execute o seguinte comando SQL**, substituindo pelo e-mail do usuário que deseja promover:
    ```sql
    UPDATE usuario
    SET is_admin = TRUE
    WHERE e_mail = 'seu-email-de-admin@email.com';
    ```

### Acessando o Painel de Admin

Após um usuário ser definido como administrador no banco, ele precisa atualizar sua sessão para que as novas permissões sejam reconhecidas.

1.  Se o usuário estiver logado, ele deve primeiro **fazer logout**.
2.  Em seguida, **fazer login novamente**.

Após o novo login, um botão **"Admin"** aparecerá no cabeçalho, dando acesso ao painel de moderação.

---

## 📂 Estrutura do Projeto

A estrutura de pastas foi organizada para promover a separação de responsabilidades e a manutenibilidade.

```
radar-pet/
├── static/
│   ├── css/
│   │   ├── anunciar.css
│   │   ├── cadastro.css
│   │   ├── denuncia.css
│   │   ├── index.css
│   │   ├── login.css
│   │   ├── pet-perdido.css
│   │   └── verpet.css
│   ├── imagens/
│   ├── js/
│   │   └── main.js
│   └── uploads/
├── templates/
│   ├── admin.html
│   ├── anunciar.html
│   ├── cadastro.html
│   ├── denuncia.html
│   ├── index.html
│   ├── login.html
│   ├── pet-perdido.html
│   └── verpet.html
├── .env
├── app.py
├── config.py
├── database.py
├── models.py
├── Procfile
└── requirements.txt
```

## 🗺️ Roadmap

Este projeto está em desenvolvimento ativo. Os próximos passos planejados incluem:

* [ ] Implementar busca por filtros (espécie, raça, localização).
* [ ] Adicionar um sistema de comentários nos anúncios.
* [ ] Integrar uma API de geolocalização para exibir um mapa.
* [ ] Implementar a moderação proativa de imagens com uma API de IA (Google Cloud Vision).
