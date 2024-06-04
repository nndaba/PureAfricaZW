[FIX]category install issue: 08/06/23(1.0.0 -> 1.1.0)

Used post_init_hook to fetch data from DB and write fetched data into the pos category m2m field.

[FIX]available in pos product with no category not showing in POS : 08/06/23(1.1.0-> 1.1.1)

Updated condition in ternary operator when a product has no category to fix the issue.