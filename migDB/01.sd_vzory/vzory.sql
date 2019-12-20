-- MySQL dump 10.13  Distrib 8.0.15, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: cogito
-- ------------------------------------------------------
-- Server version	8.0.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `sd_vzory`
--

DROP TABLE IF EXISTS `sd_vzory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `sd_vzory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `typ` varchar(20) NOT NULL,
  `rod` varchar(1) NOT NULL,
  `vzor` varchar(50) NOT NULL,
  `deklinacia` varchar(500) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=130 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sd_vzory`
--

LOCK TABLES `sd_vzory` WRITE;
/*!40000 ALTER TABLE `sd_vzory` DISABLE KEYS */;
INSERT INTO `sd_vzory` VALUES (1,'POD_M','M','vrchný','ý,ého,ému,ého,om,ým,í,ích,ím,ích,ích,ími'),(2,'POD_M','M','chlap',',a,ovi,a,ovi,om,i,ov,om,ov,och,mi'),(3,'POD_M','M','peržan',',a,ovi,a,ovi,om,i,ov,om,ov,och,mi'),(4,'POD_M','M','dedo','o,a,ovi,a,ovi,om,ovia,ov,om,ov,och,ami'),(5,'POD_M','M','feláh',',a,ovi,a,ovi,om,ovia,ov,om,ov,och,mi'),(6,'POD_M','M','botto','o,u,ovi,u,ovi,om,ovia,ov,om,ov,och,ami'),(7,'POD_M','M','hosť',',a,ovi,a,ovi,om,ia,í,om,í,och,ami'),(8,'POD_M','M','boh',',a,u,a,u,om,ovia,ov,om,ov,och,mi'),(9,'POD_M','M','mím',',a,ovi,a,ovi,om,ovia,ov,om,ov,och,ami'),(10,'POD_M','M','lovec',',a,ovi,a,ovi,om,i,ov,om,ov,och,ami'),(11,'POD_M','M','vodník',',a,ovi,a,ovi,om,i,ov,om,ov,och,mi'),(12,'POD_M','M','černoch',',a,ovi,a,ovi,om,i,ov,om,ov,och,mi'),(13,'POD_M','M','hrdina','a,u,ovi,u,ovi,om,ovia,ov,om,ov,och,ami'),(14,'POD_M','M','otec',',a,ovi,a,ovi,om,ovia,ov,om,ov,och,ami'),(15,'POD_M','M','turek',',a,ovi,a,ovi,om,i,ov,om,ov,och,ami'),(16,'POD_M','M','paris',',a,ovi,a,ovi,om,ovia,ov,om,ov,och,mi'),(17,'POD_M','M','aias',',a,ovi,a,ovi,om,ovia,ov,om,ov,och,mi'),(18,'POD_M','M','nero',',a,ovi,a,ovi,om,i,ov,om,ov,och,mi'),(19,'POD_M','M','anakreón',',a,ovi,a,ovi,om,i,ov,om,ov,och,mi'),(20,'POD_M','M','achilles',',a,ovi,a,ovi,om,ovia,ov,om,ov,och,mi'),(21,'POD_M','M','syzifos',',a,ovi,a,ovi,om,ovia,ov,om,ov,och,mi'),(22,'POD_M','M','anaxagoras',',a,ovi,a,ovi,om,ovia,ov,om,ov,och,mi'),(23,'POD_M','M','génius',',a,ovi,a,ovi,om,ovia,ov,om,ov,och,mi'),(24,'POD_M','M','pontifex',',a,ovi,a,ovi,om,ovia,ov,om,ov,och,mi'),(25,'POD_M','M','noe',',a,ovi,a,ovi,om,ovia,ov,om,ov,och,ami'),(26,'POD_M','M','futbalista','a,u,ovi,u,ovi,om,i,ov,om,ov,och,mi'),(27,'POD_M','M','bandita','a,u,ovi,u,ovi,om,i,ov,om,ov,och,mi'),(28,'POD_M','M','hume',',a,ovi,a,ovi,om,ovia,ov,om,ov,och,ami'),(29,'POD_M','M','cestujúci','i,eho,emu,eho,om,im,i,ích,ím,ích,ích,ími'),(30,'POD_M','M','dub',',a,u,,e,om,y,ov,om,y,och,mi'),(31,'POD_M','M','mak',',u,u,,u,om,y,ov,om,y,och,mi'),(32,'POD_M','M','med',',u,u,,e,om,y,ov,om,y,och,mi'),(33,'POD_M','M','svietnik',',a,u,,u,om,y,ov,om,y,och,mi'),(34,'POD_M','M','papier',',a,u,,i,om,e,ov,om,e,och,mi'),(35,'POD_M','M','model',',u,u,,u,om,y,ov,om,y,och,mi'),(36,'POD_M','M','strom',',u,u,,e,om,y,ov,om,y,och,mi'),(37,'POD_M','M','meter',',a,u,,i,om,e,ov,om,e,och,mi'),(38,'POD_M','M','hotel',',a,u,,e,om,y,ov,om,y,och,mi'),(39,'POD_M','M','rytmus',',u,u,,e,om,y,ov,om,y,och,mi'),(40,'POD_M','M','nónius',',a,u,,e,om,y,ov,om,y,och,mi'),(41,'POD_M','M','most',',a,u,,e,om,y,ov,om,y,och,mi'),(42,'POD_M','M','zlomok',',u,u,,u,om,y,ov,om,y,och,mi'),(43,'POD_M','M','šperk',',u,u,,u,om,y,ov,om,y,och,mi'),(44,'POD_M','M','ohníček',',a,u,,u,om,y,ov,om,y,och,mi'),(45,'POD_M','M','pojem',',u,u,,e,om,y,ov,om,y,och,mi'),(46,'POD_M','M','chrbát',',a,u,,e,om,y,ov,om,y,och,mi'),(47,'POD_M','M','chlieb',',a,u,,e,om,y,ov,om,y,och,mi'),(48,'POD_M','M','mráz',',u,u,,e,om,y,ov,om,y,och,mi'),(49,'POD_M','M','stôl',',a,u,,e,om,y,ov,om,y,och,mi'),(50,'POD_M','M','vietor',',a,u,,e,om,y,ov,om,y,och,mi'),(51,'POD_M','M','stroj',',a,u,,i,om,e,ov,om,e,och,mi'),(52,'POD_M','M','jeleň',',a,ovi,a,ovi,om,e,ov,om,e,och,mi'),(53,'POD_M','M','mravec',',a,ovi,a,ovi,om,e,ov,om,e,och,mi'),(54,'POD_M','M','čaj',',a,u,,i,om,e,ov,om,e,och,mi'),(55,'POD_M','M','veniec',',a,u,,i,om,e,ov,om,e,och,mi'),(56,'POD_M','M','dážď',',a,u,,i,om,e,ov,om,e,och,mi'),(57,'POD_M','M','had',',a,ovi,a,ovi,om,y,ov,om,y,och,mi'),(58,'POD_M','M','orol',',a,ovi,a,ovi,om,y,ov,om,y,och,mi'),(59,'POD_M','M','peniaz',',a,u,,i,om,e,ov,om,e,och,mi'),(60,'POD_M','M','plášť',',a,u,,i,om,e,ov,om,e,och,mi'),(61,'POD_M','M','deň',',a,u,,i,om,i,í,om,i,och,ami'),(62,'POD_M','M','kuli',',ho,mu,ho,m,m,ovia,ov,om,ov,och,ami'),(63,'POD_M','M','atašé',',,,,,,,,,,,'),(64,'POD_M','Z','žena','a,y,e,u,e,ou,y,,ám,y,ách,ami'),(65,'POD_M','Z','zora','a,y,y,e,e,ou,e,e,iam,e,e,ami'),(66,'POD_M','Z','matka','a,y,e,u,e,ou,y,,ám,y,ách,ami'),(67,'POD_M','Z','vojna','a,y,e,u,e,ou,y,,ám,y,ách,ami'),(68,'POD_M','Z','jamka','a,y,e,u,e,ou,y,,ám,y,ách,ami'),(69,'POD_M','Z','perla','a,y,e,u,e,ou,y,,ám,y,ách,ami'),(70,'POD_M','Z','kráska','a,y,e,u,e,ou,y,,am,y,ach,ami'),(71,'POD_M','Z','čarodejka','a,y,e,u,e,ou,y,,ám,y,ách,ami'),(72,'POD_M','Z','idea','a,y,e,u,i,ou,y,í,ám,y,ách,ami'),(73,'POD_M','Z','dáma','a,y,e,u,e,ou,y,,am,y,ach,ami'),(74,'POD_M','Z','úloha','a,y,e,u,e,ou,y,,ám,y,ách,ami'),(75,'POD_M','Z','izis',',y,e,u,e,ou,y,,ám,y,ách,ami'),(76,'POD_M','Z','ceres',',y,e,u,e,ou,y,,ám,y,ách,ami'),(77,'POD_M','Z','juno','a,y,e,u,e,ou,y,,am,y,ach,ami'),(78,'POD_M','Z','demeter','a,y,e,u,e,ou,y,,ám,y,ách,ami'),(79,'POD_M','Z','víchrica','a,e,i,u,i,ou,e,,iam,e,iach,ami'),(80,'POD_M','Z','ulica','a,e,i,u,i,ou,e,,iam,e,iach,ami'),(81,'POD_M','Z','funkcia','a,e,i,u,i,ou,e,í,ám,e,ách,ami'),(82,'POD_M','Z','sudkyňa','a,e,i,u,i,ou,e,,iam,e,iach,ami'),(83,'POD_M','Z','vládkyňa','a,e,i,u,i,ou,e,,iam,e,iach,ami'),(84,'POD_M','Z','čerešňa','a,e,i,u,i,ou,e,,iam,e,iach,ami'),(85,'POD_M','Z','lyža','a,e,i,u,i,ou,e,,iam,e,iach,ami'),(86,'POD_M','Z','vôňa','a,e,i,u,i,ou,e,í,am,e,ach,ami'),(87,'POD_M','Z','svieca','a,e,i,u,i,ou,e,,am,e,ach,ami'),(88,'POD_M','Z','dlaň',',e,i,,i,ou,e,í,iam,e,iach,ami'),(89,'POD_M','Z','myseľ',',e,i,,i,ou,e,í,iam,e,iach,ami'),(90,'POD_M','Z','báseň',',e,i,,i,ou,e,í,am,e,ach,ami'),(91,'POD_M','Z','koľaj',',e,i,,i,ou,e,í,am,e,ach,ami'),(92,'POD_M','Z','pani','i,ej,ej,iu,ej,ou,ie,í,iam,ie,iach,iami'),(93,'POD_M','Z','kráľovná','á,ej,ej,ú,ej,ou,é,,ám,é,ách,ami'),(94,'POD_M','Z','gazdiná','á,ej,ej,ú,ej,ou,é,,ám,é,ách,ami'),(95,'POD_M','Z','ženská','á,ej,ej,ú,ej,ou,é,ých,ým,é,ých,ými'),(96,'POD_M','Z','mať',',e,i,,i,ou,e,í,iam,e,iach,ami'),(97,'POD_M','Z','kosť',',i,i,,i,ou,i,í,iam,i,iach,ami'),(98,'POD_M','Z','cirkev',',i,i,,i,ou,i,í,iam,i,iach,ami'),(99,'POD_M','Z','kader',',e,i,,i,ou,e,í,ám,e,ách,ami'),(100,'POD_M','Z','labuť',',i,i,,i,ou,e,í,iam,e,iach,ami'),(101,'POD_M','Z','sapfo',',,,,,,,,,,,'),(102,'POD_M','S','mesto','o,a,u,o,e,om,á,,ám,á,ách,ami'),(103,'POD_M','S','mestečko','o,a,u,o,u,om,á,,ám,á,ách,ami'),(104,'POD_M','S','rádio','o,a,u,o,u,om,á,í,ám,á,ách,ami'),(105,'POD_M','S','jedlo','o,a,u,o,u,om,á,,ám,á,ách,ami'),(106,'POD_M','S','kráľovstvo','o,a,u,o,e,om,á,,ám,á,ách,ami'),(107,'POD_M','S','sklenárstvo','o,a,u,o,e,om,a,,am,a,ach,ami'),(108,'POD_M','S','slnko','o,a,u,o,u,om,á,,ám,á,ách,ami'),(109,'POD_M','S','krídlo','o,a,u,o,u,om,a,,am,a,ach,ami'),(110,'POD_M','S','rúcho','o,a,u,o,u,om,a,,am,a,ach,ami'),(111,'POD_M','S','miesto','o,a,u,o,u,om,a,,am,a,ach,ami'),(112,'POD_M','S','lýtko','o,a,u,o,u,om,a,,am,a,ach,ami'),(113,'POD_M','S','gesto','o,a,u,o,e,om,á,,ám,á,ách,ami'),(114,'POD_M','S','capriccio','o,a,u,o,u,om,á,í,ám,á,ách,ami'),(115,'POD_M','S','fórum',',a,u,,e,om,a,,am,a,ach,ami'),(116,'POD_M','S','múzeum',',a,u,,u,om,á,í,ám,á,ách,ami'),(117,'POD_M','S','srdce','e,a,u,e,i,om,ia,,iam,ia,iach,ami'),(118,'POD_M','S','riečište','e,a,u,e,i,om,ia,,iam,ia,iach,ami'),(119,'POD_M','S','drievce','e,a,u,e,i,om,ia,,iam,ia,iach,ami'),(120,'POD_M','S','líce','e,a,u,e,i,om,a,,am,a,ach,ami'),(121,'POD_M','S','citoslovce','e,a,u,e,i,om,ia,,iam,ia,iach,ami'),(122,'POD_M','S','more','e,a,u,e,i,om,ia,í,iam,ia,iach,iami'),(123,'POD_M','S','oje','e,a,u,e,i,om,e,í,am,e,ach,ami'),(124,'POD_M','S','vysvedčenie','ie,ia,iu,ie,í,ím,ia,í,iam,ia,iach,iami'),(125,'POD_M','S','dievča','a,a,u,a,i,om,á,,ám,á,ách,ami'),(126,'POD_M','S','mača','a,ťa,ťu,a,ti,ťom,ence,eniec,encom,ence,encoch,encami'),(127,'POD_M','S','kura','a,a,u,a,i,om,e,,om,e,och,ami'),(128,'POD_M','S','teľa','a,a,u,a,i,om,e,,om,e,och,ami'),(129,'POD_M','S','cestovné','é,ého,ému,é,on,ým,é,ých,ým,é,ých,ými');
/*!40000 ALTER TABLE `sd_vzory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-19 15:23:31
