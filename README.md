# Couth App — Documentação de Modelagem (Fase 1).

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

### RNF1 — Usabilidade  
- **RNF1.1** O app do aluno deve permitir acesso aos treinos e dietas com no máximo **3 cliques**.  
- **RNF1.2** O painel administrativo deve possuir **navegação lateral fixa**.  
- **RNF1.3** O sistema deve adotar **design premium e humano**, alinhado a energia, performance e saúde.

### RNF2 — Responsividade  
- **RNF2.1** O painel administrativo deve ser **otimizado para desktop**.  
- **RNF2.2** O app do aluno deve ser desenvolvido em abordagem **mobile-first**.  
- **RNF2.3** A versão web do aluno deve ser **responsiva**.

### RNF3 — Performance  
- **RNF3.1** Páginas-chave (lista de clientes, visualização de treino e dieta) devem carregar em **menos de 2 segundos** em conexão 4G média.

### RNF4 — Segurança  
- **RNF4.1** Senhas devem ser armazenadas com **hash forte** (PBKDF2 ou Argon2 – padrão Django).  
- **RNF4.2** O sistema deve utilizar **JWT ou sessão segura** para autenticação.  
- **RNF4.3** Deve haver **controle de acesso por tipo de usuário**.

### RNF5 — Disponibilidade  
- **RNF5.1** O sistema deve garantir **99% de disponibilidade mensal** em produção.
 
### RNF6 — Persistência  
- **RNF6.1** Os dados devem ser persistidos em **MySQL**, conforme modelo definido.
 
### RNF7 — Integrações  
- **RNF7.1** Não serão realizadas **integrações externas na fase 1**.
 
### RNF8 — Conformidade Legal (LGPD)  
- **RNF8.1** O sistema deve solicitar **consentimento explícito** para dados sensíveis (saúde, fotos e exames).  
- **RNF8.2** Deve existir **trilha de auditoria** para acesso a dados sensíveis.

### RNF9 — Prazo  
- **RNF9.1** O lançamento do sistema deve ocorrer até **10/03/2026**.

---

## 4. Casos de Uso (UC) + Diagramas

### 4.1 Diagrama geral
Diagrama geral de casos de uso cobrindo Personal Trainer e Aluno, com módulos da fase 1.
<img width="600" height="1190" alt="Image" src="https://github.com/user-attachments/assets/5d46b8ee-b659-4eb6-9dc0-7eaa625c6d8a" />

---

### 4.2 Especificação textual de Casos de Uso (modelo)

Abaixo estão exemplos de especificação textual no padrão adotado para o projeto.

#### UC_Treino — Gerenciar Planos de Treino
- **Ator primário:** Personal Trainer  
- **Pré-condições:** PT autenticado; aluno existente.  
- **Fluxo principal:**  
  1 - PT abre perfil do aluno → aba Treinos.  
  2 - Clica em “Criar novo treino”.  
  3 - Informa nome, datas e observações gerais.  
  4 - Cria splits A/B/C…  
  5 - Adiciona exercícios da biblioteca e configura séries/reps/intervalo/etc.  
  6 - Reordena itens se necessário.  
  7 - Salva plano.  
- **Pós-condição:** plano disponível para o aluno.  
- **Exceções:** exercício inexistente na biblioteca → PT deve cadastrar antes.

#### UC_Logbook — Registrar Logbook
- **Ator primário:** Aluno  
- **Pré-condições:** aluno autenticado; treino ativo.  
- **Fluxo principal:**  
  1 - Aluno abre “Iniciar treino”.  
  2 - Para cada exercício registra carga e repetições.  
  3 - Finaliza treino e envia.  
- **Pós-condição:** registros aparecem para PT em “Logbook”.


---

## 5. Modelagem de dados vs. Django (mapeamento)

O modelo SQL do projeto está alinhado ao domínio. Em Django, a estrutura pré definida:

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
## 5.1 DER / Banco de Dados

![Image](https://github.com/user-attachments/assets/ad8153df-7d93-4e0b-bbb5-7a69c82f2cf7)

## O DER representa os módulos principais do sistema:

- Usuários e Clientes: cadastros e vínculo personal ↔ aluno

- Treinos: planos, splits, exercícios e logbook do aluno

- Dietas: planos alimentares, refeições, alimentos e checklist de consumo

- Anamnese: perguntas padrão, envios e respostas do aluno

- Acompanhamento e Gestão: avaliações físicas, progresso (peso/fotos), exames, agenda, feedbacks e notas do personal

O diagrama foi gerado no MySQL Workbench a partir do script SQL completo do schema.

---

## 6. Wireframes — (Falta Fazer)

### Wireframes mínimos por persona

#### Admin Web (Personal)
## Login
<img width="1536" height="1024" alt="Image" src="https://github.com/user-attachments/assets/9e51572f-4aed-493d-8f21-14ab04ac3cd9" />

## Dashboard  
![Image](https://github.com/user-attachments/assets/d278693b-313e-4876-8bd4-dbe8edb1bd15)

## Clientes (lista + filtros + botão novo)  
<img width="1919" height="815" alt="Image" src="https://github.com/user-attachments/assets/1ec30028-8815-40aa-8088-a73d54a3617b" />

## Perfil do cliente (abas): Progresso, Anamnese, Avaliações, Dietas, Treinos, Exames, Feedbacks, Logbook, Fotos, Notas  
<img width="1918" height="1022" alt="Image" src="https://github.com/user-attachments/assets/edcd30c6-cb94-42e8-bc49-4d429883fe26" />

## Bibliotecas: Exercícios, Treinos‑modelo, Alimentos, Cardápios‑modelo  


## Agenda  


## Configurações (builder de anamnese + conta)

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

1 -Fechar documentação de requisitos. OK
2 - Diagramas: casos de uso (geral + módulos), classes e sequência.  OK
3 - Wireframes no Figma (baixa fidelidade primeiro).  
4 - Protótipo navegável usando os HTMLs como base.  
5 - Implementação Django por módulos, priorizando:
   
    - CRM + Bibliotecas.
    - Treinos. 
    - Dieta.  
    - Anamnese.  
    - Logbook/Progresso.  
    - Agenda/Feedbacks.

---

