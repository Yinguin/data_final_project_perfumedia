##### 1. Creating new database #####
CREATE DATABASE perfume;
USE perfume;


##### 2. Importing data from .csv file #####
# Use the table data import wizard

# Adding "perfume_id" as primary key to the table 
ALTER TABLE perfume_sql
ADD PRIMARY KEY (perfume_id);


##### 3. Checking if data was imported correctly #####
SELECT *
FROM perfume_sql;


##### 4. Checking the length of the data #####
SELECT COUNT(*)
FROM perfume_sql;
# n_rows = 2115


##### 5. Checking values in each column in the data #####

### brand: number of brands
SELECT COUNT(*)
FROM perfume_sql
GROUP BY brand;
# n_rows = 238

### name: number of names
SELECT COUNT(*)
FROM perfume_sql
GROUP BY name;
# n_rows = 1916

### category: unique values in category
SELECT DISTINCT category
FROM perfume_sql;
# Eau de Toilette, Eau de Parfum, Parfum, Eau de Cologne, Eau Fraiche

### gender: unique values in gender
SELECT DISTINCT gender
FROM perfume_sql;
# Men, Women, Unisex

### fragrance: unique values in frangrance
SELECT DISTINCT fragrance
FROM perfume_sql
ORDER BY fragrance ASC;
# aquatic, aromatic, citrusy, classic, exotic, floral, fresh, fruity, gourmand, green, leathery, oriental, powdery, spicy, sweet, woody

### notes: unique values in notes
WITH RECURSIVE numbers_cte AS (
	SELECT 1 AS n
	UNION ALL
	SELECT n + 1 FROM numbers_cte WHERE n < 15    ## the maximum number of words in a cell
)
SELECT COUNT(DISTINCT CONCAT(SUBSTRING_INDEX(SUBSTRING_INDEX(REGEXP_REPLACE(notes, '[[:space:]]+', ' '), ', ', numbers_cte.n), ', ', -1))) AS distinct_notes_count
FROM perfume_sql
CROSS JOIN numbers_cte
WHERE numbers_cte.n <= 1 + (LENGTH(notes) - LENGTH(REPLACE(notes, ', ', '')));
# 355

### cutomer_rating: lowest and highest rating
SELECT MIN(customer_rating)
FROM perfume_sql;
# 0

SELECT MAX(customer_rating)
FROM perfume_sql;
# 5

### review_count: lowest and highest number of reviews
SELECT MIN(review_count)
FROM perfume_sql;
# 0

SELECT MAX(review_count)
FROM perfume_sql;
# 2989


##### 6. Top 10 most frequently used notes #####
WITH RECURSIVE numbers_cte AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM numbers_cte WHERE n < 15 
)
SELECT word, COUNT(*) AS note_occurrences
FROM (
    SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(notes, ',', numbers_cte.n), ',', -1)) AS word
    FROM perfume_sql
    CROSS JOIN numbers_cte
    WHERE numbers_cte.n <= 1 + (LENGTH(notes) - LENGTH(REPLACE(notes, ',', '')))
) AS distinct_words_table
GROUP BY word
ORDER BY note_occurrences DESC
LIMIT 10;
# musk: 		967 
# jasmine:		757
# bergamot:		748
# patchouli:	683
# vanilla:		683
# rose:			656
# sandalwood:	637
# amber:		564
# cedar:		458
# pepper:		422


##### 7. Top 10 popular women's perfumes #####
SELECT brand, name, category
FROM (
    SELECT *
    FROM perfume_sql
    WHERE gender = 'Women'
    ORDER BY review_count DESC
) AS women_perfumes_top_10
LIMIT 10;
# 1. Yves Saint Laurent Libre Eau de Parfum
# 2. Armani My Way Eau de Parfum
# 3. Lancome Idole Eau de Parfum
# 4. Lancome La vie est belle Eau de Parfum
# 5. Armani Si	Eau de Parfum
# 6. Armani My Way Intense Eau de Parfum
# 7. Armani Si Passione Eau de Parfum
# 8. Prada	Paradoxe Eau de Parfum
# 9. Viktor & Rolf Flowerbomb Ruby Orchid Eau de Parfum
# 10. Armani di Gioia Ocean di Gioia Eau de Parfum


##### 8. Top 10 popular men's perfumes #####
SELECT brand, name, category
FROM (
    SELECT *
    FROM perfume_sql
    WHERE gender = 'Men'
    ORDER BY review_count DESC
) AS men_perfumes_top_10
LIMIT 10;
# 1. Armani	Code Homme Parfum
# 2. Yves Saint Laurent	L'Homme	Parfum
# 3. Armani	Acqua di Gio Homme Eau de Toilette
# 4. Jean Paul Gaultier	Le Male Eau de Toilette
# 5. Paco Rabanne 1 Million Eau de Toilette
# 6. Jil Sander	Sun Men	Eau de Toilette
# 7. Armani	Acqua di Gio Homme Eau de Parfum
# 8. Azzaro Wanted Eau de Parfum
# 9. Hugo Boss BOSS The Scent Eau de Toilette
# 10. DIOR Dior Homme Intense Eau de Parfum


##### 9. Top 10 popular unisex perfumes #####
SELECT brand, name, category
FROM (
    SELECT *
    FROM perfume_sql
    WHERE gender = 'Unisex'
    ORDER BY review_count DESC
) AS unisex_perfumes_top_10
LIMIT 10;
# 1. Calvin Klein CK Everyone Eau de Parfum
# 2. Calvin Klein ck one Eau de Toilette
# 3. Burberry Her Elixir Eau de Parfum
# 4. XERJOFF V-Collection Eau de Parfum
# 5. Montale Spices Arabians Tonka Eau de Parfum
# 6. XERJOFF 1861 Collection Naxos Eau de Parfum
# 7. Maison Margiela Replica Coffee Break Eau de Toilette
# 8. Montale	Oud Intense Cafe Eau de Parfum
# 9. Kilian Angels' Share Eau de Parfum
# 10. Tom Ford Signature Ombre Leather Eau de Parfum


##### 10. Top 10 popular Eau de Parfum #####
SELECT brand, name
FROM (
    SELECT *
    FROM perfume_sql
    WHERE category = 'Eau de Parfum'
    ORDER BY review_count DESC
) AS edp_perfumes_top_10
LIMIT 10;
# 1. Yves Saint Laurent	Libre
# 2. Armani	My Way
# 3. Lancome Idole
# 4. Lancome La vie est belle
# 5. Armani	Si
# 6. Armani My Way Intense
# 7. Armani Si Passione
# 8. Prada Paradoxe
# 9. Viktor & Rolf Flowerbomb Ruby Orchid
# 10. Armani di Gioia Ocean di Gioia


##### 11. Top 10 perfume brands #####
SELECT brand, COUNT(*) AS num_perfumes
FROM perfume_sql
GROUP BY brand
ORDER BY num_perfumes DESC
LIMIT 10;
# 1. Montale, 2. XERJOFF, 3. DIOR, 4.GUERLAIN, 5.Amouage, 6.Creed, 7.GIVENCHY, 8.Hugo Boss, 9.Eisenberg 10.BON PARFUMEUR


##### 12. Average customer rating of all perfumes #####
SELECT ROUND(AVG(customer_rating), 2) as avg_rating
FROM perfume_sql;
# 2.88


##### 13. Average price #####

## 13.1 Average price of all perfumes
SELECT ROUND(AVG(base_price), 2) AS avg_price
FROM perfume_sql;
# 1759.65

## 13.2 Average price of each category
SELECT category, ROUND(AVG(base_price), 2) AS avg_price
FROM perfume_sql
GROUP BY category
ORDER BY avg_price DESC;
# Parfum			4135.1
# Eau de Parfum		1860.23
# Eau Fraiche		 899.17
# Eau de Toilette	 871.77
# Eau de Cologne	 690.25

## 13.3 Average price of each gender
SELECT gender, ROUND(AVG(base_price), 2) AS avg_price
FROM perfume_sql
GROUP BY gender
ORDER BY avg_price DESC;
# Unisex	2458.28
# Women		1526.61
# Men		1285.79

## 13.4 Most expensive brand
SELECT brand, ROUND(AVG(base_price), 2) AS avg_price
FROM perfume_sql
GROUP BY brand
ORDER BY avg_price DESC
LIMIT 1;
# Clive Christian

## 13.5 Most expensive perfume
SELECT *
FROM perfume_sql
ORDER BY base_price DESC
LIMIT 1;
# XERJOFF K-Collection Elixir Parfum with base price 16000


##### 14. Addressing customer's interest in specific perfumes #####
SELECT *
FROM perfume_sql
WHERE
	brand = 'Prada'
		AND category = 'Eau de Parfum'
		AND gender = 'Women'
		AND fragrance = 'floral'
		AND base_price < 5000;
# 3 rows returned			

SELECT *
FROM perfume_sql
WHERE
    brand = 'DIOR'
    AND category = 'Eau de Parfum'
    AND (gender = 'Women' OR gender = 'Unisex')
    AND (fragrance = 'floral' OR fragrance = 'spicy' OR fragrance = 'woody')
    AND base_price < 3000;
# 10 rows returned
