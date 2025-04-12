-- Adminer 5.1.0 MariaDB 11.7.2-MariaDB-ubu2404 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;

SET NAMES utf8mb4;

CREATE DATABASE `opencvestats` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `opencvestats`;

DROP TABLE IF EXISTS `cve`;
CREATE TABLE `cve` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `link` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `guid` varchar(255) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  `type` tinyint(3) unsigned DEFAULT NULL,
  `feed` tinyint(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `guid` (`guid`),
  KEY `type` (`type`),
  KEY `feed` (`feed`),
  CONSTRAINT `cve_ibfk_1` FOREIGN KEY (`type`) REFERENCES `type_cve` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `cve_ibfk_2` FOREIGN KEY (`feed`) REFERENCES `feed` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='CVE Vulnerabilities';


DROP TABLE IF EXISTS `feed`;
CREATE TABLE `feed` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `link` varchar(255) NOT NULL,
  `description` varchar(512) DEFAULT NULL,
  `docs` varchar(255) DEFAULT NULL,
  `generator` varchar(255) DEFAULT NULL,
  `language` varchar(8) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='RSS Feeds';


DROP TABLE IF EXISTS `feed_history`;
CREATE TABLE `feed_history` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NOT NULL,
  `feed` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `feed` (`feed`),
  CONSTRAINT `feed_history_ibfk_1` FOREIGN KEY (`feed`) REFERENCES `feed` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='History of fetched feeds';


DROP TABLE IF EXISTS `type_cve`;
CREATE TABLE `type_cve` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='Type of vulnerabilities';


-- 2025-04-12 17:54:24 UTC
