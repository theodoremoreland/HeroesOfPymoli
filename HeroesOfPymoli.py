#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

file_to_load = "resources/purchase_data.csv"

purchase_data = pd.read_csv(file_to_load)
purchase_data.head()


# Player Count

player_count = purchase_data.SN.nunique()
player_count


# Purchasing Analysis (Total)

item_num = purchase_data["Item ID"].nunique()
avg_price = purchase_data["Price"].mean()
total_purchases = purchase_data["Purchase ID"].count()
net = purchase_data["Price"].sum()
summary = pd.DataFrame({"Number of Items":[item_num],
                       "Average Price":[avg_price],
                       "Total Purchases":[total_purchases],
                       "Revenue":[net]})
summary


# Gender Demographics

males = purchase_data[purchase_data['Gender'].isin(['Male'])]
females = purchase_data[purchase_data['Gender'].isin(['Female'])]
others = purchase_data[purchase_data['Gender'].isin(["Other / Non-Disclosed"])]

male = males.SN.nunique()
female = females.SN.nunique()
other = others.SN.nunique()

gender_demo_raw = pd.DataFrame({"Gender":["Male", "Female", "Other / Non-Disclosed"],
                   "Purchase Count":[male, female, other],
                   "Percentage":[round(male/player_count*100, 2), round(female/player_count*100,2), round(other/player_count*100,2)]
                  })

gender_demo = gender_demo_raw.style.format({
    'var1': '{:,.2f}'.format,
    'var2': '{:,.2f}'.format,
    'var3': '{:,.2%}'.format,
})

gender_demo

# Purchasing Analysis (Gender)

genders = ["Male","Female","Other / Non-Disclosed"]
total_spent = [males["Price"].sum(), females["Price"].sum(), others["Price"].sum()]
avg_spent = [males["Price"].mean(), females["Price"].mean(), others["Price"].mean()]
avg_spent_per_person = [males["Price"].sum()/male, females["Price"].sum()/female, others["Price"].sum()/other]

gender_summary = pd.DataFrame({"Gender":genders,
    "Purchase Count":[males["Purchase ID"].count(), females["Purchase ID"].count(), others["Purchase ID"].count()],
                               "Average Spent":avg_spent,
                               "Total Spent":total_spent,
                               "Average Spent Per Person":avg_spent_per_person})
gender_summary


# Age Demographics


bins = [0,9,14,19,24,29,34,39,100]
labels = ["<10", "10-14","15-19","20-24","25-29","30-34","35-39","40+"]


purchase_data2 = purchase_data.copy(deep="True")
purchase_data3 = purchase_data2.drop_duplicates(subset="SN",keep="first")
purchase_data3["Age Group"] = pd.cut(purchase_data["Age"], bins, labels=labels)


age_group = purchase_data3.groupby("Age Group")
age = age_group["Age"].count()
age_per = age/player_count*100
age_group_pd = pd.DataFrame({"total":age,"per":age_per})
age_group_pd


# Purchasing Analysis (Age)


purchase_data4 = purchase_data.copy(deep="True")
purchase_data4["Age Group"] = pd.cut(purchase_data["Age"], bins, labels=labels)

age_group2 = purchase_data4.groupby("Age Group")

purchase_count2 = age_group2["Purchase ID"].count()
avg_spent2 = age_group2["Price"].mean()
total_spent2 = age_group2["Price"].sum()
avg_spent_per_person2 = total_spent2/age

age_summary = pd.DataFrame({"Purchase Count":purchase_count2,
                               "Average Spent":avg_spent2,
                               "Total Spent":total_spent2,
                               "Average Spent Per Person":avg_spent_per_person2})
age_summary


# Top Spenders

spenders = purchase_data.groupby("SN")

purchase_count = spenders["SN"].count()
avg_value = spenders["Price"].mean()
total_value = spenders["Price"].sum()

spenders_summary = pd.DataFrame({"Purchase Count":purchase_count,
                                "Average Purchase Price": avg_value,
                                "Total Purchase Value":total_value})


spenders_summary.sort_values(by="Total Purchase Value", ascending=False).head()


# Most Popular Items

items_df = purchase_data[["Item ID","Item Name", "Price"]].copy()
items = items_df.groupby(["Item ID","Item Name"])

num_sold = items["Item Name"].count()
price = items["Price"].max()
value_sold = items["Price"].sum()

items_summary = pd.DataFrame({"Purchase Count":num_sold,
                            "Item Price":price,
                             "Total Purchase Value":value_sold})
items_df
items_summary.sort_values(by="Purchase Count", ascending=False).head()


# Most Profitable Items

items_summary.sort_values(by="Total Purchase Value", ascending=False).head()

