CREATE TABLE IF NOT EXISTS `mydb`.`Users` (
  `idUsers` INT NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(100) BINARY NOT NULL,
  `mail` VARCHAR(100) BINARY NOT NULL,
  `password` VARCHAR(100) BINARY NOT NULL,
  PRIMARY KEY (`idUsers`),
  UNIQUE INDEX `idUsers_UNIQUE` (`idUsers` ASC),
  UNIQUE INDEX `login_UNIQUE` (`login` ASC),
  UNIQUE INDEX `mail_UNIQUE` (`mail` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`friends`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`friends` (
  `idUsers1` INT NOT NULL,
  `idUsers2` INT NOT NULL,
  INDEX `fk_friends_Users_idx` (`idUsers1` ASC),
  INDEX `fk_friends_Users1_idx` (`idUsers2` ASC),
  PRIMARY KEY (`idUsers1`, `idUsers2`),
  CONSTRAINT `fk_friends_Users`
    FOREIGN KEY (`idUsers1`)
    REFERENCES `mydb`.`Users` (`idUsers`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_friends_Users1`
    FOREIGN KEY (`idUsers2`)
    REFERENCES `mydb`.`Users` (`idUsers`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Games`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Games` (
  `id` INT NOT NULL,
  `properties` VARCHAR(45) NULL,
  `host` INT NOT NULL,
  `start_data` DATE NULL DEFAULT now(),
  `end_date` DATE NULL,
  `path` VARCHAR(2000) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Games_Users1_idx` (`host` ASC),
  CONSTRAINT `fk_Games_Users1`
    FOREIGN KEY (`host`)
    REFERENCES `mydb`.`Users` (`idUsers`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Players`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Players` (
  `Users_idUsers` INT NOT NULL,
  `Games_id` INT NOT NULL,
  INDEX `fk_Players_Users1_idx` (`Users_idUsers` ASC),
  INDEX `fk_Players_Games1_idx` (`Games_id` ASC),
  PRIMARY KEY (`Users_idUsers`, `Games_id`),
  CONSTRAINT `fk_Players_Users1`
    FOREIGN KEY (`Users_idUsers`)
    REFERENCES `mydb`.`Users` (`idUsers`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Players_Games1`
    FOREIGN KEY (`Games_id`)
    REFERENCES `mydb`.`Games` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Riddle`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Riddle` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(2000) NULL,
  `answer` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`RiddlesInGame`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`RiddlesInGame` (
  `Riddle_id` INT NOT NULL,
  `Games_id` INT NOT NULL,
  INDEX `fk_RiddlesInGame_Riddle1_idx` (`Riddle_id` ASC),
  PRIMARY KEY (`Riddle_id`, `Games_id`),
  INDEX `fk_RiddlesInGame_Games1_idx` (`Games_id` ASC),
  CONSTRAINT `fk_RiddlesInGame_Riddle1`
    FOREIGN KEY (`Riddle_id`)
    REFERENCES `mydb`.`Riddle` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_RiddlesInGame_Games1`
    FOREIGN KEY (`Games_id`)
    REFERENCES `mydb`.`Games` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Game_Properties`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Game_Properties` (
  `privacy` INT NULL DEFAULT 0,
  `start_delay` INT NULL DEFAULT 60,
  `Games_id` INT NOT NULL,
  INDEX `fk_Game_Properties_Games1_idx` (`Games_id` ASC),
  PRIMARY KEY (`Games_id`),
  CONSTRAINT `fk_Game_Properties_Games1`
    FOREIGN KEY (`Games_id`)
    REFERENCES `mydb`.`Games` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
