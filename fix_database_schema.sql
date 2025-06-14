-- Add missing column if it doesn't exist
ALTER TABLE diseases ADD COLUMN IF NOT EXISTS how_common TEXT;

-- Update a few diseases with commonality info if the column is empty
UPDATE diseases SET how_common = 'Very common - affects millions annually, especially during cold and flu seasons' WHERE name = 'Common Cold' AND (how_common IS NULL OR how_common = '');
UPDATE diseases SET how_common = 'Very common - one of the most frequent digestive complaints, affecting people of all ages' WHERE name = 'Gastroenteritis' AND (how_common IS NULL OR how_common = '');
UPDATE diseases SET how_common = 'Common - affects about 12% of the global population, more frequent in developed countries' WHERE name = 'Migraine' AND (how_common IS NULL OR how_common = '');
UPDATE diseases SET how_common = 'Very common - most people experience tension headaches occasionally, affecting up to 80% of adults' WHERE name = 'Tension Headache' AND (how_common IS NULL OR how_common = '');
UPDATE diseases SET how_common = 'Common - affects 10-15% of the global population, more common in women' WHERE name = 'Irritable Bowel Syndrome' AND (how_common IS NULL OR how_common = '');
