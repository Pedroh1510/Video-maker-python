-- CreateTable
CREATE TABLE "Input" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "lenguage" TEXT NOT NULL,
    "searchTerm" TEXT NOT NULL,
    "prefix" TEXT NOT NULL,
    "maxSentences" INTEGER NOT NULL,
    "template" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- CreateTable
CREATE TABLE "Text" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "inputId" INTEGER NOT NULL,
    "origin" TEXT NOT NULL,
    "content" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "Text_inputId_fkey" FOREIGN KEY ("inputId") REFERENCES "Input" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "Sentences" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "textId" INTEGER NOT NULL,
    "sentence" TEXT NOT NULL,
    "keywords" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "Sentences_textId_fkey" FOREIGN KEY ("textId") REFERENCES "Text" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
