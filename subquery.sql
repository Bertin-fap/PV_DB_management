SELECT *
FROM PECVD
WHERE P1 >(SELECT AVG(P1) FROM PECVD)