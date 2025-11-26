# Couth App — Documentação de Modelagem (Fase 1)

Este repositório contém a documentação inicial do **Couth App**, uma plataforma para **Personal Trainers** gerenciarem alunos, treinos e dietas, enquanto os alunos acompanham e registram sua evolução.

---

## 1. Visão geral do sistema

**Objetivo:** plataforma para o **Personal Trainer** gerenciar alunos e prescrever treinos/dietas, enquanto o **Aluno** executa, registra e devolve progresso/feedback.

### Atores principais
- **Personal Trainer (Admin Web):** cria/gerencia conteúdo e alunos.
- **Aluno (App Mobile / Web responsivo):** consome planos e registra evolução.

### Módulos da Fase 1
- **Dashboard (admin)**
- **Agenda**
- **Clientes (CRM)**
- **Perfil do cliente (abas)**  
  - Progresso / Avaliações  
  - Anamnese  
  - Treinos  
  - Dietas  
  - Exames  
  - Feedbacks  
  - Logbook  
  - Fotos  
  - Notas
- **Bibliotecas**  
  - Exercícios  
  - Treinos‑modelo  
  - Alimentos  
  - Cardápios‑modelo
- **Configurações**  
  - Anamnese builder  
  - Conta  
  - Identidade visual
- **App aluno:** início, treinos, dieta, perfil, logbook, progresso, feedback.

---

## 2. Requisitos Funcionais (RF) — consolidados e detalhados

### RF1 — Gestão de Clientes (CRM)
- **RF1.1** Cadastrar aluno (nome, email, telefone, nascimento, plano e vencimento manual).  
- **RF1.2** Editar dados do aluno.  
- **RF1.3** Inativar/excluir aluno.  
- **RF1.4** Listar e filtrar por nome/email/status/dias restantes.  
- **RF1.5** Visualizar perfil individual com abas.

### RF2 — Anamnese
- **RF2.1** Personal cria/edita formulário padrão (perguntas, tipo, opções).  
- **RF2.2** Personal solicita novo preenchimento para um aluno.  
- **RF2.3** Aluno responde anamnese no app.  
- **RF2.4** Personal visualiza histórico de anamneses por aluno.

### RF3 — Periodização / Planos de Treino
- **RF3.1** Personal cria plano de treino com nome, vigência, observações gerais e cardio.  
- **RF3.2** Personal define splits (A/B/C…) por dia/grupo muscular.  
- **RF3.3** Personal adiciona exercícios aos splits a partir da biblioteca.  
- **RF3.4** Personal define séries, repetições, intervalo, técnicas, notas.  
- **RF3.5** Personal reordena splits e exercícios (drag/drop).  
- **RF3.6** Personal duplica plano/modelo para outro aluno.  
- **RF3.7** Aluno visualiza plano, splits e detalhes.

### RF4 — Planejamento de Dieta
- **RF4.1** Personal cria plano alimentar com vigência, ingestão hídrica, observações, prescrição extra.  
- **RF4.2** Personal define refeições (nome, horário).  
- **RF4.3** Personal adiciona alimentos por refeição a partir da biblioteca.  
- **RF4.4** Personal define quantidade/unidade.  
- **RF4.5** Sistema calcula macros totais (cálculo simples na fase 1).  
- **RF4.6** Personal duplica dieta para outro aluno.  
- **RF4.7** Aluno visualiza plano e marca consumo (checklist opcional).

### RF5 — Prescrição Suplementar / Protocolos
- **RF5.1** Personal inclui prescrição vinculada a um plano de dieta.  
- **RF5.2** Aluno visualiza prescrição dentro do plano alimentar.

### RF6 — Acompanhamento (Avaliações / Progresso)
- **RF6.1** Personal registra avaliações físicas (peso, % gordura, circunferências etc.).  
- **RF6.2** Aluno registra peso periódico.  
- **RF6.3** Aluno envia fotos (frente/costas/lado).  
- **RF6.4** Personal visualiza gráficos e histórico.

### RF7 — Exames / Documentos
- **RF7.1** Aluno envia exames (PDF/imagem) com data.  
- **RF7.2** Personal visualiza/download.

### RF8 — Comunicação / Feedback
- **RF8.1** Aluno envia feedback textual.  
- **RF8.2** Personal visualiza histórico e marca como lido.  
- **RF8.3** (Opcional fase 1) Chat simples.

### RF9 — Agenda
- **RF9.1** Personal cria/edita agendamentos com aluno.  
- **RF9.2** Personal vê calendário semanal/mensal consolidado.  
- **RF9.3** Aluno visualiza sua agenda.

### RF10 — Bibliotecas
- **RF10.1** CRUD “Meus Exercícios” (nome, categoria, vídeo, descrição).  
- **RF10.2** CRUD “Meus Treinos Modelo”.  
- **RF10.3** CRUD “Meus Alimentos” (macros).  
- **RF10.4** CRUD “Meus Cardápios Modelo”.

---

## 3. Requisitos Não Funcionais (RNF)

- **Usabilidade:**  
  - app aluno com no máximo **3 cliques** para acessar treinos/dietas;  
  - admin com navegação lateral fixa.
- **Design / Identidade:** visual premium/humano, energia/performance/saúde.
- **Responsividade:**  
  - admin otimizado para desktop;  
  - app aluno mobile‑first;  
  - web aluno responsiva.
- **Performance:** páginas‑chave (lista de clientes, treino/dieta) carregam em **< 2s** em 4G médio.
- **Segurança:**  
  - senhas com hash forte (Django PBKDF2/Argon2);  
  - JWT/Session segura;  
  - controle de acesso por tipo de usuário.
- **Disponibilidade:** 99% mensal em produção.
- **Persistência:** MySQL conforme modelo.
- **Integrações externas:** não previstas na fase 1.
- **Prazo macro:** lançamento em **10/03/2026**.
- **LGPD:** consentimento para dados sensíveis (saúde, fotos, exames) e trilha de auditoria de acesso.

---

## 4. Casos de Uso (UC) + Diagramas

### 4.1 Diagrama geral
Diagrama geral de casos de uso cobrindo Personal Trainer e Aluno, com módulos da fase 1.

### 4.2 Especificação textual de Casos de Uso (modelo)

Abaixo estão exemplos de especificação textual no padrão adotado para o projeto.

#### UC_Treino — Gerenciar Planos de Treino
- **Ator primário:** Personal Trainer  
- **Pré-condições:** PT autenticado; aluno existente.  
- **Fluxo principal:**  
  1. PT abre perfil do aluno → aba Treinos.  
  2. Clica em “Criar novo treino”.  
  3. Informa nome, datas e observações gerais.  
  4. Cria splits A/B/C…  
  5. Adiciona exercícios da biblioteca e configura séries/reps/intervalo/etc.  
  6. Reordena itens se necessário.  
  7. Salva plano.  
- **Pós-condição:** plano disponível para o aluno.  
- **Exceções:** exercício inexistente na biblioteca → PT deve cadastrar antes.

#### UC_Logbook — Registrar Logbook
- **Ator primário:** Aluno  
- **Pré-condições:** aluno autenticado; treino ativo.  
- **Fluxo principal:**  
  1. Aluno abre “Iniciar treino”.  
  2. Para cada exercício registra carga e repetições.  
  3. Finaliza treino e envia.  
- **Pós-condição:** registros aparecem para PT em “Logbook”.

> Se necessário, todas as especificações podem ser escritas no mesmo padrão.

---

## 5. Modelagem de dados vs. Django (mapeamento)

O modelo SQL do projeto está alinhado ao domínio. Em Django, a estrutura sugerida é:

- **accounts**
  - `User(AbstractUser)` com campo `tipo_usuario`
- **crm**
  - `Cliente` (FK para personal e FK para aluno/user)
- **library**
  - `Exercicio`, `Alimento`, `TreinoModelo`, `CardapioModelo`
- **workouts**
  - `PlanoTreino`, `SplitTreino`, `ItemTreino`, `LogbookAluno`
- **diet**
  - `PlanoDieta`, `Refeicao`, `ItemDieta`
- **anamnesis**
  - `PerguntaAnamnese`, `RespostaAnamnese`
- **progress**
  - `AvaliacaoFisica`, `FotoProgresso`, `ExameLaboratorial`
- **agenda**
  - `Agendamento`
- **feedback**
  - `Feedback`

**Observação importante:** `clientes.id_usuario_aluno` é **UNIQUE** (1:1 aluno ↔ cliente), adequado para controle de acesso.

---

## 6. Wireframes — (Falta Fazer)

### Onde fazer
- **Figma** (melhor custo/benefício e padrão do mercado).
- Alternativas: **Penpot** (open‑source) ou **Whimsical**.

### Wireframes mínimos por persona

#### Admin Web (Personal)
- Login  
- Dashboard  
- Clientes (lista + filtros + botão novo)  
- Perfil do cliente (abas): Progresso, Anamnese, Avaliações, Dietas, Treinos, Exames, Feedbacks, Logbook, Fotos, Notas  
- Bibliotecas: Exercícios, Treinos‑modelo, Alimentos, Cardápios‑modelo  
- Agenda  
- Configurações (builder de anamnese + conta)

#### App Aluno
- Login  
- Início (peso + pendências + mensagens)  
- Treinos (lista, split semanal, detalhe/iniciar, logbook)  
- Dieta (lista, detalhe, refeições do dia)  
- Perfil/Utilitários (exames, avaliações, fotos, anamneses, logout)

---

## 7. Frontend: HTML/CSS vs outra tecnologia

### Rota A — Django + Templates + HTMX/Alpine (rápida)
- Admin web com Django templates + Tailwind.  
- Interações dinâmicas com HTMX + Alpine.js.  
- Vantagem: entrega rápida, simples, sem SPA. Boa para fase 1.

### Rota B — Backend Django (API REST) + Front separado
- SPA para admin/aluno: React/Next ou Vue/Nuxt.  
- Mobile: Flutter ou React Native.  
- Vantagem: experiência mais “app‑like”.  
- Custo/tempo maior agora.

- Começar com **Rota A** (admin server‑rendered + Tailwind).  
O app aluno pode ser web responsivo nesta fase; migrar para mobile nativo na fase 2 se necessário.

---

## 8. Próximos passos

1. Fechar documentação de requisitos.  
2. Diagramas: casos de uso (geral + módulos), classes e sequência.  
3. Wireframes no Figma (baixa fidelidade primeiro).  
4. Protótipo navegável usando os HTMLs como base.  
5. Implementação Django por módulos, priorizando:
   1. CRM + Bibliotecas  
   2. Treinos  
   3. Dieta  
   4. Anamnese  
   5. Logbook/Progresso  
   6. Agenda/Feedbacks

---

