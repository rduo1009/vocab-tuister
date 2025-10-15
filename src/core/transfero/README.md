# Data files

The wordnet database at `wn.db.zst` was created by:

- running `import src` to download `wn.db`
- running following after `sqlite3` to remove unneeded tables

```sql
.open src/core/transfero/wn_data/wn.db

DELETE FROM definitions;
DELETE FROM sense_examples;
DELETE FROM synset_examples;
DELETE FROM counts;
DELETE FROM lexfiles;
DELETE FROM pronunciations;
DELETE FROM adjpositions;
DELETE FROM syntactic_behaviours;
DELETE FROM syntactic_behaviour_senses;
DELETE FROM tags;
DELETE FROM ilis;
DELETE FROM ili_statuses;
DELETE FROM proposed_ilis;

VACUUM;
```

- running `zstd -19 src/core/transfero/wn_data/wn.db` to compress
