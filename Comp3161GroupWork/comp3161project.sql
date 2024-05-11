-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 11, 2024 at 03:04 AM
-- Server version: 8.2.0
-- PHP Version: 8.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `comp3161project`
--

-- --------------------------------------------------------

--
-- Table structure for table `calendar_events`
--

DROP TABLE IF EXISTS `calendar_events`;
CREATE TABLE IF NOT EXISTS `calendar_events` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `coursecode` varchar(21) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `coursecode` (`coursecode`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `calendar_events`
--

INSERT INTO `calendar_events` (`id`, `title`, `description`, `start_date`, `end_date`, `coursecode`) VALUES
(1, 'Exam', 'Exam', '2024-05-01 17:56:00', '2024-05-03 17:56:00', 'MATH1000');

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
CREATE TABLE IF NOT EXISTS `courses` (
  `coursecode` varchar(21) NOT NULL,
  `name` varchar(100) NOT NULL,
  `lecturer_id` int NOT NULL,
  PRIMARY KEY (`coursecode`),
  KEY `lecturer_id` (`lecturer_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`coursecode`, `name`, `lecturer_id`) VALUES
('COMP3161', 'DBMS', 1008),
('Math1000', 'Math', 1008);

-- --------------------------------------------------------

--
-- Table structure for table `course_enrolment`
--

DROP TABLE IF EXISTS `course_enrolment`;
CREATE TABLE IF NOT EXISTS `course_enrolment` (
  `student_id` varchar(100) NOT NULL,
  `course_title` varchar(100) NOT NULL,
  `coursecode` varchar(21) NOT NULL,
  PRIMARY KEY (`coursecode`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `course_enrolment`
--

INSERT INTO `course_enrolment` (`student_id`, `course_title`, `coursecode`) VALUES
('9', 'Math', 'Math1000'),
('9', 'DBMS', 'COMP3161');

-- --------------------------------------------------------

--
-- Table structure for table `forums`
--

DROP TABLE IF EXISTS `forums`;
CREATE TABLE IF NOT EXISTS `forums` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `coursecode` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `coursecode` (`coursecode`(250))
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `forums`
--

INSERT INTO `forums` (`id`, `title`, `description`, `coursecode`) VALUES
(1, 'Math Forum', 'About Math', ''),
(2, 'Math', 'Math forum', 'Math1000');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1009 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `firstname`, `lastname`, `password`, `gender`, `type`) VALUES
(2, 'Jon', 'Graj', 'JonGra', 'male', 'Student'),
(3, 'Jon', 'Graham', 'JonGra', 'male', 'Admin'),
(9, 'Jonny', 'Test', 'Jimmy1', 'male', 'Student'),
(99, 'John', 'Grayarm', 'JohGra', 'male', 'Student'),
(1008, 'Tony', 'Mataran', 'TonMat', 'male', 'Lecturer');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
