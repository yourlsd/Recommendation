# Article Recommendations

#-----------------------------------#
#            Input Data             #
#-----------------------------------#

Affinity data: pulled the algorithm output from Adobe, based on 'People viewed this, 
also viewed that'
Parent and Popular data: 
Parent data was extracted from WP download 5-10: 
select all the records with template-article, excluding Parent ID=0.
Popular data was pulled from Adobe analytics. 
Using segment WordPress-article and see the Visits of pages.
Integrate the 'visits' column to Parent data. 
The integrated one is 'Parent and Popular' data.

Calculator:
Pulled from WP download 5-10, select all the records with template-calculator or title name 
ends with "calculator".

TO BE UPDATED.


#-----------------------------------#
#         Data Preprocessing        #
#-----------------------------------#
WP-Download 5-10:
Filter: 1269 records left
Exclude Date =-42, Parent ID =0
_yoast_wpseo_meta-robots-noindex = blank
Template = template-article (except calculators)

Select Visits,id,Title,Parent,Parent Slug columns from WP-Download 5-10 and 
paste them to Parent and popylarity.

Specific calculators recommendation changed manually:
1. Rate table (WP id 3481) --> Mortgage rates (WP id 5299) 
2. ARM Payment Calculator( WP id 10996) --> Mortgage Payment Calculator (WP id 20357)
Note: it's only changed in Excel output this time. Manually 
3. Add Mortgage rates (WP id 5299) to calculators dataset
Note: it's only changed in Excel output checking this time. 



#-----------------------------------#
#            Algorithms             #
#-----------------------------------#

The article recommendation algorithm consists of 4 parts:

3 (or less) View Affinity, people viewed this, also viewed that. Also the recommended articles should 
exist in the Parent and Popularity dataset (extracted from WordPress).
If there’s not enough numbers of view affinity articles that meet the requirement, 
complement with content similarity recommendations. (eg. Can only find 1 article here, 
find the other 2 from content similarity recommendations) 

1 (or 0) Calculator under the same parent. If there’s no calculator of this parent, complement with 
content similarity recommendations.

3 (or more) content similarity, randomly select articles of the same parent but make sure it 
is widely spread – eg. Each article appears at least once. If there are not enough siblings, 
randomly select articles from secondary content similarity group.

----------------------------------------------------------------------------------
Secondary content similarity recommendations rules:
home --> home/mortgage
bankruptcy --> credit-repair
boat --> auto/powersport
debt-relief --> debt-consolidation
home/usda --> home/mortgage
home/usda/eligibility --> home/mortgage
others --> everything before the rightmost slash: eg. business/small --> business
----------------------------------------------------------------------------------

2 (or less) popular or high conversion articles under the same parent, currently it’s not integrated well, 
but it might be good to use LT revenue, RPV, form conversion as the metrics in the future. 
For now, use visits as the metric. In the future, can randomly select top 30% articles that 
convert well.

In version 1.0, select  
A total of 9 recommendations for every page with no replication. 


------------------------------------------------------------------------------------
Order of selecting:
In this version, we first select 3 recommended articles from Affinity dataset.
Then select 2 most popular articles of the same parent from parent and popular data set, 
excluding the articles we have selected from last step. 
Then randomly select 1 calculator of the same parent.
Finally, select 3 (or more) random article of the same parent from parent and popular data set, 
excluding the articles we have selected from last step.

The order of selecting would affect the recommendation output. So the order or priority of 
selecting different types of recommendations can be changed as needed.
------------------------------------------------------------------------------------