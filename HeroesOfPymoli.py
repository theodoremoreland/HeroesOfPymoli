#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd

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
                       
print("-----------------------------------------------------------")
print(summary)


# Gender Demographics

males = purchase_data[purchase_data['Gender'].isin(['Male'])]
females = purchase_data[purchase_data['Gender'].isin(['Female'])]
others = purchase_data[purchase_data['Gender'].isin(["Other / Non-Disclosed"])]

# Returns the number of unique occurrences
male = males.SN.nunique()
female = females.SN.nunique()
other = others.SN.nunique()

gender_demographics = pd.DataFrame({"Gender":["Male", "Female", "Other / Non-Disclosed"],
                   "Purchase Count":[male, female, other],
                   "Percentage":[round(male/player_count*100, 2), round(female/player_count*100,2), round(other/player_count*100,2)]
                  })


print("-----------------------------------------------------------")
print(gender_demographics)

# Purchasing Analysis (Gender)


genders = ["Male","Female","Other / Non-Disclosed"]
total_spent_per_gender = [males["Price"].sum(), females["Price"].sum(), others["Price"].sum()]
avg_spent_per_gender = [males["Price"].mean(), females["Price"].mean(), others["Price"].mean()]
avg_spent_per_person_per_gender = [males["Price"].sum()/male, females["Price"].sum()/female, others["Price"].sum()/other]

purchase_summary_by_gender = pd.DataFrame({"Gender":genders,
    "Purchase Count":[males["Purchase ID"].count(), females["Purchase ID"].count(), others["Purchase ID"].count()],
                               "Average Spent":avg_spent_per_gender,
                               "Total Spent":total_spent_per_gender,
                               "Average Spent Per Person":avg_spent_per_person_per_gender})
                               
print("-----------------------------------------------------------")
print(purchase_summary_by_gender)


# Age Demographics

bins = [0,9,14,19,24,29,34,39,100]
labels = ["<10", "10-14","15-19","20-24","25-29","30-34","35-39","40+"]

purchase_data_copy = purchase_data.copy(deep="True")
purchase_data_copy.drop_duplicates(subset="SN",keep="first", inplace=True)
purchase_data_copy["Age Group"] = pd.cut(purchase_data["Age"], bins, labels=labels)
age_groups = purchase_data_copy.groupby("Age Group")


player_count_by_age = age_groups["Age"].count()
player_count_by_age_per_100 = player_count_by_age/player_count*100

age_group_df = pd.DataFrame({"Player Count":player_count_by_age,"Percentage":player_count_by_age_per_100})

print("-----------------------------------------------------------")
print(age_group_df)


# Purchasing Analysis (Age)

purchase_data_copy = purchase_data.copy(deep="True")
purchase_data_copy["Age Group"] = pd.cut(purchase_data["Age"], bins, labels=labels)
age_groups = purchase_data_copy.groupby("Age Group")

purchase_count_by_age = age_groups["Purchase ID"].count()
avg_spent_by_age = age_groups["Price"].mean()
total_spent_by_age = age_groups["Price"].sum()
avg_spent_per_person = total_spent_by_age/player_count_by_age


age_summary = pd.DataFrame({"Purchase Count":purchase_count_by_age,
                               "Average Spent":avg_spent_by_age,
                               "Total Spent":total_spent_by_age,
                               "Average Spent Per Person":avg_spent_per_person})
                               
print("-----------------------------------------------------------")
print(age_summary)


# Top Spenders

spenders = purchase_data.groupby("SN")

purchase_count_per_spender = spenders["SN"].count()
avg_value = spenders["Price"].mean()
total_value = spenders["Price"].sum()

spenders_summary = pd.DataFrame({"Purchase Count":purchase_count_per_spender,
                                "Average Purchase Price": avg_value,
                                "Total Purchase Value":total_value})



print("-----------------------------------------------------------")
print(spenders_summary.sort_values(by="Total Purchase Value", ascending=False).head())


# Most Popular Items

items_df = purchase_data[["Item ID","Item Name", "Price"]].copy()
items_df = items_df.groupby(["Item ID","Item Name"])

num_items_sold = items_df["Item Name"].count()
max_price_sold_per_item = items_df["Price"].max()
total_sum_per_item = items_df["Price"].sum()

items_summary = pd.DataFrame({"Purchase Count":num_items_sold,
                            "Item Price":max_price_sold_per_item,
                             "Total Purchase Value":total_sum_per_item})

print("-----------------------------------------------------------")
print(f'Most Popular Items:\n{items_summary.sort_values(by="Purchase Count", ascending=False).head()}')


# Most Profitable Items


print("-----------------------------------------------------------")
print(f'Most Profitable Items:\n{items_summary.sort_values(by="Total Purchase Value", ascending=False).head()}')


