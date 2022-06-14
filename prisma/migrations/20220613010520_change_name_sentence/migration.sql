/*
  Warnings:

  - You are about to drop the `Sentences` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropTable
PRAGMA foreign_keys=off;
DROP TABLE "Sentences";
PRAGMA foreign_keys=on;

-- CreateTable
CREATE TABLE "Sentence" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "textId" INTEGER NOT NULL,
    "sentence" TEXT NOT NULL,
    "keywords" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "Sentence_textId_fkey" FOREIGN KEY ("textId") REFERENCES "Text" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
