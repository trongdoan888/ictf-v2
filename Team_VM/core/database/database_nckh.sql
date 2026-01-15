-- MySQL dump 10.13  Distrib 5.7.44, for Linux (x86_64)
--
-- Host: localhost    Database: ictf
-- ------------------------------------------------------
-- Server version	5.7.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `curr_team_service_state`
--

DROP TABLE IF EXISTS `curr_team_service_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `curr_team_service_state` (
  `tick_id` int(11) NOT NULL,
  `team_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `state` enum('up','notfunctional','down','untested') NOT NULL DEFAULT 'untested',
  PRIMARY KEY (`tick_id`,`team_id`,`service_id`),
  KEY `tick_id` (`tick_id`,`team_id`),
  KEY `team_id` (`team_id`,`service_id`),
  KEY `tick_id_2` (`tick_id`,`service_id`),
  KEY `tick_id_3` (`tick_id`),
  KEY `team_id_2` (`team_id`),
  KEY `service_id` (`service_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `curr_team_service_state`
--

LOCK TABLES `curr_team_service_state` WRITE;
/*!40000 ALTER TABLE `curr_team_service_state` DISABLE KEYS */;
/*!40000 ALTER TABLE `curr_team_service_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_uploads`
--

DROP TABLE IF EXISTS `dashboard_uploads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dashboard_uploads` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `valid` tinyint(1) DEFAULT '1',
  `archive` longblob NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_uploads`
--

LOCK TABLES `dashboard_uploads` WRITE;
/*!40000 ALTER TABLE `dashboard_uploads` DISABLE KEYS */;
/*!40000 ALTER TABLE `dashboard_uploads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flag_submissions`
--

DROP TABLE IF EXISTS `flag_submissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flag_submissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL,
  `flag` varchar(128) NOT NULL,
  `flag_id` int(11) DEFAULT NULL,
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tick_id` int(11) NOT NULL,
  `service_id` int(11) DEFAULT NULL,
  `result` enum('correct','incorrect','ownflag','placetoolow','alreadysubmitted','notactive') DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `team_id_4` (`team_id`,`flag`),
  KEY `team_id` (`team_id`,`tick_id`,`result`),
  KEY `team_id_2` (`team_id`,`tick_id`),
  KEY `tick_id` (`tick_id`,`result`),
  KEY `tick_id_2` (`tick_id`),
  KEY `service_id` (`service_id`),
  KEY `team_id_3` (`team_id`),
  KEY `flag_id` (`flag_id`),
  KEY `flag` (`flag`),
  KEY `result` (`result`),
  KEY `created_on` (`created_on`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flag_submissions`
--

LOCK TABLES `flag_submissions` WRITE;
/*!40000 ALTER TABLE `flag_submissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `flag_submissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flags`
--

DROP TABLE IF EXISTS `flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `flag` varchar(128) NOT NULL,
  `flag_id` varchar(128) DEFAULT NULL,
  `cookie` varchar(1024) DEFAULT NULL,
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tick_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `flag` (`flag`),
  KEY `tick_id` (`tick_id`),
  KEY `team_id` (`team_id`),
  KEY `service_id` (`service_id`),
  KEY `created_on` (`created_on`),
  KEY `team_id_2` (`team_id`,`service_id`),
  KEY `team_id_3` (`team_id`,`service_id`,`created_on`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flags`
--

LOCK TABLES `flags` WRITE;
/*!40000 ALTER TABLE `flags` DISABLE KEYS */;
/*!40000 ALTER TABLE `flags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game`
--

DROP TABLE IF EXISTS `game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game` (
  `id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game`
--

LOCK TABLES `game` WRITE;
/*!40000 ALTER TABLE `game` DISABLE KEYS */;
/*!40000 ALTER TABLE `game` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `games`
--

DROP TABLE IF EXISTS `games`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `games` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `state` varchar(50) DEFAULT 'RUNNING',
  `status` varchar(50) DEFAULT 'ACTIVE',
  `current_round` int(11) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `games`
--

LOCK TABLES `games` WRITE;
/*!40000 ALTER TABLE `games` DISABLE KEYS */;
INSERT INTO `games` VALUES (1,'ictf_2026','RUNNING','ACTIVE',1);
/*!40000 ALTER TABLE `games` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partial_scores`
--

DROP TABLE IF EXISTS `partial_scores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `partial_scores` (
  `tick_id` int(11) NOT NULL,
  `team_id` int(11) NOT NULL,
  `sla_points` float NOT NULL,
  `cumulative_timeliness_points` float NOT NULL,
  `cumulative_diversity_points` float NOT NULL,
  `leetness_points` float NOT NULL,
  PRIMARY KEY (`tick_id`,`team_id`),
  KEY `team_id` (`team_id`),
  KEY `tick_id` (`tick_id`,`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partial_scores`
--

LOCK TABLES `partial_scores` WRITE;
/*!40000 ALTER TABLE `partial_scores` DISABLE KEYS */;
/*!40000 ALTER TABLE `partial_scores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rounds`
--

DROP TABLE IF EXISTS `rounds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rounds` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  `start_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rounds`
--

LOCK TABLES `rounds` WRITE;
/*!40000 ALTER TABLE `rounds` DISABLE KEYS */;
INSERT INTO `rounds` VALUES (1,1,1,'2026-01-13 14:43:31');
/*!40000 ALTER TABLE `rounds` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `script_runs`
--

DROP TABLE IF EXISTS `script_runs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `script_runs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `script_id` int(11) NOT NULL,
  `against_team_id` int(11) NOT NULL,
  `output` text,
  `error` int(11) DEFAULT NULL,
  `error_message` text,
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tick_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tick_id` (`tick_id`),
  KEY `tick_id_2` (`tick_id`,`error`),
  KEY `script_id` (`script_id`),
  KEY `script_id_2` (`script_id`,`tick_id`,`against_team_id`),
  KEY `script_id_3` (`script_id`,`tick_id`),
  KEY `against_team_id` (`against_team_id`),
  KEY `script_id_4` (`script_id`,`error`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_runs`
--

LOCK TABLES `script_runs` WRITE;
/*!40000 ALTER TABLE `script_runs` DISABLE KEYS */;
/*!40000 ALTER TABLE `script_runs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `script_state`
--

DROP TABLE IF EXISTS `script_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `script_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `script_id` int(11) NOT NULL,
  `state` enum('enabled','disabled') NOT NULL DEFAULT 'disabled',
  `reason` text NOT NULL,
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tick_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tick_id` (`tick_id`),
  KEY `tick_id_2` (`tick_id`,`script_id`),
  KEY `script_id` (`script_id`,`state`),
  KEY `script_id_2` (`script_id`),
  KEY `state` (`state`),
  KEY `created_on` (`created_on`),
  KEY `created_on_2` (`created_on`,`state`),
  KEY `created_on_3` (`created_on`,`script_id`),
  KEY `created_on_4` (`created_on`,`script_id`,`state`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_state`
--

LOCK TABLES `script_state` WRITE;
/*!40000 ALTER TABLE `script_state` DISABLE KEYS */;
/*!40000 ALTER TABLE `script_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scripts`
--

DROP TABLE IF EXISTS `scripts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scripts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(256) DEFAULT NULL,
  `type` enum('exploit','benign','getflag','setflag') NOT NULL,
  `team_id` int(11) DEFAULT NULL,
  `service_id` int(11) NOT NULL,
  `upload_id` int(11) NOT NULL,
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `current_state` enum('enabled','disabled') NOT NULL DEFAULT 'enabled',
  PRIMARY KEY (`id`),
  KEY `current_state` (`current_state`),
  KEY `created_on` (`created_on`),
  KEY `team_id` (`team_id`),
  KEY `type` (`type`),
  KEY `service_id` (`service_id`),
  KEY `upload_id` (`upload_id`),
  KEY `service_id_2` (`service_id`,`current_state`),
  KEY `service_id_3` (`service_id`,`team_id`),
  KEY `service_id_4` (`service_id`,`team_id`,`current_state`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scripts`
--

LOCK TABLES `scripts` WRITE;
/*!40000 ALTER TABLE `scripts` DISABLE KEYS */;
INSERT INTO `scripts` VALUES (1,'test_script.py','benign',NULL,1,1,'2026-01-13 15:22:42','enabled');
/*!40000 ALTER TABLE `scripts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_state`
--

DROP TABLE IF EXISTS `service_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `service_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service_id` int(11) NOT NULL,
  `state` enum('enabled','disabled') NOT NULL DEFAULT 'disabled',
  `reason` text NOT NULL,
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tick_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `service_id` (`service_id`,`state`),
  KEY `service_id_2` (`service_id`),
  KEY `state` (`state`),
  KEY `tick_id` (`tick_id`),
  KEY `tick_id_2` (`tick_id`,`state`),
  KEY `created_on` (`created_on`),
  KEY `created_on_2` (`created_on`,`state`),
  KEY `service_id_3` (`service_id`,`created_on`),
  KEY `service_id_4` (`service_id`,`created_on`,`state`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_state`
--

LOCK TABLES `service_state` WRITE;
/*!40000 ALTER TABLE `service_state` DISABLE KEYS */;
/*!40000 ALTER TABLE `service_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `port` smallint(6) DEFAULT NULL,
  `description` text NOT NULL,
  `authors` varchar(2048) DEFAULT NULL,
  `flag_id_description` text NOT NULL,
  `team_id` int(11) NOT NULL,
  `upload_id` int(11) NOT NULL,
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `current_state` enum('enabled','disabled') NOT NULL DEFAULT 'enabled',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `current_state` (`current_state`),
  KEY `port` (`port`)
) ENGINE=InnoDB AUTO_INCREMENT=10001 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES (1,'web_service',80,'Dá»‹ch vá»¥ Web máº«u',NULL,'username_id',1,1,'2026-01-13 14:27:15','enabled');
/*!40000 ALTER TABLE `services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team_connectivity_log`
--

DROP TABLE IF EXISTS `team_connectivity_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team_connectivity_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL,
  `latency` double DEFAULT NULL,
  `packetloss` double NOT NULL DEFAULT '1',
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `team_id` (`team_id`),
  KEY `created_on` (`created_on`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team_connectivity_log`
--

LOCK TABLES `team_connectivity_log` WRITE;
/*!40000 ALTER TABLE `team_connectivity_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `team_connectivity_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team_metadata`
--

DROP TABLE IF EXISTS `team_metadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team_metadata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL,
  `team_metadata_label_id` int(11) NOT NULL,
  `content` varchar(1024) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `team_id_2` (`team_id`,`team_metadata_label_id`),
  KEY `team_id` (`team_id`),
  KEY `team_metadata_label_id` (`team_metadata_label_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team_metadata`
--

LOCK TABLES `team_metadata` WRITE;
/*!40000 ALTER TABLE `team_metadata` DISABLE KEYS */;
/*!40000 ALTER TABLE `team_metadata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team_metadata_labels`
--

DROP TABLE IF EXISTS `team_metadata_labels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team_metadata_labels` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label` varchar(128) NOT NULL,
  `description` varchar(1024) NOT NULL,
  `is_public` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `description` (`description`(512))
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team_metadata_labels`
--

LOCK TABLES `team_metadata_labels` WRITE;
/*!40000 ALTER TABLE `team_metadata_labels` DISABLE KEYS */;
/*!40000 ALTER TABLE `team_metadata_labels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team_score`
--

DROP TABLE IF EXISTS `team_score`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team_score` (
  `tick_id` int(11) NOT NULL,
  `team_id` int(11) NOT NULL,
  `service_points` double NOT NULL,
  `attack_points` double NOT NULL,
  `sla` double NOT NULL,
  `total_points` double NOT NULL,
  `num_valid_ticks` int(11) NOT NULL,
  PRIMARY KEY (`tick_id`,`team_id`),
  KEY `team_id` (`team_id`),
  KEY `tick_id` (`tick_id`),
  KEY `tick_id_2` (`tick_id`,`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team_score`
--

LOCK TABLES `team_score` WRITE;
/*!40000 ALTER TABLE `team_score` DISABLE KEYS */;
/*!40000 ALTER TABLE `team_score` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team_scripts_run_status`
--

DROP TABLE IF EXISTS `team_scripts_run_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team_scripts_run_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL,
  `tick_id` int(11) NOT NULL,
  `json_list_of_scripts_to_run` text NOT NULL,
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `tick_id` (`tick_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team_scripts_run_status`
--

LOCK TABLES `team_scripts_run_status` WRITE;
/*!40000 ALTER TABLE `team_scripts_run_status` DISABLE KEYS */;
/*!40000 ALTER TABLE `team_scripts_run_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team_service_state`
--

DROP TABLE IF EXISTS `team_service_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team_service_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `state` enum('up','notfunctional','down','untested') NOT NULL DEFAULT 'untested',
  `reason` text NOT NULL,
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tick_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tick_id` (`tick_id`),
  KEY `tick_id_2` (`tick_id`,`service_id`),
  KEY `team_id` (`team_id`,`service_id`),
  KEY `team_id_2` (`team_id`),
  KEY `state` (`state`),
  KEY `service_id` (`service_id`,`created_on`),
  KEY `team_id_3` (`team_id`,`service_id`,`created_on`),
  KEY `team_id_4` (`team_id`,`service_id`,`state`),
  KEY `team_id_5` (`team_id`,`service_id`,`created_on`,`state`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team_service_state`
--

LOCK TABLES `team_service_state` WRITE;
/*!40000 ALTER TABLE `team_service_state` DISABLE KEYS */;
/*!40000 ALTER TABLE `team_service_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team_vm_key`
--

DROP TABLE IF EXISTS `team_vm_key`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team_vm_key` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL,
  `ctf_key` varchar(2048) DEFAULT NULL,
  `root_key` varchar(2048) DEFAULT NULL,
  `ip` varchar(20) DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `team_id` (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team_vm_key`
--

LOCK TABLES `team_vm_key` WRITE;
/*!40000 ALTER TABLE `team_vm_key` DISABLE KEYS */;
/*!40000 ALTER TABLE `team_vm_key` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teams` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `logo` mediumblob,
  `url` varchar(256) DEFAULT NULL,
  `country` char(128) DEFAULT NULL,
  `email` varchar(256) NOT NULL,
  `password` varchar(256) NOT NULL,
  `validated` tinyint(1) DEFAULT '0',
  `academic_team` tinyint(1) DEFAULT '0',
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `flag_token` varchar(128) NOT NULL,
  `login_token` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `flag_token` (`flag_token`),
  UNIQUE KEY `login_token` (`login_token`),
  KEY `validated` (`validated`),
  KEY `password` (`password`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams`
--

LOCK TABLES `teams` WRITE;
/*!40000 ALTER TABLE `teams` DISABLE KEYS */;
INSERT INTO `teams` VALUES (1,'Team_Test',NULL,NULL,NULL,'red@ictf.local','e10adc3949ba59abbe56e057f20f883e',1,0,'2026-01-13 14:24:50','token_red_123','login_red_123'),(2,'BlueTeam',NULL,NULL,NULL,'blue@ictf.local','e10adc3949ba59abbe56e057f20f883e',1,0,'2026-01-13 14:24:50','token_blue_456','login_blue_456');
/*!40000 ALTER TABLE `teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tick_scores`
--

DROP TABLE IF EXISTS `tick_scores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tick_scores` (
  `tick_id` int(11) NOT NULL,
  `team_id` int(11) NOT NULL,
  `sla_points` float NOT NULL,
  `attack_points` float NOT NULL,
  `defense_points` float NOT NULL,
  `total_points` float NOT NULL,
  PRIMARY KEY (`tick_id`,`team_id`),
  KEY `team_id` (`team_id`),
  KEY `tick_id` (`tick_id`,`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tick_scores`
--

LOCK TABLES `tick_scores` WRITE;
/*!40000 ALTER TABLE `tick_scores` DISABLE KEYS */;
/*!40000 ALTER TABLE `tick_scores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tickets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL,
  `ts` varchar(256) DEFAULT NULL,
  `subject` varchar(256) DEFAULT NULL,
  `msg` mediumblob,
  `response` mediumblob,
  `done` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

LOCK TABLES `tickets` WRITE;
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticks`
--

DROP TABLE IF EXISTS `ticks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ticks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time_to_change` timestamp NULL DEFAULT NULL,
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `time_to_change` (`time_to_change`),
  KEY `created_on` (`created_on`),
  KEY `time_to_change_2` (`time_to_change`,`created_on`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticks`
--

LOCK TABLES `ticks` WRITE;
/*!40000 ALTER TABLE `ticks` DISABLE KEYS */;
/*!40000 ALTER TABLE `ticks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticks_configuration`
--

DROP TABLE IF EXISTS `ticks_configuration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ticks_configuration` (
  `name` varchar(128) NOT NULL,
  `value` int(11) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticks_configuration`
--

LOCK TABLES `ticks_configuration` WRITE;
/*!40000 ALTER TABLE `ticks_configuration` DISABLE KEYS */;
INSERT INTO `ticks_configuration` VALUES ('NUMBER_OF_BENIGN_SCRIPTS',2),('NUMBER_OF_EXPLOIT_SCRIPTS',0),('NUMBER_OF_GETFLAGS',1),('TICK_TIME_IN_SECONDS',200);
/*!40000 ALTER TABLE `ticks_configuration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uploads`
--

DROP TABLE IF EXISTS `uploads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `uploads` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `payload` longblob NOT NULL,
  `upload_type` enum('service','exploit') NOT NULL,
  `is_bundle` tinyint(1) NOT NULL,
  `service_id` int(11) DEFAULT NULL,
  `feedback` text,
  `state` enum('untested','working','notworking') NOT NULL DEFAULT 'untested',
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `team_id` (`team_id`),
  KEY `upload_type` (`upload_type`),
  KEY `created_on` (`created_on`),
  KEY `created_on_2` (`created_on`,`upload_type`),
  KEY `team_id_2` (`team_id`,`created_on`),
  KEY `team_id_3` (`team_id`,`created_on`,`upload_type`),
  KEY `team_id_4` (`team_id`,`created_on`,`upload_type`,`state`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uploads`
--

LOCK TABLES `uploads` WRITE;
/*!40000 ALTER TABLE `uploads` DISABLE KEYS */;
INSERT INTO `uploads` VALUES (1,1,'service_v1',_binary 'dummy_content','service',0,NULL,NULL,'working','2026-01-13 15:21:43');
/*!40000 ALTER TABLE `uploads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vote_services`
--

DROP TABLE IF EXISTS `vote_services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vote_services` (
  `team_id` int(11) NOT NULL,
  `service_1` int(11) NOT NULL,
  `service_2` int(11) NOT NULL,
  `service_3` int(11) NOT NULL,
  PRIMARY KEY (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote_services`
--

LOCK TABLES `vote_services` WRITE;
/*!40000 ALTER TABLE `vote_services` DISABLE KEYS */;
/*!40000 ALTER TABLE `vote_services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vpn_info`
--

DROP TABLE IF EXISTS `vpn_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vpn_info` (
  `team_id` int(11) NOT NULL,
  `vpn_config` text NOT NULL,
  PRIMARY KEY (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vpn_info`
--

LOCK TABLES `vpn_info` WRITE;
/*!40000 ALTER TABLE `vpn_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `vpn_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-13 17:38:28
