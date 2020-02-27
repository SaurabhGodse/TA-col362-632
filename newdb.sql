--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.14
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: trainschedule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.trainschedule (
    train_id character varying,
    source character varying,
    destination character varying,
    distance integer,
    arrival_time time without time zone,
    departure_time time without time zone
);


ALTER TABLE public.trainschedule OWNER TO postgres;

--
-- Data for Name: trainschedule; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.trainschedule (train_id, source, destination, distance, arrival_time, departure_time) FROM stdin;
'11472'	Jabalpur	Indore	555	23:02:39	14:06:00
56434	Delhi	Bhopal	500	20:23:38	15:00:00
'22181'	Jabalpur	Nizzamuddin	906	21:29:35	07:45:00
'12328'	Dehradun	Howrah	1587	21:24:30	20:25:00
'12187'	Jabalpur	Mumbai	997	20:13:22	14:35:00
'12903'	Mumbai	Amritsar	1891	20:31:07	13:52:00
'12854'	Bhopal	Durg	894	23:33:33	12:00:00
'13010'	Dehradun	Howrah	1557	23:20:41	19:53:00
'12322'	Mumbai	Howrah	2176	14:00:43	10:43:00
56439	Itarsi	Jaipur	1900	20:33:06	08:00:00
56666	Itarsi	Mumbai	800	14:58:02	13:00:00
'12111'	Mumbai	Amravati	672	14:25:45	13:43:00
'12160'	Jabalpur	Amravati	726	18:02:32	08:38:00
'12289'	Mumbai	Nagpur	837	23:33:24	04:30:00
'19712'	Bhopal	Jaipur	790	13:31:07	12:28:00
'12869'	Mumbai	Howrah	1968	20:00:16	06:00:00
'59390'	Bhopal	Indore	263	20:06:09	18:55:00
'14114'	Dehradun	Allahabad	863	22:23:57	18:28:00
'12227'	Mumbai	Indore	829	22:28:41	04:20:00
'12197'	Bhopal	Gwalior	485	20:43:35	02:35:00
'58840'	Jabalpur	Nagpur	398	22:56:47	22:41:00
'12121'	Jabalpur	Nizzamuddin	909	09:16:49	09:15:00
'14042'	Dehradun	Delhi	339	17:54:51	16:47:00
'12453'	Ranchi	Delhi	1341	22:01:18	19:50:00
'12439'	Ranchi	Delhi	1305	19:33:08	15:29:00
'12825'	Ranchi	Delhi	1305	21:16:19	12:55:00
'12877'	Ranchi	Delhi	1341	12:35:02	05:57:00
'12206'	Dehradun	Delhi	305	22:51:49	19:25:00
'12952'	Delhi	Mumbai	1384	11:36:37	04:55:00
'12189'	Jabalpur	Nizzamuddin	961	16:38:42	16:28:00
'14631'	Dehradun	Amritsar	463	16:12:22	15:10:00
'14318'	Dehradun	Indore	1179	14:37:31	12:35:00
'12616'	Delhi	Chennai	2182	14:24:55	08:52:00
'12418'	Delhi	Allahabad	634	09:42:59	09:29:00
'12809'	Mumbai	Howrah	1968	21:02:42	16:20:00
'13026'	Bhopal	Howrah	1459	22:43:53	14:43:00
'12261'	Mumbai	Howrah	1968	07:07:39	03:05:00
'12191'	Delhi	Jabalpur	1038	19:35:12	18:32:00
'22210'	Delhi	Mumbai	1384	16:33:33	02:15:00
'11401'	Mumbai	Nagpur	1139	18:37:39	11:40:00
'12139'	Mumbai	Nagpur	891	23:58:09	22:38:00
'12953'	Mumbai	Nizzamuddin	1377	21:43:27	03:35:00
'11057'	Mumbai	Amritsar	2046	10:59:53	06:08:00
'12961'	Mumbai	Indore	829	23:13:28	16:52:00
'12622'	Delhi	Chennai	2182	18:38:52	03:48:00
'12239'	Mumbai	Jaipur	1159	22:42:39	21:35:00
'12955'	Mumbai	Jaipur	1159	14:15:08	06:19:00
'12276'	Delhi	Allahabad	634	23:41:29	03:50:00
'12916'	Delhi	Ahmedabad	933	18:22:56	13:32:00
'12958'	Delhi	Ahmedabad	934	05:10:19	04:44:00
'11272'	Bhopal	Itarsi	738	22:33:45	10:38:00
'12859'	Mumbai	Howrah	1968	12:38:18	04:25:00
'11447'	Jabalpur	Howrah	1152	20:59:41	12:28:00
71223	Bhopal	Hyderabad	667	06:00:00	01:00:00
71224	Ahmedabad	Chennai	644	14:00:50	08:30:00
71245	Chennai	Bhopal	567	22:30:50	15:22:00
87656	Durg	Hyderabad	777	12:00:55	05:33:00
'12452'	Delhi	Kanpur	440	22:55:00	21:05:00
56438	Kanpur	Mumbai	900	02:30:00	01:25:00
\.


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

