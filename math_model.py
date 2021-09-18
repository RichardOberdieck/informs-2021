import gurobipy as gp
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def get_distance(df1: pd.DataFrame, df2: pd.DataFrame):
    """Calculates the distance between all elements of df1 and df2"""
    return {(df1.iloc[i].Name, df2.iloc[j].Name): 
            np.sqrt((df1.iloc[i].x - df2.iloc[j].x)**2 + (df1.iloc[i].y - df2.iloc[j].y)**2)
            for i in range(len(df1)) for j in range(len(df2))}

def read_data(file):
    factories = pd.read_excel('data.xlsx', 'Factories')
    warehouses = pd.read_excel('data.xlsx', 'Warehouses')
    customers = pd.read_excel('data.xlsx', 'Customers')

    d1 = get_distance(factories, warehouses)
    d2 = get_distance(warehouses, customers)
    distance = {**d1, **d2}

    factories.set_index('Name',inplace=True)
    warehouses.set_index('Name',inplace=True)
    customers.set_index('Name',inplace=True)

    return factories, warehouses, customers, distance


def solve(factories, warehouses, customers, distance):
    model = gp.Model()

    x = model.addVars(factories.index, warehouses.index, name='x')
    y = model.addVars(warehouses.index, customers.index, name='y')

    model.setObjective(x.prod(distance) + y.prod(distance))

    model.addConstrs((x.sum('*',w) == y.sum(w,'*') for w in warehouses.index), name='Ensure warehouse connection')
    model.addConstrs((y.sum('*',c) >= customers.Demand[c] for c in customers.index), name='Fulfill demand')
    model.addConstrs((x.sum('*',w) <= warehouses.Capacity[w] for w in warehouses.index), name='Respect capacity')
    model.addConstrs((x.sum(f, '*') <= factories.Supply[f] for f in factories.index), name='Respect supply')

    model.optimize()

    return {v: x[v].x for v in x}, {v: y[v].x for v in y}

def plot(factories, warehouses, customers, x, y):
    fig = px.scatter(pd.concat([factories, warehouses, customers]).reset_index(), x="x", y="y", text="Name", color="Type")
    fig.update_traces(textposition='top center')
    fig.update_layout(font_size=16)
    for v in x:
        if x[v] > 0:
            fig.add_trace(go.Scatter(x=[factories.loc[v[0]].x, warehouses.loc[v[1]].x],
                                y=[factories.loc[v[0]].y, warehouses.loc[v[1]].y],
                                        line=dict(color='royalblue', width=x[v] / 10), mode='lines', showlegend=False))

    for v in y:
        if y[v] > 0:
            fig.add_trace(go.Scatter(x=[warehouses.loc[v[0]].x, customers.loc[v[1]].x],
                                y=[warehouses.loc[v[0]].y, customers.loc[v[1]].y],
                                        line=dict(color='red', width=y[v] / 10), mode='lines', showlegend=False))

    return fig