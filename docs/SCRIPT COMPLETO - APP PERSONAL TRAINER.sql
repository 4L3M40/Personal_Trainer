-- -----------------------------------------------------
-- SCRIPT COMPLETO - APP PERSONAL TRAINER (FASE 1)
-- MySQL 8+ | InnoDB | UTF8MB4
-- -----------------------------------------------------

SET NAMES utf8mb4;
SET time_zone = '+00:00';

-- 0) Schema
CREATE SCHEMA IF NOT EXISTS `personal_trainer_db`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE `personal_trainer_db`;

-- -----------------------------------------------------
-- 1) usuarios
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id_usuario` INT(11) NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  `senha_hash` VARCHAR(255) NOT NULL,
  `tipo_usuario` ENUM('personal', 'aluno') NOT NULL,
  `ativo` TINYINT(1) NOT NULL DEFAULT 1,
  `data_cadastro` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- 2) clientes
-- (cliente vinculado a personal; login aluno opcional)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clientes` (
  `id_cliente` INT(11) NOT NULL AUTO_INCREMENT,
  `id_personal` INT(11) NOT NULL,
  `id_usuario_aluno` INT(11) NULL UNIQUE,
  `nome` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `plano_nome` VARCHAR(100) NULL COMMENT 'Nome do plano (manual, ex: Trimestral)',
  `data_vencimento` DATE NULL COMMENT 'Data de validade do plano (manual)',
  `status_cliente` ENUM('ativo', 'inativo', 'vencendo') NOT NULL DEFAULT 'ativo',
  `data_nascimento` DATE NULL,
  `telefone` VARCHAR(20) NULL,
  `observacoes` TEXT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id_cliente`),
  CONSTRAINT `fk_clientes_personal`
    FOREIGN KEY (`id_personal`) REFERENCES `usuarios`(`id_usuario`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_clientes_usuario_aluno`
    FOREIGN KEY (`id_usuario_aluno`) REFERENCES `usuarios`(`id_usuario`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_clientes_personal` ON `clientes`(`id_personal`);
CREATE INDEX `idx_clientes_email` ON `clientes`(`email`);

-- -----------------------------------------------------
-- 3) exercicios
-- (biblioteca do personal)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `exercicios` (
  `id_exercicio` INT(11) NOT NULL AUTO_INCREMENT,
  `id_personal` INT(11) NOT NULL,
  `nome` VARCHAR(255) NOT NULL,
  `categoria` VARCHAR(100) NULL COMMENT 'Ex: Peito, Mobilidade, Alongamento',
  `link_video` VARCHAR(255) NULL,
  `descricao` TEXT NULL,
  `ativo` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id_exercicio`),
  CONSTRAINT `fk_exercicios_personal`
    FOREIGN KEY (`id_personal`) REFERENCES `usuarios`(`id_usuario`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_exercicios_personal` ON `exercicios`(`id_personal`);

-- -----------------------------------------------------
-- 4) planos_treino
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `planos_treino` (
  `id_plano_treino` INT(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` INT(11) NOT NULL,
  `nome_plano` VARCHAR(255) NOT NULL,
  `data_inicio` DATE NOT NULL,
  `data_expiracao` DATE NULL,
  `observacoes` TEXT NULL COMMENT 'Observações gerais, periodização',
  `exercicio_aerobico` TEXT NULL COMMENT 'Instruções para o Cardio',
  `ativo` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id_plano_treino`),
  CONSTRAINT `fk_planos_treino_cliente`
    FOREIGN KEY (`id_cliente`) REFERENCES `clientes`(`id_cliente`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_planos_treino_cliente` ON `planos_treino`(`id_cliente`);

-- -----------------------------------------------------
-- 5) treinos_split
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `treinos_split` (
  `id_split` INT(11) NOT NULL AUTO_INCREMENT,
  `id_plano_treino` INT(11) NOT NULL,
  `nome_split` VARCHAR(50) NOT NULL COMMENT 'Ex: Treino A, Treino de Pernas',
  `dia_semana` ENUM('seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom') NULL,
  `ordem_split` INT(3) NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id_split`),
  CONSTRAINT `fk_split_plano`
    FOREIGN KEY (`id_plano_treino`) REFERENCES `planos_treino`(`id_plano_treino`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_split_plano` ON `treinos_split`(`id_plano_treino`);

-- -----------------------------------------------------
-- 6) itens_treino
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `itens_treino` (
  `id_item_treino` INT(11) NOT NULL AUTO_INCREMENT,
  `id_split` INT(11) NOT NULL,
  `id_exercicio` INT(11) NOT NULL,
  `series` VARCHAR(50) NOT NULL COMMENT 'Ex: 3x10, 4xFalha',
  `repeticoes` VARCHAR(50) NULL COMMENT 'Ex: 10-12, 15, Falha',
  `intervalo` VARCHAR(50) NULL COMMENT 'Ex: 60 segundos',
  `tecnicas` VARCHAR(120) NULL COMMENT 'Ex: drop set, rest pause',
  `carga_sugerida` VARCHAR(50) NULL,
  `ordem` INT(3) NOT NULL,
  `observacoes_item` VARCHAR(255) NULL COMMENT 'Observações específicas do item',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id_item_treino`),
  CONSTRAINT `fk_itens_split`
    FOREIGN KEY (`id_split`) REFERENCES `treinos_split`(`id_split`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_itens_exercicio`
    FOREIGN KEY (`id_exercicio`) REFERENCES `exercicios`(`id_exercicio`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_itens_split` ON `itens_treino`(`id_split`);
CREATE INDEX `idx_itens_exercicio` ON `itens_treino`(`id_exercicio`);

-- -----------------------------------------------------
-- 7) logbook_aluno
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `logbook_aluno` (
  `id_log` INT(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` INT(11) NOT NULL,
  `id_item_treino` INT(11) NOT NULL,
  `data_execucao` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `carga_realizada` DECIMAL(8,2) NULL,
  `repeticoes_realizadas` INT(3) NULL,
  `feedback_aluno` TEXT NULL,

  PRIMARY KEY (`id_log`),
  CONSTRAINT `fk_log_cliente`
    FOREIGN KEY (`id_cliente`) REFERENCES `clientes`(`id_cliente`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_log_item`
    FOREIGN KEY (`id_item_treino`) REFERENCES `itens_treino`(`id_item_treino`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_log_cliente` ON `logbook_aluno`(`id_cliente`);

-- -----------------------------------------------------
-- 8) alimentos
-- (biblioteca do personal)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alimentos` (
  `id_alimento` INT(11) NOT NULL AUTO_INCREMENT,
  `id_personal` INT(11) NOT NULL,
  `nome` VARCHAR(255) NOT NULL,
  `calorias_100g` DECIMAL(8,2) NULL,
  `proteina_100g` DECIMAL(8,2) NULL,
  `carboidrato_100g` DECIMAL(8,2) NULL,
  `gordura_100g` DECIMAL(8,2) NULL,
  `fibras_100g` DECIMAL(8,2) NULL,
  `ativo` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id_alimento`),
  CONSTRAINT `fk_alimentos_personal`
    FOREIGN KEY (`id_personal`) REFERENCES `usuarios`(`id_usuario`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_alimentos_personal` ON `alimentos`(`id_personal`);

-- -----------------------------------------------------
-- 9) planos_dieta
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `planos_dieta` (
  `id_plano_dieta` INT(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` INT(11) NOT NULL,
  `nome_plano` VARCHAR(255) NOT NULL,
  `data_inicio` DATE NOT NULL,
  `data_expiracao` DATE NULL,
  `ingestao_hidrica` VARCHAR(100) NULL,
  `observacoes` TEXT NULL,
  `prescricao_extra` TEXT NULL COMMENT 'Suplementos, Fitoterápicos, Protocolo hormonal',
  `checklist_consumo_ativo` TINYINT(1) NOT NULL DEFAULT 0,
  `ativo` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id_plano_dieta`),
  CONSTRAINT `fk_planos_dieta_cliente`
    FOREIGN KEY (`id_cliente`) REFERENCES `clientes`(`id_cliente`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_planos_dieta_cliente` ON `planos_dieta`(`id_cliente`);

-- -----------------------------------------------------
-- 10) refeicoes
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `refeicoes` (
  `id_refeicao` INT(11) NOT NULL AUTO_INCREMENT,
  `id_plano_dieta` INT(11) NOT NULL,
  `nome_refeicao` VARCHAR(100) NOT NULL COMMENT 'Ex: Café da Manhã',
  `horario_sugerido` TIME NULL,
  `ordem_refeicao` INT(3) NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id_refeicao`),
  CONSTRAINT `fk_refeicoes_plano`
    FOREIGN KEY (`id_plano_dieta`) REFERENCES `planos_dieta`(`id_plano_dieta`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_refeicoes_plano` ON `refeicoes`(`id_plano_dieta`);

-- -----------------------------------------------------
-- 11) itens_dieta
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `itens_dieta` (
  `id_item_dieta` INT(11) NOT NULL AUTO_INCREMENT,
  `id_refeicao` INT(11) NOT NULL,
  `id_alimento` INT(11) NOT NULL,
  `quantidade` DECIMAL(8,2) NOT NULL COMMENT 'Quantidade em g/ml',
  `unidade_medida` VARCHAR(10) NOT NULL COMMENT 'Ex: g, ml, un',
  `observacao_alimento` VARCHAR(255) NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id_item_dieta`),
  CONSTRAINT `fk_itens_dieta_refeicao`
    FOREIGN KEY (`id_refeicao`) REFERENCES `refeicoes`(`id_refeicao`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_itens_dieta_alimento`
    FOREIGN KEY (`id_alimento`) REFERENCES `alimentos`(`id_alimento`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_itens_dieta_refeicao` ON `itens_dieta`(`id_refeicao`);
CREATE INDEX `idx_itens_dieta_alimento` ON `itens_dieta`(`id_alimento`);

-- -----------------------------------------------------
-- 12) consumo_refeicao (checklist opcional)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `consumo_refeicao` (
  `id_consumo` INT(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` INT(11) NOT NULL,
  `id_item_dieta` INT(11) NOT NULL,
  `data_consumo` DATE NOT NULL,
  `consumido` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (`id_consumo`),
  CONSTRAINT `fk_consumo_cliente`
    FOREIGN KEY (`id_cliente`) REFERENCES `clientes`(`id_cliente`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_consumo_item`
    FOREIGN KEY (`id_item_dieta`) REFERENCES `itens_dieta`(`id_item_dieta`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_consumo_cliente_data` ON `consumo_refeicao`(`id_cliente`, `data_consumo`);

-- -----------------------------------------------------
-- 13) anamneses_perguntas
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `anamneses_perguntas` (
  `id_pergunta` INT(11) NOT NULL AUTO_INCREMENT,
  `id_personal` INT(11) NOT NULL,
  `texto_pergunta` TEXT NOT NULL,
  `tipo_resposta` ENUM('texto', 'numero', 'sim_nao', 'unica_escolha', 'multipla_escolha') NOT NULL,
  `opcoes` JSON NULL COMMENT 'Lista de opções JSON se aplicável',
  `ordem_pergunta` INT(3) NOT NULL DEFAULT 1,
  `ativa` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id_pergunta`),
  CONSTRAINT `fk_perguntas_personal`
    FOREIGN KEY (`id_personal`) REFERENCES `usuarios`(`id_usuario`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_perguntas_personal` ON `anamneses_perguntas`(`id_personal`);

-- -----------------------------------------------------
-- 14) anamnese_envios
-- (cada envio = uma “rodada” de anamnese)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `anamnese_envios` (
  `id_envio` INT(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` INT(11) NOT NULL,
  `id_personal` INT(11) NOT NULL,
  `data_solicitacao` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` ENUM('pendente', 'respondido', 'cancelado') NOT NULL DEFAULT 'pendente',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (`id_envio`),
  CONSTRAINT `fk_envios_cliente`
    FOREIGN KEY (`id_cliente`) REFERENCES `clientes`(`id_cliente`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_envios_personal`
    FOREIGN KEY (`id_personal`) REFERENCES `usuarios`(`id_usuario`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- 15) anamneses_respostas
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `anamneses_respostas` (
  `id_resposta` INT(11) NOT NULL AUTO_INCREMENT,
  `id_envio` INT(11) NOT NULL,
  `id_pergunta` INT(11) NOT NULL,
  `resposta_valor` TEXT NULL COMMENT 'Texto/valor da resposta',
  `data_preenchimento` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (`id_resposta`),
  CONSTRAINT `fk_respostas_envio`
    FOREIGN KEY (`id_envio`) REFERENCES `anamnese_envios`(`id_envio`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_respostas_pergunta`
    FOREIGN KEY (`id_pergunta`) REFERENCES `anamneses_perguntas`(`id_pergunta`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_respostas_envio` ON `anamneses_respostas`(`id_envio`);

-- -----------------------------------------------------
-- 16) avaliacoes_fisicas
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `avaliacoes_fisicas` (
  `id_avaliacao` INT(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` INT(11) NOT NULL,
  `data_avaliacao` DATE NOT NULL,
  `peso` DECIMAL(6,2) NULL,
  `altura` DECIMAL(4,2) NULL,
  `percentual_gordura` DECIMAL(5,2) NULL,
  `circ_braco` DECIMAL(6,2) NULL,
  `circ_peito` DECIMAL(6,2) NULL,
  `circ_cintura` DECIMAL(6,2) NULL,
  `circ_quadril` DECIMAL(6,2) NULL,
  `circ_coxa` DECIMAL(6,2) NULL,
  `circ_panturrilha` DECIMAL(6,2) NULL,
  `observacoes` TEXT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (`id_avaliacao`),
  CONSTRAINT `fk_avaliacoes_cliente`
    FOREIGN KEY (`id_cliente`) REFERENCES `clientes`(`id_cliente`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_avaliacoes_cliente` ON `avaliacoes_fisicas`(`id_cliente`);

-- -----------------------------------------------------
-- 17) progresso_peso
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `progresso_peso` (
  `id_peso` INT(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` INT(11) NOT NULL,
  `data_registro` DATE NOT NULL,
  `peso` DECIMAL(6,2) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (`id_peso`),
  CONSTRAINT `fk_progresso_peso_cliente`
    FOREIGN KEY (`id_cliente`) REFERENCES `clientes`(`id_cliente`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_peso_cliente_data` ON `progresso_peso`(`id_cliente`, `data_registro`);

-- -----------------------------------------------------
-- 18) progresso_fotos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `progresso_fotos` (
  `id_foto` INT(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` INT(11) NOT NULL,
  `data_upload` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `url_foto` VARCHAR(512) NOT NULL COMMENT 'URL da foto armazenada',
  `observacao` VARCHAR(255) NULL,
  `tipo_foto` ENUM('frente', 'costas', 'lado', 'outra') NULL,

  PRIMARY KEY (`id_foto`),
  CONSTRAINT `fk_fotos_cliente`
    FOREIGN KEY (`id_cliente`) REFERENCES `clientes`(`id_cliente`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- 19) exames_laboratoriais
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `exames_laboratoriais` (
  `id_exame` INT(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` INT(11) NOT NULL,
  `data_upload` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `nome_arquivo` VARCHAR(255) NOT NULL,
  `url_arquivo` VARCHAR(512) NOT NULL COMMENT 'URL do PDF/Imagem',
  `data_exame` DATE NULL,

  PRIMARY KEY (`id_exame`),
  CONSTRAINT `fk_exames_cliente`
    FOREIGN KEY (`id_cliente`) REFERENCES `clientes`(`id_cliente`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- 20) feedbacks
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feedbacks` (
  `id_feedback` INT(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` INT(11) NOT NULL,
  `data_envio` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `mensagem` TEXT NOT NULL,
  `lido_personal` BOOLEAN NOT NULL DEFAULT FALSE,

  PRIMARY KEY (`id_feedback`),
  CONSTRAINT `fk_feedbacks_cliente`
    FOREIGN KEY (`id_cliente`) REFERENCES `clientes`(`id_cliente`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- 21) agendamentos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agendamentos` (
  `id_agendamento` INT(11) NOT NULL AUTO_INCREMENT,
  `id_personal` INT(11) NOT NULL,
  `id_cliente` INT(11) NOT NULL,
  `titulo` VARCHAR(255) NOT NULL,
  `data_hora_inicio` DATETIME NOT NULL,
  `data_hora_fim` DATETIME NULL,
  `observacoes` TEXT NULL,
  `status` ENUM('ativo','cancelado') NOT NULL DEFAULT 'ativo',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id_agendamento`),
  CONSTRAINT `fk_agenda_personal`
    FOREIGN KEY (`id_personal`) REFERENCES `usuarios`(`id_usuario`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_agenda_cliente`
    FOREIGN KEY (`id_cliente`) REFERENCES `clientes`(`id_cliente`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_agenda_personal` ON `agendamentos`(`id_personal`);
CREATE INDEX `idx_agenda_cliente` ON `agendamentos`(`id_cliente`);

-- -----------------------------------------------------
-- 22) notas_personal
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `notas_personal` (
  `id_nota` INT(11) NOT NULL AUTO_INCREMENT,
  `id_personal` INT(11) NOT NULL,
  `id_cliente` INT(11) NOT NULL,
  `data_nota` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `conteudo` TEXT NOT NULL,

  PRIMARY KEY (`id_nota`),
  CONSTRAINT `fk_notas_personal`
    FOREIGN KEY (`id_personal`) REFERENCES `usuarios`(`id_usuario`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_notas_cliente`
    FOREIGN KEY (`id_cliente`) REFERENCES `clientes`(`id_cliente`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX `idx_notas_personal` ON `notas_personal`(`id_personal`);
CREATE INDEX `idx_notas_cliente` ON `notas_personal`(`id_cliente`);

 