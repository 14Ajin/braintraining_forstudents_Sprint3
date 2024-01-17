-- --------------------------------------------------------
-- Hôte:                         127.0.0.1
-- Version du serveur:           8.0.34 - MySQL Community Server - GPL
-- SE du serveur:                Win64
-- HeidiSQL Version:             12.5.0.6696
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Listage des données de la table python_game_data.exercices : ~1 rows (environ)
DELETE FROM `exercices`;
INSERT INTO `exercices` (`id`, `Name`) VALUES
	(1, 'GEO01');

-- Listage des données de la table python_game_data.results : ~2 rows (environ)
DELETE FROM `results`;
INSERT INTO `results` (`id`, `Date_Hours`, `Duration`, `Number_of_try`, `Number_of_Sucess`, `fk_users_id`, `fk_exercice_id`) VALUES
	(1, '2024-01-17 21:49:28', '00:00:03', 1, 0, 2, 1),
	(2, '2024-01-17 21:49:48', '00:00:14', 4, 1, 3, 1);

-- Listage des données de la table python_game_data.users : ~3 rows (environ)
DELETE FROM `users`;
INSERT INTO `users` (`id`, `Nickname`, `Password`, `UserLevel`) VALUES
	(1, 'lzr', '173af653133d964edfc16cafe0aba33c8f500a07f3ba3f81943916910c257705', 0),
	(2, 'Gaston', '', 1),
	(3, 'Ajin', '', 1);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
