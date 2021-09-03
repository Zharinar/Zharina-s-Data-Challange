#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 
from datetime import date
from datetime import timedelta


# In[18]:


Grades = pd.read_csv(r"Desktop/grades.csv")


# # DESCRIPTIVE STATS AND CLEANING THE DATA

# In[19]:


Grades.head(10)


# In[20]:


Grades.dropna(inplace=True)


# In[21]:


Grades.describe()


# # CREATING A GRAPH THAT SHOWS TIME BETWEEN INSPECTIONS

# In[22]:


Grades.info()


# In[23]:


## I am going to change 'RESULTDTTM' to DateTime.
Grades['RESULTDTTM']=pd.to_datetime(Grades['RESULTDTTM'], infer_datetime_format=True)
Grades.info()


# In[24]:


Grades['time_between_inspections'] = Grades.groupby('LICENSENO')['RESULTDTTM'].diff()


# In[25]:


Grades2 = pd.DataFrame(Grades, columns= ['LICENSENO','RESULTDTTM', 'time_between_inspections'])


# In[26]:


Grades2["time_between_inspections"] = Grades2["time_between_inspections"].dt.days


# In[27]:


pd.set_option('display.max_rows', None)


# In[28]:


Grades2.sort_values(by= ['LICENSENO', 'RESULTDTTM'])[:10]


# In[29]:


Grades2.info()


# In[30]:


#GRAPH THE NUMBER OF DAYS BETWEEN INSPECTIONS. 
#MOST RESTAURANT RE-INSPECTIONS HAPPEN WITHIN 200 DAYS OF THE FIRST INSPECTION
plt.hist(Grades2['time_between_inspections'], bins = 10);
plt.title('Date Gap')
plt.xlabel('Days between inspections')
plt.ylabel('Inspections')
plt.xlim((0,1000))


# # LOOKING MORE CLOSELY AT THE DATA TO FIND TRENDS

# In[31]:


Cat_grade = pd.DataFrame(Grades, columns=['DESCRIPT', 'GRADE', 'SCORE'])


# In[32]:


Cat_grade.head(10)


# In[33]:


Cat_grade.DESCRIPT.value_counts()
#EATING AND DRINKING HAD THE MOST INSPECTIONS


# In[34]:


#LOOK AT THE OVERALL SCORES PER CATEGORY. 
#FROM HIGHEST TO LOWEST: RETAIL FOOD MOBILE FOOD WALK ON, EATING AND DRINKING, EATING AND DRINKING W/TAKEOUT
fig, _ = plt.subplots()
fig.set_size_inches(15, 5)
sns.despine()
_ = sns.barplot(x=Cat_grade.DESCRIPT, y=Cat_grade.SCORE, palette='rocket')
plt.xlabel("Category")
plt.ylabel("Score")
plt.title("Scores by category")
plt.show(fig)


# In[35]:


#EATING AND DRINKING HAD THE LOWEST SCORES, WHEREAS RETAIL FOOD HAD THE HIGHEST SCORES


# In[36]:


#THE TOTAL SUM OF THE POINTS THE FOOD ESTABLISHMENT RECEIVED IN  VIOLATIONS.
#WE CAN SEE HERE THAT THE MAJORITY OF FOOD ESTABLISHMENTS RECEIVED VIOLATIONS UNDER 50 (THE MAJORITY WERE UNDER 25).
Grades['SUM_VIOLATIONS'].hist().plot()


# In[37]:


#GET THE RAW SCORES
#HERE WE CAN SEE THAT THE MAJORITY OF ESTABLISHMENTS ENDED UP GETTING A GOOD GRADE
#REMEMBER SCORE=100-SUM_VIOLATIONS
Grades['SCORE'].hist().plot()


# In[38]:


#LOOK AT THE DISTRIBUTION OF GRADES OVERALL
#THIS FURTHER CONFIRMS THAT THE MAJORITY OF ESTABLISHMENTS GOT A GRADE OF AN A
Grade_distribution = Grades.groupby('GRADE').size()
pd.DataFrame({'Count of restaurant grade totals':Grade_distribution.values}, index=Grade_distribution.index)


# In[39]:


#GROUP BY ESTABLISHMENT TYPE AND COUNT # IN EACH CATEGORY
#THEN SORT FROM HIGHEST # TO LOWEST AND CREATE A BAR GRAPH
#THERE ARE MORE EATING AND DRINKING ESTABLISHMENTS being inspected
temp = Grades.groupby('DESCRIPT').size()
description_distribution = pd.DataFrame({'Count':temp.values}, index=temp.index)
Grades['DESCRIPT'].hist().plot()


# In[40]:


#EATING AND DRINKING ESTABLISHMENTS GOT THE MOST NUMBER OF INSPECTIONS AND THEY ALSO HAVE THE LOWEST OVERALL SCORES
#FOLLOWED BY EATING AND DRINKING WITH TAKEOUT!


# In[41]:


#Grouping and performing count over each group
Establishments =  Grades.groupby('LICENSENO')['LICENSENO'].count()


# In[42]:


Establishments.describe()
#The max number of inspections for one establishment is 54
#The mean is 9.5
#The min is 1


# In[43]:


sns.relplot(x="LICENSENO", y="SCORE", data=Grades)


# # LOOKING AT DATA FOR ESTABLISHMENTS WITH A GRADE OF C

# In[44]:


Grade_C = Grades[(Grades['SCORE'] <= 80)]
Grade_C.head(5)


# In[45]:


Result_C = pd.DataFrame(Grade_C, columns=['RESULT', 'DESCRIPT'])
Result_C.head(5)


# In[46]:


Result_C.shape


# In[47]:


Descriptive_Results_C =  Result_C.groupby('RESULT')['RESULT'].count()
print(Descriptive_Results_C)


# In[48]:


#OF THE ESTABLISHMENTS THAT GOT A GRADE C, THE MAJORITY OF THEM FAILED(779/881) AND 47 OF THE RE-EXTENTIONS FAILED.
#43 OF THE ESTABLISHMENTS NEEDED A HEARING
#9 WERE TEMPORARILY SHUT DOWN BY ORDER OF HEALTH DEPARTMENT
Descriptive_Results_C.plot()


# In[49]:


Grade_B = Grades[(Grades['SCORE'] >= 81)
                        & (Grades['SCORE'] < 93)]
Grade_B.head(5)


# In[50]:


Result_B = pd.DataFrame(Grade_B, columns=['RESULT', 'DESCRIPT'])
Result_B.head(5)


# In[51]:


Descriptive_Results_B =  Result_B.groupby('RESULT')['RESULT'].count()
print(Descriptive_Results_B)


# In[52]:


Descriptive_Results_B.plot()


# In[53]:


Grade_A = Grades[(Grades['SCORE'] >= 94)]              
Grade_A.head(5)


# In[54]:


Result_A = pd.DataFrame(Grade_A, columns=['RESULT', 'DESCRIPT'])
Result_A.head(5)


# In[55]:


Descriptive_Results_A =  Result_A.groupby('RESULT')['RESULT'].count()
print(Descriptive_Results_A)


# In[56]:


Descriptive_Results_A.plot()


# # FILTERING FOR 2018

# In[57]:



Grades.info()


# In[58]:


Grades.shape


# In[60]:


Grades2018 = Grades.loc[(Grades['RESULTDTTM'] >= '2018-06-23')
                        & (Grades['RESULTDTTM'] < '2018-06-30')]
Grades2018.head(5)


# In[61]:


Grades_june2018 = pd.DataFrame(Grades2018, columns=['RESULTDTTM', 'SCORE'])
Grades_june2018.head(5)


# In[62]:


Grades2018.shape


# In[63]:


Grades_june2018 = pd.DataFrame(Grades2018, columns=['SCORE', 'SUM_VIOLATIONS'])


# In[64]:


#HERE, I TRIED TO MAKE A PLOT GRAPH USING THE DATA OF JUNE 2018 BY DAY. 
#THERE WERE A TOTAL OF 173 INSPECTIONS DURING THIS TIME FRAME.
#I TRIED TO HAVE THE X-AXIS ORDERED BY DATE, BUT COULD NOT FIGURE OUT HOW TO MAKE IT WORK.
#I WOULD HAVE LOOKED AT SEASONALITY AND TREND OVER SEVERAL YEARS BUT AN ERROR MESSAGE KEPT COMING UP SAYING THAT THE DATA WAS TOO LARGE.
Grades_june2018.plot()

