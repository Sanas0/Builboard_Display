-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : lun. 21 fév. 2022 à 11:46
-- Version du serveur : 10.4.22-MariaDB
-- Version de PHP : 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `pi`
--

-- --------------------------------------------------------

--
-- Structure de la table `facturation`
--

CREATE TABLE `facturation` (
  `Id_Fact` int(25) NOT NULL,
  `Prix_Total` float NOT NULL,
  `Date_Fact` datetime NOT NULL,
  `Id_User` int(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `message`
--

CREATE TABLE `message` (
  `Id_Msg` int(25) NOT NULL,
  `Text_Msg` text NOT NULL,
  `Statut` int(25) NOT NULL,
  `Date_Msg` datetime NOT NULL,
  `Id_User` int(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `message`
--

INSERT INTO `message` (`Id_Msg`, `Text_Msg`, `Statut`, `Date_Msg`, `Id_User`) VALUES
(2, 'tttttttttttttttttttttttttttttttttt', 1, '2022-02-14 21:24:32', 5),
(3, 'ok its meee', 0, '2022-02-14 23:52:13', 4);

-- --------------------------------------------------------

--
-- Structure de la table `price_pub`
--

CREATE TABLE `price_pub` (
  `Id_Price` int(11) NOT NULL,
  `Days` int(11) NOT NULL,
  `Price` float NOT NULL,
  `Total` float NOT NULL,
  `Id_Pub` int(11) NOT NULL,
  `Pub_Name` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `price_pub`
--

INSERT INTO `price_pub` (`Id_Price`, `Days`, `Price`, `Total`, `Id_Pub`, `Pub_Name`) VALUES
(3, 3, 50875, 152625, 22, 'nutella.png'),
(4, 11, 13750, 151250, 23, 'voiture.png'),
(6, 68, 5000, 340000, 25, 'boi.png'),
(7, 9, 7791.67, 70125, 26, 'Vache.mp4'),
(8, 11, 12916.7, 142083, 27, 'Coca-Cola.mp4'),
(9, 2, 9166.67, 18333, 28, 'voiture.png');

-- --------------------------------------------------------

--
-- Structure de la table `pub`
--

CREATE TABLE `pub` (
  `Id_Pub` int(11) NOT NULL,
  `Duree` float NOT NULL,
  `Frequence` int(11) NOT NULL,
  `Date_Debut` datetime NOT NULL,
  `Date_Fin` datetime NOT NULL,
  `Prix` float NOT NULL,
  `Statut` int(11) NOT NULL,
  `File_Pub` text DEFAULT NULL,
  `Id_User` int(11) DEFAULT NULL,
  `Type` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `pub`
--

INSERT INTO `pub` (`Id_Pub`, `Duree`, `Frequence`, `Date_Debut`, `Date_Fin`, `Prix`, `Statut`, `File_Pub`, `Id_User`, `Type`) VALUES
(18, 15.8, 3, '2022-02-19 00:00:00', '2022-03-05 00:00:00', 1975, 1, 'mac.jpg', 4, 'image'),
(19, 17, 12, '2022-02-19 00:00:00', '2022-02-27 00:00:00', 8500, 0, 'Vache.mp4', 4, 'video'),
(22, 111, 11, '2022-02-16 00:00:00', '2022-02-19 00:00:00', 50875, 0, 'nutella.png', 4, 'image'),
(23, 30, 11, '2022-02-16 00:00:00', '2022-02-27 00:00:00', 13750, 1, 'voiture.png', 4, 'image'),
(25, 12, 10, '2022-02-20 00:00:00', '2022-04-29 00:00:00', 5000, 0, 'boi.png', 7, 'image'),
(26, 17, 11, '2022-02-16 00:00:00', '2022-02-25 00:00:00', 7791.67, 0, 'Vache.mp4', 7, 'video'),
(27, 31, 10, '2022-02-16 00:00:00', '2022-02-27 00:00:00', 12916.7, 0, 'Coca-Cola.mp4', 7, 'video'),
(28, 20, 11, '2022-02-24 00:00:00', '2022-02-26 00:00:00', 9166.67, 0, 'voiture.png', 7, 'image');

-- --------------------------------------------------------

--
-- Structure de la table `reclamation`
--

CREATE TABLE `reclamation` (
  `Id_Recl` int(25) NOT NULL,
  `Reponse` varchar(300) NOT NULL,
  `Date_Recl` datetime NOT NULL,
  `Id_Pub` int(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `reclamation`
--

INSERT INTO `reclamation` (`Id_Recl`, `Reponse`, `Date_Recl`, `Id_Pub`) VALUES
(3, ' Your claim has been accepted .', '2022-02-14 21:58:16', 18),
(4, 'Your claim is pending.', '2022-02-14 23:48:55', 19),
(7, 'Your claim is pending.', '2022-02-15 00:12:04', 22),
(8, ' Your claim has been accepted .', '2022-02-15 00:57:32', 23),
(10, 'Your claim is pending.', '2022-02-15 09:43:47', 25),
(11, 'Your claim is pending.', '2022-02-15 09:47:27', 26),
(12, 'Your claim is pending.', '2022-02-15 10:13:17', 27),
(13, 'Your claim is pending.', '2022-02-15 10:15:05', 28);

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

CREATE TABLE `user` (
  `Id_User` int(11) NOT NULL,
  `Nom` varchar(35) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Password` varchar(200) NOT NULL,
  `Type` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`Id_User`, `Nom`, `Email`, `Password`, `Type`) VALUES
(3, 'admin', 'admin@gmail.com', '$2b$12$5PngVdiXMpGvXgE7UYSR2.4WWSnPedKrl0wM5JgVBHGdCdXJdJJUm', 1),
(4, 'kenza', 'kenza.khalfallah@esprit.tn', '$2b$12$tZsLgbtzgc.5qUh2rUqzGeIzPzOfAAGXf57i.GMq3JjZr3Hc5X/UO', 0),
(5, 'tt', 't.t@gmail.com', '$2b$12$zY6iNE.Zs9JafoEilaF9f.ICmBgbw.gJzjc.ZMlT9UEemCHDq7koy', 0),
(6, 'hh', 'h.h@esprit.tn', '$2b$12$C4Hg9kjjHdHooABf68ubTuPw9bbG0zgmO8a5Xx0E3w21AjIq7R8Xq', 0),
(7, 'nour', 'nour.souidene@gmail.com', '$2b$12$rtfNps.Y2y1GG8pFRfgdLes3x8NCEVE2WnWpfoOHGtcoqqIGsW6vS', 0);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `facturation`
--
ALTER TABLE `facturation`
  ADD PRIMARY KEY (`Id_Fact`),
  ADD KEY `fk_User_Fact` (`Id_User`);

--
-- Index pour la table `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`Id_Msg`),
  ADD KEY `fk_User_Msg` (`Id_User`);

--
-- Index pour la table `price_pub`
--
ALTER TABLE `price_pub`
  ADD PRIMARY KEY (`Id_Price`),
  ADD KEY `fk_Pub_Price` (`Id_Pub`);

--
-- Index pour la table `pub`
--
ALTER TABLE `pub`
  ADD PRIMARY KEY (`Id_Pub`),
  ADD KEY `fk_User_Pub` (`Id_User`) USING BTREE;

--
-- Index pour la table `reclamation`
--
ALTER TABLE `reclamation`
  ADD PRIMARY KEY (`Id_Recl`),
  ADD KEY `fk_Pub_Recl` (`Id_Pub`);

--
-- Index pour la table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`Id_User`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `facturation`
--
ALTER TABLE `facturation`
  MODIFY `Id_Fact` int(25) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `message`
--
ALTER TABLE `message`
  MODIFY `Id_Msg` int(25) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `price_pub`
--
ALTER TABLE `price_pub`
  MODIFY `Id_Price` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT pour la table `pub`
--
ALTER TABLE `pub`
  MODIFY `Id_Pub` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT pour la table `reclamation`
--
ALTER TABLE `reclamation`
  MODIFY `Id_Recl` int(25) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT pour la table `user`
--
ALTER TABLE `user`
  MODIFY `Id_User` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `facturation`
--
ALTER TABLE `facturation`
  ADD CONSTRAINT `fk_User_Fact` FOREIGN KEY (`Id_User`) REFERENCES `user` (`Id_User`);

--
-- Contraintes pour la table `message`
--
ALTER TABLE `message`
  ADD CONSTRAINT `fk_User_Msg` FOREIGN KEY (`Id_User`) REFERENCES `user` (`Id_User`);

--
-- Contraintes pour la table `price_pub`
--
ALTER TABLE `price_pub`
  ADD CONSTRAINT `fk_Pub_Price` FOREIGN KEY (`Id_Pub`) REFERENCES `pub` (`Id_Pub`);

--
-- Contraintes pour la table `pub`
--
ALTER TABLE `pub`
  ADD CONSTRAINT `fk_User_Pub` FOREIGN KEY (`Id_User`) REFERENCES `user` (`Id_User`);

--
-- Contraintes pour la table `reclamation`
--
ALTER TABLE `reclamation`
  ADD CONSTRAINT `fk_Pub_Recl` FOREIGN KEY (`Id_Pub`) REFERENCES `pub` (`Id_Pub`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
