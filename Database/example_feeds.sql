-- Adminer 5.1.0 MariaDB 11.7.2-MariaDB-ubu2404 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

REPLACE INTO `feed` (`id`, `title`, `link`, `description`, `docs`, `generator`, `language`) VALUES
(1,	'CERT-FR',	'https://www.cert.ssi.gouv.fr/feed/',	'Centre gouvernemental de veille, d\'alerte et de réponse aux attaques informatiques.',	'http://www.rssboard.org/rss-specification',	'CERT-FR',	'fr-FR'),
(2,	'ZDI: Published Advisories',	'http://www.zerodayinitiative.com/rss/published/',	'The following is a list of publicly disclosed vulnerabilities discovered by Zero Day Initiative researchers. While the affected vendor is working on a patch for these vulnerabilities, Trend Micro customers are protected from exploitation by security filters delivered ahead of public disclosure. All security vulnerabilities that are acquired by the Zero Day Initiative are handled according to the ZDI Disclosure Policy. ',	NULL,	NULL,	'en'),
(3,	'ZDI: Upcoming Advisories',	'http://www.zerodayinitiative.com/rss/upcoming/',	'The following is a list of vulnerabilities discovered by Zero Day Initiative researchers that are yet to be publicly disclosed. The affected vendor has been contacted on the specified date and while they work on a patch for these vulnerabilities, Trend Micro customers are protected from exploitation by IPS filters delivered ahead of public disclosure. Once the affected vendor patches the vulnerability,. ',	NULL,	NULL,	'en');

-- 2025-04-12 17:55:09 UTC
