CREATE TABLE feeds (
  encoded_url text CONSTRAINT encoded_url_pk PRIMARY KEY,
  feed_url text NOT NULL,
  url_encoding_method text NOT NULL,
  dont_download boolean NOT NULL,
  job_ids int[] NOT NULL
);

-- "this doesn't actually index individual array values, but instead indexes the entire array"
-- http://stackoverflow.com/questions/4058731/can-postgresql-index-array-columns
-- Confirmed to speed up job_ids = '{2}' and job_ids = '{}' queries.
-- (Note: if LIMIT is used, must ORDER BY encoded_url)
CREATE INDEX job_ids_idx ON feeds USING GIN ("job_ids");

CREATE TABLE counters (
  name text CONSTRAINT name_pk PRIMARY KEY,
  count int NOT NULL
);

INSERT INTO counters (name, count) VALUES ('next_item_id', 0);
