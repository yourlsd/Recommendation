# Article Recommendations 2,0
# Updated 7-10

#-----------------------------------#
#            Input Data             #
#-----------------------------------#

Affinity data: pulled the algorithm output from Adobe, based on 'People viewed this, 
also viewed that'
Parent and Performance data: 
Parent data was extracted from WP data dump: 
select all the records with template-article, excluding Parent ID=0.
Popular data was pulled from Adobe analytics. 
Using segment WordPress-article and see the Visits of pages. 
Integrate the 'score' column to Parent data. 
The integrated one is 'Parent and Performance' data.

Calculator:
Pulled from WP data dump, select all the records with template-calculator or title name 
ends with "calculator". Add rate tables on 7-10

TO BE UPDATED.


#-----------------------------------#
#         Data Preprocessing        #
#-----------------------------------#
WP-Download 7-10:
Filter: 
Exclude Date =-42, Parent ID =0
Select _yoast_wpseo_meta-robots-noindex = blank
Template = template-article (except calculators)
Exluding articles author=TENDAYI KAPFIDZE (in the future) 
Find articles with the same name but different article ID, keep only the redirected pages.
Excluding articles with "2015,2016,2017"  in title.

Select Visits,id,Title,Parent,Parent Slug columns from WP data dump and 
paste them to Parent and popylarity.

Specific calculators recommendation changed manually:
Delete ARM Payment Calculator( WP id 3481) 



#-----------------------------------#
#            Algorithms             #
#-----------------------------------#

The article recommendation algorithm consists of 4 parts:

3 (or less) View Affinity, people viewed this, also viewed that. Also the recommended articles should 
exist in the Parent and Performance dataset (extracted from WordPress).
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

2 (or less)  articles with good performance under the same parent. Performance data is pulled from Adobe Analytics: 
'Article pages' dashboard.
Performance score = 0.4* Visits + 0.3 Time Spent per visit + 0,3 * FormStart

In version 2.0, select  
A total of 9 recommendations for every page with no replication. 


------------------------------------------------------------------------------------
Order of selecting:
In this version, we first select 3 recommended articles from Affinity dataset.
Then select 2 most popular articles of the same parent from parent and popular data set, 
excluding the articles we have selected from last step. 
Then randomly select 1 calculator of the same parent.
Finally, select 3 (or more) random article of the same parent from parent and popular data set, 
excluding the articles we have selected from last step.

In order to keep the recommendations 'widely spread', for every step, we added a counter of 'Times of being recommended' to every article,
and in every step we would select those articles with the least recommended number as prorities.

The order of selecting would affect the recommendation output. So the order or priority of 
selecting different types of recommendations can be changed as needed.
------------------------------------------------------------------------------------