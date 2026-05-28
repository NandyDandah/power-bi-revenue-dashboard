CREATE SCHEMA IF NOT EXISTS public;

DROP TABLE IF EXISTS public.sales_activities CASCADE;
DROP TABLE IF EXISTS public.orders CASCADE;
DROP TABLE IF EXISTS public.opportunities CASCADE;
DROP TABLE IF EXISTS public.products CASCADE;
DROP TABLE IF EXISTS public.customers CASCADE;
DROP TABLE IF EXISTS public.sales_reps CASCADE;

CREATE TABLE public.customers (
    customer_id integer PRIMARY KEY,
    customer_name varchar(120) NOT NULL,
    segment varchar(50) NOT NULL,
    region varchar(50) NOT NULL,
    signup_date date NOT NULL
);

CREATE TABLE public.products (
    product_id integer PRIMARY KEY,
    product_name varchar(120) NOT NULL,
    category varchar(80) NOT NULL,
    unit_price numeric(12, 2) NOT NULL
);

CREATE TABLE public.sales_reps (
    rep_id integer PRIMARY KEY,
    rep_name varchar(120) NOT NULL,
    team varchar(80) NOT NULL,
    region varchar(50) NOT NULL
);

CREATE TABLE public.orders (
    order_id integer PRIMARY KEY,
    customer_id integer NOT NULL REFERENCES public.customers(customer_id),
    product_id integer NOT NULL REFERENCES public.products(product_id),
    rep_id integer NOT NULL REFERENCES public.sales_reps(rep_id),
    order_date date NOT NULL,
    quantity integer NOT NULL,
    discount numeric(5, 4) NOT NULL DEFAULT 0,
    revenue numeric(14, 2) NOT NULL
);

CREATE TABLE public.opportunities (
    opportunity_id integer PRIMARY KEY,
    customer_id integer NOT NULL REFERENCES public.customers(customer_id),
    rep_id integer NOT NULL REFERENCES public.sales_reps(rep_id),
    created_date date NOT NULL,
    stage varchar(50) NOT NULL,
    estimated_value numeric(14, 2) NOT NULL,
    is_won boolean NOT NULL DEFAULT false
);

CREATE TABLE public.sales_activities (
    activity_id integer PRIMARY KEY,
    opportunity_id integer NOT NULL REFERENCES public.opportunities(opportunity_id),
    activity_date date NOT NULL,
    activity_type varchar(60) NOT NULL
);

CREATE INDEX idx_orders_order_date ON public.orders(order_date);
CREATE INDEX idx_orders_rep_id ON public.orders(rep_id);
CREATE INDEX idx_orders_customer_id ON public.orders(customer_id);
CREATE INDEX idx_opportunities_stage ON public.opportunities(stage);
CREATE INDEX idx_opportunities_rep_id ON public.opportunities(rep_id);
CREATE INDEX idx_sales_activities_opportunity_id ON public.sales_activities(opportunity_id);
