import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import altair as alt
from altair import pipe, limit_rows, to_values



def plot_nominal_column(column_name, 
                        df, 
                        include_na=True, 
                        percentage_limit=0, 
                        plot_type='bar', 
                        too_much_indices=True):
    '''
    Optional inputs
    
     - include_na:
        if True, keep NaN values as an index
        if False, drop NaN values
     - percentage_limit: 
         On the graph, if a represented index is considered
         to small (under percentage_limit), it is grouped in 
         the column 'other'.
     - plot_type:
         Can be 'bar' or 'pie'
    '''
    
    na_index = 'NaN'
    if include_na:
        column_data = df[column_name].fillna(na_index)
    else:
        column_data = df[column_name].dropna()
    
    ids = {}
    for index in column_data:
        try:
            ids[index] += 1
        except:
            ids[index] = 1

    size = len(column_data)
    id_to_del = []
    for index in ids:
        if ids[index] / size * 100 < percentage_limit:
            id_to_del.append(index)
    
    if len(id_to_del) > 0:
        ids['other'] = 0
        for index in id_to_del:
            ids['other'] += ids[index]
            del ids[index]
    
    # transform the dict into a list 
    # (to sort by nb of occurences so it's pretty to plot)
    item_list = list(ids.items())
    sorted_items = sorted(item_list, key=lambda x: x[1])
    x, y = [], []
    for item in sorted_items:
        x.append(item[0])
        y.append(item[1])
    
    # print info & graph
    print('-'*20)
    print(column_name)
    print('-'*20, '\n')

    nb_duplicates = column_data.duplicated().sum()
    nb_unique_values = len(column_data.unique())
    print('unique values :', nb_unique_values)
    print('duplicates :   ', nb_duplicates)
    
    plt.figure()
    plt.title('Distribution ' + column_name)
    if plot_type == 'pie':
        plt.pie(y, labels=x, autopct='%0.0f%%')
    elif plot_type == 'bar':
        plt.xlabel(column_name)
        plt.ylabel('count')
        if too_much_indices:
            plt.xticks(rotation=270)
        sns.barplot(x=x, y=y)
    plt.show()
    
    smallest_bar = x[0]
    smallest_nb_index = y[0]
    print(f'\nnb of index \'{smallest_bar}\':', (ids[smallest_bar]))


    
    
def plot_ordinal_column(column_name, 
                        ordinal_order, 
                        df, 
                        include_na=True, 
                        percentage_limit=0, 
                        plot_type='bar'):
    '''
    Optional inputs
    
     - include_na:
        if True, keep NaN values as an index
        if False, drop NaN values
     - percentage_limit: 
         On the graph, if a represented index is considered
         to small (under percentage_limit), it is grouped in 
         the column 'other'.
     - plot_type:
         Can be 'bar' or 'pie'

    '''
    
    na_index = 'NaN'
    if include_na:
        column_data = df[column_name].fillna(na_index)
        ordinal_order.append(na_index)
    else:
        column_data = df[column_name].dropna()
    
    ordinal_list = [[index, 0] for index in ordinal_order]
    
    ids = {}
    for index in column_data:
        try:
            ids[index] += 1
        except:
            ids[index] = 1
    
    #print(ids)

    size = len(column_data)
    id_to_del = []
    for index in ids:
        if ids[index] / size * 100 < percentage_limit:
            id_to_del.append(index)
    
    if len(id_to_del) > 0:
        ids['other'] = 0
        for index in id_to_del:
            ids['other'] += ids[index]
            del ids[index]
    
    # transform the dict into a list 
    # (to sort by ordinal order)
    sorted_items = ordinal_list
    for i, sub_list in enumerate(ordinal_list):
        index = sub_list[0]
        sorted_items[i][1] = ids[index]
    #sorted_items = sorted(item_list, key=lambda x: x[1])
    x, y = [], []
    for item in sorted_items:
        x.append(item[0])
        y.append(item[1])
    
    # print info & graph
    print('-'*20)
    print(column_name)
    print('-'*20, '\n')
    
    nb_duplicates = column_data.duplicated().sum()
    nb_unique_values = len(column_data.unique())
    print('unique values :', nb_unique_values)
    print('duplicates :   ', nb_duplicates)
    
    plt.title('Distribution ' + column_name)
    if plot_type == 'pie':
        plt.pie(y, labels=x, autopct='%0.0f%%')
    else:
        plt.xlabel(column_name)
        plt.ylabel('count')
        sns.barplot(x=x, y=y)
    
    smallest_bar = x[0]
    smallest_nb_index = y[0]
    print(f'\nnb of index \'{smallest_bar}\'=', (ids[smallest_bar]))
    
    return ids




def check_nb_and_tags_columns_1(nb_column, tags_column, df):
    res = True
    
    for nb_addi, addi_tags in zip(df['additives_n'], df['additives_tags']):
        if np.isnan(nb_addi) and not np.isnan(addi_tags):
            print('\n', nb_addi, '\n', addi_tags, '\n')
            res = False
            break
    return res




def check_nb_and_tags_columns_2(nb_column, tags_column, df):
    count = 0
    
    for nb_addi, addi_tags in zip(df['additives_n'], df['additives_tags']):
        if np.isnan(nb_addi) and not np.isnan(addi_tags):
            print('\n', nb_addi, '\n', addi_tags, '\n')
            count += 1
    return count




def get_column_types(column, df):
    type_list = []
    new_column = df[column].dropna()
    
    if new_column.shape[0] != df[column].shape[0]:
        type_list.append(np.nan)
        
    for i in range(new_column.shape[0]):
        type_value = type(new_column.iloc[i])
        if type_value not in type_list:
            type_list.append(type_value)
    return type_list





def correlation_matrix(columns, df, print_result=True):
    nb_rounding = 2
    
    corr = df[columns].corr()
    rounded_corr = np.round(corr, nb_rounding)
    mask = np.triu(np.ones_like(corr))
    
    if print_result:
        plt.figure()
        plt.title('Correlation matrix')
        sns.heatmap(rounded_corr, annot=True, mask=mask, cmap='coolwarm', vmin=-1, vmax=1)
        plt.show()
        
    return corr




def impute_zeros(column_group, wanted_sum_value, df, margin=0):
    # 'wanted_sum_value' can be a number or a 'df[column]'
    min_value = wanted_sum_value - margin
    max_value = wanted_sum_value + margin
    total = df[column_group].sum(axis=1)
    is_good = (min_value <= total) & (total <= max_value)
    
    for column in column_group:
        df[column][df[column].isna() & is_good] = 0
    
    return df



