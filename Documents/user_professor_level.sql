-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 04, 2022 at 08:12 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `e-exam`
--

-- --------------------------------------------------------

--
-- Table structure for table `user_professor_level`
--

CREATE TABLE `user_professor_level` (
  `id` bigint(20) NOT NULL,
  `level` varchar(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `professor_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_professor_level`
--

INSERT INTO `user_professor_level` (`id`, `level`, `created_at`, `professor_id`) VALUES
(1, 'S', '2022-05-04 17:18:13.275110', 20),
(2, 'F', '2022-05-04 17:18:39.983781', 20),
(3, 'T', '2022-05-04 17:18:55.031554', 20),
(4, 'T', '2022-05-04 17:19:06.954695', 13),
(5, 'S', '2022-05-04 17:19:11.025811', 13),
(6, 'F', '2022-05-04 17:19:17.084121', 78),
(7, 'S', '2022-05-04 17:19:20.888968', 78),
(8, 'T', '2022-05-04 17:19:24.973051', 1),
(9, 'F', '2022-05-04 17:19:29.072601', 10),
(10, 'S', '2022-05-04 17:19:34.030347', 10),
(11, 'T', '2022-05-04 17:19:38.412632', 10),
(12, 'S', '2022-05-04 18:03:42.658942', 98),
(13, 'F', '2022-05-04 18:03:46.636993', 98),
(14, 'T', '2022-05-04 18:04:10.429062', 98),
(15, 'S', '2022-05-04 18:04:16.879546', 25),
(16, 'F', '2022-05-04 18:04:21.669432', 25),
(17, 'T', '2022-05-04 18:04:29.077810', 23),
(18, 'F', '2022-05-04 18:04:34.227774', 23),
(19, 'F', '2022-05-04 18:04:43.867350', 29),
(20, 'T', '2022-05-04 18:04:50.250975', 6),
(21, 'T', '2022-05-04 18:04:56.635132', 61),
(22, 'S', '2022-05-04 18:05:00.019166', 22),
(23, 'F', '2022-05-04 18:05:04.568137', 95),
(24, 'S', '2022-05-04 18:05:16.411501', 95),
(25, 'T', '2022-05-04 18:05:42.877776', 4),
(26, 'S', '2022-05-04 18:08:02.981546', 68),
(27, 'F', '2022-05-04 18:08:08.762747', 22),
(28, 'T', '2022-05-04 18:08:13.358629', 15),
(29, 'F', '2022-05-04 18:08:20.559582', 7),
(30, 'F', '2022-05-04 18:08:31.610473', 31),
(31, 'T', '2022-05-04 18:08:36.369490', 31),
(32, 'F', '2022-05-04 18:08:41.984651', 88),
(33, 'S', '2022-05-04 18:08:46.168483', 88),
(34, 'T', '2022-05-04 18:08:54.303251', 88),
(35, 'T', '2022-05-04 18:08:59.839452', 52),
(36, 'F', '2022-05-04 18:09:04.518942', 96),
(37, 'S', '2022-05-04 18:09:10.470032', 47),
(38, 'F', '2022-05-04 18:09:20.210994', 47),
(39, 'T', '2022-05-04 18:09:33.727857', 96),
(40, 'F', '2022-05-04 18:09:46.533624', 52),
(41, 'S', '2022-05-04 18:09:58.241344', 52),
(42, 'F', '2022-05-04 18:10:05.316430', 65),
(43, 'S', '2022-05-04 18:10:09.503236', 66),
(44, 'T', '2022-05-04 18:10:31.768249', 63),
(45, 'F', '2022-05-04 18:10:36.558444', 76),
(46, 'T', '2022-05-04 18:10:42.170441', 34),
(47, 'S', '2022-05-04 18:10:48.839138', 34),
(48, 'F', '2022-05-04 18:10:55.164228', 51),
(49, 'F', '2022-05-04 18:10:59.789862', 61),
(50, 'T', '2022-05-04 18:11:06.346840', 91);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user_professor_level`
--
ALTER TABLE `user_professor_level`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_professor_level_professor_id_level_3539da02_uniq` (`professor_id`,`level`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `user_professor_level`
--
ALTER TABLE `user_professor_level`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `user_professor_level`
--
ALTER TABLE `user_professor_level`
  ADD CONSTRAINT `user_professor_level_professor_id_3ae55c51_fk_user_professor_id` FOREIGN KEY (`professor_id`) REFERENCES `user_professor` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
