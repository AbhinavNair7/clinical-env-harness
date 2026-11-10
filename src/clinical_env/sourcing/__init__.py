"""Tools for building cases on open case reports (docs/case-sourcing.md).

Search and fetch from Europe PMC, keep only CC BY or CC0 articles (checked in each article's
own full-text XML), and check a drafted case against its source: no shared 8-word runs, and
the source is not found by searching the case's most distinctive details.
"""
