-- CreateTable
CREATE TABLE "Blacklist" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "url" TEXT NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "Blacklist_url_key" ON "Blacklist"("url");
