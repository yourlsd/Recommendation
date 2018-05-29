# Recommendation

############Input Data###########

Affinity data: pulled the algorithm output from Adobe, based on 'People viewed this, also viewed this'



Parent  and Popular data: 
Parent data was extracted from WP download 5-10: 
select all the records with template-article, excluding Parent ID=0.
Popular data was pulled from Adobe analytics. 
Using segment WordPress-article and see the Visits of pages.
Integrate the 'visits' column to Parent data. 
The integrated one is 'Parent and Popular' data.



Calculator:
Pulled from WP download 5-10, select all the records with template-calculator or title name ends with "calculator"/"calculators"

TO BE UPDATED.




############Algorithm###########

The article recommendation algorithm consists of 4 parts:

4 recomendations based on Affinity