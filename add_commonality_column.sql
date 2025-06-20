-- Add how_common column to diseases table
ALTER TABLE diseases ADD COLUMN how_common TEXT;

-- Update existing diseases with commonality information
UPDATE diseases SET how_common = 'Very common - affects millions annually, especially during cold and flu seasons' WHERE name = 'Common Cold';
UPDATE diseases SET how_common = 'Very common - one of the most frequent digestive complaints, affecting people of all ages' WHERE name = 'Gastroenteritis';
UPDATE diseases SET how_common = 'Common - affects about 12% of the global population, more frequent in developed countries' WHERE name = 'Migraine';
UPDATE diseases SET how_common = 'Very common - most people experience tension headaches occasionally, affecting up to 80% of adults' WHERE name = 'Tension Headache';
UPDATE diseases SET how_common = 'Common - affects 10-15% of the global population, more common in women' WHERE name = 'Irritable Bowel Syndrome';
UPDATE diseases SET how_common = 'Very common - millions of cases occur annually, especially from contaminated food or water' WHERE name = 'Food Poisoning';
UPDATE diseases SET how_common = 'Common - viral infections are among the most frequent reasons for medical visits' WHERE name = 'Viral Infection';
UPDATE diseases SET how_common = 'Common - affects millions during seasonal outbreaks, particularly in fall and winter' WHERE name = 'Influenza';
UPDATE diseases SET how_common = 'Very common - affects 10-20% of the population, more frequent in spring and fall' WHERE name = 'Allergic Rhinitis';
UPDATE diseases SET how_common = 'Common - affects 2-5% of adults and up to 20% of children worldwide' WHERE name = 'Eczema';
UPDATE diseases SET how_common = 'Common - most people experience muscle strains during physical activities or exercise' WHERE name = 'Muscle Strain';
UPDATE diseases SET how_common = 'Common - affects people of all ages, especially those exposed to irritants or allergens' WHERE name = 'Contact Dermatitis';
UPDATE diseases SET how_common = 'Moderately common - affects about 15-20% of people at some point in their lives' WHERE name = 'Vertigo';
UPDATE diseases SET how_common = 'Common - lactose intolerance alone affects 65% of adults worldwide' WHERE name = 'Food Intolerance';
UPDATE diseases SET how_common = 'Common - affects 5-10% of the population, more frequent in developed countries' WHERE name = 'Functional Dyspepsia';
UPDATE diseases SET how_common = 'Very common - nearly everyone experiences upper respiratory infections multiple times per year' WHERE name = 'Upper Respiratory Infection';
UPDATE diseases SET how_common = 'Common - affects millions annually, particularly those exposed to viruses or bacteria' WHERE name = 'Viral Gastritis';
UPDATE diseases SET how_common = 'Common - throat irritation affects most people occasionally due to various environmental factors' WHERE name = 'Throat Irritation';
UPDATE diseases SET how_common = 'Common - affects millions annually, often accompanying viral infections' WHERE name = 'Viral Pharyngitis';
UPDATE diseases SET how_common = 'Common - affects most people occasionally due to stress, poor posture, or tension' WHERE name = 'Stress Headache';
UPDATE diseases SET how_common = 'Common - joint pain affects millions, especially older adults and active individuals' WHERE name = 'Arthralgia';
UPDATE diseases SET how_common = 'Common - inflammatory conditions affect millions worldwide, varying by specific cause' WHERE name = 'Inflammatory Pain';
UPDATE diseases SET how_common = 'Common - mild viral infections are extremely frequent, especially in children and during seasonal changes' WHERE name = 'Mild Viral Infection';
UPDATE diseases SET how_common = 'Common - bacterial infections affect millions annually, ranging from minor to serious cases' WHERE name = 'Bacterial Infection';
UPDATE diseases SET how_common = 'Common - allergic reactions affect 20-30% of the population to various substances' WHERE name = 'Allergic Reaction';
UPDATE diseases SET how_common = 'Common - inner ear disorders affect millions, particularly older adults' WHERE name = 'Inner Ear Disorder';
UPDATE diseases SET how_common = 'Moderately common - affects about 5-10% of people, more frequent with age or head injuries' WHERE name = 'Vestibular Dysfunction';
UPDATE diseases SET how_common = 'Rare but increasing - affects less than 1% of population, often underdiagnosed' WHERE name = 'Chronic Fatigue';
UPDATE diseases SET how_common = 'Very common - sleep disorders affect 30-40% of adults at some point in their lives' WHERE name = 'Sleep Disorder';
UPDATE diseases SET how_common = 'Very common - viral illnesses are among the most frequent health complaints globally' WHERE name = 'General Viral Illness';
UPDATE diseases SET how_common = 'Very common - stress-related symptoms affect majority of adults in modern society' WHERE name = 'Stress-Related Symptoms';
UPDATE diseases SET how_common = 'Very common - minor acute illnesses affect everyone multiple times per year' WHERE name = 'Minor Acute Illness';
UPDATE diseases SET how_common = 'Very common - most people experience acute minor illnesses regularly' WHERE name = 'Acute Minor Illness';
UPDATE diseases SET how_common = 'Common - general malaise affects most people occasionally, often as early sign of illness' WHERE name = 'General Malaise';
UPDATE diseases SET how_common = 'Very common - stress responses are universal human experiences in modern life' WHERE name = 'Stress Response';
UPDATE diseases SET how_common = 'Very common - mild infections are frequent occurrences affecting people of all ages' WHERE name = 'Mild Infection';
