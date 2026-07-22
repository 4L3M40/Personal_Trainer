# 🏋️ Personal Trainer

> 🚧 Projeto em desenvolvimento.

Sistema completo para gerenciamento de **Personal Trainers** e seus alunos, desenvolvido com **Django**, **Django REST Framework**, **React Native (Expo)** e **MySQL**.

O objetivo é oferecer uma plataforma moderna para acompanhamento físico, permitindo que o Personal Trainer gerencie clientes, prescreva treinos e dietas, acompanhe avaliações físicas e monitore toda a evolução dos alunos através de um painel web e um aplicativo mobile.

---

# 📖 Sobre o Projeto

O **Personal Trainer** é uma plataforma composta por dois ambientes principais:

- 💻 **Painel Web** para o Personal Trainer
- 📱 **Aplicativo Mobile** para os alunos

A plataforma centraliza todas as informações do aluno em um único sistema, facilitando o gerenciamento de treinos, dietas, avaliações, exames, progresso físico e comunicação entre Personal Trainer e cliente.

---

# 🏗️ Arquitetura

O projeto é dividido em três módulos principais:

- 💻 **Backend (API REST)** desenvolvido em Django REST Framework
- 🌐 **Painel Web** para gerenciamento dos alunos
- 📱 **Aplicativo Mobile** desenvolvido em React Native (Expo)

Todos os módulos compartilham um banco de dados **MySQL**, garantindo sincronização das informações entre o painel administrativo e o aplicativo dos alunos.

---

# 🚀 Funcionalidades

## 💻 Painel Web (Personal Trainer)

- Dashboard
- Gestão de Clientes (CRM)
- Agenda
- Cadastro de Exercícios
- Biblioteca de Exercícios
- Biblioteca de Alimentos
- Biblioteca de Treinos
- Biblioteca de Cardápios
- Criação e gerenciamento de Treinos
- Criação e gerenciamento de Dietas
- Avaliações Físicas
- Anamnese
- Upload de Exames
- Histórico de Progresso
- Feedback dos alunos
- Notas privadas
- Configurações da conta
- Configuração da identidade visual

---

## 📱 Aplicativo do Aluno

- Login
- Dashboard
- Visualização de Treinos
- Execução de Treinos
- Logbook
- Dietas
- Registro de Peso
- Upload de Fotos
- Upload de Exames
- Responder Anamnese
- Envio de Feedback
- Agenda
- Perfil do usuário

---

# 🛠️ Tecnologias

## Backend

- Python
- Django
- Django REST Framework

## Frontend Web

- HTML5
- CSS3
- JavaScript

## Mobile

- React Native
- Expo

## Banco de Dados

- MySQL

## Ferramentas

- Git
- GitHub
- VS Code
- MySQL Workbench
- Draw.io
- Figma

---

# 🗄️ Banco de Dados

O banco de dados foi modelado em **MySQL**, seguindo uma arquitetura relacional para atender todos os requisitos da plataforma.

### Principais entidades

- Usuários
- Clientes
- Exercícios
- Alimentos
- Planos de Treino
- Splits
- Itens de Treino
- Logbook
- Planos de Dieta
- Refeições
- Itens da Dieta
- Avaliações Físicas
- Perguntas de Anamnese
- Respostas de Anamnese
- Fotos de Progresso
- Exames
- Feedbacks
- Agenda
- Notas do Personal

---

# 📋 Requisitos Funcionais

O sistema contempla os seguintes módulos:

- Gestão de Clientes
- Treinos
- Dietas
- Avaliações Físicas
- Anamnese
- Progresso
- Feedback
- Agenda
- Bibliotecas
- Exames
- Configurações

---

# 🔒 Requisitos Não Funcionais

- Interface responsiva
- Mobile First
- Navegação intuitiva
- Segurança utilizando autenticação
- Controle de acesso por perfil de usuário
- Persistência de dados em MySQL
- API REST
- Tempo médio de resposta inferior a 2 segundos
- Arquitetura escalável

---

# 📚 Documentação

Toda a documentação do projeto está disponível na pasta **Documentação/**.

Ela contém:

- 📄 Análise de Requisitos
- 🗄️ Modelo SQL
- 🧩 Diagrama Entidade-Relacionamento (DER)
- 🗺️ Diagrama Geral do Sistema
- 🎨 Wireframes
- 💾 Scripts do Banco de Dados

---

# 📂 Estrutura do Projeto

```
Personal_Trainer/
│
├── Backend/
│
├── Personal_Trainer_Mobile/
│
├── Banco/
│
├── Documentação/
│   ├── Wireframes/
│   ├── Diagramas/
│   ├── Modelo_SQL.pdf
│   ├── Analise_de_Requisitos.pdf
│   └── Scripts/
│
└── README.md
```

---

# 📌 Roadmap

- [x] Levantamento de requisitos
- [x] Modelagem do banco de dados
- [x] Wireframes
- [ ] Desenvolvimento da API REST
- [ ] Desenvolvimento do Painel Web
- [ ] Desenvolvimento do Aplicativo Mobile
- [ ] Testes
- [ ] Deploy
- [ ] Publicação da primeira versão

---

# 🎯 Objetivo

Desenvolver uma plataforma completa para gerenciamento de Personal Trainers e acompanhamento de alunos, centralizando treinos, dietas, avaliações, anamnese, exames e evolução física em um único ambiente.

---

# 📷 Preview

Em breve serão adicionadas imagens do sistema, telas do painel administrativo e do aplicativo mobile.

---

# 👨‍💻 Desenvolvedor

**Evandro Wagencknecht**

Desenvolvedor de Software

### Tecnologias

`Python` • `Django` • `Django REST Framework` • `React Native` • `Expo` • `JavaScript` • `HTML5` • `CSS3` • `MySQL` • `Git`

---

## ⭐ Status

Este projeto está em desenvolvimento e recebe melhorias contínuas, com foco na construção de uma plataforma completa para gestão de Personal Trainers e acompanhamento de alunos.
