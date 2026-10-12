# Slide layout patterns

Every wireframe assumes the same margins and one clear focal point. ASCII boxes stand in for the slide area.

## Title

```
+-------------------------------------+
|                                     |
|         PRESENTATION TITLE          |
|         Subtitle goes here          |
|                                     |
|         Presenter name              |
|         Date                        |
|                          [Logo]     |
+-------------------------------------+
```

## Big statement

```
+-------------------------------------+
|     "Key quote or big statement"    |
|                                     |
|                 Attribution         |
+-------------------------------------+
```

## Three columns

```
+-------------------------------------+
|           Section title             |
+-----------+-----------+-------------+
|  [Icon]   |  [Icon]   |  [Icon]     |
|  Point 1  |  Point 2  |  Point 3    |
|  Detail   |  Detail   |  Detail     |
+-----------+-----------+-------------+
```

## Image plus text

```
+-------------------------------------+
|   Full-height      |  Heading       |
|   image            |  - Point 1     |
|                    |  - Point 2     |
+-------------------------------------+
```

## Data highlight

```
+-------------------------------------+
|               85%                   |
|     Key metric description          |
|  [10K users] [25% growth] [#1 rank] |
+-------------------------------------+
```

## Timeline

```
+-------------------------------------+
|           Our journey               |
|  2020        2021        2022       |
|    o----------o----------o          |
|  Event 1   Event 2    Event 3       |
+-------------------------------------+
```

## Comparison

```
+-------------------------------------+
|           Before vs after           |
+-----------------+-------------------+
|     BEFORE      |      AFTER        |
|   [Visual]      |    [Visual]       |
|   - Problem 1   |    - Solution 1   |
+-----------------+-------------------+
```

## Process flow

```
+-------------------------------------+
|           How it works              |
|   [1] ---> [2] ---> [3]             |
|   Step 1   Step 2   Step 3          |
+-------------------------------------+
```

## Quote plus image

```
+-------------------------------------+
|   "Quote that        [Speaker       |
|    spans lines"       photo]        |
|   Speaker name, role                |
+-------------------------------------+
```

## Before and after rewrite

Text dump before:

```
Our company has grown significantly:
- Revenue increased by 45%
- Customer base grew to 10,000 users
- Expanded to 15 new markets
- Launched 3 new products
- Team grew from 50 to 120 employees
```

After: a data highlight slide titled "2024 growth highlights" with five stat tiles (+45% revenue, 10K users, 15 markets, 3 products, 120 team) and no bullet list.

## Example per-slide spec

```
Slide 4: Growth highlights
Type: data highlight
Text: title "2024 growth highlights" 28pt bold; five tiles, number 36pt bold, label 14pt caption
Visuals: five rounded tiles in one row; accent on the first tile
Colour: background token, primary text token, accent on +45%
Animation: tiles fade in left to right, 150ms each
```
