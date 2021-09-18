# Minimizing transportation cost for wood planks

## Variables

- $x_{f,w} \geq 0$: the amount of transported material from factory $f$ to warehouse $w$.
- $y_{w,c} \geq 0$: the amount of transported material from warehouse $w$ to customer $c$.

## Minimize the transportation cost

$$\sum_{f,w} c_{f,w}x_{f,w} + \sum_{w,c} c_{w,c}y_{w,c}$$

## No storage in the warehouses, they are simply there for re-routing.

$$\sum_{f} x_{f,w} = \sum_{c} y_{w,c} \quad \quad \forall w$$

## The customer demand needs to be satisfied

$$\sum_w y_{w,c} \geq D_c \quad \quad \forall c$$

where $D_c$ is the demand of customer $c$.

## The warehouse capacity cannot be exceeded

$$\sum_f x_{f,w} \leq C_w \quad \quad \forall w$$

where $C_w$ is the capacity of the warehouse.

## The supply limits of the factories need to be respected

$$\sum_w x_{f,w} \leq S_f \quad \quad \forall f$$

where $S_f$ is the supply of factory f.