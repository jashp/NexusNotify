SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE TABLE IF NOT EXISTS `emails` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `version` int(11) NOT NULL COMMENT '0 for 8gb, 1 for 16gb, 2 for bumper',
  `location` int(11) NOT NULL COMMENT '0 for us, 1 for canada',
  `sent` int(11) NOT NULL DEFAULT '0',
  `unsubscribe` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`,`location`,`version`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

