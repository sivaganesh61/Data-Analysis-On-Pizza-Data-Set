import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

a=pd.read_csv("C:/siva/data analysis/pizza_sales.csv")
print(f"This ts the pizza Data Set:\n{a}")
print()
print()
print("First 5 rows of data:\n",a.head(5))
print()
print()
print("last 5 rows of data:\n",a.tail(5))
print()
print()
print("The columns of the data set are:\n",a.columns)
print()
print()
print("No.of rows and columns are:\n",a.shape)
print()
print()
print("describing the data in data set is:\n",a.describe())
print()
print()
print("information of the data set is:\n",a.info)
print()
print()
print("Data types of columns in a data set:\n",a.dtypes)
print()
print()
#KEY PERFORMANCE IDICATORS(KPI'S):-

total_revenue=a['total_price'].sum()
print(f"The total revenue of pizzas are: {total_revenue}")
print()
print()
total_pizzas_sold=a['quantity'].sum()
print(f"The total pizzas sold are: {total_pizzas_sold}")
print()
print()
total_orders=a['order_id'].nunique()
print(f"The total pizza orders are: {total_orders}")
print()
print()
avg_order_value=(total_revenue/total_orders)
print(f"The average order value of pizzas are: {avg_order_value}")
print()
print()
pizza_avg_orders=total_pizzas_sold/total_orders
print(f"The average orders of pizzas are: {pizza_avg_orders}")
print()
print()
#INGREDIENT ANALYSIS
ingredients=(a['pizza_ingredients']
             .str.split(',')
             .explode()
             .str.strip()
             .value_counts()
             .reset_index()
             .rename(columns={'index':'counts','pizza_ingredients':"ingredients"}))
print("These are the types of ingridients used to make different pizzas:\n",ingredients.head(15))

#DAILY TREND - TOTAL ORDERS {VISUALIZATION}
a["order_date"]=pd.to_datetime(a["order_date"],dayfirst=True)
a['day_name'] = a['order_date'].dt.day_name()
weekday_order =["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
a['day_name'] = pd.Categorical(a['day_name'], categories=weekday_order, ordered=True)
orders_by_day = a.groupby('day_name', observed=False)['order_id'].nunique()
ax = orders_by_day.plot(kind='bar', figsize=(8,5), color='red', edgecolor='black')
plt.title("Total orders by Day of week")
plt.xlabel("Day of week")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
for i, val in enumerate(orders_by_day):
    plt.text(i, val + 20, str(val), ha='center', va='bottom',fontsize=9,fontweight='bold')
plt.tight_layout()
plt.show()

#DAILY TREND - Total Revenue
a["order_date"]=pd.to_datetime(a["order_date"],dayfirst=True)
a['day_name'] = a['order_date'].dt.day_name()
weekday_order =["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
a['day_name'] = pd.Categorical(a['day_name'], categories=weekday_order, ordered=True)
orders_by_day = a.groupby('day_name', observed=False)['total_price'].sum()
ax = orders_by_day.plot(kind='bar', figsize=(8,5), color='blue', edgecolor='black')
plt.title("Total Revenue by Day of week")
plt.xlabel("Day of week")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45)
for i, val in enumerate(orders_by_day):
    plt.text(i, val + 20, str(val), ha='center', va='bottom',fontsize=9,fontweight='bold')
plt.tight_layout()
plt.show()

#HOURLY TREND - Total Orders
a['order_time'] = pd.to_datetime(a['order_time'], format='%H:%M:%S')
a['order_hour'] = a['order_time'].dt.hour
orders_by_hour = a. groupby('order_hour', observed=False)['order_id'].nunique()
ax = orders_by_hour.plot(kind='bar', figsize=(10,5), color='green', edgecolor='black')
plt.title("Total orders by Hour of Day")
plt.xlabel("Hour of Day (24-Hour Format)")
plt.ylabel("Number of orders")
plt.xticks(rotation=0)
for i, val in enumerate(orders_by_hour):
    plt.text(i, val + 5, str(val), ha='center', va='bottom',fontsize=9, fontweight='bold')
plt.tight_layout()
plt.show()

#MONTHLY TREND - Total Orders
a['order_date'] = pd. to_datetime(a['order_date'], dayfirst=True)
a['month_name'] = a['order_date'].dt.month_name()
month_order =["January","February","March","April","May","June",
"July","August","September","october","November","December"]
a['mopth_name'] = pd.Categorical(a['month_name'], categories=month_order, ordered=True)
orders_by_month = a.groupby('month_name', observed=False)['order_id'].nunique()
plt.figure(figsize=(10,5))
plt.fill_between(orders_by_month.index, orders_by_month.values, color="orange", alpha=0.6)
plt.plot(orders_by_month.index, orders_by_month.values, color="black", linewidth=2, marker='o')
plt.title("Total orders by Month")
plt.xlabel("Month")
plt.ylabel("Number of orders")
plt.xticks(rotation=45)
for i, val in enumerate(orders_by_month):
      plt.text(i, val + 20, str(val), ha='center', va='bottom',fontsize=9,fontweight='bold')
plt.tight_layout()
plt.show()

# % of Sales by Category
category_sales =a.groupby('pizza_category')['total_price'].sum()
category_pct = category_sales / category_sales.sum()* 100
plt.figure(figsize=(7,7))
colors = plt.get_cmap('tab20').colors
plt.pie(category_pct, labels=category_pct.index, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops={'edgecolor':'black','width':0.4})
plt.title("Percentage of Sales by pizza Category")
plt.show()

# % sales by Pizza Size & Category
sales_pivot = a.pivot_table(index='pizza_category',
                            columns='pizza_size',
                            values='total_price',
                            aggfunc='sum',
                            fill_value=0
                            )
sales_pct = sales_pivot / sales_pivot.sum().sum()* 100
plt.figure(figsize=(10,6))
sns.heatmap(sales_pct, annot=True,fmt=".1f", cmap ="YlOrRd", linewidths=0.5)
plt.title("% of Sales by pizza Category and Size")
plt.xlabel("Pizza Size")
plt.ylabel("Pizza Category")
plt.show()

#Total Pizzas Sold by Pizza Category
pizzas_by_category = a.groupby('pizza_category')['quantity'].sum()
colors = list(plt.get_cmap('tab20').colors)
colors = colors[:len(pizzas_by_category)]
ax = pizzas_by_category.plot(kind='bar', figsize=(8,5), color=colors, edgecolor='black')
plt.title("Total pizzas Sold by pizza category")
plt.xlabel("Pizza Category")
plt.ylabel("Total Pizzas Sold")
plt.xticks(rotation=45)
for i, val in enumerate(pizzas_by_category):
    plt.text(i, val + 5, str(val), ha='center', va='bottom', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.show()

#Top 5 Best Selling Pizzas
pizzas_by_name = a.groupby('pizza_name')['quantity'].sum()
top5 = pizzas_by_name.sort_values(ascending=False).head(5)
ax = top5.plot(kind='bar', figsize=(8,5), color='violet', edgecolor='black')
plt.title("Top 5 Pizzas Sold")
plt.xlabel("Pizza Name")
plt.ylabel("Total Pizzas Sold")
plt.xticks(rotation=45)
for i, val in enumerate(top5):
    plt.text(i, val + 2, str(val), ha='center', va='bottom',fontsize=9, fontweight='bold')
plt.tight_layout()
plt.show()

#Top 5 Best Selling Pizzas - Toatal Orders
pizzas_by_name = a.groupby('pizza_name')['order_id'].nunique()
top5 = pizzas_by_name.sort_values(ascending=False).head(5)
ax = top5.plot(kind='bar', figsize=(8,5), color='yellow', edgecolor='black')
plt.title("Top 5 Pizzas Ordered")
plt.xlabel("Pizza Name")
plt.ylabel("Total Pizzas Sold")
plt.xticks(rotation=45)
for i, val in enumerate(top5):
    plt.text(i, val + 2, str(val), ha='center', va='bottom',fontsize=9, fontweight='bold')
plt.tight_layout()
plt.show()

#Top 5 Best Selling Pizzas - Toatal Sales
pizzas_by_name = a.groupby('pizza_name')['total_price'].sum()
top5 = pizzas_by_name.sort_values(ascending=False).head(5)
ax = top5.plot(kind='bar', figsize=(8,5), color='brown', edgecolor='black')
plt.title("Top 5 Pizzas Ordered")
plt.xlabel("Pizza Name")
plt.ylabel("Total Pizzas Sold")
plt.xticks(rotation=45)
for i, val in enumerate(top5):
    plt.text(i, val + 2, str(val), ha='center', va='bottom',fontsize=9, fontweight='bold')
plt.tight_layout()
plt.show()

#Bottom 5 Least Selling Pizzas
pizzas_by_name = a.groupby('pizza_name')['total_price'].sum()
bottom5 = pizzas_by_name. sort_values(ascending=True).head(5)
ax = bottom5.plot(kind='bar',figsize=(8,5), color='orange', edgecolor='black')
plt.title("Bottom 5 Pizzas Sold")
plt.xlabel("Pizza Name")
plt.ylabel("Total Pizzas Sold")
plt.xticks(rotation=45)
for i, val in enumerate(bottom5):
    plt.text(i,val + 2, str(val), ha='center',va='bottom',fontsize=9, fontweight='bold')
plt.tight_layout()
plt.show()
