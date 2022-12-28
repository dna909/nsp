# Subpages

You can configure entities with with the prefix `navigate`, that are navigating to cards, in case it's hidden card, the navigation items will change and the arrow is bringing you back to the previous page.

```yaml
          - entity: navigate.testKey
```

will allow you to navigate to a cardGrid page with the configured key testKey

```yaml
    hiddenCards:
      - type: cardGrid
        title: Exmaple Grid
        entities:
          - entity: light.test_item
        key: testKey
```

# Override Status of Navigation Items

You can override the status of navigation items, to make them look like different entities.

```yaml
          - entity: navigate.test
            status: climate.test
```
