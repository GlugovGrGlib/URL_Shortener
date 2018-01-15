BEGIN;
--
-- Create model Urls
--
CREATE TABLE "urlapp_urls" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "url" varchar(2000) NOT NULL, "short_url" varchar(100) NOT NULL, "text_message" varchar(2000) NOT NULL, "click_count" integer NOT NULL, "add_date" datetime NOT NULL);
COMMIT;
