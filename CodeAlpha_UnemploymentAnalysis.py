import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
sns.set_palette("muted")
plt.rcParams['figure.figsize'] = (10, 6)

# loading the dataset
df = pd.read_csv("Unemployment_in_india.csv")
print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum())
df.dropna(how='all', inplace=True)

# Data cleaning
df.columns = df.columns.str.strip()
df.rename(columns={"Estimated Unemployment Rate (%)": "unemployment_rate", 'Estimated Employed': 'employed', 'Estimated Labour Participation Rate (%)': 'labour_participation_rate'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'].str.strip(), dayfirst=True)
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month  

# Data analysis
# Unemployment rate over time   
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Date', y='unemployment_rate', marker='o')
plt.title('Unemployment Rate in India Over Time')
plt.xlabel('Date')
plt.ylabel('Unemployment Rate (%)')
plt.show()

#Covid-19 impact analysis
covid_period = df[df['Date'] >= '2020-01-01']
pre_covid_period = df[df['Date'] < '2020-01-01']
plt.figure(figsize=(14, 6))
sns.lineplot(data=pre_covid_period, x='Date', y='unemployment_rate', marker='o', label='Pre-COVID')
sns.lineplot(data=covid_period, x='Date', y='unemployment_rate', marker='o', label='COVID-19 Period', color='red')
plt.axvline(x=pd.to_datetime('2020-01-01'), color='gray', linestyle='--')
plt.axvspan(pd.to_datetime('2020-01-01'), df['Date'].max(), color='red', alpha=0.1)
peak=df.loc[df['unemployment_rate'].idxmax()]
plt.annotate(f'Peak: {peak["unemployment_rate"]:.2f}%',
              xy=(peak["Date"], peak["unemployment_rate"]),
              xytext=(peak["Date"], peak["unemployment_rate"] + 2),
              arrowprops=dict(color='black', arrowstyle='->', connectionstyle="arc3"), fontsize=10)

plt.grid(True,linestyle='--', alpha=0.5)
plt.title('Unemployment Rate in India During COVID-19 Pandemic')
plt.xlabel('Date')
plt.ylabel('Unemployment Rate (%)')
plt.legend()      
plt.savefig('unemployment_covid_impact.png', dpi=300)
plt.show()
print(df.columns.tolist())

# REGIONAL ANALYSIS 
plt.figure(figsize=(12, 6))
# FIXED
region_avg = df.groupby('Region')['unemployment_rate'].mean().sort_values(ascending=False).reset_index()
sns.barplot(data=region_avg, x='unemployment_rate', y='Region', hue='Region', palette='Reds_r', legend=False)
plt.title('Average Unemployment Rate by Region')
plt.xlabel('Average Unemployment Rate (%)')
plt.ylabel('Region')
plt.tight_layout()
plt.savefig('average_unemployment_by_region.png', dpi=300, bbox_inches='tight')
plt.show()

# RURAL vs URBAN ANALYSIS
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='Area', y='unemployment_rate', hue='Area', palette='Set2', legend=False)
plt.title('Unemployment Rate: Rural vs Urban')
plt.xlabel('Area')
plt.ylabel('Unemployment Rate (%)')
plt.savefig('unemployment_rural_urban.png', dpi=300, bbox_inches='tight')
plt.show()

# LABOUR PARTICIPATION RATE OVER TIME
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Date', y='labour_participation_rate', marker='o', color='green')
plt.title('Labour Participation Rate in India Over Time')
plt.xlabel('Date')
plt.ylabel('Labour Participation Rate (%)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('labour_participation_rate.png', dpi=300, bbox_inches='tight')
plt.show()

# CORRELATION ANALYSIS
plt.figure(figsize=(8, 6))
correlation = df[['unemployment_rate', 'employed', 'labour_participation_rate']].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Between Unemployment, Employment & Labour Participation')
plt.show()

# MONTHLY TREND
plt.figure(figsize=(12, 6))
monthly_avg = df.groupby('Month')['unemployment_rate'].mean().reindex(range(1, 13))
sns.barplot(data=monthly_avg, x='Month', y='unemployment_rate', hue='Month', palette='Blues_d', legend=False)
plt.title('Average Unemployment Rate by Month')
plt.xlabel('Month')
plt.ylabel('Average Unemployment Rate (%)')
plt.xticks(ticks=range(12), labels=['Jan','Feb','Mar','Apr','May','Jun',
                                     'Jul','Aug','Sep','Oct','Nov','Dec'])
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('monthly_unemployment_trend.png', dpi=300, bbox_inches='tight')
plt.show()
import os
print("Files saved in:", os.getcwd())

#SUMMARY STATISTICS
print("=" * 50)
print("UNEMPLOYMENT ANALYSIS SUMMARY")
print("=" * 50)
print(f"Overall Average Unemployment Rate: {df['unemployment_rate'].mean():.2f}%")
print(f"Highest Unemployment Rate: {df['unemployment_rate'].max():.2f}%")
print(f"Lowest Unemployment Rate: {df['unemployment_rate'].min():.2f}%")
print(f"\nRegion with Highest Avg Unemployment: {region_avg.index[0]}")
print(f"Region with Lowest Avg Unemployment: {region_avg.index[-1]}")