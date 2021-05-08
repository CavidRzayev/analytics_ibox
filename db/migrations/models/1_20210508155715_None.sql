-- upgrade --
CREATE TABLE IF NOT EXISTS "defaultmodel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "type" VARCHAR(50),
    "status" VARCHAR(50),
    "status_message" VARCHAR(150),
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "description" TEXT,
    "shop_id" INT
);
CREATE TABLE IF NOT EXISTS "socket_logging" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "type" VARCHAR(50),
    "message" VARCHAR(1000),
    "content" TEXT,
    "status" VARCHAR(100),
    "timestamp" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "order" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "type" VARCHAR(50),
    "status" VARCHAR(50),
    "status_message" VARCHAR(150),
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "description" TEXT,
    "shop_id" INT,
    "order_id" INT,
    "payment_id" INT,
    "user_id" INT,
    "merchant_id" INT,
    "courier_id" INT,
    "point" INT   DEFAULT 1,
    "payment_status" INT,
    "payment_method" INT,
    "is_active" BOOL NOT NULL  DEFAULT True
);
CREATE INDEX IF NOT EXISTS "idx_order_order_i_b22a58" ON "order" ("order_id", "payment_id");
CREATE TABLE IF NOT EXISTS "socket_payment" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "type" VARCHAR(50),
    "status" VARCHAR(50),
    "status_message" VARCHAR(150),
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "description" TEXT,
    "shop_id" INT,
    "order_id" INT NOT NULL REFERENCES "order" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
