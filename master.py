import pandas as pd

datapath = 'data/'
df_orders = pd.read_csv(datapath + 'orders.csv')
df_order_items = pd.read_csv(datapath + 'order_items.csv', low_memory=False)
df_products = pd.read_csv(datapath + 'products.csv')
df_customers = pd.read_csv(datapath + 'customers.csv')
df_geography = pd.read_csv(datapath + 'geography.csv')
df_promotions = pd.read_csv(datapath + 'promotions.csv')
df_returns = pd.read_csv(datapath + 'returns.csv')

df_customers_geo = pd.merge(
    df_customers, 
    df_geography, 
    on='zip', 
    how='left'
)

df_orders_enriched = pd.merge(
    df_orders, 
    df_customers_geo, 
    on='customer_id', 
    how='left'
)

df_items_prod = pd.merge(
    df_order_items, 
    df_products, 
    on='product_id', 
    how='left'
)

df_items_prod_promo = pd.merge(
    df_items_prod, 
    df_promotions, 
    on='promo_id', 
    how='left'
)

df_master = pd.merge(
    df_items_prod_promo, 
    df_orders_enriched, 
    on='order_id', 
    how='left'
)

print(f"Số dòng của bảng Master: {df_master.shape[0]}")
print(f"Số cột của bảng Master: {df_master.shape[1]}")
df_master.head()

df_returns_agg = df_returns.groupby(['order_id', 'product_id']).agg({
    'return_quantity': 'sum',
    'refund_amount': 'sum'
}).reset_index()

df_master = pd.merge(df_master, df_returns_agg, on=['order_id', 'product_id'], how='left')

df_master['discount_amount'] = df_master['discount_amount'].fillna(0)

df_master['real_revenue'] = (df_master['quantity'] * df_master['unit_price']) - df_master['discount_amount']

df_master['total_cogs'] = df_master['quantity'] * df_master['cogs']

df_master['gross_profit'] = df_master['real_revenue'] - df_master['total_cogs']
df_master['margin_pct'] = (df_master['gross_profit'] / df_master['real_revenue']) * 100

df_master['order_date'] = pd.to_datetime(df_master['order_date'])
df_master['order_year'] = df_master['order_date'].dt.year
df_master['order_month'] = df_master['order_date'].dt.month

df_master.to_csv('master_data.csv', index=False)