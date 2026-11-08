# Babson Bean Café Database

## 1. The Scenario

Scenario C: Babson Bean Café. Babson Bean is an on-campus café whose till records sales, but its loyalty punch cards can't answer questions. This database tracks loyalty members, the menu, add-on options, orders, order lines, the options on each line, and payments, so the café can see what sells, which add-ons earn their keep, and who its regular customers are.

## 2. The ERD

```mermaid
erDiagram
    members |o--o{ orders : places
    orders ||--|{ order_lines : contains
    products ||--o{ order_lines : "sold on"
    order_lines ||--o{ line_options : carries
    options ||--o{ line_options : "added as"
    orders ||--|{ payments : "paid by"

    members {
        int member_id PK
        varchar first_name
        varchar mobile "unique, can change"
        varchar email "optional"
        date join_date
        int points_balance
    }
    products {
        int product_id PK
        varchar name
        varchar category "coffee, tea, food, other"
        decimal price "never below cost"
        decimal cost
        boolean available_today
    }
    options {
        int option_id PK
        varchar name
        decimal price "can be zero"
        decimal cost
    }
    orders {
        int order_id PK
        timestamp ordered_at
        int member_id FK "optional, null for non-members"
        varchar channel "counter or app"
    }
    order_lines {
        int line_id PK
        int order_id FK
        int product_id FK
        int quantity "greater than zero"
        decimal unit_price "price charged that day"
    }
    line_options {
        int line_id PK, FK
        int option_id PK, FK
        decimal price_charged "per unit, price that day"
    }
    payments {
        int payment_id PK
        int order_id FK
        varchar method "cash, card, app, points"
        decimal amount "greater than zero"
    }
```

## 3. What One Row Means

- `members`: One person who joined the loyalty program
- `products`: One item on the menu, like a latte or a muffin 
- `options`: One add-on the café offers, like oat milk or an extra shot, with its price and cost
- `orders`: One purchase at one moment, by a member or a non-member
- `order_lines`: One product within one order
- `line_options`: One add-on applied to one line, e.g. oat milk on that 2-latte line
- `payments`: One payment toward one order, an amount paid by one method

## 4. Design Choices

