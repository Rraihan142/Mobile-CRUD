-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 12, 2024 at 10:24 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `database_aplikasi`
--

-- --------------------------------------------------------

--
-- Table structure for table `pendaftaran`
--

CREATE TABLE `pendaftaran` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `tlp` varchar(15) DEFAULT NULL,
  `alamat` text DEFAULT NULL,
  `tgl_lahir` date DEFAULT NULL,
  `jekel` varchar(10) DEFAULT NULL,
  `hobi` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pendaftaran`
--

INSERT INTO `pendaftaran` (`id`, `nama`, `tlp`, `alamat`, `tgl_lahir`, `jekel`, `hobi`) VALUES
(2, 'Kodok Zuma', '081908229732', 'Kp. Rawa Pasung', '1999-12-08', 'Pria', 'Belajar'),
(3, 'kodok Zumi', '08190822932', 'Kebayoran Baru', '1999-12-14', 'Pria', 'Belajar'),
(4, 'Kdok', '0819', 'kebayorna', '2024-12-14', 'Pria', 'Belajar'),
(5, 'kodok zumba', '0819', 'Baru', '2024-12-21', 'Wanita', 'Belajar');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','konsumen') DEFAULT 'konsumen'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
(1, 'raihan', '$2b$12$9Oz3YCoopqPEtiBMs8mSwOf6zNYxF9/aKxbXITHdSx.tQab8nFBXu', 'konsumen'),
(3, 'raihan1', '$2b$12$VkuNGOteF5Ub/RgI4vcOXO2YoEtGfH549FgGfRtJJhEzn3qAW1Bjq', 'admin'),
(4, 'admin', '$2b$12$k2q7PB7x4bsM6fvDhkv7ruqqz2yvYqL8V7CGsBqaJQWR07IFxHQpC', 'admin'),
(5, 'kodok', '$2b$12$5lFpDdgwwdtI4TAmsQJirOoO4tEh1M6cJ1SXfKg60/TXpwpZzzoHa', 'konsumen');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `pendaftaran`
--
ALTER TABLE `pendaftaran`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `pendaftaran`
--
ALTER TABLE `pendaftaran`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
