/*
  Warnings:

  - A unique constraint covering the columns `[searchTerm]` on the table `Input` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[inputId]` on the table `Text` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX "Input_searchTerm_key" ON "Input"("searchTerm");

-- CreateIndex
CREATE UNIQUE INDEX "Text_inputId_key" ON "Text"("inputId");
