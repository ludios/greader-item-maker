CREATE TABLE feeds (
  encoded_url text CONSTRAINT encoded_url_pk PRIMARY KEY,
  feed_url text NOT NULL,
  url_encoding_method text NOT NULL,
  dont_download boolean NOT NULL,
  job_ids int[] NOT NULL
);

CREATE TABLE counters (
  name text CONSTRAINT name_pk PRIMARY KEY,
  count int NOT NULL
);

INSERT INTO counters (name, count) VALUES ('next_item_id', 0);
